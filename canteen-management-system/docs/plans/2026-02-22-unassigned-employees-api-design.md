# 未关联员工列表接口设计

**日期**: 2026-02-22

## 需求

在用户管理中关联员工时，下拉框应只显示**未关联**的员工档案。

## 设计

### 1. 后端接口

**接口**: `GET /api/employees/unassigned/`

**功能**: 返回未关联用户系统的员工档案列表

**响应示例**:
```json
{
  "code": 200,
  "message": "获取成功",
  "data": [
    { "id": 1, "name": "张三", "position": "CHEF", "position_display": "厨师" },
    { "id": 2, "name": "李四", "position": "CLEANER", "position_display": "保洁" }
  ]
}
```

### 2. 后端实现

在 `backend/employees/views.py` 中添加新的 ViewSet 或 action。

**逻辑**:
1. 获取所有 employee_profiles 记录
2. 获取所有已关联的 employee_id 列表（从 users 表）
3. 过滤掉已关联的员工

### 3. 前端修改

**文件**: `frontend/src/views/admin/SystemManageView.vue`

**修改**: 将 `loadUserList` 中获取员工列表的调用改为新接口

```javascript
// 改为调用未关联员工接口
const res = await getUnassignedEmployees()
if (res.code === 200) {
  employeeOptions.value = res.data
}
```

---

## 实现步骤

1. 后端：新增 `UnassignedEmployeeViewSet`
2. 后端：注册路由 `/api/employees/unassigned/`
3. 前端：新增 API 方法 `getUnassignedEmployees`
4. 前端：修改 `SystemManageView.vue` 调用新接口
