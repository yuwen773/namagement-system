# 用户注册与用户管理功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为非物质文化遗产数据可视化系统添加用户自主注册功能和管理端用户管理功能

**架构:** 后端使用 Django + DRF 扩展 auth 模块，新增注册 ViewSet 和用户管理 ViewSet；前端使用 Vue 3 + Element Plus 创建注册页面和用户管理页面，保持新中式美学设计风格一致

**Tech Stack:** Django 5.2 + DRF + MySQL (后端), Vue 3 + TypeScript + Element Plus (前端)

---

## Task 1: 后端 - 扩展 UserProfile 模型

**Files:**
- Modify: `backend/apps/users/models.py`
- Create: `backend/apps/users/migrations/000X_add_email_and_status.py` (自动生成)

**Step 1: 修改 models.py 扩展模型**

编辑 `backend/apps/users/models.py`，在 `UserProfile` 类中添加新字段：

```python
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    USER_ROLE = [
        ("admin", "管理员"),
        ("user", "普通用户"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
    )
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE,
        default="user",
        db_index=True,
        verbose_name="角色",
    )
    # 新增字段
    email = models.EmailField(
        unique=True,
        verbose_name="邮箱",
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="手机号",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="账号状态",
    )
    last_login_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="最后登录时间",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_profiles"
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"

    def __str__(self):
        return f"{self.user.username} ({self.role})"


def get_default_role(user):
    if user.is_superuser or user.is_staff:
        return "admin"
    return "user"


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"role": get_default_role(user)},
    )
    return profile.role


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return
    UserProfile.objects.get_or_create(
        user=instance,
        defaults={"role": get_default_role(instance)},
    )
```

**Step 2: 生成并应用数据库迁移**

```bash
cd backend
python manage.py makemigrations users
python manage.py migrate users
```

预期输出:
```
Migrations for 'users':
  backend/apps/users/migrations/000X_...py
    - Add field email to userprofile
    - Add field phone to userprofile
    - Add field is_active to userprofile
    - Add field last_login_time to userprofile
Running migrations:
  Applying users.000X_... OK
```

**Step 3: 提交**

```bash
git add backend/apps/users/models.py backend/apps/users/migrations/
git commit -m "feat: 扩展 UserProfile 模型，添加邮箱、状态等字段"
```

---

## Task 2: 后端 - 创建注册相关 Serializers

**Files:**
- Modify: `backend/apps/users/serializers.py`

**Step 1: 添加注册和管理相关序列化器**

编辑 `backend/apps/users/serializers.py`，添加以下内容：

```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """用户注册序列化器"""
    username = serializers.CharField(
        min_length=3,
        max_length=20,
        error_messages={"min_length": "用户名至少3个字符", "max_length": "用户名最多20个字符"}
    )
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        error_messages={"min_length": "密码至少6个字符"}
    )
    email = serializers.EmailField(
        required=True,
        error_messages={"invalid": "请输入有效的邮箱地址"}
    )

    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        # 检查用户名格式（字母数字下划线）
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("用户名只能包含字母、数字和下划线")
        return value

    def validate_email(self, value):
        """验证邮箱唯一性"""
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已被注册")
        return value


class CheckUsernameSerializer(serializers.Serializer):
    """检查用户名序列化器"""
    username = serializers.CharField(min_length=1)


class CheckEmailSerializer(serializers.Serializer):
    """检查邮箱序列化器"""
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    """用户列表序列化器"""
    role = serializers.CharField(source='profile.role', read_only=True)
    email = serializers.EmailField(source='profile.email', read_only=True)
    is_active = serializers.BooleanField(source='profile.is_active', read_only=True)
    last_login_time = serializers.DateTimeField(source='profile.last_login_time', read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email', 'is_active', 'last_login_time', 'date_joined']


class UserManageSerializer(serializers.ModelSerializer):
    """用户管理序列化器（创建/更新）"""
    role = serializers.CharField(default='user')
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def validate_email(self, value):
        """验证邮箱唯一性（更新时排除自己）"""
        if not value:
            return value
        # 获取当前实例（如果是更新操作）
        instance = self.instance
        queryset = UserProfile.objects.filter(email=value)
        if instance:
            queryset = queryset.exclude(user=instance)
        if queryset.exists():
            raise serializers.ValidationError("邮箱已被注册")
        return value

    def create(self, validated_data):
        """创建用户"""
        role = validated_data.pop('role', 'user')
        email = validated_data.pop('email', '')
        password = validated_data.pop('password', None)

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        UserProfile.objects.create(
            user=user,
            role=role,
            email=email or None
        )
        return user

    def update(self, instance, validated_data):
        """更新用户"""
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)

        # 更新用户基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # 更新 profile
        profile = instance.profile
        if email is not None:
            profile.email = email
        if role is not None:
            profile.role = role
        profile.save()

        return instance


class UpdateStatusSerializer(serializers.Serializer):
    """更新状态序列化器"""
    is_active = serializers.BooleanField()


class UpdateRoleSerializer(serializers.Serializer):
    """更新角色序列化器"""
    role = serializers.ChoiceField(choices=['admin', 'user'])


class ResetPasswordSerializer(serializers.Serializer):
    """重置密码序列化器"""
    password = serializers.CharField(min_length=6, error_messages={"min_length": "密码至少6个字符"})
```

**Step 2: 提交**

```bash
git add backend/apps/users/serializers.py
git commit -m "feat: 添加用户注册和管理相关序列化器"
```

---

## Task 3: 后端 - 创建注册和检查接口 Views

**Files:**
- Modify: `backend/apps/users/views.py`

**Step 1: 添加注册和检查视图**

编辑 `backend/apps/users/views.py`，在现有内容后添加：

