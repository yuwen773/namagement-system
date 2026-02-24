"""Phase 6.5: generate 7/30 day forecasts into em_energy_forecasts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count, Sum
from django.utils import timezone

from scripts.config import setup_django


@dataclass(frozen=True)
class ForecastJobResult:
    generated_points: int = 0
    target_groups: int = 0
    skipped_groups: int = 0


def _fit_linear(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) == 1:
        return 0.0, values[0]

    n = len(values)
    xs = list(range(n))
    sum_x = sum(xs)
    sum_y = sum(values)
    sum_x2 = sum(x * x for x in xs)
    sum_xy = sum(x * y for x, y in zip(xs, values))
    denominator = n * sum_x2 - sum_x * sum_x
    if denominator == 0:
        return 0.0, sum_y / n
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept


def _history_values(
    value_map: dict[date, float],
    end_date: date,
    days: int,
) -> list[float]:
    series = []
    for offset in range(days - 1, -1, -1):
        d = end_date - timedelta(days=offset)
        series.append(value_map.get(d, 0.0))
    return series


def generate_forecast(
    *,
    horizons: tuple[int, ...] = (7, 30),
    end_date: date | None = None,
    model_version: str = "linear-v1",
    dry_run: bool = False,
) -> ForecastJobResult:
    setup_django()

    from apps.analysis.models import EnergyForecast, ForecastTargetType
    from apps.energy.models import EnergyStatistics, PeriodType

    anchor_date = end_date or timezone.localdate()
    max_horizon = max(horizons)
    history_days = max(14, max_horizon * 2)
    history_start = anchor_date - timedelta(days=history_days - 1)

    base = EnergyStatistics.objects.filter(
        period_type=PeriodType.DAY,
        period_date__gte=history_start,
        period_date__lte=anchor_date,
    ).select_related("device", "device__room__floor__building", "energy_type")

    groups: list[tuple[str, int, int]] = []

    campus_rows = (
        base.values("device__room__floor__building__campus_id", "energy_type_id")
        .annotate(days=Count("id"))
        .order_by()
    )
    for row in campus_rows:
        if row["device__room__floor__building__campus_id"]:
            groups.append((ForecastTargetType.CAMPUS, row["device__room__floor__building__campus_id"], row["energy_type_id"]))

    building_rows = (
        base.values("device__room__floor__building_id", "energy_type_id")
        .annotate(days=Count("id"))
        .order_by()
    )
    for row in building_rows:
        if row["device__room__floor__building_id"]:
            groups.append((ForecastTargetType.BUILDING, row["device__room__floor__building_id"], row["energy_type_id"]))

    meter_rows = base.values("device_id", "energy_type_id").annotate(days=Count("id")).order_by()
    for row in meter_rows:
        groups.append((ForecastTargetType.METER, row["device_id"], row["energy_type_id"]))

    generated_points = 0
    target_groups = 0
    skipped_groups = 0

    # de-duplicate grouped keys
    for target_type, target_pk, energy_type_id in sorted(set(groups)):
        scoped = base.filter(energy_type_id=energy_type_id)
        if target_type == ForecastTargetType.CAMPUS:
            scoped = scoped.filter(device__room__floor__building__campus_id=target_pk)
        elif target_type == ForecastTargetType.BUILDING:
            scoped = scoped.filter(device__room__floor__building_id=target_pk)
        else:
            scoped = scoped.filter(device_id=target_pk)

        daily_rows = (
            scoped.values("period_date")
            .annotate(total_value=Sum("total_value"))
            .order_by("period_date")
        )
        value_map = {row["period_date"]: float(row["total_value"] or 0) for row in daily_rows}
        if not value_map:
            skipped_groups += 1
            continue

        target_groups += 1

        for horizon in horizons:
            history = _history_values(value_map, anchor_date, horizon)
            slope, intercept = _fit_linear(history)
            n = len(history)
            for step in range(1, horizon + 1):
                predict_date = anchor_date + timedelta(days=step)
                predicted = max(0.0, intercept + slope * (n + step - 1))
                defaults = {
                    "forecast_value": Decimal(str(round(predicted, 6))),
                    "model_version": model_version,
                }
                if target_type == ForecastTargetType.CAMPUS:
                    defaults.update({"campus_id": target_pk, "building": None, "meter": None})
                elif target_type == ForecastTargetType.BUILDING:
                    defaults.update({"campus": None, "building_id": target_pk, "meter": None})
                else:
                    defaults.update({"campus": None, "building": None, "meter_id": target_pk})

                if not dry_run:
                    EnergyForecast.objects.update_or_create(
                        target_type=target_type,
                        target_id=str(target_pk),
                        energy_type_id=energy_type_id,
                        forecast_date=predict_date,
                        horizon_days=horizon,
                        defaults=defaults,
                    )
                generated_points += 1

    return ForecastJobResult(
        generated_points=generated_points,
        target_groups=target_groups,
        skipped_groups=skipped_groups,
    )


if __name__ == "__main__":
    print(generate_forecast())
