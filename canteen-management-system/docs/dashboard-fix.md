# 管理员工作台数据展示修复

> 修复日期：2026-01-29
> 问题：管理员工作台无法正确展示数据

---

## 问题分析

### 后端API问题

1. **日期过滤错误** - `backend/analytics/views.py:467`
   - ❌ 使用 `created_at__date=today` 统计今天**创建**的记录
   - ✅ 应使用 `schedule__work_date=today` 统计今天**工作日期**的记录

2. **实出勤人数统计错误** - `backend/analytics/views.py:469`
   - ❌ 使用 `.count()` 统计记录数（一个员工可能有多条记录）
   - ✅ 应使用 `.values('employee').distinct().count()` 统计员工数（去重）

3. **异常统计逻辑混乱** - `backend/analytics/views.py:483`
   - ❌ 包括 `LATE, EARLY_LEAVE, MISSING, ABNORMAL`
   - ✅ 只应包括 `EARLY_LEAVE, MISSING, ABNORMAL`（迟到已单独统计）

4. **待办考勤修正统计错误** - `backend/analytics/views.py:490`
   - ❌ 统计有更正备注的考勤记录
   - ✅ 应统计 `Appeal` 表中状态为 `PENDING` 的考勤申诉

### 前端数据映射错误

前端 `DashboardView.vue` 期望的字段名与后端返回的字段名不匹配：

| 前端期望字段 | 后端返回字段 | 状态 |
|-------------|-------------|------|
| `expected_attendance` | `should_attend` | ❌ 已修复 |
| `actual_attendance` | `present` | ❌ 已修复 |
| `today_leaves` | `leaves` | ❌ 已修复 |
| `today_abnormal` | `abnormal` | ❌ 已修复 |
| `monthly_late` | `late_count` | ❌ 已修复 |
| `monthly_salary` | 无对应字段 | ⚠️  暂时置空 |

---

## 修复内容

### 后端修复 (`backend/analytics/views.py`)

#### 1. 添加 Appeal 模型导入
```python
from salaries.models import SalaryRecord, Appeal  # 添加 Appeal
```

#### 2. 修复今日考勤统计（第465-473行）
```python
# 今日考勤统计（基于工作日期，而非创建日期）
today_attendance = AttendanceRecord.objects.filter(
    schedule__work_date=today  # 修改：使用工作日期
)
# 实出勤人数：基于员工去重
today_present = today_attendance.filter(
    status__in=["NORMAL", "LATE", "EARLY_LEAVE"]
).values("employee").distinct().count()  # 修改：去重统计
today_late = today_attendance.filter(status="LATE").count()
today_missing = today_attendance.filter(status="MISSING").count()
```

#### 3. 修复异常统计（第482-485行）
```python
# 今日异常考勤（不包括迟到，因为已单独统计）
today_abnormal = today_attendance.filter(
    status__in=["EARLY_LEAVE", "MISSING", "ABNORMAL"]  # 修改：移除LATE
).count()
```

#### 4. 修复待办统计（第487-494行）
```python
# 待办事项统计
pending_leaves = LeaveRequest.objects.filter(status="PENDING").count()
# 待处理的考勤申诉（Appeal中状态为PENDING的考勤申诉）
pending_attendance_appeals = Appeal.objects.filter(  # 修改：统计申诉
    appeal_type="ATTENDANCE",
    status="PENDING"
).count()
pending_salaries = SalaryRecord.objects.filter(status="DRAFT").count()
```

#### 5. 修复本月考勤统计（第502-509行）
```python
# 本月考勤统计（基于工作日期）
month_start = today.replace(day=1)
month_attendance = AttendanceRecord.objects.filter(
    schedule__work_date__gte=month_start,  # 修改：使用工作日期
    schedule__work_date__lte=today
)
month_late = month_attendance.filter(status="LATE").count()
month_missing = month_attendance.filter(status="MISSING").count()
```

### 前端修复 (`frontend/src/views/admin/DashboardView.vue`)

#### 1. 修复今日概览卡片（第48-56行）
```vue
<div class="card-stats">
  <div class="stat-item">
    <span class="stat-value">{{ overviewData.should_attend || 0 }}</span>
    <span class="stat-label">应到</span>
  </div>
  <div class="stat-divider">/</div>
  <div class="stat-item">
    <span class="stat-value stat-highlight">{{ overviewData.present || 0 }}</span>
    <span class="stat-label">实到</span>
  </div>
</div>
```

#### 2. 修复请假卡片（第65-70行）
```vue
<div class="card-stats">
  <div class="stat-item-full">
    <span class="stat-value-large">{{ overviewData.leaves || 0 }}</span>
    <span class="stat-label">人</span>
  </div>
</div>
```

#### 3. 修复异常卡片（第78-83行）
```vue
<div class="card-stats">
  <div class="stat-item-full">
    <span class="stat-value-large stat-warning">{{ overviewData.abnormal || 0 }}</span>
    <span class="stat-label">条</span>
  </div>
</div>
```

