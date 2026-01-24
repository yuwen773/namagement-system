-- =============================================
-- 薪资记录示例数据
-- 生成时间: 2025-01-24
-- 用途: 薪资模块测试数据
-- =============================================

-- 插入薪资记录（张三，2024年12月，已发布）
INSERT INTO salary_salaryrecord (
    user_id,
    month,
    base_salary,
    overtime_hours,
    overtime_pay,
    late_count,
    early_count,
    attendance_deduction,
    final_salary,
    status,
    created_at,
    updated_at
) VALUES (
    1,                                              -- user_id (张三)
    '2024-12',
    30000.00,                                        -- base_salary
    10.0,                                            -- overtime_hours
    1704.55,                                         -- overtime_pay (30000/22/8*10)
    1,                                               -- late_count
    0,                                               -- early_count
    50.00,                                           -- attendance_deduction (1*50)
    31654.55,                                        -- final_salary (30000+1704.55-50)
    'published',                                     -- status
    NOW(),
    NOW()
);

-- 插入薪资记录（张三，2025年1月，草稿）
INSERT INTO salary_salaryrecord (
    user_id,
    month,
    base_salary,
    overtime_hours,
    overtime_pay,
    late_count,
    early_count,
    attendance_deduction,
    final_salary,
    status,
    created_at,
    updated_at
) VALUES (
    1,                                              -- user_id (张三)
    '2025-01',
    30000.00,                                        -- base_salary
    0.0,                                             -- overtime_hours
    0.00,                                            -- overtime_pay
    2,                                               -- late_count
    1,                                               -- early_count
    150.00,                                          -- attendance_deduction (3*50)
    29850.00,                                        -- final_salary (30000-150)
    'draft',                                         -- status
    NOW(),
    NOW()
);

-- 插入薪资记录（李四，2024年12月，已发布）
INSERT INTO salary_salaryrecord (
    user_id,
    month,
    base_salary,
    overtime_hours,
    overtime_pay,
    late_count,
    early_count,
    attendance_deduction,
    final_salary,
    status,
    created_at,
    updated_at
) VALUES (
    2,                                              -- user_id (李四)
    '2024-12',
    25000.00,                                        -- base_salary
    5.0,                                             -- overtime_hours
    710.23,                                          -- overtime_pay (25000/22/8*5)
    0,                                               -- late_count
    0,                                               -- early_count
    0.00,                                            -- attendance_deduction
    25710.23,                                        -- final_salary
    'published',                                     -- status
    NOW(),
    NOW()
);

-- 插入薪资记录（李四，2025年1月，已发布）
INSERT INTO salary_salaryrecord (
    user_id,
    month,
    base_salary,
    overtime_hours,
    overtime_pay,
    late_count,
    early_count,
    attendance_deduction,
    final_salary,
    status,
    created_at,
    updated_at
) VALUES (
    2,                                              -- user_id (李四)
    '2025-01',
    25000.00,                                        -- base_salary
    8.0,                                             -- overtime_hours
    1136.36,                                         -- overtime_pay (25000/22/8*8)
    1,                                               -- late_count
    0,                                               -- early_count
    50.00,                                           -- attendance_deduction
    26086.36,                                        -- final_salary
    'published',                                     -- status
    NOW(),
    NOW()
);

-- 插入薪资记录（王五，2025年1月，草稿）
INSERT INTO salary_salaryrecord (
    user_id,
    month,
    base_salary,
    overtime_hours,
    overtime_pay,
    late_count,
    early_count,
    attendance_deduction,
    final_salary,
    status,
    created_at,
    updated_at
) VALUES (
    3,                                              -- user_id (王五)
    '2025-01',
    20000.00,                                        -- base_salary
    0.0,                                             -- overtime_hours
    0.00,                                            -- overtime_pay
    0,                                               -- late_count
    0,                                               -- early_count
    0.00,                                            -- attendance_deduction
    20000.00,                                        -- final_salary
    'draft',                                         -- status
    NOW(),
    NOW()
);

SELECT '薪资测试数据插入完成！' AS result;
