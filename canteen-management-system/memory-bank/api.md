# 食堂管理系统 - 后端 API 文档

## 概述

本文档描述食堂管理系统的所有后端 API 接口。

- **Base URL**: `http://localhost:8000/api/`
- **数据格式**: JSON
- **字符编码**: UTF-8

---

## 统一响应格式

所有 API 接口返回统一的响应格式：

### 成功响应
```json
{
    "code": 200,
    "message": "成功",
    "data": {}
}
```

### 分页响应
```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "count": 100,
        "next": "http://localhost:8000/api/employees/?page=2",
        "previous": null,
        "results": []
    }
}
```

### 错误响应
```json
{
    "code": 400,
    "message": "请求参数错误",
    "errors": {
        "field_name": ["错误信息"]
    }
}
```

### 分页参数
- `page`: 页码（默认: 1）
- `page_size`: 每页数量（默认: 20，最大: 100）

---

## 1. 用户管理 (accounts)

### 1.1 用户登录

**接口**: `POST /api/accounts/login/`

**请求体**:
```json
{
    "username": "admin",
    "password": "admin123"
}
```

**响应**:
```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "id": 1,
        "username": "admin",
        "role": "ADMIN",
        "employee": null
    }
}
```

---

### 1.2 用户注册

**接口**: `POST /api/accounts/register/`

**请求体**:
```json
{
    "username": "test_user",
    "password": "123456",
    "phone": "13800138000",
    "email": "test@example.com"
}
```

**响应**: 返回创建的用户信息（默认角色: EMPLOYEE）

---

### 1.3 获取用户列表

**接口**: `GET /api/accounts/`

**权限**: 仅管理员

**查询参数**: 无（使用分页）

**响应**: 分页用户列表

---

### 1.4 获取用户详情

**接口**: `GET /api/accounts/{id}/`

**路径参数**:
- `id`: 用户 ID

---

### 1.5 创建用户

**接口**: `POST /api/accounts/`

**权限**: 仅管理员

**请求体**:
```json
{
    "username": "new_user",
    "password": "123456",
    "role": "EMPLOYEE",
    "employee": 1
}
```

**字段说明**:
- `role`: ADMIN（管理员）或 EMPLOYEE（员工）
- `employee`: 关联的员工档案 ID（可选）

---

### 1.6 更新用户

**接口**: `PUT /api/accounts/{id}/`

**请求体**: 支持部分更新

---

### 1.7 删除用户

**接口**: `DELETE /api/accounts/{id}/`

---

## 2. 员工管理 (employees)

### 2.1 获取员工列表

**接口**: `GET /api/employees/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `position` | string | 岗位过滤: CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER |
| `status` | string | 状态过滤: ACTIVE/INACTIVE/LEAVE_WITHOUT_PAY |
| `search` | string | 搜索姓名、手机号、身份证 |
| `ordering` | string | 排序: created_at, entry_date, name |
| `page` | int | 页码 |
| `page_size` | int | 每页数量 |

**响应**: 分页员工列表

---

### 2.2 获取员工详情

**接口**: `GET /api/employees/{id}/`

**路径参数**:
- `id`: 员工 ID

**响应**: 完整员工信息（包括证件信息）

---

### 2.3 创建员工

**接口**: `POST /api/employees/`

**请求体**:
```json
{
    "name": "张三",
    "gender": "MALE",
    "phone": "13800138000",
    "id_card": "110101199001011234",
    "address": "北京市朝阳区",
    "position": "CHEF",
    "entry_date": "2024-01-01",
    "status": "ACTIVE",
    "health_certificate_no": "HC123456",
    "health_certificate_expiry": "2025-12-31",
    "health_certificate_url": "",
    "chef_certificate_level": "高级"
}
```

**字段说明**:
- `gender`: MALE（男）或 FEMALE（女）
- `position`: CHEF（厨师）/PASTRY（面点）/PREP（切配）/CLEANER（保洁）/SERVER（服务员）/MANAGER（经理）
- `status`: ACTIVE（在职）/INACTIVE（离职）/LEAVE_WITHOUT_PAY（停薪留职）

---

### 2.4 更新员工

**接口**: `PUT /api/employees/{id}/`

**请求体**: 支持部分更新

---

### 2.5 删除员工

**接口**: `DELETE /api/employees/{id}/`

---

## 3. 排班管理 (schedules)

### 3.1 班次管理

#### 3.1.1 获取班次列表

**接口**: `GET /api/schedules/shifts/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | string | 班次名称过滤 |
| `ordering` | string | 排序: start_time, created_at |

