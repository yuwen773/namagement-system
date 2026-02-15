from __future__ import annotations

import os
import uuid
from datetime import datetime
from io import BytesIO, StringIO
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from apps.airquality.filters import HistoricalDataFilter
from apps.airquality.models import AirQualityData, City, MonitoringStation
from apps.airquality.serializers import HistoricalAirQualitySerializer, ProvinceCitySerializer
from apps.airquality.services import (
    POLLUTANT_FIELDS,
    calc_quality_level_from_aqi,
    get_city_hourly_trend,
    get_city_latest_snapshot,
    get_latest_station_records_queryset,
    get_station_hourly_trend,
    get_station_latest_snapshot,
    to_float,
    to_int,
)
from apps.logs.models import ImportTask, ImportTaskLog
from apps.logs.serializers import ImportTaskLogSerializer, ImportTaskSerializer
from utils.data_importer import run_import_task, submit_import_task
from utils.exception_handler import ValidationError
from utils.response import APIResponse


def _get_required_int_query_param(
    request, field: str, default: int, min_value: int, max_value: int
) -> int:
    raw_value = request.query_params.get(field, str(default))
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        raise ValidationError(f"格式错误，应为整数，范围 {min_value}-{max_value}", field=field)
    if value < min_value or value > max_value:
        raise ValidationError(f"超出范围，应为 {min_value}-{max_value}", field=field)
    return value


def _get_optional_date_query_param(request, field: str):
    raw_value = request.query_params.get(field)
    if not raw_value:
        return None
    try:
        return datetime.strptime(raw_value, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("格式错误，应为 YYYY-MM-DD", field=field)


def _parse_filter_errors(filterset: HistoricalDataFilter):
    first_field, errors = next(iter(filterset.errors.items()))
    if isinstance(errors, (list, tuple)) and errors:
        message = str(errors[0])
    else:
        message = str(errors)
    raise ValidationError(message, field=first_field)


class DataImportUploadView(APIView):
    """
    Phase 1 - Step 1.3.2

    POST /api/admin/data-import/
    form-data:
      - file: csv/xlsx/xls
      - dataset_type: provinces|cities|stations|air_quality_data (default air_quality_data)
    """

    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        upload = request.FILES.get("file")
        if not upload:
            raise ValidationError("缺少上传文件", field="file")

        dataset_type = (request.data.get("dataset_type") or "air_quality_data").strip()
        if dataset_type not in {"provinces", "cities", "stations", "air_quality_data"}:
            raise ValidationError(
                "必须是 provinces/cities/stations/air_quality_data 之一", field="dataset_type"
            )

        ext = Path(upload.name).suffix.lower()
        if ext not in {".csv", ".xlsx", ".xls"}:
            raise ValidationError("仅支持 csv/xlsx/xls", field="file")

        task_id = uuid.uuid4().hex
        rel_dir = Path("imports") / task_id
        abs_dir = Path(settings.MEDIA_ROOT) / rel_dir
        abs_dir.mkdir(parents=True, exist_ok=True)

        # Avoid path traversal.
        safe_name = os.path.basename(upload.name)
        abs_path = abs_dir / safe_name

        with abs_path.open("wb") as f:
            for chunk in upload.chunks():
                f.write(chunk)

        ImportTask.objects.create(
            task_id=task_id,
            file_name=safe_name,
            file_type=dataset_type,
            status=ImportTask.Status.PENDING,
            total_count=0,
            success_count=0,
            failed_count=0,
            initiator=request.user,
            # start_time auto_now_add
            end_time=None,
        )

        if getattr(settings, "DATA_IMPORT_ASYNC", True):
            submit_import_task(task_id=task_id, dataset_type=dataset_type, file_path=str(abs_path))
        else:
            run_import_task(task_id=task_id, dataset_type=dataset_type, file_path=str(abs_path))

        return APIResponse.success(
            data={
                "task_id": task_id,
                "status": ImportTask.Status.PENDING,
                "dataset_type": dataset_type,
            }
        )


class ImportTaskListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = ImportTask.objects.all().order_by("-start_time", "-id")

        page = _get_required_int_query_param(
            request=request, field="page", default=1, min_value=1, max_value=10_000
        )
        page_size = _get_required_int_query_param(
            request=request, field="page_size", default=20, min_value=1, max_value=200
        )

        total = qs.count()
        items = qs[(page - 1) * page_size : page * page_size]
        data = ImportTaskSerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)


class ImportTaskDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, task_id: str):
        try:
            task = ImportTask.objects.get(task_id=task_id)
        except ImportTask.DoesNotExist:
            return APIResponse.error(404, "导入任务不存在")
        return APIResponse.success(data=ImportTaskSerializer(task).data)


class ImportTaskLogListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, task_id: str):
        try:
            task = ImportTask.objects.get(task_id=task_id)
        except ImportTask.DoesNotExist:
            return APIResponse.error(404, "导入任务不存在")

        qs = ImportTaskLog.objects.filter(task=task).order_by("id")
        page = _get_required_int_query_param(
            request=request, field="page", default=1, min_value=1, max_value=10_000
        )
        page_size = _get_required_int_query_param(
            request=request, field="page_size", default=50, min_value=1, max_value=200
        )

        total = qs.count()
        items = qs[(page - 1) * page_size : page * page_size]
        data = ImportTaskLogSerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)


class ImportTaskCancelView(APIView):
    """
    Optional helper: mark a running task as FAILED (no hard cancellation of executor thread).
    """

    permission_classes = [IsAdminUser]

    def post(self, request, task_id: str):
        try:
            task = ImportTask.objects.get(task_id=task_id)
        except ImportTask.DoesNotExist:
            return APIResponse.error(404, "导入任务不存在")

        if task.status in {ImportTask.Status.SUCCESS, ImportTask.Status.FAILED}:
            return APIResponse.success(data=ImportTaskSerializer(task).data, message="任务已结束")

        task.status = ImportTask.Status.FAILED
        task.end_time = timezone.now()
        task.save(update_fields=["status", "end_time"])
        return APIResponse.success(data=ImportTaskSerializer(task).data, message="已标记为失败")


class AirQualityOverviewViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60))
    def list(self, request):
        latest_qs = get_latest_station_records_queryset()
        national = latest_qs.aggregate(
            aqi=Avg("aqi"),
            pm25=Avg("pm25"),
            pm10=Avg("pm10"),
            so2=Avg("so2"),
            no2=Avg("no2"),
            co=Avg("co"),
            o3=Avg("o3"),
        )
        city_rows = (
            latest_qs.values(
                "station__city__code",
                "station__city__name",
                "station__city__longitude",
                "station__city__latitude",
                "station__city__province__code",
                "station__city__province__name",
            )
            .annotate(
                aqi=Avg("aqi"),
                pm25=Avg("pm25"),
                pm10=Avg("pm10"),
                so2=Avg("so2"),
                no2=Avg("no2"),
                co=Avg("co"),
                o3=Avg("o3"),
            )
            .order_by("station__city__code")
        )

        map_rows = []
        for row in city_rows:
            aqi_int = to_int(row["aqi"])
            map_rows.append(
                {
                    "province_code": row["station__city__province__code"],
                    "province_name": row["station__city__province__name"],
                    "city_code": row["station__city__code"],
                    "city_name": row["station__city__name"],
                    "longitude": float(row["station__city__longitude"]),
                    "latitude": float(row["station__city__latitude"]),
                    "aqi": aqi_int,
                    "pm25": to_float(row["pm25"]),
                    "pm10": to_float(row["pm10"]),
                    "so2": to_float(row["so2"]),
                    "no2": to_float(row["no2"]),
                    "co": to_float(row["co"]),
                    "o3": to_float(row["o3"]),
                    "quality_level": calc_quality_level_from_aqi(aqi_int),
                }
            )

        payload = {
            "national": {
                "aqi": to_int(national["aqi"]),
                "pm25": to_float(national["pm25"]),
                "pm10": to_float(national["pm10"]),
                "so2": to_float(national["so2"]),
                "no2": to_float(national["no2"]),
                "co": to_float(national["co"]),
                "o3": to_float(national["o3"]),
                "quality_level": calc_quality_level_from_aqi(to_int(national["aqi"])),
            },
            "map_data": ProvinceCitySerializer(map_rows, many=True).data,
            "city_count": len(map_rows),
        }
        return APIResponse.success(data=payload)

    @action(detail=False, methods=["get"], url_path="top-cities")
    @method_decorator(cache_page(60))
    def top_cities(self, request):
        limit = _get_required_int_query_param(
            request=request, field="limit", default=10, min_value=1, max_value=50
        )
        latest_qs = get_latest_station_records_queryset()
        ranked_rows = list(
            latest_qs.values("station__city__code", "station__city__name")
            .annotate(aqi=Avg("aqi"))
            .order_by("aqi")
        )

        best = [
            {
                "city_code": row["station__city__code"],
                "city_name": row["station__city__name"],
                "aqi": to_int(row["aqi"]),
                "quality_level": calc_quality_level_from_aqi(to_int(row["aqi"])),
            }
            for row in ranked_rows[:limit]
        ]
        worst = [
            {
                "city_code": row["station__city__code"],
                "city_name": row["station__city__name"],
                "aqi": to_int(row["aqi"]),
                "quality_level": calc_quality_level_from_aqi(to_int(row["aqi"])),
            }
            for row in list(reversed(ranked_rows[-limit:]))
        ]

        return APIResponse.success(data={"best": best, "worst": worst})


class CityDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code: str):
        city = City.objects.select_related("province").filter(code=code).first()
        if city is None:
            return APIResponse.error(404, "城市不存在")

        snapshot = get_city_latest_snapshot(city)
        if snapshot is None:
            return APIResponse.error(404, "该城市暂无实时监测数据")

        return APIResponse.success(
            data={
                "city_code": city.code,
                "city_name": city.name,
                "province_code": city.province.code,
                "province_name": city.province.name,
                "longitude": float(city.longitude),
                "latitude": float(city.latitude),
                "snapshot": snapshot,
            }
        )


class CityTrendView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code: str):
        city = City.objects.select_related("province").filter(code=code).first()
        if city is None:
            return APIResponse.error(404, "城市不存在")

        hours = _get_required_int_query_param(
            request=request, field="hours", default=24, min_value=1, max_value=168
        )
        trend = get_city_hourly_trend(city, hours=hours)
        return APIResponse.success(
            data={
                "city_code": city.code,
                "city_name": city.name,
                "hours": hours,
                "trend": trend,
            }
        )


class StationDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code: str):
        station = (
            MonitoringStation.objects.select_related("city__province").filter(code=code).first()
        )
        if station is None:
            return APIResponse.error(404, "站点不存在")

        snapshot = get_station_latest_snapshot(station)
        if snapshot is None:
            return APIResponse.error(404, "该站点暂无实时监测数据")

        return APIResponse.success(
            data={
                "station_code": station.code,
                "station_name": station.name,
                "station_type": station.station_type,
                "address": station.address,
                "city_code": station.city.code,
                "city_name": station.city.name,
                "province_code": station.city.province.code,
                "province_name": station.city.province.name,
                "snapshot": snapshot,
            }
        )


class StationTrendView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code: str):
        station = (
            MonitoringStation.objects.select_related("city__province").filter(code=code).first()
        )
        if station is None:
            return APIResponse.error(404, "站点不存在")

        hours = _get_required_int_query_param(
            request=request, field="hours", default=24, min_value=1, max_value=168
        )
        trend = get_station_hourly_trend(station, hours=hours)
        return APIResponse.success(
            data={
                "station_code": station.code,
                "station_name": station.name,
                "hours": hours,
                "trend": trend,
            }
        )


class HistoricalDataViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    ordering_fields = {"monitor_time", "-monitor_time", "aqi", "-aqi"}

    def _get_filtered_queryset(self, request):
        queryset = AirQualityData.objects.select_related("station__city__province")
        filterset = HistoricalDataFilter(data=request.query_params, queryset=queryset)
        if not filterset.is_valid():
            _parse_filter_errors(filterset)
        return filterset.qs

    def list(self, request):
        page = _get_required_int_query_param(
            request=request, field="page", default=1, min_value=1, max_value=100_000
        )
        page_size = _get_required_int_query_param(
            request=request, field="page_size", default=20, min_value=1, max_value=200
        )
        ordering = request.query_params.get("ordering", "-monitor_time")
        if ordering not in self.ordering_fields:
            raise ValidationError("仅支持 monitor_time/-monitor_time/aqi/-aqi", field="ordering")

        queryset = self._get_filtered_queryset(request).order_by(ordering, "-id")
        total = queryset.count()
        items = queryset[(page - 1) * page_size : page * page_size]
        data = HistoricalAirQualitySerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        export_format = (request.query_params.get("format") or "csv").lower()
        if export_format not in {"csv", "xlsx"}:
            raise ValidationError("仅支持 csv/xlsx", field="format")

        queryset = self._get_filtered_queryset(request).order_by("-monitor_time", "-id")
        if not queryset.exists():
            return APIResponse.error(400, "没有可导出的数据")

        rows = list(
            queryset.values(
                "station__city__province__code",
                "station__city__province__name",
                "station__city__code",
                "station__city__name",
                "station__code",
                "station__name",
                "monitor_time",
                "aqi",
                "pm25",
                "pm10",
                "so2",
                "no2",
                "co",
                "o3",
                "quality_level",
            )
        )
        data_frame = pd.DataFrame(rows).rename(
            columns={
                "station__city__province__code": "province_code",
                "station__city__province__name": "province_name",
                "station__city__code": "city_code",
                "station__city__name": "city_name",
                "station__code": "station_code",
                "station__name": "station_name",
            }
        )

        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        if export_format == "csv":
            buffer = StringIO()
            data_frame.to_csv(buffer, index=False, encoding="utf-8-sig")
            response = HttpResponse(buffer.getvalue(), content_type="text/csv; charset=utf-8")
            response["Content-Disposition"] = f'attachment; filename="historical_data_{timestamp}.csv"'
            return response

        buffer = BytesIO()
        data_frame.to_excel(buffer, index=False)
        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="historical_data_{timestamp}.xlsx"'
        return response