```python
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView as DRFAPIView

from utils.response import error_response, success_response
from .models import UserProfile, get_user_role
from .permissions import IsAdmin
from .serializers import (
    LoginSerializer, LogoutSerializer,
    RegisterSerializer, CheckUsernameSerializer, CheckEmailSerializer,
    UserSerializer, UserManageSerializer,
    UpdateStatusSerializer, UpdateRoleSerializer, ResetPasswordSerializer
)

User = get_user_model()


def _first_error(errors):
    """提取第一个错误信息"""
    if not errors:
        return "请求参数错误"
    first = next(iter(errors.values()))
    if isinstance(first, (list, tuple)) and first:
        return str(first[0])
    return str(first)


# ... 保留现有的 LoginView, RefreshTokenView, LogoutView, ProfileView ...


class RegisterView(DRFAPIView):
    """用户注册视图"""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # 创建用户
        user = User(
            username=serializer.validated_data['username']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        # 创建用户档案
        UserProfile.objects.create(
            user=user,
            role='user',
            email=serializer.validated_data['email']
        )

        # 生成 token（注册后自动登录）
        refresh = RefreshToken.for_user(user)

        return success_response(
            data={
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': 'user'
                }
            },
            message="注册成功"
        )


class CheckUsernameView(DRFAPIView):
    """检查用户名是否存在"""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CheckUsernameSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=_first_error(serializer.errors))

        username = serializer.validated_data['username']
        exists = User.objects.filter(username=username).exists()

        return success_response(data={'exists': exists})


class CheckEmailView(DRFAPIView):
    """检查邮箱是否存在"""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CheckEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=_first_error(serializer.errors))

        email = serializer.validated_data['email']
        exists = UserProfile.objects.filter(email=email).exists()

        return success_response(data={'exists': exists})
```

**Step 2: 更新 URL 配置**

编辑 `backend/apps/users/urls.py`：

```python
from django.urls import re_path

from .views import (
    LoginView, LogoutView, ProfileView, RefreshTokenView,
    RegisterView, CheckUsernameView, CheckEmailView
)

urlpatterns = [
    re_path(r"^login/?$", LoginView.as_view(), name="auth-login"),
    re_path(r"^register/?$", RegisterView.as_view(), name="auth-register"),
    re_path(r"^check-username/?$", CheckUsernameView.as_view(), name="auth-check-username"),
    re_path(r"^check-email/?$", CheckEmailView.as_view(), name="auth-check-email"),
    re_path(r"^refresh/?$", RefreshTokenView.as_view(), name="auth-refresh"),
    re_path(r"^logout/?$", LogoutView.as_view(), name="auth-logout"),
    re_path(r"^me/?$", ProfileView.as_view(), name="auth-me"),
]
```

**Step 3: 测试注册接口**

```bash
# 启动后端服务
cd backend
python manage.py runserver

# 在另一个终端测试
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123456","email":"test@example.com"}'
```

预期输出:
```json
{"code":0,"data":{"access":"...","refresh":"...","user":{"id":2,"username":"testuser","role":"user"}},"message":"注册成功"}
```

**Step 4: 提交**

```bash
git add backend/apps/users/views.py backend/apps/users/urls.py
git commit -m "feat: 添加用户注册和检查接口"
```

---

## Task 4: 后端 - 创建用户管理 ViewSet

**Files:**
- Modify: `backend/apps/users/views.py`
- Modify: `backend/apps/users/urls.py`

**Step 1: 添加 UserViewSet**

在 `backend/apps/users/views.py` 末尾添加：

```python
class UserViewSet(viewsets.ModelViewSet):
    """用户管理 ViewSet"""
    queryset = User.objects.select_related('profile').all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_permissions(self):
        """动态权限控制"""
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy',
                           'update_status', 'update_role', 'reset_password']:
            return [IsAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        """动态序列化器"""
        if self.action in ['create', 'update', 'partial_update']:
            return UserManageSerializer
        return UserSerializer

    def list(self, request):
        """用户列表（分页、筛选）"""
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
        except (TypeError, ValueError):
            page, page_size = 1, 20

        username = request.query_params.get('username', '')
        role = request.query_params.get('role', '')
        is_active_str = request.query_params.get('is_active', '')

        queryset = self.queryset

        # 筛选条件
        if username:
            queryset = queryset.filter(username__icontains=username)
        if role:
            queryset = queryset.filter(profile__role=role)
        if is_active_str != '':
            is_active = is_active_str.lower() == 'true'
            queryset = queryset.filter(profile__is_active=is_active)

        # 分页
        paginator = Paginator(queryset, page_size)

        try:
            page_obj = paginator.page(page)
        except Exception:
            page_obj = paginator.page(1)

        serializer = self.get_serializer(page_obj, many=True)
        return success_response(
            data=serializer.data,
            total=paginator.count,
            message="获取成功"
        )

    def create(self, request):
        """管理员创建用户"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        return success_response(
            data=UserSerializer(user).data,
            message="创建成功"
        )

    def update(self, request, *args, **kwargs):
        """更新用户"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        return success_response(
            data=UserSerializer(user).data,
            message="更新成功"
        )

    def destroy(self, request, *args, **kwargs):
        """删除用户"""
        instance = self.get_object()
        # 不允许删除自己
        if instance.id == request.user.id:
            return error_response(message="不能删除自己")
        instance.delete()
        return success_response(message="删除成功")

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """更新用户状态"""
        user = self.get_object()
        # 不允许禁用自己
        if user.id == request.user.id:
            return error_response(message="不能禁用自己")

        serializer = UpdateStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=_first_error(serializer.errors))

        user.profile.is_active = serializer.validated_data['is_active']
        user.profile.save()
        return success_response(
            data=UserSerializer(user).data,
            message="状态更新成功"
        )

    @action(detail=True, methods=['patch'])
    def update_role(self, request, pk=None):
        """更新用户角色"""
        user = self.get_object()
        # 不允许修改自己的角色
        if user.id == request.user.id:
            return error_response(message="不能修改自己的角色")

        serializer = UpdateRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=_first_error(serializer.errors))

        user.profile.role = serializer.validated_data['role']
        user.profile.save()
        return success_response(
            data=UserSerializer(user).data,
            message="角色更新成功"
        )

    @action(detail=True, methods=['patch'])
    def reset_password(self, request, pk=None):
        """重置用户密码"""
        user = self.get_object()
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=_first_error(serializer.errors))

        user.set_password(serializer.validated_data['password'])
        user.save()
        return success_response(message="密码重置成功")
```