---

#### 3.1.2 获取班次详情

**接口**: `GET /api/schedules/shifts/{id}/`

---

#### 3.1.3 创建班次

**接口**: `POST /api/schedules/shifts/`

**请求体**:
```json
{
    "name": "早班",
    "start_time": "06:00:00",
    "end_time": "14:00:00"
}
```

---

#### 3.1.4 更新班次

**接口**: `PUT /api/schedules/shifts/{id}/`

---

#### 3.1.5 删除班次

**接口**: `DELETE /api/schedules/shifts/{id}/`

---

### 3.2 排班计划

#### 3.2.1 获取排班列表

**接口**: `GET /api/schedules/schedules/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `employee` | int | 员工 ID |
| `shift` | int | 班次 ID |
| `work_date` | date | 工作日期 (YYYY-MM-DD) |
| `is_swapped` | bool | 是否调班 |
| `search` | string | 搜索员工姓名、手机号 |
| `ordering` | string | 排序: work_date, created_at |

---

#### 3.2.2 获取排班详情

**接口**: `GET /api/schedules/schedules/{id}/`

---

#### 3.2.3 创建排班

**接口**: `POST /api/schedules/schedules/`

**请求体**:
```json
{
    "employee": 1,
    "shift": 1,
    "work_date": "2024-01-15"
}
```

---

#### 3.2.4 更新排班

**接口**: `PUT /api/schedules/schedules/{id}/`

---

#### 3.2.5 删除排班

**接口**: `DELETE /api/schedules/schedules/{id}/`

---

#### 3.2.6 批量创建排班

**接口**: `POST /api/schedules/schedules/batch_create/`

**请求体**:
```json
{
    "employee_ids": [1, 2, 3],
    "shift_id": 1,
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
}
```

**响应**:
```json
{
    "code": 200,
    "message": "批量创建成功",
    "data": {
        "created_count": 90,
        "skipped_count": 0,
        "total_dates": 31,
        "total_employees": 3
    }
}
```

---

#### 3.2.7 日历视图

**接口**: `POST /api/schedules/schedules/calendar_view/`

**请求体**:
```json
{
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "employee_id": 1
}
```

**响应**: 按日期分组的排班数据

---

### 3.3 调班申请

#### 3.3.1 获取调班申请列表

**接口**: `GET /api/schedules/shift-requests/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `requester` | int | 申请人 ID |
| `status` | string | 状态: PENDING/APPROVED/REJECTED |
| `target_date` | date | 目标日期 |
| `search` | string | 搜索申请人姓名、原因 |

---

#### 3.3.2 获取调班申请详情

**接口**: `GET /api/schedules/shift-requests/{id}/`

---

#### 3.3.3 创建调班申请

**接口**: `POST /api/schedules/shift-requests/`

**请求体**:
```json
{
    "original_schedule": 1,
    "target_date": "2024-01-20",
    "target_shift": 2,
    "reason": "个人原因",
    "requester_id": 1
}
```

---

#### 3.3.4 更新调班申请

**接口**: `PUT /api/schedules/shift-requests/{id}/`

---

#### 3.3.5 删除调班申请

**接口**: `DELETE /api/schedules/shift-requests/{id}/`

---

#### 3.3.6 审批调班申请

**接口**: `POST /api/schedules/shift-requests/{id}/approve/`

**请求体**:
```json
{
    "approve": true,
    "approval_remark": "同意"
}
```

---

#### 3.3.7 我的调班申请

**接口**: `GET /api/schedules/shift-requests/my_requests/?employee_id=1`

