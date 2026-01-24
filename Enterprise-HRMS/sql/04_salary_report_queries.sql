-- =============================================
-- 薪资统计查询脚本
-- 生成时间: 2025-01-24
-- 用途: 薪资数据分析与报表
-- =============================================

-- 1. 查询某月薪资汇总
SELECT
    month,
    COUNT(*) AS record_count,
    SUM(base_salary) AS total_base_salary,
    SUM(overtime_pay) AS total_overtime_pay,
    SUM(attendance_deduction) AS total_deduction,
    SUM(final_salary) AS total_final_salary,
    AVG(final_salary) AS avg_final_salary
FROM salary_salaryrecord
WHERE month = '2025-01' AND status = 'published'
GROUP BY month;

-- 2. 查询员工年度薪资汇总
SELECT
    sr.user_id,
    u.real_name,
    sr.month,
    sr.base_salary,
    sr.final_salary,
    SUM(sr.final_salary) OVER (PARTITION BY sr.user_id ORDER BY sr.month) AS cumulative_salary
FROM salary_salaryrecord sr
JOIN accounts_user u ON sr.user_id = u.id
WHERE sr.status = 'published'
ORDER BY sr.user_id, sr.month;

-- 3. 查询考勤扣款排名（某月）
SELECT
    sr.user_id,
    u.real_name,
    sr.late_count,
    sr.early_count,
    sr.attendance_deduction
FROM salary_salaryrecord sr
JOIN accounts_user u ON sr.user_id = u.id
WHERE sr.month = '2025-01'
ORDER BY sr.attendance_deduction DESC;

-- 4. 查询加班时长排名（某月）
SELECT
    sr.user_id,
    u.real_name,
    sr.overtime_hours,
    sr.overtime_pay
FROM salary_salaryrecord sr
JOIN accounts_user u ON sr.user_id = u.id
WHERE sr.month = '2025-01' AND sr.overtime_hours > 0
ORDER BY sr.overtime_hours DESC;

-- 5. 薪资发放状态统计
SELECT
    status,
    month,
    COUNT(*) AS count,
    SUM(final_salary) AS total_amount
FROM salary_salaryrecord
GROUP BY status, month
ORDER BY month DESC, status;

-- 6. 薪资结构分析（某月）
SELECT
    '基本工资' AS category,
    SUM(base_salary) AS amount
FROM salary_salaryrecord
WHERE month = '2025-01'
UNION ALL
SELECT
    '加班费' AS category,
    SUM(overtime_pay) AS amount
FROM salary_salaryrecord
WHERE month = '2025-01'
UNION ALL
SELECT
    '考勤扣款' AS category,
    SUM(attendance_deduction) * -1 AS amount
FROM salary_salaryrecord
WHERE month = '2025-01';
