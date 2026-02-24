from datetime import date, datetime, time, timedelta

from django.db.models import Avg, Count, Q, Sum
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.alarms.models import Alarm, AlarmStatus
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


class AnalysisViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EnergyData.objects.none()

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
    def dashboard(self, request):
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
    def trend(self, request):
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
    def distribution(self, request):
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
    def ranking(self, request):
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
    def comparison(self, request):
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
    def forecast(self, request):
        params = self._validate_query(ForecastQuerySerializer)
        target = params["target"]
        horizon = 7 if params["period"] == "7d" else 30

        energy_queryset = EnergyData.objects.select_related("device", "energy_type")
        energy_queryset = self._apply_common_filters(energy_queryset, params)

        # target specific aliases
        target_id = request.query_params.get("target_id")
        if target == "campus" and target_id:
            energy_queryset = energy_queryset.filter(device__room__floor__building__campus_id=target_id)
        if target == "building" and target_id:
            energy_queryset = energy_queryset.filter(device__room__floor__building_id=target_id)
        if target == "meter" and target_id:
            if str(target_id).isdigit():
                energy_queryset = energy_queryset.filter(device_id=int(target_id))
            else:
                energy_queryset = energy_queryset.filter(device__device_id=target_id)

        end_date = timezone.localdate()
        start_date = end_date - timedelta(days=max(horizon * 2, 14))
        energy_queryset = energy_queryset.filter(
            timestamp__gte=_day_range(start_date)[0],
            timestamp__lte=_day_range(end_date)[1],
        )

        daily_rows = (
            energy_queryset
            .annotate(day=TruncDate("timestamp"))
            .values("day")
            .annotate(total_value=Sum("value"))
            .order_by("day")
        )

        value_map = {row["day"]: float(row["total_value"] or 0) for row in daily_rows}
        history_days = [end_date - timedelta(days=offset) for offset in range(horizon - 1, -1, -1)]
        history_values = [value_map.get(day, 0.0) for day in history_days]

        if history_values:
            baseline = sum(history_values) / len(history_values)
        else:
            baseline = 0.0

        # simple linear trend forecast
        if len(history_values) <= 1:
            slope = 0.0
            intercept = baseline
        else:
            n = len(history_values)
            xs = list(range(n))
            sum_x = sum(xs)
            sum_y = sum(history_values)
            sum_x2 = sum(x * x for x in xs)
            sum_xy = sum(x * y for x, y in zip(xs, history_values))
            denominator = n * sum_x2 - sum_x * sum_x
            if denominator == 0:
                slope = 0.0
                intercept = baseline
            else:
                slope = (n * sum_xy - sum_x * sum_y) / denominator
                intercept = (sum_y - slope * sum_x) / n

        forecast_items = []
        n = len(history_values)
        for step in range(1, horizon + 1):
            predict_date = end_date + timedelta(days=step)
            prediction = max(0.0, intercept + slope * (n + step - 1))
            forecast_items.append({"date": predict_date.isoformat(), "predicted_value": round(prediction, 6)})

        history_items = [
            {"date": day.isoformat(), "value": round(value, 6)}
            for day, value in zip(history_days, history_values)
        ]

        return Response(
            {
                "target": target,
                "period": params["period"],
                "baseline_avg": round(baseline, 6),
                "history": history_items,
                "forecast": forecast_items,
            }
        )