---

#### 3.3.8 待审批调班申请

**接口**: `GET /api/schedules/shift-requests/pending/`

**权限**: 仅管理员

---

## 4. 考勤管理 (attendance)

### 4.1 获取考勤记录列表

**接口**: `GET /api/attendance/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `employee` | int | 员工 ID |
| `status` | string | 状态: NORMAL/LATE/EARLY_LEAVE/MISSING/ABNORMAL |
| `search` | string | 搜索姓名、手机号、打卡地点 |
| `ordering` | string | 排序: created_at, clock_in_time, clock_out_time |

---

### 4.2 获取考勤详情

**接口**: `GET /api/attendance/{id}/`

---

### 4.3 创建考勤记录

**接口**: `POST /api/attendance/`

**权限**: 仅管理员（手动创建）

---

### 4.4 更新考勤记录

**接口**: `PUT /api/attendance/{id}/`

---

### 4.5 删除考勤记录

**接口**: `DELETE /api/attendance/{id}/`

---

### 4.6 员工签到

**接口**: `POST /api/attendance/clock_in/`

**请求体**:
```json
{
    "employee_id": 1,
    "schedule_id": 1,
    "clock_in_location": "食堂一楼"
}
```

**响应**:
```json
{
    "code": 200,
    "message": "签到成功",
    "data": {
        "id": 1,
        "employee": 1,
        "clock_in_time": "2024-01-15T08:05:00Z",
        "clock_in_location": "食堂一楼",
        "status": "LATE",
        "is_late": true,
        "late_minutes": 5
    }
}
```

---

### 4.7 员工签退

**接口**: `POST /api/attendance/clock_out/`

**请求体**:
```json
{
    "employee_id": 1,
    "clock_out_location": "食堂一楼"
}
```

**响应**:
```json
{
    "code": 200,
    "message": "签退成功",
    "data": {
        "id": 1,
        "clock_out_time": "2024-01-15T18:30:00Z",
        "clock_out_location": "食堂一楼",
        "overtime_hours": 4.5,
        "is_early_leave": false
    }
}
```

---

### 4.8 考勤统计

**接口**: `POST /api/attendance/statistics/`

**请求体**:
```json
{
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "employee_id": 1
}
```

**响应**:
```json
{
    "code": 200,
    "data": {
        "total_days": 22,
        "present_days": 20,
        "late_count": 2,
        "early_leave_count": 1,
        "missing_count": 0,
        "overtime_hours": 8.5
    }
}
```

---

### 4.9 更正考勤

**接口**: `POST /api/attendance/{id}/correct/`

**权限**: 仅管理员

**请求体**:
```json
{
    "status": "NORMAL",
    "correction_remark": "误判，更正为正常"
}
```

---

### 4.10 我的考勤记录

**接口**: `GET /api/attendance/my_attendance/?employee_id=1&start_date=2024-01-01&end_date=2024-01-31`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `employee_id` | int | 员工 ID（必填） |
| `start_date` | date | 开始日期 |
| `end_date` | date | 结束日期 |

---

## 5. 请假管理 (leaves)

### 5.1 获取请假列表

**接口**: `GET /api/leaves/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `employee` | int | 员工 ID |
| `leave_type` | string | 类型: ANNUAL/SICK/PERSONAL/MATERNITY/PATERNITY/OTHER |
| `status` | string | 状态: PENDING/APPROVED/REJECTED/CANCELLED |
| `search` | string | 搜索姓名、手机号、原因 |

---

### 5.2 获取请假详情

**接口**: `GET /api/leaves/{id}/`

---

### 5.3 创建请假申请

**接口**: `POST /api/leaves/`

**请求体**:
```json
{
    "employee": 1,
    "leave_type": "ANNUAL",
    "start_time": "2024-01-20T09:00:00",
    "end_time": "2024-01-22T18:00:00",
    "reason": "家事"
}
```

**字段说明**:
- `leave_type`: ANNUAL（年假）/SICK（病假）/PERSONAL（事假）/MATERNITY（产假）/PATERNITY（陪产假）/OTHER（其他）

