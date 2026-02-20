from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notice
from .serializers import NoticeSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """仅管理员可写，普通用户可读"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'


class NoticeViewSet(viewsets.ModelViewSet):
    """公告 CRUD API"""
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """根据用户角色返回不同范围的公告"""
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'admin':
            # 管理员可以看到全部公告
            return Notice.objects.all()
        # 普通用户只看启用公告
        return Notice.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        """获取公告列表（支持分页和筛选）"""
        queryset = self.get_queryset()

        # 搜索
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(title__icontains=search)

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
        if ordering in ['created_at', '-created_at', 'title', '-title']:
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

    def retrieve(self, request, *args, **kwargs):
        """获取公告详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 0, "data": serializer.data})

    def create(self, request, *args, **kwargs):
        """创建公告"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"code": 0, "data": serializer.data, "message": "创建成功"}, status=201)

    def update(self, request, *args, **kwargs):
        """更新公告"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"code": 0, "data": serializer.data, "message": "更新成功"})

    def destroy(self, request, *args, **kwargs):
        """删除公告"""
        instance = self.get_object()
        instance.delete()
        return Response({"code": 0, "message": "删除成功"})
