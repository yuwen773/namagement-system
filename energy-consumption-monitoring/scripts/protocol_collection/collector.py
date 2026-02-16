"""Protocol collector for phase 1.5 acceptance."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import time

from .adapters import AdapterError, JsonTcpProtocolAdapter
from .config import (
    CollectionConfig,
    MeterMapping,
    REQUIRED_EM_ENERGY_DATA_FIELDS,
    READABLE_FIELDS,
    load_collection_config,
)


def run_collection(
    config: CollectionConfig,
    iterations: int,
    output_path: str | Path,
) -> list[dict]:
    adapters = [JsonTcpProtocolAdapter(mapping=mapping, policy=config.policy) for mapping in config.meters]
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    collected: list[dict] = []
    try:
        output.write_text("", encoding="utf-8")
        for index in range(iterations):
            for mapping, adapter in zip(config.meters, adapters):
                record = collect_single_record(mapping, adapter)
                _validate_record_schema(record)
                collected.append(record)
                with output.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            if index < iterations - 1:
                time.sleep(config.policy.sample_interval_sec)
    finally:
        for adapter in adapters:
            adapter.close()

    return collected


def collect_single_record(mapping: MeterMapping, adapter: JsonTcpProtocolAdapter) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        measurements = adapter.read_measurements()
    except AdapterError:
        measurements = {field: None for field in READABLE_FIELDS}

    record = {
        "device": mapping.device,
        "energy_type": mapping.energy_type,
        "timestamp": timestamp,
        "value": measurements["value"],
        "voltage": measurements["voltage"],
        "current": measurements["current"],
        "power": measurements["power"],
        "flow_rate": measurements["flow_rate"],
    }
    return record


def _validate_record_schema(record: dict) -> None:
    keys = tuple(record.keys())
    if keys != REQUIRED_EM_ENERGY_DATA_FIELDS:
        raise ValueError(
            "Collected record keys must match em_energy_data fields exactly. "
            f"Expected: {REQUIRED_EM_ENERGY_DATA_FIELDS}, got: {keys}"
        )


def run_collection_from_config(
    config_path: str | Path,
    iterations: int = 3,
    output_path: str | Path = "scripts/protocol_collection/output/collected_energy_data.jsonl",
) -> list[dict]:
    config = load_collection_config(config_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    return run_collection(config=config, iterations=iterations, output_path=output_path)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run phase 1.5 protocol collection.")
    parser.add_argument(
        "--config",
        default="scripts/protocol_collection/collection_config.example.json",
        help="Path to collection config json.",
    )
    parser.add_argument("--iterations", type=int, default=3, help="Collection loop count.")
    parser.add_argument(
        "--output",
        default="scripts/protocol_collection/output/collected_energy_data.jsonl",
        help="Output jsonl path.",
    )
    args = parser.parse_args()

    records = run_collection_from_config(
        config_path=args.config,
        iterations=args.iterations,
        output_path=args.output,
    )
    print(f"Collected {len(records)} records.")
    print(f"Output: {Path(args.output).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
