"""
Import real air quality data from dataSource directory.

This script handles:
1. air_pollution_china.csv - 3000 records with virtual station IDs
2. BeiJing/*.xlsx - 12 Excel files with historical data (2013-2017)
"""
import csv
import os
import sys
import django
from datetime import datetime

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'air_quality_system.settings')
django.setup()

import pandas as pd
from django.utils import timezone
from apps.airquality.models import Province, City, MonitoringStation, AirQualityData

# City name mapping (Chinese to English)
CITY_NAME_MAP = {
    'Beijing': 'Beijing City',
    'Shanghai': 'Shanghai City',
    'Guangzhou': 'Guangzhou City',
    'Shenzhen': 'Shenzhen City',
    'Chengdu': 'Chengdu City',
}

# Fuzzy city name matching (partial match)
def find_city(name_part):
    """Find city by partial name match."""
    for key, value in CITY_NAME_MAP.items():
        if key in name_part or value in name_part:
            return City.objects.filter(name=value).first()
    return None

# Station name mapping for Beijing Excel files
BEIJING_STATION_MAP = {
    'Aotizhongxin.xlsx': {'name': '奥体中心', 'code': '1110A', 'address': '朝阳区奥林匹克体育中心', 'type': 'Urban'},
    'Changping.xlsx': {'name': '昌平', 'code': '1111A', 'address': '昌平区监测站', 'type': 'Suburban'},
    'Dingling.xlsx': {'name': '定陵', 'code': '1112A', 'address': '昌平区定陵监测点', 'type': 'Suburban'},
    'Dongsi.xlsx': {'name': '东四', 'code': '1113A', 'address': '东城区东四北大街', 'type': 'Urban'},
    'Guanyuan.xlsx': {'name': '官园', 'code': '1114A', 'address': '西城区官园', 'type': 'Urban'},
    'Gucheng.xlsx': {'name': '古城', 'code': '1115A', 'address': '石景山区古城大街', 'type': 'Urban'},
    'Huairou.xlsx': {'name': '怀柔', 'code': '1116A', 'address': '怀柔区监测站', 'type': 'Suburban'},
    'Nongzhanguan.xlsx': {'name': '农展馆', 'code': '1117A', 'address': '朝阳区农业展览馆', 'type': 'Urban'},
    'Shunyi.xlsx': {'name': '顺义', 'code': '1118A', 'address': '顺义区监测站', 'type': 'Suburban'},
    'Tiantan.xlsx': {'name': '天坛', 'code': '1119A', 'address': '东城区天坛', 'type': 'Urban'},
    'Wanliu.xlsx': {'name': '万柳', 'code': '111A0', 'address': '海淀区万柳地区', 'type': 'Urban'},
    'Wanshouxigong.xlsx': {'name': '万寿西宫', 'code': '111A1', 'address': '海淀区万寿西宫', 'type': 'Urban'},
}

def import_pollution_china_csv():
    """Import air_pollution_china.csv with virtual station mapping."""
    print('\n' + '='*60)
    print('Step 1: Importing air_pollution_china.csv')
    print('='*60)

    csv_file = os.path.join(os.path.dirname(__file__), 'air_pollution_china.csv')

    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return 0

    # Read CSV
    df = pd.read_csv(csv_file)
    print(f"Total records in file: {len(df)}")

    # Get Beijing city
    beijing_city = find_city('Beijing')
    if not beijing_city:
        print("Beijing city not found in database!")
        return 0

    records_created = 0
    records_skipped = 0

    # Group by Station ID and create virtual stations
    station_ids = df['Station ID'].unique()
    print(f"Unique Station IDs: {len(station_ids)}")

    for station_id in station_ids:
        # Create or get virtual station
        station_code = f"V{int(station_id):03d}"
        station_name = f"虚拟站点-{int(station_id)}"

        # Get coordinates for this station
        station_data = df[df['Station ID'] == station_id].iloc[0]
        latitude = station_data['Latitude']
        longitude = station_data['Longitude']

        station, created = MonitoringStation.objects.get_or_create(
            code=station_code,
            defaults={
                'name': station_name,
                'city': beijing_city,
                'address': f'虚拟监测点 {int(station_id)}',
                'station_type': 'Urban',
            }
        )

        if created:
            print(f"  Created virtual station: {station_code}")

        # Import data for this station
        station_df = df[df['Station ID'] == station_id]

        for _, row in station_df.iterrows():
            try:
                # Parse date - use column indices
                # Columns: 0:PM2.5, 1:PM10, 2:NO2, 3:SO2, 4:CO, 5:O3, ..., 13:AQI, 14:Season, 15:City, 16:Lat, 17:Lon, 18:DayOfWeek, 19:Hour, 20:Month, 21:Year, 22:Weather, 23:StationID
                year = int(row.iloc[21])   # Year column
                month = int(row.iloc[20])  # Month column
                hour = int(row.iloc[19])   # Hour column

                # Use day 1 (no day column available)
                day = 1

                monitor_time = timezone.make_aware(datetime(year, month, day, hour))

                # Check if record already exists
                if AirQualityData.objects.filter(station=station, monitor_time=monitor_time).exists():
                    continue

                # Extract pollutant values - use indices
                aqi = int(row.iloc[13]) if pd.notna(row.iloc[13]) else 50
                pm25 = safe_float(row.iloc[0])   # PM2.5
                pm10 = safe_float(row.iloc[1])   # PM10
                so2 = safe_float(row.iloc[3])    # SO2
                no2 = safe_float(row.iloc[2])    # NO2
                co = safe_float(row.iloc[4])     # CO
                o3 = safe_float(row.iloc[5])     # O3

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
                records_skipped += 1
                # print(f"    Error: {type(e).__name__}")

    print(f"\nRecords created: {records_created}")
    print(f"Records skipped: {records_skipped}")
    return records_created

