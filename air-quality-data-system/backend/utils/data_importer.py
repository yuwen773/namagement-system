"""
Data import utilities (Phase 1 - Step 1.3.1).

Responsibilities:
- Parse CSV/Excel
- Validate required columns and value ranges
- Bulk insert with chunking
- Collect per-row errors and persist ImportTaskLog

Note:
- AirQualityData.save() is bypassed by bulk_create, so quality_level must be precomputed.
"""

from __future__ import annotations

import json
import logging
import os
import re
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from django.conf import settings
from django.db import IntegrityError, close_old_connections, transaction
from django.utils import timezone

from apps.airquality.models import AirQualityData, City, MonitoringStation, Province
from apps.logs.models import ErrorLog, ImportTask, ImportTaskLog

logger = logging.getLogger(__name__)


EXECUTOR = ThreadPoolExecutor(max_workers=int(os.getenv("DATA_IMPORT_MAX_WORKERS", "2")))


def _canon(s: str) -> str:
    s = str(s).strip()
    # Normalize common full-width punctuation and units into ASCII forms.
    s = (
        s.replace("（", "(")
        .replace("）", ")")
        .replace("／", "/")
        .replace("，", ",")
        .replace("：", ":")
        .replace("µ", "u")
        .replace("μ", "u")
        .replace("³", "3")
        .replace("℃", "c")
    )
    s = s.lower()
    s = re.sub(r"\s+", "", s)
    return s


def _safe_snippet(row_dict: Dict[str, Any], limit: int = 1000) -> str:
    text = json.dumps(row_dict, ensure_ascii=True, default=str)
    if len(text) > limit:
        return text[:limit] + "..."
    return text


def _parse_decimal(value: Any) -> Optional[Decimal]:
    if value is None:
        return None
    # pandas may give NaN float
    try:
        if isinstance(value, float) and value != value:
            return None
    except Exception:
        pass
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        return None
    try:
        d = Decimal(s)
    except (InvalidOperation, ValueError):
        # Try float -> str
        try:
            d = Decimal(str(float(s)))
        except Exception as e:
            raise ValueError(f"not a decimal: {value}") from e
    return d


def _parse_int(value: Any) -> int:
    if value is None:
        raise ValueError("missing")
    try:
        if isinstance(value, float) and value != value:
            raise ValueError("missing")
    except Exception:
        pass
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        raise ValueError("missing")
    try:
        return int(Decimal(s))
    except Exception as e:
        raise ValueError(f"not an int: {value}") from e


def _parse_dt(value: Any) -> datetime:
    if value is None:
        raise ValueError("missing")
    # pandas Timestamp has to_pydatetime()
    if hasattr(value, "to_pydatetime"):
        dt = value.to_pydatetime()
    else:
        s = str(value).strip()
        if s == "" or s.lower() in {"nan", "none", "null"}:
            raise ValueError("missing")
        # Accept ISO-like strings.
        try:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            # Common fallback.
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
                try:
                    dt = datetime.strptime(s, fmt)
                    break
                except ValueError:
                    dt = None  # type: ignore[assignment]
            if dt is None:
                raise ValueError(f"invalid datetime: {value}")

    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


@dataclass(frozen=True)
class ImportTemplate:
    name: str
    required_fields: Tuple[str, ...]
    field_aliases: Dict[str, Tuple[str, ...]]

    def map_columns(self, input_columns: Iterable[str]) -> Dict[str, str]:
        canon_to_original: Dict[str, str] = {_canon(c): c for c in input_columns}
        mapped: Dict[str, str] = {}
        for field, aliases in self.field_aliases.items():
            for a in aliases:
                key = _canon(a)
                if key in canon_to_original:
                    mapped[field] = canon_to_original[key]
                    break
        return mapped

    def missing_required(self, mapped_fields: Dict[str, str]) -> List[str]:
        missing = []
        for f in self.required_fields:
            if f not in mapped_fields:
                missing.append(f)
        return missing