#### 4. 修复本月统计卡片（第127-148行）
```vue
<div class="monthly-card">
  <div class="monthly-icon">👥</div>
  <div class="monthly-content">
    <div class="monthly-value">{{ overviewData.total_employees || 0 }}</div>
    <div class="monthly-label">员工总数</div>
  </div>
</div>
<div class="monthly-card">
  <div class="monthly-icon">⏰</div>
  <div class="monthly-content">
    <div class="monthly-value">{{ overviewData.late_count || 0 }}</div>
    <div class="monthly-label">迟到次数</div>
  </div>
</div>
<div class="monthly-card">
  <div class="monthly-icon">💰</div>
  <div class="monthly-content">
    <div class="monthly-value">{{ formatSalary(overviewData.total_salary) }}</div>
    <div class="monthly-label">薪资支出</div>
  </div>
</div>
```

#### 5. 修复数据加载逻辑（第229-297行）
```javascript
const loadOverviewData = async () => {
  overviewLoading.value = true
  try {
    const response = await getOverviewStatistics()
    if (response.code === 200) {
      const data = response.data

      // 映射今日数据
      overviewData.value = {
        should_attend: data.today?.should_attend || 0,
        present: data.today?.present || 0,
        leaves: data.today?.leaves || 0,
        abnormal: data.today?.abnormal || 0,
        total_employees: data.overview?.total_employees || 0,
        late_count: data.month_attendance?.late_count || 0,
        missing_count: data.month_attendance?.missing_count || 0,
        total_salary: null // 薪资数据暂时为空
      }

      // 构建待办事项列表
      const todos = []
      const pending = data.pending || {}

      // 待审批请假
      if (pending.leaves > 0) {
        todos.push({
          id: 'pending-leaves',
          type: 'leave',
          typeName: '请假审批',
          title: `${pending.leaves} 条待审批请假申请`,
          time: '立即处理',
          data: { count: pending.leaves }
        })
      }

      // 待处理考勤修正
      if (pending.attendance_corrections > 0) {
        todos.push({
          id: 'pending-attendance',
          type: 'appeal',
          typeName: '考勤申诉',
          title: `${pending.attendance_corrections} 条待处理考勤申诉`,
          time: '立即处理',
          data: { count: pending.attendance_corrections }
        })
      }

      // 待生成薪资
      if (pending.salary_generation > 0) {
        todos.push({
          id: 'pending-salaries',
          type: 'salary',
          typeName: '薪资生成',
          title: `${pending.salary_generation} 份薪资待生成`,
          time: '立即处理',
          data: { count: pending.salary_generation }
        })
      }

      todoItems.value = todos
    }
  } catch (error) {
    console.error('加载总览数据失败:', error)
    ElMessage.error('加载总览数据失败')
  } finally {
    overviewLoading.value = false
  }
}
```

---

## 验证方法

### 1. 启动后端服务
```bash
cd backend
python manage.py runserver
```

### 2. 启动前端服务
```bash
cd frontend
npm run dev
```

### 3. 测试API
```bash
# 直接测试后端API
curl http://127.0.0.1:8000/api/analytics/overview/
```

### 4. 检查前端
- 打开浏览器访问 `http://localhost:5173`
- 登录管理员账号（用户名：`admin001`，密码：`123456`）
- 进入管理员工作台页面
- 检查以下数据是否正确显示：
  - 今日概览：应到/实到、今日请假、今日异常
  - 待办事项：请假审批、考勤申诉、薪资生成
  - 本月统计：员工总数、迟到次数

---

## 预期结果

修复后，管理员工作台应显示类似以下数据：

```json
{
  "code": 200,
  "message": "获取总览统计数据成功",
  "data": {
    "today": {
      "should_attend": 2,
      "present": 2,
      "late": 0,
      "missing": 0,
      "leaves": 1,
      "abnormal": 1,
      "attendance_rate": 100.0
    },
    "pending": {
      "leaves": 35,
      "attendance_corrections": 21,
      "salary_generation": 29
    },
    "overview": {
      "total_employees": 93,
      "total_positions": 6
    },
    "month_attendance": {
      "late_count": 7,
      "missing_count": 3
    }
  }
}
```

---

## 注意事项

1. **清除浏览器缓存**：修改后建议清除浏览器缓存或使用无痕模式访问
2. **检查数据**：确保测试数据已生成（运行 `python manage.py generate_test_data`）
3. **检查CORS**：确保后端 CORS 配置正确，前端可以正常访问 API
4. **薪资数据**：薪资支出字段暂时为空，需要后端添加相应计算逻辑

---

## 相关文件

### 后端文件
- `backend/analytics/views.py` - 统计分析视图（已修复）
- `backend/analytics/urls.py` - URL路由配置
- `backend/attendance/models.py` - 考勤模型
- `backend/salaries/models.py` - 薪资和申诉模型

### 前端文件
- `frontend/src/views/admin/DashboardView.vue` - 管理员工作台（已修复）
- `frontend/src/api/analytics.js` - 统计分析API
- `frontend/src/api/request.js` - 请求配置
- `frontend/vite.config.js` - Vite配置（代理设置）
