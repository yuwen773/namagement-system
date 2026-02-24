"""Phase 6.3: optional Spark offline analysis with Python fallback."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import json

from django.db.models import Avg, Count, Sum

from scripts.config import setup_django


@dataclass(frozen=True)
class SparkAnalysisResult:
    mode: str
    rows_written: int
    output_path: str


def _python_fallback(output_path: Path) -> SparkAnalysisResult:
    from apps.energy.models import EnergyData

    rows = (
        EnergyData.objects.values("energy_type__code")
        .annotate(total_value=Sum("value"), avg_value=Avg("value"), records=Count("id"))
        .order_by("energy_type__code")
    )
    payload = [
        {
            "energy_type": row["energy_type__code"],
            "total_value": float(row["total_value"] or 0),
            "avg_value": float(row["avg_value"] or 0),
            "records": int(row["records"] or 0),
        }
        for row in rows
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return SparkAnalysisResult(mode="python-fallback", rows_written=len(payload), output_path=str(output_path))


def run_spark_offline_analysis(
    *,
    output_file: str = "tmp/reports/spark_offline_analysis.json",
) -> SparkAnalysisResult:
    setup_django()

    output_path = Path(output_file)
    try:
        from pyspark.sql import SparkSession
    except Exception:  # noqa: BLE001
        return _python_fallback(output_path)

    from apps.energy.models import EnergyData

    rows = list(
        EnergyData.objects.values("energy_type__code", "value", "timestamp")
    )
    if not rows:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("[]", encoding="utf-8")
        return SparkAnalysisResult(mode="spark", rows_written=0, output_path=str(output_path))

    spark = SparkSession.builder.appName("energy-offline-analysis").getOrCreate()
    try:
        frame = spark.createDataFrame(rows)
        result = (
            frame.groupBy("energy_type__code")
            .sum("value")
            .withColumnRenamed("energy_type__code", "energy_type")
            .withColumnRenamed("sum(value)", "total_value")
        )
        records = [row.asDict() for row in result.collect()]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        return SparkAnalysisResult(mode="spark", rows_written=len(records), output_path=str(output_path))
    finally:
        spark.stop()


if __name__ == "__main__":
    print(run_spark_offline_analysis())
