from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum, Q, Count
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import SalaryRecord, Appeal
from .serializers import (
    SalaryRecordSerializer, SalaryRecordListSerializer,
    SalaryRecordCreateSerializer, SalaryGenerateSerializer,
    SalaryAdjustSerializer, AppealSerializer, AppealListSerializer,
    AppealCreateSerializer, AppealApprovalSerializer, MyAppealSerializer
)
from employees.models import EmployeeProfile
from schedules.models import Schedule
from attendance.models import AttendanceRecord
from leaves.models import LeaveRequest
from utils.response import ApiResponse
from utils.pagination import StandardPagination
from utils.constants import (
    POSITION_ALLOWANCE_MAP,
    DEFAULT_BASE_SALARY,
    DAYS_PER_MONTH,
    HOURS_PER_DAY,
    OVERTIME_RATE,
    LATE_DEDUCTION,
    MISSING_DEDUCTION,
    SALARY_STATUS_DRAFT,
    SALARY_STATUS_PUBLISHED,
    SALARY_STATUS_ADJUSTED,
    SALARY_STATUS_APPEALED,
)


def get_position_allowance(position):
    """获取岗位津贴"""
    return Decimal(str(POSITION_ALLOWANCE_MAP.get(position, 0)))


def calculate_daily_salary(base_salary):
    """计算日工资"""
    return Decimal(str(base_salary)) / Decimal(str(DAYS_PER_MONTH))


def calculate_hourly_salary(daily_salary):
    """计算时薪"""
    return daily_salary / Decimal(str(HOURS_PER_DAY))


def calculate_overtime_pay(overtime_hours, base_salary):
    """计算加班费"""
    daily_salary = calculate_daily_salary(base_salary)
    hourly_salary = calculate_hourly_salary(daily_salary)
    return hourly_salary * Decimal(str(OVERTIME_RATE)) * Decimal(str(overtime_hours))


def calculate_late_deduction(late_count):
    """计算迟到扣款"""
    return Decimal(str(late_count)) * Decimal(str(LATE_DEDUCTION))


def calculate_missing_deduction(missing_count):
    """计算缺卡扣款"""
    return Decimal(str(missing_count)) * Decimal(str(MISSING_DEDUCTION))


