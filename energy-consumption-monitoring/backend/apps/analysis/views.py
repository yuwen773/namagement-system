from datetime import date, datetime, time, timedelta

from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.alarms.models import Alarm, AlarmStatus
from apps.analysis.models import EnergyForecast, ForecastTargetType
from apps.analysis.serializers import (
    BaseAnalysisQuerySerializer,
    ComparisonQuerySerializer,
    DistributionQuerySerializer,
    ForecastQuerySerializer,
    RankingQuerySerializer,
    TrendQuerySerializer,
)
from apps.devices.models import Device
from apps.energy.models import EnergyData


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


class AnalysisEmptySerializer(serializers.Serializer):
    """用于 schema 推断的占位序列化器。"""


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

        return queryset

    @action(detail=False, methods=["get"], url_path="dashboard")
    @extend_schema(
        summary="获取综合监控概览",
        parameters=[BaseAnalysisQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def dashboard(self, request):
        """返回能耗总览、覆盖率和告警统计。"""
        params = self._validate_query(BaseAnalysisQuerySerializer)
        energy_queryset = self._apply_common_filters(
            EnergyData.objects.select_related("energy_type", "device"),
            params,
        )

        totals = energy_queryset.values(
            "energy_type__code",
            "energy_type__name",
            "energy_type__unit",
        ).annotate(
            total_value=Sum("value"),
        ).order_by("energy_type__code")

        overall = energy_queryset.aggregate(
            total_value=Sum("value"),
            avg_power=Avg("power"),
            records=Count("id"),
        )

        total_devices = Device.objects.count()
        covered_devices = energy_queryset.values("device_id").distinct().count()
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

        return Response(
            {
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
        )

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

        energy_queryset = self._apply_common_filters(
            EnergyData.objects.select_related("device", "energy_type"),
            params,
        )

        if period == "day":
            trunc_func = TruncDate("timestamp")
            label_format = "%Y-%m-%d"
        elif period == "month":
            trunc_func = TruncMonth("timestamp")
            label_format = "%Y-%m"
        else:
            trunc_func = TruncYear("timestamp")
            label_format = "%Y"

        rows = (
            energy_queryset
            .annotate(bucket=trunc_func)
            .values("bucket")
            .annotate(
                total_value=Sum("value"),
                avg_power=Avg("power"),
                records=Count("id"),
            )
            .order_by("bucket")
        )

        series = [
            {
                "period": row["bucket"].strftime(label_format) if row["bucket"] else None,
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
        """按区域或能源类型返回能耗占比分布。"""
        params = self._validate_query(DistributionQuerySerializer)
        distribution_type = params["type"]

        energy_queryset = self._apply_common_filters(
            EnergyData.objects.select_related("device", "energy_type"),
            params,
        )

        if distribution_type == "area":
            rows = (
                energy_queryset
                .values("device__room__floor__building__area_type")
                .annotate(total_value=Sum("value"))
                .order_by("-total_value")
            )
            data = [
                {
                    "name": row["device__room__floor__building__area_type"] or "UNKNOWN",
                    "value": row["total_value"] or 0,
                }
                for row in rows
            ]
        else:
            rows = (
                energy_queryset
                .values("energy_type__code", "energy_type__name")
                .annotate(total_value=Sum("value"))
                .order_by("-total_value")
            )
            data = [
                {
                    "name": row["energy_type__code"],
                    "label": row["energy_type__name"],
                    "value": row["total_value"] or 0,
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

        energy_queryset = self._apply_common_filters(
            EnergyData.objects.select_related("device", "energy_type"),
            params,
        )

        if ranking_type == "building":
            rows = (
                energy_queryset
                .values("device__room__floor__building_id", "device__room__floor__building__name")
                .annotate(total_value=Sum("value"))
                .order_by("-total_value")[:limit]
            )
            items = [
                {
                    "target_id": row["device__room__floor__building_id"],
                    "target_name": row["device__room__floor__building__name"] or "UNKNOWN",
                    "total_value": row["total_value"] or 0,
                }
                for row in rows
            ]
        elif ranking_type == "room":
            rows = (
                energy_queryset
                .values("device__room_id", "device__room__room_number", "device__room__floor__building__name")
                .annotate(total_value=Sum("value"))
                .order_by("-total_value")[:limit]
            )
            items = [
                {
                    "target_id": row["device__room_id"],
                    "target_name": f"{row['device__room__floor__building__name']}-{row['device__room__room_number']}",
                    "total_value": row["total_value"] or 0,
                }
                for row in rows
            ]
        else:
            rows = (
                energy_queryset
                .values("device__room__department")
                .annotate(total_value=Sum("value"))
                .order_by("-total_value")[:limit]
            )
            items = [
                {
                    "target_name": row["device__room__department"] or "UNKNOWN",
                    "total_value": row["total_value"] or 0,
                }
                for row in rows
            ]

        for index, item in enumerate(items, start=1):
            item["rank"] = index

        return Response({"type": ranking_type, "limit": limit, "items": items})

    @action(detail=False, methods=["get"], url_path="comparison")
    @extend_schema(
        summary="获取同比环比对比",
        parameters=[ComparisonQuerySerializer],
        responses={200: OpenApiTypes.OBJECT},
    )
    def comparison(self, request):
        """返回当前周期与环比、同比的总量与变化率。"""
        params = self._validate_query(ComparisonQuerySerializer)
        period = params["period"]
        anchor_date = params.get("anchor_date", timezone.localdate())

        energy_queryset = self._apply_common_filters(EnergyData.objects.all(), params)

        if period == "day":
            current_start, current_end = _day_range(anchor_date)
            previous_start, previous_end = _day_range(anchor_date - timedelta(days=1))
            yoy_start, yoy_end = _day_range(_shift_year(anchor_date, -1))
        elif period == "month":
            current_start, current_end = _month_range(anchor_date)
            previous_anchor = (anchor_date.replace(day=1) - timedelta(days=1))
            previous_start, previous_end = _month_range(previous_anchor)
            yoy_start, yoy_end = _month_range(_shift_year(anchor_date, -1))
        else:
            current_start, current_end = _year_range(anchor_date)
            previous_anchor = _shift_year(anchor_date, -1)
            previous_start, previous_end = _year_range(previous_anchor)
            yoy_start, yoy_end = _year_range(_shift_year(anchor_date, -1))

        current_total = energy_queryset.filter(
            timestamp__gte=current_start,
            timestamp__lte=current_end,
        ).aggregate(total=Sum("value"))["total"] or 0

        previous_total = energy_queryset.filter(
            timestamp__gte=previous_start,
            timestamp__lte=previous_end,
        ).aggregate(total=Sum("value"))["total"] or 0

        yoy_total = energy_queryset.filter(
            timestamp__gte=yoy_start,
            timestamp__lte=yoy_end,
        ).aggregate(total=Sum("value"))["total"] or 0

        return Response(
            {
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
        )

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

        if target_id:
            forecast_queryset = forecast_queryset.filter(target_id=target_id)
        else:
            hint_fields = {"campus": "campus_id", "building": "building_id", "meter": "target_id"}
            field_name = hint_fields[target]
            return Response(
                {
                    "target": target,
                    "period": params["period"],
                    "history": [],
                    "forecast": [],
                    "message": f"缺少 target_id，请指定 `{field_name}`。",
                }
            )

        if model_version:
            forecast_queryset = forecast_queryset.filter(model_version=model_version)

        forecast_rows = list(
            forecast_queryset.values("forecast_date", "forecast_value", "model_version").order_by("forecast_date")
        )

        energy_queryset = self._apply_common_filters(
            EnergyData.objects.select_related("device", "energy_type"),
            params,
        )
        if target == "campus":
            energy_queryset = energy_queryset.filter(device__room__floor__building__campus_id=target_id)
        if target == "building":
            energy_queryset = energy_queryset.filter(device__room__floor__building_id=target_id)
        if target == "meter":
            if str(target_id).isdigit():
                energy_queryset = energy_queryset.filter(device_id=int(target_id))
            else:
                energy_queryset = energy_queryset.filter(device__device_id=target_id)

        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=max(horizon * 2, 14))
        history_rows = (
            energy_queryset.filter(
                timestamp__gte=_day_range(start_date)[0],
                timestamp__lte=_day_range(end_date)[1],
            )
            .annotate(day=TruncDate("timestamp"))
            .values("day")
            .annotate(total_value=Sum("value"))
            .order_by("day")
        )
        history_items = [
            {"date": row["day"].isoformat(), "value": round(float(row["total_value"] or 0), 6)}
            for row in history_rows
            if row["day"] is not None
        ]
        forecast_items = [
            {"date": row["forecast_date"].isoformat(), "predicted_value": round(float(row["forecast_value"] or 0), 6)}
            for row in forecast_rows
        ]
        baseline = round(sum(item["value"] for item in history_items) / len(history_items), 6) if history_items else 0

        return Response(
            {
                "target": target,
                "period": params["period"],
                "target_id": target_id,
                "baseline_avg": baseline,
                "model_version": forecast_rows[0]["model_version"] if forecast_rows else model_version or None,
                "history": history_items,
                "forecast": forecast_items,
            }
        )
