-- 考勤记录示例数据
-- 注意：此脚本用于测试环境，会清空现有的考勤记录

-- 清空考勤表（谨慎使用！）
-- TRUNCATE TABLE attendance_attendance;

-- 插入考勤记录
-- 用户1 (admin) 的考勤记录
INSERT INTO attendance_attendance (user_id, date, check_in_time, check_out_time, status, created_at, updated_at)
VALUES
    (1, '2024-01-22', '08:45:00', '18:30:00', 'normal', NOW(), NOW()),
    (1, '2024-01-23', '09:15:00', '18:00:00', 'late', NOW(), NOW()),
    (1, '2024-01-24', '08:50:00', '17:30:00', 'early', NOW(), NOW()),
    (1, '2024-01-25', '08:55:00', '19:00:00', 'normal', NOW(), NOW()),
    (1, '2024-01-26', '08:40:00', '18:20:00', 'normal', NOW(), NOW());

-- 用户2 的考勤记录（如果有）
INSERT INTO attendance_attendance (user_id, date, check_in_time, check_out_time, status, created_at, updated_at)
VALUES
    (2, '2024-01-22', '08:30:00', '18:45:00', 'normal', NOW(), NOW()),
    (2, '2024-01-23', '09:05:00', '18:30:00', 'late', NOW(), NOW()),
    (2, '2024-01-24', '08:55:00', '18:15:00', 'normal', NOW(), NOW()),
    (2, '2024-01-25', '08:40:00', '18:00:00', 'normal', NOW(), NOW()),
    (2, '2024-01-26', NULL, NULL, 'absent', NOW(), NOW());

-- 用户3 的考勤记录（如果有）
INSERT INTO attendance_attendance (user_id, date, check_in_time, check_out_time, status, created_at, updated_at)
VALUES
    (3, '2024-01-22', '08:50:00', '18:20:00', 'normal', NOW(), NOW()),
    (3, '2024-01-23', '08:45:00', '18:30:00', 'normal', NOW(), NOW()),
    (3, '2024-01-24', '09:20:00', '18:00:00', 'late', NOW(), NOW()),
    (3, '2024-01-25', '08:55:00', '17:40:00', 'early', NOW(), NOW()),
    (3, '2024-01-26', '08:30:00', '18:45:00', 'normal', NOW(), NOW());

-- 今日考勤记录示例（用于测试签到/签退）
INSERT INTO attendance_attendance (user_id, date, check_in_time, check_out_time, status, created_at, updated_at)
VALUES
    (1, CURDATE(), '09:30:00', NULL, 'late', NOW(), NOW());
