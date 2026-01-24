from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import ApprovalRequest
from .serializers import (
    ApprovalRequestSerializer,
    ApprovalRequestListSerializer,
    ApprovalRequestCreateSerializer
)
from HRMS.permissions import IsHROrAdmin, IsEmployeeOrHROrAdmin


class ApprovalRequestViewSet(viewsets.ModelViewSet):
    """
    审批请求 ViewSet

    list: 获取我的申请列表（普通员工看自己，人事/管理员看全部）
    create: 提交新申请
    retrieve: 获取申请详情
    update/partial_update: 更新申请（仅限待审批状态的自己创建的申请）
    destroy: 删除申请（仅限待审批状态的自己创建的申请）
    """

    queryset = ApprovalRequest.objects.all()
    permission_classes = [IsEmployeeOrHROrAdmin]

    def get_serializer_class(self):
        """动态选择序列化器"""
        if self.action == 'list':
            return ApprovalRequestListSerializer
        elif self.action in ['create']:
            return ApprovalRequestCreateSerializer
        return ApprovalRequestSerializer

    def get_queryset(self):
        """过滤查询集"""
        user = self.request.user
        queryset = ApprovalRequest.objects.select_related('user', 'approver')

        # 普通员工只能看自己的申请
        if user.role == 'employee':
            return queryset.filter(user=user)

        # 人事/管理员可以看全部
        return queryset

    def perform_create(self, serializer):
        """创建时自动设置用户"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        获取待审批列表（HR/Admin）
        """
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        # 待审批的申请
        queryset = ApprovalRequest.objects.filter(
            status='pending'
        ).select_related('user', 'approver').order_by('created_at')

        # 支持类型筛选
        type_filter = request.query_params.get('request_type')
        if type_filter:
            queryset = queryset.filter(request_type=type_filter)

        # 支持申请人筛选
        applicant = request.query_params.get('applicant')
        if applicant:
            queryset = queryset.filter(user__real_name__contains=applicant)

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ApprovalRequestListSerializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return Response({
                'code': 0,
                'data': paginated_data.get('results', []),
                'total': paginated_data.get('count', 0)
            })

        serializer = ApprovalRequestListSerializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        审批通过
        """
        approval_request = self.get_object()

        # 检查状态
        if approval_request.status != 'pending':
            return Response({
                'code': 400,
                'message': '该申请已审批，不能重复审批'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查权限
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        # 审批通过
        approval_request.status = 'approved'
        approval_request.approver = request.user
        approval_request.approver_reason = request.data.get('approver_reason', '')
        approval_request.save()

        serializer = ApprovalRequestSerializer(approval_request)
        return Response({
            'code': 0,
            'message': '审批通过',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        审批驳回
        """
        approval_request = self.get_object()

        # 检查状态
        if approval_request.status != 'pending':
            return Response({
                'code': 400,
                'message': '该申请已审批，不能重复审批'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查权限
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        # 审批驳回
        approval_request.status = 'rejected'
        approval_request.approver = request.user
        approval_request.approver_reason = request.data.get('approver_reason', '')
        approval_request.save()

        serializer = ApprovalRequestSerializer(approval_request)
        return Response({
            'code': 0,
            'message': '审批驳回',
            'data': serializer.data
        })

    def list(self, request, *args, **kwargs):
        """重写 list 方法，统一响应格式"""
        queryset = self.filter_queryset(self.get_queryset())

        # 支持状态筛选
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 支持类型筛选
        type_filter = request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(request_type=type_filter)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data).data
            return Response({
                'code': 0,
                'data': paginated_data.get('results', []),
                'total': paginated_data.get('count', 0),
                'page': int(request.query_params.get('page', 1)),
                'page_size': int(request.query_params.get('page_size', 10))
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
        })

    def retrieve(self, request, *args, **kwargs):
        """重写 retrieve 方法，统一响应格式"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """重写 create 方法，统一响应格式"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 返回完整详情
        instance = ApprovalRequest.objects.get(pk=serializer.instance.pk)
        output_serializer = ApprovalRequestSerializer(instance)

        return Response({
            'code': 0,
            'message': '申请提交成功',
            'data': output_serializer.data
        }, status=status.HTTP_201_CREATED)
