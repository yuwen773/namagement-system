from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from utils.pagination import StandardPageNumberPagination
from utils.response import error_response, success_response

from .models import UserProfile, get_user_role
from .permissions import IsAdmin
from .serializers import (
    CheckEmailSerializer,
    CheckUsernameSerializer,
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UpdateRoleSerializer,
    UpdateStatusSerializer,
    UserManageSerializer,
    UserSerializer,
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


class UserViewSet(ModelViewSet):
    """用户管理 ViewSet - 管理员进行用户 CRUD 操作"""

    queryset = User.objects.select_related("profile").all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = StandardPageNumberPagination

    def get_permissions(self):
        """动态权限控制：管理员专属操作"""
        if self.action in ["list", "create", "update", "destroy", "update_status", "update_role", "reset_password"]:
            return [IsAdmin()]
        return super().get_permissions()

    def get_serializer_class(self):
        """动态序列化器选择：创建/更新使用管理用序列化器"""
        if self.action in ["create", "update"]:
            return UserManageSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        """用户列表 - 支持分页和过滤"""
        queryset = self.get_queryset()

        # 过滤参数
        username = request.query_params.get("username", "").strip()
        role = request.query_params.get("role", "").strip()
        is_active = request.query_params.get("is_active", "").strip()

        if username:
            queryset = queryset.filter(username__icontains=username)
        if role:
            queryset = queryset.filter(profile__role=role)
        if is_active:
            queryset = queryset.filter(profile__is_active=is_active.lower() == "true")

        # 分页
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)

        return success_response(
            data=serializer.data,
            total=queryset.count(),
            message="获取用户列表成功",
        )

    def create(self, request, *args, **kwargs):
        """创建新用户（管理员）"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        return success_response(
            data=UserSerializer(user).data,
            message="创建用户成功",
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """更新用户信息"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # 不允许修改自己
        if instance.id == request.user.id:
            return error_response(
                message="不允许修改自己的账号信息",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        return success_response(
            data=UserSerializer(user).data,
            message="更新用户成功",
        )

    def destroy(self, request, *args, **kwargs):
        """删除用户"""
        instance = self.get_object()

        # 不允许删除自己
        if instance.id == request.user.id:
            return error_response(
                message="不允许删除自己的账号",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        instance.delete()
        return success_response(message="删除用户成功")

    @action(methods=["patch"], detail=False, url_path="update-status")
    def update_status(self, request, *args, **kwargs):
        """批量更新用户状态（启用/禁用）"""
        serializer = UpdateStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user_ids = serializer.validated_data["user_ids"]
        is_active = serializer.validated_data["is_active"]

        # 不允许修改自己的状态
        if request.user.id in user_ids:
            return error_response(
                message="不允许修改自己的账号状态",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # 批量更新
        updated_count = UserProfile.objects.filter(user_id__in=user_ids).update(is_active=is_active)

        return success_response(
            data={"updated_count": updated_count},
            message=f"{'启用' if is_active else '禁用'}成功",
        )

    @action(methods=["patch"], detail=False, url_path="update-role")
    def update_role(self, request, *args, **kwargs):
        """批量更新用户角色"""
        serializer = UpdateRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user_ids = serializer.validated_data["user_ids"]
        role = serializer.validated_data["role"]

        # 不允许修改自己的角色
        if request.user.id in user_ids:
            return error_response(
                message="不允许修改自己的角色",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # 批量更新
        updated_count = UserProfile.objects.filter(user_id__in=user_ids).update(role=role)

        return success_response(
            data={"updated_count": updated_count},
            message="角色修改成功",
        )

    @action(methods=["patch"], detail=False, url_path="reset-password")
    def reset_password(self, request, *args, **kwargs):
        """管理员重置用户密码"""
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        return success_response(
            data={"user_id": user.id, "username": user.username},
            message="密码重置成功",
        )