TEMPLATES: Dict[str, ImportTemplate] = {
    "provinces": ImportTemplate(
        name="provinces",
        required_fields=("code", "name", "level"),
        field_aliases={
            "code": ("code", "province_code", "省代码", "省份代码"),
            "name": ("name", "province_name", "省名", "省份", "省份名称"),
            "level": ("level", "province_level", "行政级别"),
        },
    ),
    "cities": ImportTemplate(
        name="cities",
        required_fields=("code", "name", "province_code", "longitude", "latitude"),
        field_aliases={
            "code": ("code", "city_code", "市代码", "城市代码"),
            "name": ("name", "city_name", "市名", "城市", "城市名称"),
            "province_code": ("province_code", "省代码", "省份代码"),
            "longitude": ("longitude", "lng", "经度"),
            "latitude": ("latitude", "lat", "纬度"),
        },
    ),
    "stations": ImportTemplate(
        name="stations",
        required_fields=("code", "name", "city_code", "address", "station_type"),
        field_aliases={
            "code": ("code", "station_code", "站点编码", "站点代码"),
            "name": ("name", "station_name", "站点名称"),
            "city_code": ("city_code", "市代码", "城市代码"),
            "address": ("address", "站点地址", "地址"),
            "station_type": ("station_type", "type", "站点类型"),
        },
    ),
    "air_quality_data": ImportTemplate(
        name="air_quality_data",
        required_fields=("station_code", "monitor_time", "aqi"),
        field_aliases={
            "station_code": ("station_code", "station", "station_id", "stationid", "站点编码", "站点代码"),
            "monitor_time": ("monitor_time", "monitortime", "time", "datetime", "timestamp", "监测时间", "时间"),
            "aqi": ("aqi",),
            "pm25": ("pm25", "pm2.5", "pm2.5(ug/m3)", "pm2_5", "pm2.5ugm3"),
            "pm10": ("pm10", "pm10(ug/m3)", "pm10ugm3"),
            "so2": ("so2", "so2(ug/m3)"),
            "no2": ("no2", "no2(ug/m3)"),
            "co": ("co", "co(mg/m3)", "co(mg/m³)"),
            "o3": ("o3", "o3(ug/m3)"),
        },
    ),
}


def submit_import_task(task_id: str, dataset_type: str, file_path: str, chunk_size: int = 2000) -> None:
    EXECUTOR.submit(run_import_task, task_id=task_id, dataset_type=dataset_type, file_path=file_path, chunk_size=chunk_size)


def run_import_task(task_id: str, dataset_type: str, file_path: str, chunk_size: int = 2000) -> None:
    close_old_connections()
    try:
        task = ImportTask.objects.get(task_id=task_id)
    except ImportTask.DoesNotExist:
        logger.error("ImportTask not found: %s", task_id)
        return

    task.status = ImportTask.Status.RUNNING
    task.save(update_fields=["status"])

    try:
        template = TEMPLATES.get(dataset_type)
        if not template:
            raise ValueError(f"unknown dataset_type: {dataset_type}")

        ext = Path(file_path).suffix.lower()
        total, success, failed = _import_file_by_template(
            template=template,
            dataset_type=dataset_type,
            file_path=file_path,
            ext=ext,
            task=task,
            chunk_size=chunk_size,
        )

        task.total_count = total
        task.success_count = success
        task.failed_count = failed
        # "FAILED" is reserved for task-level failures (parse errors, unexpected exceptions).
        # Row-level validation failures are reflected in failed_count + ImportTaskLog.
        task.status = ImportTask.Status.SUCCESS
        task.end_time = timezone.now()
        task.save(update_fields=["total_count", "success_count", "failed_count", "status", "end_time"])
    except Exception as exc:
        task.status = ImportTask.Status.FAILED
        task.end_time = timezone.now()
        task.save(update_fields=["status", "end_time"])

        ErrorLog.objects.create(
            error_type=exc.__class__.__name__,
            error_message=str(exc),
            stack_trace=traceback.format_exc(),
        )
        logger.exception("Import failed: %s", task_id)
    finally:
        close_old_connections()


