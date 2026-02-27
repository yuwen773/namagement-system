-- ================================================================
-- Energy Monitoring System - Fix Demo Data for Visualization
-- This script fixes:
-- 1. Room departments (NULL -> proper values)
-- 2. Recent energy data (past 90 days + today)
-- 3. Forecast data (next 30 days)
-- ================================================================

USE `energy_monitoring`;

-- ================================================================
-- 1. Fix Room Departments
-- ================================================================
SET @dept_index = 0;

UPDATE em_rooms r
INNER JOIN (
    SELECT id,
        FLOOR((ROW_NUMBER() OVER (ORDER BY id) - 1) / 10) AS dept_group
    FROM em_rooms
    WHERE department IS NULL
) ranked ON r.id = ranked.id
SET r.department = CASE dept_group
    WHEN 0 THEN '计算机学院'
    WHEN 1 THEN '数学学院'
    WHEN 2 THEN '物理学院'
    WHEN 3 THEN '化学学院'
    WHEN 4 THEN '文学院'
    WHEN 5 THEN '外国语学院'
    WHEN 6 THEN '经济管理学院'
    ELSE '艺术学院'
END;

SELECT CONCAT('Updated departments for ', ROW_COUNT(), ' rooms') AS result;

-- ================================================================
-- 2. Clear and regenerate recent energy data (past 90 days)
-- ================================================================

-- First, clear recent data
DELETE FROM em_energy_data
WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL 90 DAY);

DELETE FROM em_energy_statistics
WHERE period_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY);

DELETE FROM em_energy_forecasts
WHERE forecast_date >= CURDATE();

-- ================================================================
-- 3. Generate Hourly Energy Data for Past 90 Days
-- ================================================================

DROP TEMPORARY TABLE IF EXISTS temp_dates;
CREATE TEMPORARY TABLE temp_dates (
    hour_index INT,
    hour_datetime DATETIME(6),
    day_index INT,
    hour_of_day INT,
    day_of_week INT
);

-- Generate hourly timestamps for past 90 days
INSERT INTO temp_dates
SELECT
    seq AS hour_index,
    DATE_SUB(DATE_SUB(CURDATE(), INTERVAL 90 DAY), INTERVAL -seq HOUR) AS hour_datetime,
    FLOOR(seq / 24) AS day_index,
    seq % 24 AS hour_of_day,
    FLOOR(seq / 24) % 7 AS day_of_week
FROM (
    SELECT t4.n * 10000 + t3.n * 1000 + t2.n * 100 + t1.n * 10 + t0.n AS seq
    FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
        UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t0
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
        UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
        UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
        UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t3
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2) t4
    WHERE t4.n * 10000 + t3.n * 1000 + t2.n * 100 + t1.n * 10 + t0.n < 90 * 24
) seq_table
WHERE DATE_SUB(DATE_SUB(CURDATE(), INTERVAL 90 DAY), INTERVAL -seq HOUR) < NOW();

-- Insert energy data with realistic patterns
INSERT INTO em_energy_data
(device_id, energy_type_id, timestamp, value, power, voltage, current, source_type, created_at, updated_at)
SELECT
    d.id AS device_id,
    d.energy_type_id,
    t.hour_datetime AS timestamp,
    -- Simulated accumulated value (meter reading)
    (t.day_index * 120 + t.hour_of_day * 5 +
        CASE
            WHEN t.hour_of_day BETWEEN 6 AND 9 THEN 20
            WHEN t.hour_of_day BETWEEN 9 AND 12 THEN 15
            WHEN t.hour_of_day BETWEEN 12 AND 14 THEN 10
            WHEN t.hour_of_day BETWEEN 14 AND 18 THEN 18
            WHEN t.hour_of_day BETWEEN 18 AND 22 THEN 12
            ELSE 5
        END +
        (d.id % 100) * 0.5 +
        RAND() * 10) AS value,
    -- Power varies by hour and day type
    CASE
        WHEN t.day_of_week >= 5 THEN  -- Weekend
            CASE
                WHEN t.hour_of_day BETWEEN 8 AND 22 THEN 3 + RAND() * 2
                ELSE 1 + RAND()
            END
        ELSE  -- Weekday
            CASE
                WHEN t.hour_of_day BETWEEN 6 AND 9 THEN 8 + RAND() * 4
                WHEN t.hour_of_day BETWEEN 9 AND 12 THEN 6 + RAND() * 3
                WHEN t.hour_of_day BETWEEN 12 AND 14 THEN 4 + RAND() * 2
                WHEN t.hour_of_day BETWEEN 14 AND 18 THEN 7 + RAND() * 4
                WHEN t.hour_of_day BETWEEN 18 AND 22 THEN 5 + RAND() * 3
                ELSE 2 + RAND() * 2
            END
    END * CASE et.code
        WHEN 'WATER' THEN 0.3
        WHEN 'GAS' THEN 0.2
        ELSE 1.0
    END AS power,
    220 AS voltage,
    CASE
        WHEN t.day_of_week >= 5 THEN
            CASE
                WHEN t.hour_of_day BETWEEN 8 AND 22 THEN (3 + RAND() * 2) / 220
                ELSE (1 + RAND()) / 220
            END
        ELSE
            CASE
                WHEN t.hour_of_day BETWEEN 6 AND 9 THEN (8 + RAND() * 4) / 220
                WHEN t.hour_of_day BETWEEN 9 AND 12 THEN (6 + RAND() * 3) / 220
                WHEN t.hour_of_day BETWEEN 12 AND 14 THEN (4 + RAND() * 2) / 220
                WHEN t.hour_of_day BETWEEN 14 AND 18 THEN (7 + RAND() * 4) / 220
                WHEN t.hour_of_day BETWEEN 18 AND 22 THEN (5 + RAND() * 3) / 220
                ELSE (2 + RAND() * 2) / 220
            END
    END AS current,
    'MANUAL' AS source_type,
    NOW() AS created_at,
    NOW() AS updated_at
