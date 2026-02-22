"""Socket simulators for protocol collection acceptance in phase 1.5."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import socketserver
import threading
from typing import Any


DEFAULT_MODBUS_DATA = {
    "METER-MODBUS-001": {
        "total_kwh": 1280.53,
        "voltage_v": 221.4,
        "current_a": 18.6,
        "power_kw": 4.12,
    }
}

DEFAULT_BACNET_DATA = {
    "METER-BACNET-001": {
        "total_m3": 663.74,
        "flow_rate_m3h": 2.07,
    }
}


class _ProtocolRequestHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        while True:
            line = self.rfile.readline()
            if not line:
                return
            try:
                request = json.loads(line.decode("utf-8"))
                response = self.server.process_request_payload(request)  # type: ignore[attr-defined]
            except Exception as exc:  # noqa: BLE001 - return structured error to client
                response = {"ok": False, "error": str(exc)}
            self.wfile.write((json.dumps(response, ensure_ascii=True) + "\n").encode("utf-8"))


class _ThreadingProtocolServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], protocol: str, meter_data: dict[str, dict[str, float]]):
        super().__init__(server_address, _ProtocolRequestHandler)
        self.protocol = protocol
        self.meter_data = meter_data

    def process_request_payload(self, request: dict[str, Any]) -> dict[str, Any]:
        if request.get("action") != "read_point":
            return {"ok": False, "error": "Unsupported action"}
        if request.get("protocol") != self.protocol:
            return {"ok": False, "error": f"Protocol mismatch, expected {self.protocol}"}

        meter_id = str(request.get("meter_id", "")).strip()
        point = str(request.get("point", "")).strip()
        meter_points = self.meter_data.get(meter_id)
        if meter_points is None:
            return {"ok": False, "error": f"Unknown meter_id '{meter_id}'"}
        if point not in meter_points:
            return {"ok": False, "error": f"Unknown point '{point}' for meter '{meter_id}'"}

        value = meter_points[point]
        return {
            "ok": True,
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


@dataclass
class RunningSimulator:
    protocol: str
    host: str
    port: int
    server: _ThreadingProtocolServer
    thread: threading.Thread

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)


def start_protocol_simulator(
    protocol: str,
    host: str,
    port: int,
    meter_data: dict[str, dict[str, float]],
) -> RunningSimulator:
    server = _ThreadingProtocolServer((host, port), protocol=protocol, meter_data=meter_data)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return RunningSimulator(protocol=protocol, host=host, port=port, server=server, thread=thread)


def start_default_simulators(
    host: str = "127.0.0.1",
    modbus_port: int = 15020,
    bacnet_port: int = 14780,
) -> dict[str, RunningSimulator]:
    return {
        "modbus": start_protocol_simulator("modbus", host, modbus_port, DEFAULT_MODBUS_DATA),
        "bacnet": start_protocol_simulator("bacnet", host, bacnet_port, DEFAULT_BACNET_DATA),
    }


def stop_simulators(simulators: dict[str, RunningSimulator]) -> None:
    for simulator in simulators.values():
        simulator.stop()


def main() -> int:
    simulators = start_default_simulators()
    print("Modbus simulator listening on 127.0.0.1:15020")
    print("BACnet simulator listening on 127.0.0.1:14780")
    print("Press Ctrl+C to stop.")
    try:
        simulators["modbus"].thread.join()
        simulators["bacnet"].thread.join()
    except KeyboardInterrupt:
        pass
    finally:
        stop_simulators(simulators)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

