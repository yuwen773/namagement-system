from __future__ import annotations

import csv
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from pandas.errors import ParserError
from django.db import transaction

from apps.categories.models import Category
from apps.heritage.models import HeritageItem
from apps.inheritors.models import Inheritor
from apps.regions.models import Region

from .models import ImportError, ImportJob

DATASET_HERITAGE = "heritage"
DATASET_INHERITOR = "inheritor"
SUPPORTED_DATASET_TYPES = {DATASET_HERITAGE, DATASET_INHERITOR}

HERITAGE_FIELD_ALIASES = {
    "name": ["name", "title", "title_en", "item_name", "heritage_name", "label"],
    "category": ["category", "type", "type_of_element_en", "heritage_type"],
    "category_code": ["category_code", "type_code", "type_acronym", "list"],
    "level": ["level", "grade"],
    "country": ["country", "countries", "country_name"],
    "country_code": ["country_code", "iso_code"],
    "area": ["area", "region_name"],
    "protection_unit": ["protection_unit", "protection"],
    "description": ["description", "desc", "summary"],
}

INHERITOR_FIELD_ALIASES = {
    "name": ["name", "inheritor_name"],
    "heritage_name": ["heritage_name", "heritage_item", "item_name"],
    "heritage_id": ["heritage_id", "item_id"],
    "country": ["country", "country_name"],
    "country_code": ["country_code", "iso_code"],
    "gender": ["gender", "sex"],
    "level": ["level", "grade"],
    "area": ["area", "region_name"],
    "description": ["description", "desc", "summary"],
}

HERITAGE_REQUIRED_FIELDS = ("name", "category_or_code", "level", "country_or_code")
INHERITOR_REQUIRED_FIELDS = ("name", "heritage_name_or_id", "country_or_code")

LEVEL_ALIASES = {
    "national": HeritageItem.LEVEL_NATIONAL,
    "nationallevel": HeritageItem.LEVEL_NATIONAL,
    "provincial": HeritageItem.LEVEL_PROVINCIAL,
    "provinciallevel": HeritageItem.LEVEL_PROVINCIAL,
    "citycounty": HeritageItem.LEVEL_CITY_COUNTY,
    "city/county": HeritageItem.LEVEL_CITY_COUNTY,
    "city_county": HeritageItem.LEVEL_CITY_COUNTY,
    "citycountylevel": HeritageItem.LEVEL_CITY_COUNTY,
}

GENDER_ALIASES = {
    "male": Inheritor.GENDER_MALE,
    "m": Inheritor.GENDER_MALE,
    "female": Inheritor.GENDER_FEMALE,
    "f": Inheritor.GENDER_FEMALE,
    "other": Inheritor.GENDER_OTHER,
    "unknown": Inheritor.GENDER_OTHER,
}


class RowImportError(Exception):
    def __init__(self, field_name: str, error_message: str):
        super().__init__(error_message)
        self.field_name = field_name
        self.error_message = error_message


@dataclass
class ImportRunResult:
    dataset_type: str
    file_name: str
    commit: bool
    total_rows: int
    success_count: int
    error_count: int
    created_count: int
    updated_count: int
    required_fields: tuple[str, ...]
    job_id: int | None
    job_status: str | None
    error_report: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_type": self.dataset_type,
            "file_name": self.file_name,
            "commit": self.commit,
            "total_rows": self.total_rows,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "created_count": self.created_count,
            "updated_count": self.updated_count,
            "required_fields": list(self.required_fields),
            "job_id": self.job_id,
            "job_status": self.job_status,
            "error_report": self.error_report,
        }


