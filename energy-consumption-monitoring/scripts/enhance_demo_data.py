from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import math
import random

from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from scripts.config import setup_django


@dataclass(frozen=True)
class EnhanceResult:
    created_floors: int
    created_rooms: int
    created_devices: int
    created_energy_rows: int
    updated_last_data_time: int


def enhance_demo_data(
    *,
    hours: int = 72,
    interval_minutes: int = 15,
    batch_size: int = 2000,
) -> EnhanceResult:
    setup_django()

    from apps.buildings.models import Building, Floor, Room
    from apps.devices.models import Device, DeviceStatus, EnergyCode, EnergyType
    from apps.energy.models import EnergyData

    if hours <= 0:
        raise ValueError("hours must be > 0")
    if interval_minutes <= 0:
        raise ValueError("interval_minutes must be > 0")

    electricity = EnergyType.objects.filter(code=EnergyCode.ELECTRICITY).first()
    if not electricity:
        raise ValueError("EnergyType ELECTRICITY does not exist")

    created_floors = 0
    created_rooms = 0
    created_devices = 0
    updated_last_data_time = 0

    buildings = list(Building.objects.order_by("id"))
    if not buildings:
        return EnhanceResult(0, 0, 0, 0, 0)

    with transaction.atomic():
        for building in buildings:
            floor = Floor.objects.filter(building_id=building.id).order_by("floor_number", "id").first()
            if floor is None:
                floor = Floor.objects.create(building=building, floor_number=1, name="F1")
                created_floors += 1

            room = Room.objects.filter(floor__building_id=building.id).order_by("id").first()
            if room is None:
                room = Room.objects.create(floor=floor, room_number="101")
                created_rooms += 1

            has_device = Device.objects.filter(room__floor__building_id=building.id).exists()
            if has_device:
                continue

            device_code = f"ELEC-B{building.id:03d}"
            if Device.objects.filter(device_id=device_code).exists():
                device_code = f"ELEC-B{building.id:03d}-{random.randint(100, 999)}"
            Device.objects.create(
                device_id=device_code,
                name=f"Meter-{building.code}",
                energy_type=electricity,
                room=room,
                status=DeviceStatus.ONLINE,
            )
            created_devices += 1

    now = timezone.now()
    aligned_now = now.replace(second=0, microsecond=0)
    minute_shift = aligned_now.minute % interval_minutes
    if minute_shift:
        aligned_now = aligned_now - timedelta(minutes=minute_shift)
    points = max(1, int(hours * 60 / interval_minutes))
    start_time = aligned_now - timedelta(minutes=(points - 1) * interval_minutes)
    timestamps = [start_time + timedelta(minutes=interval_minutes * idx) for idx in range(points)]

    target_devices = list(
        Device.objects.select_related("energy_type").filter(
            room__isnull=False,
            room__floor__building__isnull=False,
        )
    )
    if not target_devices:
        return EnhanceResult(created_floors, created_rooms, created_devices, 0, 0)

    created_energy_rows = 0
    to_insert: list[EnergyData] = []
    end_time = timestamps[-1]

    for device in target_devices:
        existing_timestamps = set(
            EnergyData.objects.filter(
                device_id=device.id,
                timestamp__gte=start_time,
                timestamp__lte=end_time,
            ).values_list("timestamp", flat=True)
        )

        last_value = (
            EnergyData.objects.filter(device_id=device.id, timestamp__lt=start_time)
            .aggregate(max_value=Max("value"))
            .get("max_value")
        )
        value = float(last_value or 0.0)
        seed = device.id * 137
        rng = random.Random(seed)
        base = rng.uniform(2.0, 12.0)
        amplitude = rng.uniform(0.5, 3.5)
        phase = rng.uniform(0, math.pi)

        for idx, ts in enumerate(timestamps):
            if ts in existing_timestamps:
                continue

            hour = ts.hour + ts.minute / 60.0
            daily_cycle = math.sin((2 * math.pi * hour / 24.0) + phase)
            wave = math.sin((2 * math.pi * idx / 16.0) + phase / 2)
            power = max(0.2, base + amplitude * daily_cycle + 0.8 * wave + rng.uniform(-0.25, 0.25))
            value += power * (interval_minutes / 60.0)

            to_insert.append(
                EnergyData(
                    device_id=device.id,
                    energy_type_id=device.energy_type_id,
                    timestamp=ts,
                    value=round(value, 6),
                    power=round(power, 3),
                    voltage=220 if device.energy_type.code == EnergyCode.ELECTRICITY else None,
                )
            )

            if len(to_insert) >= batch_size:
                EnergyData.objects.bulk_create(to_insert, batch_size=batch_size, ignore_conflicts=True)
                created_energy_rows += len(to_insert)
                to_insert.clear()

        updated = Device.objects.filter(pk=device.id).update(last_data_time=end_time, status=DeviceStatus.ONLINE)
        updated_last_data_time += int(updated > 0)

    if to_insert:
        EnergyData.objects.bulk_create(to_insert, batch_size=batch_size, ignore_conflicts=True)
        created_energy_rows += len(to_insert)

    return EnhanceResult(
        created_floors=created_floors,
        created_rooms=created_rooms,
        created_devices=created_devices,
        created_energy_rows=created_energy_rows,
        updated_last_data_time=updated_last_data_time,
    )