def _import_file_by_template(
    *,
    template: ImportTemplate,
    dataset_type: str,
    file_path: str,
    ext: str,
    task: ImportTask,
    chunk_size: int,
) -> Tuple[int, int, int]:
    try:
        import pandas as pd  # type: ignore
    except Exception as e:
        raise RuntimeError("pandas is required for data import") from e

    if ext not in {".csv", ".xlsx", ".xls"}:
        raise ValueError(f"unsupported file type: {ext}")

    total = 0
    success = 0
    failed = 0

    def process_df(df, base_row_number: int) -> Tuple[int, int, int]:
        nonlocal total, success, failed
        if df is None or df.empty:
            return (0, 0, 0)

        mapped = template.map_columns(df.columns)
        missing = template.missing_required(mapped)
        if missing:
            # Missing required columns is a file-level error: log once.
            ImportTaskLog.objects.create(
                task=task,
                row_number=1,
                error_reason=f"缺失必填列: {', '.join(missing)}",
                raw_data_snippet=None,
            )
            raise ValueError(f"missing required columns: {missing}")

        # Rename input columns to internal field names we use downstream.
        rename_map = {v: k for k, v in mapped.items()}
        df = df.rename(columns=rename_map)

        # Ensure all known fields exist; missing optional fields -> None.
        for field in template.field_aliases.keys():
            if field not in df.columns:
                df[field] = None

        rows = df.to_dict(orient="records")
        total += len(rows)

        if dataset_type == "provinces":
            s, f = _import_provinces(task, rows, base_row_number)
        elif dataset_type == "cities":
            s, f = _import_cities(task, rows, base_row_number)
        elif dataset_type == "stations":
            s, f = _import_stations(task, rows, base_row_number)
        elif dataset_type == "air_quality_data":
            s, f = _import_air_quality_data(task, rows, base_row_number, chunk_size=chunk_size)
        else:
            raise ValueError(f"unknown dataset_type: {dataset_type}")

        success += s
        failed += f
        task.total_count = total
        task.success_count = success
        task.failed_count = failed
        task.save(update_fields=["total_count", "success_count", "failed_count"])
        return (len(rows), s, f)

    if ext == ".csv":
        # CSV: stream in chunks to support large files.
        encodings = ["utf-8-sig", "utf-8", "gbk"]
        reader = None
        last_err = None
        for enc in encodings:
            try:
                reader = pd.read_csv(file_path, chunksize=chunk_size, encoding=enc)
                # Smoke read first chunk to validate encoding.
                first = next(iter(reader))
                # Re-create iterator (pandas chunk iterators can't be rewound).
                reader = pd.read_csv(file_path, chunksize=chunk_size, encoding=enc)
                break
            except Exception as e:
                last_err = e
                reader = None
        if reader is None:
            raise ValueError(f"failed to read csv: {last_err}")

        row_base = 2  # header is row 1
        for chunk in reader:
            process_df(chunk, row_base)
            row_base += len(chunk)
    else:
        # Excel: read all (most Excel files are not huge in this project context).
        engine = "openpyxl" if ext == ".xlsx" else "xlrd"
        df = pd.read_excel(file_path, engine=engine)
        process_df(df, 2)

    return total, success, failed


def _bulk_log_errors(task: ImportTask, items: List[Tuple[int, str, Optional[str]]]) -> None:
    if not items:
        return
    logs = [
        ImportTaskLog(task=task, row_number=row, error_reason=reason, raw_data_snippet=snippet)
        for (row, reason, snippet) in items
    ]
    ImportTaskLog.objects.bulk_create(logs, batch_size=1000)


