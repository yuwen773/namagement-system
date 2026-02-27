-- ================================================================
-- Energy Monitoring System - Demo Data Generator
-- This script generates comprehensive demo data for chart visualization
-- ================================================================

USE `energy_monitoring`;

-- Variables for configuration
SET @days_to_generate = 90;
SET @forecast_days = 30;
SET @current_date = NOW();

-- ================================================================
-- 1. Clear existing demo data (optional - uncomment if needed)
-- ================================================================
-- DELETE FROM em_energy_data WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL @days_to_generate DAY);
-- DELETE FROM em_energy_statistics WHERE period_date >= DATE_SUB(CURDATE(), INTERVAL @days_to_generate DAY);
-- DELETE FROM em_energy_forecasts WHERE forecast_date >= CURDATE();

-- ================================================================
-- 2. Generate Energy Data (hourly for past 90 days)
-- ================================================================
DROP TEMPORARY TABLE IF EXISTS temp_energy_data;
CREATE TEMPORARY TABLE temp_energy_data (
    device_id BIGINT,
    energy_type_id BIGINT,
    timestamp DATETIME(6),
    value DECIMAL(18, 6),
    power DECIMAL(12, 3),
    voltage DECIMAL(10, 3),
    current DECIMAL(10, 3),
    PRIMARY KEY (device_id, energy_type_id, timestamp)
);

-- Insert hourly data for each device
INSERT INTO temp_energy_data
SELECT
    d.id AS device_id,
    d.energy_type_id,
    timestamp_add(DATE_SUB(@current_date, INTERVAL @days_to_generate DAY), INTERVAL seq HOUR) AS timestamp,
    -- Simulated accumulated value
    (seq * 5.0 + (seq % 24) * 2.0 + (RAND() - 0.5) * 10.0) AS value,
    -- Simulated power (varies by hour)
    CASE
        WHEN (seq % 24) BETWEEN 6 AND 9 THEN 8 + RAND() * 4
        WHEN (seq % 24) BETWEEN 9 AND 12 THEN 6 + RAND() * 3
        WHEN (seq % 24) BETWEEN 12 AND 14 THEN 4 + RAND() * 2
        WHEN (seq % 24) BETWEEN 14 AND 18 THEN 7 + RAND() * 4
        WHEN (seq % 24) BETWEEN 18 AND 22 THEN 5 + RAND() * 3
        ELSE 2 + RAND() * 2
    END AS power,
    220 AS voltage,
    CASE
        WHEN (seq % 24) BETWEEN 6 AND 9 THEN (8 + RAND() * 4) / 220
        WHEN (seq % 24) BETWEEN 9 AND 12 THEN (6 + RAND() * 3) / 220
        WHEN (seq % 24) BETWEEN 12 AND 14 THEN (4 + RAND() * 2) / 220
        WHEN (seq % 24) BETWEEN 14 AND 18 THEN (7 + RAND() * 4) / 220
        WHEN (seq % 24) BETWEEN 18 AND 22 THEN (5 + RAND() * 3) / 220
        ELSE (2 + RAND() * 2) / 220
    END AS current
FROM (
    SELECT d.id, d.energy_type_id,
        (t4.n * 10000 + t3.n * 1000 + t2.n * 100 + t1.n * 10 + t0.n) AS seq
    FROM em_devices d
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
                UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t0
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
                UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
                UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) t3
    CROSS JOIN (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) t4
    WHERE (t4.n * 10000 + t3.n * 1000 + t2.n * 100 + t1.n * 10 + t0.n) < (@days_to_generate * 24)
) AS seq_table
WHERE d.room_id IS NOT NULL
HAVING timestamp < @current_date;

-- Insert into main table (ignore duplicates)
INSERT INTO em_energy_data
(device_id, energy_type_id, timestamp, value, power, voltage, current, source_type, created_at, updated_at)
SELECT device_id, energy_type_id, timestamp, value, power, voltage, current, 'MANUAL', NOW(), NOW()
FROM temp_energy_data
ON DUPLICATE KEY UPDATE
    value = VALUES(value),
    power = VALUES(power),
    updated_at = NOW();

-- Update device last_data_time
UPDATE em_devices d
SET last_data_time = (
    SELECT MAX(timestamp)
    FROM em_energy_data e
    WHERE e.device_id = d.id
),
    status = 'ONLINE'
WHERE d.room_id IS NOT NULL;

SELECT CONCAT('Energy data generated: ', COUNT(*), ' records') AS result
FROM temp_energy_data;

-- ================================================================
-- 3. Generate Daily Statistics
-- ================================================================
INSERT INTO em_energy_statistics
(device_id, energy_type_id, period_type, period_date, total_value, peak_value, avg_value, peak_time, cost, created_at, updated_at)
SELECT
    e.device_id,
    e.energy_type_id,
    'DAY' AS period_type,
    DATE(e.timestamp) AS period_date,
    MAX(e.value) - MIN(e.value) AS total_value,
    (SELECT MAX(power) FROM em_energy_data e2
     WHERE e2.device_id = e.device_id
     AND DATE(e2.timestamp) = DATE(e.timestamp)) AS peak_value,
    AVG(e.power) AS avg_value,
    DATE_ADD(DATE(e.timestamp), INTERVAL 14 HOUR) AS peak_time,
    (MAX(e.value) - MIN(e.value)) *
        CASE et.code
            WHEN 'ELECTRICITY' THEN 0.8
            WHEN 'WATER' THEN 5.0
            WHEN 'GAS' THEN 3.0
            ELSE 1.0
        END AS cost,
    NOW() AS created_at,
    NOW() AS updated_at
