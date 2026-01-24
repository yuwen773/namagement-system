from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import ProtectedError
from .models import Department, Post
from .serializers import DepartmentSerializer, DepartmentTreeSerializer, PostSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    部门管理 ViewSet
    - list: 获取部门列表（扁平）
    - retrieve: 获取单个部门详情
    - create: 创建部门
    - update: 更新部门
    - partial_update: 部分更新
    - destroy: 删除部门（检查保护）
    - tree: 获取树形结构
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_serializer_class(self):
        if self.action == "tree":
            return DepartmentTreeSerializer
        return DepartmentSerializer

    def list(self, request, *args, **kwargs):
        """获取部门列表，可选只获取根部门"""
        queryset = self.get_queryset()
        only_root = request.query_params.get("only_root", None)
        if only_root == "true":
            queryset = queryset.filter(parent__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @action(detail=False, methods=["get"])
    def tree(self, request):
        """获取树形结构部门列表"""
        # 获取所有根部门及其子部门
        roots = Department.objects.filter(parent__isnull=True, is_active=True)
        serializer = self.get_serializer(roots, many=True)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """删除部门前检查是否存在子部门或关联员工"""
        instance = self.get_object()
        try:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {"detail": "无法删除：该部门存在子部门或关联员工"},
                status=status.HTTP_400_BAD_REQUEST
            )


class PostViewSet(viewsets.ModelViewSet):
    """
    岗位管理 ViewSet
    - list: 获取岗位列表
    - retrieve: 获取单个岗位详情
    - create: 创建岗位
    - update: 更新岗位
    - partial_update: 部分更新
    - destroy: 删除岗位
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        """获取岗位列表，可选只获取启用的岗位"""
        queryset = self.get_queryset()
        only_active = request.query_params.get("only_active", None)
        if only_active == "true":
            queryset = queryset.filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })
