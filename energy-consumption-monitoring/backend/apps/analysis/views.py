from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.core.cache import cache
from django.db.models import Avg, Count, F, IntegerField, Q, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Func
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.alarms.models import Alarm, AlarmStatus
from apps.accounts.models import UserProfile
from apps.analysis.models import Achievement, EnergyForecast, ForecastTargetType, UserAchievement
from apps.analysis.serializers import (
    AchievementSerializer,
    BaseAnalysisQuerySerializer,
    ComparisonQuerySerializer,
    DistributionQuerySerializer,
    ForecastQuerySerializer,
    HourlyDistributionQuerySerializer,
    RankingQuerySerializer,
    RealTimePowerQuerySerializer,
    TrendQuerySerializer,
    UserAchievementSerializer,
)
from apps.buildings.models import Room
from apps.devices.models import Device
from apps.energy.models import EnergyData, EnergyStatistics, PeriodType
from energy_monitoring.permissions import IsAdmin, is_admin_user


def _day_range(target_date: date):
    tz = timezone.get_current_timezone()
    start = timezone.make_aware(datetime.combine(target_date, time.min), tz)
    end = timezone.make_aware(datetime.combine(target_date, time.max), tz)
    return start, end


def _month_range(target_date: date):
    first_day = target_date.replace(day=1)
    if first_day.month == 12:
        next_month = first_day.replace(year=first_day.year + 1, month=1)
    else:
        next_month = first_day.replace(month=first_day.month + 1)
    last_day = next_month - timedelta(days=1)
    return _day_range(first_day)[0], _day_range(last_day)[1]


def _year_range(target_date: date):
    first_day = target_date.replace(month=1, day=1)
    last_day = target_date.replace(month=12, day=31)
    return _day_range(first_day)[0], _day_range(last_day)[1]


def _shift_year(target_date: date, years: int):
    try:
        return target_date.replace(year=target_date.year + years)
    except ValueError:
        # handle Feb 29
        return target_date.replace(month=2, day=28, year=target_date.year + years)


def _safe_rate(current_value, previous_value):
    if not previous_value:
        return None
    return (float(current_value) - float(previous_value)) / float(previous_value) * 100


def _ensure_aware_datetime(value: datetime | None):
    if value is None:
        return None
    if timezone.is_naive(value):
        return timezone.make_aware(value, timezone.get_current_timezone())
    return value


DEFAULT_ACHIEVEMENTS = [
    {
        "code": "ENERGY_PIONEER",
        "name": "Energy Pioneer",
        "description": "Keep monthly usage below your peer average for 3 months.",
        "icon": "flash",
        "points": 20,
        "sort_order": 10,
    },
    {
        "code": "WATER_SAVER",
        "name": "Water Saver",
        "description": "Reduce water usage by 10% over last month.",
        "icon": "drop",
        "points": 15,
        "sort_order": 20,
    },
    {
        "code": "LOW_CARBON",
        "name": "Low Carbon",
        "description": "Cut estimated carbon emissions by 50kg.",
        "icon": "leaf",
        "points": 20,
        "sort_order": 30,
    },
    {
        "code": "MONTHLY_TOP10",
        "name": "Monthly Top 10",
        "description": "Enter top 10 in monthly energy-saving ranking.",
        "icon": "trophy",
        "points": 25,
        "sort_order": 40,
    },
    {
        "code": "HUNDRED_DAYS",
        "name": "100-Day Streak",
        "description": "Submit valid usage records for 100 consecutive days.",
        "icon": "calendar",
        "points": 30,
        "sort_order": 50,
    },
    {
        "code": "ENERGY_STEWARD",
        "name": "Energy Steward",
        "description": "Bind 3 rooms and keep all with no overdue alarms.",
        "icon": "shield",
        "points": 18,
        "sort_order": 60,
    },
]

ENERGY_PRICE_MAP = {
    "ELECTRICITY": Decimal("0.85"),
    "WATER": Decimal("3.00"),
    "GAS": Decimal("2.50"),
}

CARBON_FACTOR_MAP = {
    "ELECTRICITY": Decimal("0.57"),
    "WATER": Decimal("0.20"),
    "GAS": Decimal("2.02"),
}


class AnalysisEmptySerializer(serializers.Serializer):
    """用于 schema 推断的占位序列化器。"""


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all().order_by("sort_order", "id")
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def _ensure_default_achievements(self):
        if Achievement.objects.exists():
            return
        Achievement.objects.bulk_create([Achievement(**item) for item in DEFAULT_ACHIEVEMENTS], ignore_conflicts=True)

    def _get_user_achievement_rows(self, user, achievements):
        achievement_ids = [item.id for item in achievements]
        existing_rows = {
            row.achievement_id: row
            for row in UserAchievement.objects.filter(user=user, achievement_id__in=achievement_ids)
        }
        rows = []
        to_create = []
        for achievement in achievements:
            row = existing_rows.get(achievement.id)
            if row is None:
                row = UserAchievement(
                    user=user,
                    achievement=achievement,
                    unlocked=False,
                    progress=Decimal("0.00"),
                )
                to_create.append(row)
            rows.append(row)
        if to_create:
            UserAchievement.objects.bulk_create(to_create, ignore_conflicts=True)
            rows = list(
                UserAchievement.objects.select_related("achievement")
                .filter(user=user, achievement_id__in=achievement_ids)
                .order_by("achievement__sort_order", "achievement_id")
            )
        return rows

    def list(self, request, *args, **kwargs):
        self._ensure_default_achievements()
        queryset = self.get_queryset()
        if not is_admin_user(request.user):
            queryset = queryset.filter(is_active=True)
        achievements = list(queryset)
        rows = self._get_user_achievement_rows(request.user, achievements)
        serializer = UserAchievementSerializer(rows, many=True)
        unlocked_count = sum(1 for row in rows if row.unlocked)
        return Response(
            {
                "items": serializer.data,
                "summary": {
                    "total": len(rows),
                    "unlocked": unlocked_count,
                    "locked": len(rows) - unlocked_count,
                },
            }
        )

    @action(detail=False, methods=["get"], url_path="definitions", permission_classes=[IsAdmin])
    def definitions(self, request):
        serializer = AchievementSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class AnalysisViewSet(viewsets.GenericViewSet):
    """统计分析与预测接口。"""

    permission_classes = [IsAuthenticated]
    queryset = EnergyData.objects.none()
    serializer_class = AnalysisEmptySerializer

    def _validate_query(self, serializer_class):
        serializer = serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _apply_common_filters(self, queryset, params):
        device_tokens = [item.strip() for item in str(params.get("device_id", "")).split(",") if item.strip()]
        if device_tokens:
            device_ids = [int(item) for item in device_tokens if item.isdigit()]
            device_codes = [item for item in device_tokens if not item.isdigit()]
            query = Q()
            if device_ids:
                query |= Q(device_id__in=device_ids)
            if device_codes:
                query |= Q(device__device_id__in=device_codes)
            queryset = queryset.filter(query)

        energy_type = params.get("energy_type")
        if energy_type:
            if str(energy_type).isdigit():
                queryset = queryset.filter(energy_type_id=int(energy_type))
            else:
                queryset = queryset.filter(energy_type__code__iexact=str(energy_type).strip())

        campus_id = params.get("campus_id")
        if campus_id:
            queryset = queryset.filter(device__room__floor__building__campus_id=campus_id)

        building_id = params.get("building_id")
        if building_id:
            queryset = queryset.filter(device__room__floor__building_id=building_id)

        room_id = params.get("room_id")
        if room_id:
            queryset = queryset.filter(device__room_id=room_id)

        start_date = params.get("start_date")
        if start_date:
            queryset = queryset.filter(timestamp__gte=_day_range(start_date)[0])

        end_date = params.get("end_date")
        if end_date:
            queryset = queryset.filter(timestamp__lte=_day_range(end_date)[1])

        if not is_admin_user(self.request.user):
            room_ids = self._bound_room_ids()
            if room_ids:
                queryset = queryset.filter(device__room_id__in=room_ids)
            else:
                queryset = queryset.none()

        return queryset

    def _period_type_by_granularity(self, period: str):
        return {
            "day": PeriodType.DAY,
            "month": PeriodType.MONTH,
            "year": PeriodType.YEAR,
        }.get(period, PeriodType.DAY)

    def _apply_statistics_filters(self, queryset, params, period_type: str):
        queryset = queryset.filter(period_type=period_type)

        device_tokens = [item.strip() for item in str(params.get("device_id", "")).split(",") if item.strip()]
        if device_tokens:
            device_ids = [int(item) for item in device_tokens if item.isdigit()]
            device_codes = [item for item in device_tokens if not item.isdigit()]
            query = Q()
            if device_ids:
                query |= Q(device_id__in=device_ids)
            if device_codes:
                query |= Q(device__device_id__in=device_codes)
            queryset = queryset.filter(query)

        energy_type = params.get("energy_type")
        if energy_type:
            if str(energy_type).isdigit():
                queryset = queryset.filter(energy_type_id=int(energy_type))
            else:
                queryset = queryset.filter(energy_type__code__iexact=str(energy_type).strip())

        campus_id = params.get("campus_id")
        if campus_id:
            queryset = queryset.filter(device__room__floor__building__campus_id=campus_id)

        building_id = params.get("building_id")
        if building_id:
            queryset = queryset.filter(device__room__floor__building_id=building_id)

        room_id = params.get("room_id")
        if room_id:
            queryset = queryset.filter(device__room_id=room_id)

        start_date = params.get("start_date")
        if start_date:
            queryset = queryset.filter(period_date__gte=start_date)

        end_date = params.get("end_date")
        if end_date:
            queryset = queryset.filter(period_date__lte=end_date)

        if not is_admin_user(self.request.user):
            room_ids = self._bound_room_ids()
            if room_ids:
                queryset = queryset.filter(device__room_id__in=room_ids)
            else:
                queryset = queryset.none()

        return queryset

    def _apply_alarm_filters(self, queryset, params):
        device_tokens = [item.strip() for item in str(params.get("device_id", "")).split(",") if item.strip()]
        if device_tokens:
            device_ids = [int(item) for item in device_tokens if item.isdigit()]
            device_codes = [item for item in device_tokens if not item.isdigit()]
            query = Q()
            if device_ids:
                query |= Q(device_id__in=device_ids)
            if device_codes:
                query |= Q(device__device_id__in=device_codes)
            queryset = queryset.filter(query)

        energy_type = params.get("energy_type")
        if energy_type:
            if str(energy_type).isdigit():
                queryset = queryset.filter(device__energy_type_id=int(energy_type))
            else:
                queryset = queryset.filter(device__energy_type__code__iexact=str(energy_type).strip())

        campus_id = params.get("campus_id")
        if campus_id:
            queryset = queryset.filter(device__room__floor__building__campus_id=campus_id)

        building_id = params.get("building_id")
        if building_id:
            queryset = queryset.filter(device__room__floor__building_id=building_id)

        room_id = params.get("room_id")
        if room_id:
            queryset = queryset.filter(device__room_id=room_id)

        start_date = params.get("start_date")
        if start_date:
            queryset = queryset.filter(alarm_time__gte=_day_range(start_date)[0])

        end_date = params.get("end_date")
        if end_date:
            queryset = queryset.filter(alarm_time__lte=_day_range(end_date)[1])

        if not is_admin_user(self.request.user):
            room_ids = self._bound_room_ids()
            if room_ids:
                queryset = queryset.filter(device__room_id__in=room_ids)
            else:
                queryset = queryset.none()

        return queryset

    def _bound_room_ids(self):
        profile = getattr(self.request.user, "profile", None)
        if profile is None:
            profile, _ = UserProfile.objects.get_or_create(user=self.request.user, defaults={"bind_rooms": []})
        return [int(item) for item in profile.bind_rooms if str(item).isdigit()]

    def _my_target(self, ranking_type: str):
        room_ids = self._bound_room_ids()
        if not room_ids:
            return None
        room = (
            Room.objects.select_related("floor", "floor__building")
            .filter(id__in=room_ids)
            .order_by("id")
            .first()
        )
        if room is None:
            return None
        if ranking_type == "room":
            return str(room.id)
        if ranking_type == "building":
            return str(room.floor.building_id)
        return str(room.department or "UNKNOWN")

    def _comparison_ranges(self, period: str, anchor_date: date):
        if period == "day":
            current_start, current_end = _day_range(anchor_date)
            previous_start, previous_end = _day_range(anchor_date - timedelta(days=1))
            yoy_start, yoy_end = _day_range(_shift_year(anchor_date, -1))
        elif period == "month":
            current_start, current_end = _month_range(anchor_date)
            previous_anchor = anchor_date.replace(day=1) - timedelta(days=1)
            previous_start, previous_end = _month_range(previous_anchor)
            yoy_start, yoy_end = _month_range(_shift_year(anchor_date, -1))
        else:
            current_start, current_end = _year_range(anchor_date)
            previous_anchor = _shift_year(anchor_date, -1)
            previous_start, previous_end = _year_range(previous_anchor)
            yoy_start, yoy_end = _year_range(_shift_year(anchor_date, -1))
        return (
            (current_start, current_end),
            (previous_start, previous_end),
            (yoy_start, yoy_end),
        )

    def _comparison_summary_payload(self, stats_queryset, period: str, anchor_date: date):
        (current_start, current_end), (previous_start, previous_end), (yoy_start, yoy_end) = self._comparison_ranges(
            period,
            anchor_date,
        )
        current_total = stats_queryset.filter(
            period_date__gte=current_start.date(),
            period_date__lte=current_end.date(),
        ).aggregate(total=Sum("total_value"))["total"] or 0
        previous_total = stats_queryset.filter(
            period_date__gte=previous_start.date(),
            period_date__lte=previous_end.date(),
        ).aggregate(total=Sum("total_value"))["total"] or 0
        yoy_total = stats_queryset.filter(
            period_date__gte=yoy_start.date(),
            period_date__lte=yoy_end.date(),
        ).aggregate(total=Sum("total_value"))["total"] or 0
        return {
            "period": period,
            "anchor_date": anchor_date.isoformat(),
            "current_total": current_total,
            "chain_total": previous_total,
            "yoy_total": yoy_total,
            "chain_change_rate": _safe_rate(current_total, previous_total),
            "yoy_change_rate": _safe_rate(current_total, yoy_total),
            "current_range": [current_start.date().isoformat(), current_end.date().isoformat()],
            "chain_range": [previous_start.date().isoformat(), previous_end.date().isoformat()],
            "yoy_range": [yoy_start.date().isoformat(), yoy_end.date().isoformat()],
        }

    @action(detail=False, methods=["get"], url_path="dashboard")
    @extend_schema(
        summary="获取综合监控概览",
        parameters=[BaseAnalysisQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def dashboard(self, request):
        """返回能耗总览、覆盖率和告警统计。"""
        params = self._validate_query(BaseAnalysisQuerySerializer)

        # Generate cache key based on filters
        cache_key = (
            f"dashboard:"
            f"{params.get('campus_id') or 'all'}:"
            f"{params.get('building_id') or 'all'}:"
            f"{params.get('room_id') or 'all'}:"
            f"{params.get('energy_type') or 'all'}:"
            f"{params.get('device_id') or 'all'}"
        )
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        stats_queryset = self._apply_statistics_filters(
            EnergyStatistics.objects.select_related("energy_type", "device"),
            params,
            PeriodType.DAY,
        )

        totals = stats_queryset.values(
            "energy_type__code",
            "energy_type__name",
            "energy_type__unit",
        ).annotate(
            total_value=Sum("total_value"),
        ).order_by("energy_type__code")

        overall = stats_queryset.aggregate(
            total_value=Sum("total_value"),
            avg_power=Avg("avg_value"),
            records=Count("id"),
        )

        total_devices = Device.objects.count()
        covered_devices = stats_queryset.values("device_id").distinct().count()
        coverage_rate = (covered_devices / total_devices * 100) if total_devices else 0

        alarm_queryset = Alarm.objects.select_related("device")
        alarm_queryset = self._apply_alarm_filters(alarm_queryset, params)
        today_start = _day_range(timezone.localdate())[0]
        alarm_stats = alarm_queryset.aggregate(
            total=Count("id"),
            pending=Count("id", filter=Q(status=AlarmStatus.PENDING)),
            processed=Count("id", filter=Q(status=AlarmStatus.PROCESSED)),
            ignored=Count("id", filter=Q(status=AlarmStatus.IGNORED)),
            today=Count("id", filter=Q(alarm_time__gte=today_start)),
        )

        payload = {
            "summary": {
                "total_energy": overall["total_value"] or 0,
                "average_power": overall["avg_power"] or 0,
                "data_coverage_rate": round(coverage_rate, 2),
                "total_records": overall["records"],
                "devices_with_data": covered_devices,
                "devices_total": total_devices,
            },
            "energy_totals": list(totals),
            "alarm_statistics": alarm_stats,
        }
        # Cache for 30 seconds
        cache.set(cache_key, payload, timeout=30)
        return Response(payload)

    @action(detail=False, methods=["get"], url_path="trend")
    @extend_schema(
        summary="获取能耗趋势",
        parameters=[TrendQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def trend(self, request):
        """按日/月/年粒度返回趋势序列。"""
        params = self._validate_query(TrendQuerySerializer)
        period = params["period"]

        stats_queryset = self._apply_statistics_filters(
            EnergyStatistics.objects.select_related("device", "energy_type"),
            params,
            PeriodType.DAY,
        )

        if period == "day":
            rows = (
                stats_queryset.values("period_date")
                .annotate(
                    total_value=Sum("total_value"),
                    avg_power=Avg("avg_value"),
                    records=Count("id"),
                )
                .order_by("period_date")
            )
            series = [
                {
                    "period": row["period_date"].isoformat() if row["period_date"] else None,
                    "total_value": row["total_value"] or 0,
                    "avg_power": row["avg_power"] or 0,
                    "records": row["records"],
                }
                for row in rows
            ]
        elif period == "month":
            rows = (
                stats_queryset.annotate(bucket=TruncMonth("period_date"))
                .values("bucket")
                .annotate(
                    total_value=Sum("total_value"),
                    avg_power=Avg("avg_value"),
                    records=Count("id"),
                )
                .order_by("bucket")
            )
            series = [
                {
                    "period": row["bucket"].strftime("%Y-%m") if row["bucket"] else None,
                    "total_value": row["total_value"] or 0,
                    "avg_power": row["avg_power"] or 0,
                    "records": row["records"],
                }
                for row in rows
            ]
        else:  # year
            rows = (
                stats_queryset.annotate(bucket=TruncYear("period_date"))
                .values("bucket")
                .annotate(
                    total_value=Sum("total_value"),
                    avg_power=Avg("avg_value"),
                    records=Count("id"),
                )
                .order_by("bucket")
            )
            series = [
                {
                    "period": row["bucket"].strftime("%Y") if row["bucket"] else None,
                    "total_value": row["total_value"] or 0,
                    "avg_power": row["avg_power"] or 0,
                    "records": row["records"],
                }
                for row in rows
            ]

        return Response({"period": period, "series": series})

    @action(detail=False, methods=["get"], url_path="distribution")
    @extend_schema(
        summary="获取能耗分布",
        parameters=[DistributionQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def distribution(self, request):
        """按区域或能源类型返回能耗占比分布（使用预聚合统计数据）。"""
        params = self._validate_query(DistributionQuerySerializer)
        distribution_type = params["type"]
        period = params.get("period", "month")

        # 将 period 转换为 PeriodType
        period_type_map = {
            "day": PeriodType.DAY,
            "month": PeriodType.MONTH,
            "year": PeriodType.YEAR,
        }
        period_type = period_type_map.get(period, PeriodType.MONTH)

        # 使用预聚合的 EnergyStatistics 表查询
        stats_queryset = EnergyStatistics.objects.select_related(
            "device", "device__room", "device__room__floor", "device__room__floor__building", "energy_type"
        ).filter(period_type=period_type)

        # 应用时间范围过滤
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        if start_date:
            stats_queryset = stats_queryset.filter(period_date__gte=start_date)
        if end_date:
            stats_queryset = stats_queryset.filter(period_date__lte=end_date)

        # 应用其他过滤条件
        device_tokens = [item.strip() for item in str(params.get("device_id", "")).split(",") if item.strip()]
        if device_tokens:
            device_ids = [int(item) for item in device_tokens if item.isdigit()]
            device_codes = [item for item in device_tokens if not item.isdigit()]
            query = Q()
            if device_ids:
                query |= Q(device_id__in=device_ids)
            if device_codes:
                query |= Q(device__device_id__in=device_codes)
            stats_queryset = stats_queryset.filter(query)

        energy_type = params.get("energy_type")
        if energy_type:
            if str(energy_type).isdigit():
                stats_queryset = stats_queryset.filter(energy_type_id=int(energy_type))
            else:
                stats_queryset = stats_queryset.filter(energy_type__code__iexact=str(energy_type).strip())

        campus_id = params.get("campus_id")
        if campus_id:
            stats_queryset = stats_queryset.filter(device__room__floor__building__campus_id=campus_id)

        building_id = params.get("building_id")
        if building_id:
            stats_queryset = stats_queryset.filter(device__room__floor__building_id=building_id)

        room_id = params.get("room_id")
        if room_id:
            stats_queryset = stats_queryset.filter(device__room_id=room_id)

        # 权限过滤
        if not is_admin_user(self.request.user):
            room_ids = self._bound_room_ids()
            if room_ids:
                stats_queryset = stats_queryset.filter(device__room_id__in=room_ids)
            else:
                stats_queryset = stats_queryset.none()

        if distribution_type == "area":
            rows = (
                stats_queryset
                .values("device__room__floor__building__area_type")
                .annotate(total_value=Sum("total_value"))
                .order_by("-total_value")
            )
            data = [
                {
                    "name": row["device__room__floor__building__area_type"] or "UNKNOWN",
                    "value": float(row["total_value"] or 0),
                }
                for row in rows
            ]
        else:
            rows = (
                stats_queryset
                .values("energy_type__code", "energy_type__name")
                .annotate(total_value=Sum("total_value"))
                .order_by("-total_value")
            )
            data = [
                {
                    "name": row["energy_type__code"],
                    "label": row["energy_type__name"],
                    "value": float(row["total_value"] or 0),
                }
                for row in rows
            ]

        return Response({"type": distribution_type, "items": data})

    @action(detail=False, methods=["get"], url_path="ranking")
    @extend_schema(
        summary="获取能耗排名",
        parameters=[RankingQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def ranking(self, request):
        """按楼宇/房间/部门返回能耗 TopN 排名。"""
        params = self._validate_query(RankingQuerySerializer)
        ranking_type = params["type"]
        limit = params["limit"]

        stats_queryset = self._apply_statistics_filters(
            EnergyStatistics.objects.select_related("device", "energy_type"),
            params,
            PeriodType.DAY,
        )

        if ranking_type == "building":
            all_rows = (
                stats_queryset
                .values("device__room__floor__building_id", "device__room__floor__building__name")
                .annotate(total_value=Sum("total_value"))
                .order_by("-total_value")
            )
            normalized = [
                {
                    "target_id": str(row["device__room__floor__building_id"]),
                    "target_name": row["device__room__floor__building__name"] or "UNKNOWN",
                    "total_value": row["total_value"] or 0,
                }
                for row in all_rows
            ]
        elif ranking_type == "room":
            all_rows = (
                stats_queryset
                .values("device__room_id", "device__room__room_number", "device__room__floor__building__name")
                .annotate(total_value=Sum("total_value"))
                .order_by("-total_value")
            )
            normalized = [
                {
                    "target_id": str(row["device__room_id"]),
                    "target_name": f"{row['device__room__floor__building__name']}-{row['device__room__room_number']}",
                    "total_value": row["total_value"] or 0,
                }
                for row in all_rows
            ]
        else:
            all_rows = (
                stats_queryset
                .values("device__room__department")
                .annotate(total_value=Sum("total_value"))
                .order_by("-total_value")
            )
            normalized = [
                {
                    "target_id": row["device__room__department"] or "UNKNOWN",
                    "target_name": row["device__room__department"] or "UNKNOWN",
                    "total_value": row["total_value"] or 0,
                }
                for row in all_rows
            ]

        my_target_id = self._my_target(ranking_type)
        my_rank = None
        for index, item in enumerate(normalized, start=1):
            if my_target_id is not None and str(item["target_id"]) == str(my_target_id):
                my_rank = index
                break

        items = []
        for index, item in enumerate(normalized[:limit], start=1):
            payload = dict(item)
            payload["rank"] = index
            payload["is_me"] = my_target_id is not None and str(item["target_id"]) == str(my_target_id)
            items.append(payload)

        return Response(
            {
                "type": ranking_type,
                "limit": limit,
                "my_rank": my_rank,
                "my_rank_change": None,
                "my_target_id": my_target_id,
                "items": items,
            }
        )

    @action(detail=False, methods=["get"], url_path="comparison")
    @extend_schema(
        summary="获取同比环比对比",
        parameters=[ComparisonQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def comparison(self, request):
        """返回对比分析结果，支持 summary/radar/trend/history_rank 视图。"""
        params = self._validate_query(ComparisonQuerySerializer)
        period = params["period"]
        anchor_date = params.get("anchor_date", timezone.localdate())
        view = params.get("view", "summary")

        period_type = self._period_type_by_granularity(period)
        stats_queryset = self._apply_statistics_filters(
            EnergyStatistics.objects.select_related("device", "energy_type"),
            params,
            period_type,
        )
        summary_payload = self._comparison_summary_payload(stats_queryset, period, anchor_date)
        if view == "summary":
            summary_payload["view"] = "summary"
            return Response(summary_payload)

        if view == "radar":
            compare_type = params.get("type") or request.query_params.get("type") or "school"
            compare_type = str(compare_type).strip().lower()
            (current_start, current_end), _, _ = self._comparison_ranges(period, anchor_date)
            period_stats_queryset = stats_queryset.filter(
                period_date__gte=current_start.date(),
                period_date__lte=current_end.date(),
            )
            room_ids = self._bound_room_ids()
            my_queryset = period_stats_queryset.filter(device__room_id__in=room_ids)
            benchmark_queryset = period_stats_queryset
            if compare_type == "building" and room_ids:
                building_ids = list(
                    Room.objects.filter(id__in=room_ids).values_list("floor__building_id", flat=True).distinct()
                )
                benchmark_queryset = period_stats_queryset.filter(device__room__floor__building_id__in=building_ids)
            elif compare_type == "similar" and room_ids:
                departments = list(
                    Room.objects.filter(id__in=room_ids).values_list("department", flat=True).distinct()
                )
                benchmark_queryset = period_stats_queryset.filter(device__room__department__in=departments)

            def _metric_vector(target_queryset):
                energy_map = {
                    str(item["energy_type__code"]): float(item["total"] or 0)
                    for item in target_queryset.values("energy_type__code").annotate(total=Sum("total_value"))
                }
                total_usage = sum(energy_map.values())
                total_cost = 0.0
                total_carbon = 0.0
                for code, total in energy_map.items():
                    total_cost += total * float(ENERGY_PRICE_MAP.get(code, Decimal("1.00")))
                    total_carbon += total * float(CARBON_FACTOR_MAP.get(code, Decimal("0.50")))
                saving_score = max(0.0, 100.0 - min(100.0, total_usage / 10.0))
                return {
                    "electricity": energy_map.get("ELECTRICITY", 0.0),
                    "water": energy_map.get("WATER", 0.0),
                    "gas": energy_map.get("GAS", 0.0),
                    "cost": total_cost,
                    "carbon": total_carbon,
                    "saving": saving_score,
                }

            my_metrics = _metric_vector(my_queryset)
            benchmark_metrics = _metric_vector(benchmark_queryset)
            metric_keys = ["electricity", "water", "gas", "cost", "carbon", "saving"]
            metric_names = ["用电", "用水", "用气", "费用", "碳排", "节能"]
            indicators = []
            my_values = []
            benchmark_values = []
            for key, name in zip(metric_keys, metric_names, strict=False):
                my_value = my_metrics[key]
                benchmark_value = benchmark_metrics[key]
                max_value = max(my_value, benchmark_value, 1.0) * 1.2
                indicators.append({"name": name, "max": round(max_value, 2)})
                my_values.append(round(my_value, 4))
                benchmark_values.append(round(benchmark_value, 4))
            return Response(
                {
                    "view": "radar",
                    "period": "month",
                    "target_type": compare_type,
                    "indicators": indicators,
                    "series": [
                        {"name": "我的用能", "value": my_values},
                        {"name": "对比基准", "value": benchmark_values},
                    ],
                }
            )

        if view == "trend":
            month_stats_queryset = self._apply_statistics_filters(
                EnergyStatistics.objects.select_related("device", "energy_type"),
                params,
                PeriodType.MONTH,
            )
            month_points = []
            cursor = anchor_date.replace(day=1)
            for _ in range(6):
                month_points.append(cursor)
                cursor = (cursor - timedelta(days=1)).replace(day=1)
            lookup_months = set(month_points)
            for month_point in month_points:
                lookup_months.add((month_point - timedelta(days=1)).replace(day=1))
                lookup_months.add(_shift_year(month_point, -1).replace(day=1))
            min_month = min(lookup_months)
            max_month = max(lookup_months)
            totals_by_month = {
                row["period_date"]: row["total_value"] or 0
                for row in month_stats_queryset.filter(period_date__gte=min_month, period_date__lte=max_month)
                .values("period_date")
                .annotate(total_value=Sum("total_value"))
            }
            trend_series = []
            for month_point in month_points:
                chain_month = (month_point - timedelta(days=1)).replace(day=1)
                yoy_month = _shift_year(month_point, -1).replace(day=1)
                current_total = totals_by_month.get(month_point, 0)
                chain_total = totals_by_month.get(chain_month, 0)
                yoy_total = totals_by_month.get(yoy_month, 0)
                trend_series.append(
                    {
                        "period": month_point.strftime("%Y-%m"),
                        "current_total": current_total,
                        "chain_total": chain_total,
                        "yoy_total": yoy_total,
                        "chain_change_rate": _safe_rate(current_total, chain_total),
                        "yoy_change_rate": _safe_rate(current_total, yoy_total),
                    }
                )
            trend_series.reverse()
            return Response({"view": "trend", "period": "month", "series": trend_series})

        my_target_id = self._my_target("building")
        if my_target_id is None:
            return Response({"view": "history_rank", "target_id": None, "series": []})
        month_stats_queryset = self._apply_statistics_filters(
            EnergyStatistics.objects.select_related("device", "energy_type"),
            params,
            PeriodType.MONTH,
        )
        month_points = []
        month_cursor = anchor_date.replace(day=1)
        for _ in range(6):
            month_points.append(month_cursor)
            month_cursor = (month_cursor - timedelta(days=1)).replace(day=1)
        month_rows = (
            month_stats_queryset.filter(period_date__in=month_points)
            .values("period_date", "device__room__floor__building_id")
            .annotate(total_value=Sum("total_value"))
            .order_by("period_date", "-total_value")
        )
        grouped_rows = {}
        for row in month_rows:
            period_date = row["period_date"]
            grouped_rows.setdefault(period_date, []).append(row)

        history_series = []
        previous_rank = None
        for month_point in month_points:
            period_rows = grouped_rows.get(month_point, [])
            rank = None
            total_targets = len(period_rows)
            for idx, row in enumerate(period_rows, start=1):
                if str(row["device__room__floor__building_id"]) == str(my_target_id):
                    rank = idx
                    break
            history_series.append(
                {
                    "period": month_point.strftime("%Y-%m"),
                    "rank": rank,
                    "rank_change": (previous_rank - rank) if rank and previous_rank else None,
                    "total_targets": total_targets,
                }
            )
            previous_rank = rank
        history_series.reverse()
        return Response({"view": "history_rank", "target_id": my_target_id, "series": history_series})

    @action(detail=False, methods=["get"], url_path="hourly-distribution")
    @extend_schema(
        summary="获取分时段用能分布",
        parameters=[HourlyDistributionQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def hourly_distribution(self, request):
        params = self._validate_query(HourlyDistributionQuerySerializer)
        queryset = self._apply_common_filters(EnergyData.objects.all(), params)
        buckets = [
            ("00-04", 0, 4),
            ("04-08", 4, 8),
            ("08-12", 8, 12),
            ("12-16", 12, 16),
            ("16-20", 16, 20),
            ("20-24", 20, 24),
        ]
        rows = (
            queryset.annotate(hour=Func(F("timestamp"), function="HOUR", output_field=IntegerField()))
            .values("hour")
            .annotate(total_value=Sum("value"), records=Count("id"))
        )
        bucket_stats = {
            label: {"total_value": 0, "records": 0}
            for label, _, _ in buckets
        }
        for row in rows:
            hour = row["hour"]
            if hour is None:
                continue
            bucket_index = min(hour // 4, len(buckets) - 1)
            label = buckets[bucket_index][0]
            bucket_stats[label]["total_value"] += row["total_value"] or 0
            bucket_stats[label]["records"] += row["records"] or 0

        data = []
        for label, _, _ in buckets:
            total_value = bucket_stats[label]["total_value"]
            records = bucket_stats[label]["records"]
            avg_value = total_value / records if records else 0
            data.append(
                {
                    "time_range": label,
                    "total_value": total_value,
                    "avg_value": avg_value,
                    "records": records,
                }
            )
        return Response({"buckets": data})

    @action(detail=False, methods=["get"], url_path="forecast")
    @extend_schema(
        summary="获取趋势预测",
        parameters=[ForecastQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def forecast(self, request):
        """读取 em_energy_forecasts 并返回历史与预测序列。"""
        params = self._validate_query(ForecastQuerySerializer)
        target = params["target"]
        horizon = 7 if params["period"] == "7d" else 30
        target_id = str(params.get("target_id") or request.query_params.get("target_id") or "").strip()
        model_version = str(params.get("model_version") or request.query_params.get("model_version") or "").strip()

        forecast_queryset = EnergyForecast.objects.select_related("energy_type")
        forecast_queryset = forecast_queryset.filter(horizon_days=horizon)

        target_type_map = {
            "campus": ForecastTargetType.CAMPUS,
            "building": ForecastTargetType.BUILDING,
            "meter": ForecastTargetType.METER,
        }
        forecast_queryset = forecast_queryset.filter(target_type=target_type_map[target])

        energy_type = params.get("energy_type")
        if energy_type:
            if str(energy_type).isdigit():
                forecast_queryset = forecast_queryset.filter(energy_type_id=int(energy_type))
            else:
                forecast_queryset = forecast_queryset.filter(energy_type__code__iexact=str(energy_type).strip())

        if model_version:
            forecast_queryset = forecast_queryset.filter(model_version=model_version)

        # When no target_id is specified, aggregate all forecasts by date
        if target_id:
            forecast_queryset = forecast_queryset.filter(target_id=target_id)
            forecast_rows = list(
                forecast_queryset.values("forecast_date", "forecast_value", "model_version").order_by("forecast_date")
            )
        else:
            # Aggregate all forecasts by date - sum forecast values for each date
            forecast_rows = list(
                forecast_queryset.values("forecast_date")
                .annotate(forecast_value=Sum("forecast_value"))
                .values("forecast_date", "forecast_value")
                .order_by("forecast_date")
            )

        stats_queryset = self._apply_statistics_filters(
            EnergyStatistics.objects.select_related("device", "energy_type"),
            params,
            PeriodType.DAY,
        )
        if target == "campus" and target_id:
            stats_queryset = stats_queryset.filter(device__room__floor__building__campus_id=target_id)
        if target == "building" and target_id:
            stats_queryset = stats_queryset.filter(device__room__floor__building_id=target_id)
        if target == "meter" and target_id:
            if str(target_id).isdigit():
                stats_queryset = stats_queryset.filter(device_id=int(target_id))
            else:
                stats_queryset = stats_queryset.filter(device__device_id=target_id)

        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=max(horizon * 2, 14))
        history_rows = (
            stats_queryset.filter(period_date__gte=start_date, period_date__lte=end_date)
            .values("period_date")
            .annotate(total_value=Sum("total_value"))
            .order_by("period_date")
        )
        history_items = [
            {"date": row["period_date"].isoformat(), "value": round(float(row["total_value"] or 0), 6)}
            for row in history_rows
            if row["period_date"] is not None
        ]
        forecast_items = [
            {"date": row["forecast_date"].isoformat(), "predicted_value": round(float(row["forecast_value"] or 0), 6)}
            for row in forecast_rows
        ]
        baseline = round(sum(item["value"] for item in history_items) / len(history_items), 6) if history_items else 0

        # Get model_version from forecast rows if available
        forecast_model_version = None
        if forecast_rows:
            forecast_model_version = forecast_rows[0].get("model_version") or model_version or None

        return Response(
            {
                "target": target,
                "period": params["period"],
                "target_id": target_id or None,
                "baseline_avg": baseline,
                "model_version": forecast_model_version,
                "history": history_items,
                "forecast": forecast_items,
            }
        )

    @action(detail=False, methods=["get"], url_path="real-time-power")
    @extend_schema(
        summary="获取实时功率序列",
        parameters=[RealTimePowerQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def real_time_power(self, request):
        params = self._validate_query(RealTimePowerQuerySerializer)
        hours = int(params["hours"])
        interval_minutes = int(params["interval_minutes"])
        cache_key = (
            "real_time_power:"
            f"{hours}:{interval_minutes}:"
            f"{params.get('campus_id') or 'all'}:{params.get('building_id') or 'all'}:"
            f"{params.get('room_id') or 'all'}:{params.get('energy_type') or 'all'}:"
            f"{params.get('device_id') or 'all'}"
        )
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        end_time = timezone.now()
        start_time = end_time - timedelta(hours=hours)

        queryset = self._apply_common_filters(EnergyData.objects.all(), params)
        queryset = queryset.filter(timestamp__gte=start_time, timestamp__lte=end_time).exclude(power__isnull=True)

        interval_seconds = interval_minutes * 60
        bucket_rows = (
            queryset.extra(
                select={
                    "bucket": (
                        f"FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(timestamp) / {interval_seconds}) * {interval_seconds})"
                    )
                }
            )
            .values("bucket")
            .annotate(
                total_power=Sum("power"),
                sample_count=Count("id"),
                device_count=Count("device_id", distinct=True),
            )
            .order_by("bucket")
        )
        series = []
        for row in bucket_rows:
            bucket = row["bucket"]
            if isinstance(bucket, datetime):
                bucket = _ensure_aware_datetime(bucket)
                timestamp_value = bucket.isoformat()
            else:
                timestamp_value = str(bucket) if bucket is not None else None
            sample_count = row["sample_count"] or 0
            total_power = float(row["total_power"] or 0)
            series.append(
                {
                    "timestamp": timestamp_value,
                    "total_power": round(total_power, 3),
                    "avg_power": round(total_power / sample_count, 3) if sample_count else 0,
                    "device_count": row["device_count"] or 0,
                }
            )

        latest_record = queryset.values(
            "timestamp", "power", "device_id", "device__device_id", "device__name"
        ).order_by("-timestamp", "-id").first()
        peak_record = queryset.values(
            "timestamp", "power", "device_id", "device__device_id", "device__name"
        ).order_by("-power", "-timestamp").first()

        latest_snapshot = None
        if latest_record:
            latest_ts = _ensure_aware_datetime(latest_record["timestamp"])
            latest_snapshot = {
                "timestamp": latest_ts.isoformat() if latest_ts else None,
                "power": float(latest_record["power"] or 0),
                "device_id": latest_record["device_id"],
                "device_code": latest_record["device__device_id"],
                "device_name": latest_record["device__name"],
            }

        peak_snapshot = None
        if peak_record:
            peak_ts = _ensure_aware_datetime(peak_record["timestamp"])
            peak_snapshot = {
                "timestamp": peak_ts.isoformat() if peak_ts else None,
                "power": float(peak_record["power"] or 0),
                "device_id": peak_record["device_id"],
                "device_code": peak_record["device__device_id"],
                "device_name": peak_record["device__name"],
            }

        payload = {
            "hours": hours,
            "interval_minutes": interval_minutes,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "points": len(series),
            "series": series,
            "latest": latest_snapshot,
            "peak": peak_snapshot,
        }
        cache.set(cache_key, payload, timeout=30)
        return Response(payload)
