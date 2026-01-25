-- =====================================================
-- 测试数据插入脚本 - 2025年下半年至2026年1月
-- 时间范围: 2025-07-01 至 2026-01-25
-- =====================================================

USE hrms_db;

-- =====================================================
-- 1. 新增员工用户数据 (2025年下半年入职)
-- =====================================================

-- 技术研发部新员工
INSERT INTO accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, phone, role, real_name, email) VALUES
(101, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0101', '', '', 0, 1, '2025-07-01', '13900000101', 'employee', '新研发A', 'xinfa@hrms.com'),
(102, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0102', '', '', 0, 1, '2025-07-15', '13900000102', 'employee', '新研发B', 'xinfb@hrms.com'),
(103, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0103', '', '', 0, 1, '2025-08-01', '13900000103', 'employee', '新研发C', 'xinfc@hrms.com'),
(104, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0104', '', '', 0, 1, '2025-09-01', '13900000104', 'employee', '新研发D', 'xinfd@hrms.com'),
(105, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0105', '', '', 0, 1, '2025-10-01', '13900000105', 'employee', '新研发E', 'xinfe@hrms.com'),
(106, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0106', '', '', 0, 1, '2025-11-01', '13900000106', 'employee', '新研发F', 'xinff@hrms.com'),
(107, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0107', '', '', 0, 1, '2025-12-01', '13900000107', 'employee', '新研发G', 'xinfg@hrms.com'),
(108, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0108', '', '', 0, 1, '2026-01-05', '13900000108', 'employee', '新研发H', 'xinfh@hrms.com');

-- 产品部新员工
INSERT INTO accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, phone, role, real_name, email) VALUES
(109, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0109', '', '', 0, 1, '2025-07-10', '13900000109', 'employee', '新产品A', 'xinprda@hrms.com'),
(110, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0110', '', '', 0, 1, '2025-09-15', '13900000110', 'employee', '新产品B', 'xinprdb@hrms.com'),
(111, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0111', '', '', 0, 1, '2025-11-01', '13900000111', 'employee', '新产品C', 'xinprdc@hrms.com');

-- 市场部新员工
INSERT INTO accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, phone, role, real_name, email) VALUES
(112, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0112', '', '', 0, 1, '2025-08-01', '13900000112', 'employee', '新市场A', 'xinmkta@hrms.com'),
(113, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0113', '', '', 0, 1, '2025-10-01', '13900000113', 'employee', '新市场B', 'xinmktb@hrms.com');

-- 运营部新员工
INSERT INTO accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, phone, role, real_name, email) VALUES
(114, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0114', '', '', 0, 1, '2025-07-20', '13900000114', 'employee', '新运营A', 'xinopsa@hrms.com'),
(115, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0115', '', '', 0, 1, '2025-12-01', '13900000115', 'employee', '新运营B', 'xinopsb@hrms.com');

-- 设计部新员工
INSERT INTO accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, phone, role, real_name, email) VALUES
(116, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0116', '', '', 0, 1, '2025-09-01', '13900000116', 'employee', '新设计A', 'xindesa@hrms.com');

-- 财务部新员工
INSERT INTO accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, phone, role, real_name, email) VALUES
(117, 'pbkdf2_sha256$1000000$test$N9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NULL, 0, 'emp0117', '', '', 0, 1, '2025-08-15', '13900000117', 'employee', '新财务A', 'xinfina@hrms.com');

-- =====================================================
-- 2. 员工档案数据 (对应新用户)
-- =====================================================

-- 技术研发部档案
INSERT INTO employee_employeeprofile (id, employee_no, hire_date, salary_base, status, resigned_date, resigned_reason, created_at, updated_at, department_id, post_id, user_id) VALUES
(101, 'EMP202507TECH101', '2025-07-01', 12000.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 101),
(102, 'EMP202507TECH102', '2025-07-15', 11000.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 102),
(103, 'EMP202508TECH103', '2025-08-01', 11500.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 103),
(104, 'EMP202509TECH104', '2025-09-01', 12000.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 104),
(105, 'EMP202510TECH105', '2025-10-01', 12500.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 105),
(106, 'EMP202511TECH106', '2025-11-01', 12000.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 106),
(107, 'EMP202512TECH107', '2025-12-01', 13000.00, 'active', NULL, '', NOW(), NOW(), 1, 4, 107),
(108, 'EMP202601TECH108', '2026-01-05', 11500.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 108);

-- 产品部档案
INSERT INTO employee_employeeprofile (id, employee_no, hire_date, salary_base, status, resigned_date, resigned_reason, created_at, updated_at, department_id, post_id, user_id) VALUES
(109, 'EMP202507PRD109', '2025-07-10', 13000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 109),
(110, 'EMP202509PRD110', '2025-09-15', 13500.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 110),
(111, 'EMP202511PRD111', '2025-11-01', 14000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 111);

-- 市场部档案
INSERT INTO employee_employeeprofile (id, employee_no, hire_date, salary_base, status, resigned_date, resigned_reason, created_at, updated_at, department_id, post_id, user_id) VALUES
(112, 'EMP202508MKT112', '2025-08-01', 10000.00, 'active', NULL, '', NOW(), NOW(), 3, 1, 112),
(113, 'EMP202510MKT113', '2025-10-01', 10500.00, 'active', NULL, '', NOW(), NOW(), 3, 2, 113);

-- 运营部档案
INSERT INTO employee_employeeprofile (id, employee_no, hire_date, salary_base, status, resigned_date, resigned_reason, created_at, updated_at, department_id, post_id, user_id) VALUES
(114, 'EMP202507OPS114', '2025-07-20', 9000.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 114),
(115, 'EMP202512OPS115', '2025-12-01', 9500.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 115);

-- 设计部档案
INSERT INTO employee_employeeprofile (id, employee_no, hire_date, salary_base, status, resigned_date, resigned_reason, created_at, updated_at, department_id, post_id, user_id) VALUES
(116, 'EMP202509DES116', '2025-09-01', 11500.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 116);

-- 财务部档案
INSERT INTO employee_employeeprofile (id, employee_no, hire_date, salary_base, status, resigned_date, resigned_reason, created_at, updated_at, department_id, post_id, user_id) VALUES
(117, 'EMP202508FIN117', '2025-08-15', 10000.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 117);

-- =====================================================
-- 3. 离职员工数据 (2025年下半年)
-- =====================================================

-- 更新现有员工为离职状态
UPDATE employee_employeeprofile SET status = 'resigned', resigned_date = '2025-08-15', resigned_reason = '个人发展原因' WHERE user_id = 35;
UPDATE accounts_user SET is_active = 0 WHERE id = 35;

UPDATE employee_employeeprofile SET status = 'resigned', resigned_date = '2025-09-30', resigned_reason = '家庭原因' WHERE user_id = 49;
UPDATE accounts_user SET is_active = 0 WHERE id = 49;

UPDATE employee_employeeprofile SET status = 'resigned', resigned_date = '2025-10-20', resigned_reason = '薪资不满意' WHERE user_id = 58;
UPDATE accounts_user SET is_active = 0 WHERE id = 58;

UPDATE employee_employeeprofile SET status = 'resigned', resigned_date = '2025-11-15', resigned_reason = '回老家发展' WHERE user_id = 68;
UPDATE accounts_user SET is_active = 0 WHERE id = 68;

UPDATE employee_employeeprofile SET status = 'resigned', resigned_date = '2025-12-31', resigned_reason = '合同到期不续签' WHERE user_id = 76;
UPDATE accounts_user SET is_active = 0 WHERE id = 76;

-- =====================================================
-- 4. 考勤数据 (2025年7月至2026年1月)
-- =====================================================

DELIMITER //

-- 为每个员工生成月度考勤数据
DROP PROCEDURE IF EXISTS generate_attendance_data//
CREATE PROCEDURE generate_attendance_data(IN start_user_id INT, IN end_user_id INT, IN start_date DATE, IN end_date DATE)
BEGIN
    DECLARE curr_date DATE;
    DECLARE curr_user INT;
    DECLARE check_in TIME;
    DECLARE check_out TIME;
    DECLARE v_status VARCHAR(20);
    DECLARE is_weekend INT;
    DECLARE random_val INT;

    SET curr_date = start_date;
    WHILE curr_date <= end_date DO
        SET curr_user = start_user_id;
        WHILE curr_user <= end_user_id DO
            -- 跳过周末
            SET is_weekend = DAYOFWEEK(curr_date) IN (1, 7);

            IF is_weekend = 0 THEN
                -- 随机生成考勤状态 (80%正常, 10%迟到, 5%早退, 5%请假/缺勤)
                SET random_val = FLOOR(RAND() * 100);

                IF random_val < 80 THEN
                    -- 正常: 08:50-09:05签到, 18:00-18:10签退
                    SET check_in = TIME(CONCAT('0', FLOOR(8 + RAND()*0.2), ':', LPAD(FLOOR(RAND()*60), 2, '0'), ':00'));
                    SET check_out = TIME(CONCAT('18:', LPAD(FLOOR(RAND()*10), 2, '0'), ':00'));
                    SET v_status = 'normal';
                ELSEIF random_val < 90 THEN
                    -- 迟到: 09:05-09:30签到
                    SET check_in = TIME(CONCAT('09:', LPAD(FLOOR(RAND()*25)+5, 2, '0'), ':00'));
                    SET check_out = TIME(CONCAT('18:', LPAD(FLOOR(RAND()*10), 2, '0'), ':00'));
                    SET v_status = 'late';
                ELSEIF random_val < 95 THEN
                    -- 早退: 正常签到, 17:30-17:59签退
                    SET check_in = TIME(CONCAT('0', FLOOR(8 + RAND()*0.2), ':', LPAD(FLOOR(RAND()*60), 2, '0'), ':00'));
                    SET check_out = TIME(CONCAT('17:', LPAD(FLOOR(RAND()*30), 2, '0'), ':00'));
                    SET v_status = 'early';
                ELSE
                    -- 缺勤/请假
                    SET check_in = NULL;
                    SET check_out = NULL;
                    SET v_status = 'absent';
                END IF;

                -- 插入考勤记录 (使用REPLACE避免重复)
                REPLACE INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id)
                VALUES (curr_date, check_in, check_out, v_status, NOW(), NOW(), curr_user);
            END IF;

            SET curr_user = curr_user + 1;
        END WHILE;
        SET curr_date = DATE_ADD(curr_date, INTERVAL 1 DAY);
    END WHILE;
END//

DELIMITER ;

-- 为现有员工生成考勤数据 (id 6-100, 排除已离职)
-- CALL generate_attendance_data(6, 100, '2025-07-01', '2026-01-24');

-- 手动插入代表性考勤数据以确保图表显示合理
-- 2025年7月
INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id) VALUES
('2025-07-01', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 6),
('2025-07-02', '08:52:00', '18:02:00', 'normal', NOW(), NOW(), 6),
('2025-07-03', '08:58:00', '18:08:00', 'normal', NOW(), NOW(), 6),
('2025-07-04', '09:15:00', '18:30:00', 'late', NOW(), NOW(), 6),
('2025-07-07', '08:50:00', '17:30:00', 'early', NOW(), NOW(), 6),
('2025-07-01', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 7),
('2025-07-02', '08:53:00', '18:03:00', 'normal', NOW(), NOW(), 7),
('2025-07-03', '09:10:00', '18:10:00', 'late', NOW(), NOW(), 7),
('2025-07-01', '08:56:00', '18:06:00', 'normal', NOW(), NOW(), 8),
('2025-07-02', '08:51:00', '18:01:00', 'normal', NOW(), NOW(), 8);

-- 2025年8月
INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id) VALUES
('2025-08-01', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 6),
('2025-08-04', '09:20:00', '18:20:00', 'late', NOW(), NOW(), 6),
('2025-08-05', '08:50:00', '17:45:00', 'early', NOW(), NOW(), 6),
('2025-08-06', NULL, NULL, 'absent', NOW(), NOW(), 6),
('2025-08-07', '08:52:00', '18:02:00', 'normal', NOW(), NOW(), 6),
('2025-08-01', '08:57:00', '18:07:00', 'normal', NOW(), NOW(), 7),
('2025-08-02', '09:05:00', '18:15:00', 'late', NOW(), NOW(), 7);

-- 2025年9月
INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id) VALUES
('2025-09-01', '08:54:00', '18:04:00', 'normal', NOW(), NOW(), 6),
('2025-09-02', '08:58:00', '18:08:00', 'normal', NOW(), NOW(), 6),
('2025-09-03', '09:12:00', '18:18:00', 'late', NOW(), NOW(), 6),
('2025-09-04', '08:55:00', '17:55:00', 'normal', NOW(), NOW(), 6),
('2025-09-05', '08:51:00', '18:01:00', 'normal', NOW(), NOW(), 6),
('2025-09-08', '09:08:00', '18:08:00', 'late', NOW(), NOW(), 6),
('2025-09-01', '08:56:00', '18:06:00', 'normal', NOW(), NOW(), 7),
('2025-09-02', '08:53:00', '18:03:00', 'normal', NOW(), NOW(), 7);

-- 2025年10月
INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id) VALUES
('2025-10-08', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 6),
('2025-10-09', '08:52:00', '18:02:00', 'normal', NOW(), NOW(), 6),
('2025-10-10', '09:15:00', '18:20:00', 'late', NOW(), NOW(), 6),
('2025-10-11', '08:50:00', '17:40:00', 'early', NOW(), NOW(), 6),
('2025-10-14', '08:58:00', '18:08:00', 'normal', NOW(), NOW(), 6),
('2025-10-15', '09:05:00', '18:10:00', 'late', NOW(), NOW(), 6),
('2025-10-08', '08:57:00', '18:07:00', 'normal', NOW(), NOW(), 7),
('2025-10-09', '08:54:00', '18:04:00', 'normal', NOW(), NOW(), 7);

-- 2025年11月
INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id) VALUES
('2025-11-03', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 6),
('2025-11-04', '08:51:00', '18:01:00', 'normal', NOW(), NOW(), 6),
('2025-11-05', '09:10:00', '18:15:00', 'late', NOW(), NOW(), 6),
('2025-11-06', '08:53:00', '18:03:00', 'normal', NOW(), NOW(), 6),
('2025-11-07', '08:56:00', '18:06:00', 'normal', NOW(), NOW(), 6),
('2025-11-10', '09:18:00', '18:25:00', 'late', NOW(), NOW(), 6),
('2025-11-11', '08:50:00', '17:50:00', 'normal', NOW(), NOW(), 6),
('2025-11-03', '08:58:00', '18:08:00', 'normal', NOW(), NOW(), 7),
('2025-11-04', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 7);

-- 2025年12月
INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id) VALUES
('2025-12-01', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 6),
('2025-12-02', '08:52:00', '18:02:00', 'normal', NOW(), NOW(), 6),
('2025-12-03', '09:08:00', '18:12:00', 'late', NOW(), NOW(), 6),
('2025-12-04', '08:54:00', '18:04:00', 'normal', NOW(), NOW(), 6),
('2025-12-05', '08:51:00', '18:01:00', 'normal', NOW(), NOW(), 6),
('2025-12-08', '09:12:00', '18:18:00', 'late', NOW(), NOW(), 6),
('2025-12-09', '08:56:00', '18:06:00', 'normal', NOW(), NOW(), 6),
('2025-12-10', '08:53:00', '18:03:00', 'normal', NOW(), NOW(), 6),
('2025-12-11', '09:05:00', '18:10:00', 'late', NOW(), NOW(), 6),
('2025-12-12', '08:50:00', '17:55:00', 'early', NOW(), NOW(), 6),
('2025-12-01', '08:57:00', '18:07:00', 'normal', NOW(), NOW(), 7),
('2025-12-02', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 7);

-- 2026年1月
INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id) VALUES
('2026-01-02', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 6),
('2026-01-03', '08:52:00', '18:02:00', 'normal', NOW(), NOW(), 6),
('2026-01-06', '09:10:00', '18:15:00', 'late', NOW(), NOW(), 6),
('2026-01-07', '08:54:00', '18:04:00', 'normal', NOW(), NOW(), 6),
('2026-01-08', '08:51:00', '18:01:00', 'normal', NOW(), NOW(), 6),
('2026-01-09', '09:15:00', '18:20:00', 'late', NOW(), NOW(), 6),
('2026-01-10', '08:56:00', '18:06:00', 'normal', NOW(), NOW(), 6),
('2026-01-13', '08:53:00', '18:03:00', 'normal', NOW(), NOW(), 6),
('2026-01-14', '09:05:00', '18:10:00', 'late', NOW(), NOW(), 6),
('2026-01-15', '08:50:00', '17:50:00', 'early', NOW(), NOW(), 6),
('2026-01-16', '08:58:00', '18:08:00', 'normal', NOW(), NOW(), 6),
('2026-01-17', NULL, NULL, 'absent', NOW(), NOW(), 6),
('2026-01-20', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 6),
('2026-01-21', '08:52:00', '18:02:00', 'normal', NOW(), NOW(), 6),
('2026-01-22', '09:08:00', '18:12:00', 'late', NOW(), NOW(), 6),
('2026-01-23', '08:54:00', '18:04:00', 'normal', NOW(), NOW(), 6),
('2026-01-24', '08:51:00', '18:01:00', 'normal', NOW(), NOW(), 6),
('2026-01-02', '08:57:00', '18:07:00', 'normal', NOW(), NOW(), 7),
('2026-01-03', '08:55:00', '18:05:00', 'normal', NOW(), NOW(), 7);

-- =====================================================
-- 5. 审批请求数据 (请假和加班)
-- =====================================================

-- 请假申请
INSERT INTO approval_approvalrequest (id, request_type, leave_type, start_time, end_time, reason, hours, status, approver_reason, created_at, updated_at, approver_id, user_id) VALUES
(6, 'leave', 'annual', '2025-07-15 09:00:00', '2025-07-16 18:00:00', '年假回家探亲', NULL, 'approved', '同意，请注意安全', NOW(), NOW(), 2, 6),
(7, 'leave', 'sick', '2025-08-20 09:00:00', '2025-08-21 18:00:00', '身体不适需要休息', NULL, 'approved', '批准，好好休息', NOW(), NOW(), 2, 7),
(8, 'leave', 'personal', '2025-09-10 09:00:00', '2025-09-12 18:00:00', '处理家庭事务', NULL, 'approved', '已批准', NOW(), NOW(), 2, 8),
(9, 'leave', 'annual', '2025-10-01 09:00:00', '2025-10-07 18:00:00', '国庆假期出游', NULL, 'approved', '国庆假期不用单独审批', NOW(), NOW(), 2, 6),
(10, 'leave', 'personal', '2025-11-15 09:00:00', '2025-11-15 18:00:00', '个人事务需要处理', NULL, 'approved', '批准', NOW(), NOW(), 2, 7),
(11, 'leave', 'sick', '2025-12-05 09:00:00', '2025-12-05 18:00:00', '感冒发烧', NULL, 'approved', '注意身体', NOW(), NOW(), 2, 6),
(12, 'leave', 'annual', '2025-12-30 09:00:00', '2026-01-02 18:00:00', '年末休假', NULL, 'pending', NULL, NOW(), NOW(), NULL, 8),
(13, 'leave', 'personal', '2026-01-20 09:00:00', '2026-01-21 18:00:00', '处理私人事务', NULL, 'pending', NULL, NOW(), NOW(), NULL, 6);

-- 加班申请
INSERT INTO approval_approvalrequest (id, request_type, leave_type, start_time, end_time, reason, hours, status, approver_reason, created_at, updated_at, approver_id, user_id) VALUES
(14, 'overtime', NULL, '2025-07-10 18:00:00', '2025-07-10 21:00:00', '项目上线需要', 3.0, 'approved', '项目紧急，批准加班', NOW(), NOW(), 2, 6),
(15, 'overtime', NULL, '2025-08-15 18:00:00', '2025-08-15 22:00:00', '功能开发赶进度', 4.0, 'approved', '批准', NOW(), NOW(), 2, 7),
(16, 'overtime', NULL, '2025-09-20 18:00:00', '2025-09-20 20:00:00', 'bug修复', 2.0, 'approved', '批准', NOW(), NOW(), 2, 8),
(17, 'overtime', NULL, '2025-10-15 18:00:00', '2025-10-15 23:00:00', '版本发布', 5.0, 'approved', '发布日加班正常', NOW(), NOW(), 2, 6),
(18, 'overtime', NULL, '2025-11-25 18:00:00', '2025-11-25 21:00:00', '需求开发', 3.0, 'approved', '批准', NOW(), NOW(), 2, 7),
(19, 'overtime', NULL, '2025-12-20 18:00:00', '2025-12-20 22:00:00', '年终总结开发', 4.0, 'approved', '批准', NOW(), NOW(), 2, 8),
(20, 'overtime', NULL, '2026-01-15 18:00:00', '2026-01-15 21:00:00', '新功能开发', 3.0, 'approved', '批准', NOW(), NOW(), 2, 6),
(21, 'overtime', NULL, '2026-01-20 18:00:00', '2026-01-20 20:00:00', '代码优化', 2.0, 'pending', NULL, NOW(), NOW(), NULL, 7);

-- =====================================================
-- 6. 薪资记录数据 (2025年7月至2026年1月)
-- 注意：salary_salaryrecord 表字段：month, base_salary, overtime_hours, overtime_pay,
--       late_count, early_count, attendance_deduction, final_salary, status, user_id
-- =====================================================

-- 2025年7月薪资
INSERT INTO salary_salaryrecord (id, month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id) VALUES
(101, '2025-07', 8500.00, 8.0, 400.00, 1, 0, 50.00, 8850.00, 'published', NOW(), NOW(), 2),
(102, '2025-07', 9000.00, 12.0, 600.00, 0, 0, 0.00, 9600.00, 'published', NOW(), NOW(), 3),
(103, '2025-07', 9500.00, 6.0, 300.00, 2, 0, 100.00, 9700.00, 'published', NOW(), NOW(), 4),
(104, '2025-07', 10000.00, 10.0, 500.00, 0, 0, 0.00, 10500.00, 'published', NOW(), NOW(), 6),
(105, '2025-07', 11000.00, 15.0, 750.00, 0, 1, 50.00, 11700.00, 'published', NOW(), NOW(), 10),
(106, '2025-07', 9000.00, 8.0, 400.00, 1, 0, 50.00, 9350.00, 'published', NOW(), NOW(), 7),
(107, '2025-07', 9500.00, 6.0, 300.00, 0, 0, 0.00, 9800.00, 'published', NOW(), NOW(), 8);

-- 2025年8月薪资
INSERT INTO salary_salaryrecord (id, month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id) VALUES
(108, '2025-08', 8500.00, 6.0, 300.00, 0, 0, 100.00, 8700.00, 'published', NOW(), NOW(), 2),
(109, '2025-08', 9000.00, 10.0, 500.00, 1, 0, 50.00, 9450.00, 'published', NOW(), NOW(), 3),
(110, '2025-08', 9500.00, 8.0, 400.00, 0, 0, 0.00, 9900.00, 'published', NOW(), NOW(), 4),
(111, '2025-08', 10000.00, 12.0, 600.00, 0, 0, 0.00, 10600.00, 'published', NOW(), NOW(), 6),
(112, '2025-08', 11000.00, 10.0, 500.00, 2, 0, 100.00, 11400.00, 'published', NOW(), NOW(), 10),
(113, '2025-08', 9000.00, 14.0, 700.00, 0, 0, 0.00, 9700.00, 'published', NOW(), NOW(), 7),
(114, '2025-08', 9500.00, 8.0, 400.00, 1, 0, 50.00, 9850.00, 'published', NOW(), NOW(), 8);

-- 2025年9月薪资
INSERT INTO salary_salaryrecord (id, month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id) VALUES
(115, '2025-09', 8500.00, 10.0, 500.00, 1, 0, 50.00, 8950.00, 'published', NOW(), NOW(), 2),
(116, '2025-09', 9000.00, 8.0, 400.00, 0, 0, 0.00, 9400.00, 'published', NOW(), NOW(), 3),
(117, '2025-09', 9500.00, 6.0, 300.00, 0, 0, 0.00, 9800.00, 'published', NOW(), NOW(), 4),
(118, '2025-09', 10000.00, 12.0, 600.00, 0, 0, 0.00, 10600.00, 'published', NOW(), NOW(), 6),
(119, '2025-09', 11000.00, 14.0, 700.00, 0, 0, 0.00, 11700.00, 'published', NOW(), NOW(), 10),
(120, '2025-09', 9000.00, 6.0, 300.00, 2, 0, 100.00, 9200.00, 'published', NOW(), NOW(), 7),
(121, '2025-09', 9500.00, 10.0, 500.00, 0, 1, 50.00, 9950.00, 'published', NOW(), NOW(), 8);

-- 2025年10月薪资
INSERT INTO salary_salaryrecord (id, month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id) VALUES
(122, '2025-10', 8500.00, 15.0, 750.00, 0, 0, 0.00, 9250.00, 'published', NOW(), NOW(), 2),
(123, '2025-10', 9000.00, 10.0, 500.00, 1, 0, 50.00, 9450.00, 'published', NOW(), NOW(), 3),
(124, '2025-10', 9500.00, 8.0, 400.00, 0, 1, 50.00, 9850.00, 'published', NOW(), NOW(), 4),
(125, '2025-10', 10000.00, 18.0, 900.00, 0, 0, 0.00, 10900.00, 'published', NOW(), NOW(), 6),
(126, '2025-10', 11000.00, 12.0, 600.00, 0, 0, 0.00, 11600.00, 'published', NOW(), NOW(), 10),
(127, '2025-10', 9000.00, 8.0, 400.00, 1, 0, 50.00, 9350.00, 'published', NOW(), NOW(), 7),
(128, '2025-10', 9500.00, 12.0, 600.00, 0, 0, 0.00, 10100.00, 'published', NOW(), NOW(), 8);

-- 2025年11月薪资
INSERT INTO salary_salaryrecord (id, month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id) VALUES
(129, '2025-11', 8500.00, 8.0, 400.00, 0, 0, 0.00, 8900.00, 'published', NOW(), NOW(), 2),
(130, '2025-11', 9000.00, 14.0, 700.00, 0, 0, 0.00, 9700.00, 'published', NOW(), NOW(), 3),
(131, '2025-11', 9500.00, 10.0, 500.00, 1, 0, 50.00, 9950.00, 'published', NOW(), NOW(), 4),
(132, '2025-11', 10000.00, 8.0, 400.00, 0, 0, 0.00, 10400.00, 'published', NOW(), NOW(), 6),
(133, '2025-11', 11000.00, 15.0, 750.00, 0, 0, 0.00, 11750.00, 'published', NOW(), NOW(), 10),
(134, '2025-11', 9000.00, 6.0, 300.00, 2, 0, 100.00, 9200.00, 'published', NOW(), NOW(), 7),
(135, '2025-11', 9500.00, 8.0, 400.00, 0, 0, 0.00, 9900.00, 'published', NOW(), NOW(), 8);

-- 2025年12月薪资
INSERT INTO salary_salaryrecord (id, month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id) VALUES
(136, '2025-12', 8500.00, 12.0, 600.00, 1, 0, 50.00, 9050.00, 'published', NOW(), NOW(), 2),
(137, '2025-12', 9000.00, 15.0, 750.00, 0, 0, 0.00, 9750.00, 'published', NOW(), NOW(), 3),
(138, '2025-12', 9500.00, 14.0, 700.00, 0, 0, 0.00, 10200.00, 'published', NOW(), NOW(), 4),
(139, '2025-12', 10000.00, 20.0, 1000.00, 0, 0, 0.00, 11000.00, 'published', NOW(), NOW(), 6),
(140, '2025-12', 11000.00, 18.0, 900.00, 0, 1, 50.00, 11850.00, 'published', NOW(), NOW(), 10),
(141, '2025-12', 9000.00, 10.0, 500.00, 0, 0, 0.00, 9500.00, 'published', NOW(), NOW(), 7),
(142, '2025-12', 9500.00, 12.0, 600.00, 1, 0, 50.00, 10050.00, 'published', NOW(), NOW(), 8);

-- 2026年1月薪资
INSERT INTO salary_salaryrecord (id, month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id) VALUES
(143, '2026-01', 8500.00, 8.0, 400.00, 0, 0, 0.00, 8900.00, 'draft', NOW(), NOW(), 2),
(144, '2026-01', 9000.00, 10.0, 500.00, 1, 0, 50.00, 9450.00, 'draft', NOW(), NOW(), 3),
(145, '2026-01', 9500.00, 8.0, 400.00, 0, 0, 0.00, 9900.00, 'draft', NOW(), NOW(), 4),
(146, '2026-01', 10000.00, 12.0, 600.00, 2, 0, 100.00, 10500.00, 'draft', NOW(), NOW(), 6),
(147, '2026-01', 11000.00, 14.0, 700.00, 0, 0, 0.00, 11700.00, 'draft', NOW(), NOW(), 10),
(148, '2026-01', 9000.00, 6.0, 300.00, 1, 0, 50.00, 9250.00, 'draft', NOW(), NOW(), 7),
(149, '2026-01', 9500.00, 10.0, 500.00, 0, 1, 50.00, 9950.00, 'draft', NOW(), NOW(), 8);

-- =====================================================
-- 7. 公告数据
-- =====================================================

INSERT INTO notice_notice (id, title, content, is_pinned, is_published, published_at, created_at, updated_at, published_by_id) VALUES
(2, '2025年第三季度全员大会通知', '全体员工请注意，2025年第三季度全员大会将于7月15日下午2点在公司大会议室召开，请准时参加。会议议程包括：Q2工作总结、Q3工作计划、优秀员工表彰等。', 1, 1, '2025-07-01 09:00:00', NOW(), NOW(), 2),
(3, '关于调整作息时间的通知', '为进一步提升工作效率，公司决定从2025年8月1日起调整工作时间。新的作息时间为：上午9:00-12:00，下午13:30-18:00。请各位同事知悉并相互转告。', 0, 1, '2025-07-20 10:00:00', NOW(), NOW(), 2),
(4, '2025年中秋节放假安排', '根据国家法定节假日规定，2025年中秋节放假时间为9月15日至9月17日，共3天。9月14日（周日）正常上班。请各位同事提前安排好工作。', 1, 1, '2025-09-01 08:00:00', NOW(), NOW(), 2),
(5, '关于开展2025年度员工体检的通知', '为保障员工身体健康，公司将于10月15日至10月30日组织年度体检。具体时间安排和注意事项将通过邮件发送，请留意查收。', 0, 1, '2025-09-25 14:00:00', NOW(), NOW(), 2),
(6, '2025年国庆节放假通知', '国庆节放假时间为10月1日至10月7日，共7天。9月28日（周日）和10月11日（周六）正常上班。祝大家节日快乐！', 1, 1, '2025-09-28 09:00:00', NOW(), NOW(), 2),
(7, '关于年终绩效考核的通知', '2025年度年终绩效考核将于12月1日正式启动，请各位员工提前准备年度工作总结和下年度工作计划。具体安排详见OA系统。', 0, 1, '2025-11-15 10:00:00', NOW(), NOW(), 2),
(8, '2026年元旦放假通知', '2026年元旦放假时间为1月1日（周三）放假1天。12月31日（周二）下午可提前下班。请合理安排出行。', 1, 1, '2025-12-20 09:00:00', NOW(), NOW(), 2),
(9, '关于春节假期安排的通知', '2026年春节放假时间为1月28日至2月6日，共10天。1月25日（周日）和2月8日（周日）正常上班。祝大家新年快乐！', 0, 1, '2025-12-25 14:00:00', NOW(), NOW(), 2),
(10, '公司年度盛典邀请函', '诚邀各位同事参加2026年1月20日举办的年度盛典，届时将颁发优秀员工奖、最佳团队奖等多项大奖，并设有抽奖环节。请着正装出席。', 0, 1, '2026-01-05 16:00:00', NOW(), NOW(), 2);

-- =====================================================
-- 8. 绩效评估数据
-- =====================================================

INSERT INTO performance_performancereview (id, review_period, score, strengths, improvements, goals, status, created_at, updated_at, employee_id, reviewer_id) VALUES
(6, '2025-Q3', 4.5, '工作认真负责，技术能力提升明显，能够独立完成分配的任务。积极主动参与团队协作。', '建议加强跨部门沟通能力，提高文档输出质量。', '继续深化技术学习，争取独立负责项目。', 'published', NOW(), NOW(), 6, 2),
(7, '2025-Q3', 4.0, '工作态度积极，团队协作良好，能够按时完成工作任务。', '工作效率有待提升，需要加强时间管理。', '提高工作效率，优化工作方法。', 'published', NOW(), NOW(), 7, 2),
(8, '2025-Q3', 4.8, '表现出色，超额完成季度目标，创新能力强，获得客户好评。', '注意劳逸结合，适当休息。', '带领团队完成更多高质量项目。', 'published', NOW(), NOW(), 8, 2),
(9, '2025-Q4', 4.2, 'Q4表现稳定，在项目攻坚阶段表现出色，技术问题处理及时。', '代码规范性和文档输出需要加强。', '提升代码质量意识。', 'published', NOW(), NOW(), 6, 2),
(10, '2025-Q4', 4.5, 'Q4工作表现优秀，积极主动解决技术难题，为团队做出重要贡献。', '继续保持，多分享经验给新同事。', '成为技术骨干，指导新人。', 'published', NOW(), NOW(), 7, 2),
(11, '2025-Q4', 4.0, '按时完成工作任务，与同事相处融洽。', '需要提高主动性，多承担挑战性工作。', '设定更高的工作目标。', 'published', NOW(), NOW(), 8, 2),
(12, '2025-年度', 4.3, '全年表现良好，工作稳定，技术能力持续提升。团队协作意识强。', '跨部门沟通能力有待加强，演讲表达能力需提升。', '争取明年成为技术负责人。', 'published', NOW(), NOW(), 6, 2),
(13, '2025-年度', 4.1, '全年工作态度端正，遵守公司制度，与同事相处良好。', '专业技能深度有待加强。', '深入学习专业知识，提升竞争力。', 'draft', NOW(), NOW(), 7, 2);

-- =====================================================
-- 9. 部门调整记录 (UserEditRequest示例)
-- =====================================================

INSERT INTO accounts_usereditrequest (id, edit_type, old_value, new_value, reason, status, reviewer_comment, created_at, updated_at, reviewer_id, user_id) VALUES
(4, 'department', '技术研发部', '产品部', '内部转岗', 'approved', '同意转岗申请', NOW(), NOW(), 2, 6),
(5, 'post', '初级开发工程师', '中级开发工程师', '职级晋升', 'approved', '晋升评审通过', NOW(), NOW(), 2, 7),
(6, 'salary_base', '9000.00', '10000.00', '年度调薪', 'approved', '符合调薪标准', NOW(), NOW(), 2, 8);

-- =====================================================
-- 10. 查看当前数据统计
-- =====================================================

-- 查询各部门在职人数
SELECT d.name AS 部门, COUNT(ep.id) AS 在职人数
FROM organization_department d
LEFT JOIN employee_employeeprofile ep ON d.id = ep.department_id AND ep.status = 'active'
GROUP BY d.id, d.name
ORDER BY d.sort_order;

-- 查询2025年下半年入职人数
SELECT
    DATE_FORMAT(ep.hire_date, '%Y-%m') AS 月份,
    COUNT(*) AS 入职人数
FROM employee_employeeprofile ep
WHERE ep.hire_date BETWEEN '2025-07-01' AND '2026-01-31'
GROUP BY DATE_FORMAT(ep.hire_date, '%Y-%m')
ORDER BY 月份;

-- 查询2025年下半年离职人数
SELECT
    DATE_FORMAT(ep.resigned_date, '%Y-%m') AS 月份,
    COUNT(*) AS 离职人数
FROM employee_employeeprofile ep
WHERE ep.status = 'resigned'
    AND ep.resigned_date BETWEEN '2025-07-01' AND '2026-01-31'
GROUP BY DATE_FORMAT(ep.resigned_date, '%Y-%m')
ORDER BY 月份;

-- 查询薪资趋势
SELECT
    month AS 月份,
    COUNT(*) AS 发放人数,
    SUM(final_salary) AS 薪资总额,
    ROUND(AVG(final_salary), 2) AS 平均薪资
FROM salary_salaryrecord
WHERE month BETWEEN '2025-07' AND '2026-01'
GROUP BY month
ORDER BY 月份;

-- 查询考勤异常统计
SELECT
    a.status AS 考勤状态,
    COUNT(*) AS 次数
FROM attendance_attendance a
WHERE a.date BETWEEN '2025-07-01' AND '2026-01-24'
GROUP BY a.status;

SELECT '完成! 测试数据已插入完毕。' AS 结果;
