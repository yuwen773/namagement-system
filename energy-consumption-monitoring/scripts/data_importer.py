"""Phase 5 data importer with multi-format read, cleaning, and chunked import."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import math
from pathlib import Path
import sys
import time
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

import pandas as pd

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.config import ImportConfig, load_import_config, setup_django
from scripts.data_cleaner import CleaningReport, EnergyDataCleaner


@dataclass(frozen=True)
class ImportExecutionOptions:
    file_path: Path
    file_format: str | None = None
    batch_size: int | None = None
    mode: str = "orm"
    config_path: Path | None = None
    preview_rows: int | None = None
    api_base_url: str | None = None
    api_token: str | None = None
    api_endpoint: str | None = None
    checkpoint_file: Path = Path("tmp/import_checkpoint.json")
    resume: bool = False
    continue_on_error: bool = True
    dry_run: bool = False


@dataclass(frozen=True)
class ImportSummary:
    mode: str
    source_file: str
    source_rows: int
    valid_rows: int
    invalid_rows: int
    anomaly_rows: int
    chunk_count: int
    imported_rows: int
    skipped_rows: int
    failed_chunks: int
    duration_seconds: float
    rows_per_second: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "source_file": self.source_file,
            "source_rows": self.source_rows,
            "valid_rows": self.valid_rows,
            "invalid_rows": self.invalid_rows,
            "anomaly_rows": self.anomaly_rows,
            "chunk_count": self.chunk_count,
            "imported_rows": self.imported_rows,
            "skipped_rows": self.skipped_rows,
            "failed_chunks": self.failed_chunks,
            "duration_seconds": round(self.duration_seconds, 3),
            "rows_per_second": round(self.rows_per_second, 3),
        }


class MultiFormatDataReader:
    """Read CSV/Excel/JSON files to dataframe."""

    def read(self, file_path: Path, file_format: str | None = None) -> tuple[pd.DataFrame, str]:
        resolved_format = self._detect_format(file_path=file_path, file_format=file_format)

        if resolved_format == "csv":
            dataframe = pd.read_csv(file_path)
        elif resolved_format == "excel":
            dataframe = pd.read_excel(file_path)
        elif resolved_format == "json":
            dataframe = self._read_json(file_path)
        else:
            raise ValueError(f"Unsupported format: {resolved_format}")
        return dataframe, resolved_format

    def _detect_format(self, file_path: Path, file_format: str | None) -> str:
        if file_format:
            normalized = file_format.lower().strip()
            if normalized in {"csv", "excel", "json"}:
                return normalized
            raise ValueError("file_format must be one of csv/excel/json")

        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            return "csv"
        if suffix in {".xls", ".xlsx"}:
            return "excel"
        if suffix == ".json":
            return "json"
        raise ValueError(f"Cannot infer file format from suffix: {suffix}")

    def _read_json(self, file_path: Path) -> pd.DataFrame:
        content = json.loads(file_path.read_text(encoding="utf-8-sig"))
        if isinstance(content, list):
            return pd.DataFrame(content)
        if isinstance(content, dict) and isinstance(content.get("records"), list):
            return pd.DataFrame(content["records"])
        raise ValueError("JSON file must be an array or an object containing records array.")


class CheckpointStore:
    """Store chunk-level resume checkpoint."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, state: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()


