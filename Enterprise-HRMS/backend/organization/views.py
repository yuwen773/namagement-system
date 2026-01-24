from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import ProtectedError

from HRMS.permissions import IsHROrAdminOrReadOnly
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

    权限：登录用户可查看，HR/Admin 可管理
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsHROrAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "tree":
            return DepartmentTreeSerializer
        return DepartmentSerializer

    def list(self, request, *args, **kwargs):
        """获取部门列表（支持分页和查询条件）"""
        queryset = self.get_queryset()

        # 只获取根部门
        only_root = request.query_params.get("only_root", None)
        if only_root == "true":
            queryset = queryset.filter(parent__isnull=True)

        # 按名称搜索
        keyword = request.query_params.get("keyword")
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        # 只获取启用的
        only_active = request.query_params.get("only_active", None)
        if only_active == "true":
            queryset = queryset.filter(is_active=True)

        # 分页
        total = queryset.count()
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
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

    权限：登录用户可查看，HR/Admin 可管理
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsHROrAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        """获取岗位列表（支持分页和查询条件）"""
        queryset = self.get_queryset()

        # 只获取启用的岗位
        only_active = request.query_params.get("only_active", None)
        if only_active == "true":
            queryset = queryset.filter(is_active=True)

        # 按名称搜索
        keyword = request.query_params.get("keyword")
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        # 分页
        total = queryset.count()
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
