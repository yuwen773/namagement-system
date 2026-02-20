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
        """只返回启用的公告"""
        return Notice.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        """获取公告列表"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"code": 0, "data": serializer.data, "total": queryset.count()})

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