class BatchImporter:
    """Chunked importer for ORM/API modes with progress and resume."""

    def __init__(
        self,
        config: ImportConfig,
        mode: str,
        batch_size: int,
        continue_on_error: bool,
        checkpoint_store: CheckpointStore,
    ):
        mode_value = mode.lower().strip()
        if mode_value not in {"orm", "api"}:
            raise ValueError("mode must be 'orm' or 'api'")
        self.config = config
        self.mode = mode_value
        self.batch_size = batch_size
        self.continue_on_error = continue_on_error
        self.checkpoint_store = checkpoint_store

    def import_dataframe(
        self,
        dataframe: pd.DataFrame,
        source_file: Path,
        resume: bool,
    ) -> tuple[int, int, int]:
        total_rows = len(dataframe.index)
        if total_rows == 0:
            return 0, 0, 0

        total_chunks = max(1, math.ceil(total_rows / self.batch_size))
        start_chunk = self._resolve_start_chunk(
            source_file=source_file,
            total_chunks=total_chunks,
            resume=resume,
        )

        imported_rows = 0
        skipped_rows = 0
        failed_chunks = 0
        started_at = time.time()

        for chunk_index in range(start_chunk, total_chunks):
            chunk_start = chunk_index * self.batch_size
            chunk_end = min(chunk_start + self.batch_size, total_rows)
            chunk_df = dataframe.iloc[chunk_start:chunk_end]
            chunk_records = chunk_df.to_dict(orient="records")
            chunk_size = len(chunk_records)

            try:
                imported_count, skipped_count = self._import_chunk(chunk_records)
                imported_rows += imported_count
                skipped_rows += skipped_count
                self._update_checkpoint(source_file, total_chunks, chunk_index + 1)
                elapsed = max(time.time() - started_at, 0.001)
                percent = round((chunk_end / total_rows) * 100, 2)
                rate = round((chunk_end / elapsed), 2)
                print(
                    f"[chunk {chunk_index + 1}/{total_chunks}] "
                    f"processed={chunk_end}/{total_rows} ({percent}%) "
                    f"imported={imported_rows} skipped={skipped_rows} rate={rate} rows/s"
                )
            except Exception as exc:  # noqa: BLE001
                failed_chunks += 1
                skipped_rows += chunk_size
                print(f"[chunk {chunk_index + 1}/{total_chunks}] failed: {exc}")
                if not self.continue_on_error:
                    raise

        if failed_chunks == 0:
            self.checkpoint_store.clear()
        return imported_rows, skipped_rows, failed_chunks

    def _resolve_start_chunk(self, source_file: Path, total_chunks: int, resume: bool) -> int:
        if not resume:
            self._update_checkpoint(source_file, total_chunks, 0)
            return 0

        state = self.checkpoint_store.load()
        if not state:
            self._update_checkpoint(source_file, total_chunks, 0)
            return 0

        fingerprint = self._build_fingerprint(source_file)
        if state.get("fingerprint") != fingerprint:
            print("checkpoint file exists but source file changed, restarting from chunk 0")
            self._update_checkpoint(source_file, total_chunks, 0)
            return 0

        saved_chunk = int(state.get("next_chunk_index", 0))
        if saved_chunk >= total_chunks:
            print("checkpoint indicates import already completed, restarting from chunk 0")
            self._update_checkpoint(source_file, total_chunks, 0)
            return 0
        print(f"resume enabled, continuing from chunk {saved_chunk + 1}/{total_chunks}")
        return saved_chunk

    def _update_checkpoint(self, source_file: Path, total_chunks: int, next_chunk_index: int) -> None:
        state = {
            "fingerprint": self._build_fingerprint(source_file),
            "mode": self.mode,
            "batch_size": self.batch_size,
            "total_chunks": total_chunks,
            "next_chunk_index": next_chunk_index,
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
        self.checkpoint_store.save(state)

    @staticmethod
    def _build_fingerprint(source_file: Path) -> dict[str, Any]:
        stat = source_file.stat()
        return {
            "path": str(source_file.resolve()),
            "size": stat.st_size,
            "mtime": stat.st_mtime,
        }

    def _import_chunk(self, records: list[dict[str, Any]]) -> tuple[int, int]:
        if self.mode == "orm":
            return self._import_chunk_via_orm(records)
        return self._import_chunk_via_api(records)

    def _import_chunk_via_api(self, records: list[dict[str, Any]]) -> tuple[int, int]:
        payload = {
            "format": "json",
            "records": [self._serialize_api_record(record) for record in records],
        }
        url = self.config.api.base_url.rstrip("/") + self.config.api.endpoint
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.config.api.token:
            headers["Authorization"] = f"Bearer {self.config.api.token}"

        req = urllib_request.Request(url=url, data=data, headers=headers, method="POST")
        try:
            with urllib_request.urlopen(req, timeout=self.config.api.timeout_sec) as response:
                body = response.read().decode("utf-8")
        except urllib_error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"API import failed with HTTP {exc.code}: {details}") from exc
        except urllib_error.URLError as exc:
            raise RuntimeError(f"API import failed: {exc}") from exc

        parsed = json.loads(body)
        if isinstance(parsed, dict) and "code" in parsed:
            if int(parsed.get("code", 1)) != 0:
                raise RuntimeError(f"API response code is not success: {parsed}")
            data_node = parsed.get("data") or {}
            imported = int(data_node.get("imported_count", 0))
            submitted = int(data_node.get("submitted_count", len(records)))
            skipped = max(submitted - imported, 0)
            return imported, skipped

        imported = int(parsed.get("imported_count", 0))
        submitted = int(parsed.get("submitted_count", len(records)))
        skipped = max(submitted - imported, 0)
        return imported, skipped

    def _import_chunk_via_orm(self, records: list[dict[str, Any]]) -> tuple[int, int]:
        setup_django()
        from django.db import transaction
        from django.db.models import Q
        from django.utils import timezone

        from apps.devices.models import Device, EnergyType
        from apps.energy.models import EnergyData

        devices = list(Device.objects.select_related("energy_type").all())
        device_map = {str(item.pk): item for item in devices}
        device_map.update({item.device_id: item for item in devices})

        energy_types = list(EnergyType.objects.all())
        energy_type_map = {str(item.pk): item for item in energy_types}
        energy_type_map.update({item.code.upper(): item for item in energy_types})

        chunk_instances = []
        skipped = 0

        for record in records:
            try:
                device = self._resolve_device(record, device_map=device_map)
                energy_type = self._resolve_energy_type(
                    record,
                    device_energy_type=device.energy_type,
                    energy_type_map=energy_type_map,
                )
                timestamp = self._resolve_timestamp(record, timezone)
                instance = EnergyData(
                    device=device,
                    energy_type=energy_type,
                    timestamp=timestamp,
                    value=record["value"],
                    voltage=record.get("voltage"),
                    current=record.get("current"),
                    power=record.get("power"),
                    flow_rate=record.get("flow_rate"),
                )
                chunk_instances.append(instance)
            except Exception:
                skipped += 1

        if not chunk_instances:
            return 0, skipped

        with transaction.atomic():
            before = EnergyData.objects.count()
            EnergyData.objects.bulk_create(
                chunk_instances,
                batch_size=self.batch_size,
                ignore_conflicts=True,
            )
            after = EnergyData.objects.count()

            latest_map: dict[int, Any] = {}
            for item in chunk_instances:
                latest_ts = latest_map.get(item.device_id)
                if latest_ts is None or latest_ts < item.timestamp:
                    latest_map[item.device_id] = item.timestamp
            for device_pk, ts in latest_map.items():
                Device.objects.filter(pk=device_pk).filter(
                    Q(last_data_time__isnull=True) | Q(last_data_time__lt=ts)
                ).update(last_data_time=ts)

        imported = max(after - before, 0)
        skipped += max(len(chunk_instances) - imported, 0)
        return imported, skipped

    def _resolve_device(self, record: dict[str, Any], device_map: dict[str, Any]):
        device_raw = record.get("device")
        key = str(device_raw).strip() if device_raw is not None else ""
        if not key:
            raise ValueError("missing device")
        device = device_map.get(key)
        if not device:
            raise ValueError(f"device not found: {key}")
        return device

    def _resolve_energy_type(
        self,
        record: dict[str, Any],
        device_energy_type: Any,
        energy_type_map: dict[str, Any],
    ):
        value = record.get("energy_type")
        if value in (None, ""):
            return device_energy_type
        key = str(value).strip().upper()
        energy_type = energy_type_map.get(key)
        if not energy_type:
            raise ValueError(f"energy type not found: {value}")
        if energy_type.id != device_energy_type.id:
            raise ValueError("energy_type and device mapping mismatch")
        return energy_type

    @staticmethod
    def _resolve_timestamp(record: dict[str, Any], timezone_module):
        value = record.get("timestamp")
        if isinstance(value, pd.Timestamp):
            dt = value.to_pydatetime()
        elif isinstance(value, datetime):
            dt = value
        else:
            parsed = pd.to_datetime(value, errors="coerce")
            if pd.isna(parsed):
                raise ValueError("invalid timestamp")
            dt = parsed.to_pydatetime()
        if timezone_module.is_naive(dt):
            return timezone_module.make_aware(dt, timezone_module.get_current_timezone())
        return dt

    @staticmethod
    def _serialize_api_record(record: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        for key in ("device", "energy_type", "timestamp", "value", "voltage", "current", "power", "flow_rate"):
            value = record.get(key)
            if isinstance(value, pd.Timestamp):
                normalized[key] = value.isoformat()
            elif hasattr(value, "item"):
                normalized[key] = value.item()
            elif isinstance(value, float) and math.isnan(value):
                normalized[key] = None
            else:
                normalized[key] = value
        return normalized


def run_import_job(options: ImportExecutionOptions) -> tuple[CleaningReport, ImportSummary]:
    config = load_import_config(options.config_path)
    config = _apply_cli_overrides(config, options)

    reader = MultiFormatDataReader()
    raw_df, detected_format = reader.read(options.file_path, options.file_format)
    print(
        f"loaded {len(raw_df.index)} rows from {options.file_path} (format={detected_format}, "
        f"columns={list(raw_df.columns)})"
    )
    preview_rows = options.preview_rows if options.preview_rows is not None else config.preview_rows
    if preview_rows > 0 and len(raw_df.index) > 0:
        print("data preview:")
        print(raw_df.head(preview_rows).to_string(index=False))

    cleaner = EnergyDataCleaner(config=config)
    cleaned_df, clean_report = cleaner.clean(raw_df, drop_invalid=True)
    print(f"cleaning report: {json.dumps(clean_report.to_dict(), ensure_ascii=False)}")

    if options.dry_run:
        summary = ImportSummary(
            mode=options.mode,
            source_file=str(options.file_path),
            source_rows=clean_report.source_rows,
            valid_rows=clean_report.valid_rows,
            invalid_rows=clean_report.invalid_rows,
            anomaly_rows=clean_report.anomaly_rows,
            chunk_count=0,
            imported_rows=0,
            skipped_rows=clean_report.invalid_rows,
            failed_chunks=0,
            duration_seconds=0,
            rows_per_second=0,
        )
        return clean_report, summary

    batch_size = options.batch_size or config.default_batch_size
    checkpoint_store = CheckpointStore(path=options.checkpoint_file)
    importer = BatchImporter(
        config=config,
        mode=options.mode,
        batch_size=batch_size,
        continue_on_error=options.continue_on_error,
        checkpoint_store=checkpoint_store,
    )

    started_at = time.time()
    imported_rows, skipped_rows, failed_chunks = importer.import_dataframe(
        dataframe=cleaned_df,
        source_file=options.file_path,
        resume=options.resume,
    )
    duration = max(time.time() - started_at, 0.001)
    rows_per_second = imported_rows / duration
    chunk_count = max(1, math.ceil(max(len(cleaned_df.index), 1) / batch_size))
    summary = ImportSummary(
        mode=options.mode,
        source_file=str(options.file_path),
        source_rows=clean_report.source_rows,
        valid_rows=clean_report.valid_rows,
        invalid_rows=clean_report.invalid_rows,
        anomaly_rows=clean_report.anomaly_rows,
        chunk_count=chunk_count,
        imported_rows=imported_rows,
        skipped_rows=skipped_rows + clean_report.invalid_rows,
        failed_chunks=failed_chunks,
        duration_seconds=duration,
        rows_per_second=rows_per_second,
    )
    return clean_report, summary


def _apply_cli_overrides(config: ImportConfig, options: ImportExecutionOptions) -> ImportConfig:
    api = config.api
    if options.api_base_url:
        api = api.__class__(
            base_url=options.api_base_url.rstrip("/"),
            endpoint=api.endpoint,
            timeout_sec=api.timeout_sec,
            token=api.token,
        )
    if options.api_endpoint:
        api = api.__class__(
            base_url=api.base_url,
            endpoint=options.api_endpoint,
            timeout_sec=api.timeout_sec,
            token=api.token,
        )
    if options.api_token:
        api = api.__class__(
            base_url=api.base_url,
            endpoint=api.endpoint,
            timeout_sec=api.timeout_sec,
            token=options.api_token,
        )
    return ImportConfig(
        default_batch_size=config.default_batch_size,
        preview_rows=config.preview_rows,
        timezone=config.timezone,
        required_columns=config.required_columns,
        target_columns=config.target_columns,
        column_aliases=config.column_aliases,
        numeric_ranges=config.numeric_ranges,
        api=api,
        device_mapping=config.device_mapping,
        energy_type_mapping=config.energy_type_mapping,
    )


def build_arg_parser():
    import argparse

    parser = argparse.ArgumentParser(description="Import energy data from CSV/Excel/JSON files.")
    parser.add_argument("file_path", type=Path, help="Path to source file")
    parser.add_argument("--format", choices=["csv", "excel", "json"], default=None, help="Explicit file format")
    parser.add_argument("--mode", choices=["orm", "api"], default="orm", help="Import mode")
    parser.add_argument("--batch-size", type=int, default=None, help="Rows per chunk")
    parser.add_argument("--preview", type=int, default=None, help="Rows for preview output")
    parser.add_argument("--config", type=Path, default=None, help="Import config JSON path")
    parser.add_argument("--api-base-url", default=None, help="Base URL for API mode")
    parser.add_argument("--api-endpoint", default=None, help="Batch import endpoint for API mode")
    parser.add_argument("--api-token", default=None, help="JWT token for API mode")
    parser.add_argument(
        "--checkpoint-file",
        type=Path,
        default=Path("tmp/import_checkpoint.json"),
        help="Checkpoint file path for resume",
    )
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    error_group = parser.add_mutually_exclusive_group()
    error_group.add_argument(
        "--continue-on-error",
        dest="continue_on_error",
        action="store_true",
        default=True,
        help="Continue when chunk import fails (default)",
    )
    error_group.add_argument(
        "--stop-on-error",
        dest="continue_on_error",
        action="store_false",
        help="Stop immediately when chunk import fails",
    )
    parser.add_argument("--dry-run", action="store_true", help="Read and clean only, do not import")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    options = ImportExecutionOptions(
        file_path=args.file_path,
        file_format=args.format,
        mode=args.mode,
        batch_size=args.batch_size,
        preview_rows=args.preview,
        config_path=args.config,
        api_base_url=args.api_base_url,
        api_endpoint=args.api_endpoint,
        api_token=args.api_token,
        checkpoint_file=args.checkpoint_file,
        resume=args.resume,
        continue_on_error=bool(args.continue_on_error),
        dry_run=args.dry_run,
    )
    _, summary = run_import_job(options)
    print(f"import summary: {json.dumps(summary.to_dict(), ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