def _import_provinces(task: ImportTask, rows: List[Dict[str, Any]], base_row_number: int) -> Tuple[int, int]:
    errors: List[Tuple[int, str, Optional[str]]] = []
    to_create: List[Province] = []
    existing = set(Province.objects.values_list("code", flat=True))
    for idx, r in enumerate(rows):
        row_num = base_row_number + idx
        code = str(r.get("code", "")).strip()
        name = str(r.get("name", "")).strip()
        level = str(r.get("level", "")).strip()
        if not code or not name or not level:
            errors.append((row_num, "code/name/level 为必填", _safe_snippet(r)))
            continue
        if code in existing:
            errors.append((row_num, f"省代码重复: {code}", _safe_snippet(r)))
            continue
        p = Province(code=code, name=name, level=level)
        try:
            p.full_clean()
        except Exception as e:
            errors.append((row_num, f"校验失败: {e}", _safe_snippet(r)))
            continue
        to_create.append(p)
        existing.add(code)

    with transaction.atomic():
        Province.objects.bulk_create(to_create, batch_size=2000)
    _bulk_log_errors(task, errors)
    return (len(to_create), len(errors))


def _import_cities(task: ImportTask, rows: List[Dict[str, Any]], base_row_number: int) -> Tuple[int, int]:
    errors: List[Tuple[int, str, Optional[str]]] = []
    to_create: List[City] = []
    existing = set(City.objects.values_list("code", flat=True))
    province_by_code = {p.code: p for p in Province.objects.all()}

    for idx, r in enumerate(rows):
        row_num = base_row_number + idx
        code = str(r.get("code", "")).strip()
        name = str(r.get("name", "")).strip()
        province_code = str(r.get("province_code", "")).strip()
        if not code or not name or not province_code:
            errors.append((row_num, "code/name/province_code 为必填", _safe_snippet(r)))
            continue
        if code in existing:
            errors.append((row_num, f"市代码重复: {code}", _safe_snippet(r)))
            continue
        province = province_by_code.get(province_code)
        if not province:
            errors.append((row_num, f"找不到省份: {province_code}", _safe_snippet(r)))
            continue
        try:
            lng = _parse_decimal(r.get("longitude"))
            lat = _parse_decimal(r.get("latitude"))
            if lng is None or lat is None:
                raise ValueError("longitude/latitude 为必填且必须为数字")
        except Exception as e:
            errors.append((row_num, f"经纬度解析失败: {e}", _safe_snippet(r)))
            continue
        c = City(code=code, name=name, province=province, longitude=lng, latitude=lat)
        try:
            c.full_clean()
        except Exception as e:
            errors.append((row_num, f"校验失败: {e}", _safe_snippet(r)))
            continue
        to_create.append(c)
        existing.add(code)

    with transaction.atomic():
        City.objects.bulk_create(to_create, batch_size=2000)
    _bulk_log_errors(task, errors)
    return (len(to_create), len(errors))


def _import_stations(task: ImportTask, rows: List[Dict[str, Any]], base_row_number: int) -> Tuple[int, int]:
    errors: List[Tuple[int, str, Optional[str]]] = []
    to_create: List[MonitoringStation] = []
    existing = set(MonitoringStation.objects.values_list("code", flat=True))
    city_by_code = {c.code: c for c in City.objects.all()}

    for idx, r in enumerate(rows):
        row_num = base_row_number + idx
        code = str(r.get("code", "")).strip()
        name = str(r.get("name", "")).strip()
        city_code = str(r.get("city_code", "")).strip()
        address = str(r.get("address", "")).strip()
        station_type = str(r.get("station_type", "")).strip()
        if not code or not name or not city_code or not address or not station_type:
            errors.append((row_num, "code/name/city_code/address/station_type 为必填", _safe_snippet(r)))
            continue
        if code in existing:
            errors.append((row_num, f"站点编码重复: {code}", _safe_snippet(r)))
            continue
        city = city_by_code.get(city_code)
        if not city:
            errors.append((row_num, f"找不到城市: {city_code}", _safe_snippet(r)))
            continue
        s = MonitoringStation(
            code=code,
            name=name,
            city=city,
            address=address,
            station_type=station_type,
        )
        try:
            s.full_clean()
        except Exception as e:
            errors.append((row_num, f"校验失败: {e}", _safe_snippet(r)))
            continue
        to_create.append(s)
        existing.add(code)

    with transaction.atomic():
        MonitoringStation.objects.bulk_create(to_create, batch_size=2000)
    _bulk_log_errors(task, errors)
    return (len(to_create), len(errors))


