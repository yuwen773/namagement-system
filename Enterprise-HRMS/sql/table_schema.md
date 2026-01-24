# HRMS 数据库表结构文档

## 一、ER 关系图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              accounts_user                                   │
│  (id, username, password, phone, role, real_name, email, is_superuser...)  │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │ 1:N (user_id)
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      employee_employeeprofile                               │
│  (id, employee_no, hire_date, salary_base, status, department_id, post_id) │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │ references
           ▼
┌─────────────────────┐    ┌─────────────────────┐
│ organization_dept   │◄───┤ organization_dept  │ (自关联 parent_id)
│ (id, name, code...) │    │                     │
└─────────────────────┘    └─────────────────────┘
           │
           │ 1:N
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         organization_post                                   │
│  (id, name, code, description, sort_order, is_active)                      │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │ 1:N (post_id)
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         attendance_attendance                               │
│  (id, date, check_in_time, check_out_time, status, user_id)                │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │ 1:N (user_id)
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          salary_salaryrecord                                │
│  (id, month, base_salary, overtime_hours, late_count, final_salary, ...)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 二、核心业务表结构

### 1. organization_department（部门表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | bigint | PK AUTO_INCREMENT | 主键 |
| name | varchar(50) | NOT NULL | 部门名称 |
| code | varchar(20) | UNIQUE NOT NULL | 部门编码 |
| sort_order | int | NOT NULL | 排序序号 |
| is_active | tinyint(1) | NOT NULL | 是否启用 |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |
| parent_id | bigint | FK -> self | 上级部门ID（自关联） |

**索引：**
- PRIMARY (id)
- UNIQUE (code)
- INDEX (parent_id)

### 2. organization_post（岗位表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | bigint | PK AUTO_INCREMENT | 主键 |
| name | varchar(50) | NOT NULL | 岗位名称 |
| code | varchar(20) | UNIQUE NOT NULL | 岗位编码 |
| description | longtext | NOT NULL | 岗位描述 |
| sort_order | int | NOT NULL | 排序序号 |
| is_active | tinyint(1) | NOT NULL | 是否启用 |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |

**索引：**
- PRIMARY (id)
- UNIQUE (code)

### 3. accounts_user（用户表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | bigint | PK AUTO_INCREMENT | 主键 |
| password | varchar(128) | NOT NULL | 加密密码 |
| last_login | datetime(6) | NULL | 最后登录时间 |
| is_superuser | tinyint(1) | NOT NULL | 超级用户标识 |
| username | varchar(150) | UNIQUE NOT NULL | 用户名 |
| first_name | varchar(150) | NOT NULL | 名 |
| last_name | varchar(150) | NOT NULL | 姓 |
| is_staff | tinyint(1) | NOT NULL | 员工标识 |
| is_active | tinyint(1) | NOT NULL | 是否激活 |
| date_joined | datetime(6) | NOT NULL | 注册时间 |
| phone | varchar(11) | UNIQUE NOT NULL | 手机号 |
| role | varchar(20) | NOT NULL | 角色 (employee/hr/admin) |
| real_name | varchar(50) | NOT NULL | 真实姓名 |
| email | varchar(254) | UNIQUE NOT NULL | 邮箱 |

**索引：**
- PRIMARY (id)
- UNIQUE (username)
- UNIQUE (phone)
- UNIQUE (email)

### 4. employee_employeeprofile（员工档案表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | bigint | PK AUTO_INCREMENT | 主键 |
| employee_no | varchar(20) | UNIQUE NOT NULL | 员工编号 |
| hire_date | date | NOT NULL | 入职日期 |
| salary_base | decimal(10,2) | NOT NULL | 基本工资 |
| status | varchar(20) | NOT NULL | 状态 (active/resigned) |
| resigned_date | date | NULL | 离职日期 |
| resigned_reason | longtext | NOT NULL | 离职原因 |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |
| department_id | bigint | FK -> organization_department | 部门ID |
| post_id | bigint | FK -> organization_post | 岗位ID |
| user_id | bigint | FK -> accounts_user | 用户ID |

**索引：**
- PRIMARY (id)
- UNIQUE (employee_no)
- UNIQUE (user_id)
- INDEX (department_id)
- INDEX (post_id)

**外键约束：**
- department_id -> organization_department(id)
- post_id -> organization_post(id)
- user_id -> accounts_user(id)

### 5. attendance_attendance（考勤表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | bigint | PK AUTO_INCREMENT | 主键 |
| date | date | NOT NULL | 考勤日期 |
| check_in_time | time(6) | NULL | 签到时间 |
| check_out_time | time(6) | NULL | 签退时间 |
| status | varchar(20) | NOT NULL | 状态 (normal/late/early/absent) |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |
| user_id | bigint | FK -> accounts_user | 用户ID |

**索引：**
- PRIMARY (id)
- UNIQUE (user_id, date)
- INDEX (date)

**外键约束：**
- user_id -> accounts_user(id)

### 6. salary_salaryrecord（薪资记录表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | bigint | PK AUTO_INCREMENT | 主键 |
| month | varchar(7) | NOT NULL | 月份 (YYYY-MM) |
| base_salary | decimal(10,2) | NOT NULL | 基本工资 |
| overtime_hours | decimal(6,1) | NOT NULL | 加班小时数 |
| overtime_pay | decimal(10,2) | NOT NULL | 加班工资 |
| late_count | int | NOT NULL | 迟到次数 |
| early_count | int | NOT NULL | 早退次数 |
| attendance_deduction | decimal(10,2) NOT NULL | 考勤扣款 |
| final_salary | decimal(10,2) | NOT NULL | 最终工资 |
| status | varchar(20) | NOT NULL | 状态 (draft/published) |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |
| user_id | bigint | FK -> accounts_user | 用户ID |

**索引：**
- PRIMARY (id)
- UNIQUE (user_id, month)

**外键约束：**
- user_id -> accounts_user(id)

## 三、薪资计算公式

```
final_salary = base_salary + overtime_pay - attendance_deduction

其中:
- overtime_pay = overtime_hours * (base_salary / 22 / 8)
- attendance_deduction = (late_count + early_count) * 50
```

## 四、员工编号规则

```
EMP{YYYYMM}{DEPT_CODE}{3-digit_seq}
示例: EMP202401TECH001
```

## 五、测试数据说明

- **测试密码**: `Test123456.`
- **密码哈希**: `pbkdf2_sha256$1000000$jvYT8esvy8dqFSaE1Pul7b$F9aFo9R4opyBsRAKIFrok6LQKWZ0ZzG3a5rwwNDtHQg=`
- **用户角色分布**: 1 Admin + 3 HR + 96 Employee
- **考勤数据**: 每个员工约30天记录
- **薪资数据**: 每个员工近3个月记录
