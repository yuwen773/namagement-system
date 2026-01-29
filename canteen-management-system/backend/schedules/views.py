from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from datetime import timedelta

from .models import Shift, Schedule, ShiftSwapRequest
from .serializers import (
    ShiftSerializer, ShiftListSerializer,
    ScheduleSerializer, ScheduleListSerializer, ScheduleDetailSerializer,
    BatchScheduleSerializer,
    ShiftSwapRequestSerializer, ShiftSwapRequestListSerializer,
    ShiftSwapApprovalSerializer, CalendarViewSerializer
)
from utils.response import ApiResponse
from utils.pagination import StandardPagination


class ShiftViewSet(viewsets.ModelViewSet):
    """
    班次定义视图集
    提供班次的增删改查操作
    """
    queryset = Shift.objects.all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['start_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return ShiftListSerializer
        return ShiftSerializer

    def list(self, request, *args, **kwargs):
        """获取班次列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """获取班次详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """创建班次"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.success(data=serializer.data, message='班次创建成功', code=201)

    def update(self, request, *args, **kwargs):
        """更新班次"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(data=serializer.data, message='班次更新成功')

    def destroy(self, request, *args, **kwargs):
        """删除班次"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='班次删除成功')


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    排班计划视图集
    提供排班的增删改查、批量排班和日历视图功能
    """
    queryset = Schedule.objects.select_related('employee', 'shift').all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'shift', 'work_date', 'is_swapped']
    search_fields = ['employee__name', 'employee__phone']
    ordering_fields = ['work_date', 'created_at']
    ordering = ['-work_date', 'shift__start_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return ScheduleListSerializer
        elif self.action == 'retrieve':
            return ScheduleDetailSerializer
        return ScheduleSerializer

    def list(self, request, *args, **kwargs):
        """获取排班列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """获取排班详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """创建排班"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 检查是否创建成功
        if serializer.data:
            return ApiResponse.success(data=serializer.data, message='排班创建成功', code=201)
        return ApiResponse.error(message='排班创建失败')

    def update(self, request, *args, **kwargs):
        """更新排班"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(data=serializer.data, message='排班更新成功')

    def destroy(self, request, *args, **kwargs):
        """删除排班"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='排班删除成功')

    @action(detail=False, methods=['post'])
    def batch_create(self, request):
        """
        批量排班接口
        一次为多个员工在日期范围内创建排班
        如果排班已存在，根据 force_update 参数决定是否更新
        """
        serializer = BatchScheduleSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(message='参数验证失败', errors=serializer.errors)

        data = serializer.validated_data
        employee_ids = data['employee_ids']
        shift_id = data['shift_id']
        start_date = data['start_date']
        end_date = data['end_date']
        force_update = data.get('force_update', True)

        # 计算日期范围内的所有日期
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            current_date += timedelta(days=1)

        # 批量创建排班记录
        created_count = 0
        updated_count = 0
        skipped_count = 0
        errors = []

        shift = Shift.objects.get(id=shift_id)

        for employee_id in employee_ids:
            for work_date in date_range:
                try:
                    # 尝试获取已存在的排班
                    existing_schedule = Schedule.objects.filter(
                        employee_id=employee_id,
                        work_date=work_date
                    ).first()

                    if existing_schedule:
                        # 排班已存在
                        if force_update:
                            # 检查班次是否相同
                            if existing_schedule.shift_id != shift_id:
                                existing_schedule.shift_id = shift_id
                                existing_schedule.save()
                                updated_count += 1
                            else:
                                skipped_count += 1
                        else:
                            skipped_count += 1
                    else:
                        # 创建新排班
                        Schedule.objects.create(
                            employee_id=employee_id,
                            shift_id=shift_id,
                            work_date=work_date
                        )
                        created_count += 1
                except Exception as e:
                    errors.append(f'员工 {employee_id} 在 {work_date} 排班失败: {str(e)}')

        result = {
            'created_count': created_count,
            'updated_count': updated_count,
            'skipped_count': skipped_count,
            'total_dates': len(date_range),
            'total_employees': len(employee_ids)
        }
        if errors:
            result['errors'] = errors[:5]  # 只返回前5个错误

        # 构建更详细的消息
        message_parts = []
        if created_count > 0:
            message_parts.append(f'创建 {created_count} 条')
        if updated_count > 0:
            message_parts.append(f'更新 {updated_count} 条')
        if skipped_count > 0:
            message_parts.append(f'跳过 {skipped_count} 条')

        message = '批量排班完成' + ('，' + '、'.join(message_parts) if message_parts else '')
        if not message_parts:
            message = '批量排班完成，但没有处理任何记录'

        return ApiResponse.success(data=result, message=message)

    @action(detail=False, methods=['post'])
    def calendar_view(self, request):
        """
        日历视图接口
        返回指定日期范围的排班数据，用于日历组件展示
        """
        serializer = CalendarViewSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(message='参数验证失败', errors=serializer.errors)

        data = serializer.validated_data
        start_date = data['start_date']
        end_date = data['end_date']
        employee_id = data.get('employee_id')

        # 构建查询条件
        filters = Q(work_date__gte=start_date) & Q(work_date__lte=end_date)
        if employee_id:
            filters &= Q(employee_id=employee_id)

        # 查询排班记录
        schedules = Schedule.objects.filter(filters).select_related('employee', 'shift')

        # 按日期分组返回数据
        result = {}
        for schedule in schedules:
            date_str = schedule.work_date.strftime('%Y-%m-%d')
            if date_str not in result:
                result[date_str] = []

            result[date_str].append({
                'id': schedule.id,
                'employee_id': schedule.employee_id,
                'employee_name': schedule.employee.name,
                'employee_position': schedule.employee.get_position_display(),
                'position_display': schedule.employee.get_position_display(),
                'shift_id': schedule.shift_id,
                'shift_name': schedule.shift.name,
                'start_time': schedule.shift.start_time.strftime('%H:%M'),
                'end_time': schedule.shift.end_time.strftime('%H:%M'),
                'work_date': date_str,
                'is_swapped': schedule.is_swapped
            })

        return ApiResponse.success(data={
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'schedules': result,
            'total_count': len(schedules)
        })


class ShiftSwapRequestViewSet(viewsets.ModelViewSet):
    """
    调班申请视图集
    提供调班申请的增删改查和审批功能
    """
    queryset = ShiftSwapRequest.objects.select_related(
        'requester', 'original_schedule', 'original_schedule__shift',
        'target_shift', 'approver'
    ).all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['requester', 'status', 'target_date']
    search_fields = ['requester__name', 'reason']
    ordering_fields = ['created_at', 'target_date']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ShiftSwapRequestListSerializer
        return ShiftSwapRequestSerializer

    def list(self, request, *args, **kwargs):
        """获取调班申请列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """获取调班申请详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """创建调班申请"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 验证原定排班是否属于当前用户
        original_schedule = serializer.validated_data['original_schedule']
        if request.data.get('requester_id'):
            # 管理员可以代为创建
            requester_id = request.data.get('requester_id')
            from employees.models import EmployeeProfile
            requester = EmployeeProfile.objects.get(id=requester_id)
            serializer.validated_data['requester'] = requester
        else:
            # 员工自己创建
            # TODO: 这里需要从 token 中获取当前登录用户信息
            # 暂时跳过此验证
            pass

        self.perform_create(serializer)
        return ApiResponse.success(data=serializer.data, message='调班申请提交成功', code=201)

    def update(self, request, *args, **kwargs):
        """更新调班申请"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(data=serializer.data, message='调班申请更新成功')

    def destroy(self, request, *args, **kwargs):
        """删除调班申请"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='调班申请删除成功')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        调班审核接口
        批准或拒绝调班申请
        """
        swap_request = self.get_object()

        # 检查当前申请状态
        if swap_request.status != 'PENDING':
            return ApiResponse.error(
                message=f'该申请已被{swap_request.get_status_display()}，无法重复操作'
            )

        # 验证审批参数
        serializer = ShiftSwapApprovalSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.error(message='参数验证失败', errors=serializer.errors)

        data = serializer.validated_data
        approve_status = data['approve']
        approval_remark = data.get('approval_remark', '')

        # 更新申请状态
        swap_request.status = approve_status
        swap_request.approval_remark = approval_remark

        # TODO: 这里需要从 token 中获取当前登录管理员信息
        # swap_request.approver = current_admin_user

        swap_request.save()

        # 如果批准，更新排班记录
        if approve_status == 'APPROVED':
            original_schedule = swap_request.original_schedule

            # 检查目标日期是否已有排班
            existing_schedule = Schedule.objects.filter(
                employee=swap_request.requester,
                work_date=swap_request.target_date
            ).first()

            if existing_schedule:
                # 如果已有排班，更新班次
                existing_schedule.shift = swap_request.target_shift
                existing_schedule.is_swapped = True
                existing_schedule.save()

                # 标记原排班为已调班
                original_schedule.is_swapped = True
                original_schedule.save()
            else:
                # 如果没有排班，删除原排班，创建新排班
                original_work_date = original_schedule.work_date

                # 删除原排班
                original_schedule.delete()

                # 创建新排班
                Schedule.objects.create(
                    employee=swap_request.requester,
                    shift=swap_request.target_shift,
                    work_date=swap_request.target_date,
                    is_swapped=True
                )

        return ApiResponse.success(
            data=ShiftSwapRequestSerializer(swap_request).data,
            message=f'调班申请已{swap_request.get_status_display()}'
        )

    @action(detail=False, methods=['get'])
    def my_requests(self, request):
        """
        我的调班申请接口
        返回当前登录员工的所有调班申请
        """
        # TODO: 这里需要从 token 中获取当前登录用户信息
        # 暂时返回所有记录
        employee_id = request.query_params.get('employee_id')

        if not employee_id:
            return ApiResponse.error(message='请提供员工ID')

        requests = self.queryset.filter(requester_id=employee_id)
        page = self.paginate_queryset(requests)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(requests, many=True)
        return ApiResponse.success(data=serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        待审批调班申请列表
        管理员查看所有待审批的调班申请
        """
        pending_requests = self.queryset.filter(status='PENDING')
        page = self.paginate_queryset(pending_requests)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(pending_requests, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')
