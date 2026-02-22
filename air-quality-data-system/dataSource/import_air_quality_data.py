"""
Import air quality data from CSV file to database.
Run from project root: python backend/manage.py shell < import_script.py
"""
import csv
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_quality_system.settings')
django.setup()

from apps.airquality.models import AirQualityData, MonitoringStation
from django.utils import timezone

# Clear existing air quality data
print("Clearing existing air quality data...")
AirQualityData.objects.all().delete()
print(f"Cleared {AirQualityData.objects.count()} records")

# Import air quality data
csv_file = os.path.join(os.path.dirname(__file__), 'air_quality_data_sample.csv')
print(f"Importing air quality data from {csv_file}...")

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    records_to_create = []
    skipped_count = 0
    inserted_count = 0

    for row in reader:
        # Find the station
        try:
            station = MonitoringStation.objects.get(code=row['station_code'])
        except MonitoringStation.DoesNotExist:
            skipped_count += 1
            continue

        # Parse the monitor time
        from datetime import datetime
        monitor_time = datetime.strptime(row['monitor_time'], '%Y-%m-%d %H:%M:%S')

        # Make timezone-aware
        monitor_time = timezone.make_aware(monitor_time)

        # Create record
        records_to_create.append(AirQualityData(
            station=station,
            monitor_time=monitor_time,
            aqi=int(row['aqi']),
            pm25=float(row['pm25']),
            pm10=float(row['pm10']),
            so2=float(row['so2']),
            no2=float(row['no2']),
            co=float(row['co']),
            o3=float(row['o3'])
        ))

        # Batch create every 500 records
        if len(records_to_create) >= 500:
            AirQualityData.objects.bulk_create(records_to_create)
            inserted_count += len(records_to_create)
            print(f"  Inserted {inserted_count} records...")
            records_to_create = []

    # Insert remaining records
    if records_to_create:
        AirQualityData.objects.bulk_create(records_to_create)
        inserted_count += len(records_to_create)
        print(f"  Inserted {inserted_count} records...")

print(f"\nImport completed!")
print(f"Total AirQualityData records: {AirQualityData.objects.count()}")
print(f"Skipped records (station not found): {skipped_count}")
