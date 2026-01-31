"""
用户认证视图模块

包含用户注册、登录等认证相关的视图。
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.utils import timezone
from django.db.models import Count, Q
from utils.response import ApiResponse
from utils.exceptions import ValidationError as BusinessValidationError, PermissionDeniedError
from utils.permissions import IsAdminUser
from utils.constants import UserRole
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer, LoginSerializer, UpdateProfileSerializer, ChangePasswordSerializer, UserListSerializer
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    用户注册接口

    请求方法：POST
    路由：/api/accounts/register/

    请求参数：
        - username: 用户名（必填，3-20个字符）
        - password: 密码（必填，至少8位）
        - password_confirm: 确认密码（必填）
        - email: 邮箱（可选）

    成功响应（201）：
        {
            "code": 201,
            "message": "注册成功",
            "data": {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "role": "user",
                "is_active": true,
                "created_at": "2026-01-30T12:00:00Z"
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "参数验证失败",
            "errors": {
                "username": ["该用户名已被注册"]
            }
        }

    Returns:
        Response: 注册结果响应
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        try:
            # 使用事务确保用户和用户资料同时创建成功
            with transaction.atomic():
                user = serializer.save()

            # 返回用户基本信息
            response_data = UserSerializer(user).data
            return ApiResponse.success(
                data=response_data,
                message='注册成功',
                code=201
            )

        except Exception as e:
            # 事务失败时自动回滚
            raise BusinessValidationError(
                detail=f'注册失败：{str(e)}'
            )

    # 验证失败，返回详细错误信息
    return ApiResponse.error(
        message='参数验证失败',
        errors=serializer.errors
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    健康检查接口

    用于测试 accounts 模块是否正常工作。

    Returns:
        Response: 健康状态响应
    """
    return ApiResponse.success(
        data={'status': 'healthy', 'module': 'accounts'},
        message='accounts 模块运行正常'
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    用户登录接口

    请求方法：POST
    路由：/api/accounts/login/

    请求参数：
        - username: 用户名（必填）
        - password: 密码（必填）

    成功响应（200）：
        {
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "user": {
                    "id": 1,
                    "username": "testuser",
                    "email": "test@example.com",
                    "role": "user",
                    "is_active": true
                }
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "参数验证失败",
            "errors": {...}
        }

    Returns:
        Response: 登录结果响应
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        # 更新最后登录时间
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        # 生成 JWT Token
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # 返回 Token 和用户信息
        response_data = {
            'token': access_token,
            'refresh_token': refresh_token,
            'user': UserSerializer(user).data
        }

        return ApiResponse.success(
            data=response_data,
            message='登录成功'
        )

    # 验证失败，返回详细错误信息
    return ApiResponse.error(
        message='参数验证失败',
        errors=serializer.errors
    )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def me(request):
    """
    获取/更新当前用户信息接口

    请求方法：GET / PUT
    路由：/api/accounts/me/

    请求头：
        Authorization: Bearer <access_token>

    GET 请求 - 获取用户信息：
    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "role": "user",
                "is_active": true,
                "created_at": "2026-01-30T12:00:00Z"
            }
        }

    PUT 请求 - 更新用户资料：
    请求参数：
        - nickname: 昵称（可选，最大50个字符）
        - bio: 个人简介（可选，最大500个字符）
        - avatar_url: 头像 URL（可选）
        - phone: 手机号（可选，需符合格式且唯一）

    请求体示例：
        {
            "nickname": "美食家小王",
            "bio": "热爱烹饪，喜欢尝试各种菜谱"
        }

    成功响应（200）：
        {
            "code": 200,
            "message": "更新成功",
            "data": {
                "id": 1,
                "user_id": 1,
                "username": "testuser",
                "nickname": "美食家小王",
                "phone": null,
                "bio": "热爱烹饪，喜欢尝试各种菜谱",
                "avatar_url": "",
                "created_at": "2026-01-30T12:00:00Z"
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "参数验证失败",
            "errors": {
                "phone": ["该手机号已被使用"]
            }
        }

    错误响应（401）：
        {
            "code": 401,
            "message": "未提供有效的认证凭据",
            "data": null
        }

    Returns:
        Response: 当前用户信息或更新结果
    """
    if request.method == 'GET':
        # 获取当前用户信息
        serializer = UserSerializer(request.user)
        return ApiResponse.success(
            data=serializer.data,
            message='获取成功'
        )

    elif request.method == 'PUT':
        # 更新用户资料
        # 获取或创建用户资料
        profile, created = request.user.profile.__class__.objects.get_or_create(
            user=request.user,
            defaults={
                'nickname': request.user.username,
                'bio': '',
                'avatar_url': ''
            }
        )

        # 使用 UpdateProfileSerializer 验证和更新数据
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(
                data=UserProfileSerializer(profile).data,
                message='更新成功'
            )

        # 验证失败，返回详细错误信息
        return ApiResponse.error(
            message='参数验证失败',
            errors=serializer.errors
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    修改密码接口

    请求方法：PUT
    路由：/api/accounts/password/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - old_password: 旧密码（必填）
        - new_password: 新密码（必填，至少8位）
        - new_password_confirm: 确认新密码（必填）

    请求体示例：
        {
            "old_password": "oldpass123",
            "new_password": "newpass456",
            "new_password_confirm": "newpass456"
        }

    成功响应（200）：
        {
            "code": 200,
            "message": "密码修改成功",
            "data": null
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "参数验证失败",
            "errors": {
                "old_password": ["旧密码不正确"]
            }
        }

    错误响应（401）：
        {
            "code": 401,
            "message": "未提供有效的认证凭据",
            "data": null
        }

    Returns:
        Response: 修改密码结果响应
    """
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'user': request.user}
    )

    if serializer.is_valid():
        # 保存新密码
        serializer.save()

        return ApiResponse.success(
            message='密码修改成功'
        )

    # 验证失败，返回详细错误信息
    return ApiResponse.error(
        message='参数验证失败',
        errors=serializer.errors
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    """
    管理员统计接口（仅管理员可访问）

    请求方法：GET
    路由：/api/accounts/admin/stats/

    请求头：
        Authorization: Bearer <access_token>

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "total_users": 150,
                "active_users": 142,
                "admin_count": 5,
                "user_count": 145,
                "today_new_users": 3
            }
        }

    错误响应（403）：
        {
            "code": 403,
            "message": "权限不足，仅管理员可访问",
            "data": null
        }

    Returns:
        Response: 管理员统计数据响应
    """
    from datetime import datetime

    # 获取今天的日期范围
    today = timezone.now().date()
    today_start = timezone.make_aware(datetime(today.year, today.month, today.day))

    # 统计数据
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    admin_count = User.objects.filter(role=UserRole.ADMIN).count()
    user_count = User.objects.filter(role=UserRole.USER).count()
    today_new_users = User.objects.filter(created_at__gte=today_start).count()

    response_data = {
        'total_users': total_users,
        'active_users': active_users,
        'admin_count': admin_count,
        'user_count': user_count,
        'today_new_users': today_new_users
    }

    return ApiResponse.success(
        data=response_data,
        message='获取成功'
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def role_check(request):
    """
    角色检查接口（用于测试权限控制）

    请求方法：GET
    路由：/api/accounts/role-check/

    请求头：
        Authorization: Bearer <access_token>

    成功响应（200）：
        {
            "code": 200,
            "message": "角色检查成功",
            "data": {
                "username": "testuser",
                "role": "user",
                "is_admin": false,
                "can_access_admin": false
            }
        }

    Returns:
        Response: 角色检查结果响应
    """
    user = request.user
    is_admin = user.role == UserRole.ADMIN

    response_data = {
        'username': user.username,
        'role': user.role,
        'is_admin': is_admin,
        'can_access_admin': is_admin
    }

    return ApiResponse.success(
        data=response_data,
        message='角色检查成功'
    )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
    """
    用户列表接口（仅管理员可访问）

    请求方法：GET
    路由：/api/accounts/admin/users/

    请求头：
        Authorization: Bearer <access_token>

    请求参数：
        - page: 页码（可选，默认为1）
        - page_size: 每页数量（可选，默认20，最大100）
        - search: 搜索关键词（可选，搜索用户名或邮箱）
        - role: 角色筛选（可选，user/admin）

    请求示例：
        GET /api/accounts/admin/users/?page=1&page_size=20&search=test&role=user

    成功响应（200）：
        {
            "code": 200,
            "message": "获取成功",
            "data": {
                "count": 150,
                "next": null,
                "previous": "http://localhost:8000/api/accounts/admin/users/?page=1",
                "results": [
                    {
                        "id": 1,
                        "username": "testuser",
                        "email": "test@example.com",
                        "role": "user",
                        "is_active": true,
                        "nickname": "测试用户",
                        "phone": "13800138000",
                        "last_login": "2026-01-30T12:00:00Z",
                        "created_at": "2026-01-30T12:00:00Z"
                    }
                ]
            }
        }

    错误响应（403）：
        {
            "code": 403,
            "message": "权限不足，仅管理员可访问",
            "data": null
        }

    Returns:
        Response: 用户列表响应
    """
    from utils.pagination import StandardPagination
    from rest_framework.decorators import authentication_classes, permission_classes
    from rest_framework.settings import api_settings

    # 获取查询参数
    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', StandardPagination.page_size)
    search = request.query_params.get('search', '')
    role_filter = request.query_params.get('role', '')

    # 构建查询集
    queryset = User.objects.all()

    # 搜索功能（用户名或邮箱）
    if search:
        queryset = queryset.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    # 角色筛选
    if role_filter:
        if role_filter in [UserRole.USER, UserRole.ADMIN]:
            queryset = queryset.filter(role=role_filter)

    # 按创建时间降序排列
    queryset = queryset.order_by('-created_at')

    # 分页
    paginator = StandardPagination()
    page_size = int(page_size)
    # 限制最大 page_size
    if page_size > paginator.max_page_size:
        page_size = paginator.max_page_size

    paginator.page_size = page_size
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    # 序列化数据
    serializer = UserListSerializer(paginated_queryset, many=True)

    return ApiResponse.success(
        data=paginator.get_paginated_response(serializer.data),
        message='获取成功'
    )


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def ban_user(request, user_id):
    """
    封禁用户接口（仅管理员可访问）

    请求方法：PUT
    路由：/api/accounts/admin/users/<user_id>/ban/

    请求头：
        Authorization: Bearer <access_token>

    路径参数：
        - user_id: 用户 ID

    成功响应（200）：
        {
            "code": 200,
            "message": "用户已封禁",
            "data": {
                "id": 2,
                "username": "testuser",
                "email": "test@example.com",
                "role": "user",
                "is_active": false,
                "created_at": "2026-01-30T12:00:00Z"
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "不能封禁自己",
            "data": null
        }

    错误响应（403）：
        {
            "code": 403,
            "message": "权限不足，仅管理员可访问",
            "data": null
        }

    错误响应（404）：
        {
            "code": 404,
            "message": "用户不存在",
            "data": null
        }

    Returns:
        Response: 封禁用户响应
    """
    # 防止封禁自己
    if request.user.id == int(user_id):
        raise BusinessValidationError(detail='不能封禁自己')

    # 获取目标用户
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise BusinessValidationError(detail='用户不存在', code=404)

    # 检查用户是否已被封禁
    if not target_user.is_active:
        raise BusinessValidationError(detail='该用户已被封禁')

    # 封禁用户
    target_user.is_active = False
    target_user.save(update_fields=['is_active'])

    return ApiResponse.success(
        data=UserListSerializer(target_user).data,
        message='用户已封禁'
    )


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def unban_user(request, user_id):
    """
    解封用户接口（仅管理员可访问）

    请求方法：PUT
    路由：/api/accounts/admin/users/<user_id>/unban/

    请求头：
        Authorization: Bearer <access_token>

    路径参数：
        - user_id: 用户 ID

    成功响应（200）：
        {
            "code": 200,
            "message": "用户已解封",
            "data": {
                "id": 2,
                "username": "testuser",
                "email": "test@example.com",
                "role": "user",
                "is_active": true,
                "created_at": "2026-01-30T12:00:00Z"
            }
        }

    错误响应（400）：
        {
            "code": 400,
            "message": "该用户未被封禁",
            "data": null
        }

    错误响应（403）：
        {
            "code": 403,
            "message": "权限不足，仅管理员可访问",
            "data": null
        }

    错误响应（404）：
        {
            "code": 404,
            "message": "用户不存在",
            "data": null
        }

    Returns:
        Response: 解封用户响应
    """
    # 获取目标用户
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise BusinessValidationError(detail='用户不存在', code=404)

    # 检查用户是否已被封禁
    if target_user.is_active:
        raise BusinessValidationError(detail='该用户未被封禁')

    # 解封用户
    target_user.is_active = True
    target_user.save(update_fields=['is_active'])

    return ApiResponse.success(
        data=UserListSerializer(target_user).data,
        message='用户已解封'
    )
