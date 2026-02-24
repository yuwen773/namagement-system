"""Phase 6.2: evaluate alarm rules and create alarms."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

from django.db.models import Q
from django.utils import timezone

from scripts.config import setup_django


@dataclass(frozen=True)
class AlarmCheckResult:
    threshold_created: int = 0
    mutation_created: int = 0
    offline_created: int = 0
    skipped_duplicates: int = 0


def _to_decimal(value) -> Decimal:
    try:
        return Decimal(str(value))
    except Exception:  # noqa: BLE001
        return Decimal("0")


def _mutation_threshold(raw_value: Decimal) -> Decimal:
    if raw_value > 1:
        return raw_value / Decimal("100")
    return raw_value


def _already_exists(
    *,
    alarm_model,
    device_id: int,
    alarm_type: str,
    rule_id: int | None,
    alarm_time,
    dedup_window_hours: int,
) -> bool:
    window_start = alarm_time - timedelta(hours=dedup_window_hours)
    query = alarm_model.objects.filter(
        device_id=device_id,
        alarm_type=alarm_type,
        alarm_time__gte=window_start,
    )
    if rule_id is None:
        query = query.filter(rule__isnull=True)
    else:
        query = query.filter(rule_id=rule_id)
    return query.exists()


def check_alarms(
    *,
    device_filter: str | None = None,
    dry_run: bool = False,
    offline_minutes: int = 120,
    dedup_window_hours: int = 6,
) -> AlarmCheckResult:
    setup_django()

    from apps.alarms.models import Alarm, AlarmRule, AlarmType, ConditionType
    from apps.devices.models import Device
    from apps.energy.models import EnergyData

    device_queryset = Device.objects.select_related("energy_type")
    if device_filter:
        if str(device_filter).isdigit():
            device_queryset = device_queryset.filter(pk=int(device_filter))
        else:
            device_queryset = device_queryset.filter(device_id=str(device_filter).strip())

    active_rules = AlarmRule.objects.filter(is_active=True).select_related("energy_type")
    now = timezone.now()

    threshold_created = 0
    mutation_created = 0
    offline_created = 0
    skipped_duplicates = 0

    # THRESHOLD/MUTATION: evaluate rule by device energy type
    for rule in active_rules:
        scoped_devices = device_queryset.filter(energy_type_id=rule.energy_type_id)
        for device in scoped_devices:
            if rule.condition_type == ConditionType.THRESHOLD:
                latest = (
                    EnergyData.objects.filter(device_id=device.id, energy_type_id=rule.energy_type_id)
                    .order_by("-timestamp", "-id")
                    .first()
                )
                if latest is None:
                    continue
                if _to_decimal(latest.value) <= _to_decimal(rule.threshold_value):
                    continue
                if _already_exists(
                    alarm_model=Alarm,
                    device_id=device.id,
                    alarm_type=AlarmType.THRESHOLD,
                    rule_id=rule.id,
                    alarm_time=latest.timestamp,
                    dedup_window_hours=dedup_window_hours,
                ):
                    skipped_duplicates += 1
                    continue
                if not dry_run:
                    Alarm.objects.create(
                        device_id=device.id,
                        rule_id=rule.id,
                        alarm_type=AlarmType.THRESHOLD,
                        alarm_value=latest.value,
                        alarm_time=latest.timestamp,
                    )
                threshold_created += 1

            if rule.condition_type == ConditionType.MUTATION:
                latest_two = list(
                    EnergyData.objects.filter(device_id=device.id, energy_type_id=rule.energy_type_id)
                    .order_by("-timestamp", "-id")[:2]
                )
                if len(latest_two) < 2:
                    continue
                current = _to_decimal(latest_two[0].value)
                previous = _to_decimal(latest_two[1].value)
                if previous == 0:
                    continue
                rate = abs(current - previous) / previous
                threshold = _mutation_threshold(_to_decimal(rule.threshold_value))
                if rate <= threshold:
                    continue
                if _already_exists(
                    alarm_model=Alarm,
                    device_id=device.id,
                    alarm_type=AlarmType.MUTATION,
                    rule_id=rule.id,
                    alarm_time=latest_two[0].timestamp,
                    dedup_window_hours=dedup_window_hours,
                ):
                    skipped_duplicates += 1
                    continue
                if not dry_run:
                    Alarm.objects.create(
                        device_id=device.id,
                        rule_id=rule.id,
                        alarm_type=AlarmType.MUTATION,
                        alarm_value=latest_two[0].value,
                        alarm_time=latest_two[0].timestamp,
                        remark=f"change_rate={rate:.4f}, threshold={threshold:.4f}",
                    )
                mutation_created += 1

    # OFFLINE: check all selected devices, independent of rule records
    offline_cutoff = now - timedelta(minutes=offline_minutes)
    offline_devices = device_queryset.filter(
        Q(last_data_time__isnull=True) | Q(last_data_time__lt=offline_cutoff)
    )
    for device in offline_devices:
        alarm_time = device.last_data_time or now
        if _already_exists(
            alarm_model=Alarm,
            device_id=device.id,
            alarm_type=AlarmType.OFFLINE,
            rule_id=None,
            alarm_time=alarm_time,
            dedup_window_hours=dedup_window_hours,
        ):
            skipped_duplicates += 1
            continue
        if not dry_run:
            Alarm.objects.create(
                device_id=device.id,
                rule=None,
                alarm_type=AlarmType.OFFLINE,
                alarm_value=None,
                alarm_time=alarm_time,
                remark=f"offline > {offline_minutes} minutes",
            )
        offline_created += 1

    return AlarmCheckResult(
        threshold_created=threshold_created,
        mutation_created=mutation_created,
        offline_created=offline_created,
        skipped_duplicates=skipped_duplicates,
    )


if __name__ == "__main__":
    print(check_alarms())
