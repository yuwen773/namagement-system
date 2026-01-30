"""
用户认证视图模块

包含用户注册、登录等认证相关的视图。
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.utils import timezone
from utils.response import ApiResponse
from utils.exceptions import ValidationError as BusinessValidationError
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer, LoginSerializer
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
