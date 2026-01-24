from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer,
    AdminResetPasswordSerializer, UserListSerializer, UserRoleUpdateSerializer,
    UserStatusUpdateSerializer
)
from HRMS.permissions import IsAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


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


class AdminResetPasswordView(GenericAPIView):
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

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # 使用 set_password 自动哈希
        instance.set_password(serializer.validated_data['new_password'])
        instance.save()

        return Response({
            'code': 0,
            'message': f'用户 {instance.real_name} 的密码已重置'
        })


class UserListView(ListAPIView):
    """
    用户列表接口
    GET /api/auth/users/
    仅管理员可访问
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        """获取用户列表，支持状态筛选"""
        queryset = User.objects.all().order_by('-date_joined')

        # 支持状态筛选
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset

    def list(self, request, *args, **kwargs):
        """统一响应格式"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })


class UserRoleUpdateView(UpdateAPIView):
    """
    用户角色更新接口
    PUT /api/auth/users/{id}/role/
    仅管理员可访问
    """
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        """排除当前管理员自己"""
        return User.objects.exclude(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 更新角色
        old_role = instance.get_role_display()
        instance.role = serializer.validated_data['role']
        instance.save()

        new_role = instance.get_role_display()

        return Response({
            'code': 0,
            'message': f'用户 {instance.real_name} 的角色已从 "{old_role}" 更新为 "{new_role}"'
        })


class UserStatusUpdateView(UpdateAPIView):
    """
    用户状态更新接口
    PUT /api/auth/users/{id}/status/
    仅管理员可访问
    """
    serializer_class = UserStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        """排除当前管理员自己"""
        return User.objects.exclude(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 更新状态
        new_status = serializer.validated_data['is_active']
        instance.is_active = new_status
        instance.save()

        status_text = '启用' if new_status else '禁用'

        return Response({
            'code': 0,
            'message': f'用户 {instance.real_name} 已{status_text}'
        })