---

### 5.4 更新请假申请

**接口**: `PUT /api/leaves/{id}/`

---

### 5.5 删除请假申请

**接口**: `DELETE /api/leaves/{id}/`

---

### 5.6 我的请假申请

**接口**: `GET /api/leaves/my-requests/?employee_id=1&status=PENDING`

---

### 5.7 待审批请假申请

**接口**: `GET /api/leaves/pending/`

**权限**: 仅管理员

---

### 5.8 审批请假申请

**接口**: `POST /api/leaves/{id}/approve/`

**请求体**:
```json
{
    "approve": true,
    "approval_remark": "同意",
    "approver_id": 2
}
```

---

## 6. 薪资管理 (salaries)

### 6.1 薪资记录

#### 6.1.1 获取薪资列表

**接口**: `GET /api/salaries/salaries/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `employee` | int | 员工 ID |
| `year_month` | string | 年月 (YYYY-MM) |
| `status` | string | 状态: DRAFT/PUBLISHED/ADJUSTED/APPEALED |
| `search` | string | 搜索姓名、手机号 |

---

#### 6.1.2 获取薪资详情

**接口**: `GET /api/salaries/salaries/{id}/`

---

#### 6.1.3 创建薪资记录

**接口**: `POST /api/salaries/salaries/`

**请求体**:
```json
{
    "employee": 1,
    "year_month": "2024-01",
    "base_salary": 3000.00,
    "position_allowance": 800.00,
    "overtime_pay": 500.00,
    "deductions": 20.00,
    "work_days": 22,
    "late_count": 1,
    "missing_count": 0,
    "overtime_hours": 8.0
}
```

---

#### 6.1.4 更新薪资记录

**接口**: `PUT /api/salaries/salaries/{id}/`

---

#### 6.1.5 删除薪资记录

**接口**: `DELETE /api/salaries/salaries/{id}/`

---

#### 6.1.6 生成薪资（自动计算）

**接口**: `POST /api/salaries/salaries/generate/`

**请求体**:
```json
{
    "year_month": "2024-01",
    "employee_ids": [1, 2, 3]
}
```

**响应**:
```json
{
    "code": 200,
    "message": "薪资生成完成",
    "data": {
        "created": 3,
        "skipped": 0,
        "errors": []
    }
}
```

**薪资计算公式**:
- 日工资 = 基本工资 ÷ 21.75 天
- 小时工资 = 日工资 ÷ 8 小时
- 加班费 = 小时工资 × 1.5 × 加班小时数
- 迟到扣款 = 20 元/次
- 缺卡扣款 = 50 元/次
- 实发工资 = 基本工资 + 岗位津贴 + 加班费 - 迟到扣款 - 缺卡扣款

**岗位津贴标准**:
| 岗位 | 津贴（元） |
|------|-----------|
| CHEF（厨师） | 800 |
| PASTRY（面点） | 700 |
| PREP（切配） | 500 |
| CLEANER（保洁） | 300 |
| SERVER（服务员） | 400 |
| MANAGER（经理） | 1000 |

---

#### 6.1.7 调整薪资

**接口**: `POST /api/salaries/salaries/{id}/adjust/`

**权限**: 仅管理员

**请求体**:
```json
{
    "base_salary": 3500.00,
    "overtime_pay": 600.00,
    "reason": "绩效调整"
}
```

---

#### 6.1.8 发布薪资

**接口**: `POST /api/salaries/salaries/{id}/publish/`

**权限**: 仅管理员

**说明**: 将状态从 DRAFT 改为 PUBLISHED

---

#### 6.1.9 我的薪资记录

**接口**: `GET /api/salaries/salaries/my-salaries/?employee_id=1&year_month=2024-01`

---

### 6.2 异常申诉

#### 6.2.1 获取申诉列表

**接口**: `GET /api/salaries/appeals/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `appeal_type` | string | 类型: ATTENDANCE/SALARY |
| `employee` | int | 员工 ID |
| `status` | string | 状态: PENDING/APPROVED/REJECTED |
| `search` | string | 搜索姓名、原因 |

