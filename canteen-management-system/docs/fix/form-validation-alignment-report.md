# 前后端表单校验对齐报告

**生成日期**: 2026-02-22

## 一、发现的问题及修复

### 问题 1: 员工管理 - id_card 字段

| 项目 | 问题 | 修复 |
|------|------|------|
| 前端 | id_card 无 required 校验 | ✅ 已添加 `required: true` |
| 后端 | required=True | 无需修改 |

**修复内容**:
- `frontend/src/views/admin/EmployeeManageView.vue`
- 添加 `required: true, message: '请输入身份证号'`

---

### 问题 2: 排班管理 - approval_remark 字段

| 项目 | 问题 | 修复 |
|------|------|------|
| 前端 | required=true | 无需修改 |
| 后端 | required=False | ✅ 已改为 required=True |

**修复内容**:
- `backend/schedules/serializers.py`
- `ShiftSwapApprovalSerializer.approval_remark`
- 添加自定义错误消息

```python
approval_remark = serializers.CharField(
    required=True,
    allow_blank=False,
    max_length=500,
    error_messages={
        'required': '审批意见不能为空',
        'blank': '审批意见不能为空',
        'max_length': '审批意见最多500个字符'
    }
)
```

---

### 问题 3: 请假管理 - leave_type 选项不一致

| 后端 | 前端 |
|------|------|
| SICK, PERSONAL, COMPENSATORY | ANNUAL, SICK, PERSONAL, MATERNITY, PATERNITY, OTHER |

**修复内容**:

1. 后端 `backend/leaves/models.py` - 添加前端使用的类型:
```python
class LeaveType(models.TextChoices):
    ANNUAL = 'ANNUAL', '年假'
    SICK = 'SICK', '病假'
    PERSONAL = 'PERSONAL', '事假'
    MATERNITY = 'MATERNITY', '产假'
    PATERNITY = 'PATERNITY', '陪产假'
    COMPENSATORY = 'COMPENSATORY', '调休'
    OTHER = 'OTHER', '其他'
```

2. 前端 `frontend/src/views/employee/LeaveView.vue` - 添加 COMPENSATORY 支持:
```javascript
const getLeaveTypeTagType = (type) => ({
    ANNUAL: 'success', SICK: 'danger', PERSONAL: 'warning',
    MATERNITY: 'info', PATERNITY: 'info', COMPENSATORY: 'warning', OTHER: 'info'
}[type] || 'info')
const getLeaveTypeLabel = (type) => ({
    ANNUAL: '年假', SICK: '病假', PERSONAL: '事假',
    MATERNITY: '产假', PATERNITY: '陪产假', COMPENSATORY: '调休', OTHER: '其他'
}[type] || type)
```

---

## 二、修复后的校验一致情况

| 模块 | 字段 | 前端 required | 后端 required | 状态 |
|------|------|--------------|--------------|------|
| employees | id_card | true | true | ✅ 一致 |
| schedules | approval_remark | true | true | ✅ 一致 |
| leaves | leave_type | - | - | ✅ 类型一致 |

---

## 三、注意事项

### 需要数据库迁移

修改 `backend/leaves/models.py` 后，需要执行数据库迁移：
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```
