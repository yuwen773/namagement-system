"""Unified scheduler for Modbus/BACnet collectors with DB persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import sys
import time
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.config import setup_django
from scripts.protocol_collection.config import CollectionPolicy
from scripts.protocol_collectors.bacnet_collector import BacnetCollector, BacnetCollectorConfig
from scripts.protocol_collectors.modbus_collector import ModbusCollector, ModbusCollectorConfig


@dataclass(frozen=True)
class RunnerOutputConfig:
    batch_size: int = 500
    write_jsonl: bool = True
    jsonl_path: str = "scripts/protocol_collectors/output/collected_energy_data.jsonl"
    write_database: bool = True


@dataclass(frozen=True)
class RunnerConfig:
    policy: CollectionPolicy
    output: RunnerOutputConfig
    modbus_collectors: list[ModbusCollectorConfig]
    bacnet_collectors: list[BacnetCollectorConfig]


def load_runner_config(path: str | Path) -> RunnerConfig:
    raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    policy_raw = raw.get("policy", {})
    output_raw = raw.get("output", {})

    policy = CollectionPolicy(
        sample_interval_sec=float(policy_raw.get("sample_interval_sec", 5)),
        request_timeout_sec=float(policy_raw.get("request_timeout_sec", 2)),
        retry_times=int(policy_raw.get("retry_times", 3)),
        retry_backoff_sec=float(policy_raw.get("retry_backoff_sec", 1)),
        reconnect_interval_sec=float(policy_raw.get("reconnect_interval_sec", 2)),
    )
    output = RunnerOutputConfig(
        batch_size=int(output_raw.get("batch_size", 500)),
        write_jsonl=bool(output_raw.get("write_jsonl", True)),
        jsonl_path=str(output_raw.get("jsonl_path", "scripts/protocol_collectors/output/collected_energy_data.jsonl")),
        write_database=bool(output_raw.get("write_database", True)),
    )

    modbus_collectors = [_parse_modbus_collector(item) for item in raw.get("modbus_collectors", [])]
    bacnet_collectors = [_parse_bacnet_collector(item) for item in raw.get("bacnet_collectors", [])]
    if not modbus_collectors and not bacnet_collectors:
        raise ValueError("collector config must include at least one modbus_collectors or bacnet_collectors item")

    return RunnerConfig(
        policy=policy,
        output=output,
        modbus_collectors=modbus_collectors,
        bacnet_collectors=bacnet_collectors,
    )


def _parse_modbus_collector(raw: dict[str, Any]) -> ModbusCollectorConfig:
    return ModbusCollectorConfig(
        meter_id=str(raw["meter_id"]),
        device=str(raw["device"]),
        room=str(raw.get("room", "")),
        host=str(raw.get("host", "127.0.0.1")),
        port=int(raw["port"]),
        energy_type=str(raw.get("energy_type", "ELECTRICITY")),
        gateway_mode=str(raw.get("gateway_mode", "direct_meter")),
        point_map=raw.get("point_map"),
    )


def _parse_bacnet_collector(raw: dict[str, Any]) -> BacnetCollectorConfig:
    return BacnetCollectorConfig(
        meter_id=str(raw["meter_id"]),
        device=str(raw["device"]),
        room=str(raw.get("room", "")),
        host=str(raw.get("host", "127.0.0.1")),
        port=int(raw["port"]),
        energy_type=str(raw.get("energy_type", "WATER")),
        gateway_mode=str(raw.get("gateway_mode", "gateway_forward")),
        point_map=raw.get("point_map"),
    )


def run_collectors(
    config: RunnerConfig,
    iterations: int,
    flush_size: int | None = None,
) -> dict[str, int]:
    flush_batch_size = flush_size or config.output.batch_size
    collectors: list[Any] = []
    for item in config.modbus_collectors:
        collectors.append(ModbusCollector(item, policy=config.policy))
    for item in config.bacnet_collectors:
        collectors.append(BacnetCollector(item, policy=config.policy))

    pending_records: list[dict[str, Any]] = []
    total_collected = 0
    total_imported = 0
    total_skipped = 0
    total_failed = 0

    jsonl_file: Path | None = None
    if config.output.write_jsonl:
        jsonl_file = Path(config.output.jsonl_path)
        jsonl_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        for cycle in range(iterations):
            for collector in collectors:
                try:
                    record = collector.collect_once()
                    pending_records.append(record)
                    total_collected += 1
                    if jsonl_file is not None:
                        with jsonl_file.open("a", encoding="utf-8") as handle:
                            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                except Exception as exc:  # noqa: BLE001
                    total_failed += 1
                    print(f"[cycle {cycle + 1}] collector failed and will retry next cycle: {exc}")

            if pending_records and len(pending_records) >= flush_batch_size:
                try:
                    imported, skipped = _flush_records(
                        records=pending_records,
                        write_database=config.output.write_database,
                        batch_size=flush_batch_size,
                    )
                    total_imported += imported
                    total_skipped += skipped
                    pending_records = []
                except Exception as exc:  # noqa: BLE001
                    total_failed += 1
                    print(f"[cycle {cycle + 1}] flush failed, will retry next cycle: {exc}")

            print(
                f"[cycle {cycle + 1}/{iterations}] "
                f"collected={total_collected} imported={total_imported} "
                f"skipped={total_skipped} failed={total_failed}"
            )
            if cycle < iterations - 1:
                time.sleep(config.policy.sample_interval_sec)

        if pending_records:
            try:
                imported, skipped = _flush_records(
                    records=pending_records,
                    write_database=config.output.write_database,
                    batch_size=flush_batch_size,
                )
                total_imported += imported
                total_skipped += skipped
            except Exception as exc:  # noqa: BLE001
                total_failed += 1
                print(f"final flush failed: {exc}")
    finally:
        for collector in collectors:
            collector.close()

    return {
        "collected": total_collected,
        "imported": total_imported,
        "skipped": total_skipped,
        "failed": total_failed,
    }


def _flush_records(records: list[dict[str, Any]], write_database: bool, batch_size: int) -> tuple[int, int]:
    if not write_database:
        return 0, 0

    setup_django()
    from django.db import transaction
    from django.db.models import Q
    from django.utils import timezone
    from django.utils.dateparse import parse_datetime

    from apps.devices.models import Device, EnergyType
    from apps.energy.models import EnergyData

    devices = Device.objects.select_related("energy_type").all()
    device_by_pk = {str(item.pk): item for item in devices}
    device_by_code = {item.device_id: item for item in devices}
    energy_types = EnergyType.objects.all()
    energy_by_pk = {str(item.pk): item for item in energy_types}
    energy_by_code = {item.code.upper(): item for item in energy_types}

    instances = []
    skipped = 0
    for record in records:
        try:
            device_value = str(record.get("device", "")).strip()
            device = device_by_pk.get(device_value) or device_by_code.get(device_value)
            if device is None:
                raise ValueError(f"unknown device {device_value}")

            energy_value = str(record.get("energy_type", "")).strip().upper()
            energy_type = energy_by_pk.get(energy_value) or energy_by_code.get(energy_value) or device.energy_type
            if energy_type.id != device.energy_type_id:
                raise ValueError("energy type mismatch")

            parsed_ts = parse_datetime(str(record["timestamp"]))
            if parsed_ts is None:
                raise ValueError("invalid timestamp")
            if timezone.is_naive(parsed_ts):
                parsed_ts = timezone.make_aware(parsed_ts, timezone.get_current_timezone())

            instances.append(
                EnergyData(
                    device=device,
                    energy_type=energy_type,
                    timestamp=parsed_ts,
                    value=record["value"],
                    voltage=record.get("voltage"),
                    current=record.get("current"),
                    power=record.get("power"),
                    flow_rate=record.get("flow_rate"),
                )
            )
        except Exception:
            skipped += 1

    if not instances:
        return 0, skipped

    with transaction.atomic():
        before = EnergyData.objects.count()
        EnergyData.objects.bulk_create(instances, batch_size=batch_size, ignore_conflicts=True)
        after = EnergyData.objects.count()

        latest_map: dict[int, Any] = {}
        for instance in instances:
            latest = latest_map.get(instance.device_id)
            if latest is None or latest < instance.timestamp:
                latest_map[instance.device_id] = instance.timestamp

        for device_pk, ts in latest_map.items():
            Device.objects.filter(pk=device_pk).filter(
                Q(last_data_time__isnull=True) | Q(last_data_time__lt=ts)
            ).update(last_data_time=ts)

    imported = max(after - before, 0)
    skipped += max(len(instances) - imported, 0)
    return imported, skipped


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run Modbus/BACnet collection tasks and persist to em_energy_data.")
    parser.add_argument(
        "--config",
        default="scripts/protocol_collectors/collector_config.example.json",
        help="collector config json path",
    )
    parser.add_argument("--iterations", type=int, default=10, help="collection loop count")
    parser.add_argument("--flush-size", type=int, default=None, help="records per DB flush")
    args = parser.parse_args()

    config = load_runner_config(args.config)
    summary = run_collectors(config=config, iterations=args.iterations, flush_size=args.flush_size)
    print(f"collector summary: {json.dumps(summary, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
