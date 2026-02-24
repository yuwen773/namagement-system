"""Phase 6.1: aggregate energy statistics into em_energy_statistics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from typing import Iterable

from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.utils import timezone

from scripts.config import setup_django


@dataclass(frozen=True)
class StatisticsJobResult:
    scanned_groups: int = 0
    created_count: int = 0
    updated_count: int = 0
    skipped_count: int = 0


_DEFAULT_RATES = {
    "WATER": Decimal("3.00"),
    "ELECTRICITY": Decimal("0.80"),
    "GAS": Decimal("2.20"),
}


def _as_aware(dt_date: date, is_end: bool) -> datetime:
    tz = timezone.get_current_timezone()
    dt = datetime.combine(dt_date, time.max if is_end else time.min)
    return timezone.make_aware(dt, tz)


def _period_defs(period_types: Iterable[str]):
    from apps.energy.models import PeriodType

    mapping = {
        PeriodType.DAY: TruncDate,
        PeriodType.MONTH: TruncMonth,
        PeriodType.YEAR: TruncYear,
    }
    for period_type in period_types:
        trunc = mapping.get(period_type)
        if trunc is not None:
            yield period_type, trunc


def _cost_for_row(energy_code: str, total_value: Decimal | None, rates: dict[str, Decimal]) -> Decimal:
    if total_value is None:
        return Decimal("0")
    rate = rates.get((energy_code or "").upper(), Decimal("0"))
    return (total_value * rate).quantize(Decimal("0.01"))


def generate_statistics(
    *,
    start_date: date | None = None,
    end_date: date | None = None,
    dry_run: bool = False,
    period_types: Iterable[str] = ("DAY", "MONTH", "YEAR"),
    rates: dict[str, Decimal] | None = None,
) -> StatisticsJobResult:
    """Generate day/month/year aggregates from EnergyData."""
    setup_django()

    from apps.energy.models import EnergyData, EnergyStatistics

    effective_rates = _DEFAULT_RATES.copy()
    if rates:
        effective_rates.update(rates)

    queryset = EnergyData.objects.select_related("energy_type")
    if start_date:
        queryset = queryset.filter(timestamp__gte=_as_aware(start_date, is_end=False))
    if end_date:
        queryset = queryset.filter(timestamp__lte=_as_aware(end_date, is_end=True))

    if not queryset.exists():
        return StatisticsJobResult(skipped_count=1)

    scanned_groups = 0
    created_count = 0
    updated_count = 0

    for period_type, trunc_func in _period_defs(period_types):
        grouped = (
            queryset.annotate(period_value=trunc_func("timestamp"))
            .values("device_id", "energy_type_id", "energy_type__code", "period_value")
            .annotate(total_value=Sum("value"), avg_value=Avg("value"))
            .order_by("device_id", "energy_type_id", "period_value")
        )

        for row in grouped:
            period_value = row["period_value"]
            if period_value is None:
                continue

            scanned_groups += 1
            period_date = period_value.date() if hasattr(period_value, "date") else period_value

            period_data = queryset.filter(
                device_id=row["device_id"],
                energy_type_id=row["energy_type_id"],
                timestamp__year=period_date.year,
            )
            if period_type == "MONTH":
                period_data = period_data.filter(timestamp__month=period_date.month)
            if period_type == "DAY":
                period_data = period_data.filter(timestamp__date=period_date)

            peak_row = period_data.order_by("-value", "timestamp").values("value", "timestamp").first()
            peak_value = peak_row["value"] if peak_row else None
            peak_time = peak_row["timestamp"] if peak_row else None

            defaults = {
                "total_value": row["total_value"] or Decimal("0"),
                "avg_value": row["avg_value"],
                "peak_value": peak_value,
                "peak_time": peak_time,
                "cost": _cost_for_row(row["energy_type__code"], row["total_value"], effective_rates),
            }

            if dry_run:
                continue

            _, created = EnergyStatistics.objects.update_or_create(
                device_id=row["device_id"],
                energy_type_id=row["energy_type_id"],
                period_type=period_type,
                period_date=period_date,
                defaults=defaults,
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

    if dry_run:
        return StatisticsJobResult(scanned_groups=scanned_groups)

    return StatisticsJobResult(
        scanned_groups=scanned_groups,
        created_count=created_count,
        updated_count=updated_count,
    )


if __name__ == "__main__":
    result = generate_statistics()
    print(result)
