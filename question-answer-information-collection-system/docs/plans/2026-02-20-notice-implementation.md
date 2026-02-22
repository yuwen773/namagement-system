# 公告功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为问答信息采集系统添加公告功能，支持管理员发布公告，所有登录用户可查看

**Architecture:**
- 后端：新建 `apps.notices` 应用，使用 DRF ViewSet 实现 CRUD API
- 前端：新建公告管理页面 + 在导航栏集成消息图标弹窗
- 权限：管理员可增删改，普通用户只读

**Tech Stack:** Django 5.2 + DRF, Vue 3 + Element Plus

---

## Task 1: 创建 notices app 结构和模型

**Files:**
- Create: `backend/apps/notices/__init__.py`
- Create: `backend/apps/notices/apps.py`
- Create: `backend/apps/notices/models.py`
- Create: `backend/apps/notices/migrations/__init__.py`
- Modify: `backend/qa_project/settings.py:58` - 添加 `apps.notices.apps.NoticesConfig`

**Step 1: 创建 notices 目录和 __init__.py**

```python
# backend/apps/notices/__init__.py
default_app_config = 'apps.notices.apps.NoticesConfig'
```

**Step 2: 创建 apps.py**

```python
# backend/apps/notices/apps.py
from django.apps import AppConfig


class NoticesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notices"
    label = "notices"
    verbose_name = "公告管理"
```

**Step 3: 创建 models.py**

```python
# backend/apps/notices/models.py
from django.db import models


class Notice(models.Model):
    """公告模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告列表'
        ordering = ['-created_at']
        db_table = 'notices'

    def __str__(self):
        return self.title
```

**Step 4: 创建空的 migrations/__init__.py**

```python
# backend/apps/notices/migrations/__init__.py
```

**Step 5: 修改 settings.py 添加应用**

在 `INSTALLED_APPS` 末尾添加:
```python
"apps.notices.apps.NoticesConfig",
```

**Step 6: 生成迁移文件**

Run: `cd backend && python manage.py makemigrations notices`
Expected: 输出 "Migrations for 'notices': notices/migrations/0001_initial.py"

**Step 7: 执行迁移**

Run: `cd backend && python manage.py migrate`
Expected: 输出 "Apply migrations ...: notices, OK"

---

## Task 2: 实现 notices API (Serializer + ViewSet + URL)

**Files:**
- Create: `backend/apps/notices/serializers.py`
- Create: `backend/apps/notices/views.py`
- Create: `backend/apps/notices/urls.py`
- Modify: `backend/qa_project/urls.py` - 添加 include

**Step 1: 创建 serializers.py**

```python
# backend/apps/notices/serializers.py
from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    """公告序列化器"""
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
```

**Step 2: 创建 views.py**

```python
# backend/apps/notices/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notice
from .serializers import NoticeSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """仅管理员可写，普通用户可读"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'


class NoticeViewSet(viewsets.ModelViewSet):
    """公告 CRUD API"""
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """只返回启用的公告"""
        return Notice.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        """获取公告列表"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": 0, "data": serializer.data, "total": queryset.count()})

    def retrieve(self, request, *args, **kwargs):
        """获取公告详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 0, "data": serializer.data})

    def create(self, request, *args, **kwargs):
        """创建公告"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"code": 0, "data": serializer.data, "message": "创建成功"}, status=201)

    def update(self, request, *args, **kwargs):
        """更新公告"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"code": 0, "data": serializer.data, "message": "更新成功"})

    def destroy(self, request, *args, **kwargs):
        """删除公告"""
        instance = self.get_object()
        instance.delete()
        return Response({"code": 0, "message": "删除成功"})
```

**Step 3: 创建 urls.py**

```python
# backend/apps/notices/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet

router = DefaultRouter()
router.register(r'', NoticeViewSet, basename='notice')

urlpatterns = [
    path('', include(router.urls)),
]
```

**Step 4: 修改 qa_project/urls.py**

在 `urlpatterns` 末尾添加:
```python
# Notices API
path("api/notices/", include("apps.notices.urls")),
```

---

## Task 3: 创建前端 API 模块

**Files:**
- Create: `frontend/src/api/notices.js`

**Step 1: 创建 notices.js API 模块**

```javascript
// frontend/src/api/notices.js
import request from '@/utils/request'

export function getNoticeList(params) {
  return request.get('/api/notices/', { params })
}

export function getNoticeDetail(id) {
  return request.get(`/api/notices/${id}/`)
}

export function createNotice(data) {
  return request.post('/api/notices/', data)
}

export function updateNotice(id, data) {
  return request.patch(`/api/notices/${id}/`, data)
}

export function deleteNotice(id) {
  return request.delete(`/api/notices/${id}/`)
}
```

---

## Task 4: 创建管理员公告管理页面

**Files:**
- Create: `frontend/src/views/NoticeManagement.vue`
- Modify: `frontend/src/router/index.js` - 添加路由

**Step 1: 创建 NoticeManagement.vue**

参考 `UserManagement.vue` 的结构，创建一个类似的公告管理页面，包含：
- 标题：公告管理
- 表格列：ID、标题、创建时间、状态、操作
- 操作：编辑、删除
- 对话框：添加/编辑公告（标题、内容、是否启用）

**Step 2: 修改 router/index.js 添加路由**

```javascript
import NoticeManagement from '@/views/NoticeManagement.vue'

// 在路由数组中添加:
{
  path: '/notices',
  name: 'NoticeManagement',
  component: NoticeManagement,
  meta: { requiresAuth: true, roles: ['admin'], layout: 'admin', title: '公告管理' }
}
```

---

## Task 5: 在导航栏集成消息图标

**Files:**
- Modify: `frontend/src/components/AppLayout.vue`

**Step 1: 添加消息图标和弹窗**

在 AppLayout.vue 的顶部导航栏右侧（用户头像旁边）添加：
- 消息图标（SVG）
- 点击弹出 el-dialog 或 el-drawer
- 弹窗内显示公告列表（只读）

参考现有代码风格，与用户管理页面保持一致。

---

## Task 6: 测试验证

**Step 1: 后端测试**

Run: `cd backend && python manage.py test apps.notices --verbosity=2`
或手动测试 API:
- GET /api/notices/ - 应返回空列表
- POST /api/notices/ - 创建公告（需要 admin 角色）
- GET /api/notices/1/ - 查看详情
- PATCH /api/notices/1/ - 更新公告
- DELETE /api/notices/1/ - 删除公告

**Step 2: 前端测试**

Run: `cd frontend && npm run dev`
- 访问 /notices 页面（管理员）
- 访问 /dashboard，确认导航栏有消息图标
- 点击消息图标，弹窗显示公告列表

---

## Task 7: 提交代码

```bash
git add backend/apps/notices frontend/src/api/notices.js frontend/src/views/NoticeManagement.vue frontend/src/components/AppLayout.vue frontend/src/router/index.js docs/plans/2026-02-20-notice-design.md
git commit -m "feat: 添加公告功能

- 新增 notices 应用，支持 CRUD API
- 管理员可发布/编辑/删除公告
- 用户可在导航栏查看公告列表
- 权限：管理员读写，普通用户只读"

git push
```
