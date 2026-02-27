"""
Comprehensive demo data generator for Energy Monitoring System.

This command generates:
1. Historical energy data for the past 90 days (hourly)
2. Daily statistics for the past 90 days
3. Monthly statistics for the past 12 months
4. Forecast data for the next 7-30 days
5. Comparison data with proper period labels
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Max, Sum
from django.utils import timezone

from apps.buildings.models import Building, Floor, Room
from apps.devices.models import Device, DeviceStatus, EnergyCode, EnergyType
from apps.energy.models import EnergyData, EnergyStatistics
from apps.analysis.models import EnergyForecast, ForecastTargetType


@dataclass(frozen=True)
class GenerationResult:
    devices_processed: int
    energy_data_created: int
    statistics_created: int
    forecasts_created: int


def generate_realistic_power(hour: float, seed: int) -> float:
    """Generate realistic power consumption based on time of day."""
    rng = random.Random(seed + int(hour))

    # Base load varies by time of day
    if 6 <= hour < 9:  # Morning peak
        base = 8.0 + rng.uniform(-1, 2)
    elif 9 <= hour < 12:  # Late morning
        base = 6.0 + rng.uniform(-0.5, 1)
    elif 12 <= hour < 14:  # Lunch dip
        base = 4.0 + rng.uniform(-0.5, 0.5)
    elif 14 <= hour < 18:  # Afternoon peak
        base = 7.0 + rng.uniform(-1, 1.5)
    elif 18 <= hour < 22:  # Evening
        base = 5.0 + rng.uniform(-0.5, 1)
    else:  # Night
        base = 2.0 + rng.uniform(-0.3, 0.5)

    # Add weekly pattern (weekends lower)
    day_of_week = (seed // 24) % 7
    if day_of_week >= 5:  # Weekend
        base *= 0.6

    # Add seasonal variation
    day_of_year = (seed // 24) % 365
    seasonal = 1.0 + 0.3 * math.sin(2 * math.pi * (day_of_year - 15) / 365)

    return max(0.5, base * seasonal + rng.uniform(-0.5, 0.5))


class Command(BaseCommand):
    help = "Generate comprehensive demo data for chart visualization"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=90,
            help="Number of historical days to generate"
        )
        parser.add_argument(
            "--forecast-days",
            type=int,
            default=30,
            help="Number of forecast days to generate"
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Batch size for bulk inserts"
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Skip days that already have data"
        )

    def handle(self, *args, **options):
        days = options["days"]
        forecast_days = options["forecast_days"]
        batch_size = options["batch_size"]
        skip_existing = options["skip_existing"]

        self.stdout.write(f"Generating demo data for {days} days + {forecast_days} forecast days...")

        result = self.generate_data(days, forecast_days, batch_size, skip_existing)

        self.stdout.write(self.style.SUCCESS(
            f"\nGeneration complete:\n"
            f"  Devices processed: {result.devices_processed}\n"
            f"  Energy data created: {result.energy_data_created}\n"
            f"  Statistics created: {result.statistics_created}\n"
            f"  Forecasts created: {result.forecasts_created}"
        ))

    def generate_data(
        self,
        days: int,
        forecast_days: int,
        batch_size: int,
        skip_existing: bool
    ) -> GenerationResult:
        """Generate all demo data."""

        # Get all energy types
        energy_types = list(EnergyType.objects.all())
        if not energy_types:
            self.stdout.write(self.style.ERROR("No energy types found. Please run init_db.sql first"))
            return GenerationResult(0, 0, 0, 0)

        # Get or create devices for each building
        devices = self.get_or_create_devices(energy_types)

        energy_data_count = 0
        stats_count = 0
        forecast_count = 0

        now = timezone.now()

        # Generate historical data
        for device in devices:
            with transaction.atomic():
                # Generate hourly energy data
                energy_data_count += self.generate_energy_data(
                    device, now, days, batch_size, skip_existing
                )

                # Generate daily statistics
                stats_count += self.generate_statistics(
                    device, now, days, skip_existing
                )

                # Generate monthly statistics
                stats_count += self.generate_monthly_statistics(
                    device, now, skip_existing
                )

                # Generate forecasts
                forecast_count += self.generate_forecasts(
                    device, now, forecast_days
                )

        return GenerationResult(
            devices_processed=len(devices),
            energy_data_created=energy_data_count,
            statistics_created=stats_count,
            forecasts_created=forecast_count
        )

    def get_or_create_devices(self, energy_types: list[EnergyType]) -> list[Device]:
        """Get existing devices or create new ones for each building."""
        devices = []
        buildings = Building.objects.all()

        if not buildings:
            # Create default campus and building if none exist
            from apps.buildings.models import Campus
            campus = Campus.objects.first()
            if not campus:
                campus = Campus.objects.create(
                    name="示例校区",
                    code="DEMO",
                    capacity=10000
                )

            building = Building.objects.create(
                campus=campus,
                name="示例教学楼",
                code="DEMO-B001",
                area_type="TEACHING",
                floors_count=3,
                gross_floor_area=15000
            )

            # Create floors
            for i in range(1, 4):
                Floor.objects.create(
                    building=building,
                    floor_number=i,
                    name=f"{i}F"
                )

            buildings = [building]

        for building in buildings:
            # Get or create floor and room
            floor = Floor.objects.filter(building=building).first()
            if not floor:
                floor = Floor.objects.create(
                    building=building,
                    floor_number=1,
                    name="1F"
                )

            room = Room.objects.filter(floor=floor).first()
            if not room:
                room = Room.objects.create(
                    floor=floor,
                    room_number="101",
                    room_type="CLASSROOM",
                    area=80
                )

            # Create device for each energy type
            for energy_type in energy_types:
                device_code = f"{energy_type.code}-{building.code}"

                device, created = Device.objects.get_or_create(
                    device_id=device_code,
                    defaults={
                        "name": f"{building.name}-{energy_type.name}表",
                        "energy_type": energy_type,
                        "room": room,
                        "status": DeviceStatus.ONLINE,
                    }
                )
                devices.append(device)

        return devices

    def generate_energy_data(
        self,
        device: Device,
        now: datetime,
        days: int,
        batch_size: int,
        skip_existing: bool
    ) -> int:
        """Generate hourly energy data for the specified period."""
        count = 0
        to_insert = []

        start_date = (now - timedelta(days=days)).replace(minute=0, second=0, microsecond=0)

        for day in range(days):
            current_date = start_date + timedelta(days=day)

            if skip_existing:
                existing = EnergyData.objects.filter(
                    device=device,
                    timestamp__date=current_date.date()
                ).exists()
                if existing:
                    continue

            # Generate hourly data for this day
            for hour in range(24):
                timestamp = current_date.replace(hour=hour)

                # Skip if exists
                if EnergyData.objects.filter(
                    device=device,
                    energy_type=device.energy_type,
                    timestamp=timestamp
                ).exists():
                    continue

                # Generate realistic power value
                seed = device.id * 1000 + day * 24 + hour
                power = generate_realistic_power(hour + day * 24, seed)

                # Calculate accumulated value (simulating meter reading)
                base_value = day * 24 * 5 + hour * 5  # Base accumulation
                value = base_value + power

                energy_data = EnergyData(
                    device=device,
                    energy_type=device.energy_type,
                    timestamp=timestamp,
                    value=round(value, 6),
                    power=round(power, 3),
                    voltage=220 if device.energy_type.code == EnergyCode.ELECTRICITY else None,
                    current=round(power / 220, 3) if device.energy_type.code == EnergyCode.ELECTRICITY else None,
                )
                to_insert.append(energy_data)
                count += 1

                if len(to_insert) >= batch_size:
                    EnergyData.objects.bulk_create(to_insert, ignore_conflicts=True)
                    to_insert.clear()

        if to_insert:
            EnergyData.objects.bulk_create(to_insert, ignore_conflicts=True)

        # Update device last_data_time
        device.last_data_time = now
        device.save(update_fields=["last_data_time"])

        return count

    def generate_statistics(
        self,
        device: Device,
        now: datetime,
        days: int,
        skip_existing: bool
    ) -> int:
        """Generate daily statistics from energy data."""
        count = 0
        start_date = (now - timedelta(days=days)).date()

        for day in range(days):
            period_date = start_date + timedelta(days=day)

            if skip_existing:
                existing = EnergyStatistics.objects.filter(
                    device=device,
                    period_type="DAY",
                    period_date=period_date
                ).exists()
                if existing:
                    continue

            # Calculate from energy data
            day_start = timezone.make_aware(datetime.combine(period_date, datetime.min.time()))
            day_end = day_start + timedelta(days=1)

            energy_data = EnergyData.objects.filter(
                device=device,
                timestamp__gte=day_start,
                timestamp__lt=day_end
            ).order_by("timestamp")

            if energy_data.count() < 2:
                continue

            first_value = energy_data.first().value
            last_value = energy_data.last().value
            total_value = max(0, last_value - first_value)

            # Calculate peak and average
            powers = [e.power for e in energy_data if e.power]
            peak_value = max(powers) if powers else None
            avg_value = sum(powers) / len(powers) if powers else None

            # Estimate cost (electricity: 0.8 yuan/kWh, water: 5 yuan/m3, gas: 3 yuan/m3)
            unit_price = {
                EnergyCode.ELECTRICITY: 0.8,
                EnergyCode.WATER: 5.0,
                EnergyCode.GAS: 3.0,
            }.get(device.energy_type.code, 1.0)

            cost = total_value * unit_price

            EnergyStatistics.objects.create(
                device=device,
                energy_type=device.energy_type,
                period_type="DAY",
                period_date=period_date,
                total_value=round(total_value, 6),
                peak_value=round(peak_value, 6) if peak_value else None,
                avg_value=round(avg_value, 6) if avg_value else None,
                peak_time=day_start.replace(hour=14) if peak_value else None,
                cost=round(cost, 2)
            )
            count += 1

        return count

    def generate_monthly_statistics(
        self,
        device: Device,
        now: datetime,
        skip_existing: bool
    ) -> int:
        """Generate monthly statistics for the past 12 months."""
        count = 0

        for month in range(12):
            # Calculate month date
            year = now.year - (1 if now.month - month <= 0 else 0)
            month_num = (now.month - month - 1) % 12 + 1
            period_date = datetime(year, month_num, 1).date()

            if skip_existing:
                existing = EnergyStatistics.objects.filter(
                    device=device,
                    period_type="MONTH",
                    period_date=period_date
                ).exists()
                if existing:
                    continue

            # Calculate month boundaries
            month_start = timezone.make_aware(datetime.combine(
                period_date.replace(day=1),
                datetime.min.time()
            ))

            if month_num == 12:
                month_end = timezone.make_aware(datetime.combine(
                    datetime(year + 1, 1, 1),
                    datetime.min.time()
                ))
            else:
                month_end = timezone.make_aware(datetime.combine(
                    datetime(year, month_num + 1, 1),
                    datetime.min.time()
                ))

            # Try to get from daily statistics first
            daily_stats = EnergyStatistics.objects.filter(
                device=device,
                period_type="DAY",
                period_date__gte=period_date,
                period_date__lt=month_end
            )

            if daily_stats.count() > 0:
                # Aggregate from daily stats
                total = daily_stats.aggregate(
                    total_value=Sum("total_value"),
                    peak_value=Max("peak_value"),
                    total_cost=Sum("cost")
                )

                if total["total_value"]:
                    total_avg = daily_stats.aggregate(
                        avg=Sum("avg_value") / daily_stats.count()
                    )
                    EnergyStatistics.objects.create(
                        device=device,
                        energy_type=device.energy_type,
                        period_type="MONTH",
                        period_date=period_date,
                        total_value=round(total["total_value"], 6),
                        peak_value=round(total["peak_value"], 6) if total["peak_value"] else None,
                        avg_value=round(total_avg["avg"], 6) if total_avg["avg"] else None,
                        cost=round(total["total_cost"] or 0, 2)
                    )
                    count += 1
            else:
                # Generate from energy data directly
                energy_data = EnergyData.objects.filter(
                    device=device,
                    timestamp__gte=month_start,
                    timestamp__lt=month_end
                ).order_by("timestamp")

                if energy_data.count() >= 2:
                    total_value = energy_data.last().value - energy_data.first().value
                    powers = [e.power for e in energy_data if e.power]
                    peak_value = max(powers) if powers else None
                    avg_value = sum(powers) / len(powers) if powers else None

                    unit_price = {
                        EnergyCode.ELECTRICITY: 0.8,
                        EnergyCode.WATER: 5.0,
                        EnergyCode.GAS: 3.0,
                    }.get(device.energy_type.code, 1.0)

                    cost = total_value * unit_price

                    EnergyStatistics.objects.create(
                        device=device,
                        energy_type=device.energy_type,
                        period_type="MONTH",
                        period_date=period_date,
                        total_value=round(total_value, 6),
                        peak_value=round(peak_value, 6) if peak_value else None,
                        avg_value=round(avg_value, 6) if avg_value else None,
                        cost=round(cost, 2)
                    )
                    count += 1

        return count

    def generate_forecasts(
        self,
        device: Device,
        now: datetime,
        days: int
    ) -> int:
        """Generate forecast data for the next N days."""
        count = 0

        # Get recent actual data for trend analysis
        recent_start = (now - timedelta(days=30)).date()
        recent_stats = EnergyStatistics.objects.filter(
            device=device,
            period_type="DAY",
            period_date__gte=recent_start
        ).order_by("period_date")

        # Calculate average daily consumption
        if recent_stats.count() > 0:
            avg_daily = recent_stats.aggregate(avg=Sum("total_value") / recent_stats.count())["avg"] or 50
        else:
            avg_daily = 50

        # Generate forecast
        for day in range(1, days + 1):
            forecast_date = (now.date() + timedelta(days=day))

            # Check if already exists
            if EnergyForecast.objects.filter(
                target_type="METER",
                target_id=str(device.device_id),
                forecast_date=forecast_date
            ).exists():
                continue

            # Add some variation and trend
            seed = device.id * 100 + day
            rng = random.Random(seed)

            # Weekly pattern
            day_of_week = (now.weekday() + day) % 7
            if day_of_week >= 5:  # Weekend
                weekend_factor = 0.7
            else:
                weekend_factor = 1.0

            # Add slight upward trend (1% per week)
            trend_factor = 1 + (day / 7) * 0.01

            # Random variation
            variation = rng.uniform(0.85, 1.15)

            forecast_value = avg_daily * weekend_factor * trend_factor * variation

            EnergyForecast.objects.create(
                target_type=ForecastTargetType.METER,
                target_id=str(device.device_id),
                energy_type=device.energy_type,
                forecast_date=forecast_date,
                forecast_value=round(forecast_value, 6),
                horizon_days=days,
                model_version="demo-v1",
                meter=device,
                campus=device.room.floor.building.campus if device.room else None,
                building=device.room.floor.building if device.room else None,
            )
            count += 1

        return count
