from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from utils.response import error_response, success_response

from .models import get_user_role
from .serializers import LoginSerializer, LogoutSerializer


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
