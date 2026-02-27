"""
Standalone script to generate comprehensive demo data for Energy Monitoring System.
This script connects directly to MySQL to avoid Django circular import issues.
"""
import math
import random
from datetime import datetime, timedelta
import pymysql

# Database configuration - UPDATE PASSWORD
DB_CONFIG = {
    'host': 'localhost',
    'port': int(os.environ.get('MYSQL_PORT', '3306')),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PWD', os.environ.get('MYSQL_PASSWORD', '123456')),
    'database': 'energy_monitoring',
    'charset': 'utf8mb4'
}


def get_connection():
    """Get MySQL database connection."""
    return pymysql.connect(**DB_CONFIG)


def get_devices(conn):
    """Get all devices from database."""
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT d.id, d.device_id, d.energy_type_id, et.code as energy_code,
                   r.floor_id, f.building_id, b.campus_id
            FROM em_devices d
            JOIN em_energy_types et ON d.energy_type_id = et.id
            LEFT JOIN em_rooms r ON d.room_id = r.id
            LEFT JOIN em_floors f ON r.floor_id = f.id
            LEFT JOIN em_buildings b ON f.building_id = b.id
        """)
        return cursor.fetchall()


def generate_realistic_power(hour, seed):
    """Generate realistic power consumption based on time of day."""
    rng = random.Random(seed + int(hour))

    # Base load varies by time of day
    if 6 <= hour < 9:
        base = 8.0 + rng.uniform(-1, 2)
    elif 9 <= hour < 12:
        base = 6.0 + rng.uniform(-0.5, 1)
    elif 12 <= hour < 14:
        base = 4.0 + rng.uniform(-0.5, 0.5)
    elif 14 <= hour < 18:
        base = 7.0 + rng.uniform(-1, 1.5)
    elif 18 <= hour < 22:
        base = 5.0 + rng.uniform(-0.5, 1)
    else:
        base = 2.0 + rng.uniform(-0.3, 0.5)

    # Weekly pattern
    day_of_week = (seed // 24) % 7
    if day_of_week >= 5:
        base *= 0.6

    # Seasonal variation
    day_of_year = (seed // 24) % 365
    seasonal = 1.0 + 0.3 * math.sin(2 * math.pi * (day_of_year - 15) / 365)

    return max(0.5, base * seasonal + rng.uniform(-0.5, 0.5))


def generate_energy_data(conn, devices, days=90):
    """Generate hourly energy data."""
    print(f"Generating energy data for {days} days...")

    now = datetime.now()
    start_date = (now - timedelta(days=days)).replace(minute=0, second=0, microsecond=0)

    count = 0
    batch_size = 1000
    to_insert = []

    for device in devices:
        device_id = device['id']
        energy_type_id = device['energy_type_id']
        energy_code = device['energy_code']

        # Get existing last value
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT value FROM em_energy_data
                WHERE device_id = %s AND energy_type_id = %s
                ORDER BY timestamp DESC LIMIT 1
            """, (device_id, energy_type_id))
            result = cursor.fetchone()
            base_value = result['value'] if result else 0.0

        value = float(base_value)

        for day in range(days):
            current_date = start_date + timedelta(days=day)

            for hour in range(24):
                timestamp = current_date.replace(hour=hour)

                # Check if exists
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id FROM em_energy_data
                        WHERE device_id = %s AND energy_type_id = %s AND timestamp = %s
                    """, (device_id, energy_type_id, timestamp))
                    if cursor.fetchone():
                        continue

                # Generate power
                seed = device_id * 1000 + day * 24 + hour
                power = generate_realistic_power(hour + day * 24, seed)
                value += power * 1.0  # 1 hour

                voltage = 220 if energy_code == 'ELECTRICITY' else None
                current_val = round(power / 220, 3) if energy_code == 'ELECTRICITY' else None

                to_insert.append((
                    device_id, energy_type_id, timestamp,
                    round(value, 6), voltage, current_val, round(power, 3)
                ))
                count += 1

                if len(to_insert) >= batch_size:
                    with conn.cursor() as cursor:
                        cursor.executemany("""
                            INSERT INTO em_energy_data
                            (device_id, energy_type_id, timestamp, value, voltage, current, power, source_type, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, 'MANUAL', NOW(), NOW())
                            ON DUPLICATE KEY UPDATE value = VALUES(value), power = VALUES(power)
                        """, to_insert)
                    conn.commit()
                    to_insert.clear()

        # Update device last_data_time
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE em_devices SET last_data_time = %s WHERE id = %s
            """, (now, device_id))
        conn.commit()

    if to_insert:
        with conn.cursor() as cursor:
            cursor.executemany("""
                INSERT INTO em_energy_data
                (device_id, energy_type_id, timestamp, value, voltage, current, power, source_type, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'MANUAL', NOW(), NOW())
                ON DUPLICATE KEY UPDATE value = VALUES(value), power = VALUES(power)
            """, to_insert)
        conn.commit()

    print(f"  Generated {count} energy data records")
    return count


