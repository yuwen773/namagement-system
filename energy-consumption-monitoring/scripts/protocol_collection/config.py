"""Configuration models and loader for protocol collection scripts."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Literal

REQUIRED_EM_ENERGY_DATA_FIELDS = (
    "device",
    "energy_type",
    "timestamp",
    "value",
    "voltage",
    "current",
    "power",
    "flow_rate",
)

READABLE_FIELDS = ("value", "voltage", "current", "power", "flow_rate")
SUPPORTED_PROTOCOLS = ("modbus", "bacnet")
SUPPORTED_GATEWAY_MODES = ("gateway_forward", "direct_meter")


@dataclass(frozen=True)
class CollectionPolicy:
    sample_interval_sec: float
    request_timeout_sec: float
    retry_times: int
    retry_backoff_sec: float
    reconnect_interval_sec: float


@dataclass(frozen=True)
class MeterMapping:
    meter_id: str
    device: str
    room: str
    protocol: Literal["modbus", "bacnet"]
    gateway_mode: Literal["gateway_forward", "direct_meter"]
    host: str
    port: int
    energy_type: str
    point_map: dict[str, str | None]


@dataclass(frozen=True)
class CollectionConfig:
    policy: CollectionPolicy
    meters: list[MeterMapping]


def load_collection_config(path: str | Path) -> CollectionConfig:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    policy = _parse_policy(raw.get("policy", {}))
    meters = [_parse_meter(item) for item in raw.get("meters", [])]
    if not meters:
        raise ValueError("Configuration must include at least one meter mapping in 'meters'.")
    return CollectionConfig(policy=policy, meters=meters)


def _parse_policy(raw: dict) -> CollectionPolicy:
    return CollectionPolicy(
        sample_interval_sec=float(raw.get("sample_interval_sec", 5)),
        request_timeout_sec=float(raw.get("request_timeout_sec", 2)),
        retry_times=int(raw.get("retry_times", 3)),
        retry_backoff_sec=float(raw.get("retry_backoff_sec", 1)),
        reconnect_interval_sec=float(raw.get("reconnect_interval_sec", 2)),
    )


def _parse_meter(raw: dict) -> MeterMapping:
    protocol = str(raw.get("protocol", "")).lower().strip()
    if protocol not in SUPPORTED_PROTOCOLS:
        raise ValueError(f"Unsupported protocol '{protocol}'. Expected one of {SUPPORTED_PROTOCOLS}.")

    gateway_mode = str(raw.get("gateway_mode", "")).lower().strip()
    if gateway_mode not in SUPPORTED_GATEWAY_MODES:
        raise ValueError(
            f"Unsupported gateway_mode '{gateway_mode}'. Expected one of {SUPPORTED_GATEWAY_MODES}."
        )

    meter_id = _required_str(raw, "meter_id")
    device = _required_str(raw, "device")
    room = _required_str(raw, "room")
    host = _required_str(raw, "host")
    energy_type = _required_str(raw, "energy_type")
    port = int(raw.get("port"))

    point_map_raw = raw.get("point_map") or {}
    point_map: dict[str, str | None] = {}
    for field in READABLE_FIELDS:
        point = point_map_raw.get(field)
        point_map[field] = str(point).strip() if point else None

    if point_map["value"] is None:
        raise ValueError(f"Meter '{meter_id}' point_map.value is required.")

    return MeterMapping(
        meter_id=meter_id,
        device=device,
        room=room,
        protocol=protocol,  # type: ignore[arg-type]
        gateway_mode=gateway_mode,  # type: ignore[arg-type]
        host=host,
        port=port,
        energy_type=energy_type,
        point_map=point_map,
    )


def _required_str(raw: dict, key: str) -> str:
    value = str(raw.get(key, "")).strip()
    if not value:
        raise ValueError(f"Missing required string field: {key}")
    return value