FROM temp_dates t
CROSS JOIN em_devices d
INNER JOIN em_energy_types et ON d.energy_type_id = et.id
INNER JOIN em_rooms r ON d.room_id = r.id
WHERE t.hour_datetime >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
AND t.hour_datetime < NOW()
AND d.id <= 50  -- Limit to first 50 devices for reasonable dataset
ON DUPLICATE KEY UPDATE
    value = VALUES(value),
    power = VALUES(power),
    updated_at = NOW();

SELECT CONCAT('Generated ', ROW_COUNT(), ' energy data records') AS result;

-- Update device last_data_time
UPDATE em_devices d
SET last_data_time = (
    SELECT MAX(timestamp)
    FROM em_energy_data e
    WHERE e.device_id = d.id
),
status = 'ONLINE'
WHERE d.id <= 50;

-- ================================================================
-- 4. Generate Daily Statistics
-- ================================================================

INSERT INTO em_energy_statistics
(device_id, energy_type_id, period_type, period_date, total_value, peak_value, avg_value, peak_time, cost, created_at, updated_at)
SELECT
    s.device_id,
    s.energy_type_id,
    'DAY' AS period_type,
    s.period_date,
    s.total_value,
    s.peak_value,
    s.avg_value,
    DATE_ADD(s.period_date, INTERVAL 14 HOUR) AS peak_time,
    s.total_value *
        CASE et.code
            WHEN 'ELECTRICITY' THEN 0.8
            WHEN 'WATER' THEN 5.0
            WHEN 'GAS' THEN 3.0
            ELSE 1.0
        END AS cost,
    NOW() AS created_at,
    NOW() AS updated_at
FROM (
    SELECT
        e.device_id,
        e.energy_type_id,
        DATE(e.timestamp) AS period_date,
        MAX(e.value) - MIN(e.value) AS total_value,
        MAX(e.power) AS peak_value,
        AVG(e.power) AS avg_value
    FROM em_energy_data e
    WHERE e.timestamp >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
    GROUP BY e.device_id, e.energy_type_id, DATE(e.timestamp)
) s
JOIN em_energy_types et ON s.energy_type_id = et.id
ON DUPLICATE KEY UPDATE
    total_value = VALUES(total_value),
    peak_value = VALUES(peak_value),
    avg_value = VALUES(avg_value),
    cost = VALUES(cost),
    updated_at = NOW();

SELECT CONCAT('Generated ', ROW_COUNT(), ' daily statistics') AS result;

-- ================================================================
-- 5. Generate Monthly Statistics
-- ================================================================

INSERT INTO em_energy_statistics
(device_id, energy_type_id, period_type, period_date, total_value, peak_value, avg_value, cost, created_at, updated_at)
SELECT
    device_id,
    energy_type_id,
    'MONTH' AS period_type,
    month_date,
    SUM(total_value) AS total_value,
    MAX(peak_value) AS peak_value,
    AVG(avg_value) AS avg_value,
    SUM(cost) AS cost,
    NOW() AS created_at,
    NOW() AS updated_at
