from decimal import Decimal
from django.db import models
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import SalaryRecord
from .serializers import (
    SalaryCalculateSerializer,
    SalaryRecordSerializer,
    SalaryRecordListSerializer
)
from employee.models import EmployeeProfile


class SalaryCalculateViewSet(viewsets.ViewSet):
    """薪资计算视图集"""
    permission_classes = [IsAuthenticated]

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
    """薪资记录管理视图集"""
    permission_classes = [IsAuthenticated]
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
        """薪资记录列表"""
        queryset = self.get_queryset()
        month = request.query_params.get('month')

        if month:
            queryset = queryset.filter(month=month)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'data': serializer.data,
            'total': queryset.count()
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
        """保存薪资记录"""
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
