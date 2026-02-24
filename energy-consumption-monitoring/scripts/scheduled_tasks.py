"""Phase 6.4: cron-friendly scheduled task entrypoints."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
import json

from django.db.models import Count, Sum
from django.utils import timezone

from scripts.check_alarms import check_alarms
from scripts.config import setup_django
from scripts.generate_forecast import generate_forecast
from scripts.generate_statistics import generate_statistics


@dataclass(frozen=True)
class ScheduledResult:
    task: str
    detail: dict


def run_hourly_alarm_check(dry_run: bool = False) -> ScheduledResult:
    result = check_alarms(dry_run=dry_run)
    return ScheduledResult(
        task="hourly_alarm_check",
        detail={
            "threshold": result.threshold_created,
            "mutation": result.mutation_created,
            "offline": result.offline_created,
            "skipped_duplicates": result.skipped_duplicates,
        },
    )


def run_daily_statistics(dry_run: bool = False) -> ScheduledResult:
    target_day = timezone.localdate() - timedelta(days=1)
    stats_result = generate_statistics(
        start_date=target_day,
        end_date=target_day,
        dry_run=dry_run,
        period_types=("DAY", "MONTH", "YEAR"),
    )
    forecast_result = generate_forecast(dry_run=dry_run)
    return ScheduledResult(
        task="daily_statistics",
        detail={
            "day": target_day.isoformat(),
            "statistics_groups": stats_result.scanned_groups,
            "statistics_created": stats_result.created_count,
            "statistics_updated": stats_result.updated_count,
            "forecast_groups": forecast_result.target_groups,
            "forecast_points": forecast_result.generated_points,
        },
    )


def run_weekly_report(output_dir: str = "tmp/reports") -> ScheduledResult:
    setup_django()
    from apps.alarms.models import Alarm
    from apps.energy.models import EnergyStatistics, PeriodType

    today = timezone.localdate()
    start_day = today - timedelta(days=7)
    energy_rows = (
        EnergyStatistics.objects.filter(
            period_type=PeriodType.DAY,
            period_date__gte=start_day,
            period_date__lte=today,
        )
        .values("energy_type__code")
        .annotate(total_value=Sum("total_value"), records=Count("id"))
        .order_by("energy_type__code")
    )
    alarm_count = Alarm.objects.filter(alarm_time__date__gte=start_day, alarm_time__date__lte=today).count()

    payload = {
        "generated_at": timezone.now().isoformat(),
        "range": [start_day.isoformat(), today.isoformat()],
        "energy_summary": [
            {
                "energy_type": row["energy_type__code"],
                "total_value": float(row["total_value"] or 0),
                "records": int(row["records"] or 0),
            }
            for row in energy_rows
        ],
        "alarm_count": alarm_count,
    }

    report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"weekly-analysis-{today.isoformat()}.json"
    report_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    return ScheduledResult(task="weekly_report", detail={"report_file": str(report_file)})


def run_task(task: str, dry_run: bool = False) -> ScheduledResult:
    if task == "hourly":
        return run_hourly_alarm_check(dry_run=dry_run)
    if task == "daily":
        return run_daily_statistics(dry_run=dry_run)
    if task == "weekly":
        return run_weekly_report()
    raise ValueError(f"Unsupported task: {task}")
