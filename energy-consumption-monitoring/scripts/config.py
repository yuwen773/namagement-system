"""Shared configuration helpers for phase 5 scripts."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import sys
from typing import Any


@dataclass(frozen=True)
class NumericRangeRule:
    min_value: float | None = None
    max_value: float | None = None


@dataclass(frozen=True)
class ApiImportConfig:
    base_url: str = "http://127.0.0.1:8000"
    endpoint: str = "/api/energy-data/batch-import/"
    timeout_sec: int = 60
    token: str | None = None


@dataclass(frozen=True)
class ImportConfig:
    default_batch_size: int = 1_000
    preview_rows: int = 5
    timezone: str = "Asia/Shanghai"
    required_columns: tuple[str, ...] = ("device", "energy_type", "timestamp", "value")
    target_columns: tuple[str, ...] = (
        "device",
        "energy_type",
        "timestamp",
        "value",
        "voltage",
        "current",
        "power",
        "flow_rate",
    )
    column_aliases: dict[str, tuple[str, ...]] = field(
        default_factory=lambda: {
            "device": ("device_id", "meter_id", "nmi_id"),
            "energy_type": ("energy_type_id", "energy_type_code", "type", "type_code"),
            "timestamp": ("time", "datetime", "record_time"),
            "value": ("consumption", "usage", "reading", "total_kwh", "total_m3"),
            "voltage": ("voltage_v",),
            "current": ("current_a",),
            "power": ("power_kw", "power_w"),
            "flow_rate": ("flow", "flow_rate_m3h", "flow_rate_lps"),
        }
    )
    numeric_ranges: dict[str, NumericRangeRule] = field(
        default_factory=lambda: {
            "value": NumericRangeRule(min_value=0),
            "voltage": NumericRangeRule(min_value=0, max_value=1000),
            "current": NumericRangeRule(min_value=0, max_value=5000),
            "power": NumericRangeRule(min_value=0, max_value=50000),
            "flow_rate": NumericRangeRule(min_value=0, max_value=50000),
        }
    )
    api: ApiImportConfig = field(default_factory=ApiImportConfig)
    device_mapping: dict[str, str] = field(default_factory=dict)
    energy_type_mapping: dict[str, str] = field(default_factory=dict)


def load_import_config(path: str | Path | None = None) -> ImportConfig:
    """Load import config from JSON file. Missing file falls back to defaults."""
    if path is None:
        env_path = os.getenv("ENERGY_IMPORT_CONFIG")
        path = env_path if env_path else None
    if path is None:
        return ImportConfig()

    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Import config not found: {config_path}")

    raw = json.loads(config_path.read_text(encoding="utf-8-sig"))
    defaults = ImportConfig()
    return ImportConfig(
        default_batch_size=int(raw.get("default_batch_size", defaults.default_batch_size)),
        preview_rows=int(raw.get("preview_rows", defaults.preview_rows)),
        timezone=str(raw.get("timezone", defaults.timezone)),
        required_columns=tuple(raw.get("required_columns", defaults.required_columns)),
        target_columns=tuple(raw.get("target_columns", defaults.target_columns)),
        column_aliases=_parse_aliases(raw.get("column_aliases"), defaults.column_aliases),
        numeric_ranges=_parse_numeric_ranges(raw.get("numeric_ranges"), defaults.numeric_ranges),
        api=_parse_api_config(raw.get("api"), defaults.api),
        device_mapping=_normalize_mapping(raw.get("device_mapping", {})),
        energy_type_mapping=_normalize_mapping(raw.get("energy_type_mapping", {})),
    )


def _parse_aliases(raw: Any, defaults: dict[str, tuple[str, ...]]) -> dict[str, tuple[str, ...]]:
    if not isinstance(raw, dict):
        return defaults
    aliases: dict[str, tuple[str, ...]] = {}
    for field_name, default_aliases in defaults.items():
        values = raw.get(field_name, list(default_aliases))
        if not isinstance(values, list):
            values = list(default_aliases)
        aliases[field_name] = tuple(str(item).strip() for item in values if str(item).strip())
    return aliases


def _parse_numeric_ranges(
    raw: Any,
    defaults: dict[str, NumericRangeRule],
) -> dict[str, NumericRangeRule]:
    if not isinstance(raw, dict):
        return defaults
    ranges: dict[str, NumericRangeRule] = {}
    for field_name, default_rule in defaults.items():
        item = raw.get(field_name, {})
        if not isinstance(item, dict):
            ranges[field_name] = default_rule
            continue
        min_value = item.get("min_value", default_rule.min_value)
        max_value = item.get("max_value", default_rule.max_value)
        ranges[field_name] = NumericRangeRule(
            min_value=float(min_value) if min_value is not None else None,
            max_value=float(max_value) if max_value is not None else None,
        )
    return ranges


def _parse_api_config(raw: Any, defaults: ApiImportConfig) -> ApiImportConfig:
    if not isinstance(raw, dict):
        return defaults
    return ApiImportConfig(
        base_url=str(raw.get("base_url", defaults.base_url)).rstrip("/"),
        endpoint=str(raw.get("endpoint", defaults.endpoint)),
        timeout_sec=int(raw.get("timeout_sec", defaults.timeout_sec)),
        token=str(raw["token"]).strip() if raw.get("token") else defaults.token,
    )


def _normalize_mapping(raw: Any) -> dict[str, str]:
    if not isinstance(raw, dict):
        return {}
    result: dict[str, str] = {}
    for key, value in raw.items():
        left = str(key).strip()
        right = str(value).strip()
        if left and right:
            result[left] = right
    return result


def setup_django() -> None:
    """Bootstrap Django ORM for standalone scripts."""
    repo_root = Path(__file__).resolve().parents[1]
    backend_dir = repo_root / "backend"
    backend_dir_str = str(backend_dir)
    if backend_dir_str not in sys.path:
        sys.path.insert(0, backend_dir_str)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "energy_monitoring.settings")

    import django

    django.setup()
