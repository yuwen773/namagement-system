"""Modbus collector for periodic energy data reads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from scripts.protocol_collection.adapters import JsonTcpProtocolAdapter
from scripts.protocol_collection.config import CollectionPolicy, MeterMapping


@dataclass(frozen=True)
class ModbusCollectorConfig:
    meter_id: str
    device: str
    room: str
    host: str
    port: int
    energy_type: str = "ELECTRICITY"
    gateway_mode: str = "direct_meter"
    point_map: dict[str, str | None] | None = None

    def as_mapping(self, policy: CollectionPolicy) -> MeterMapping:
        points = self.point_map or {
            "value": "total_kwh",
            "voltage": "voltage_v",
            "current": "current_a",
            "power": "power_kw",
            "flow_rate": None,
        }
        return MeterMapping(
            meter_id=self.meter_id,
            device=self.device,
            room=self.room,
            protocol="modbus",
            gateway_mode=self.gateway_mode,  # type: ignore[arg-type]
            host=self.host,
            port=self.port,
            energy_type=self.energy_type,
            point_map=points,
        )


class ModbusCollector:
    """Single Modbus meter collector with retry/reconnect behavior."""

    def __init__(self, config: ModbusCollectorConfig, policy: CollectionPolicy):
        self.config = config
        self.mapping = config.as_mapping(policy)
        self.adapter = JsonTcpProtocolAdapter(mapping=self.mapping, policy=policy)

    def collect_once(self) -> dict[str, Any]:
        measurements = self.adapter.read_measurements()
        return {
            "device": self.mapping.device,
            "energy_type": self.mapping.energy_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "value": measurements.get("value"),
            "voltage": measurements.get("voltage"),
            "current": measurements.get("current"),
            "power": measurements.get("power"),
            "flow_rate": measurements.get("flow_rate"),
        }

    def close(self) -> None:
        self.adapter.close()

