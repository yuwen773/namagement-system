# 反馈功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为天猫宠物用品采集平台添加用户反馈功能，用户可提交问题/建议给管理员，管理员可查看和处理反馈。

**Architecture:** 创建独立的 feedback 应用，复用现有 users 应用的 User 模型，使用 DRF ViewSet 实现 REST API，前端使用 Element Plus 组件构建页面。

**Tech Stack:** Django 5.2 + DRF, Vue 3 + Element Plus

---

## 后端实现

### Task 1: 创建 Django feedback 应用

**Files:**
- Create: `backend/feedback/__init__.py`
- Create: `backend/feedback/apps.py`
- Create: `backend/feedback/models.py`
- Create: `backend/feedback/serializers.py`
- Create: `backend/feedback/views.py`
- Create: `backend/feedback/urls.py`
- Modify: `backend/tmall_project/settings.py:40-45` (添加 app 配置)
- Modify: `backend/tmall_project/urls.py:25-30` (添加路由)

**Step 1: 创建应用目录和基础文件**

```bash
mkdir -p backend/feedback
touch backend/feedback/__init__.py
```

**Step 2: 创建 apps.py**

```python
from django.apps import AppConfig

class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback'
    verbose_name = '反馈管理'
```

**Step 3: 创建 models.py**

```python
import uuid
from django.db import models
from users.models import User

class Feedback(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processed', '已处理'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    title = models.CharField(max_length=200, verbose_name='反馈标题')
    content = models.TextField(verbose_name='反馈内容')
    contact = models.CharField(max_length=100, blank=True, verbose_name='联系方式')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'feedback'
        verbose_name = '反馈'
        verbose_name_plural = '反馈'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
```

**Step 4: 注册应用到 settings.py**

在 INSTALLED_APPS 中添加:
```python
'feedback.apps.FeedbackConfig',
```

**Step 5: 执行数据库迁移**

```bash
cd backend
python manage.py makemigrations feedback
python manage.py migrate
```

---

### Task 2: 实现 Serializers

**Files:**
- Modify: `backend/feedback/serializers.py` (创建文件)

**Step 1: 创建 serializers.py**

```python
from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'user_username', 'title', 'content', 'contact', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']

class FeedbackListSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user_username', 'title', 'status', 'created_at']

class FeedbackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['status']
```

---

### Task 3: 实现 Views

**Files:**
- Modify: `backend/feedback/views.py` (创建文件)

**Step 1: 创建 views.py**

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackListSerializer, FeedbackUpdateSerializer
from users.permissions import IsAdmin

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return FeedbackListSerializer
        elif self.action in ['update', 'partial_update']:
            return FeedbackUpdateSerializer
        return FeedbackSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            # 管理员查看所有反馈，支持状态筛选
            status_filter = self.request.query_params.get('status')
            if status_filter:
                return Feedback.objects.filter(status=status_filter).order_by('-created_at')
            return Feedback.objects.all().order_by('-created_at')
        else:
            # 普通用户只能查看自己的反馈
            return Feedback.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my(self, request):
        """用户查看自己的反馈列表"""
        feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
        serializer = FeedbackListSerializer(feedbacks, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': feedbacks.count()
        })

    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def process(self, request, pk=None):
        """管理员标记为已处理"""
        feedback = self.get_object()
        feedback.status = 'processed'
        feedback.save()
        return Response({'code': 0, 'message': '已标记为已处理'})
```

---

### Task 4: 配置路由

**Files:**
- Modify: `backend/feedback/urls.py` (创建文件)
- Modify: `backend/tmall_project/urls.py` (添加路由)

**Step 1: 创建 urls.py**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackViewSet

router = DefaultRouter()
router.register(r'', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('api/feedback/', include(router.urls)),
]
```

**Step 2: 修改主路由 urls.py**

在 tmall_project/urls.py 添加:
```python
path('', include('feedback.urls')),
```

---

## 前端实现