def generate_statistics(conn, devices, days=90):
    """Generate daily statistics from energy data."""
    print(f"Generating statistics for {days} days...")

    count = 0
    now = datetime.now()
    start_date = (now - timedelta(days=days)).date()

    for device in devices:
        device_id = device['id']
        energy_type_id = device['energy_type_id']

        for day in range(days):
            period_date = start_date + timedelta(days=day)

            # Check if exists
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM em_energy_statistics
                    WHERE device_id = %s AND energy_type_id = %s AND period_type = 'DAY' AND period_date = %s
                """, (device_id, energy_type_id, period_date))
                if cursor.fetchone():
                    continue

            # Get energy data for this day
            day_start = datetime.combine(period_date, datetime.min.time())
            day_end = day_start + timedelta(days=1)

            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("""
                    SELECT value, power FROM em_energy_data
                    WHERE device_id = %s AND energy_type_id = %s
                    AND timestamp >= %s AND timestamp < %s
                    ORDER BY timestamp
                """, (device_id, energy_type_id, day_start, day_end))
                energy_data = cursor.fetchall()

            if len(energy_data) < 2:
                continue

            first_value = energy_data[0]['value']
            last_value = energy_data[-1]['value']
            total_value = max(0, float(last_value) - float(first_value))

            powers = [e['power'] for e in energy_data if e['power']]
            peak_value = max(powers) if powers else 0
            avg_value = sum(powers) / len(powers) if powers else 0

            # Estimate cost
            unit_price = {'ELECTRICITY': 0.8, 'WATER': 5.0, 'GAS': 3.0}.get(device['energy_code'], 1.0)
            cost = total_value * unit_price

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO em_energy_statistics
                    (device_id, energy_type_id, period_type, period_date, total_value, peak_value, avg_value, peak_time, cost, created_at, updated_at)
                    VALUES (%s, %s, 'DAY', %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON DUPLICATE KEY UPDATE total_value = VALUES(total_value)
                """, (device_id, energy_type_id, period_date, round(total_value, 6),
                      round(peak_value, 6) if peak_value else None,
                      round(avg_value, 6) if avg_value else None,
                      day_start.replace(hour=14) if peak_value else None,
                      round(cost, 2)))
                conn.commit()
                count += 1

    print(f"  Generated {count} statistics records")
    return count


def generate_forecasts(conn, devices, forecast_days=30):
    """Generate forecast data."""
    print(f"Generating forecasts for {forecast_days} days...")

    count = 0
    now = datetime.now()

    for device in devices:
        device_id = device['id']
        energy_type_id = device['energy_type_id']
        device_code = device['device_id']
        campus_id = device['campus_id']
        building_id = device['building_id']

        # Get average daily consumption
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT AVG(total_value) as avg_daily
                FROM em_energy_statistics
                WHERE device_id = %s AND energy_type_id = %s AND period_type = 'DAY'
                AND period_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            """, (device_id, energy_type_id))
            result = cursor.fetchone()
            avg_daily = float(result['avg_daily']) if result and result['avg_daily'] else 50.0

        for day in range(1, forecast_days + 1):
            forecast_date = (now.date() + timedelta(days=day))

            # Check if exists
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM em_energy_forecasts
                    WHERE target_type = 'METER' AND target_id = %s AND energy_type_id = %s AND forecast_date = %s
                """, (device_code, energy_type_id, forecast_date))
                if cursor.fetchone():
                    continue

            # Add variation
            seed = device_id * 100 + day
            rng = random.Random(seed)

            day_of_week = (now.weekday() + day) % 7
            weekend_factor = 0.7 if day_of_week >= 5 else 1.0
            trend_factor = 1 + (day / 7) * 0.01
            variation = rng.uniform(0.85, 1.15)

            forecast_value = avg_daily * weekend_factor * trend_factor * variation

            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO em_energy_forecasts
                    (target_type, target_id, energy_type_id, forecast_date, forecast_value, horizon_days, model_version, meter_id, campus_id, building_id, created_at, updated_at)
                    VALUES ('METER', %s, %s, %s, %s, %s, 'demo-v1', %s, %s, %s, NOW(), NOW())
                    ON DUPLICATE KEY UPDATE forecast_value = VALUES(forecast_value)
                """, (device_code, energy_type_id, forecast_date, round(forecast_value, 6),
                      forecast_days, device_id, campus_id, building_id))
                conn.commit()
                count += 1

    print(f"  Generated {count} forecast records")
    return count


def main():
    """Main function."""
    import os

    print("=== Energy Monitoring Demo Data Generator ===\n")

    # Get password from environment or use default
    DB_CONFIG['password'] = os.environ.get('MYSQL_PWD', '123456')
    print(f"Using MySQL password: {'***' if DB_CONFIG['password'] else '(empty)'}\n")

    try:
        conn = get_connection()
        print("Connected to database successfully\n")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        print("\nTry setting MYSQL_PWD environment variable:")
        print("  Windows: set MYSQL_PWD=your_password")
        print("  Linux/Mac: export MYSQL_PWD=your_password")
        return

    try:
        # Get devices
        devices = get_devices(conn)
        if not devices:
            print("No devices found. Please run init_db.sql first.")
            return

        print(f"Found {len(devices)} devices\n")

        # Generate data
        energy_count = generate_energy_data(conn, devices, days=90)
        stats_count = generate_statistics(conn, devices, days=90)
        forecast_count = generate_forecasts(conn, devices, forecast_days=30)

        print(f"\n=== Summary ===")
        print(f"Energy data: {energy_count} records")
        print(f"Statistics: {stats_count} records")
        print(f"Forecasts: {forecast_count} records")
        print("\nDemo data generation completed successfully!")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
