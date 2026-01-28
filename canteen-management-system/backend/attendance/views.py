from django.shortcuts import render
from django.db.models import Q, Sum, F
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import AttendanceRecord
from .serializers import (
    AttendanceRecordSerializer,
    AttendanceRecordListSerializer,
    ClockInSerializer,
    ClockOutSerializer,
    AttendanceStatisticsSerializer,
    AttendanceStatisticsResponseSerializer,
    AttendanceCorrectionSerializer,
)
from employees.models import EmployeeProfile
from schedules.models import Schedule


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """考勤记录视图集"""

    queryset = AttendanceRecord.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'status']
    search_fields = ['employee__name', 'employee__phone', 'clock_in_location', 'clock_out_location']
    ordering_fields = ['created_at', 'clock_in_time', 'clock_out_time']
    ordering = ['-clock_in_time']

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'list':
            return AttendanceRecordListSerializer
        return AttendanceRecordSerializer

    def create(self, request, *args, **kwargs):
        """创建考勤记录（管理员手动创建）"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'code': 200,
                'message': '考勤记录创建成功',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def retrieve(self, request, *args, **kwargs):
        """获取考勤记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })

    def list(self, request, *args, **kwargs):
        """获取考勤记录列表"""
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
        """更新考勤记录"""
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
        """删除考勤记录"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'code': 200,
            'message': '删除成功',
            'data': None
        })

    @action(detail=False, methods=['post'])
    def clock_in(self, request):
        """
        员工签到接口

        请求参数：
        - schedule_id: 排班ID（可选，如果不提供则查找今日排班）
        - clock_in_location: 签到地点（可选）
        """
        # TODO: 从请求中获取员工ID（后续需要实现登录认证后从token中获取）
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response({
                'code': 400,
                'message': '缺少员工ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = EmployeeProfile.objects.get(id=employee_id)
        except EmployeeProfile.DoesNotExist:
            return Response({
                'code': 404,
                'message': '员工不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        # 验证请求参数
        serializer = ClockInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 获取排班信息
        schedule = data.get('schedule_id')

        # 如果没有提供排班，查找今日排班
        if not schedule:
            today = timezone.now().date()
            try:
                schedule = Schedule.objects.filter(employee=employee, work_date=today).first()
            except Schedule.DoesNotExist:
                pass

        # 检查是否已有今日签到记录
        today = timezone.now().date()
        existing_attendance = AttendanceRecord.objects.filter(
            employee=employee,
            schedule__work_date=today
        ).first()

        if existing_attendance and existing_attendance.clock_in_time:
            return Response({
                'code': 400,
                'message': '今日已签到，请勿重复签到',
                'data': {
                    'clock_in_time': existing_attendance.clock_in_time,
                    'status': existing_attendance.get_status_display()
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建或更新考勤记录
        clock_in_location = data.get('clock_in_location', '')

        if existing_attendance:
            # 更新已有记录（只有签退的情况）
            existing_attendance.clock_in_time = timezone.now()
            existing_attendance.clock_in_location = clock_in_location
            existing_attendance.save()
            attendance = existing_attendance
        else:
            # 创建新记录
            attendance = AttendanceRecord.objects.create(
                employee=employee,
                schedule=schedule,
                clock_in_time=timezone.now(),
                clock_in_location=clock_in_location
            )

        # 返回签到结果
        result_serializer = AttendanceRecordSerializer(attendance)
        return Response({
            'code': 200,
            'message': '签到成功',
            'data': result_serializer.data
        })

    @action(detail=False, methods=['post'])
    def clock_out(self, request):
        """
        员工签退接口

        请求参数：
        - clock_out_location: 签退地点（可选）
        """
        # TODO: 从请求中获取员工ID（后续需要实现登录认证后从token中获取）
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response({
                'code': 400,
                'message': '缺少员工ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = EmployeeProfile.objects.get(id=employee_id)
        except EmployeeProfile.DoesNotExist:
            return Response({
                'code': 404,
                'message': '员工不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        # 验证请求参数
        serializer = ClockOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 查找今日考勤记录
        today = timezone.now().date()
        try:
            attendance = AttendanceRecord.objects.filter(
                employee=employee,
                schedule__work_date=today
            ).first()
        except AttendanceRecord.DoesNotExist:
            attendance = None

        if not attendance:
            return Response({
                'code': 400,
                'message': '未找到今日签到记录，请先签到',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        if not attendance.clock_in_time:
            return Response({
                'code': 400,
                'message': '未找到签到记录，请先签到',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        if attendance.clock_out_time:
            return Response({
                'code': 400,
                'message': '今日已签退，请勿重复签退',
                'data': {
                    'clock_out_time': attendance.clock_out_time,
                    'status': attendance.get_status_display()
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新签退信息
        attendance.clock_out_time = timezone.now()
        attendance.clock_out_location = data.get('clock_out_location', '')
        attendance.save()

        # 返回签退结果
        result_serializer = AttendanceRecordSerializer(attendance)
        return Response({
            'code': 200,
            'message': '签退成功',
            'data': result_serializer.data
        })

    @action(detail=False, methods=['post'])
    def statistics(self, request):
        """
        考勤统计接口

        请求参数：
        - start_date: 开始日期
        - end_date: 结束日期
        - employee_id: 员工ID（可选，不提供则统计所有员工）

        返回数据：
        - total_days: 总天数
        - present_days: 出勤天数
        - late_count: 迟到次数
        - early_leave_count: 早退次数
        - missing_count: 缺卡次数
        - overtime_hours: 加班时长
        """
        # 验证请求参数
        serializer = AttendanceStatisticsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        start_date = data['start_date']
        end_date = data['end_date']
        employee_id = data.get('employee_id')

        # 构建查询条件
        queryset = AttendanceRecord.objects.filter(
            schedule__work_date__range=[start_date, end_date]
        )

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        # 统计数据
        total_days = queryset.count()
        present_days = queryset.exclude(
            status__in=[AttendanceRecord.Status.MISSING, AttendanceRecord.Status.ABNORMAL]
        ).count()
        late_count = queryset.filter(status=AttendanceRecord.Status.LATE).count()
        early_leave_count = queryset.filter(status=AttendanceRecord.Status.EARLY_LEAVE).count()
        missing_count = queryset.filter(status=AttendanceRecord.Status.MISSING).count()

        # 计算总加班时长
        overtime_result = queryset.aggregate(
            total_overtime=Sum('overtime_hours')
        )
        overtime_hours = overtime_result['total_overtime'] or 0

        # 返回统计结果
        result_data = {
            'total_days': total_days,
            'present_days': present_days,
            'late_count': late_count,
            'early_leave_count': early_leave_count,
            'missing_count': missing_count,
            'overtime_hours': round(overtime_hours, 2)
        }

        result_serializer = AttendanceStatisticsResponseSerializer(result_data)

        return Response({
            'code': 200,
            'message': '统计成功',
            'data': result_serializer.data
        })

    @action(detail=True, methods=['post'])
    def correct(self, request, pk=None):
        """
        异常处理接口（管理员修改考勤状态）

        请求参数：
        - status: 修改后的状态
        - correction_remark: 更正备注（必填）
        """
        attendance = self.get_object()

        # 验证请求参数
        serializer = AttendanceCorrectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 更新考勤状态
        attendance.status = data['status']
        attendance.correction_remark = data['correction_remark']
        attendance.save()

        # 返回更新结果
        result_serializer = AttendanceRecordSerializer(attendance)
        return Response({
            'code': 200,
            'message': '考勤状态修改成功',
            'data': result_serializer.data
        })

    @action(detail=False, methods=['get'])
    def my_attendance(self, request):
        """
        我的考勤记录接口（员工查看自己的考勤记录）

        查询参数：
        - employee_id: 员工ID
        - start_date: 开始日期（可选）
        - end_date: 结束日期（可选）
        """
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response({
                'code': 400,
                'message': '缺少员工ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # 构建查询条件
        queryset = AttendanceRecord.objects.filter(employee_id=employee_id)

        # 日期范围筛选
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(schedule__work_date__range=[start_date, end_date])

        # 排序
        queryset = queryset.order_by('-schedule__work_date')

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AttendanceRecordListSerializer(page, many=True)
            return self.get_paginated_response({
                'code': 200,
                'message': '获取成功',
                'data': serializer.data
            })

        serializer = AttendanceRecordListSerializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': '获取成功',
            'data': serializer.data
        })
