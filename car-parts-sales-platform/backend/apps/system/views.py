"""
系统管理视图

包含系统配置、消息通知、操作日志的视图
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.utils import timezone

from utils.response import ApiResponse
from utils.pagination import StandardPagination
from .models import SystemConfig, Message, OperationLog
from .serializers import (
    SystemConfigSerializer,
    SystemConfigListSerializer,
    MessageSerializer,
    MessageListSerializer,
    MessageCreateSerializer,
    OperationLogSerializer,
    OperationLogListSerializer,
)


class SystemConfigViewSet(viewsets.ModelViewSet):
    """
    系统配置 ViewSet

    list: 获取配置列表
    retrieve: 获取配置详情
    create: 创建配置（管理员）
    update: 更新配置（管理员）
    partial_update: 部分更新（管理员）
    destroy: 删除配置（管理员）
    """
    queryset = SystemConfig.objects.all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'is_editable']
    search_fields = ['key', 'description']
    ordering_fields = ['category', 'key', 'created_at']
    ordering = ['category', 'key']

    def get_permissions(self):
        """只有管理员可以操作配置"""
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'list':
            return SystemConfigListSerializer
        return SystemConfigSerializer

    def list(self, request, *args, **kwargs):
        """获取配置列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取配置详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建配置"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(
            message='创建成功',
            data=serializer.data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新配置"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除配置"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')


class MessageViewSet(viewsets.ModelViewSet):
    """
    站内消息 ViewSet

    list: 获取消息列表
    retrieve: 获取消息详情
    create: 发送消息（管理员）
    update: 更新消息（管理员）
    destroy: 删除消息（管理员）
    my-messages: 获取当前用户的消息
    mark-read: 标记消息已读
    """

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['message_type', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """普通用户只能看自己的消息"""
        queryset = Message.objects.all()
        if not self.request.user.is_staff:
            # 非管理员只能看自己的消息或全员消息
            queryset = queryset.filter(
                models.Q(recipient=self.request.user) | models.Q(recipient__isnull=True)
            )
        return queryset

    def get_permissions(self):
        """不同操作不同权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return MessageListSerializer
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def list(self, request, *args, **kwargs):
        """获取消息列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取消息详情"""
        instance = self.get_object()
        # 标记为已读
        if instance.status != 'read':
            instance.status = 'read'
            instance.read_at = timezone.now()
            instance.save(update_fields=['status', 'read_at'])
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)

    @action(detail=False, methods=['get'], url_path='my-messages')
    def my_messages(self, request):
        """
        获取当前用户的消息

        查询参数：
        - status: 状态筛选（draft/sent/read）
        - message_type: 消息类型
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        """标记消息已读"""
        instance = self.get_object()
        instance.status = 'read'
        instance.read_at = timezone.now()
        instance.save(update_fields=['status', 'read_at'])
        serializer = self.get_serializer(instance)
        return ApiResponse.success(message='已标记为已读', data=serializer.data)

    def create(self, request, *args, **kwargs):
        """发送消息"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 设置发送时间
        message = serializer.save()
        message.status = 'sent'
        message.sent_at = timezone.now()
        message.save(update_fields=['status', 'sent_at'])

        return ApiResponse.success(
            message='发送成功',
            data=MessageSerializer(message).data,
            code=201
        )

    def update(self, request, *args, **kwargs):
        """更新消息"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(message='更新成功', data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除消息"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='删除成功')


class OperationLogViewSet(viewsets.ModelViewSet):
    """
    操作日志 ViewSet（仅管理员可访问）

    list: 获取日志列表
    retrieve: 获取日志详情
    """

    queryset = OperationLog.objects.all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['action_type', 'object_type', 'status']
    search_fields = ['detail', 'object_type', 'object_id']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """只有管理员可以查看日志"""
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'list':
            return OperationLogListSerializer
        return OperationLogSerializer

    def list(self, request, *args, **kwargs):
        """获取日志列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取日志详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data)
