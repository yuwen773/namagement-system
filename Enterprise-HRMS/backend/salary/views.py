from decimal import Decimal
from django.db import models
from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from HRMS.permissions import IsHROrAdmin, IsEmployeeOrHROrAdmin
from .models import SalaryRecord, SalaryException
from .serializers import (
    SalaryCalculateSerializer,
    SalaryRecordSerializer,
    SalaryRecordListSerializer,
    SalaryExceptionSerializer,
    SalaryExceptionListSerializer,
    SalaryExceptionCreateSerializer,
    SalaryExceptionResolveSerializer
)
from employee.models import EmployeeProfile


class SalaryCalculateViewSet(viewsets.ViewSet):
    """
    薪资计算视图集

    权限：仅 HR/Admin 可访问薪资计算功能
    """
    permission_classes = [IsHROrAdmin]

    def list(self, request):
        """薪资计算接口"""
        return Response({'message': '请使用 POST /api/salary/calculate/ 计算薪资'})

    def create(self, request):
        """计算薪资"""
        serializer = SalaryCalculateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 400, 'message': '参数错误', 'errors': serializer.errors},
                          status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['user_id']
        month = serializer.validated_data['month']

        # 获取员工档案
        try:
            profile = EmployeeProfile.objects.select_related('user', 'department').get(
                user_id=user_id,
                status='active'
            )
        except EmployeeProfile.DoesNotExist:
            return Response({'code': 404, 'message': '员工不存在或已离职'},
                          status=status.HTTP_404_NOT_FOUND)

        # 获取当月考勤统计
        from attendance.models import Attendance
        attendance_stats = Attendance.objects.filter(
            user_id=user_id,
            date__startswith=month
        ).aggregate(
            late_count=Count('id', filter=models.Q(status='late')),
            early_count=Count('id', filter=models.Q(status='early')),
            present_count=Count('id', filter=models.Q(status='normal'))
        )

        late_count = attendance_stats['late_count'] or 0
        early_count = attendance_stats['early_count'] or 0
        present_count = attendance_stats['present_count'] or 0

        # 计算薪资
        base_salary = profile.salary_base

        # 时薪 = 基本工资 / 22 / 8
        hourly_rate = base_salary / Decimal('22') / Decimal('8')

        # 考勤扣款 = (迟到次数 + 早退次数) * 50
        attendance_deduction = (Decimal(late_count) + Decimal(early_count)) * Decimal('50')

        # 加班费（暂时为0，后续可扩展）
        overtime_hours = Decimal('0')
        overtime_pay = Decimal('0')

        # 实发工资 = 基本工资 + 加班费 - 考勤扣款
        final_salary = base_salary + overtime_pay - attendance_deduction

        # 计算工作日天数（简化计算：每月约22天）
        workday_count = 22

        result = {
            'user_id': user_id,
            'username': profile.user.username,
            'real_name': profile.user.real_name,
            'month': month,
            'base_salary': base_salary,
            'hourly_rate': round(hourly_rate, 2),
            'overtime_hours': overtime_hours,
            'overtime_pay': overtime_pay,
            'late_count': late_count,
            'early_count': early_count,
            'attendance_deduction': attendance_deduction,
            'final_salary': final_salary,
            'workday_count': workday_count,
            'present_count': present_count
        }

        return Response({
            'code': 0,
            'data': result
        })


