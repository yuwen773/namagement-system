"""Protocol adapters for simulator-based Modbus/BACnet reads."""

from __future__ import annotations

from dataclasses import dataclass
import json
import socket
import time
from typing import Any

from .config import CollectionPolicy, MeterMapping, READABLE_FIELDS


@dataclass
class AdapterError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


class JsonTcpProtocolAdapter:
    """Gateway-facing adapter with timeout, retry and reconnect behavior."""

    def __init__(self, mapping: MeterMapping, policy: CollectionPolicy):
        self.mapping = mapping
        self.policy = policy
        self._sock: socket.socket | None = None
        self._reader = None
        self._writer = None

    def close(self) -> None:
        if self._reader is not None:
            self._reader.close()
            self._reader = None
        if self._writer is not None:
            self._writer.close()
            self._writer = None
        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def read_measurements(self) -> dict[str, float | None]:
        measurements: dict[str, float | None] = {field: None for field in READABLE_FIELDS}
        for field, point in self.mapping.point_map.items():
            if not point:
                continue
            measurements[field] = float(self._read_point_with_retry(point))
        return measurements

    def _read_point_with_retry(self, point: str) -> float:
        last_error: Exception | None = None
        attempts = self.policy.retry_times + 1
        for attempt in range(attempts):
            try:
                return self._read_point_once(point)
            except Exception as exc:  # noqa: BLE001 - propagate with context after retries
                last_error = exc
                self.close()
                if attempt < attempts - 1:
                    time.sleep(self.policy.retry_backoff_sec)
        raise AdapterError(
            f"[{self.mapping.protocol}] meter={self.mapping.meter_id} point={point} read failed "
            f"after {attempts} attempts: {last_error}"
        )

    def _read_point_once(self, point: str) -> float:
        self._ensure_connected()
        request = {
            "action": "read_point",
            "protocol": self.mapping.protocol,
            "meter_id": self.mapping.meter_id,
            "point": point,
        }
        payload = (json.dumps(request, ensure_ascii=True) + "\n").encode("utf-8")
        assert self._sock is not None
        self._sock.sendall(payload)
        response = self._read_response_line()
        if not response.get("ok"):
            error = response.get("error", "unknown simulator error")
            raise AdapterError(str(error))
        value = response.get("value")
        if value is None:
            raise AdapterError(f"Missing 'value' in simulator response for point '{point}'.")
        return float(value)

    def _ensure_connected(self) -> None:
        if self._sock is not None:
            return

        attempts = self.policy.retry_times + 1
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                self._sock = socket.create_connection(
                    (self.mapping.host, self.mapping.port),
                    timeout=self.policy.request_timeout_sec,
                )
                self._sock.settimeout(self.policy.request_timeout_sec)
                return
            except OSError as exc:
                last_error = exc
                if attempt < attempts - 1:
                    time.sleep(self.policy.reconnect_interval_sec)
        raise AdapterError(
            f"[{self.mapping.protocol}] connect failed "
            f"{self.mapping.host}:{self.mapping.port} after {attempts} attempts: {last_error}"
        )

    def _read_response_line(self) -> dict[str, Any]:
        assert self._sock is not None
        buffer = bytearray()
        while True:
            chunk = self._sock.recv(4096)
            if not chunk:
                raise AdapterError("Connection closed by simulator.")
            buffer.extend(chunk)
            if b"\n" in chunk:
                break
        line = bytes(buffer).splitlines()[0].decode("utf-8")
        return json.loads(line)