class SalaryRecordViewSet(viewsets.ModelViewSet):
    """薪资记录视图集"""
    queryset = SalaryRecord.objects.select_related('employee').all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'year_month', 'status']
    search_fields = ['employee__name', 'employee__phone']
    ordering_fields = ['created_at', 'year_month']
    ordering = ['-year_month', '-created_at']

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return SalaryRecordListSerializer
        elif self.action == 'create':
            return SalaryRecordCreateSerializer
        return SalaryRecordSerializer

    def list(self, request, *args, **kwargs):
        """获取薪资记录列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """获取薪资记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """创建薪资记录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 返回完整的薪资记录信息
        instance = serializer.instance
        response_serializer = SalaryRecordSerializer(instance)
        return ApiResponse.success(data=response_serializer.data, message='薪资记录创建成功', code=201)

    def update(self, request, *args, **kwargs):
        """更新薪资记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = SalaryRecordCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 返回完整的薪资记录信息
        response_serializer = SalaryRecordSerializer(instance)
        return ApiResponse.success(data=response_serializer.data, message='薪资记录更新成功')

    def destroy(self, request, *args, **kwargs):
        """删除薪资记录"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='薪资记录删除成功')

    @action(detail=False, methods=['post'], url_path='generate')
    def generate_salary(self, request):
        """
        薪资生成接口
        根据考勤数据自动计算月薪
        """
        serializer = SalaryGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        year_month = serializer.validated_data['year_month']
        employee_ids = serializer.validated_data.get('employee_ids')

        # 验证年月格式
        try:
            year, month = map(int, year_month.split('-'))
            if month < 1 or month > 12:
                raise ValueError
        except (ValueError, AttributeError):
            return Response({
                'code': 400,
                'message': '年月格式不正确，应为 YYYY-MM'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 计算该月的起始和结束日期
        if month == 12:
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            start_date = datetime(year, month, 1).date()
            end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)

        # 获取需要生成薪资的员工
        if employee_ids:
            employees = EmployeeProfile.objects.filter(id__in=employee_ids, status='ACTIVE')
        else:
            employees = EmployeeProfile.objects.filter(status='ACTIVE')

        created_count = 0
        skipped_count = 0
        errors = []

        for employee in employees:
            try:
                # 检查是否已存在薪资记录
                if SalaryRecord.objects.filter(employee=employee, year_month=year_month).exists():
                    skipped_count += 1
                    continue

                # 统计考勤数据
                attendance_records = AttendanceRecord.objects.filter(
                    employee=employee,
                    created_at__gte=start_date,
                    created_at__lte=end_date
                )

                # 统计迟到次数
                late_count = attendance_records.filter(status='LATE').count()

                # 统计缺卡次数
                missing_count = attendance_records.filter(status='MISSING').count()

                # 计算总加班时长
                overtime_hours_sum = attendance_records.aggregate(
                    total=Sum('overtime_hours')
                )['total'] or Decimal('0')

                # 统计出勤天数（有签到或签退记录的日期）
                work_days = attendance_records.filter(
                    Q(clock_in_time__isnull=False) | Q(clock_out_time__isnull=False)
                ).values('created_at__date').distinct().count()

                # 统计请假天数
                leave_days = LeaveRequest.objects.filter(
                    employee=employee,
                    status='APPROVED',
                    start_time__lte=end_date,
                    end_time__gte=start_date
                ).count()

                # 获取基本工资（可以从员工档案获取，这里使用默认值）
                base_salary = Decimal(str(DEFAULT_BASE_SALARY))

                # 计算各项薪资组成
                position_allowance = get_position_allowance(employee.position)
                overtime_pay = calculate_overtime_pay(float(overtime_hours_sum), float(base_salary))
                late_deduction = calculate_late_deduction(late_count)
                missing_deduction = calculate_missing_deduction(missing_count)
                total_deductions = late_deduction + missing_deduction

                # 创建薪资记录
                salary_record = SalaryRecord.objects.create(
                    employee=employee,
                    year_month=year_month,
                    base_salary=base_salary,
                    position_allowance=position_allowance,
                    overtime_pay=overtime_pay,
                    deductions=total_deductions,
                    work_days=work_days,
                    late_count=late_count,
                    missing_count=missing_count,
                    overtime_hours=overtime_hours_sum,
                    status='DRAFT'
                )

                # 自动计算实发工资（在 save 方法中完成）
                salary_record.save()
                created_count += 1

            except Exception as e:
                errors.append(f"员工 {employee.name} 薪资生成失败: {str(e)}")

        return ApiResponse.success(data={
            'created': created_count,
            'skipped': skipped_count,
            'errors': errors
        }, message='薪资生成完成')

    @action(detail=True, methods=['post'], url_path='adjust')
    def adjust_salary(self, request, pk=None):
        """
        薪资调整接口
        管理员手动调整薪资金额
        """
        instance = self.get_object()
        serializer = SalaryAdjustSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 获取调整参数
        base_salary = serializer.validated_data.get('base_salary')
        position_allowance = serializer.validated_data.get('position_allowance')
        overtime_pay = serializer.validated_data.get('overtime_pay')
        deductions = serializer.validated_data.get('deductions')
        reason = serializer.validated_data['reason']

        # 更新薪资字段
        if base_salary is not None:
            instance.base_salary = base_salary
        if position_allowance is not None:
            instance.position_allowance = position_allowance
        if overtime_pay is not None:
            instance.overtime_pay = overtime_pay
        if deductions is not None:
            instance.deductions = deductions

        # 更新备注
        if instance.remark:
            instance.remark += f"\n调整记录: {reason} ({timezone.now().strftime('%Y-%m-%d %H:%M')})"
        else:
            instance.remark = f"调整记录: {reason} ({timezone.now().strftime('%Y-%m-%d %H:%M')})"

        # 更新状态为已调整
        instance.status = 'ADJUSTED'
        instance.save()

        # 返回更新后的薪资记录
        response_serializer = SalaryRecordSerializer(instance)
        return ApiResponse.success(data=response_serializer.data, message='薪资调整成功')

    @action(detail=True, methods=['post'], url_path='publish')
    def publish_salary(self, request, pk=None):
        """
        发布薪资接口
        将薪资状态从草稿改为已发布
        """
        instance = self.get_object()

        if instance.status != 'DRAFT':
            return ApiResponse.error(message='只有草稿状态的薪资记录才能发布')

        instance.status = 'PUBLISHED'
        instance.save()

        response_serializer = SalaryRecordSerializer(instance)
        return ApiResponse.success(data=response_serializer.data, message='薪资发布成功')

    @action(detail=False, methods=['get'], url_path='my-salaries')
    def my_salaries(self, request):
        """
        我的薪资记录接口
        员工查询自己的薪资记录
        """
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return ApiResponse.error(message='请提供 employee_id 参数')

        queryset = self.queryset.filter(employee_id=employee_id)

        # 支持按年月筛选
        year_month = request.query_params.get('year_month')
        if year_month:
            queryset = queryset.filter(year_month=year_month)

        # 支持按状态筛选
        status_param = request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        queryset = queryset.order_by('-year_month')

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SalaryRecordSerializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = SalaryRecordSerializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='查询成功')


class AppealViewSet(viewsets.ModelViewSet):
    """异常申诉视图集"""
    queryset = Appeal.objects.select_related('employee', 'approver').all()
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['appeal_type', 'employee', 'status']
    search_fields = ['employee__name', 'reason', 'approval_remark']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return AppealListSerializer
        elif self.action == 'create':
            return AppealCreateSerializer
        return AppealSerializer

    def list(self, request, *args, **kwargs):
        """获取异常申诉列表"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """获取异常申诉详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """创建异常申诉"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 如果是薪资申诉，更新薪资记录状态为申诉中
        appeal = serializer.instance
        if appeal.appeal_type == 'SALARY':
            salary_record = SalaryRecord.objects.filter(id=appeal.target_id).first()
            if salary_record:
                salary_record.status = 'APPEALED'
                salary_record.save()

        # 返回完整的申诉信息
        response_serializer = AppealSerializer(appeal)
        return ApiResponse.success(data=response_serializer.data, message='申诉提交成功', code=201)

    def update(self, request, *args, **kwargs):
        """更新异常申诉"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = AppealCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_serializer = AppealSerializer(instance)
        return ApiResponse.success(data=response_serializer.data, message='申诉更新成功')

    def destroy(self, request, *args, **kwargs):
        """删除异常申诉"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(message='申诉删除成功')

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_appeal(self, request, pk=None):
        """
        申诉审批接口
        管理员批准或拒绝申诉
        """
        instance = self.get_object()

        if instance.status != 'PENDING':
            return ApiResponse.error(message='只有待审批状态的申诉才能审批')

        serializer = AppealApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        approve = serializer.validated_data['approve']
        approval_remark = serializer.validated_data.get('approval_remark', '')
        approver_id = request.data.get('approver_id')

        if not approver_id:
            return ApiResponse.error(message='请提供 approver_id（审批人ID）')

        try:
            approver = EmployeeProfile.objects.get(id=approver_id)
        except EmployeeProfile.DoesNotExist:
            return ApiResponse.error(message='审批人不存在')

        # 更新申诉状态
        instance.status = 'APPROVED' if approve else 'REJECTED'
        instance.approver = approver
        instance.approval_remark = approval_remark
        instance.save()

        # 如果是薪资申诉被拒绝，恢复薪资记录状态
        if instance.appeal_type == 'SALARY' and not approve:
            salary_record = SalaryRecord.objects.filter(id=instance.target_id).first()
            if salary_record:
                salary_record.status = 'PUBLISHED'
                salary_record.save()

        # 返回更新后的申诉信息
        response_serializer = AppealSerializer(instance)
        return ApiResponse.success(data=response_serializer.data, message='申诉审批完成')

    @action(detail=False, methods=['get'], url_path='pending')
    def pending_appeals(self, request):
        """
        待审批申诉列表
        管理员查看所有待审批的申诉
        """
        queryset = self.queryset.filter(status='PENDING')

        # 支持按申诉类型筛选
        appeal_type = request.query_params.get('appeal_type')
        if appeal_type:
            queryset = queryset.filter(appeal_type=appeal_type)

        queryset = queryset.order_by('-created_at')

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AppealListSerializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = AppealListSerializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='查询成功')

    @action(detail=False, methods=['get'], url_path='my-appeals')
    def my_appeals(self, request):
        """
        我的申诉接口
        员工查询自己的申诉记录
        """
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return ApiResponse.error(message='请提供 employee_id 参数')

        queryset = self.queryset.filter(employee_id=employee_id)

        # 支持按申诉类型筛选
        appeal_type = request.query_params.get('appeal_type')
        if appeal_type:
            queryset = queryset.filter(appeal_type=appeal_type)

        # 支持按状态筛选
        status_param = request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        queryset = queryset.order_by('-created_at')

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MyAppealSerializer(page, many=True)
            return ApiResponse.paginate(data=self.get_paginated_response(serializer.data))

        serializer = MyAppealSerializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='查询成功')
