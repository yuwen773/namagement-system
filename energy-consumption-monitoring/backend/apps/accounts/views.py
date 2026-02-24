from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import (
    ChangePasswordSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


User = get_user_model()


AuthTokenResponseSerializer = inline_serializer(
    name="AuthTokenResponse",
    fields={
        "user": UserSerializer(),
        "access": serializers.CharField(),
        "refresh": serializers.CharField(),
    },
)
RefreshTokenResponseSerializer = inline_serializer(
    name="RefreshTokenResponse",
    fields={
        "access": serializers.CharField(),
    },
)
SimpleMessageSerializer = inline_serializer(
    name="SimpleMessageResponse",
    fields={
        "message": serializers.CharField(),
    },
)


@extend_schema_view(
    register=extend_schema(
        summary="用户注册",
        description="创建新用户并返回 access/refresh token。",
        request=UserRegisterSerializer,
        responses={201: AuthTokenResponseSerializer},
    ),
    login=extend_schema(
        summary="用户登录",
        description="用户名密码登录并返回 access/refresh token。",
        request=UserLoginSerializer,
        responses={200: AuthTokenResponseSerializer},
    ),
    refresh=extend_schema(
        summary="刷新访问令牌",
        description="使用 refresh token 换取新的 access token。",
        request=TokenRefreshSerializer,
        responses={200: RefreshTokenResponseSerializer},
    ),
    user_info=extend_schema(
        summary="获取当前用户信息",
        responses={200: UserSerializer},
    ),
    change_password=extend_schema(
        summary="修改当前用户密码",
        request=ChangePasswordSerializer,
        responses={
            200: SimpleMessageSerializer,
            400: OpenApiResponse(description="旧密码错误或参数校验失败"),
        },
    ),
)
class AuthViewSet(viewsets.GenericViewSet):
    """认证与用户会话相关接口。"""

    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in {"register", "login", "refresh"}:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        """注册新用户。"""
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        """用户登录并获取令牌。"""
        serializer = UserLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )

    @action(detail=False, methods=["post"], url_path="refresh")
    def refresh(self, request):
        """刷新 access token。"""
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    @action(detail=False, methods=["get"], url_path="user-info")
    def user_info(self, request):
        """返回当前登录用户信息。"""
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=["post"], url_path="change-password")
    def change_password(self, request):
        """修改当前登录用户密码。"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        if not user.check_password(old_password):
            return Response(
                {"message": "旧密码错误"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"message": "密码修改成功"})