FROM (
    SELECT
        device_id,
        energy_type_id,
        DATE_FORMAT(period_date, '%Y-%m-01') AS month_date,
        total_value,
        peak_value,
        avg_value,
        cost
    FROM em_energy_statistics
    WHERE period_type = 'DAY'
    AND period_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
) s
GROUP BY device_id, energy_type_id, month_date
ON DUPLICATE KEY UPDATE
    total_value = VALUES(total_value),
    peak_value = VALUES(peak_value),
    avg_value = VALUES(avg_value),
    cost = VALUES(cost),
    updated_at = NOW();

SELECT CONCAT('Generated ', ROW_COUNT(), ' monthly statistics') AS result;

-- ================================================================
-- 6. Generate Forecast Data (next 30 days)
-- ================================================================

DROP TEMPORARY TABLE IF EXISTS temp_forecast_dates;
CREATE TEMPORARY TABLE temp_forecast_dates (
    forecast_day INT,
    forecast_date DATE,
    day_of_week INT
);

INSERT INTO temp_forecast_dates
SELECT
    seq AS forecast_day,
    DATE_ADD(CURDATE(), INTERVAL seq DAY) AS forecast_date,
    (DAYOFWEEK(DATE_ADD(CURDATE(), INTERVAL seq DAY)) - 1) % 7 AS day_of_week
FROM (
    SELECT t1.n * 10 + t0.n AS seq
    FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
        UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t0
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2) t1
    WHERE t1.n * 10 + t0.n < 30
) seq_table;

-- Get average daily consumption per device
DROP TEMPORARY TABLE IF EXISTS temp_avg_daily;
CREATE TEMPORARY TABLE temp_avg_daily AS
SELECT
    device_id,
    energy_type_id,
    AVG(total_value) AS avg_daily
FROM em_energy_statistics
WHERE period_type = 'DAY'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
AND period_date < CURDATE()
GROUP BY device_id, energy_type_id;

-- Generate forecasts
INSERT INTO em_energy_forecasts
(target_type, target_id, energy_type_id, forecast_date, forecast_value, horizon_days, model_version, meter_id, campus_id, building_id)
SELECT
    'METER' AS target_type,
    d.device_id AS target_id,
    d.energy_type_id,
    f.forecast_date,
    -- Forecast with weekly pattern and slight trend
    COALESCE(avg.avg_daily, 50) *
        (1 + (f.day_of_week >= 5) * -0.3) *  -- Weekend adjustment
        (1 + f.forecast_day * 0.005) *  -- Slight upward trend
        (0.9 + RAND() * 0.2) AS forecast_value,  -- Random variation
    30 AS horizon_days,
    'demo-v2' AS model_version,
    d.id AS meter_id,
    bld.campus_id,
    bld.id AS building_id
FROM temp_forecast_dates f
CROSS JOIN em_devices d
INNER JOIN em_rooms r ON d.room_id = r.id
INNER JOIN em_floors fl ON r.floor_id = fl.id
INNER JOIN em_buildings bld ON fl.building_id = bld.id
LEFT JOIN temp_avg_daily avg ON d.id = avg.device_id AND d.energy_type_id = avg.energy_type_id
WHERE d.id <= 50
AND f.forecast_date < DATE_ADD(CURDATE(), INTERVAL 30 DAY)
ON DUPLICATE KEY UPDATE
    forecast_value = VALUES(forecast_value),
    updated_at = NOW();

SELECT CONCAT('Generated ', ROW_COUNT(), ' forecast records') AS result;

-- ================================================================
-- 7. Summary
-- ================================================================
SELECT '=== Demo Data Fix Summary ===' AS '';
SELECT
    'Room departments updated' AS 'Task',
    COUNT(*) AS 'Count'
FROM em_rooms
WHERE department IS NOT NULL

UNION ALL

SELECT
    'Energy data (past 90 days)',
    COUNT(*)
FROM em_energy_data
WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)

UNION ALL

SELECT
    'Daily statistics (past 90 days)',
    COUNT(*)
FROM em_energy_statistics
WHERE period_type = 'DAY'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)

UNION ALL

SELECT
    'Monthly statistics (12 months)',
    COUNT(*)
FROM em_energy_statistics
WHERE period_type = 'MONTH'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)

UNION ALL

SELECT
    'Forecast data (next 30 days)',
    COUNT(*)
FROM em_energy_forecasts
WHERE forecast_date >= CURDATE()
AND forecast_date < DATE_ADD(CURDATE(), INTERVAL 30 DAY);

SELECT 'Demo data fix completed!' AS '';
