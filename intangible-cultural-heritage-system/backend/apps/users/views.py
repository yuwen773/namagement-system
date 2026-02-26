from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from utils.response import error_response, success_response

from django.contrib.auth import get_user_model

from .models import get_user_role
from .serializers import (
    CheckEmailSerializer,
    CheckUsernameSerializer,
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
)

User = get_user_model()


def _first_error(errors):
    if not errors:
        return "请求参数错误"
    first = next(iter(errors.values()))
    if isinstance(first, (list, tuple)) and first:
        return str(first[0])
    return str(first)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return success_response(
            data=serializer.validated_data,
            message="登录成功",
        )


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return success_response(data=serializer.validated_data, message="刷新成功")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=_first_error(serializer.errors))

        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            if str(token.get("user_id")) != str(request.user.id):
                return error_response(
                    message="无权注销该 token",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
            token.blacklist()
        except TokenError:
            return error_response(message="refresh token 无效或已过期")

        return success_response(message="登出成功")


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "id": request.user.id,
            "username": request.user.username,
            "role": get_user_role(request.user),
        }
        return success_response(data=data, message="获取成功")


class RegisterView(APIView):
    """用户注册接口"""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        # 生成 JWT tokens
        refresh = RefreshToken.for_user(user)

        return success_response(
            data={
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": "user",
                },
            },
            message="注册成功",
            status_code=status.HTTP_201_CREATED,
        )


class CheckUsernameView(APIView):
    """检查用户名是否可用"""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CheckUsernameSerializer(data=request.data)
        if not serializer.is_valid():
            # 验证失败表示用户名已存在或格式不正确
            return success_response(
                data={"exists": True},
                message="用户名不可用",
            )
        # 验证通过表示用户名可用
        return success_response(
            data={"exists": False},
            message="用户名可用",
        )


class CheckEmailView(APIView):
    """检查邮箱是否可用"""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = CheckEmailSerializer(data=request.data)
        if not serializer.is_valid():
            # 验证失败表示邮箱已存在
            return success_response(
                data={"exists": True},
                message="邮箱不可用",
            )
        # 验证通过表示邮箱可用
        return success_response(
            data={"exists": False},
            message="邮箱可用",
        )
