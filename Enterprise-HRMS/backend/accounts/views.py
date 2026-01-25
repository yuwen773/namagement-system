from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, GenericAPIView, RetrieveAPIView
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


class CurrentUserView(RetrieveAPIView):
    """
    获取当前登录用户信息
    GET /api/auth/me/
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({
            'code': 0,
            'data': serializer.data
        })


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


from rest_framework import viewsets, status
from rest_framework.decorators import action
from HRMS.permissions import IsHROrAdmin
from .models import UserEditRequest
from .serializers import (
    UserEditRequestCreateSerializer, UserEditRequestSerializer,
    UserEditRequestListSerializer, UserEditRequestActionSerializer
)


class UserEditRequestViewSet(viewsets.ModelViewSet):
    """
    信息修改申请 ViewSet
    提供 CRUD 和审批操作
    """
    queryset = UserEditRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """根据 action 选择不同的序列化器"""
        if self.action == 'list':
            return UserEditRequestListSerializer
        elif self.action == 'create':
            return UserEditRequestCreateSerializer
        elif self.action in ['approve', 'reject']:
            return UserEditRequestActionSerializer
        return UserEditRequestSerializer

    def get_queryset(self):
        """过滤查询集"""
        user = self.request.user

        # 普通员工只能看自己的申请
        if user.role == 'employee':
            return UserEditRequest.objects.filter(user=user)

        # HR/Admin 可以看所有待审批申请
        return UserEditRequest.objects.all()

    def get_object(self):
        """获取对象并检查权限"""
        obj = super().get_object()

        # 普通员工只能操作自己的申请
        if self.request.user.role == 'employee' and obj.user != self.request.user:
            self.permission_denied(self.request)

        return obj

    def create(self, request, *args, **kwargs):
        """创建修改申请"""
        user = request.user
        edit_type = request.data.get('edit_type')
        new_value = request.data.get('new_value')

        # 获取旧值
        if edit_type == 'phone':
            old_value = user.phone
        elif edit_type == 'email':
            old_value = user.email
        else:
            old_value = ''

        # 检查是否有待审批的同类申请
        pending = UserEditRequest.objects.filter(
            user=user,
            edit_type=edit_type,
            status='pending'
        ).exists()

        if pending:
            return Response({
                'code': 400,
                'message': '您已有一条待审批的同类申请，请等待审批完成后再提交'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 创建申请
        edit_request = UserEditRequest.objects.create(
            user=user,
            edit_type=edit_type,
            old_value=old_value,
            new_value=new_value,
            reason=request.data.get('reason', '')
        )

        return Response({
            'code': 201,
            'message': '修改申请已提交，请等待审批',
            'data': UserEditRequestSerializer(edit_request).data
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """获取申请列表"""
        queryset = self.get_queryset()

        # 支持状态筛选
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 支持类型筛选
        type_filter = request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(edit_type=type_filter)

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

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        待审批列表（HR/Admin 专用）
        GET /api/auth/edit-requests/pending/
        """
        # 只有 HR/Admin 可以访问
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '只有人事或管理员可以访问此接口'
            }, status=status.HTTP_403_FORBIDDEN)

        queryset = UserEditRequest.objects.filter(status='pending')

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

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        审批通过
        POST /api/auth/edit-requests/{id}/approve/
        """
        edit_request = self.get_object()

        # 只有 HR/Admin 可以审批
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '只有人事或管理员可以审批申请'
            }, status=status.HTTP_403_FORBIDDEN)

        if edit_request.status != 'pending':
            return Response({
                'code': 400,
                'message': '该申请已审批，不能重复审批'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 审批通过，更新用户信息
        user = edit_request.user
        if edit_request.edit_type == 'phone':
            user.phone = edit_request.new_value
        elif edit_request.edit_type == 'email':
            user.email = edit_request.new_value

        user.save()

        # 更新申请状态
        edit_request.status = 'approved'
        edit_request.reviewer = request.user
        edit_request.reviewer_comment = request.data.get('reviewer_comment', '')
        edit_request.save()

        return Response({
            'code': 0,
            'message': f'已批准 {user.real_name} 的{edit_request.get_edit_type_display()}修改申请'
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        审批驳回
        POST /api/auth/edit-requests/{id}/reject/
        """
        edit_request = self.get_object()

        # 只有 HR/Admin 可以审批
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '只有人事或管理员可以审批申请'
            }, status=status.HTTP_403_FORBIDDEN)

        if edit_request.status != 'pending':
            return Response({
                'code': 400,
                'message': '该申请已审批，不能重复审批'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新申请状态
        edit_request.status = 'rejected'
        edit_request.reviewer = request.user
        edit_request.reviewer_comment = request.data.get('reviewer_comment', '')
        edit_request.save()

        return Response({
            'code': 0,
            'message': f'已驳回 {edit_request.user.real_name} 的{edit_request.get_edit_type_display()}修改申请'
        })