### Task 5: 创建用户端反馈页面

**Files:**
- Create: `frontend/src/views/user/Feedback.vue`
- Modify: `frontend/src/router/index.js` (添加路由)
- Modify: `frontend/src/api/feedbackApi.js` (创建 API 文件)

**Step 1: 创建 API 文件**

```javascript
import axios from '@/utils/axios'

export const feedbackApi = {
  // 提交反馈
  create(data) {
    return axios.post('/api/feedback/', data)
  },
  // 我的反馈列表
  getMyList() {
    return axios.get('/api/feedback/my/')
  },
  // 管理员获取全部反馈
  getList(params) {
    return axios.get('/api/feedback/', { params })
  },
  // 管理员更新状态
  updateStatus(id, status) {
    return axios.patch(`/api/feedback/${id}/`, { status })
  },
  // 管理员删除
  delete(id) {
    return axios.delete(`/api/feedback/${id}/`)
  },
  // 标记为已处理
  process(id) {
    return axios.post(`/api/feedback/${id}/process/`)
  }
}
```

**Step 2: 创建用户端反馈页面**

创建 `frontend/src/views/user/Feedback.vue`，包含:
- 反馈提交表单（标题、内容、联系方式）
- 我的反馈列表（显示状态）
- 使用 Element Plus 的 el-form, el-input, el-button, el-table 组件

**Step 3: 添加路由**

在 router/index.js 用户端路由添加:
```javascript
{
  path: '/user/feedback',
  name: 'UserFeedback',
  component: () => import('@/views/user/Feedback.vue'),
  meta: { roles: ['user'] }
}
```

---

### Task 6: 创建管理端反馈管理页面

**Files:**
- Create: `frontend/src/views/admin/Feedback.vue`
- Modify: `frontend/src/router/index.js` (添加路由)

**Step 1: 创建管理端页面**

创建 `frontend/src/views/admin/Feedback.vue`，包含:
- 反馈列表（支持状态筛选）
- 查看详情对话框
- 标记已处理按钮
- 删除按钮
- 使用 Element Plus 组件

**Step 2: 添加路由**

在 router/index.js 管理端路由添加:
```javascript
{
  path: '/admin/feedback',
  name: 'AdminFeedback',
  component: () => import('@/views/admin/Feedback.vue'),
  meta: { roles: ['admin'] }
}
```

---

### Task 7: 添加页面入口

**Files:**
- Modify: `frontend/src/views/user/Profile.vue` (添加反馈入口按钮)
- Modify: `frontend/src/components/Layout/AdminLayout.vue` (添加侧边栏菜单)

**Step 1: 用户端入口**

在 Profile.vue 个人中心页面添加"意见反馈"按钮，链接到 /user/feedback

**Step 2: 管理端侧边栏**

在 AdminLayout.vue 侧边栏添加"反馈管理"菜单项

---

## 测试

### Task 8: 测试验证

**Step 1: 测试用户提交反馈**

1. 登录普通用户账号
2. 进入反馈页面
3. 填写标题、内容、联系方式
4. 提交成功后在列表中显示

**Step 2: 测试用户查看自己反馈**

1. 登录普通用户账号
2. 查看反馈列表，只能看到自己提交的

**Step 3: 测试管理员查看**

1. 登录管理员账号
2. 查看反馈列表，可以看到所有用户的反馈

**Step 4: 测试管理员处理**

1. 管理员标记反馈为"已处理"
2. 状态更新成功

**Step 5: 测试管理员删除**

1. 管理员删除反馈
2. 反馈被删除

---

## 实施顺序

1. Task 1: 创建 Django feedback 应用 + models
2. Task 2: 实现 Serializers
3. Task 3: 实现 Views
4. Task 4: 配置路由
5. Task 5: 创建用户端反馈页面
6. Task 6: 创建管理端反馈管理页面
7. Task 7: 添加页面入口
8. Task 8: 测试验证
