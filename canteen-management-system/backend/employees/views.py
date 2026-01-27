from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import EmployeeProfile
from .serializers import (
    EmployeeProfileSerializer,
    EmployeeProfileListSerializer
)


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """
    员工档案视图集
    提供员工档案的 CRUD 操作和筛选功能
    """
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
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
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        """
        员工档案详情接口
        GET /api/employees/{id}/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        创建员工档案接口
        POST /api/employees/
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 201,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'code': 400,
            'message': '创建失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        更新员工档案接口
        PUT /api/employees/{id}/
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'code': 200,
                'message': '更新成功',
                'data': serializer.data
            })

        return Response({
            'code': 400,
            'message': '更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        删除员工档案接口
        DELETE /api/employees/{id}/
        """
        instance = self.get_object()
        instance.delete()
        return Response({
            'code': 200,
            'message': '删除成功'
        })
