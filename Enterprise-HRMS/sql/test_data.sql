-- HRMS 测试数据插入脚本
-- 生成时间: 2026-01-24
-- 测试密码: Test123456.
-- 密码哈希: pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 清空所有表数据（按外键约束顺序）
-- ============================================
TRUNCATE TABLE salary_salaryrecord;
TRUNCATE TABLE attendance_attendance;
TRUNCATE TABLE employee_employeeprofile;
TRUNCATE TABLE accounts_user;
TRUNCATE TABLE organization_post;
TRUNCATE TABLE organization_department;

-- 重置自增ID
ALTER TABLE organization_department AUTO_INCREMENT = 1;
ALTER TABLE organization_post AUTO_INCREMENT = 1;
ALTER TABLE accounts_user AUTO_INCREMENT = 1;
ALTER TABLE employee_employeeprofile AUTO_INCREMENT = 1;
ALTER TABLE attendance_attendance AUTO_INCREMENT = 1;
ALTER TABLE salary_salaryrecord AUTO_INCREMENT = 1;

-- ============================================
-- 1. 部门表 (organization_department) - 10条
-- ============================================
INSERT INTO `organization_department` (`id`, `name`, `code`, `sort_order`, `is_active`, `created_at`, `updated_at`, `parent_id`) VALUES
(1, '技术研发部', 'TECH', 1, 1, NOW(), NOW(), NULL),
(2, '产品部', 'PRD', 2, 1, NOW(), NOW(), NULL),
(3, '市场部', 'MKT', 3, 1, NOW(), NOW(), NULL),
(4, '人力资源部', 'HR', 4, 1, NOW(), NOW(), NULL),
(5, '财务部', 'FIN', 5, 1, NOW(), NOW(), NULL),
(6, '运营部', 'OPS', 6, 1, NOW(), NOW(), NULL),
(7, '设计部', 'DES', 7, 1, NOW(), NOW(), NULL),
(8, '客服部', 'CS', 8, 1, NOW(), NOW(), NULL),
(9, '行政部', 'ADM', 9, 1, NOW(), NOW(), NULL),
(10, '法务部', 'LEG', 10, 1, NOW(), NOW(), NULL);

-- ============================================
-- 2. 岗位表 (organization_post) - 10条
-- ============================================
INSERT INTO `organization_post` (`id`, `name`, `code`, `description`, `sort_order`, `is_active`, `created_at`, `updated_at`) VALUES
(1, '初级开发工程师', 'JDEV', '负责基础开发工作，使用公司技术栈完成功能开发', 1, 1, NOW(), NOW()),
(2, '中级开发工程师', 'MDEV', '承担核心模块开发，指导初级工程师', 2, 1, NOW(), NOW()),
(3, '高级开发工程师', 'SDEV', '负责技术架构设计，攻克技术难题', 3, 1, NOW(), NOW()),
(4, '技术总监', 'TD', '技术团队管理，技术战略规划', 4, 1, NOW(), NOW()),
(5, '产品经理', 'PM', '产品规划，需求分析，项目管理', 5, 1, NOW(), NOW()),
(6, 'UI/UX设计师', 'UI', '界面设计，用户体验优化', 6, 1, NOW(), NOW()),
(7, '人事专员', 'HRSP', '招聘，员工关系，薪酬福利', 7, 1, NOW(), NOW()),
(8, '财务专员', 'FASP', '账务处理，财务报表，税务申报', 8, 1, NOW(), NOW()),
(9, '运营专员', 'OPSP', '日常运营，数据分析，活动策划', 9, 1, NOW(), NOW()),
(10, '客户成功经理', 'CSM', '客户服务，客户满意度维护', 10, 1, NOW(), NOW());

-- ============================================
-- 3. 用户表 (accounts_user) - 100条
-- 角色: 1 Admin + 3 HR + 96 Employee
-- ============================================
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
-- 管理员
(1, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 1, 'admin', '', '', 1, 1, '2024-01-01 00:00:00', '13800000001', 'admin', '系统管理员', 'admin@hrms.com'),
-- 人事专员 (3人)
(2, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'hr001', '', '', 1, 1, '2024-01-15 00:00:00', '13800000002', 'hr', '张人事', 'hr001@hrms.com'),
(3, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'hr002', '', '', 1, 1, '2024-02-01 00:00:00', '13800000003', 'hr', '李人事', 'hr002@hrms.com'),
(4, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'hr003', '', '', 1, 1, '2024-03-01 00:00:00', '13800000004', 'hr', '王人事', 'hr003@hrms.com');

