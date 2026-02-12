from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsAdmin, IsUserOrAdmin


class RegisterView(APIView):
    """
    用户注册接口

    提供用户注册功能，允许新用户创建账号。注册成功后返回用户基本信息。

    权限要求：
        无需认证（AllowAny）

    请求体：
        username: 用户名（必填，唯一）
        password: 密码（必填，最少6位）
        password_confirm: 确认密码（必填）
        email: 邮箱地址（选填）
        real_name: 真实姓名（选填）
        phone: 手机号码（选填）

    响应：
        成功：返回用户基本信息（code: 0）
        失败：返回错误信息（code: -1）
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary='用户注册',
        description='''
        创建新用户账号，需要提供用户名、密码等信息。

        **验证规则：**
        - 用户名必须唯一
        - 密码长度不能少于6位
        - 两次密码输入必须一致
        - 用户名和密码为必填项

        **成功响应：**
        返回创建的用户信息，包含用户ID、用户名、角色等基本信息。

        **失败响应：**
        返回详细的验证错误信息，如用户名已存在、密码不一致等。
        ''',
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        tags=['认证'],
        examples=[
            OpenApiExample(
                '成功注册',
                value={
                    'username': 'testuser',
                    'password': 'password123',
                    'password_confirm': 'password123',
                    'email': 'test@example.com',
                    'real_name': '测试用户',
                    'phone': '13800138000'
                }
            ),
        ]
    )
    def post(self, request):
        """
        处理用户注册请求

        Args:
            request: 包含用户注册信息的请求对象

        Returns:
            Response: 注册成功返回用户信息（201），失败返回错误信息（400）
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'code': 0,
                'message': '注册成功',
                'data': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'code': -1,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    用户登录接口

    提供用户登录功能，验证用户凭据并返回JWT Token。

    权限要求：
        无需认证（AllowAny）

    请求体：
        username: 用户名（必填）
        password: 密码（必填）

    响应：
        成功：返回访问令牌、刷新令牌和用户信息（code: 0）
        失败：返回错误信息（code: -1）

    Token说明：
        - access_token: 用于API认证的访问令牌，有效期2小时
        - refresh_token: 用于刷新访问令牌的刷新令牌，有效期7天
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary='用户登录',
        description='''
        验证用户凭据并返回JWT Token。

        **验证规则：**
        - 用户名必须存在
        - 密码必须正确
        - 用户账号必须是启用状态（is_active=True）

        **成功响应：**
        返回JWT访问令牌、刷新令牌和用户信息。

        - access_token: 访问令牌，有效期2小时
        - refresh_token: 刷新令牌，有效期7天
        - user: 当前登录用户信息

        **失败响应：**
        - 用户名或密码错误
        - 用户已被禁用
        - 用户名或密码为空
        ''',
        request=UserLoginSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        tags=['认证'],
        examples=[
            OpenApiExample(
                '成功登录',
                value={
                    'username': 'admin',
                    'password': 'admin123'
                }
            ),
        ]
    )
    def post(self, request):
        """
        处理用户登录请求

        Args:
            request: 包含用户名和密码的请求对象

        Returns:
            Response: 登录成功返回Token和用户信息（200），失败返回错误信息（400）
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 0,
                'message': '登录成功',
                'data': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': UserSerializer(user).data
                }
            })
        return Response({
            'code': -1,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    用户登出接口

    提供用户登出功能，清除客户端的 Token。

    权限要求：
        无需认证（AllowAny）

    请求方法：
        POST

    响应：
        成功：返回成功消息（code: 0）

    注意事项：
        JWT Token 是无状态的，登出主要由客户端删除本地 Token 实现
        此接口主要用于记录登出日志或执行其他登出相关业务逻辑
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary='用户登出',
        description='''
        执行用户登出操作。

        **说明：**
        - JWT Token 是无状态的，服务端无法主动失效
        - 客户端需要删除本地存储的 access_token 和 refresh_token
        - 此接口主要用于记录登出日志或执行其他登出相关业务逻辑

        **客户端操作：**
        - 删除 localStorage 中的 access_token
        - 删除 localStorage 中的 refresh_token
        - 删除 localStorage 中的 user 信息
        - 跳转到登录页面
        ''',
        responses={
            200: OpenApiTypes.OBJECT,
        },
        tags=['认证'],
    )
    def post(self, request):
        """
        处理用户登出请求

        Args:
            request: 请求对象

        Returns:
            Response: 返回登出成功消息
        """
        # JWT 是无状态的，登出主要由客户端处理
        # 这里可以添加登出日志等业务逻辑
        return Response({
            'code': 0,
            'message': '登出成功'
        })


class ProfileView(APIView):
    """
    获取/更新当前用户信息

    提供当前登录用户的信息查询和更新功能。

    权限要求：
        需要认证（IsAuthenticated）

    GET方法：
        获取当前登录用户的个人信息

    PUT方法：
        更新当前登录用户的个人信息（部分更新）
        可更新字段：real_name、email、phone

    响应：
        成功：返回用户信息（code: 0）
        失败：返回错误信息（code: -1）
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='获取当前用户信息',
        description='''
        获取当前登录用户的个人信息。

        **返回信息包括：**
        - id: 用户ID
        - username: 用户名
        - real_name: 真实姓名
        - email: 邮箱地址
        - phone: 手机号码
        - role: 用户角色
        - created_at: 创建时间

        **权限要求：**
        需要有效的访问令牌（JWT Token）
        ''',
        responses={
            200: OpenApiTypes.OBJECT,
        },
        tags=['用户'],
    )
    def get(self, request):
        """
        获取当前用户信息

        Args:
            request: 已认证的请求对象

        Returns:
            Response: 返回当前用户信息
        """
        serializer = UserProfileSerializer(request.user)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @extend_schema(
        summary='更新当前用户信息',
        description='''
        更新当前登录用户的个人信息，支持部分更新。

        **可更新字段：**
        - real_name: 真实姓名
        - email: 邮箱地址
        - phone: 手机号码

        **只读字段（不可更新）：**
        - username: 用户名
        - role: 用户角色
        - is_active: 账号状态

        **权限要求：**
        需要有效的访问令牌（JWT Token）
        ''',
        request=UserProfileSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        tags=['用户'],
        examples=[
            OpenApiExample(
                '更新用户信息',
                value={
                    'real_name': '张三',
                    'email': 'zhangsan@example.com',
                    'phone': '13900139000'
                }
            ),
        ]
    )
    def put(self, request):
        """
        更新当前用户信息

        Args:
            request: 包含更新数据的请求对象

        Returns:
            Response: 更新成功返回用户信息（200），失败返回错误信息（400）
        """
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 0,
                'message': '信息更新成功',
                'data': serializer.data
            })
        return Response({
            'code': -1,
            'message': '信息更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    修改密码接口

    提供当前登录用户修改密码的功能。

    权限要求：
        需要认证（IsAuthenticated）

    请求体：
        old_password: 原密码（必填）
        new_password: 新密码（必填，最少6位）

    响应：
        成功：返回成功消息（code: 0）
        失败：返回错误信息（code: -1）

    注意事项：
        - 原密码必须正确
        - 新密码长度不能少于6位
        - 修改密码后需要重新登录
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='修改密码',
        description='''
        修改当前登录用户的密码。

        **验证规则：**
        - 原密码必须正确
        - 新密码长度不能少于6位
        - 新密码不能与原密码相同

        **成功后影响：**
        修改密码成功后，所有有效的Token将失效，需要使用新密码重新登录。

        **权限要求：**
        需要有效的访问令牌（JWT Token）
        ''',
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        tags=['用户'],
        examples=[
            OpenApiExample(
                '修改密码',
                value={
                    'old_password': 'oldpassword123',
                    'new_password': 'newpassword456'
                }
            ),
        ]
    )
    def post(self, request):
        """
        处理密码修改请求

        Args:
            request: 包含原密码和新密码的请求对象

        Returns:
            Response: 修改成功返回成功消息（200），失败返回错误信息（400）
        """
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not request.user.check_password(old_password):
                return Response({
                    'code': -1,
                    'message': '原密码错误'
                }, status=status.HTTP_400_BAD_REQUEST)

            request.user.set_password(new_password)
            request.user.save()
            return Response({
                'code': 0,
                'message': '密码修改成功'
            })
        return Response({
            'code': -1,
            'message': '密码修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集（管理员专用）

    提供完整的用户CRUD操作和用户管理功能，仅管理员可访问。

    权限要求：
        - 需要认证（IsAuthenticated）
        - 需要管理员权限（IsAdmin）

    支持的操作：
        - list: 获取用户列表（支持筛选和搜索）
        - retrieve: 获取用户详情
        - create: 创建新用户
        - update: 更新用户信息（完整更新）
        - partial_update: 更新用户信息（部分更新）
        - disable: 禁用用户（自定义操作）
        - enable: 启用用户（自定义操作）
        - reset_password: 重置用户密码（自定义操作）
        - delete: 删除用户（自定义操作）

    列表筛选参数：
        - username: 按用户名模糊搜索
        - role: 按角色筛选（ADMIN/USER）
        - is_active: 按状态筛选（true/false）
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        summary='获取用户列表',
        description='''
        获取系统中的所有用户列表，支持按条件筛选。

        **筛选参数：**
        - username: 按用户名模糊搜索（不区分大小写）
        - role: 按角色筛选（ADMIN/USER）
        - is_active: 按账号状态筛选（true/false）

        **返回信息：**
        分页返回用户列表，每个用户包含完整信息。

        **权限要求：**
        需要管理员权限
        ''',
        parameters=[
            OpenApiParameter(
                name='username',
                description='用户名（模糊搜索）',
                type=OpenApiTypes.STR,
                required=False
            ),
            OpenApiParameter(
                name='role',
                description='角色筛选（ADMIN/USER）',
                type=OpenApiTypes.STR,
                required=False
            ),
            OpenApiParameter(
                name='is_active',
                description='账号状态（true/false）',
                type=OpenApiTypes.BOOL,
                required=False
            ),
        ],
        responses={
            200: OpenApiTypes.OBJECT,
        },
        tags=['用户管理'],
    )
    def list(self, request, *args, **kwargs):
        """
        获取用户列表

        Args:
            request: 包含筛选参数的请求对象

        Returns:
            Response: 返回用户列表和总数
        """
        queryset = self.get_queryset()
        # 支持按用户名搜索
        username = request.query_params.get('username')
        if username:
            queryset = queryset.filter(username__icontains=username)
        # 支持按角色筛选
        role = request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        # 支持按状态筛选
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'code': 0,
                'data': serializer.data,
                'total': self.paginator.page.paginator.count
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @extend_schema(
        summary='禁用用户',
        description='''
        禁用指定的用户账号。

        **影响：**
        - 用户将无法登录系统
        - 用户的Token将失效
        - 用户数据保留，不会被删除

        **权限要求：**
        需要管理员权限
        ''',
        responses={
            200: OpenApiTypes.OBJECT,
        },
        tags=['用户管理'],
    )
    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        """
        禁用用户

        Args:
            request: 请求对象
            pk: 用户ID

        Returns:
            Response: 返回操作结果
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 已禁用'
        })

    @extend_schema(
        summary='启用用户',
        description='''
        启用已被禁用的用户账号。

        **影响：**
        - 用户可以重新登录系统
        - 用户功能恢复正常

        **权限要求：**
        需要管理员权限
        ''',
        responses={
            200: OpenApiTypes.OBJECT,
        },
        tags=['用户管理'],
    )
    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        """
        启用用户

        Args:
            request: 请求对象
            pk: 用户ID

        Returns:
            Response: 返回操作结果
        """
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 已启用'
        })

    @extend_schema(
        summary='重置用户密码',
        description='''
        重置指定用户的密码。

        **请求参数：**
        - new_password: 新密码（可选，默认为123456）

        **影响：**
        - 用户需要使用新密码重新登录
        - 所有有效的Token将失效

        **权限要求：**
        需要管理员权限
        ''',
        request=OpenApiTypes.OBJECT,
        responses={
            200: OpenApiTypes.OBJECT,
        },
        tags=['用户管理'],
        examples=[
            OpenApiExample(
                '重置密码',
                value={'new_password': 'newpassword123'}
            ),
        ]
    )
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """
        重置用户密码

        Args:
            request: 包含新密码的请求对象
            pk: 用户ID

        Returns:
            Response: 返回操作结果
        """
        user = self.get_object()
        new_password = request.data.get('new_password', '123456')
        user.set_password(new_password)
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 密码已重置为: {new_password}'
        })

    @extend_schema(
        summary='更新用户角色',
        description='''
        更新指定用户的角色。

        **请求参数：**
        - role: 新角色（ADMIN-管理员, USER-普通用户）

        **影响：**
        - 用户的权限会立即改变
        - 角色变更后需要重新登录

        **权限要求：**
        需要管理员权限
        ''',
        request=OpenApiTypes.OBJECT,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        tags=['用户管理'],
        examples=[
            OpenApiExample(
                '更新角色',
                value={'role': 'ADMIN'}
            ),
        ]
    )
    @action(detail=True, methods=['put'])
    def role(self, request, pk=None):
        """
        更新用户角色

        Args:
            request: 包含新角色的请求对象
            pk: 用户ID

        Returns:
            Response: 返回操作结果
        """
        user = self.get_object()
        new_role = request.data.get('role')

        if not new_role:
            return Response({
                'code': -1,
                'message': '角色不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        if new_role not in ['ADMIN', 'USER']:
            return Response({
                'code': -1,
                'message': '角色必须是 ADMIN 或 USER'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.role = new_role
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 角色已更新为 {new_role}',
            'data': UserSerializer(user).data
        })
        """
        重置用户密码

        Args:
            request: 包含新密码的请求对象
            pk: 用户ID

        Returns:
            Response: 返回操作结果
        """
        user = self.get_object()
        new_password = request.data.get('new_password', '123456')
        user.set_password(new_password)
        user.save()
        return Response({
            'code': 0,
            'message': f'用户 {user.username} 密码已重置为: {new_password}'
        })

    @extend_schema(
        summary='删除用户',
        description='''
        删除指定的用户账号及其所有相关数据。

        **限制：**
        - 不能删除当前登录的管理员账号

        **影响：**
        - 用户数据将被永久删除
        - 相关的票房数据等关联数据可能被级联删除

        **权限要求：**
        需要管理员权限
        ''',
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        tags=['用户管理'],
    )
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        """
        删除用户

        Args:
            request: 请求对象
            pk: 用户ID

        Returns:
            Response: 返回操作结果
        """
        user = self.get_object()
        # 防止删除管理员自己
        if user == request.user:
            return Response({
                'code': -1,
                'message': '不能删除当前登录的管理员账户'
            }, status=status.HTTP_400_BAD_REQUEST)
        username = user.username
        user.delete()
        return Response({
            'code': 0,
            'message': f'用户 {username} 已删除'
        })
