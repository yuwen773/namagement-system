"""
Import air_pollution_china.csv with date inference.

This script infers actual dates from Year+Month+Hour+DayOfWeek.
"""
import csv
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_quality_system.settings')
django.setup()

import pandas as pd
from django.utils import timezone
from apps.airquality.models import City, MonitoringStation, AirQualityData

# Day of week mapping (English to Python weekday)
DAY_OF_WEEK_MAP = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}

def find_city(name_part):
    """Find city by partial name match."""
    city_map = {
        'Beijing': 'Beijing City',
        'Shanghai': 'Shanghai City',
        'Guangzhou': 'Guangzhou City',
        'Shenzhen': 'Shenzhen City',
        'Chengdu': 'Chengdu City',
    }
    for key, value in city_map.items():
        if key in name_part or value in name_part:
            return City.objects.filter(name=value).first()
    return None

def get_matching_dates(year, month, day_of_week):
    """
    Get all dates in a month that match a specific day of week.

    Args:
        year: Year (e.g., 2016)
        month: Month (1-12)
        day_of_week: Python weekday (0=Monday, 6=Sunday)

    Returns:
        List of datetime objects representing matching dates
    """
    matching_dates = []

    # Start from first day of the month
    current_date = datetime(year, month, 1)

    # Find all matching days in this month
    while current_date.month == month:
        if current_date.weekday() == day_of_week:
            matching_dates.append(current_date)
        current_date += timedelta(days=1)

    return matching_dates

def import_with_date_inference():
    """Import air_pollution_china.csv with date inference."""
    print('\n' + '='*60)
    print('Importing air_pollution_china.csv with Date Inference')
    print('='*60)

    csv_file = os.path.join(os.path.dirname(__file__), 'air_pollution_china.csv')

    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return

    # Read CSV
    df = pd.read_csv(csv_file, encoding='gbk')
    print(f"Total records in file: {len(df)}")

    # Get city for each record
    records_created = 0
    records_skipped = 0
    duplicate_count = 0
    error_count = 0

    # Group by City, Year, Month, Hour, DayOfWeek
    # For each group, we need to distribute records across matching dates
    grouped = df.groupby(['City', 'Year', 'Month', 'Hour', 'Day of Week'])

    print(f"Processing {len(grouped)} groups...")

    group_num = 0
    for (city_name, year, month, hour, day_of_week_str), group in grouped:
        group_num += 1
        if group_num <= 3:  # Print first 3 groups for debugging
            print(f"  Group {group_num}: {city_name}, {year}-{month:02d}, {hour}h, {day_of_week_str} ({len(group)} records)")

    for (city_name, year, month, hour, day_of_week_str), group in grouped:
        # Find or create city
        city = find_city(city_name)
        if not city:
            # Create virtual city if not exists
            from apps.airquality.models import Province
            province = Province.objects.first()  # Use existing province

            # Generate unique city code
            city_code = f"V{len(City.objects.all()) + 1:04d}"

            city, _ = City.objects.get_or_create(
                name=f"{city_name} City",
                defaults={
                    'code': city_code,
                    'province': province,
                    'longitude': 116.4074,
                    'latitude': 39.9042,
                }
            )

        # Get matching dates for this month/day_of_week combination
        day_of_week = DAY_OF_WEEK_MAP.get(day_of_week_str)
        if day_of_week is None:
            print(f"  Warning: Unknown day of week '{day_of_week_str}'")
            continue

        matching_dates = get_matching_dates(int(year), int(month), day_of_week)

        if not matching_dates:
            print(f"  Warning: No matching dates for {year}-{month:02d} {day_of_week_str}")
            continue

        # Create virtual station for this group
        station_code = f"V{int(year)%100:02d}{int(month):02d}{int(hour):02d}"
        station_name = f"{city_name} {year}-{month:02d}"

        station, created = MonitoringStation.objects.get_or_create(
            code=station_code,
            defaults={
                'name': station_name,
                'city': city,
                'address': f'虚拟监测点 {city_name}',
                'station_type': 'Urban',
            }
        )

        # Distribute records across matching dates
        for idx, (_, row) in enumerate(group.iterrows()):
            try:
                # Use corresponding date from matching dates
                date_idx = idx % len(matching_dates)
                match_date = matching_dates[date_idx]

                # Create full datetime
                monitor_time = timezone.make_aware(
                    datetime(match_date.year, match_date.month, match_date.day, int(hour))
                )

                # Check if record already exists
                if AirQualityData.objects.filter(
                    station=station,
                    monitor_time=monitor_time
                ).exists():
                    duplicate_count += 1
                    continue

                # Extract pollutant values - use column indices to avoid encoding issues
                # Columns: 0:PM2.5, 1:PM10, 2:NO2, 3:SO2, 4:CO, 5:O3, ..., 13:AQI, 14:Season, 15:City, 16:Lat, 17:Lon, 18:DayOfWeek, 19:Hour, 20:Month, 21:Year, 22:Weather, 23:StationID

                def safe_float(val):
                    if pd.isna(val):
                        return 0.0
                    try:
                        return float(val)
                    except:
                        return 0.0

                aqi = safe_float(row.iloc[13])
                pm25 = safe_float(row.iloc[0])
                pm10 = safe_float(row.iloc[1])
                so2 = safe_float(row.iloc[3])
                no2 = safe_float(row.iloc[2])
                co = safe_float(row.iloc[4])
                o3 = safe_float(row.iloc[5])

                AirQualityData.objects.create(
                    station=station,
                    monitor_time=monitor_time,
                    aqi=aqi,
                    pm25=pm25,
                    pm10=pm10,
                    so2=so2,
                    no2=no2,
                    co=co,
                    o3=o3,
                )
                records_created += 1

            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Only print first 5 errors
                    print(f"  Error: {type(e).__name__}: {e}")
                continue

    print(f"\nRecords created: {records_created}")
    print(f"Records skipped (duplicate): {duplicate_count}")
    print(f"Records skipped (error): {error_count}")
    print(f"Total skipped: {records_skipped}")
    print('='*60)

    return records_created

if __name__ == '__main__':
    count = import_with_date_inference()
    print(f"\nTotal records imported: {count}")

    # Verify total records
    from apps.airquality.models import AirQualityData
    print(f"Total AirQualityData records in database: {AirQualityData.objects.count()}")
