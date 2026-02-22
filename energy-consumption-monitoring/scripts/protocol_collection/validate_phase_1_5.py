"""Acceptance checks for phase 1.5 (Modbus/BACnet collection environment)."""

from __future__ import annotations

from pathlib import Path
import time

from .adapters import JsonTcpProtocolAdapter
from .collector import run_collection_from_config
from .config import REQUIRED_EM_ENERGY_DATA_FIELDS, load_collection_config
from .simulators import start_default_simulators, start_protocol_simulator, stop_simulators


def main() -> int:
    checklist: list[tuple[str, bool, str]] = []
    config_path = Path("scripts/protocol_collection/collection_config.example.json")
    output_path = Path("scripts/protocol_collection/output/phase_1_5_validation.jsonl")

    simulators = start_default_simulators()
    try:
        config = load_collection_config(config_path)
        records = run_collection_from_config(
            config_path=config_path,
            iterations=2,
            output_path=output_path,
        )

        modbus_records = [row for row in records if row["energy_type"] == "ELECTRICITY"]
        bacnet_records = [row for row in records if row["energy_type"] == "WATER"]

        modbus_stable = _is_stable(modbus_records, "value")
        bacnet_stable = _is_stable(bacnet_records, "value")
        checklist.append(("Modbus simulator is readable with stable points", modbus_stable, "value tolerance <= 0.001"))
        checklist.append(("BACnet simulator is readable with stable points", bacnet_stable, "value tolerance <= 0.001"))

        reconnect_ok = _test_reconnect(config, simulators)
        checklist.append(("Collector can reconnect after network interruption", reconnect_ok, "stop/restart simulator then read succeeds"))

        field_alignment_ok = all(tuple(row.keys()) == REQUIRED_EM_ENERGY_DATA_FIELDS for row in records)
        checklist.append(
            ("Collected fields align with em_energy_data model fields", field_alignment_ok, str(REQUIRED_EM_ENERGY_DATA_FIELDS))
        )

        no_hardware_ok = len(records) > 0 and output_path.exists()
        checklist.append(("Acceptance works with protocol simulators only", no_hardware_ok, f"records={len(records)}"))
    finally:
        stop_simulators(simulators)

    all_ok = all(item[1] for item in checklist)
    for title, passed, detail in checklist:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {title} - {detail}")
    print(f"Validation report: {output_path.resolve()}")
    return 0 if all_ok else 1


def _is_stable(records: list[dict], field: str) -> bool:
    if len(records) < 2:
        return False
    first = records[0].get(field)
    second = records[1].get(field)
    if first is None or second is None:
        return False
    return abs(float(first) - float(second)) <= 0.001


def _test_reconnect(config, simulators: dict) -> bool:
    mapping = next(item for item in config.meters if item.protocol == "modbus")
    adapter = JsonTcpProtocolAdapter(mapping, config.policy)
    try:
        initial_value = adapter.read_measurements()["value"]
        if initial_value is None:
            return False

        simulators["modbus"].stop()
        adapter.close()
        time.sleep(config.policy.reconnect_interval_sec)
        try:
            adapter.read_measurements()
            # When simulator is down, reads should not silently succeed.
            return False
        except Exception:  # noqa: BLE001
            pass

        simulators["modbus"] = start_protocol_simulator(
            protocol="modbus",
            host=mapping.host,
            port=mapping.port,
            meter_data={"METER-MODBUS-001": {"total_kwh": 1280.53, "voltage_v": 221.4, "current_a": 18.6, "power_kw": 4.12}},
        )
        recovered_value = adapter.read_measurements()["value"]
        return recovered_value is not None
    except Exception:  # noqa: BLE001 - used for boolean acceptance
        return False
    finally:
        adapter.close()


if __name__ == "__main__":
    raise SystemExit(main())
