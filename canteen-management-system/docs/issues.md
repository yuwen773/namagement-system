# 问题记录

本文档记录项目开发过程中遇到的问题及解决方案。

---

## 2026-01-28

### 问题 1: 前端 API 请求路径重复 `/api`

**描述**: 前端请求后端时出现重复的 `/api` 路径，如 `/api/api/employees/`

**原因**:
- `request.js` 中 `baseURL: '/api'`
- `employee.js` 中 URL 又包含了 `/api` 前缀（如 `/api/employees/`）

**修复**:
移除 `employee.js` 中所有 URL 的 `/api` 前缀

**影响文件**:
- `frontend/src/api/employee.js`

**状态**: ✅ 已解决

---

### 问题 2: 后端视图缺少统一响应格式

**描述**:
部分后端视图的 `list`/`retrieve` 方法使用 DRF 默认返回格式，没有包装成 `{ code, message, data }` 统一格式，导致前端响应拦截器判断 `res.code` 为 `undefined` 时报错 `API 错误: undefined`

**原因**:
- `ShiftViewSet`、`ScheduleViewSet`、`ShiftSwapRequestViewSet` 只覆盖了 `create` 方法
- `SalaryRecordViewSet`、`AppealViewSet` 也缺少 `list`/`retrieve` 方法
- DRF 默认的 `list`/`retrieve` 返回数据，不包含 `code` 和 `message` 字段

**修复**:
为所有视图集添加 `list`、`retrieve`、`update`、`destroy` 方法，返回统一响应格式

**影响文件**:
- `backend/schedules/views.py` - `ShiftViewSet`、`ScheduleViewSet`、`ShiftSwapRequestViewSet`
- `backend/salaries/views.py` - `SalaryRecordViewSet`、`AppealViewSet`

**状态**: ✅ 已解决

---

### 问题 3: 后端分页响应格式与前端不匹配

**描述**:
后端使用 `get_paginated_response()` 时返回的格式与前端期望不一致

**原因**:
- 后端使用 `get_paginated_response({ code: 200, message: '...', data: serializer.data })`
- DRF 将整个字典放入 `results` 字段，返回格式变成：
  ```json
  {
    "count": 10,
    "results": {
      "code": 200,
      "message": "获取成功",
      "data": [...]
    }
  }
  ```
- 前端期望格式：
  ```json
  {
    "code": 200,
    "message": "获取成功",
    "data": {
      "count": 10,
      "results": [...]
    }
  }
  ```

**修复**:
移除 `get_paginated_response()` 调用，手动构建正确的分页响应格式

**影响文件**:
- `backend/attendance/views.py` - `list` 方法、`my_attendance` 方法
- `backend/leaves/views.py` - `list` 方法
- `backend/schedules/views.py` - `ScheduleViewSet.list`、`ShiftSwapRequestViewSet.list`、`my_requests`、`pending`
- `backend/salaries/views.py` - `SalaryRecordViewSet.list`、`AppealViewSet.list`、`my_salaries`、`pending_appeals`、`my_appeals`

**状态**: ✅ 已解决

---

### 问题 4: 前端员工列表数据结构不匹配

**描述**:
排班管理页面加载员工列表失败，显示"加载员工列表失败"

**原因**:
- `ScheduleManageView.vue` 中使用 `data.data.results` 期望分页格式
- 但 `employees` API 不支持分页，直接返回数组 `data: [...]`

**修复**:
将 `data.data.results` 改为 `data.data`

**影响文件**:
- `frontend/src/views/admin/ScheduleManageView.vue`

**状态**: ✅ 已解决

---

### 问题 5: Element Plus 组件显示英文

**描述**:
Element Plus 组件（如 `el-pagination`、`el-calendar`、`el-date-picker`）显示英文而非中文

**原因**:
- `main.js` 中注册 Element Plus 时未配置中文语言包

**修复**:
1. 导入 Element Plus 中文语言包：`import zhCn from 'element-plus/dist/locale/zh-cn.mjs'`
2. 注册时配置语言选项：`app.use(ElementPlus, { locale: zhCn })`

**影响文件**:
- `frontend/src/main.js`

**状态**: ✅ 已解决

---

### 问题 6: 排班管理页面显示英文

**描述**:
排班管理页面中岗位显示英文（如 "CHEF"）而非中文（如 "厨师"）

**原因**:
1. 前端使用了 `employee_position` 字段（返回英文枚举值）而非 `position_display`（返回中文显示值）
2. 后端 `ShiftSwapRequestSerializer` 缺少格式化的班次信息字段
3. 前端 `getShiftTagType` 函数未支持所有班次类型

**修复**:
1. 前端将 `employee_position` 改为 `position_display`
2. 后端添加 `original_schedule_info` 和 `target_schedule_info` 方法
3. 扩展前端班次类型映射，支持早餐班、中餐班、晚餐班、早中连班、中晚连班、夜宵班、行政班、保洁早班、保洁晚班

**影响文件**:
- `frontend/src/views/admin/ScheduleManageView.vue`
- `backend/schedules/serializers.py`

**状态**: ✅ 已解决

---

## 问题状态统计

| 状态 | 数量 |
|:-----|:-----|
| ✅ 已解决 | 6 |
| 🔄 进行中 | 0 |
| ⏳ 待处理 | 0 |
| ❌ 已关闭 | 0 |
