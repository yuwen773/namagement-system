from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import LeaveRequest
from .serializers import (
    LeaveRequestSerializer,
    LeaveRequestListSerializer,
    LeaveRequestCreateSerializer,
    LeaveRequestApprovalSerializer,
    LeaveRequestMySerializer,
)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    请假申请视图集
    """
    queryset = LeaveRequest.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'leave_type', 'status']
    search_fields = ['employee__name', 'employee__phone', 'reason', 'approval_remark']
    ordering_fields = ['created_at', 'start_time', 'end_time']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """根据操作选择序列化器"""
        if self.action == 'list':
            return LeaveRequestListSerializer
        elif self.action == 'create':
            return LeaveRequestCreateSerializer
        elif self.action == 'my_requests':
            return LeaveRequestMySerializer
        elif self.action == 'approve':
            return LeaveRequestApprovalSerializer
        return LeaveRequestSerializer

    def create(self, request, *args, **kwargs):
        """创建请假申请，返回统一格式"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 返回完整的请假申请信息
        instance = serializer.instance
        response_serializer = LeaveRequestSerializer(instance)

        return Response({
            'code': 200,
            'message': '请假申请提交成功',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """获取详情，返回统一格式"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def list(self, request, *args, **kwargs):
        """获取列表，返回统一格式"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        """更新请假申请，返回统一格式"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'code': 200,
            'message': '更新成功',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """删除请假申请，返回统一格式"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'code': 200,
            'message': '删除成功'
        })

    @action(detail=False, methods=['get'], url_path='my-requests')
    def my_requests(self, request):
        """
        我的请假申请接口
        查询当前员工的请假记录
        """
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return Response({
                'code': 400,
                'message': '缺少 employee_id 参数'
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.queryset.filter(employee_id=employee_id)

        # 筛选参数
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        queryset = queryset.order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='pending')
    def pending(self, request):
        """
        待审批列表接口（管理员）
        查询所有待审批的请假申请
        """
        queryset = self.queryset.filter(status=LeaveRequest.Status.PENDING)
        queryset = queryset.order_by('-created_at')
        serializer = LeaveRequestListSerializer(queryset, many=True)

        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """
        请假审批接口（管理员）
        批准或拒绝请假申请
        """
        leave_request = self.get_object()

        # 检查状态
        if leave_request.status != LeaveRequest.Status.PENDING:
            return Response({
                'code': 400,
                'message': '该请假申请已被处理'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        approve = serializer.validated_data.get('approve')
        approval_remark = serializer.validated_data.get('approval_remark', '')

        # 获取审批人（从请求中获取，后续从 token 中获取）
        approver_id = request.data.get('approver_id')

        if approve:
            # 批准
            leave_request.status = LeaveRequest.Status.APPROVED
        else:
            # 拒绝
            leave_request.status = LeaveRequest.Status.REJECTED

        leave_request.approval_remark = approval_remark

        if approver_id:
            try:
                from employees.models import EmployeeProfile
                approver = EmployeeProfile.objects.get(id=approver_id)
                leave_request.approver = approver
            except EmployeeProfile.DoesNotExist:
                pass

        leave_request.save()

        # 返回更新后的请假申请信息
        response_serializer = LeaveRequestSerializer(leave_request)

        return Response({
            'code': 200,
            'message': '审批成功',
            'data': response_serializer.data
        })
