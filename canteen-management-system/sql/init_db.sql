-- 食堂管理系统数据库初始化脚本
-- 生成日期: 2026-01-27

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `canteen_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `canteen_management`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- 1. 员工业务档案表
-- ----------------------------
DROP TABLE IF EXISTS `employee_profiles`;
CREATE TABLE `employee_profiles` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '档案ID',
    `name` VARCHAR(50) NOT NULL COMMENT '姓名',
    `gender` ENUM('MALE', 'FEMALE') DEFAULT 'MALE' COMMENT '性别',
    `phone` VARCHAR(20) NOT NULL COMMENT '联系方式',
    `id_card` VARCHAR(18) UNIQUE COMMENT '身份证号',
    `address` VARCHAR(255) COMMENT '家庭住址',
    `position` ENUM('CHEF', 'PASTRY', 'PREP', 'CLEANER', 'SERVER', 'MANAGER') NOT NULL COMMENT '岗位: 厨师/面点/切配/保洁/服务员/经理',
    `entry_date` DATE NOT NULL COMMENT '入职时间',
    `status` ENUM('ACTIVE', 'INACTIVE', 'LEAVE_WITHOUT_PAY') DEFAULT 'ACTIVE' COMMENT '在职状态: 在职/离职/停薪留职',
    `health_certificate_no` VARCHAR(50) COMMENT '健康证号',
    `health_certificate_expiry` DATE COMMENT '健康证有效期',
    `health_certificate_url` VARCHAR(255) COMMENT '健康证图片地址',
    `chef_certificate_level` VARCHAR(20) COMMENT '厨师等级证',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工业务档案表';

-- ----------------------------
-- 2. 系统用户账号表
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(50) UNIQUE NOT NULL COMMENT '登录账号',
    `password` VARCHAR(255) NOT NULL COMMENT '登录密码(开发阶段明文)',
    `employee_id` BIGINT COMMENT '关联员工档案ID',
    `role` ENUM('ADMIN', 'EMPLOYEE') DEFAULT 'EMPLOYEE' COMMENT '角色类型: 管理员/普通员工',
    `status` ENUM('ENABLED', 'DISABLED') DEFAULT 'ENABLED' COMMENT '账号状态: 启用/禁用',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`employee_id`) REFERENCES `employee_profiles`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统用户账号表';

-- ----------------------------
-- 3. 班次定义表
-- ----------------------------
DROP TABLE IF EXISTS `shifts`;
CREATE TABLE `shifts` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '班次ID',
    `name` VARCHAR(20) NOT NULL COMMENT '班次名称: 早班/中班/晚班/全天',
    `start_time` TIME NOT NULL COMMENT '上班开始时间',
    `end_time` TIME NOT NULL COMMENT '下班结束时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班次定义表';

-- ----------------------------
-- 4. 排班计划表
-- ----------------------------
DROP TABLE IF EXISTS `schedules`;
CREATE TABLE `schedules` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '排班ID',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `shift_id` BIGINT NOT NULL COMMENT '班次ID',
    `work_date` DATE NOT NULL COMMENT '排班日期',
    `is_swapped` TINYINT(1) DEFAULT 0 COMMENT '是否已调班',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`employee_id`) REFERENCES `employee_profiles`(`id`),
    FOREIGN KEY (`shift_id`) REFERENCES `shifts`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='排班计划表';

-- ----------------------------
-- 5. 调班申请表
-- ----------------------------
DROP TABLE IF EXISTS `shift_swap_requests`;
CREATE TABLE `shift_swap_requests` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '申请ID',
    `requester_id` BIGINT NOT NULL COMMENT '发起员工ID',
    `original_schedule_id` BIGINT NOT NULL COMMENT '原定排班ID',
    `target_date` DATE NOT NULL COMMENT '期望调整日期',
    `target_shift_id` BIGINT NOT NULL COMMENT '期望调整班次',
    `reason` TEXT COMMENT '申请原因',
    `status` ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING' COMMENT '审批状态',
    `approver_id` BIGINT COMMENT '审批管理员ID',
    `approval_remark` TEXT COMMENT '审批意见',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`requester_id`) REFERENCES `employee_profiles`(`id`),
    FOREIGN KEY (`original_schedule_id`) REFERENCES `schedules`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='调班申请表';

-- ----------------------------
-- 6. 考勤打卡记录表
-- ----------------------------
DROP TABLE IF EXISTS `attendance_records`;
CREATE TABLE `attendance_records` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '考勤ID',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `schedule_id` BIGINT COMMENT '关联排班ID',
    `clock_in_time` DATETIME COMMENT '签到时间',
    `clock_out_time` DATETIME COMMENT '签退时间',
    `clock_in_location` VARCHAR(100) COMMENT '签到地点',
    `clock_out_location` VARCHAR(100) COMMENT '签退地点',
    `status` ENUM('NORMAL', 'LATE', 'EARLY_LEAVE', 'MISSING', 'ABNORMAL') DEFAULT 'NORMAL' COMMENT '考勤状态',
    `correction_remark` TEXT COMMENT '管理员修正备注',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`employee_id`) REFERENCES `employee_profiles`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考勤记录表';

-- ----------------------------
-- 7. 请假审批表
-- ----------------------------
DROP TABLE IF EXISTS `leave_requests`;
CREATE TABLE `leave_requests` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '请假ID',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `leave_type` ENUM('SICK', 'PERSONAL', 'COMPENSATORY') NOT NULL COMMENT '请假类型: 病假/事假/调休',
    `start_time` DATETIME NOT NULL COMMENT '开始时间',
    `end_time` DATETIME NOT NULL COMMENT '结束时间',
    `reason` TEXT COMMENT '请假原因',
    `status` ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING' COMMENT '审批状态',
    `approver_id` BIGINT COMMENT '审批人ID',
    `approval_remark` TEXT COMMENT '审批意见',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`employee_id`) REFERENCES `employee_profiles`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='请假审批表';

-- ----------------------------
-- 8. 薪资记录表
-- ----------------------------
DROP TABLE IF EXISTS `salary_records`;
CREATE TABLE `salary_records` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '薪资记录ID',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `year_month` VARCHAR(7) NOT NULL COMMENT '薪资月份 (YYYY-MM)',
    `base_salary` DECIMAL(10, 2) NOT NULL COMMENT '基本工资',
    `position_allowance` DECIMAL(10, 2) DEFAULT 0.00 COMMENT '岗位津贴',
    `overtime_pay` DECIMAL(10, 2) DEFAULT 0.00 COMMENT '加班费',
    `deductions` DECIMAL(10, 2) DEFAULT 0.00 COMMENT '扣款(迟到/缺卡等)',
    `total_salary` DECIMAL(10, 2) NOT NULL COMMENT '实发工资',
    `status` ENUM('GENERATED', 'PAID', 'DISPUTE') DEFAULT 'GENERATED' COMMENT '状态: 已生成/已发放/有异议',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`employee_id`) REFERENCES `employee_profiles`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='薪资记录表';

-- ----------------------------
-- 9. 异常申诉表
-- ----------------------------
DROP TABLE IF EXISTS `appeals`;
CREATE TABLE `appeals` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '申诉ID',
    `type` ENUM('ATTENDANCE', 'SALARY') NOT NULL COMMENT '申诉类型',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `target_id` BIGINT NOT NULL COMMENT '关联记录ID(考勤或薪资表ID)',
    `reason` TEXT NOT NULL COMMENT '申诉理由',
    `status` ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING' COMMENT '审批状态',
    `approver_id` BIGINT COMMENT '审批管理员ID',
    `approval_remark` TEXT COMMENT '审批意见',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`employee_id`) REFERENCES `employee_profiles`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='异常申诉表';

-- ----------------------------
-- 插入测试数据
-- ----------------------------

-- 1. 员工业务档案
INSERT INTO `employee_profiles` (`name`, `gender`, `phone`, `id_card`, `address`, `position`, `entry_date`, `status`, `health_certificate_no`, `health_certificate_expiry`, `chef_certificate_level`) VALUES
('张大厨', 'MALE', '13800138001', '110101198001011234', '北京市朝阳区幸福路1号', 'CHEF', '2023-01-01', 'ACTIVE', 'H12345678', '2026-12-31', '高级厨师'),
('李面点', 'FEMALE', '13800138002', '110101198505052345', '北京市海淀区中关村', 'PASTRY', '2023-02-15', 'ACTIVE', 'H23456789', '2026-06-30', '中级面点师'),
('王保洁', 'FEMALE', '13800138003', '110101197510103456', '北京市丰台区南苑', 'CLEANER', '2023-03-10', 'ACTIVE', 'H34567890', '2026-03-10', NULL),
('赵切配', 'MALE', '13800138004', '110101199012124567', '北京市昌平区回龙观', 'PREP', '2023-05-20', 'ACTIVE', 'H45678901', '2026-05-20', NULL),
('孙服务', 'FEMALE', '13800138005', '110101199508085678', '北京市通州区北苑', 'SERVER', '2023-06-01', 'ACTIVE', 'H56789012', '2026-06-01', NULL),
('钱店长', 'MALE', '13800138006', '110101198203036789', '北京市西城区月坛', 'MANAGER', '2022-10-01', 'ACTIVE', 'H67890123', '2026-10-01', '餐饮管理一级'),
('周小厨', 'MALE', '13800138007', '110101199207077890', '北京市顺义区后沙峪', 'CHEF', '2023-08-15', 'ACTIVE', 'H78901234', '2026-08-15', '初级厨师'),
('吴保洁', 'FEMALE', '13800138008', '110101197211118901', '北京市大兴区黄村', 'CLEANER', '2023-09-01', 'ACTIVE', 'H89012345', '2026-09-01', NULL),
('郑切配', 'MALE', '13800138009', '110101198804049012', '北京市房山区良乡', 'PREP', '2023-11-01', 'ACTIVE', 'H90123456', '2026-11-01', NULL),
('冯面点', 'FEMALE', '13800138010', '110101198402020123', '北京市平谷区', 'PASTRY', '2024-01-01', 'ACTIVE', 'H01234567', '2027-01-01', '高级面点师');

-- 2. 系统用户账号
INSERT INTO `users` (`username`, `password`, `employee_id`, `role`, `status`) VALUES
('admin', 'admin123', 6, 'ADMIN', 'ENABLED'),
('zhangdachu', '123456', 1, 'EMPLOYEE', 'ENABLED'),
('limiandian', '123456', 2, 'EMPLOYEE', 'ENABLED'),
('zhaoqiepei', '123456', 4, 'EMPLOYEE', 'ENABLED'),
('sunfuwu', '123456', 5, 'EMPLOYEE', 'ENABLED'),
('zhouxiaochu', '123456', 7, 'EMPLOYEE', 'ENABLED'),
('zhengqiepei', '123456', 9, 'EMPLOYEE', 'ENABLED'),
('fengmiandian', '123456', 10, 'EMPLOYEE', 'ENABLED'),
('test_user1', '123456', NULL, 'EMPLOYEE', 'ENABLED'),
('test_user2', '123456', NULL, 'EMPLOYEE', 'DISABLED');

-- 3. 班次定义
INSERT INTO `shifts` (`name`, `start_time`, `end_time`) VALUES
('早餐班', '05:30:00', '10:00:00'),
('中餐班', '10:00:00', '14:30:00'),
('晚餐班', '16:00:00', '20:30:00'),
('全天班', '08:00:00', '20:00:00'),
('早中连班', '05:30:00', '14:30:00'),
('中晚连班', '10:00:00', '20:30:00'),
('夜宵班', '20:30:00', '00:30:00'),
('行政班', '09:00:00', '18:00:00'),
('保洁早班', '06:00:00', '11:00:00'),
('保洁晚班', '14:00:00', '19:00:00');

-- 4. 排班计划
INSERT INTO `schedules` (`employee_id`, `shift_id`, `work_date`) VALUES
(1, 1, '2026-01-27'), (2, 1, '2026-01-27'), (3, 9, '2026-01-27'),
(4, 2, '2026-01-27'), (5, 2, '2026-01-27'), (1, 1, '2026-01-28'),
(2, 5, '2026-01-28'), (3, 9, '2026-01-28'), (4, 2, '2026-01-28'),
(5, 6, '2026-01-28');

-- 5. 调班申请
INSERT INTO `shift_swap_requests` (`requester_id`, `original_schedule_id`, `target_date`, `target_shift_id`, `reason`, `status`) VALUES
(1, 1, '2026-01-29', 2, '家里有急事，想换到中餐班', 'PENDING'),
(2, 2, '2026-01-27', 3, '身体不适，早餐班起不来', 'APPROVED'),
(4, 4, '2026-01-30', 4, '需要全天值班补工时', 'REJECTED'),
(5, 5, '2026-01-28', 1, '调班申请测试1', 'PENDING'),
(1, 6, '2026-01-31', 3, '调班申请测试2', 'PENDING'),
(2, 7, '2026-01-29', 1, '调班申请测试3', 'APPROVED'),
(3, 3, '2026-01-27', 10, '调班申请测试4', 'PENDING'),
(4, 9, '2026-02-01', 2, '调班申请测试5', 'REJECTED'),
(5, 10, '2026-01-29', 6, '调班申请测试6', 'PENDING'),
(1, 1, '2026-01-30', 5, '调班申请测试7', 'PENDING');

-- 6. 考勤打卡记录
INSERT INTO `attendance_records` (`employee_id`, `schedule_id`, `clock_in_time`, `clock_out_time`, `status`) VALUES
(1, 1, '2026-01-27 05:25:00', '2026-01-27 10:05:00', 'NORMAL'),
(2, 1, '2026-01-27 05:40:00', '2026-01-27 10:02:00', 'LATE'),
(3, 3, '2026-01-27 05:55:00', '2026-01-27 11:10:00', 'NORMAL'),
(4, 4, '2026-01-27 10:00:00', NULL, 'MISSING'),
(5, 5, '2026-01-27 10:15:00', '2026-01-27 14:35:00', 'LATE'),
(1, 6, '2026-01-28 05:28:00', '2026-01-28 10:00:00', 'NORMAL'),
(2, 7, '2026-01-28 05:30:00', '2026-01-28 14:35:00', 'NORMAL'),
(3, 8, '2026-01-28 06:05:00', '2026-01-28 11:05:00', 'LATE'),
(4, 9, '2026-01-28 10:00:00', '2026-01-28 14:20:00', 'EARLY_LEAVE'),
(5, 10, '2026-01-28 10:00:00', '2026-01-28 20:35:00', 'NORMAL');

-- 7. 请假审批
INSERT INTO `leave_requests` (`employee_id`, `leave_type`, `start_time`, `end_time`, `reason`, `status`) VALUES
(1, 'SICK', '2026-01-20 08:00:00', '2026-01-20 18:00:00', '感冒发烧', 'APPROVED'),
(2, 'PERSONAL', '2026-01-21 10:00:00', '2026-01-21 14:00:00', '家里办证', 'APPROVED'),
(3, 'COMPENSATORY', '2026-01-22 08:00:00', '2026-01-22 18:00:00', '加班调休', 'REJECTED'),
(4, 'SICK', '2026-01-25 08:00:00', '2026-01-26 18:00:00', '肠胃炎', 'PENDING'),
(5, 'PERSONAL', '2026-01-30 08:00:00', '2026-01-30 18:00:00', '回老家', 'PENDING'),
(6, 'PERSONAL', '2026-02-01 08:00:00', '2026-02-01 18:00:00', '请假测试1', 'PENDING'),
(7, 'SICK', '2026-02-02 08:00:00', '2026-02-02 18:00:00', '请假测试2', 'APPROVED'),
(8, 'COMPENSATORY', '2026-02-03 08:00:00', '2026-02-03 18:00:00', '请假测试3', 'REJECTED'),
(9, 'PERSONAL', '2026-02-04 08:00:00', '2026-02-04 18:00:00', '请假测试4', 'PENDING'),
(10, 'SICK', '2026-02-05 08:00:00', '2026-02-05 18:00:00', '请假测试5', 'APPROVED');

-- 8. 薪资记录
INSERT INTO `salary_records` (`employee_id`, `year_month`, `base_salary`, `position_allowance`, `overtime_pay`, `deductions`, `total_salary`, `status`) VALUES
(1, '2025-12', 6000.00, 1000.00, 500.00, 50.00, 7450.00, 'PAID'),
(2, '2025-12', 5500.00, 800.00, 300.00, 0.00, 6600.00, 'PAID'),
(3, '2025-12', 3500.00, 200.00, 200.00, 20.00, 3880.00, 'PAID'),
(4, '2025-12', 4500.00, 500.00, 400.00, 100.00, 5300.00, 'DISPUTE'),
(5, '2025-12', 4000.00, 300.00, 100.00, 0.00, 4400.00, 'PAID'),
(6, '2025-12', 8000.00, 2000.00, 0.00, 0.00, 10000.00, 'PAID'),
(7, '2025-12', 5000.00, 600.00, 200.00, 30.00, 5770.00, 'GENERATED'),
(8, '2025-12', 3500.00, 200.00, 150.00, 0.00, 3850.00, 'GENERATED'),
(9, '2025-12', 4500.00, 500.00, 300.00, 50.00, 5250.00, 'GENERATED'),
(10, '2025-12', 5500.00, 800.00, 400.00, 0.00, 6700.00, 'GENERATED');

-- 9. 异常申诉
INSERT INTO `appeals` (`type`, `employee_id`, `target_id`, `reason`, `status`) VALUES
('ATTENDANCE', 4, 4, '打卡机坏了，实际已按时签退', 'PENDING'),
('SALARY', 4, 4, '12月加班费算少了，多加了2小时', 'PENDING'),
('ATTENDANCE', 2, 2, '迟到是因为食堂门口卸货堵住了', 'APPROVED'),
('ATTENDANCE', 5, 5, '申诉测试1', 'REJECTED'),
('SALARY', 1, 1, '申诉测试2', 'PENDING'),
('ATTENDANCE', 7, 7, '申诉测试3', 'APPROVED'),
('SALARY', 9, 9, '申诉测试4', 'PENDING'),
('ATTENDANCE', 10, 10, '申诉测试5', 'REJECTED'),
('ATTENDANCE', 3, 3, '申诉测试6', 'PENDING'),
('SALARY', 2, 2, '申诉测试7', 'PENDING');

SET FOREIGN_KEY_CHECKS = 1;
