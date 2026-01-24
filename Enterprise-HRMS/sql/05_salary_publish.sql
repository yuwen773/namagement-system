-- =============================================
-- 薪资发布操作脚本
-- 生成时间: 2025-01-24
-- 用途: 将草稿状态薪资更新为已发布
-- =============================================

-- 1. 发布单条薪资记录
UPDATE salary_salaryrecord
SET status = 'published', updated_at = NOW()
WHERE id = 1 AND status = 'draft';

-- 2. 发布某员工某月薪资
UPDATE salary_salaryrecord
SET status = 'published', updated_at = NOW()
WHERE user_id = 1 AND month = '2025-01' AND status = 'draft';

-- 3. 批量发布某月所有草稿薪资
UPDATE salary_salaryrecord
SET status = 'published', updated_at = NOW()
WHERE month = '2025-01' AND status = 'draft';

-- 4. 撤销发布（将已发布改为草稿）
UPDATE salary_salaryrecord
SET status = 'draft', updated_at = NOW()
WHERE id = 1 AND status = 'published';

-- 5. 查看待发布的薪资记录
SELECT
    sr.id,
    u.real_name,
    sr.month,
    sr.base_salary,
    sr.final_salary,
    sr.status
FROM salary_salaryrecord sr
JOIN accounts_user u ON sr.user_id = u.id
WHERE sr.status = 'draft'
ORDER BY sr.month, u.real_name;

-- 6. 查看某月薪资发放情况
SELECT
    sr.month,
    sr.status,
    COUNT(*) AS count,
    SUM(sr.final_salary) AS total_amount
FROM salary_salaryrecord sr
WHERE sr.month = '2025-01'
GROUP BY sr.month, sr.status;
