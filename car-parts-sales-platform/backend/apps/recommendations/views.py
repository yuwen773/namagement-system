"""
推荐管理视图
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from utils.response import ApiResponse
from utils.pagination import StandardPagination
from .models import RecommendationRule, RecommendedProduct
from .serializers import (
    RecommendationRuleSerializer,
    RecommendationRuleDetailSerializer,
    RecommendedProductSerializer,
    RecommendedProductCreateSerializer
)


class RecommendationRuleViewSet(viewsets.ModelViewSet):
    """
    推荐规则管理 ViewSet

    list: 获取推荐规则列表
    retrieve: 获取规则详情（包含关联商品）
    create: 创建推荐规则（管理员）
    update: 更新推荐规则（管理员）
    partial_update: 部分更新（管理员）
    destroy: 删除推荐规则（管理员）
    """
    queryset = RecommendationRule.objects.all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rule_type', 'is_active']
    ordering_fields = ['priority', 'created_at']
    ordering = ['-priority', '-created_at']

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecommendationRuleDetailSerializer
        return RecommendationRuleSerializer

    def list(self, request, *args, **kwargs):
        """获取推荐规则列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取规则详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建推荐规则"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新推荐规则"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除推荐规则"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')

    @action(detail=False, methods=['get'])
    def active(self, request):
        """获取启用的推荐规则"""
        rules = RecommendationRule.objects.filter(is_active=True).order_by('-priority')
        serializer = self.get_serializer(rules, many=True)
        return ApiResponse.success(data=serializer.data)


class RecommendedProductViewSet(viewsets.ModelViewSet):
    """
    推荐商品管理 ViewSet

    list: 获取推荐商品列表
    retrieve: 获取推荐商品详情
    create: 添加推荐商品（管理员）
    update: 更新推荐商品（管理员）
    partial_update: 部分更新（管理员）
    destroy: 删除推荐商品（管理员）
    """
    queryset = RecommendedProduct.objects.select_related('rule', 'product')
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rule']
    ordering_fields = ['sort_order', 'created_at']
    ordering = ['-sort_order', '-created_at']

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecommendedProductCreateSerializer
        return RecommendedProductSerializer

    def list(self, request, *args, **kwargs):
        """获取推荐商品列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取推荐商品详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """添加推荐商品"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='添加成功',
            data=RecommendedProductSerializer(serializer.instance).data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新推荐商品"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=RecommendedProductSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        """删除推荐商品"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')