---

#### 6.2.2 获取申诉详情

**接口**: `GET /api/salaries/appeals/{id}/`

---

#### 6.2.3 创建申诉

**接口**: `POST /api/salaries/appeals/`

**请求体**:
```json
{
    "appeal_type": "ATTENDANCE",
    "employee": 1,
    "target_id": 5,
    "reason": "当日实际按时签到，系统误判"
}
```

**字段说明**:
- `appeal_type`: ATTENDANCE（考勤申诉）/SALARY（薪资申诉）
- `target_id`: 关联的考勤记录 ID 或薪资记录 ID

---

#### 6.2.4 更新申诉

**接口**: `PUT /api/salaries/appeals/{id}/`

---

#### 6.2.5 删除申诉

**接口**: `DELETE /api/salaries/appeals/{id}/`

---

#### 6.2.6 审批申诉

**接口**: `POST /api/salaries/appeals/{id}/approve/`

**权限**: 仅管理员

**请求体**:
```json
{
    "approve": true,
    "approval_remark": "核实后同意",
    "approver_id": 2
}
```

---

#### 6.2.7 待审批申诉

**接口**: `GET /api/salaries/appeals/pending/?appeal_type=SALARY`

**权限**: 仅管理员

---

#### 6.2.8 我的申诉

**接口**: `GET /api/salaries/appeals/my-appeals/?employee_id=1`

---

## 7. 统计分析 (analytics)

### 7.1 员工统计

**接口**: `GET /api/analytics/employees/`

**响应**:
```json
{
    "code": 200,
    "data": {
        "overview": {
            "total_count": 50,
            "health_cert_rate": 95.0,
            "chef_cert_rate": 30.0
        },
        "position_distribution": {
            "labels": ["厨师", "面点", "切配", "保洁", "服务员", "经理"],
            "data": [10, 8, 12, 15, 5, 3]
        },
        "certificates": {
            "health_cert_count": 45,
            "chef_cert_count": 15
        },
        "status_distribution": {
            "labels": ["在职", "离职", "停薪留职"],
            "data": [50, 5, 2]
        }
    }
}
```

---

### 7.2 考勤统计