class OfflineImporterService:
    def __init__(
        self,
        file_path: str | Path,
        dataset_type: str,
        *,
        commit: bool,
        created_by=None,
        default_level: str | None = None,
        default_country: str | None = None,
        batch_size: int = 100,
        error_output: str | Path | None = None,
    ):
        self.file_path = Path(file_path).expanduser().resolve()
        self.dataset_type = dataset_type.strip().lower()
        self.commit = commit
        self.created_by = created_by
        self.default_level = (default_level or "").strip()
        self.default_country = (default_country or "").strip()
        self.batch_size = max(1, int(batch_size))
        self.error_output = Path(error_output).expanduser().resolve() if error_output else None

        if self.dataset_type not in SUPPORTED_DATASET_TYPES:
            supported = ", ".join(sorted(SUPPORTED_DATASET_TYPES))
            raise ValueError(f"Unsupported dataset type: {dataset_type}. Supported: {supported}")

    def run(self) -> ImportRunResult:
        if not self.file_path.exists():
            raise ValueError(f"File not found: {self.file_path}")

        data_frame = self._load_table(self.file_path)
        total_rows = len(data_frame.index)
        column_map = self._resolve_columns(data_frame.columns)
        required_fields = self._required_fields()

        errors: list[dict[str, Any]] = []
        success_count = 0
        created_count = 0
        updated_count = 0
        import_job = None

        if self.commit:
            import_job = ImportJob.objects.create(
                file_name=self.file_path.name,
                status=ImportJob.STATUS_PROCESSING,
                total_rows=total_rows,
                created_by=self.created_by,
            )

        for row_index, raw_row in enumerate(data_frame.to_dict(orient="records"), start=2):
            normalized_row = self._extract_canonical_row(raw_row, column_map)
            sanitized_raw = self._sanitize_raw_data(raw_row)

            try:
                if self.dataset_type == DATASET_HERITAGE:
                    operation = self._import_heritage_row(normalized_row)
                else:
                    operation = self._import_inheritor_row(normalized_row)
            except RowImportError as error:
                errors.append(
                    {
                        "row_number": row_index,
                        "field_name": error.field_name,
                        "error_message": error.error_message,
                        "raw_data": sanitized_raw,
                    }
                )
                continue
            except Exception as error:
                errors.append(
                    {
                        "row_number": row_index,
                        "field_name": "__all__",
                        "error_message": f"Unexpected error: {error}",
                        "raw_data": sanitized_raw,
                    }
                )
                continue

            success_count += 1
            if operation == "created":
                created_count += 1
            else:
                updated_count += 1

        error_report = self._write_error_report(errors) if errors else None

        if self.commit and import_job:
            self._persist_import_errors(import_job, errors)
            import_job.success_count = success_count
            import_job.error_count = len(errors)
            import_job.total_rows = total_rows
            if success_count == 0 and errors:
                import_job.status = ImportJob.STATUS_FAILED
            else:
                import_job.status = ImportJob.STATUS_COMPLETED
            import_job.save(
                update_fields=["success_count", "error_count", "total_rows", "status"]
            )

        return ImportRunResult(
            dataset_type=self.dataset_type,
            file_name=self.file_path.name,
            commit=self.commit,
            total_rows=total_rows,
            success_count=success_count,
            error_count=len(errors),
            created_count=created_count,
            updated_count=updated_count,
            required_fields=required_fields,
            job_id=import_job.id if import_job else None,
            job_status=import_job.status if import_job else None,
            error_report=error_report,
        )

    def _load_table(self, file_path: Path) -> pd.DataFrame:
        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            for encoding in ("utf-8-sig", "utf-8", "gb18030"):
                try:
                    return pd.read_csv(
                        file_path,
                        dtype=str,
                        keep_default_na=False,
                        encoding=encoding,
                    )
                except ParserError:
                    return pd.read_csv(
                        file_path,
                        dtype=str,
                        keep_default_na=False,
                        encoding=encoding,
                        engine="python",
                        on_bad_lines="skip",
                    )
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"Unable to decode CSV file: {file_path}")

        if suffix in {".xls", ".xlsx"}:
            return pd.read_excel(file_path, dtype=str)

        raise ValueError("Unsupported file format. Use CSV or Excel (.xls/.xlsx).")

    def _resolve_columns(self, columns: list[str]) -> dict[str, str]:
        field_aliases = (
            HERITAGE_FIELD_ALIASES
            if self.dataset_type == DATASET_HERITAGE
            else INHERITOR_FIELD_ALIASES
        )
        alias_map: dict[str, str] = {}
        for canonical_field, aliases in field_aliases.items():
            for alias in aliases:
                alias_map[_normalize_column_key(alias)] = canonical_field

        resolved: dict[str, str] = {}
        for original_name in columns:
            canonical = alias_map.get(_normalize_column_key(str(original_name)))
            if canonical and canonical not in resolved:
                resolved[canonical] = str(original_name)

        return resolved

    def _extract_canonical_row(
        self, raw_row: dict[str, Any], column_map: dict[str, str]
    ) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for field_name, source_column in column_map.items():
            normalized[field_name] = _normalize_text(raw_row.get(source_column))

        if self.default_level and not normalized.get("level"):
            normalized["level"] = self.default_level

        if self.default_country:
            if not normalized.get("country"):
                normalized["country"] = self.default_country

        return normalized

    def _import_heritage_row(self, row: dict[str, str]) -> str:
        name = row.get("name", "")
        category_name = row.get("category", "")
        category_code = row.get("category_code", "")
        level = row.get("level", "")
        country = row.get("country", "")
        country_code = row.get("country_code", "")

        if not name:
            raise RowImportError("name", "Missing required field: name")
        if not category_name and not category_code:
            raise RowImportError("category", "Missing required field: category/category_code")
        if not level:
            raise RowImportError("level", "Missing required field: level")
        if not country and not country_code:
            raise RowImportError("country", "Missing required field: country/country_code")

        normalized_level = self._normalize_level(level)
        category = self._resolve_category(category_name, category_code, normalized_level)
        region = self._resolve_region(country, country_code)

        defaults = {
            "level": normalized_level,
            "area": row.get("area", ""),
            "protection_unit": row.get("protection_unit", ""),
            "description": row.get("description", ""),
        }

        if self.commit:
            with transaction.atomic():
                _, created = HeritageItem.objects.update_or_create(
                    name=name,
                    category=category,
                    region=region,
                    defaults=defaults,
                )
            return "created" if created else "updated"

        exists = HeritageItem.objects.filter(
            name=name,
            category=category,
            region=region,
        ).exists()
        return "updated" if exists else "created"

    def _import_inheritor_row(self, row: dict[str, str]) -> str:
        name = row.get("name", "")
        heritage_name = row.get("heritage_name", "")
        heritage_id = row.get("heritage_id", "")
        country = row.get("country", "")
        country_code = row.get("country_code", "")

        if not name:
            raise RowImportError("name", "Missing required field: name")
        if not heritage_name and not heritage_id:
            raise RowImportError(
                "heritage_name",
                "Missing required field: heritage_name/heritage_id",
            )
        if not country and not country_code:
            raise RowImportError("country", "Missing required field: country/country_code")

        region = self._resolve_region(country, country_code)
        heritage_item = self._resolve_heritage_item(heritage_name, heritage_id, region.id)

        level_value = row.get("level", "")
        gender_value = row.get("gender", "")

        defaults = {
            "region": region,
            "level": self._normalize_level(level_value) if level_value else "",
            "gender": self._normalize_gender(gender_value) if gender_value else "",
            "area": row.get("area", ""),
            "description": row.get("description", ""),
        }

        if self.commit:
            with transaction.atomic():
                _, created = Inheritor.objects.update_or_create(
                    name=name,
                    heritage_item=heritage_item,
                    defaults=defaults,
                )
            return "created" if created else "updated"

        exists = Inheritor.objects.filter(name=name, heritage_item=heritage_item).exists()
        return "updated" if exists else "created"

    def _resolve_category(
        self,
        category_name: str,
        category_code: str,
        level: str,
    ) -> Category:
        if category_code:
            by_code = Category.objects.filter(code__iexact=category_code)
            if by_code.count() == 1:
                return by_code.first()
            if by_code.count() > 1:
                raise RowImportError(
                    "category",
                    f"Ambiguous category code match: {category_code}",
                )

        if category_name:
            by_name = Category.objects.filter(name__iexact=category_name, level=level)
            if by_name.count() == 1:
                return by_name.first()
            if by_name.count() > 1:
                raise RowImportError(
                    "category",
                    f"Ambiguous category name match: {category_name}",
                )

        raise RowImportError(
            "category",
            f"Category not found: name={category_name or '-'} code={category_code or '-'} level={level}",
        )

    def _resolve_region(self, country: str, country_code: str) -> Region:
        if country_code:
            region = Region.objects.filter(country_code__iexact=country_code).first()
            if region:
                return region

        for candidate in _split_country_candidates(country):
            region = Region.objects.filter(country_code__iexact=candidate).first()
            if region:
                return region

            region = Region.objects.filter(country_name__iexact=candidate).first()
            if region:
                return region

            iso_code = Region.normalize_country_code(candidate)
            if iso_code:
                region = Region.objects.filter(country_code__iexact=iso_code).first()
                if region:
                    return region

        raise RowImportError(
            "country",
            f"Region not found: country={country or '-'} country_code={country_code or '-'}",
        )

    def _resolve_heritage_item(
        self, heritage_name: str, heritage_id: str, region_id: int
    ) -> HeritageItem:
        queryset = HeritageItem.objects.all()

        if heritage_id:
            if not heritage_id.isdigit():
                raise RowImportError("heritage_id", f"Invalid heritage_id: {heritage_id}")
            queryset = queryset.filter(id=int(heritage_id))
        else:
            queryset = queryset.filter(name__iexact=heritage_name)

        by_region = queryset.filter(region_id=region_id)
        if by_region.count() == 1:
            return by_region.first()

        if by_region.count() > 1:
            raise RowImportError(
                "heritage_name",
                f"Ambiguous heritage item in region: {heritage_name or heritage_id}",
            )

        if queryset.count() == 1:
            return queryset.first()

        if queryset.count() > 1:
            raise RowImportError(
                "heritage_name",
                f"Ambiguous heritage item match: {heritage_name or heritage_id}",
            )

        raise RowImportError(
            "heritage_name",
            f"Heritage item not found: {heritage_name or heritage_id}",
        )

    def _normalize_level(self, level: str) -> str:
        normalized = LEVEL_ALIASES.get(_normalize_column_key(level))
        if not normalized:
            supported = ", ".join(sorted(set(LEVEL_ALIASES.values())))
            raise RowImportError("level", f"Unsupported level: {level}. Supported: {supported}")
        return normalized

    def _normalize_gender(self, gender: str) -> str:
        normalized = GENDER_ALIASES.get(_normalize_column_key(gender))
        if not normalized:
            supported = ", ".join(sorted(set(GENDER_ALIASES.values())))
            raise RowImportError(
                "gender",
                f"Unsupported gender: {gender}. Supported: {supported}",
            )
        return normalized

    def _persist_import_errors(
        self, import_job: ImportJob, errors: list[dict[str, Any]]
    ) -> None:
        if not errors:
            return

        error_records = [
            ImportError(
                import_job=import_job,
                row_number=error["row_number"],
                field_name=error["field_name"],
                error_message=error["error_message"],
                raw_data=error["raw_data"],
            )
            for error in errors
        ]

        for start in range(0, len(error_records), self.batch_size):
            ImportError.objects.bulk_create(error_records[start : start + self.batch_size])

    def _write_error_report(self, errors: list[dict[str, Any]]) -> str:
        if self.error_output:
            output_path = self.error_output
        else:
            repo_root = Path(__file__).resolve().parents[3]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = repo_root / "tmp" / f"import_errors_{self.dataset_type}_{timestamp}.csv"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["row_number", "field_name", "error_message", "raw_data"])
            for error in errors:
                writer.writerow(
                    [
                        error["row_number"],
                        error["field_name"],
                        error["error_message"],
                        json.dumps(error["raw_data"], ensure_ascii=False),
                    ]
                )

        return str(output_path)

    def _required_fields(self) -> tuple[str, ...]:
        if self.dataset_type == DATASET_HERITAGE:
            return HERITAGE_REQUIRED_FIELDS
        return INHERITOR_REQUIRED_FIELDS

    def _sanitize_raw_data(self, raw_row: dict[str, Any]) -> dict[str, str]:
        return {str(key): _normalize_text(value) for key, value in raw_row.items()}


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, float) and pd.isna(value):
        return ""

    text = str(value)
    if text.lower() == "nan":
        return ""
    return unicodedata.normalize("NFKC", text).strip()


def _normalize_column_key(value: str) -> str:
    normalized = _normalize_text(value).lower()
    return re.sub(r"[\s\-_./]+", "", normalized)


def _split_country_candidates(value: str) -> list[str]:
    text = _normalize_text(value)
    if not text:
        return []

    candidates = [segment.strip() for segment in re.split(r"[;|/]", text) if segment.strip()]
    if not candidates:
        return [text]

    expanded: list[str] = []
    for candidate in candidates:
        if "," in candidate:
            comma_parts = [item.strip() for item in candidate.split(",") if item.strip()]
            expanded.extend(comma_parts)
        expanded.append(candidate)
    return expanded
