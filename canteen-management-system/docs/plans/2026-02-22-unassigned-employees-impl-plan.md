# 未关联员工列表接口实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 新增后端接口 `GET /api/employees/unassigned/`，返回未关联用户系统的员工档案列表，前端调用该接口填充用户管理中的员工下拉框。

**架构:** 在 employees 应用中添加新的 ViewSet，通过 action 方式实现，路由注册到 `/api/employees/unassigned/`。

**技术栈:** Django REST Framework, Vue 3

---

## 实现步骤

### Task 1: 后端 - 新增 ViewSet

**Files:**
- Modify: `backend/employees/views.py`
- Modify: `backend/employees/urls.py`

**Step 1: 在 employees/views.py 中添加 UnassignedEmployeeViewSet**

打开 `backend/employees/views.py`，在文件末尾添加新的 ViewSet：

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Exists, OuterRef
from accounts.models import User
from .models import EmployeeProfile
from .serializers import EmployeeProfileListSerializer


class UnassignedEmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """未关联用户系统的员工档案视图集"""

    def get_queryset(self):
        # 获取所有已关联的 employee_id
        assigned_ids = User.objects.exclude(
            employee_id__isnull=True
        ).values_list('employee_id', flat=True)

        # 返回未关联的员工档案
        return EmployeeProfile.objects.exclude(
            id__in=assigned_ids
        ).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EmployeeProfileListSerializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
```

**Step 2: 注册路由**

打开 `backend/employees/urls.py`，添加路由：

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeProfileViewSet, UnassignedEmployeeViewSet

router = DefaultRouter()
router.register(r'', EmployeeProfileViewSet, basename='employee')
router.register(r'unassigned', UnassignedEmployeeViewSet, basename='unassigned-employee')

urlpatterns = [
    path('', include(router.urls)),
]
```

**Step 3: 验证后端接口**

启动后端服务，访问 `http://localhost:8000/api/employees/unassigned/`，确认返回未关联员工的 JSON 数据。

---

### Task 2: 前端 - 新增 API 方法

**Files:**
- Modify: `frontend/src/api/employee.js` (或 employees.js)

**Step 1: 在 API 文件中添加方法**

打开 `frontend/src/api/` 目录，找到 employee 相关的 API 文件，添加：

```javascript
// 获取未关联用户系统的员工列表
export function getUnassignedEmployees() {
  return request({
    url: '/employees/unassigned/',
    method: 'get'
  })
}
```

---

### Task 3: 前端 - 修改 SystemManageView

**Files:**
- Modify: `frontend/src/views/admin/SystemManageView.vue`

**Step 1: 导入新 API 方法**

在文件顶部的 import 区域添加：

```javascript
import { getEmployeeList, getUnassignedEmployees, createUser, updateUser, deleteUser, getUserList } from '@/api'
```

**Step 2: 修改 loadEmployeeList 函数**

找到 `loadEmployeeList` 函数（约第 425 行），将：

```javascript
const res = await getEmployeeList({ page_size: 1000 })
if (res.code === 200) {
  employeeOptions.value = res.data.results || res.data
}
```

改为：

```javascript
const res = await getUnassignedEmployees()
if (res.code === 200) {
  employeeOptions.value = res.data
}
```

---

### Task 4: 验证

1. 启动后端服务：`python manage.py runserver`
2. 启动前端服务：`npm run dev`
3. 登录系统，进入用户管理
4. 点击"新增用户"，查看"关联员工"下拉框
5. 确认下拉框只显示未关联的员工档案

---

## 预期结果

- 后端接口 `/api/employees/unassigned/` 返回未关联员工的 JSON
- 前端用户管理中的"关联员工"下拉框只显示未关联的员工
- 已关联员工的档案不再出现在下拉框中