-- 技术研发部 (20人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(5, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0001', '', '', 0, 1, '2024-01-10 00:00:00', '13800000005', 'employee', '张伟', 'zhangwei@hrms.com'),
(6, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0002', '', '', 0, 1, '2024-01-15 00:00:00', '13800000006', 'employee', '李娜', 'lina@hrms.com'),
(7, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0003', '', '', 0, 1, '2024-02-01 00:00:00', '13800000007', 'employee', '王强', 'wangqiang@hrms.com'),
(8, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0004', '', '', 0, 1, '2024-02-10 00:00:00', '13800000008', 'employee', '刘洋', 'liuyang@hrms.com'),
(9, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0005', '', '', 0, 1, '2024-02-20 00:00:00', '13800000009', 'employee', '陈静', 'chenjing@hrms.com'),
(10, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0006', '', '', 0, 1, '2024-03-01 00:00:00', '13800000010', 'employee', '赵磊', 'zhaolei@hrms.com'),
(11, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0007', '', '', 0, 1, '2024-03-05 00:00:00', '13800000011', 'employee', '吴敏', 'wumin@hrms.com'),
(12, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0008', '', '', 0, 1, '2024-03-10 00:00:00', '13800000012', 'employee', '周杰', 'zhoujie@hrms.com'),
(13, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0009', '', '', 0, 1, '2024-03-15 00:00:00', '13800000013', 'employee', '徐丽', 'xuli@hrms.com'),
(14, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0010', '', '', 0, 1, '2024-03-20 00:00:00', '13800000014', 'employee', '孙鹏', 'sunpeng@hrms.com'),
(15, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0011', '', '', 0, 1, '2024-04-01 00:00:00', '13800000015', 'employee', '马艳', 'mayan@hrms.com'),
(16, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0012', '', '', 0, 1, '2024-04-05 00:00:00', '13800000016', 'employee', '朱浩', 'zhuhao@hrms.com'),
(17, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0013', '', '', 0, 1, '2024-04-10 00:00:00', '13800000017', 'employee', '胡芳', 'hufang@hrms.com'),
(18, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0014', '', '', 0, 1, '2024-04-15 00:00:00', '13800000018', 'employee', '林宇', 'linyu@hrms.com'),
(19, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0015', '', '', 0, 1, '2024-04-20 00:00:00', '13800000019', 'employee', '韩梅', 'hanmei@hrms.com'),
(20, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0016', '', '', 0, 1, '2024-05-01 00:00:00', '13800000020', 'employee', '高健', 'gaojian@hrms.com'),
(21, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0017', '', '', 0, 1, '2024-05-05 00:00:00', '13800000021', 'employee', '谢婷', 'xieting@hrms.com'),
(22, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0018', '', '', 0, 1, '2024-05-10 00:00:00', '13800000022', 'employee', '唐伟', 'tangwei@hrms.com'),
(23, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0019', '', '', 0, 1, '2024-05-15 00:00:00', '13800000023', 'employee', '董雪', 'dongxue@hrms.com'),
(24, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0020', '', '', 0, 1, '2024-05-20 00:00:00', '13800000024', 'employee', '冯涛', 'fengtao@hrms.com');

-- 产品部 (10人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(25, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0021', '', '', 0, 1, '2024-01-20 00:00:00', '13800000025', 'employee', '曹鹏', 'caopeng@hrms.com'),
(26, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0022', '', '', 0, 1, '2024-02-15 00:00:00', '13800000026', 'employee', '邓琴', 'dengqin@hrms.com'),
(27, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0023', '', '', 0, 1, '2024-03-01 00:00:00', '13800000027', 'employee', '苏磊', 'sulei@hrms.com'),
(28, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0024', '', '', 0, 1, '2024-03-20 00:00:00', '13800000028', 'employee', '杨帆', 'yangfan@hrms.com'),
(29, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0025', '', '', 0, 1, '2024-04-01 00:00:00', '13800000029', 'employee', '于慧', 'yuhui@hrms.com'),
(30, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0026', '', '', 0, 1, '2024-04-15 00:00:00', '13800000030', 'employee', '何刚', 'hegang@hrms.com'),
(31, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0027', '', '', 0, 1, '2024-05-01 00:00:00', '13800000031', 'employee', '吕娜', 'lvna@hrms.com'),
(32, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0028', '', '', 0, 1, '2024-05-10 00:00:00', '13800000032', 'employee', '潘明', 'panming@hrms.com'),
(33, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0029', '', '', 0, 1, '2024-05-20 00:00:00', '13800000033', 'employee', '罗娟', 'luojuan@hrms.com'),
(34, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0030', '', '', 0, 1, '2024-06-01 00:00:00', '13800000034', 'employee', '肖鹏', 'xiaopeng@hrms.com');

-- 市场部 (10人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(35, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0031', '', '', 0, 1, '2024-01-25 00:00:00', '13800000035', 'employee', '梁伟', 'liangwei@hrms.com'),
(36, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0032', '', '', 0, 1, '2024-02-20 00:00:00', '13800000036', 'employee', '田莉', 'tianli@hrms.com'),
(37, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0033', '', '', 0, 1, '2024-03-10 00:00:00', '13800000037', 'employee', '蒋明', 'jiangming@hrms.com'),
(38, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0034', '', '', 0, 1, '2024-03-25 00:00:00', '13800000038', 'employee', '雷艳', 'leiyan@hrms.com'),
(39, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0035', '', '', 0, 1, '2024-04-05 00:00:00', '13800000039', 'employee', '段强', 'duanqiang@hrms.com'),
(40, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0036', '', '', 0, 1, '2024-04-20 00:00:00', '13800000040', 'employee', '武娜', 'wuna@hrms.com'),
(41, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0037', '', '', 0, 1, '2024-05-05 00:00:00', '13800000041', 'employee', '贺鹏', 'hepeng@hrms.com'),
(42, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0038', '', '', 0, 1, '2024-05-15 00:00:00', '13800000042', 'employee', '康芳', 'kangfang@hrms.com'),
(43, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0039', '', '', 0, 1, '2024-06-01 00:00:00', '13800000043', 'employee', '姚磊', 'yaolei@hrms.com'),
(44, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0040', '', '', 0, 1, '2024-06-10 00:00:00', '13800000044', 'employee', '姜莉', 'jiangli@hrms.com');

-- 人力资源部 (5人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(45, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0041', '', '', 0, 1, '2024-02-01 00:00:00', '13800000045', 'employee', '范明', 'fanming@hrms.com'),
(46, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0042', '', '', 0, 1, '2024-03-01 00:00:00', '13800000046', 'employee', '丁倩', 'dingqian@hrms.com'),
(47, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0043', '', '', 0, 1, '2024-04-01 00:00:00', '13800000047', 'employee', '魏强', 'weiqiang@hrms.com'),
(48, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0044', '', '', 0, 1, '2024-05-01 00:00:00', '13800000048', 'employee', '秦艳', 'qinyan@hrms.com'),
(49, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0045', '', '', 0, 1, '2024-06-01 00:00:00', '13800000049', 'employee', '彭鹏', 'pengpeng@hrms.com');

-- 财务部 (8人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(50, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0046', '', '', 0, 1, '2024-01-10 00:00:00', '13800000050', 'employee', '邵杰', 'shaojie@hrms.com'),
(51, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0047', '', '', 0, 1, '2024-02-15 00:00:00', '13800000051', 'employee', '阎丽', 'yanli@hrms.com'),
(52, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0048', '', '', 0, 1, '2024-03-01 00:00:00', '13800000052', 'employee', '薛磊', 'xuelei@hrms.com'),
(53, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0049', '', '', 0, 1, '2024-03-20 00:00:00', '13800000053', 'employee', '余娜', 'yuna@hrms.com'),
(54, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0050', '', '', 0, 1, '2024-04-05 00:00:00', '13800000054', 'employee', '郝鹏', 'haopeng@hrms.com'),
(55, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0051', '', '', 0, 1, '2024-04-20 00:00:00', '13800000055', 'employee', '侯芳', 'houfang@hrms.com'),
(56, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0052', '', '', 0, 1, '2024-05-05 00:00:00', '13800000056', 'employee', '毛强', 'maoqiang@hrms.com'),
(57, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0053', '', '', 0, 1, '2024-05-20 00:00:00', '13800000057', 'employee', '郭倩', 'guoqian@hrms.com');

-- 运营部 (10人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(58, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0054', '', '', 0, 1, '2024-01-20 00:00:00', '13800000058', 'employee', '戴伟', 'daiwei@hrms.com'),
(59, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0055', '', '', 0, 1, '2024-02-10 00:00:00', '13800000059', 'employee', '任莉', 'renli@hrms.com'),
(60, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0056', '', '', 0, 1, '2024-02-28 00:00:00', '13800000060', 'employee', '袁明', 'yuanming@hrms.com'),
(61, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0057', '', '', 0, 1, '2024-03-15 00:00:00', '13800000061', 'employee', '金艳', 'jinyan@hrms.com'),
(62, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0058', '', '', 0, 1, '2024-04-01 00:00:00', '13800000062', 'employee', '戚强', 'qiqiang@hrms.com'),
(63, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0059', '', '', 0, 1, '2024-04-15 00:00:00', '13800000063', 'employee', '谢娜', 'xiena@hrms.com'),
(64, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0060', '', '', 0, 1, '2024-04-30 00:00:00', '13800000064', 'employee', '喻鹏', 'yupeng@hrms.com'),
(65, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0061', '', '', 0, 1, '2024-05-10 00:00:00', '13800000065', 'employee', '柏芳', 'baifang@hrms.com'),
(66, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0062', '', '', 0, 1, '2024-05-25 00:00:00', '13800000066', 'employee', '丛强', 'congqiang@hrms.com'),
(67, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0063', '', '', 0, 1, '2024-06-05 00:00:00', '13800000067', 'employee', '赖倩', 'laiqian@hrms.com');

-- 设计部 (8人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(68, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0064', '', '', 0, 1, '2024-02-01 00:00:00', '13800000068', 'employee', '葛伟', 'gewei@hrms.com'),
(69, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0065', '', '', 0, 1, '2024-02-20 00:00:00', '13800000069', 'employee', '瞿莉', 'quli@hrms.com'),
(70, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0066', '', '', 0, 1, '2024-03-10 00:00:00', '13800000070', 'employee', '童明', 'tongming@hrms.com'),
(71, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0067', '', '', 0, 1, '2024-03-25 00:00:00', '13800000071', 'employee', '向艳', 'xiangyan@hrms.com'),
(72, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0068', '', '', 0, 1, '2024-04-10 00:00:00', '13800000072', 'employee', '卜强', 'buqiang@hrms.com'),
(73, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0069', '', '', 0, 1, '2024-04-25 00:00:00', '13800000073', 'employee', '燕娜', 'yanna@hrms.com'),
(74, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0070', '', '', 0, 1, '2024-05-05 00:00:00', '13800000074', 'employee', '门鹏', 'menpeng@hrms.com'),
(75, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0071', '', '', 0, 1, '2024-05-20 00:00:00', '13800000075', 'employee', '农芳', 'nongfang@hrms.com');

-- 客服部 (8人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(76, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0072', '', '', 0, 1, '2024-01-15 00:00:00', '13800000076', 'employee', '苍伟', 'cangwei@hrms.com'),
(77, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0073', '', '', 0, 1, '2024-02-01 00:00:00', '13800000077', 'employee', '樊莉', 'fanli@hrms.com'),
(78, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0074', '', '', 0, 1, '2024-02-20 00:00:00', '13800000078', 'employee', '利明', 'liming@hrms.com'),
(79, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0075', '', '', 0, 1, '2024-03-10 00:00:00', '13800000079', 'employee', '贵艳', 'guiyan@hrms.com'),
(80, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0076', '', '', 0, 1, '2024-03-25 00:00:00', '13800000080', 'employee', '农强', 'nongqiang@hrms.com'),
(81, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0077', '', '', 0, 1, '2024-04-05 00:00:00', '13800000081', 'employee', '凡娜', 'fanna@hrms.com'),
(82, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0078', '', '', 0, 1, '2024-04-20 00:00:00', '13800000082', 'employee', '黎鹏', 'lipeng@hrms.com'),
(83, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0079', '', '', 0, 1, '2024-05-05 00:00:00', '13800000083', 'employee', '苗芳', 'miaofang@hrms.com');

-- 行政部 (5人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(84, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0080', '', '', 0, 1, '2024-01-20 00:00:00', '13800000084', 'employee', '禹伟', 'yuwei@hrms.com'),
(85, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0081', '', '', 0, 1, '2024-02-15 00:00:00', '13800000085', 'employee', '巴莉', 'bali@hrms.com'),
(86, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0082', '', '', 0, 1, '2024-03-01 00:00:00', '13800000086', 'employee', '蒙明', 'mengming@hrms.com'),
(87, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0083', '', '', 0, 1, '2024-03-20 00:00:00', '13800000087', 'employee', '泉艳', 'quanyan@hrms.com'),
(88, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0084', '', '', 0, 1, '2024-04-10 00:00:00', '13800000088', 'employee', '敬强', 'jingqiang@hrms.com');

-- 法务部 (2人)
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(89, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0085', '', '', 0, 1, '2024-02-01 00:00:00', '13800000089', 'employee', '湛伟', 'zhanwei@hrms.com'),
(90, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0086', '', '', 0, 1, '2024-03-01 00:00:00', '13800000090', 'employee', '晏莉', 'yanli2@hrms.com');

-- 补充剩余10人
INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `phone`, `role`, `real_name`, `email`) VALUES
(91, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0087', '', '', 0, 1, '2024-06-01 00:00:00', '13800000091', 'employee', '巩伟', 'gongwei@hrms.com'),
(92, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0088', '', '', 0, 1, '2024-06-05 00:00:00', '13800000092', 'employee', '仲莉', 'zhongli@hrms.com'),
(93, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0089', '', '', 0, 1, '2024-06-10 00:00:00', '13800000093', 'employee', '毕明', 'biming@hrms.com'),
(94, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0090', '', '', 0, 1, '2024-06-15 00:00:00', '13800000094', 'employee', '景艳', 'jingyan@hrms.com'),
(95, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0091', '', '', 0, 1, '2024-06-20 00:00:00', '13800000095', 'employee', '晏强', 'yanqiang@hrms.com'),
(96, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0092', '', '', 0, 1, '2024-06-25 00:00:00', '13800000096', 'employee', '诸娜', 'zhuna@hrms.com'),
(97, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0093', '', '', 0, 1, '2024-06-28 00:00:00', '13800000097', 'employee', '屠鹏', 'tupeng@hrms.com'),
(98, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0094', '', '', 0, 1, '2024-06-30 00:00:00', '13800000098', 'employee', '鞠芳', 'jufang@hrms.com'),
(99, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0095', '', '', 0, 1, '2024-07-01 00:00:00', '13800000099', 'employee', '仰伟', 'yangwei@hrms.com'),
(100, 'pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=', NOW(), 0, 'emp0096', '', '', 0, 1, '2024-07-05 00:00:00', '13800000100', 'employee', '麦莉', 'maili@hrms.com');

-- ============================================
-- 4. 员工档案表 (employee_employeeprofile) - 100条
-- ============================================
-- 技术研发部 (20人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(1, 'EMP202401TECH001', '2024-01-10', 8000.00, 'active', NULL, '', NOW(), NOW(), 1, 1, 5),
(2, 'EMP202401TECH002', '2024-01-15', 8500.00, 'active', NULL, '', NOW(), NOW(), 1, 1, 6),
(3, 'EMP202402TECH003', '2024-02-01', 9000.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 7),
(4, 'EMP202402TECH004', '2024-02-10', 9000.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 8),
(5, 'EMP202402TECH005', '2024-02-20', 9500.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 9),
(6, 'EMP202403TECH006', '2024-03-01', 9500.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 10),
(7, 'EMP202403TECH007', '2024-03-05', 10000.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 11),
(8, 'EMP202403TECH008', '2024-03-10', 10000.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 12),
(9, 'EMP202403TECH009', '2024-03-15', 10500.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 13),
(10, 'EMP202403TECH010', '2024-03-20', 11000.00, 'active', NULL, '', NOW(), NOW(), 1, 4, 14),
(11, 'EMP202404TECH011', '2024-04-01', 8000.00, 'active', NULL, '', NOW(), NOW(), 1, 1, 15),
(12, 'EMP202404TECH012', '2024-04-05', 8500.00, 'active', NULL, '', NOW(), NOW(), 1, 1, 16),
(13, 'EMP202404TECH013', '2024-04-10', 9000.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 17),
(14, 'EMP202404TECH014', '2024-04-15', 9500.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 18),
(15, 'EMP202404TECH015', '2024-04-20', 10000.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 19),
(16, 'EMP202405TECH016', '2024-05-01', 10000.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 20),
(17, 'EMP202405TECH017', '2024-05-05', 10500.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 21),
(18, 'EMP202405TECH018', '2024-05-10', 11000.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 22),
(19, 'EMP202405TECH019', '2024-05-15', 11500.00, 'active', NULL, '', NOW(), NOW(), 1, 3, 23),
(20, 'EMP202405TECH020', '2024-05-20', 12000.00, 'active', NULL, '', NOW(), NOW(), 1, 4, 24);

-- 产品部 (10人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(21, 'EMP202401PRD021', '2024-01-20', 9000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 25),
(22, 'EMP202402PRD022', '2024-02-15', 9500.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 26),
(23, 'EMP202403PRD023', '2024-03-01', 10000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 27),
(24, 'EMP202403PRD024', '2024-03-20', 10500.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 28),
(25, 'EMP202404PRD025', '2024-04-01', 11000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 29),
(26, 'EMP202404PRD026', '2024-04-15', 11000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 30),
(27, 'EMP202405PRD027', '2024-05-01', 11500.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 31),
(28, 'EMP202405PRD028', '2024-05-10', 11500.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 32),
(29, 'EMP202405PRD029', '2024-05-20', 12000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 33),
(30, 'EMP202406PRD030', '2024-06-01', 12000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 34);

-- 市场部 (10人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(31, 'EMP202401MKT031', '2024-01-25', 7500.00, 'active', NULL, '', NOW(), NOW(), 3, 1, 35),
(32, 'EMP202402MKT032', '2024-02-20', 8000.00, 'active', NULL, '', NOW(), NOW(), 3, 1, 36),
(33, 'EMP202403MKT033', '2024-03-10', 8500.00, 'active', NULL, '', NOW(), NOW(), 3, 2, 37),
(34, 'EMP202403MKT034', '2024-03-25', 9000.00, 'active', NULL, '', NOW(), NOW(), 3, 2, 38),
(35, 'EMP202404MKT035', '2024-04-05', 9500.00, 'active', NULL, '', NOW(), NOW(), 3, 2, 39),
(36, 'EMP202404MKT036', '2024-04-20', 10000.00, 'active', NULL, '', NOW(), NOW(), 3, 2, 40),
(37, 'EMP202405MKT037', '2024-05-05', 10000.00, 'active', NULL, '', NOW(), NOW(), 3, 3, 41),
(38, 'EMP202405MKT038', '2024-05-15', 10500.00, 'active', NULL, '', NOW(), NOW(), 3, 3, 42),
(39, 'EMP202406MKT039', '2024-06-01', 11000.00, 'active', NULL, '', NOW(), NOW(), 3, 3, 43),
(40, 'EMP202406MKT040', '2024-06-10', 11000.00, 'active', NULL, '', NOW(), NOW(), 3, 3, 44);

-- 人力资源部 (5人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(41, 'EMP202402HR041', '2024-02-01', 7000.00, 'active', NULL, '', NOW(), NOW(), 4, 7, 45),
(42, 'EMP202403HR042', '2024-03-01', 7500.00, 'active', NULL, '', NOW(), NOW(), 4, 7, 46),
(43, 'EMP202404HR043', '2024-04-01', 8000.00, 'active', NULL, '', NOW(), NOW(), 4, 7, 47),
(44, 'EMP202405HR044', '2024-05-01', 8500.00, 'active', NULL, '', NOW(), NOW(), 4, 7, 48),
(45, 'EMP202406HR045', '2024-06-01', 9000.00, 'active', NULL, '', NOW(), NOW(), 4, 7, 49);

-- 财务部 (8人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(46, 'EMP202401FIN046', '2024-01-10', 7500.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 50),
(47, 'EMP202402FIN047', '2024-02-15', 8000.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 51),
(48, 'EMP202403FIN048', '2024-03-01', 8500.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 52),
(49, 'EMP202403FIN049', '2024-03-20', 8500.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 53),
(50, 'EMP202404FIN050', '2024-04-05', 9000.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 54),
(51, 'EMP202404FIN051', '2024-04-20', 9000.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 55),
(52, 'EMP202405FIN052', '2024-05-05', 9500.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 56),
(53, 'EMP202405FIN053', '2024-05-20', 10000.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 57);

-- 运营部 (10人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(54, 'EMP202401OPS054', '2024-01-20', 6500.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 58),
(55, 'EMP202402OPS055', '2024-02-10', 7000.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 59),
(56, 'EMP202402OPS056', '2024-02-28', 7500.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 60),
(57, 'EMP202403OPS057', '2024-03-15', 7500.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 61),
(58, 'EMP202404OPS058', '2024-04-01', 8000.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 62),
(59, 'EMP202404OPS059', '2024-04-15', 8000.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 63),
(60, 'EMP202404OPS060', '2024-04-30', 8500.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 64),
(61, 'EMP202405OPS061', '2024-05-10', 8500.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 65),
(62, 'EMP202405OPS062', '2024-05-25', 9000.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 66),
(63, 'EMP202406OPS063', '2024-06-05', 9000.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 67);

-- 设计部 (8人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(64, 'EMP202402DES064', '2024-02-01', 8500.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 68),
(65, 'EMP202402DES065', '2024-02-20', 9000.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 69),
(66, 'EMP202403DES066', '2024-03-10', 9500.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 70),
(67, 'EMP202403DES067', '2024-03-25', 10000.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 71),
(68, 'EMP202404DES068', '2024-04-10', 10000.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 72),
(69, 'EMP202404DES069', '2024-04-25', 10500.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 73),
(70, 'EMP202405DES070', '2024-05-05', 10500.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 74),
(71, 'EMP202405DES071', '2024-05-20', 11000.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 75);

-- 客服部 (8人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(72, 'EMP202401CS072', '2024-01-15', 5500.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 76),
(73, 'EMP202402CS073', '2024-02-01', 6000.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 77),
(74, 'EMP202402CS074', '2024-02-20', 6500.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 78),
(75, 'EMP202403CS075', '2024-03-10', 6500.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 79),
(76, 'EMP202403CS076', '2024-03-25', 7000.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 80),
(77, 'EMP202404CS077', '2024-04-05', 7000.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 81),
(78, 'EMP202404CS078', '2024-04-20', 7500.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 82),
(79, 'EMP202405CS079', '2024-05-05', 7500.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 83);

-- 行政部 (5人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(80, 'EMP202401ADM080', '2024-01-20', 6000.00, 'active', NULL, '', NOW(), NOW(), 9, 1, 84),
(81, 'EMP202402ADM081', '2024-02-15', 6500.00, 'active', NULL, '', NOW(), NOW(), 9, 1, 85),
(82, 'EMP202403ADM082', '2024-03-01', 7000.00, 'active', NULL, '', NOW(), NOW(), 9, 1, 86),
(83, 'EMP202403ADM083', '2024-03-20', 7000.00, 'active', NULL, '', NOW(), NOW(), 9, 1, 87),
(84, 'EMP202404ADM084', '2024-04-10', 7500.00, 'active', NULL, '', NOW(), NOW(), 9, 1, 88);

-- 法务部 (2人)
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(85, 'EMP202402LEG085', '2024-02-01', 10000.00, 'active', NULL, '', NOW(), NOW(), 10, 1, 89),
(86, 'EMP202403LEG086', '2024-03-01', 11000.00, 'active', NULL, '', NOW(), NOW(), 10, 1, 90);

-- 补充剩余14人
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(87, 'EMP202406TECH087', '2024-06-01', 9000.00, 'active', NULL, '', NOW(), NOW(), 1, 2, 91),
(88, 'EMP202406PRD088', '2024-06-05', 10000.00, 'active', NULL, '', NOW(), NOW(), 2, 5, 92),
(89, 'EMP202406MKT089', '2024-06-10', 8500.00, 'active', NULL, '', NOW(), NOW(), 3, 1, 93),
(90, 'EMP202406OPS090', '2024-06-15', 7500.00, 'active', NULL, '', NOW(), NOW(), 6, 9, 94),
(91, 'EMP202406FIN091', '2024-06-20', 8500.00, 'active', NULL, '', NOW(), NOW(), 5, 8, 95),
(92, 'EMP202406CS092', '2024-06-25', 6500.00, 'active', NULL, '', NOW(), NOW(), 8, 10, 96),
(93, 'EMP202406DES093', '2024-06-28', 9500.00, 'active', NULL, '', NOW(), NOW(), 7, 6, 97),
(94, 'EMP202406HR094', '2024-06-30', 7500.00, 'active', NULL, '', NOW(), NOW(), 4, 7, 98),
(95, 'EMP202407ADM095', '2024-07-01', 6500.00, 'active', NULL, '', NOW(), NOW(), 9, 1, 99),
(96, 'EMP202407LEG096', '2024-07-05', 10000.00, 'active', NULL, '', NOW(), NOW(), 10, 1, 100);

-- 已离职员工 (测试离职统计) - 4人
INSERT INTO `employee_employeeprofile` (`id`, `employee_no`, `hire_date`, `salary_base`, `status`, `resigned_date`, `resigned_reason`, `created_at`, `updated_at`, `department_id`, `post_id`, `user_id`) VALUES
(97, 'EMP202312TECH097', '2023-12-01', 9000.00, 'resigned', '2024-11-15', '个人原因离职', NOW(), NOW(), 1, 2, 5),
(98, 'EMP202401MKT098', '2024-01-05', 7500.00, 'resigned', '2024-10-20', '回家发展', NOW(), NOW(), 3, 1, 35),
(99, 'EMP202402OPS099', '2024-02-10', 7000.00, 'resigned', '2024-09-30', '继续深造', NOW(), NOW(), 6, 9, 58),
(100, 'EMP202403FIN100', '2024-03-01', 8000.00, 'resigned', '2024-08-15', '薪资不满意', NOW(), NOW(), 5, 8, 50);

-- ============================================
-- 5. 考勤表 (attendance_attendance)
-- 使用存储过程生成近30天考勤数据
-- 状态分布: 85%正常, 10%迟到, 3%早退, 2%缺勤
-- ============================================
DELIMITER //

DROP PROCEDURE IF EXISTS generate_attendance//
CREATE PROCEDURE generate_attendance(IN start_user INT, IN end_user INT, IN start_date DATE, IN num_days INT)
BEGIN
    DECLARE u INT;
    DECLARE d DATE;
    DECLARE i INT DEFAULT 0;
    DECLARE w INT;
    DECLARE r INT;
    DECLARE in_t TIME;
    DECLARE out_t TIME;
    DECLARE stat VARCHAR(20);

    SET i = 0;
    WHILE i < num_days DO
        SET d = DATE_ADD(start_date, INTERVAL i DAY);
        SET w = DAYOFWEEK(d);
        IF w BETWEEN 2 AND 6 THEN
            SET u = start_user;
            WHILE u <= end_user DO
                SET r = RAND() * 100;
                IF r < 85 THEN
                    SET in_t = TIME('08:55:00') + INTERVAL (RAND() * 10) SECOND;
                    SET out_t = TIME('18:05:00') + INTERVAL (RAND() * 10) SECOND;
                    SET stat = 'normal';
                ELSEIF r < 95 THEN
                    SET in_t = TIME('09:05:00') + INTERVAL (RAND() * 30) SECOND;
                    SET out_t = NULL;
                    SET stat = 'late';
                ELSEIF r < 98 THEN
                    SET in_t = NULL;
                    SET out_t = TIME('17:45:00') + INTERVAL (RAND() * 10) SECOND;
                    SET stat = 'early';
                ELSE
                    SET in_t = NULL;
                    SET out_t = NULL;
                    SET stat = 'absent';
                END IF;
                INSERT INTO attendance_attendance (date, check_in_time, check_out_time, status, created_at, updated_at, user_id)
                VALUES (d, in_t, out_t, stat, NOW(), NOW(), u);
                SET u = u + 1;
            END WHILE;
        END IF;
        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;

-- 执行: 生成用户5-100从2024-12-01开始30天的考勤数据
-- CALL generate_attendance(5, 100, '2024-12-01', 30);

-- ============================================
-- 6. 薪资记录表 (salary_salaryrecord)
-- 使用存储过程生成薪资数据
-- 公式: final = base + overtime - deduction
-- 80%已发布, 20%草稿
-- ============================================
DELIMITER //

DROP PROCEDURE IF EXISTS generate_salary//
CREATE PROCEDURE generate_salary(IN start_user INT, IN end_user INT, IN sal_month VARCHAR(7))
BEGIN
    DECLARE u INT;
    DECLARE base DEC(10,2);
    DECLARE ot_hours DEC(6,1);
    DECLARE ot_pay DEC(10,2);
    DECLARE late_cnt INT;
    DECLARE early_cnt INT;
    DECLARE ded DEC(10,2);
    DECLARE final DEC(10,2);
    DECLARE r INT;

    SET u = start_user;
    WHILE u <= end_user DO
        SELECT salary_base INTO base FROM employee_employeeprofile WHERE user_id = u LIMIT 1;
        IF base IS NOT NULL THEN
            SET ot_hours = RAND() * 20;
            SET ot_pay = ROUND(ot_hours * (base / 22 / 8), 2);
            SET late_cnt = FLOOR(RAND() * 5);
            SET early_cnt = FLOOR(RAND() * 3);
            SET ded = (late_cnt + early_cnt) * 50;
            SET final = base + ot_pay - ded;
            SET r = RAND() * 100;
            IF r < 80 THEN
                INSERT INTO salary_salaryrecord (month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id)
                VALUES (sal_month, base, ot_hours, ot_pay, late_cnt, early_cnt, ded, final, 'published', NOW(), NOW(), u);
            ELSE
                INSERT INTO salary_salaryrecord (month, base_salary, overtime_hours, overtime_pay, late_count, early_count, attendance_deduction, final_salary, status, created_at, updated_at, user_id)
                VALUES (sal_month, base, ot_hours, ot_pay, late_cnt, early_cnt, ded, final, 'draft', NOW(), NOW(), u);
            END IF;
        END IF;
        SET u = u + 1;
    END WHILE;
END//

DELIMITER ;

-- 执行: 生成2024-11, 2024-12, 2025-01薪资数据
-- CALL generate_salary(5, 100, '2024-11');
-- CALL generate_salary(5, 100, '2024-12');
-- CALL generate_salary(5, 100, '2025-01');

SET FOREIGN_KEY_CHECKS = 1;
