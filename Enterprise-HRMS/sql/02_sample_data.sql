-- 样例数据脚本
-- 执行前确保已创建数据库和表结构

USE hrms_db;

-- ============================================
-- 0. 清理已有数据
-- ============================================
DELETE FROM employee_employeeprofile;
DELETE FROM accounts_user;
DELETE FROM organization_post;
DELETE FROM organization_department;

-- 临时禁用外键约束检查（解决执行顺序问题）
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. 部门数据（树形结构）
-- ============================================
INSERT INTO organization_department (id, name, code, parent_id, sort_order, is_active, created_at, updated_at) VALUES
(1, '总公司', 'ROOT', NULL, 1, 1, NOW(), NOW()),
(2, '技术部', 'TECH', 1, 1, 1, NOW(), NOW()),
(3, '产品部', 'PM', 1, 2, 1, NOW(), NOW()),
(4, '人力资源部', 'HR', 1, 3, 1, NOW(), NOW()),
(5, '财务部', 'FIN', 1, 4, 1, NOW(), NOW()),
(6, '市场部', 'MKT', 1, 5, 1, NOW(), NOW()),
(7, '后端开发组', 'BE', 2, 1, 1, NOW(), NOW()),
(8, '前端开发组', 'FE', 2, 2, 1, NOW(), NOW()),
(9, '测试组', 'QA', 2, 3, 1, NOW(), NOW());

-- ============================================
-- 2. 岗位数据
-- ============================================
INSERT INTO organization_post (id, name, code, description, sort_order, is_active, created_at, updated_at) VALUES
(1, '后端工程师', 'BE_DEV', '负责服务端开发与维护', 1, 1, NOW(), NOW()),
(2, '前端工程师', 'FE_DEV', '负责前端页面开发', 2, 1, NOW(), NOW()),
(3, '测试工程师', 'QA_ENG', '负责软件测试工作', 3, 1, NOW(), NOW()),
(4, '产品经理', 'PM_MGR', '负责产品规划与需求管理', 4, 1, NOW(), NOW()),
(5, '人事专员', 'HR_SPEC', '负责招聘与员工关系', 5, 1, NOW(), NOW()),
(6, '财务专员', 'FIN_SPEC', '负责财务核算与报表', 6, 1, NOW(), NOW()),
(7, '市场专员', 'MKT_SPEC', '负责市场推广与品牌', 7, 1, NOW(), NOW()),
(8, '技术总监', 'TECH_DIR', '负责技术团队管理', 8, 1, NOW(), NOW()),
(9, 'CEO', 'CEO', '公司首席执行官', 9, 1, NOW(), NOW());

-- ============================================
-- 3. 用户数据
-- ============================================
INSERT INTO accounts_user (id, password, is_superuser, username, email, is_staff, is_active, date_joined, real_name, phone, role, first_name, last_name) VALUES
(1, '$pbkdf2_sha256$720000$admin$placeholder', 0, 'admin', 'admin@example.com', 1, 1, NOW(), '系统管理员', '13800000000', 'admin', '', ''),
(2, '$pbkdf2_sha256$720000$zhangsan$placeholder', 0, 'zhangsan', 'zhangsan@example.com', 0, 1, NOW(), '张三', '13800000001', 'employee', '', ''),
(3, '$pbkdf2_sha256$720000$lisi$placeholder', 0, 'lisi', 'lisi@example.com', 0, 1, NOW(), '李四', '13800000002', 'employee', '', ''),
(4, '$pbkdf2_sha256$720000$wangwu$placeholder', 0, 'wangwu', 'wangwu@example.com', 0, 1, NOW(), '王五', '13800000003', 'employee', '', ''),
(5, '$pbkdf2_sha256$720000$zhaoliu$placeholder', 0, 'zhaoliu', 'zhaoliu@example.com', 0, 1, NOW(), '赵六', '13800000004', 'employee', '', ''),
(6, '$pbkdf2_sha256$720000$sunqi$placeholder', 0, 'sunqi', 'sunqi@example.com', 0, 1, NOW(), '孙七', '13800000005', 'employee', '', '');

-- ============================================
-- 4. 员工档案数据
-- ============================================
INSERT INTO employee_employeeprofile (id, user_id, employee_no, department_id, post_id, hire_date, salary_base, status, resigned_date, resigned_reason, created_at, updated_at) VALUES
(1, 1, 'EMP202501TECH001', 2, 8, '2023-01-15', 30000, 'active', NULL, '', NOW(), NOW()),
(2, 2, 'EMP202501BE001', 7, 1, '2024-01-10', 15000, 'active', NULL, '', NOW(), NOW()),
(3, 3, 'EMP202501FE001', 8, 2, '2024-02-15', 14000, 'active', NULL, '', NOW(), NOW()),
(4, 4, 'EMP202501PM001', 3, 4, '2023-06-01', 18000, 'active', NULL, '', NOW(), NOW()),
(5, 5, 'EMP202501HR001', 4, 5, '2024-03-01', 10000, 'active', NULL, '', NOW(), NOW()),
(6, 6, 'EMP202402MKT001', 6, 7, '2024-02-20', 12000, 'resigned', '2024-12-01', '个人原因', NOW(), NOW());

-- 恢复外键约束检查
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 验证数据
-- ============================================
SELECT '部门' AS 类型, COUNT(*) AS 数量 FROM organization_department
UNION ALL
SELECT '岗位', COUNT(*) FROM organization_post
UNION ALL
SELECT '用户', COUNT(*) FROM accounts_user
UNION ALL
SELECT '员工档案', COUNT(*) FROM employee_employeeprofile;

-- 查看员工列表
SELECT
    ep.employee_no AS 工号,
    u.real_name AS 姓名,
    d.name AS 部门,
    p.name AS 岗位,
    ep.hire_date AS 入职日期,
    ep.salary_base AS 基本工资,
    ep.status AS 状态
FROM employee_employeeprofile ep
LEFT JOIN accounts_user u ON ep.user_id = u.id
LEFT JOIN organization_department d ON ep.department_id = d.id
LEFT JOIN organization_post p ON ep.post_id = p.id;
