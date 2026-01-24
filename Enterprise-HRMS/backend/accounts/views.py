from rest_framework import status, generics
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer, AdminResetPasswordSerializer
from HRMS.permissions import IsAdmin


class RegisterView(CreateAPIView):
    """
    用户注册接口
    POST /api/auth/register/
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # 允许未认证用户访问

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            'code': 201,
            'message': '注册成功',
            'data': UserSerializer(user).data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    自定义登录视图
    POST /api/auth/login/
    使用自定义序列化器返回 real_name 和 role
    """
    serializer_class = CustomTokenObtainPairSerializer


class AdminResetPasswordView(generics.UpdateAPIView):
    """
    管理员重置用户密码
    POST /api/auth/users/{user_id}/reset-password/
    仅管理员可访问
    """
    serializer_class = AdminResetPasswordSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        # 排除当前管理员自己
        return User.objects.filter(is_staff=False).exclude(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 使用 set_password 自动哈希
        instance.set_password(serializer.validated_data['new_password'])
        instance.save()

        return Response({
            'code': 0,
            'message': f'用户 {instance.real_name} 的密码已重置'
        })