def import_beijing_excel_files():
    """Import Beijing Excel files (2013-2017 historical data)."""
    print('\n' + '='*60)
    print('Step 2: Importing Beijing Excel Files')
    print('='*60)

    beijing_dir = os.path.join(os.path.dirname(__file__), 'BeiJing')

    if not os.path.exists(beijing_dir):
        print(f"Directory not found: {beijing_dir}")
        return 0

    # Get Beijing city
    beijing_city = find_city('Beijing')
    if not beijing_city:
        print("Beijing city not found in database!")
        return 0

    total_records = 0
    total_files = 0

    for filename, station_info in BEIJING_STATION_MAP.items():
        file_path = os.path.join(beijing_dir, filename)

        if not os.path.exists(file_path):
            print(f"File not found: {filename}")
            continue

        print(f"\nProcessing: {filename}")

        # Create or get station
        station, created = MonitoringStation.objects.get_or_create(
            code=station_info['code'],
            defaults={
                'name': station_info['name'],
                'city': beijing_city,
                'address': station_info['address'],
                'station_type': station_info['type'],
            }
        )

        if created:
            print(f"  Created station: {station_info['name']} ({station_info['code']})")

        # Read Excel file
        try:
            df = pd.read_excel(file_path)
            print(f"  Records in file: {len(df)}")
        except Exception as e:
            print(f"  Error reading file: {e}")
            continue

        records_created = 0
        records_skipped = 0

        for _, row in df.iterrows():
            try:
                # Parse date (Excel stores dates differently)
                date_val = row.iloc[0]  # First column is date

                # Handle different date formats
                if pd.isna(date_val):
                    records_skipped += 1
                    continue

                if isinstance(date_val, str):
                    # String date format like "2013-03-01"
                    date_parts = date_val.split('-')
                    if len(date_parts) >= 3:
                        year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
                    else:
                        continue
                else:
                    # Pandas Timestamp
                    year = date_val.year
                    month = date_val.month
                    day = date_val.day

                # Use noon as default time (historical data is daily)
                monitor_time = timezone.make_aware(datetime(year, month, day, 12, 0, 0))

                # Skip if record already exists
                if AirQualityData.objects.filter(station=station, monitor_time=monitor_time).exists():
                    records_skipped += 1
                    continue

                # Extract pollutant values (columns: date, AQI, level, PM2.5, PM10, SO2, CO, NO2, O3)
                aqi_val = row.iloc[1]
                pm25_val = row.iloc[3]
                pm10_val = row.iloc[4]
                so2_val = row.iloc[5]
                co_val = row.iloc[6]
                no2_val = row.iloc[7]
                o3_val = row.iloc[8]

                # Skip if AQI is missing
                if pd.isna(aqi_val):
                    records_skipped += 1
                    continue

                aqi = int(aqi_val)
                pm25 = float(pm25_val) if pd.notna(pm25_val) else 0
                pm10 = float(pm10_val) if pd.notna(pm10_val) else 0
                so2 = float(so2_val) if pd.notna(so2_val) else 0
                co = float(co_val) if pd.notna(co_val) else 0
                no2 = float(no2_val) if pd.notna(no2_val) else 0
                o3 = float(o3_val) if pd.notna(o3_val) else 0

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
                records_skipped += 1
                print(f"    Error processing row: {e}")
                continue

        print(f"  Records created: {records_created}")
        print(f"  Records skipped: {records_skipped}")

        total_records += records_created
        total_files += 1

    print(f"\n{'='*60}")
    print(f"Total files processed: {total_files}")
    print(f"Total records created: {total_records}")
    print('='*60)

    return total_records

def main():
    print("\n" + "="*60)
    print("Real Air Quality Data Import Script")
    print("="*60)

    # Step 1: Import air_pollution_china.csv
    count1 = import_pollution_china_csv()

    # Step 2: Import Beijing Excel files
    count2 = import_beijing_excel_files()

    # Summary
    print("\n" + "="*60)
    print("Import Summary")
    print("="*60)
    print(f"air_pollution_china.csv: {count1} records")
    print(f"Beijing Excel files: {count2} records")
    print(f"Total: {count1 + count2} records")

    # Verify total records in database
    total_db = AirQualityData.objects.count()
    print(f"\nTotal AirQualityData records in database: {total_db}")
    print("="*60)

if __name__ == '__main__':
    main()
