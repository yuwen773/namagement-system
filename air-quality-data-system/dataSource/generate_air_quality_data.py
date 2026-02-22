"""
Generate sample air quality data CSV file for testing.
"""
import csv
from datetime import datetime, timedelta
import random

# Define station codes (matching the stations in stations.csv)
station_codes = [
    # Beijing
    '1101A', '1102A', '1103A', '1104A', '1105A', '1106A', '1107A', '1108A', '1109A',
    # Shanghai
    '1201A', '1202A', '1203A', '1204A',
    # Guangzhou
    '4401A', '4402A', '4403A', '4404A', '4405A', '4406A', '4407A', '4408A', '4409A',
    # Shenzhen
    '4401B', '4402B', '4403B', '4404B', '4405B', '4406B',
    # Chengdu
    '5101A', '5102A', '5103A', '5104A', '5105A', '5106A', '5107A'
]

# Generate hourly data for the past 7 days
end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
start_time = end_time - timedelta(days=7)

output_file = 'dataSource/air_quality_data_sample.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['station_code', 'monitor_time', 'aqi', 'pm25', 'pm10', 'so2', 'no2', 'co', 'o3'])

    current_time = start_time
    record_count = 0

    while current_time <= end_time:
        for station_code in station_codes:
            # Generate simulated data
            base_aqi = random.randint(30, 180)

            # Add daily variation (higher during daytime)
            hour_factor = 1 + 0.3 * (12 - abs(current_time.hour - 12)) / 12
            aqi = int(base_aqi * hour_factor)
            aqi = max(0, min(500, aqi))

            # Calculate PM values
            pm25 = round(aqi * 0.6 + random.uniform(-10, 10), 2)
            pm10 = round(aqi * 0.8 + random.uniform(-15, 15), 2)

            # Generate other pollutant values
            so2 = round(random.uniform(5, 30), 2)
            no2 = round(random.uniform(15, 50), 2)
            co = round(random.uniform(0.5, 2.5), 2)
            o3 = round(random.uniform(20, 120), 2)

            # Ensure PM values are not negative
            pm25 = max(0, pm25)
            pm10 = max(0, pm10)

            writer.writerow([
                station_code,
                current_time.strftime('%Y-%m-%d %H:%M:%S'),
                aqi, pm25, pm10, so2, no2, co, o3
            ])
            record_count += 1

        current_time += timedelta(hours=1)

print(f'Created {output_file} with {record_count} records')
print(f'Time range: {start_time} to {end_time}')
print(f'Stations: {len(station_codes)}')
