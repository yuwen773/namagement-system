"""Data cleaning pipeline used by phase 5 data import scripts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from scripts.config import ImportConfig


@dataclass(frozen=True)
class CleaningReport:
    source_rows: int
    valid_rows: int
    invalid_rows: int
    anomaly_rows: int
    dropped_rows: int
    error_examples: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_rows": self.source_rows,
            "valid_rows": self.valid_rows,
            "invalid_rows": self.invalid_rows,
            "anomaly_rows": self.anomaly_rows,
            "dropped_rows": self.dropped_rows,
            "error_examples": self.error_examples,
        }


class EnergyDataCleaner:
    """Normalize and validate imported dataframe rows."""

    def __init__(self, config: ImportConfig):
        self.config = config

    def clean(
        self,
        dataframe: pd.DataFrame,
        drop_invalid: bool = True,
    ) -> tuple[pd.DataFrame, CleaningReport]:
        source_rows = len(dataframe.index)
        if source_rows == 0:
            empty_df = pd.DataFrame(columns=self.config.target_columns)
            return (
                empty_df,
                CleaningReport(
                    source_rows=0,
                    valid_rows=0,
                    invalid_rows=0,
                    anomaly_rows=0,
                    dropped_rows=0,
                    error_examples=[],
                ),
            )

        working_df = dataframe.copy()
        working_df.columns = [str(col).strip().lower() for col in working_df.columns]

        standardized = self._standardize_columns(working_df)
        standardized = self._standardize_units(standardized)
        standardized = self._convert_types(standardized)

        validated, error_examples = self._validate_rows(standardized)
        anomaly_mask = self._detect_anomalies(validated)
        validated["_is_anomaly"] = anomaly_mask

        if drop_invalid:
            cleaned = validated[validated["_error_message"] == ""].copy()
            dropped_rows = int((validated["_error_message"] != "").sum())
        else:
            cleaned = validated.copy()
            dropped_rows = 0

        cleaned = cleaned.loc[:, list(self.config.target_columns) + ["_is_anomaly", "_error_message"]]
        cleaned = cleaned.reset_index(drop=True)

        invalid_rows = int((validated["_error_message"] != "").sum())
        valid_rows = source_rows - invalid_rows
        anomaly_rows = int(anomaly_mask.sum())

        report = CleaningReport(
            source_rows=source_rows,
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
            anomaly_rows=anomaly_rows,
            dropped_rows=dropped_rows,
            error_examples=error_examples,
        )
        return cleaned, report

    def _standardize_columns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        result = pd.DataFrame(index=dataframe.index)
        result["_power_from_w"] = (
            "power_w" in dataframe.columns
            and "power" not in dataframe.columns
            and "power_kw" not in dataframe.columns
        )
        result["_flow_rate_from_lps"] = (
            "flow_rate_lps" in dataframe.columns
            and "flow_rate" not in dataframe.columns
            and "flow_rate_m3h" not in dataframe.columns
        )

        for target in self.config.target_columns:
            source_columns = self._get_source_columns(dataframe, target)
            if source_columns:
                result[target] = dataframe[source_columns].bfill(axis=1).iloc[:, 0]
            else:
                result[target] = None

        # Keep original unit columns if present for later conversion.
        for extra in ("value_unit", "power_unit", "flow_rate_unit", "energy_type"):
            if extra in dataframe.columns and extra not in result.columns:
                result[extra] = dataframe[extra]

        return result

    def _get_source_columns(self, dataframe: pd.DataFrame, target: str) -> list[str]:
        candidates = [target]
        candidates.extend(self.config.column_aliases.get(target, ()))
        source_columns = []
        for column in candidates:
            key = str(column).strip().lower()
            if key in dataframe.columns and key not in source_columns:
                source_columns.append(key)
        return source_columns

    def _standardize_units(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        # Convert W to kW if no explicit power_unit, and convert L/s to m3/h.
        if "power" in dataframe.columns:
            power_unit = dataframe.get("power_unit")
            if power_unit is not None:
                normalized_power_unit = power_unit.astype(str).str.upper().str.strip()
                watt_mask = normalized_power_unit.eq("W")
                dataframe.loc[watt_mask, "power"] = pd.to_numeric(
                    dataframe.loc[watt_mask, "power"],
                    errors="coerce",
                ) / 1000.0
            elif bool(dataframe.get("_power_from_w", False).iloc[0]):
                dataframe["power"] = pd.to_numeric(dataframe["power"], errors="coerce") / 1000.0

        if "flow_rate" in dataframe.columns:
            flow_rate_unit = dataframe.get("flow_rate_unit")
            if flow_rate_unit is not None:
                normalized_flow_rate_unit = flow_rate_unit.astype(str).str.upper().str.strip()
                liter_per_sec_mask = normalized_flow_rate_unit.isin(["L/S", "LPS"])
                dataframe.loc[liter_per_sec_mask, "flow_rate"] = pd.to_numeric(
                    dataframe.loc[liter_per_sec_mask, "flow_rate"],
                    errors="coerce",
                ) * 3.6
            elif bool(dataframe.get("_flow_rate_from_lps", False).iloc[0]):
                dataframe["flow_rate"] = pd.to_numeric(dataframe["flow_rate"], errors="coerce") * 3.6

        if "value" in dataframe.columns:
            value_unit = dataframe.get("value_unit")
            if value_unit is not None:
                normalized_value_unit = value_unit.astype(str).str.upper().str.strip()
                wh_mask = normalized_value_unit.eq("WH")
                dataframe.loc[wh_mask, "value"] = pd.to_numeric(
                    dataframe.loc[wh_mask, "value"],
                    errors="coerce",
                ) / 1000.0
        return dataframe

    def _convert_types(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe["device"] = dataframe["device"].astype(str).str.strip()
        dataframe["device"] = dataframe["device"].replace({"": None, "nan": None, "None": None})
        dataframe["device"] = dataframe["device"].map(
            lambda value: self.config.device_mapping.get(str(value), value) if value else value
        )

        dataframe["energy_type"] = dataframe["energy_type"].astype(str).str.strip().str.upper()
        dataframe["energy_type"] = dataframe["energy_type"].replace({"": None, "NAN": None, "NONE": None})
        dataframe["energy_type"] = dataframe["energy_type"].map(
            lambda value: self.config.energy_type_mapping.get(str(value), value) if value else value
        )

        dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"], errors="coerce")
        for field in ("value", "voltage", "current", "power", "flow_rate"):
            dataframe[field] = pd.to_numeric(dataframe[field], errors="coerce")
        return dataframe

    def _validate_rows(self, dataframe: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
        errors: list[str] = []
        messages = []

        for index, row in dataframe.iterrows():
            row_errors: list[str] = []
            row_no = index + 1

            for required in self.config.required_columns:
                if self._is_empty_value(row.get(required)):
                    row_errors.append(f"row {row_no}: missing required field '{required}'")

            timestamp = row.get("timestamp")
            if not self._is_empty_value(timestamp) and pd.isna(timestamp):
                row_errors.append(f"row {row_no}: invalid timestamp format")

            for field_name, rule in self.config.numeric_ranges.items():
                value = row.get(field_name)
                if self._is_empty_value(value):
                    continue
                if pd.isna(value):
                    row_errors.append(f"row {row_no}: field '{field_name}' is not numeric")
                    continue
                numeric = float(value)
                if rule.min_value is not None and numeric < rule.min_value:
                    row_errors.append(
                        f"row {row_no}: field '{field_name}' below min ({numeric} < {rule.min_value})"
                    )
                if rule.max_value is not None and numeric > rule.max_value:
                    row_errors.append(
                        f"row {row_no}: field '{field_name}' above max ({numeric} > {rule.max_value})"
                    )

            message = "; ".join(row_errors)
            messages.append(message)
            if message and len(errors) < 20:
                errors.append(message)

        dataframe["_error_message"] = messages
        return dataframe, errors

    def _detect_anomalies(self, dataframe: pd.DataFrame) -> pd.Series:
        anomaly_mask = pd.Series(False, index=dataframe.index)
        if "power" in dataframe.columns:
            anomaly_mask = anomaly_mask | (dataframe["power"].fillna(0) < 0)
        if "value" in dataframe.columns:
            anomaly_mask = anomaly_mask | (dataframe["value"].fillna(0) < 0)
        return anomaly_mask

    @staticmethod
    def _is_empty_value(value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return value.strip() == ""
        return bool(pd.isna(value))