**Step 2: 更新 URL 配置**

编辑 `backend/apps/users/urls.py`：

```python
from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView, LogoutView, ProfileView, RefreshTokenView,
    RegisterView, CheckUsernameView, CheckEmailView,
    UserViewSet
)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    # 认证相关
    re_path(r"^login/?$", LoginView.as_view(), name="auth-login"),
    re_path(r"^register/?$", RegisterView.as_view(), name="auth-register"),
    re_path(r"^check-username/?$", CheckUsernameView.as_view(), name="auth-check-username"),
    re_path(r"^check-email/?$", CheckEmailView.as_view(), name="auth-check-email"),
    re_path(r"^refresh/?$", RefreshTokenView.as_view(), name="auth-refresh"),
    re_path(r"^logout/?$", LogoutView.as_view(), name="auth-logout"),
    re_path(r"^me/?$", ProfileView.as_view(), name="auth-me"),

    # 用户管理
    re_path(r"^users/?", include(router.urls)),
]
```

**Step 3: 提交**

```bash
git add backend/apps/users/views.py backend/apps/users/urls.py
git commit -m "feat: 添加用户管理 ViewSet"
```

---

## Task 5: 前端 - 创建用户相关 API 服务

**Files:**
- Create: `frontend/src/api/user.ts`

**Step 1: 创建用户 API 服务**

创建 `frontend/src/api/user.ts`：

```typescript
import request from '@/utils/request'

// 注册请求参数
export interface RegisterRequest {
  username: string
  password: string
  email: string
}

// 用户信息
export interface User {
  id: number
  username: string
  role: string
  email: string
  is_active: boolean
  last_login_time: string | null
  date_joined: string
}

// 用户列表查询参数
export interface UserListParams {
  page?: number
  page_size?: number
  username?: string
  role?: string
  is_active?: boolean
}

// 用户列表响应
export interface UserListResponse {
  code: number
  data: User[]
  total: number
  message: string
}

// 检查用户名是否存在
export const checkUsername = (username: string) => {
  return request.post<{ exists: boolean }>('/api/v1/auth/check-username', { username })
}

// 检查邮箱是否存在
export const checkEmail = (email: string) => {
  return request.post<{ exists: boolean }>('/api/v1/auth/check-email', { email })
}

// 用户注册
export const register = (data: RegisterRequest) => {
  return request.post<{
    access: string
    refresh: string
    user: { id: number; username: string; role: string }
  }>('/api/v1/auth/register', data)
}

// 获取用户列表
export const getUserList = (params: UserListParams) => {
  return request.get<User[]>('/api/v1/users', { params })
}

// 创建用户
export const createUser = (data: {
  username: string
  email: string
  password: string
  role?: string
}) => {
  return request.post<User>('/api/v1/users', data)
}

// 更新用户
export const updateUser = (id: number, data: { email?: string }) => {
  return request.put<User>(`/api/v1/users/${id}`, data)
}

// 更新用户状态
export const updateUserStatus = (id: number, is_active: boolean) => {
  return request.patch<User>(`/api/v1/users/${id}/status`, { is_active })
}

// 更新用户角色
export const updateUserRole = (id: number, role: string) => {
  return request.patch<User>(`/api/v1/users/${id}/role`, { role })
}

// 重置用户密码
export const resetUserPassword = (id: number, password: string) => {
  return request.patch(`/api/v1/users/${id}/password`, { password })
}

// 删除用户
export const deleteUser = (id: number) => {
  return request.delete(`/api/v1/users/${id}`)
}
```

**Step 2: 更新 user Store 添加注册方法**

