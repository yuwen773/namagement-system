from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer


class RegisterView(viewsets.GenericViewSet):
    """用户注册视图"""
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def create(self, request):
        """POST /api/auth/register/ - 创建新用户"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'code': 0,
            'message': '注册成功',
            'data': UserSerializer(user, context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)


class UserDetailView(viewsets.GenericViewSet):
    """当前用户信息视图"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_me(self, request):
        """GET /api/auth/me/ - 获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def update_me(self, request):
        """PUT/PATCH /api/auth/me/ - 修改当前用户信息"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'code': 0,
            'message': '更新成功',
            'data': serializer.data
        })


class IsAdminRole(permissions.BasePermission):
    """自定义权限：检查 role 字段是否为 admin"""
    message = "您没有执行该操作的权限。"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class UserListView(viewsets.GenericViewSet):
    """用户管理视图（仅管理员）"""
    permission_classes = [IsAdminRole]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        """GET /api/auth/users/ - 获取用户列表（支持分页和筛选）"""
        queryset = self.get_queryset()

        # 搜索
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(username__icontains=search)

        # 角色筛选
        role = request.query_params.get('role', '')
        if role:
            queryset = queryset.filter(role=role)

        # 状态筛选
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # 创建时间范围筛选
        created_at_after = request.query_params.get('created_at_after')
        created_at_before = request.query_params.get('created_at_before')
        if created_at_after:
            queryset = queryset.filter(created_at__gte=created_at_after)
        if created_at_before:
            queryset = queryset.filter(created_at__lte=created_at_before)

        # 排序
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering in ['created_at', '-created_at', 'username', '-username']:
            queryset = queryset.order_by(ordering)

        # 分页
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            page_size = min(page_size, 100)
        except (ValueError, TypeError):
            page, page_size = 1, 20

        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total
        })

    def retrieve(self, request, pk=None):
        """GET /api/auth/users/<id>/ - 获取单个用户"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def update(self, request, pk=None):
        """PUT/PATCH /api/auth/users/<id>/ - 更新用户"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'code': 0,
            'message': '更新成功',
            'data': serializer.data
        })

    def destroy(self, request, pk=None):
        """DELETE /api/auth/users/<id>/ - 删除用户"""
        instance = self.get_object()
        instance.delete()
        return Response({
            'code': 0,
            'message': '删除成功'
        }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        """POST /api/auth/users/create/ - 管理员创建用户"""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'code': 0,
            'message': '创建成功',
            'data': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