FROM em_energy_data e
JOIN em_energy_types et ON e.energy_type_id = et.id
WHERE e.timestamp >= DATE_SUB(CURDATE(), INTERVAL @days_to_generate DAY)
GROUP BY e.device_id, e.energy_type_id, DATE(e.timestamp)
ON DUPLICATE KEY UPDATE
    total_value = VALUES(total_value),
    peak_value = VALUES(peak_value),
    avg_value = VALUES(avg_value),
    cost = VALUES(cost),
    updated_at = NOW();

SELECT CONCAT('Daily statistics generated: ', COUNT(*), ' records') AS result
FROM em_energy_statistics
WHERE period_type = 'DAY'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL @days_to_generate DAY);

-- ================================================================
-- 4. Generate Monthly Statistics (aggregate from daily)
-- ================================================================
INSERT INTO em_energy_statistics
(device_id, energy_type_id, period_type, period_date, total_value, peak_value, avg_value, cost, created_at, updated_at)
SELECT
    device_id,
    energy_type_id,
    'MONTH' AS period_type,
    DATE_FORMAT(period_date, '%Y-%m-01') AS month_date,
    SUM(total_value) AS total_value,
    MAX(peak_value) AS peak_value,
    AVG(avg_value) AS avg_value,
    SUM(cost) AS cost,
    NOW() AS created_at,
    NOW() AS updated_at
FROM em_energy_statistics
WHERE period_type = 'DAY'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY device_id, energy_type_id, DATE_FORMAT(period_date, '%Y-%m')
ON DUPLICATE KEY UPDATE
    total_value = VALUES(total_value),
    peak_value = VALUES(peak_value),
    avg_value = VALUES(avg_value),
    cost = VALUES(cost),
    updated_at = NOW();

SELECT CONCAT('Monthly statistics generated: ', COUNT(*), ' records') AS result
FROM em_energy_statistics
WHERE period_type = 'MONTH'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH);

-- ================================================================
-- 5. Generate Forecast Data
-- ================================================================
DROP TEMPORARY TABLE IF EXISTS temp_forecasts;
CREATE TEMPORARY TABLE temp_forecasts (
    target_type VARCHAR(16),
    target_id VARCHAR(64),
    energy_type_id BIGINT,
    forecast_date DATE,
    forecast_value DECIMAL(18, 6),
    horizon_days INT,
    model_version VARCHAR(64),
    meter_id BIGINT,
    campus_id BIGINT,
    building_id BIGINT
);

-- Get average daily consumption for each device
INSERT INTO temp_forecasts
SELECT
    'METER' AS target_type,
    d.device_id AS target_id,
    d.energy_type_id,
    DATE_ADD(CURDATE(), INTERVAL seq DAY) AS forecast_date,
    -- Forecast value with variation
    COALESCE(daily_avg.avg_daily, 50) *
        (1 + (seq % 7) * 0.05) *  -- Weekly pattern
        (1 + (seq / 30) * 0.01) *  -- Slight upward trend
        (0.9 + RAND() * 0.2) AS forecast_value,  -- Random variation
    @forecast_days AS horizon_days,
    'demo-v1' AS model_version,
    d.id AS meter_id,
    r.campus_id,
    r.building_id
FROM em_devices d
LEFT JOIN em_rooms r ON d.room_id = r.id
LEFT JOIN (
    SELECT device_id, energy_type_id, AVG(total_value) AS avg_daily
    FROM em_energy_statistics
    WHERE period_type = 'DAY'
    AND period_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY device_id, energy_type_id
) daily_avg ON d.id = daily_avg.device_id AND d.energy_type_id = daily_avg.energy_type_id
CROSS JOIN (
    SELECT 0 AS seq UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
    UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9
    UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14
    UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19
    UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23 UNION SELECT 24
    UNION SELECT 25 UNION SELECT 26 UNION SELECT 27 UNION SELECT 28 UNION SELECT 29
) seq_table
WHERE d.room_id IS NOT NULL
AND seq < @forecast_days;

-- Insert into main table
INSERT INTO em_energy_forecasts
(target_type, target_id, energy_type_id, forecast_date, forecast_value, horizon_days, model_version, meter_id, campus_id, building_id, created_at, updated_at)
SELECT * FROM temp_forecasts
ON DUPLICATE KEY UPDATE
    forecast_value = VALUES(forecast_value),
    updated_at = NOW();

SELECT CONCAT('Forecast data generated: ', COUNT(*), ' records') AS result
FROM temp_forecasts;

-- ================================================================
-- 6. Summary
-- ================================================================
SELECT '=== Demo Data Generation Summary ===' AS '';
SELECT
    'Energy Data (90 days hourly)' AS 'Data Type',
    COUNT(*) AS 'Records Generated'
FROM em_energy_data
WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL @days_to_generate DAY)

UNION ALL

SELECT
    'Daily Statistics (90 days)',
    COUNT(*)
FROM em_energy_statistics
WHERE period_type = 'DAY'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL @days_to_generate DAY)

UNION ALL

SELECT
    'Monthly Statistics (12 months)',
    COUNT(*)
FROM em_energy_statistics
WHERE period_type = 'MONTH'
AND period_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)

UNION ALL

SELECT
    'Forecasts (30 days)',
    COUNT(*)
FROM em_energy_forecasts
WHERE forecast_date >= CURDATE()
AND forecast_date < DATE_ADD(CURDATE(), INTERVAL @forecast_days DAY);

SELECT 'Demo data generation completed!' AS '';
