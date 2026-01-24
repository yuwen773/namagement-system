from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import EmployeeProfile
from .serializers import (
    EmployeeListSerializer,
    EmployeeProfileSerializer,
    EmployeeProfileCreateSerializer,
)


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    """
    员工档案 ViewSet
    """
    queryset = EmployeeProfile.objects.select_related('user', 'department', 'post')
    serializer_class = EmployeeProfileSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        if self.action == 'create':
            return EmployeeProfileCreateSerializer
        return EmployeeProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # 按状态筛选
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def list(self, request, *args, **kwargs):
        """获取员工列表"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    def retrieve(self, request, *args, **kwargs):
        """获取员工详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """创建员工档案（入职办理）"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
            'code': 0,
            'message': '入职办理成功',
            'data': EmployeeProfileSerializer(profile).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """获取待入职用户列表（未关联档案的用户）"""
        from accounts.models import User
        from django.db.models import Q

        # 查找没有 profile 的用户
        pending_users = User.objects.filter(
            profile__isnull=True
        ).order_by('-date_joined')

        return Response({
            'code': 0,
            'data': [{
                'id': user.id,
                'username': user.username,
                'real_name': user.real_name,
                'phone': user.phone,
                'email': user.email,
                'date_joined': user.date_joined,
            } for user in pending_users],
            'total': pending_users.count()
        })