class CityComparisonView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        city_codes = request.data.get("city_codes")
        if not isinstance(city_codes, list) or len(city_codes) < 2:
            raise ValidationError("至少提供 2 个城市代码", field="city_codes")
        if len(city_codes) > 10:
            raise ValidationError("最多支持 10 个城市对比", field="city_codes")

        normalized_codes = []
        for item in city_codes:
            code = str(item).strip()
            if code and code not in normalized_codes:
                normalized_codes.append(code)
        if len(normalized_codes) < 2:
            raise ValidationError("至少提供 2 个不同城市代码", field="city_codes")

        hours = request.data.get("hours", 24)
        try:
            hours = int(hours)
        except (TypeError, ValueError):
            raise ValidationError("格式错误，应为整数，范围 1-168", field="hours")
        if hours < 1 or hours > 168:
            raise ValidationError("超出范围，应为 1-168", field="hours")

        city_map = {
            city.code: city
            for city in City.objects.filter(code__in=normalized_codes).select_related("province")
        }
        missing_codes = [code for code in normalized_codes if code not in city_map]
        if missing_codes:
            return APIResponse.error(404, f"城市不存在: {', '.join(missing_codes)}")

        series = []
        for code in normalized_codes:
            city = city_map[code]
            series.append(
                {
                    "city_code": city.code,
                    "city_name": city.name,
                    "province_name": city.province.name,
                    "trend": get_city_hourly_trend(city, hours=hours),
                }
            )

        return APIResponse.success(data={"hours": hours, "series": series})


class CorrelationAnalysisView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pollutant_x = (request.query_params.get("pollutant_x") or "pm25").strip().lower()
        pollutant_y = (request.query_params.get("pollutant_y") or "pm10").strip().lower()
        if pollutant_x not in POLLUTANT_FIELDS:
            raise ValidationError(f"仅支持字段: {', '.join(POLLUTANT_FIELDS)}", field="pollutant_x")
        if pollutant_y not in POLLUTANT_FIELDS:
            raise ValidationError(f"仅支持字段: {', '.join(POLLUTANT_FIELDS)}", field="pollutant_y")
        if pollutant_x == pollutant_y:
            raise ValidationError("pollutant_x 与 pollutant_y 不能相同", field="pollutant_y")

        queryset = AirQualityData.objects.all()
        city_code = request.query_params.get("city_code")
        if city_code:
            queryset = queryset.filter(station__city__code=city_code.strip())

        start_date = _get_optional_date_query_param(request, "start_date")
        end_date = _get_optional_date_query_param(request, "end_date")
        if start_date:
            queryset = queryset.filter(monitor_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(monitor_time__date__lte=end_date)

        values = list(
            queryset.exclude(**{pollutant_x: None})
            .exclude(**{pollutant_y: None})
            .values(pollutant_x, pollutant_y)
        )
        if len(values) < 2:
            return APIResponse.success(
                data={
                    "pollutant_x": pollutant_x,
                    "pollutant_y": pollutant_y,
                    "sample_count": len(values),
                    "correlation": None,
                    "scatter_data": [],
                }
            )

        data_frame = pd.DataFrame(values)
        correlation = data_frame[pollutant_x].corr(data_frame[pollutant_y])
        if pd.isna(correlation):
            correlation = None
        else:
            correlation = round(float(correlation), 4)

        max_points = _get_required_int_query_param(
            request=request, field="max_points", default=2000, min_value=100, max_value=20_000
        )
        scatter_data = [
            {"x": float(item[pollutant_x]), "y": float(item[pollutant_y])}
            for item in values[:max_points]
        ]

        return APIResponse.success(
            data={
                "pollutant_x": pollutant_x,
                "pollutant_y": pollutant_y,
                "sample_count": len(values),
                "correlation": correlation,
                "scatter_data": scatter_data,
            }
        )


class AQIDistributionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = AirQualityData.objects.all()
        city_code = request.query_params.get("city_code")
        if city_code:
            queryset = queryset.filter(station__city__code=city_code.strip())

        start_date = _get_optional_date_query_param(request, "start_date")
        end_date = _get_optional_date_query_param(request, "end_date")
        if start_date:
            queryset = queryset.filter(monitor_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(monitor_time__date__lte=end_date)

        total = queryset.count()
        count_map = {
            item["quality_level"]: item["count"]
            for item in queryset.values("quality_level").annotate(count=Count("id"))
        }
        distribution = []
        for level, label in AirQualityData.QualityLevel.choices:
            count = int(count_map.get(level, 0))
            percentage = 0.0 if total == 0 else round((count * 100.0) / total, 2)
            distribution.append(
                {"quality_level": level, "quality_label": label, "count": count, "percentage": percentage}
            )

        return APIResponse.success(data={"total": total, "distribution": distribution})