**接口**: `GET /api/analytics/attendance/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `start_date` | date | 开始日期 (YYYY-MM-DD) |
| `end_date` | date | 结束日期 (YYYY-MM-DD) |
| `days` | int | 最近 N 天（默认: 7） |

**响应**:
```json
{
    "code": 200,
    "data": {
        "overview": {
            "total_should_attend": 100,
            "attendance_rate": 95.5,
            "late_count": 3,
            "missing_count": 1,
            "total_overtime_hours": 45.5
        },
        "status_distribution": {
            "labels": ["正常", "迟到", "早退", "缺卡", "异常"],
            "data": [90, 3, 2, 1, 0]
        },
        "daily_trend": [
            {
                "date": "2024-01-01",
                "normal": 18,
                "late": 1,
                "early_leave": 0,
                "missing": 0
            }
        ],
        "position_stats": [
            {
                "position": "厨师",
                "late_count": 1,
                "missing_count": 0,
                "overtime_hours": 20.5
            }
        ]
    }
}
```

---

### 7.3 薪资统计

**接口**: `GET /api/analytics/salaries/`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `months` | int | 最近 N 个月（默认: 12） |

**响应**:
```json
{
    "code": 200,
    "data": {
        "monthly_trend": [
            {
                "year_month": "2024-01",
                "total_salary": 150000.0,
                "avg_salary": 3000.0,
                "count": 50
            }
        ],
        "position_comparison": [
            {
                "position": "厨师",
                "total_salary": 24000.0,
                "avg_salary": 4800.0,
                "count": 5
            }
        ],
        "composition": {
            "base_salary": 90000.0,
            "position_allowance": 25000.0,
            "overtime_pay": 15000.0,
            "deductions": 500.0,
            "distribution": {
                "labels": ["基本工资", "岗位津贴", "加班费", "扣款"],
                "data": [90000, 25000, 15000, 500]
            }
        }
    }
}
```

---

### 7.4 概览统计（仪表盘）

**接口**: `GET /api/analytics/overview/`

**响应**:
```json
{
    "code": 200,
    "data": {
        "today": {
            "should_attend": 45,
            "present": 43,
            "late": 2,
            "missing": 0,
            "leaves": 1,
            "abnormal": 2,
            "attendance_rate": 95.56
        },
        "pending": {
            "leaves": 3,
            "attendance_corrections": 5,
            "salary_generation": 1
        },
        "overview": {
            "total_employees": 50,
            "total_positions": 6
        },
        "month_attendance": {
            "late_count": 15,
            "missing_count": 3
        }
    }
}
```

---

## 枚举值说明

### 员工岗位 (position)
| 值 | 说明 |
|----|------|
| CHEF | 厨师 |
| PASTRY | 面点 |
| PREP | 切配 |
| CLEANER | 保洁 |
| SERVER | 服务员 |
| MANAGER | 经理 |

### 员工状态 (status)
| 值 | 说明 |
|----|------|
| ACTIVE | 在职 |
| INACTIVE | 离职 |
| LEAVE_WITHOUT_PAY | 停薪留职 |

### 用户角色 (role)
| 值 | 说明 |
|----|------|
| ADMIN | 管理员 |
| EMPLOYEE | 员工 |

### 考勤状态 (status)
| 值 | 说明 |
|----|------|
| NORMAL | 正常 |
| LATE | 迟到 |
| EARLY_LEAVE | 早退 |
| MISSING | 缺卡 |
| ABNORMAL | 异常 |

### 请假类型 (leave_type)
| 值 | 说明 |
|----|------|
| ANNUAL | 年假 |
| SICK | 病假 |
| PERSONAL | 事假 |
| MATERNITY | 产假 |
| PATERNITY | 陪产假 |
| OTHER | 其他 |

### 审批状态 (status)
| 值 | 说明 |
|----|------|
| PENDING | 待审批 |
| APPROVED | 已批准 |
| REJECTED | 已拒绝 |
| CANCELLED | 已取消 |

### 薪资状态 (status)
| 值 | 说明 |
|----|------|
| DRAFT | 草稿 |
| PUBLISHED | 已发布 |
| ADJUSTED | 已调整 |
| APPEALED | 申诉中 |

### 申诉类型 (appeal_type)
| 值 | 说明 |
|----|------|
| ATTENDANCE | 考勤申诉 |
| SALARY | 薪资申诉 |

---

## 常量配置

### 考勤规则
- **宽限时间**: ±5 分钟
- **迟到判定**: 签到时间 > 班次开始时间 + 5 分钟
- **早退判定**: 签退时间 < 班次结束时间 - 5 分钟
- **缺卡判定**: 无签到记录 或 无签退记录

### 薪资计算常量
| 常量 | 值 | 说明 |
|------|-----|------|
| DEFAULT_BASE_SALARY | 3000 | 默认基本工资（元） |
| DAYS_PER_MONTH | 21.75 | 月计薪天数 |
| HOURS_PER_DAY | 8 | 日工作小时数 |
| OVERTIME_RATE | 1.5 | 加班工资倍率 |
| LATE_DEDUCTION | 20 | 迟到扣款（元/次） |
| MISSING_DEDUCTION | 50 | 缺卡扣款（元/次） |
| GRACE_PERIOD_MINUTES | 5 | 考勤宽限期（分钟） |

---

## 错误码说明

| HTTP 状态码 | 说明 |
|------------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 注意事项

1. **日期格式**: 所有日期字段使用 `YYYY-MM-DD` 格式，日期时间使用 ISO 8601 格式
2. **分页**: 默认每页 20 条，最大 100 条
3. **权限**: 部分接口需要管理员权限
4. **薪资安全**: 薪资数据默认脱敏，需点击查看明文
5. **考勤宽限**: ±5 分钟内不算迟到/早退
