# 后端必填字段汇总报告

**生成日期**: 2026-02-22

## 一、汇总表

| 模块 | 必填字段数 | 主要涉及的业务 |
|------|-----------|---------------|
| accounts | 4 | 登录、注册 |
| employees | 7 | 员工信息 |
| attendance | 5 | 考勤记录、统计 |
| leaves | 5+ | 请假申请 |
| salaries | 13+ | 薪资记录 |
| schedules | 4+ | 排班管理 |

---

## 二、各模块详细必填字段

### 1. accounts (账户模块)

#### LoginSerializer (登录)
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| username | CharField | 用户名不能为空 |
| password | CharField | 密码不能为空 |

#### RegisterSerializer (注册)
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| username | CharField | 用户名不能为空 |
| password | CharField | 密码不能为空 |

---

### 2. employees (员工模块)

#### EmployeeSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| name | CharField | 姓名不能为空 |
| phone | CharField | 手机号不能为空 |
| id_card | CharField | (DRF默认) |
| gender | ChoiceField | 性别不能为空 |
| position | ChoiceField | 职位不能为空 |
| entry_date | DateField | 入职日期不能为空 |
| status | ChoiceField | 状态不能为空 |

---

### 3. attendance (考勤模块)

#### AttendanceRecordSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| employee | ForeignKey | (DRF默认) |

#### AttendanceStatisticsSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| start_date | DateField | 开始日期不能为空 |
| end_date | DateField | 结束日期不能为空 |

#### AttendanceCorrectionSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| status | ChoiceField | (DRF默认) |
| correction_remark | CharField | (DRF默认) |

---

### 4. leaves (请假模块)

#### LeaveRequestSerializer / LeaveRequestCreateSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| employee | PrimaryKeyRelatedField | (DRF默认) |
| leave_type | CharField | (DRF默认) |
| start_time | DateTimeField | (DRF默认) |
| end_time | DateTimeField | (DRF默认) |
| reason | CharField | (DRF默认) |

#### LeaveRequestApprovalSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| approve | BooleanField | (DRF默认) |

---

### 5. salaries (薪资模块)

#### SalaryRecordSerializer / SalaryRecordCreateSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| employee | ForeignKey | (DRF默认) |
| year_month | CharField | (DRF默认) |
| base_salary | DecimalField | (DRF默认) |
| position_allowance | DecimalField | (DRF默认) |
| overtime_pay | DecimalField | (DRF默认) |
| deductions | DecimalField | (DRF默认) |
| work_days | IntegerField | (DRF默认) |
| late_count | IntegerField | (DRF默认) |
| missing_count | IntegerField | (DRF默认) |
| overtime_hours | DecimalField | (DRF默认) |
| status | CharField | (DRF默认) |
| remark | CharField | (DRF默认) |

#### SalaryGenerateSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| year_month | CharField | (DRF默认) |

#### SalaryAdjustSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| reason | CharField | 调整原因（必填） |

#### AppealSerializer / AppealCreateSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| appeal_type | CharField | (DRF默认) |
| employee | ForeignKey | (DRF默认) |
| target_id | IntegerField | (DRF默认) |
| reason | CharField | (DRF默认) |

#### AppealApprovalSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| approve | BooleanField | (DRF默认) |

---

### 6. schedules (排班模块)

#### BatchScheduleSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| employee_ids | ListField | 员工ID列表不能为空 |
| shift_id | IntegerField | 班次ID不能为空 |
| start_date | DateField | 开始日期不能为空 |
| end_date | DateField | 结束日期不能为空 |

#### CalendarViewSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| start_date | DateField | 开始日期不能为空 |
| end_date | DateField | 结束日期不能为空 |

#### ShiftSwapApprovalSerializer
| 字段名 | 类型 | 错误消息 |
|--------|------|----------|
| approve | BooleanField | (DRF默认) |

---

## 三、错误消息规范化情况

| 模块 | 自定义错误消息 | DRF默认错误消息 |
|------|--------------|----------------|
| accounts | ✅ 有 | 部分 |
| employees | ✅ 完善 | 部分 |
| attendance | ✅ 部分 | 部分 |
| leaves | ❌ 无 | 全部 |
| salaries | ❌ 无 | 全部 |
| schedules | ✅ 部分 | 部分 |

---

## 四、建议

1. **统一错误消息**: leaves 和 salaries 模块的 serializers 缺少自定义错误消息，建议补充
2. **前端表单验证**: 可根据此报告配置前端表单的必填校验规则
