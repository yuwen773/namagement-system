from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.db.models import Avg, OuterRef, Subquery
from django.db.models.functions import TruncHour
from django.utils import timezone

from .models import AirQualityData, MonitoringStation

POLLUTANT_FIELDS = ("pm25", "pm10", "so2", "no2", "co", "o3")


def to_float(value: Any, digits: int = 2) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)


def to_int(value: Any) -> int | None:
    if value is None:
        return None
    return int(round(float(value)))


def clamp_aqi(value: int) -> int:
    return max(0, min(500, value))


def calc_quality_level_from_aqi(aqi: int | None) -> str:
    if aqi is None:
        return ""
    return AirQualityData._calc_quality_level(clamp_aqi(aqi))


def _aggregate_snapshot(queryset) -> dict[str, Any] | None:
    if not queryset.exists():
        return None

    aggregated = queryset.aggregate(
        aqi=Avg("aqi"),
        pm25=Avg("pm25"),
        pm10=Avg("pm10"),
        so2=Avg("so2"),
        no2=Avg("no2"),
        co=Avg("co"),
        o3=Avg("o3"),
    )
    aqi_int = to_int(aggregated["aqi"])
    return {
        "aqi": aqi_int,
        "pm25": to_float(aggregated["pm25"]),
        "pm10": to_float(aggregated["pm10"]),
        "so2": to_float(aggregated["so2"]),
        "no2": to_float(aggregated["no2"]),
        "co": to_float(aggregated["co"]),
        "o3": to_float(aggregated["o3"]),
        "quality_level": calc_quality_level_from_aqi(aqi_int),
    }


def get_city_latest_snapshot(city) -> dict[str, Any] | None:
    latest_time = (
        AirQualityData.objects.filter(station__city=city)
        .order_by("-monitor_time")
        .values_list("monitor_time", flat=True)
        .first()
    )
    if latest_time is None:
        return None

    snapshot_qs = AirQualityData.objects.filter(station__city=city, monitor_time=latest_time)
    snapshot = _aggregate_snapshot(snapshot_qs)
    if snapshot is None:
        return None
    snapshot["monitor_time"] = latest_time
    snapshot["station_count"] = snapshot_qs.values("station_id").distinct().count()
    return snapshot


def get_station_latest_snapshot(station) -> dict[str, Any] | None:
    record = (
        AirQualityData.objects.filter(station=station).order_by("-monitor_time", "-id").first()
    )
    if record is None:
        return None

    return {
        "monitor_time": record.monitor_time,
        "aqi": int(record.aqi),
        "pm25": to_float(record.pm25),
        "pm10": to_float(record.pm10),
        "so2": to_float(record.so2),
        "no2": to_float(record.no2),
        "co": to_float(record.co),
        "o3": to_float(record.o3),
        "quality_level": record.quality_level,
    }


def get_city_hourly_trend(city, hours: int = 24) -> list[dict[str, Any]]:
    latest_snapshot = get_city_latest_snapshot(city)
    if latest_snapshot is None:
        return []

    latest_time = latest_snapshot["monitor_time"]
    start_time = latest_time - timedelta(hours=max(hours, 1) - 1)

    rows = (
        AirQualityData.objects.filter(
            station__city=city, monitor_time__gte=start_time, monitor_time__lte=latest_time
        )
        .annotate(hour=TruncHour("monitor_time", tzinfo=timezone.get_current_timezone()))
        .values("hour")
        .annotate(
            aqi=Avg("aqi"),
            pm25=Avg("pm25"),
            pm10=Avg("pm10"),
            so2=Avg("so2"),
            no2=Avg("no2"),
            co=Avg("co"),
            o3=Avg("o3"),
        )
        .order_by("hour")
    )

    result = []
    for row in rows:
        result.append(
            {
                "time": row["hour"],
                "aqi": to_int(row["aqi"]),
                "pm25": to_float(row["pm25"]),
                "pm10": to_float(row["pm10"]),
                "so2": to_float(row["so2"]),
                "no2": to_float(row["no2"]),
                "co": to_float(row["co"]),
                "o3": to_float(row["o3"]),
            }
        )
    return result


def get_station_hourly_trend(station, hours: int = 24) -> list[dict[str, Any]]:
    latest_snapshot = get_station_latest_snapshot(station)
    if latest_snapshot is None:
        return []

    latest_time = latest_snapshot["monitor_time"]
    start_time = latest_time - timedelta(hours=max(hours, 1) - 1)

    rows = (
        AirQualityData.objects.filter(
            station=station, monitor_time__gte=start_time, monitor_time__lte=latest_time
        )
        .annotate(hour=TruncHour("monitor_time", tzinfo=timezone.get_current_timezone()))
        .values("hour")
        .annotate(
            aqi=Avg("aqi"),
            pm25=Avg("pm25"),
            pm10=Avg("pm10"),
            so2=Avg("so2"),
            no2=Avg("no2"),
            co=Avg("co"),
            o3=Avg("o3"),
        )
        .order_by("hour")
    )

    result = []
    for row in rows:
        result.append(
            {
                "time": row["hour"],
                "aqi": to_int(row["aqi"]),
                "pm25": to_float(row["pm25"]),
                "pm10": to_float(row["pm10"]),
                "so2": to_float(row["so2"]),
                "no2": to_float(row["no2"]),
                "co": to_float(row["co"]),
                "o3": to_float(row["o3"]),
            }
        )
    return result


def get_latest_station_records_queryset():
    latest_record_subquery = (
        AirQualityData.objects.filter(station=OuterRef("pk"))
        .order_by("-monitor_time", "-id")
        .values("pk")[:1]
    )
    latest_ids = (
        MonitoringStation.objects.annotate(latest_record_id=Subquery(latest_record_subquery))
        .filter(latest_record_id__isnull=False)
        .values("latest_record_id")
    )
    return AirQualityData.objects.filter(pk__in=Subquery(latest_ids)).select_related(
        "station__city__province"
    )