class SalaryRecordViewSet(viewsets.ModelViewSet):
    """
    薪资记录管理视图集

    权限说明：
    - list, retrieve: 登录用户可访问（普通员工只能看自己已发布的薪资）
    - save, publish: 仅 HR/Admin 可访问
    """
    permission_classes = [IsEmployeeOrHROrAdmin]
    queryset = SalaryRecord.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SalaryRecordListSerializer
        return SalaryRecordSerializer

    def get_queryset(self):
        """根据用户角色返回不同数据"""
        user = self.request.user

        # 普通员工只能看自己的薪资记录
        if user.role == 'employee':
            return SalaryRecord.objects.filter(user=user, status='published')

        # 人事和管理员可以看所有已发布的薪资记录
        return SalaryRecord.objects.filter(status='published')

    def list(self, request, *args, **kwargs):
        """薪资记录列表（支持分页和月份范围查询）"""
        queryset = self.get_queryset()

        # 兼容单月查询 (month)
        month = request.query_params.get('month')
        if month and not request.query_params.get('month_start') and not request.query_params.get('month_end'):
            queryset = queryset.filter(month=month)

        # 筛选月份范围 (month_start, month_end)
        month_start = request.query_params.get('month_start')
        month_end = request.query_params.get('month_end')
        if month_start:
            queryset = queryset.filter(month__gte=month_start)
        if month_end:
            queryset = queryset.filter(month__lte=month_end)

        # 获取分页参数
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        # 分页
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })

    def retrieve(self, request, *args, **kwargs):
        """薪资记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @action(detail=False, methods=['post'])
    def save(self, request):
        """保存薪资记录（仅 HR/Admin 可访问）"""
        # 权限检查已由 permission_classes 处理，但 save 是 action，需要额外检查
        if request.user.role not in ['hr', 'admin']:
            return Response({
                'code': 403,
                'message': '权限不足，需要人事或管理员权限'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = SalaryCalculateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 400, 'message': '参数错误'},
                          status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['user_id']
        month = serializer.validated_data['month']

        # 检查是否已存在
        if SalaryRecord.objects.filter(user_id=user_id, month=month).exists():
            return Response({'code': 400, 'message': '该月份薪资记录已存在'},
                          status=status.HTTP_400_BAD_REQUEST)

        # 重新计算
        calculate_request = type('Request', (), {'data': request.data})()
        result = SalaryCalculateViewSet().create(calculate_request)

        if result.status_code != 200:
            return result

        data = result.data['data']

        record = SalaryRecord.objects.create(
            user_id=user_id,
            month=month,
            base_salary=data['base_salary'],
            overtime_hours=data['overtime_hours'],
            overtime_pay=data['overtime_pay'],
            late_count=data['late_count'],
            early_count=data['early_count'],
            attendance_deduction=data['attendance_deduction'],
            final_salary=data['final_salary']
        )

        return Response({
            'code': 0,
            'message': '保存成功',
            'data': SalaryRecordSerializer(record).data
        }, status=status.HTTP_201_CREATED)


# ==================== 薪资异常处理 ====================

class SalaryExceptionViewSet(viewsets.ModelViewSet):
    """
    薪资异常处理 ViewSet

    list: 获取异常列表
    create: 创建异常报告（所有用户可上报）
    retrieve: 获取异常详情
    update/partial_update: 更新异常（HR/Admin）
    resolve: 处理异常（HR/Admin）
    my-exceptions: 获取我上报的异常（员工）
    pending: 获取待处理异常（HR/Admin）
    """
    queryset = SalaryException.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return SalaryExceptionListSerializer
        elif self.action == 'create':
            return SalaryExceptionCreateSerializer
        elif self.action in ['update', 'partial_update', 'resolve']:
            return SalaryExceptionResolveSerializer
        return SalaryExceptionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = SalaryException.objects.select_related(
            'salary_record__user',
            'reported_by',
            'assigned_to'
        )

        # 根据状态筛选
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 根据类型筛选
        exception_type = self.request.query_params.get('exception_type')
        if exception_type:
            queryset = queryset.filter(exception_type=exception_type)

        # 按员工ID筛选（HR/Admin可用）
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(salary_record__user_id=user_id)

        # 按月份筛选
        month = self.request.query_params.get('month')
        if month:
            queryset = queryset.filter(salary_record__month=month)

        # 按日期范围筛选
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        if date_start:
            queryset = queryset.filter(created_at__date__gte=date_start)
        if date_end:
            queryset = queryset.filter(created_at__date__lte=date_end)

        # 普通员工只能看自己上报的异常
        if user.role == 'employee':
            queryset = queryset.filter(reported_by=user)

        return queryset

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsHROrAdmin()]

    def list(self, request, *args, **kwargs):
        """获取异常列表"""
        queryset = self.get_queryset()

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        queryset = queryset[start:end]

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })

    def create(self, request, *args, **kwargs):
        """上报异常"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 400, 'message': '参数错误', 'errors': serializer.errors},
                          status=status.HTTP_400_BAD_REQUEST)

        exception = serializer.save()

        return Response({
            'code': 0,
            'message': '异常已上报',
            'data': SalaryExceptionSerializer(exception).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """获取异常详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 0,
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """
        处理异常（HR/Admin）
        """
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        exception = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'code': 400, 'message': '参数错误', 'errors': serializer.errors},
                          status=status.HTTP_400_BAD_REQUEST)

        # 更新异常
        exception.resolution = serializer.validated_data.get('resolution', '')
        exception.adjustment_amount = serializer.validated_data.get('adjustment_amount', 0)
        exception.status = serializer.validated_data.get('status', 'resolved')
        exception.assigned_to = request.user
        exception.resolved_at = timezone.now()
        exception.save()

        # 如果调整金额不为0，更新薪资记录
        if exception.adjustment_amount != 0:
            salary_record = exception.salary_record
            salary_record.final_salary = salary_record.final_salary + exception.adjustment_amount
            salary_record.save()

        return Response({
            'code': 0,
            'message': '异常已处理',
            'data': SalaryExceptionSerializer(exception).data
        })

    @action(detail=False, methods=['get'])
    def my_exceptions(self, request):
        """
        获取我上报的异常列表
        """
        exceptions = SalaryException.objects.filter(
            reported_by=request.user
        ).select_related(
            'salary_record__user'
        ).order_by('-created_at')

        serializer = SalaryExceptionListSerializer(exceptions, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': len(serializer.data)
        })

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        获取待处理的异常列表（HR/Admin）
        """
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        exceptions = SalaryException.objects.filter(
            status__in=['pending', 'processing']
        ).select_related(
            'salary_record__user',
            'reported_by'
        ).order_by('-created_at')

        serializer = SalaryExceptionListSerializer(exceptions, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': len(serializer.data)
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        获取异常统计信息（HR/Admin）
        """
        if request.user.role == 'employee':
            return Response({
                'code': 403,
                'message': '权限不足'
            }, status=status.HTTP_403_FORBIDDEN)

        from django.db.models import Count

        # 按状态统计
        status_stats = SalaryException.objects.values('status').annotate(
            count=Count('id')
        )

        # 按类型统计
        type_stats = SalaryException.objects.values('exception_type').annotate(
            count=Count('id')
        )

        return Response({
            'code': 0,
            'data': {
                'by_status': list(status_stats),
                'by_type': list(type_stats),
                'total': SalaryException.objects.count(),
                'pending': SalaryException.objects.filter(status='pending').count(),
                'resolved': SalaryException.objects.filter(status='resolved').count()
            }
        })