def _import_air_quality_data(
    task: ImportTask,
    rows: List[Dict[str, Any]],
    base_row_number: int,
    *,
    chunk_size: int,
) -> Tuple[int, int]:
    errors: List[Tuple[int, str, Optional[str]]] = []
    to_create: List[AirQualityData] = []

    station_codes = {str(r.get("station_code", "")).strip() for r in rows if str(r.get("station_code", "")).strip()}
    station_map = {s.code: s for s in MonitoringStation.objects.filter(code__in=station_codes)}

    def flush(batch: List[AirQualityData], batch_row_nums: List[int]) -> Tuple[int, int]:
        if not batch:
            return (0, 0)
        try:
            with transaction.atomic():
                AirQualityData.objects.bulk_create(batch, batch_size=2000)
            return (len(batch), 0)
        except IntegrityError:
            # Fallback to per-row inserts to isolate duplicates/invalid constraints.
            ok = 0
            bad = 0
            for i, obj in enumerate(batch):
                row_num = batch_row_nums[i]
                try:
                    with transaction.atomic():
                        obj.save()
                    ok += 1
                except Exception as e:
                    bad += 1
                    errors.append((row_num, f"写入失败: {e}", None))
            return (ok, bad)

    batch_objs: List[AirQualityData] = []
    batch_rows: List[int] = []
    inserted = 0
    rejected = 0

    for idx, r in enumerate(rows):
        row_num = base_row_number + idx
        code = str(r.get("station_code", "")).strip()
        if not code:
            rejected += 1
            errors.append((row_num, "station_code 为必填", _safe_snippet(r)))
            continue
        station = station_map.get(code)
        if not station:
            rejected += 1
            errors.append((row_num, f"找不到站点: {code}（请先导入/创建站点基础数据）", _safe_snippet(r)))
            continue

        try:
            monitor_time = _parse_dt(r.get("monitor_time"))
        except Exception as e:
            rejected += 1
            errors.append((row_num, f"monitor_time 解析失败: {e}", _safe_snippet(r)))
            continue

        try:
            aqi = _parse_int(r.get("aqi"))
            if not (0 <= aqi <= 500):
                raise ValueError("AQI 必须在 0-500")
        except Exception as e:
            rejected += 1
            errors.append((row_num, f"aqi 解析失败: {e}", _safe_snippet(r)))
            continue

        try:
            pm25 = _parse_decimal(r.get("pm25"))
            pm10 = _parse_decimal(r.get("pm10"))
            so2 = _parse_decimal(r.get("so2"))
            no2 = _parse_decimal(r.get("no2"))
            co = _parse_decimal(r.get("co"))
            o3 = _parse_decimal(r.get("o3"))
            for name, v in (("pm25", pm25), ("pm10", pm10), ("so2", so2), ("no2", no2), ("co", co), ("o3", o3)):
                if v is not None and v < 0:
                    raise ValueError(f"{name} must be >= 0")
        except Exception as e:
            rejected += 1
            errors.append((row_num, f"污染物解析失败: {e}", _safe_snippet(r)))
            continue

        obj = AirQualityData(
            station=station,
            monitor_time=monitor_time,
            aqi=aqi,
            pm25=pm25,
            pm10=pm10,
            so2=so2,
            no2=no2,
            co=co,
            o3=o3,
            quality_level=AirQualityData._calc_quality_level(int(aqi)),
        )
        try:
            obj.full_clean()
        except Exception as e:
            rejected += 1
            errors.append((row_num, f"校验失败: {e}", _safe_snippet(r)))
            continue

        batch_objs.append(obj)
        batch_rows.append(row_num)

        if len(batch_objs) >= chunk_size:
            ok, bad = flush(batch_objs, batch_rows)
            inserted += ok
            rejected += bad
            batch_objs = []
            batch_rows = []

    if batch_objs:
        ok, bad = flush(batch_objs, batch_rows)
        inserted += ok
        rejected += bad

    _bulk_log_errors(task, errors)
    return (inserted, rejected)