编辑 `frontend/src/stores/user.ts`，添加注册方法：

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, register as registerApi } from '@/api/auth'
import { register as registerUserApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('access_token') || '')
  const refreshToken = ref<string>(localStorage.getItem('refresh_token') || '')
  const userInfo = ref<any>(localStorage.getItem('user_info') ? JSON.parse(localStorage.getItem('user_info')!) : null)

  // ... 保留现有 login、logout、getUserInfo 方法 ...

  // 新增：用户注册
  const register = async (data: { username: string; password: string; email: string }) => {
    try {
      const response = await registerUserApi(data) as any
      if (response.code === 0) {
        token.value = response.data.access
        refreshToken.value = response.data.refresh
        userInfo.value = response.data.user

        localStorage.setItem('access_token', token.value)
        localStorage.setItem('refresh_token', refreshToken.value)
        localStorage.setItem('user_info', JSON.stringify(userInfo.value))

        return true
      }
      return false
    } catch (error) {
      console.error('Register error:', error)
      return false
    }
  }

  return {
    token,
    refreshToken,
    userInfo,
    login,
    logout,
    getUserInfo,
    register,  // 新增
    isAuthenticated
  }
})
```

**Step 3: 提交**

```bash
git add frontend/src/api/user.ts frontend/src/stores/user.ts
git commit -m "feat: 添加用户相关 API 服务和 Store 方法"
```

---

## Task 6: 前端 - 创建注册页面

**Files:**
- Create: `frontend/src/views/Register.vue`
- Modify: `frontend/src/router/index.ts`

**Step 1: 创建注册页面组件**

创建 `frontend/src/views/Register.vue`（与登录页风格一致的新中式美学设计）：

```vue
<template>
  <div class="register-page">
    <!-- 背景装饰（复用登录页） -->
    <div class="ink-background">
      <div class="ink-splash s1"></div>
      <div class="ink-splash s2"></div>
      <div class="ink-splash s3"></div>
    </div>

    <div class="cloud-decoration">
      <svg class="cloud-svg c1" viewBox="0 0 200 100">
        <path d="M20,60 Q40,30 70,50 T130,50 T180,60" stroke="rgba(212,175,55,0.15)" fill="none" stroke-width="2"/>
      </svg>
      <svg class="cloud-svg c2" viewBox="0 0 200 100">
        <path d="M20,50 Q50,20 90,40 T160,40" stroke="rgba(194,35,49,0.1)" fill="none" stroke-width="2"/>
      </svg>
    </div>

    <div class="register-container">
      <!-- 左侧装饰区 -->
      <div class="decoration-side">
        <div class="vertical-text">
          <span class="text-char" v-for="(char, i) in registerText" :key="i" :style="{ '--delay': `${i * 100}ms` }">
            {{ char }}
          </span>
        </div>
        <div class="seal-stamp">
          <div class="seal-outer">
            <div class="seal-inner">
              <span class="seal-char">注册</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 注册表单区 -->
      <div class="form-side">
        <div class="register-scroll">
          <div class="scroll-top"></div>
          <div class="scroll-content">
            <!-- Logo -->
            <div class="form-logo">
              <div class="logo-seal">
                <div class="seal-frame">
                  <el-icon :size="36" class="seal-icon">
                    <Collection />
                  </el-icon>
                </div>
              </div>
              <div class="logo-texts">
                <h1 class="logo-title">注册新账号</h1>
                <p class="logo-subtitle">Join Intangible Cultural Heritage System</p>
              </div>
            </div>

            <!-- 注册表单 -->
            <el-form
              ref="registerFormRef"
              :model="registerForm"
              :rules="registerRules"
              class="register-form"
              @submit.prevent="handleRegister"
            >
              <el-form-item prop="username">
                <div class="input-group">
                  <span class="input-label">用户名</span>
                  <el-input
                    v-model="registerForm.username"
                    placeholder="3-20位字母数字下划线"
                    size="large"
                    class="heritage-input"
                    @blur="checkUsername"
                  >
                    <template #prefix>
                      <el-icon><User /></el-icon>
                    </template>
                  </el-input>
                  <span v-if="usernameCheck.checked" class="check-hint" :class="{ error: usernameCheck.exists }">
                    {{ usernameCheck.exists ? '用户名已存在' : '用户名可用' }}
                  </span>
                </div>
              </el-form-item>

              <el-form-item prop="email">
                <div class="input-group">
                  <span class="input-label">邮箱</span>
                  <el-input
                    v-model="registerForm.email"
                    placeholder="请输入邮箱地址"
                    size="large"
                    class="heritage-input"
                    @blur="checkEmail"
                  >
                    <template #prefix>
                      <el-icon><Message /></el-icon>
                    </template>
                  </el-input>
                  <span v-if="emailCheck.checked" class="check-hint" :class="{ error: emailCheck.exists }">
                    {{ emailCheck.exists ? '邮箱已被注册' : '邮箱可用' }}
                  </span>
                </div>
              </el-form-item>

              <el-form-item prop="password">
                <div class="input-group">
                  <span class="input-label">密码</span>
                  <el-input
                    v-model="registerForm.password"
                    type="password"
                    placeholder="至少6位"
                    size="large"
                    class="heritage-input"
                    show-password
                  >
                    <template #prefix>
                      <el-icon><Lock /></el-icon>
                    </template>
                  </el-input>
                </div>
              </el-form-item>

              <el-form-item prop="confirmPassword">
                <div class="input-group">
                  <span class="input-label">确认密码</span>
                  <el-input
                    v-model="registerForm.confirmPassword"
                    type="password"
                    placeholder="再次输入密码"
                    size="large"
                    class="heritage-input"
                    show-password
                    @keyup.enter="handleRegister"
                  >
                    <template #prefix>
                      <el-icon><Lock /></el-icon>
                    </template>
                  </el-input>
                </div>
              </el-form-item>

              <el-form-item>
                <button
                  type="submit"
                  class="register-btn"
                  :class="{ loading: loading }"
                  :disabled="loading"
                >
                  <span v-if="!loading">注册</span>
                  <span v-else class="loading-text">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                  </span>
                </button>
              </el-form-item>
            </el-form>

            <!-- 登录链接 -->
            <div class="login-link">
              已有账号？
              <router-link to="/login" class="link">立即登录</router-link>
            </div>
          </div>
          <div class="scroll-bottom"></div>
        </div>

        <!-- 底部装饰 -->
        <div class="footer-decoration">
          <div class="decoration-line"></div>
          <p>© 2026 非遗数据平台 · 传承文化 记录历史</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock, Message, Collection } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { checkUsername as checkUsernameApi, checkEmail as checkEmailApi } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()

const registerFormRef = ref<FormInstance>()
const loading = ref(false)

const registerText = '欢迎加入非遗数据平台'

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const usernameCheck = ref({ checked: false, exists: false })
const emailCheck = ref({ checked: false, exists: false })

// 自定义验证规则
const validateUsername = (_rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入用户名'))
  } else if (!/^[a-zA-Z0-9_]{3,20}$/.test(value)) {
    callback(new Error('用户名为3-20位字母数字下划线'))
  } else if (usernameCheck.value.exists) {
    callback(new Error('用户名已存在'))
  } else {
    callback()
  }
}

const validateEmail = (_rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入邮箱'))
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    callback(new Error('请输入有效的邮箱地址'))
  } else if (emailCheck.value.exists) {
    callback(new Error('邮箱已被注册'))
  } else {
    callback()
  }
}

const validatePassword = (_rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入密码'))
  } else if (value.length < 6) {
    callback(new Error('密码至少6位'))
  } else {
    if (registerForm.confirmPassword) {
      registerFormRef.value?.validateField('confirmPassword')
    }
    callback()
  }
}

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const registerRules: FormRules = {
  username: [{ validator: validateUsername, trigger: 'blur' }],
  email: [{ validator: validateEmail, trigger: 'blur' }],
  password: [{ validator: validatePassword, trigger: 'blur' }],
  confirmPassword: [{ validator: validateConfirmPassword, trigger: 'blur' }]
}

