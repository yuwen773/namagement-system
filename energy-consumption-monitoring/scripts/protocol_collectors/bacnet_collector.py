"""BACnet collector for periodic energy data reads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from scripts.protocol_collection.adapters import JsonTcpProtocolAdapter
from scripts.protocol_collection.config import CollectionPolicy, MeterMapping


@dataclass(frozen=True)
class BacnetCollectorConfig:
    meter_id: str
    device: str
    room: str
    host: str
    port: int
    energy_type: str = "WATER"
    gateway_mode: str = "gateway_forward"
    point_map: dict[str, str | None] | None = None

    def as_mapping(self, policy: CollectionPolicy) -> MeterMapping:
        points = self.point_map or {
            "value": "total_m3",
            "voltage": None,
            "current": None,
            "power": None,
            "flow_rate": "flow_rate_m3h",
        }
        return MeterMapping(
            meter_id=self.meter_id,
            device=self.device,
            room=self.room,
            protocol="bacnet",
            gateway_mode=self.gateway_mode,  # type: ignore[arg-type]
            host=self.host,
            port=self.port,
            energy_type=self.energy_type,
            point_map=points,
        )


class BacnetCollector:
    """Single BACnet meter collector with retry/reconnect behavior."""

    def __init__(self, config: BacnetCollectorConfig, policy: CollectionPolicy):
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

