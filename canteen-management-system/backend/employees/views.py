from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import EmployeeProfile
from .serializers import (
    EmployeeProfileSerializer,
    EmployeeProfileListSerializer
)
from utils.response import ApiResponse
from utils.pagination import StandardPagination


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """
    员工档案视图集
    提供员工档案的 CRUD 操作和筛选功能
    """
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['position', 'status']
    search_fields = ['name', 'phone', 'id_card']
    ordering_fields = ['created_at', 'entry_date', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        根据不同的操作返回不同的序列化器
        """
        if self.action == 'list':
            return EmployeeProfileListSerializer
        return EmployeeProfileSerializer

    def list(self, request, *args, **kwargs):
        """
        员工档案列表接口
        GET /api/employees/
        支持筛选：position, status
        支持搜索：name, phone, id_card
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """
        员工档案详情接口
        GET /api/employees/{id}/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """
        创建员工档案接口
        POST /api/employees/
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='创建成功', code=201)

        return ApiResponse.error(message='创建失败', errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        """
        更新员工档案接口
        PUT /api/employees/{id}/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='更新成功')

        return ApiResponse.error(message='更新失败', errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """
        删除员工档案接口
        DELETE /api/employees/{id}/
        """
        instance = self.get_object()
        instance.delete()
        return ApiResponse.success(message='删除成功')