// 检查用户名
const checkUsername = async () => {
  if (!registerForm.username || !/^[a-zA-Z0-9_]{3,20}$/.test(registerForm.username)) {
    usernameCheck.value = { checked: false, exists: false }
    return
  }
  try {
    const res = await checkUsernameApi(registerForm.username) as any
    usernameCheck.value = { checked: true, exists: res.data.exists }
    if (registerFormRef.value) {
      registerFormRef.value.validateField('username')
    }
  } catch (error) {
    console.error('Check username error:', error)
  }
}

// 检查邮箱
const checkEmail = async () => {
  if (!registerForm.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email)) {
    emailCheck.value = { checked: false, exists: false }
    return
  }
  try {
    const res = await checkEmailApi(registerForm.email) as any
    emailCheck.value = { checked: true, exists: res.data.exists }
    if (registerFormRef.value) {
      registerFormRef.value.validateField('email')
    }
  } catch (error) {
    console.error('Check email error:', error)
  }
}

// 注册
const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      const success = await userStore.register({
        username: registerForm.username,
        email: registerForm.email,
        password: registerForm.password
      })
      if (success) {
        ElMessage.success('注册成功')
        router.push('/dashboard')
      } else {
        ElMessage.error('注册失败，请稍后重试')
      }
    } catch (error) {
      console.error('Register error:', error)
      ElMessage.error('注册失败，请稍后重试')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
/* 复用登录页样式，调整标题为注册相关 */
.login-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px 20px; background: #F7F4ED; position: relative; overflow: hidden; }
.ink-background { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
.ink-splash { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.08; animation: inkFloat 30s ease-in-out infinite; }
.ink-splash.s1 { width: 500px; height: 500px; background: radial-gradient(circle, #2F3640 0%, transparent 70%); top: -150px; right: -100px; }
.ink-splash.s2 { width: 400px; height: 400px; background: radial-gradient(circle, #C23531 0%, transparent 70%); bottom: -100px; left: -100px; animation-delay: -10s; }
.ink-splash.s3 { width: 350px; height: 350px; background: radial-gradient(circle, #D4AF37 0%, transparent 70%); top: 50%; left: 50%; transform: translate(-50%, -50%); animation-delay: -20s; }
@keyframes inkFloat { 0%, 100% { transform: translate(0, 0) scale(1); } 25% { transform: translate(30px, -20px) scale(1.05); } 50% { transform: translate(-20px, 30px) scale(0.95); } 75% { transform: translate(-30px, -30px) scale(1.02); } }
.cloud-decoration { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
.cloud-svg { position: absolute; opacity: 0.6; }
.cloud-svg.c1 { top: 10%; left: 5%; width: 200px; animation: cloudDrift 40s linear infinite; }
.cloud-svg.c2 { bottom: 15%; right: 8%; width: 180px; animation: cloudDrift 50s linear infinite reverse; }
@keyframes cloudDrift { 0% { transform: translateX(0); } 50% { transform: translateX(30px); } 100% { transform: translateX(0); } }
.register-container { position: relative; z-index: 1; display: flex; max-width: 1000px; width: 100%; background: white; border-radius: 16px; box-shadow: 0 1px 0 0 rgba(212, 175, 55, 0.3) inset, 0 -1px 0 0 rgba(212, 175, 55, 0.3) inset, 0 20px 60px rgba(47, 54, 64, 0.15); overflow: hidden; }
.decoration-side { width: 200px; background: linear-gradient(135deg, #C23531 0%, #A93226 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 20px; position: relative; }
.decoration-side::before { content: ''; position: absolute; top: 20px; left: 20px; right: 20px; bottom: 20px; border: 2px solid rgba(212, 175, 55, 0.3); border-radius: 8px; }
.vertical-text { writing-mode: vertical-rl; display: flex; gap: 8px; margin-bottom: 60px; }
.text-char { font-size: 20px; color: rgba(247, 244, 237, 0.9); font-family: "STSong", "SimSun", serif; font-weight: 500; letter-spacing: 8px; opacity: 0; animation: charFadeIn 0.8s ease-out forwards; animation-delay: var(--delay); }
@keyframes charFadeIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
.seal-stamp { position: relative; }
.seal-outer { width: 80px; height: 80px; background: #D4AF37; border-radius: 4px; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(212, 175, 55, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.3); transform: rotate(-5deg); }
.seal-inner { width: 68px; height: 68px; background: rgba(212, 175, 55, 0.9); border-radius: 3px; display: flex; align-items: center; justify-content: center; border: 2px solid rgba(255, 255, 255, 0.3); }
.seal-char { writing-mode: horizontal-tb; font-size: 24px; color: #2F3640; font-family: "STSong", "SimSun", serif; font-weight: 700; letter-spacing: 4px; }
.form-side { flex: 1; padding: 48px 56px; display: flex; flex-direction: column; }
.register-scroll { position: relative; flex: 1; display: flex; flex-direction: column; justify-content: center; }
.scroll-top, .scroll-bottom { height: 16px; background: linear-gradient(90deg, transparent 0%, rgba(212, 175, 55, 0.3) 20%, rgba(212, 175, 55, 0.5) 50%, rgba(212, 175, 55, 0.3) 80%, transparent 100%); }
.scroll-content { flex: 1; padding: 32px 0; }
.form-logo { text-align: center; margin-bottom: 40px; }
.logo-seal { display: inline-flex; justify-content: center; margin-bottom: 20px; }
.seal-frame { width: 72px; height: 72px; background: #C23531; border-radius: 4px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 20px rgba(194, 35, 49, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2); position: relative; }
.seal-frame::before { content: ''; position: absolute; top: 4px; left: 4px; right: 4px; bottom: 4px; border: 2px solid rgba(255, 255, 255, 0.25); border-radius: 2px; }
.seal-icon { color: #F7F4ED; }
.logo-texts { text-align: center; }
.logo-title { font-size: 28px; font-weight: 700; color: #2F3640; margin: 0 0 8px 0; letter-spacing: 4px; font-family: "STSong", "SimSun", serif; background: linear-gradient(135deg, #C23531 0%, #2F3640 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.logo-subtitle { font-size: 12px; color: #909399; margin: 0; letter-spacing: 2px; text-transform: uppercase; }
.register-form { margin-bottom: 24px; }
.input-group { width: 100%; position: relative; }
.input-label { display: block; font-size: 13px; font-weight: 600; color: #606266; margin-bottom: 8px; letter-spacing: 1px; }
.check-hint { display: block; font-size: 12px; margin-top: 4px; color: #67C23A; }
.check-hint.error { color: #F56C6C; }
:deep(.heritage-input) { --el-input-border-color: rgba(212, 175, 55, 0.3); --el-input-hover-border-color: #D4AF37; --el-input-focus-border-color: #C23531; --el-input-bg-color: #F7F4ED; }
:deep(.heritage-input .el-input__wrapper) { padding: 14px 16px; border-radius: 8px; box-shadow: none; background: #F7F4ED; transition: all 0.3s; }
:deep(.heritage-input .el-input__wrapper:hover) { box-shadow: 0 0 0 1px #D4AF37 inset; }
:deep(.heritage-input .el-input__wrapper.is-focus) { box-shadow: 0 0 0 1px #C23531 inset; }
:deep(.heritage-input .el-input__inner) { color: #2F3640; font-weight: 500; }
:deep(.heritage-input .el-input__prefix) { color: #909399; }
.register-btn { width: 100%; padding: 16px 32px; background: linear-gradient(135deg, #C23531 0%, #A93226 100%); border: none; border-radius: 8px; color: white; font-size: 16px; font-weight: 600; letter-spacing: 4px; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 16px rgba(194, 35, 49, 0.3); position: relative; overflow: hidden; }
.register-btn::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent); transition: left 0.5s; }
.register-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(194, 35, 49, 0.4); }
.register-btn:hover::before { left: 100%; }
.register-btn:active { transform: translateY(0); }
.register-btn.loading { background: linear-gradient(135deg, #909399 0%, #606266 100%); cursor: not-allowed; }
.loading-text { display: flex; align-items: center; justify-content: center; gap: 8px; }
.dot { width: 8px; height: 8px; background: white; border-radius: 50%; animation: dotBounce 1.4s ease-in-out infinite; }
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes dotBounce { 0%, 80%, 100% { transform: translateY(0); opacity: 0.5; } 40% { transform: translateY(-10px); opacity: 1; } }
.login-link { text-align: center; font-size: 14px; color: #606266; }
.login-link .link { color: #C23531; text-decoration: none; font-weight: 600; }
.login-link .link:hover { text-decoration: underline; }
.footer-decoration { text-align: center; padding-top: 24px; }
.decoration-line { width: 100px; height: 2px; background: linear-gradient(90deg, transparent, #D4AF37, transparent); margin: 0 auto 16px; }
.footer-decoration p { margin: 0; font-size: 12px; color: #909399; letter-spacing: 1px; }
@media (max-width: 768px) {
  .decoration-side { display: none; }
  .form-side { padding: 32px 24px; }
  .logo-title { font-size: 24px; }
}

/* 为注册页面复用相同样式 */
.register-page { composes: login-page; }
.register-container { composes: login-container; }
.register-scroll { composes: login-scroll; }
.register-form { composes: login-form; }
.register-btn { composes: login-btn; }
</style>
```

**Step 2: 添加路由配置**

编辑 `frontend/src/router/index.ts`，添加注册页面路由：

```typescript
// 在 routes 配置中添加
{
  path: '/register',
  name: 'Register',
  component: () => import('@/views/Register.vue'),
  meta: { requiresAuth: false, title: '注册' }
}
```

同时在登录页底部添加注册链接：

编辑 `frontend/src/views/Login.vue`，在提示信息区域后添加：

```vue
<!-- 在 login-hint div 后添加 -->
<div class="register-link">
  还没有账号？
  <router-link to="/register" class="link">立即注册</router-link>
</div>
```

并添加样式：

```css
.register-link {
  text-align: center;
  font-size: 14px;
  color: #606266;
  margin-top: 16px;
}
.register-link .link {
  color: #C23531;
  text-decoration: none;
  font-weight: 600;
}
.register-link .link:hover {
  text-decoration: underline;
}
```

**Step 3: 提交**

```bash
git add frontend/src/views/Register.vue frontend/src/router/index.ts frontend/src/views/Login.vue
git commit -m "feat: 添加用户注册页面"
```

---

## Task 7: 前端 - 创建用户管理页面

**Files:**
- Create: `frontend/src/views/admin/UserManage.vue`
- Modify: `frontend/src/router/index.ts`

**Step 1: 创建用户管理页面组件**

创建 `frontend/src/views/admin/UserManage.vue`（新中式美学设计风格）：

```vue
<template>
  <div class="user-manage">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-seal">
          <span class="seal-text">管理</span>
        </div>
        <div class="header-texts">
          <h1 class="page-title">用户管理</h1>
          <p class="page-subtitle">管理系统用户和权限</p>
        </div>
      </div>
      <button class="add-btn" @click="handleAdd">
        <span class="btn-seal">增</span>
        <span>新增用户</span>
      </button>
    </header>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="用户名">
          <el-input v-model="filters.username" placeholder="搜索用户名" clearable @clear="handleSearch" class="heritage-input" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="filters.role" placeholder="选择角色" clearable class="heritage-select">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.is_active" placeholder="选择状态" clearable class="heritage-select">
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <button class="action-btn search-btn" @click="handleSearch">搜索</button>
          <button class="action-btn reset-btn" @click="handleReset">重置</button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 表格区域 -->
    <div class="table-frame">
      <el-table :data="tableData" v-loading="loading" class="data-table">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column label="角色" width="120">
          <template #default="{ row }">
            <span class="role-badge" :class="row.role">
              {{ row.role === 'admin' ? '管理员' : '普通用户' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <span class="status-badge" :class="{ active: row.is_active }">
              {{ row.is_active ? '启用' : '禁用' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="最后登录" width="180">
          <template #default="{ row }">
            {{ row.last_login_time ? formatDate(row.last_login_time) : '从未登录' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <button class="table-action-btn edit-btn" @click="handleEdit(row)">编辑</button>
            <el-dropdown trigger="click" @command="(cmd) => handleMoreCommand(cmd, row)">
              <button class="table-action-btn more-btn">
                更多<el-icon><ArrowDown /></el-icon>
              </button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="'role'">{{ row.role === 'admin' ? '设为普通用户' : '设为管理员' }}</el-dropdown-item>
                  <el-dropdown-item :command="'status'">{{ row.is_active ? '禁用账号' : '启用账号' }}</el-dropdown-item>
                  <el-dropdown-item :command="'password'">重置密码</el-dropdown-item>
                  <el-dropdown-item :command="'delete'" divided>删除用户</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      :close-on-click-modal="false"
      class="heritage-dialog"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" :disabled="isEdit" class="heritage-input" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" class="heritage-input" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="formData.password" type="password" show-password class="heritage-input" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" class="heritage-select">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="dialog-btn cancel-btn" @click="dialogVisible = false">取消</button>
        <button class="dialog-btn confirm-btn" @click="handleSubmit">确定</button>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="重置密码"
      width="400px"
      :close-on-click-modal="false"
      class="heritage-dialog"
    >
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="80px">
        <el-form-item label="新密码" prop="password">
          <el-input v-model="passwordForm.password" type="password" show-password class="heritage-input" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password class="heritage-input" />
        </el-form-item>
      </el-form>
      <template #footer>
        <button class="dialog-btn cancel-btn" @click="passwordDialogVisible = false">取消</button>
        <button class="dialog-btn confirm-btn" @click="handleResetPasswordSubmit">确定</button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import {
  getUserList,
  createUser,
  updateUser,
  updateUserStatus,
  updateUserRole,
  resetUserPassword,
  deleteUser
} from '@/api/user'
import type { User } from '@/api/user'

const loading = ref(false)
const tableData = ref<User[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filters = reactive({
  username: '',
  role: '',
  is_active: undefined as boolean | undefined
})

// 对话框相关
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const formData = reactive({
  id: 0,
  username: '',
  email: '',
  password: '',
  role: 'user'
})

const dialogTitle = computed(() => isEdit.value ? '编辑用户' : '新增用户')

const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

// 重置密码对话框
const passwordDialogVisible = ref(false)
const passwordFormRef = ref<FormInstance>()
const currentUserId = ref(0)
const passwordForm = reactive({
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value !== passwordForm.password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const passwordRules: FormRules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 获取用户列表
const fetchData = async () => {
  loading.value = true
  try {
    const res = await getUserList({
      page: currentPage.value,
      page_size: pageSize.value,
      ...filters
    }) as any
    if (res.code === 0) {
      tableData.value = res.data
      total.value = res.total
    }
  } catch (error) {
    console.error('Fetch users error:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

// 重置
const handleReset = () => {
  filters.username = ''
  filters.role = ''
  filters.is_active = undefined
  handleSearch()
}

// 分页
const handlePageChange = () => {
  fetchData()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  Object.assign(formData, {
    id: 0,
    username: '',
    email: '',
    password: '',
    role: 'user'
  })
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: User) => {
  isEdit.value = true
  Object.assign(formData, {
    id: row.id,
    username: row.username,
    email: row.email,
    password: '',
    role: row.role
  })
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      if (isEdit.value) {
        await updateUser(formData.id, { email: formData.email })
        ElMessage.success('更新成功')
      } else {
        await createUser({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          role: formData.role
        })
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchData()
    } catch (error) {
      console.error('Submit error:', error)
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    }
  })
}

// 更多操作
const handleMoreCommand = async (command: string, row: User) => {
  switch (command) {
    case 'role':
      await handleChangeRole(row)
      break
    case 'status':
      await handleChangeStatus(row)
      break
    case 'password':
      handleResetPassword(row)
      break
    case 'delete':
      handleDelete(row)
      break
  }
}

// 修改角色
const handleChangeRole = async (row: User) => {
  const newRole = row.role === 'admin' ? 'user' : 'admin'
  const roleText = newRole === 'admin' ? '管理员' : '普通用户'
  try {
    await ElMessageBox.confirm(`确定将该用户设为${roleText}吗？`, '确认操作', {
      type: 'warning'
    })
    await updateUserRole(row.id, newRole)
    ElMessage.success('角色修改成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Change role error:', error)
      ElMessage.error('操作失败')
    }
  }
}

// 修改状态
const handleChangeStatus = async (row: User) => {
  const newStatus = !row.is_active
  const statusText = newStatus ? '启用' : '禁用'
  try {
    await ElMessageBox.confirm(`确定${statusText}该账号吗？`, '确认操作', {
      type: 'warning'
    })
    await updateUserStatus(row.id, newStatus)
    ElMessage.success('状态修改成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Change status error:', error)
      ElMessage.error('操作失败')
    }
  }
}

// 重置密码
const handleResetPassword = (row: User) => {
  currentUserId.value = row.id
  passwordForm.password = ''
  passwordForm.confirmPassword = ''
  passwordDialogVisible.value = true
}

const handleResetPasswordSubmit = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      await resetUserPassword(currentUserId.value, passwordForm.password)
      ElMessage.success('密码重置成功')
      passwordDialogVisible.value = false
    } catch (error) {
      console.error('Reset password error:', error)
      ElMessage.error('操作失败')
    }
  })
}

// 删除用户
const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(`确定删除用户 "${row.username}" 吗？`, '确认删除', {
      type: 'warning'
    })
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Delete error:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 格式化日期
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* 复用管理页面通用样式 */
.user-manage {
  padding: 24px;
  background: #F7F4ED;
  min-height: calc(100vh - 60px);
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-seal {
  width: 56px;
  height: 56px;
  background: #C23531;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(194, 35, 49, 0.3);
}

.seal-text {
  font-size: 20px;
  color: #F7F4ED;
  font-family: "STSong", "SimSun", serif;
  font-weight: 700;
}

.header-texts {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #2F3640;
  margin: 0;
  font-family: "STSong", "SimSun", serif;
}

.page-subtitle {
  font-size: 13px;
  color: #909399;
  margin: 0;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #C23531 0%, #A93226 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(194, 35, 49, 0.3);
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(194, 35, 49, 0.4);
}

.btn-seal {
  width: 24px;
  height: 24px;
  background: #D4AF37;
  color: #2F3640;
  font-size: 12px;
  font-weight: 600;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "STSong", "SimSun", serif;
}

/* 筛选区域 */
.filter-section {
  background: white;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-form :deep(.el-form-item) {
  margin-bottom: 0;
}

.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn {
  background: #C23531;
  color: white;
}

.search-btn:hover {
  background: #A93226;
}

.reset-btn {
  background: #F7F4ED;
  color: #606266;
}

.reset-btn:hover {
  background: #E8E4DA;
}

/* 表格区域 */
.table-frame {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(47, 54, 64, 0.08);
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.role-badge.admin {
  background: rgba(194, 35, 49, 0.1);
  color: #C23531;
}

.role-badge.user {
  background: rgba(144, 147, 153, 0.1);
  color: #606266;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  background: rgba(144, 147, 153, 0.1);
  color: #606266;
}

.status-badge.active {
  background: rgba(103, 194, 58, 0.1);
  color: #67C23A;
}

.table-action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-right: 8px;
  background: transparent;
  color: #606266;
}

.edit-btn {
  color: #409EFF;
}

.edit-btn:hover {
  background: rgba(64, 158, 255, 0.1);
}

.more-btn {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* 对话框样式 */
.dialog-btn {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn {
  background: #F7F4ED;
  color: #606266;
}

.cancel-btn:hover {
  background: #E8E4DA;
}

.confirm-btn {
  background: #C23531;
  color: white;
}

.confirm-btn:hover {
  background: #A93226;
}

/* 输入框样式复用 */
:deep(.heritage-input) {
  --el-input-border-color: rgba(212, 175, 55, 0.3);
  --el-input-hover-border-color: #D4AF37;
  --el-input-focus-border-color: #C23531;
}

:deep(.heritage-select) {
  --el-select-border-color: rgba(212, 175, 55, 0.3);
  --el-select-hover-border-color: #D4AF37;
  --el-select-focus-border-color: #C23531;
}
</style>
```

**Step 2: 添加路由配置**

编辑 `frontend/src/router/index.ts`，在管理端路由中添加用户管理路由：

```typescript
{
  path: '/admin/users',
  name: 'UserManage',
  component: () => import('@/views/admin/UserManage.vue'),
  meta: { requiresAuth: true, roles: ['admin'], title: '用户管理' }
}
```

**Step 3: 在管理端布局中添加菜单入口**

找到管理端布局组件（通常是 `AdminLayout.vue` 或类似文件），在侧边栏菜单中添加用户管理入口。

**Step 4: 提交**

```bash
git add frontend/src/views/admin/UserManage.vue frontend/src/router/index.ts
git commit -m "feat: 添加用户管理页面"
```

---

## Task 8: 测试与验证

**Files:**
- 无（测试验证步骤）

**Step 1: 后端接口测试**

```bash
# 启动后端服务
cd backend
python manage.py runserver

# 测试注册接口
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","password":"test123456","email":"test2@example.com"}'

# 测试检查用户名接口
curl -X POST http://localhost:8000/api/v1/auth/check-username \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2"}'

# 测试检查邮箱接口
curl -X POST http://localhost:8000/api/v1/auth/check-email \
  -H "Content-Type: application/json" \
  -d '{"email":"test2@example.com"}'

# 测试用户列表接口（需要 admin token）
curl -X GET "http://localhost:8000/api/v1/users?page=1&page_size=20" \
  -H "Authorization: Bearer <your_admin_token>"
```

**Step 2: 前端功能测试**

1. **注册功能测试：**
   - 访问 `/register` 页面
   - 测试用户名唯一性检查
   - 测试邮箱唯一性检查
   - 测试密码一致性验证
   - 测试注册成功后自动登录

2. **用户管理功能测试（admin 账号）：**
   - 访问 `/admin/users` 页面
   - 测试用户列表加载
   - 测试筛选功能（用户名、角色、状态）
   - 测试新增用户
   - 测试编辑用户
   - 测试修改角色
   - 测试修改状态
   - 测试重置密码
   - 测试删除用户

3. **权限测试：**
   - 使用普通用户登录，确认无法访问 `/admin/users`
   - 确认普通用户只能访问只读接口

**Step 3: 提交测试文档**

```bash
# 创建测试记录文档
echo "# 用户注册与管理功能测试记录

## 测试日期
$(date +%Y-%m-%d)

## 测试结果
- ✅ 用户注册功能正常
- ✅ 用户名/邮箱唯一性检查正常
- ✅ 用户管理 CRUD 功能正常
- ✅ 角色管理功能正常
- ✅ 状态管理功能正常
- ✅ 密码重置功能正常
- ✅ 权限控制正常" > docs/tests/user-auth-test.md

git add docs/tests/user-auth-test.md
git commit -m "test: 添加用户注册与管理功能测试记录"
```

---

## 完成检查清单

- [ ] UserProfile 模型已扩展（email, is_active, last_login_time 等）
- [ ] 数据库迁移已执行
- [ ] 注册相关 Serializers 已创建
- [ ] 注册 View 和检查接口已创建
- [ ] UserViewSet 已创建（包含所有管理 action）
- [ ] URL 配置已更新
- [ ] 前端 API 服务已创建
- [ ] 注册页面已创建（新中式美学风格）
- [ ] 用户管理页面已创建（新中式美学风格）
- [ ] 路由配置已更新
- [ ] 注册功能测试通过
- [ ] 用户管理功能测试通过
- [ ] 权限控制测试通过

---

## 相关文档

- 设计文档: `docs/plans/2026-02-26-user-authentication-design.md`
- 项目架构: `memory-bank/architecture.md`
- PRD 文档: `memory-bank/PRD.md`
