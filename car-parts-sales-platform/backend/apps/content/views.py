"""
内容管理视图
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from utils.response import ApiResponse
from utils.pagination import StandardPagination
from .models import ModificationCase, FAQ
from .serializers import (
    ModificationCaseListSerializer,
    ModificationCaseDetailSerializer,
    ModificationCaseCreateSerializer,
    FAQSerializer
)


class ModificationCaseViewSet(viewsets.ModelViewSet):
    """
    改装案例管理 ViewSet

    list: 获取案例列表（只显示已发布的）
    retrieve: 获取案例详情
    create: 创建案例（管理员）
    update: 更新案例（管理员）
    partial_update: 部分更新（管理员）
    destroy: 删除案例（管理员）
    """
    queryset = ModificationCase.objects.all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'summary', 'content', 'author']
    ordering_fields = ['sort_order', 'published_at', 'view_count', 'created_at']
    ordering = ['-sort_order', '-published_at', '-created_at']

    def get_queryset(self):
        """普通用户只看已发布的案例"""
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(status='published')
        return queryset

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return ModificationCaseListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ModificationCaseCreateSerializer
        return ModificationCaseDetailSerializer

    def list(self, request, *args, **kwargs):
        """获取案例列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取案例详情"""
        instance = self.get_object()
        # 增加浏览量
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建案例"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=ModificationCaseDetailSerializer(serializer.instance).data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新案例"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=ModificationCaseDetailSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        """删除案例"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')


class FAQViewSet(viewsets.ModelViewSet):
    """
    常见问题管理 ViewSet

    list: 获取问题列表（只显示启用的）
    retrieve: 获取问题详情
    create: 创建问题（管理员）
    update: 更新问题（管理员）
    partial_update: 部分更新（管理员）
    destroy: 删除问题（管理员）
    """
    queryset = FAQ.objects.all()
    pagination_class = StandardPagination
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['question', 'answer']
    ordering_fields = ['category', 'sort_order', 'created_at']
    ordering = ['category', 'sort_order', '-created_at']

    def get_queryset(self):
        """普通用户只看启用的问题"""
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def list(self, request, *args, **kwargs):
        """获取问题列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取问题详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建问题"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新问题"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除问题"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')
