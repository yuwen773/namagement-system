# 用户注册与用户管理功能设计文档

**日期**: 2026-02-26
**系统**: 非物质文化遗产数据可视化系统
**状态**: 设计完成，待实施

---

## 一、需求概述

### 当前状态
- ✅ 已有登录功能（账号密码 + JWT）
- ✅ 已有角色模型（`UserProfile`，支持 `admin` / `user`）
- ❌ 缺少用户注册功能
- ❌ 管理端缺少用户管理功能（CRUD、角色分配等）

### 目标功能
1. 用户自主注册（用户名 + 密码 + 邮箱）
2. 管理端用户管理（完整 CRUD + 角色管理 + 状态管理 + 密码管理）
3. 用户名/邮箱唯一性实时检查
4. 管理员手动重置用户密码

---

## 二、整体架构设计

### 后端 API 端点

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/v1/auth/register` | 用户自主注册 | AllowAny |
| POST | `/api/v1/auth/check-username` | 检查用户名是否存在 | AllowAny |
| POST | `/api/v1/auth/check-email` | 检查邮箱是否存在 | AllowAny |
| GET | `/api/v1/users` | 获取用户列表（分页、筛选） | IsAdmin |
| POST | `/api/v1/users` | 管理员创建用户 | IsAdmin |
| PUT | `/api/v1/users/:id` | 更新用户信息 | IsAdmin |
| PATCH | `/api/v1/users/:id/status` | 修改用户状态 | IsAdmin |
| PATCH | `/api/v1/users/:id/role` | 修改用户角色 | IsAdmin |
| PATCH | `/api/v1/users/:id/password` | 重置用户密码 | IsAdmin |
| DELETE | `/api/v1/users/:id` | 删除用户 | IsAdmin |

### 前端页面

| 路径 | 页面 | 说明 |
|------|------|------|
| `/register` | 注册页面 | 用户自主注册 |
| `/admin/users` | 用户管理页面 | 管理端用户 CRUD |

---

## 三、后端实现设计

### 数据模型扩展

```python
# backend/apps/users/models.py

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
```

### Serializers 层

```python
# backend/apps/users/serializers.py

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=20)
    password = serializers.CharField(min_length=6, write_only=True)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已被注册")
        return value


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role')
    email = serializers.EmailField(source='profile.email')
    is_active = serializers.BooleanField(source='profile.is_active')
    last_login_time = serializers.DateTimeField(source='profile.last_login_time')

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email', 'is_active', 'last_login_time', 'date_joined']


class UserManageSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        email = validated_data.pop('email', '')
        password = validated_data.pop('password', None)

        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        UserProfile.objects.create(
            user=user,
            role=role,
            email=email
        )
        return user
```

### Views 层

```python
# backend/apps/users/views.py

class RegisterView(APIView):
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
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

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


class CheckUsernameView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        exists = User.objects.filter(username=username).exists()
        return success_response(data={'exists': exists})


class CheckEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        exists = UserProfile.objects.filter(email=email).exists()
        return success_response(data={'exists': exists})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('profile').all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'destroy',
                           'update_status', 'update_role', 'reset_password']:
            return [IsAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return UserManageSerializer
        return UserSerializer

    def list(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        username = request.query_params.get('username', '')
        role = request.query_params.get('role', '')
        is_active = request.query_params.get('is_active', '')

        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)
        if role:
            queryset = queryset.filter(profile__role=role)
        if is_active != '':
            queryset = queryset.filter(profile__is_active=is_active == 'true')

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        serializer = self.get_serializer(page_obj, many=True)
        return success_response(
            data=serializer.data,
            total=paginator.count
        )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        user = self.get_object()
        is_active = request.data.get('is_active')
        user.profile.is_active = is_active
        user.profile.save()
        return success_response(message="状态更新成功")

    @action(detail=True, methods=['patch'])
    def update_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get('role')
        user.profile.role = role
        user.profile.save()
        return success_response(message="角色更新成功")

    @action(detail=True, methods=['patch'])
    def reset_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('password')
        user.set_password(new_password)
        user.save()
        return success_response(message="密码重置成功")
```

---

## 四、前端实现设计

### 注册页面 (`/register`)

**表单字段：**
| 字段 | 验证规则 |
|------|---------|
| 用户名 | 3-20字符，字母数字下划线，实时检查唯一性 |
| 邮箱 | 标准邮箱格式，实时检查唯一性 |
| 密码 | 最少6位 |
| 确认密码 | 与密码一致 |

**交互细节：**
- 用户名/邮箱失焦时异步检查是否已存在
- 密码强度提示
- 注册成功后自动登录并跳转到仪表盘
- 底部「已有账号？去登录」链接

### 用户管理页面 (`/admin/users`)

**页面布局：**
```
┌─────────────────────────────────────────────────────┐
│  页面标题: 用户管理              [+ 新增用户] 按钮   │
├─────────────────────────────────────────────────────┤
│  筛选区: [用户名搜索] [角色筛选] [状态筛选] [搜索]   │
├─────────────────────────────────────────────────────┤
│  表格: ID, 用户名, 邮箱, 角色, 状态, 最后登录, 操作 │
└─────────────────────────────────────────────────────┘
```

**表格操作：**
- 编辑：弹出编辑对话框
- 更多操作下拉菜单：修改角色、修改状态、重置密码、删除

### API 服务层

```typescript
// frontend/src/api/user.ts

export interface RegisterRequest {
  username: string
  password: string
  email: string
}

export interface UserListParams {
  page?: number
  page_size?: number
  username?: string
  role?: string
  is_active?: boolean
}

export const checkUsername = (username: string) => {
  return request.post('/api/v1/auth/check-username', { username })
}

export const checkEmail = (email: string) => {
  return request.post('/api/v1/auth/check-email', { email })
}

export const register = (data: RegisterRequest) => {
  return request.post('/api/v1/auth/register', data)
}

export const getUserList = (params: UserListParams) => {
  return request.get('/api/v1/users', { params })
}

export const createUser = (data: any) => {
  return request.post('/api/v1/users', data)
}

export const updateUser = (id: number, data: any) => {
  return request.put(`/api/v1/users/${id}`, data)
}

export const updateUserStatus = (id: number, is_active: boolean) => {
  return request.patch(`/api/v1/users/${id}/status`, { is_active })
}

export const updateUserRole = (id: number, role: string) => {
  return request.patch(`/api/v1/users/${id}/role`, { role })
}

export const resetUserPassword = (id: number, password: string) => {
  return request.patch(`/api/v1/users/${id}/password`, { password })
}

export const deleteUser = (id: number) => {
  return request.delete(`/api/v1/users/${id}`)
}
```

---

## 五、安全策略

| 风险点 | 防护措施 |
|--------|---------|
| 用户名枚举攻击 | 统一返回「用户名或密码错误」 |
| 暴力破解 | 登录/注册接口限流（1分钟5次） |
| 密码泄露 | 后端加密存储 |
| CSRF | JWT + Authorization Header |
| SQL 注入 | DRF ORM 自动转义 |
| 越权操作 | `IsAdmin` 权限类 |

---

## 六、错误码规范

| 错误码 | 说明 |
|--------|------|
| 40001 | 用户名已存在 |
| 40002 | 邮箱已被注册 |
| 40003 | 密码格式不符合要求 |
| 40004 | 两次密码不一致 |
| 40301 | 无权限操作 |
| 40401 | 用户不存在 |
| 42901 | 请求过于频繁 |

---

## 七、实施步骤

1. 后端 - 扩展 UserProfile 模型
2. 后端 - 实现注册接口
3. 后端 - 实现用户管理 ViewSet
4. 前端 - 创建注册页面
5. 前端 - 创建用户管理页面
6. 前端 - 更新路由配置
7. 测试 - 接口测试
8. 测试 - 前端功能测试
