from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.db.models.fields import DecimalField
from django.utils import timezone
from datetime import timedelta

from HRMS.permissions import IsHROrAdmin
from employee.models import EmployeeProfile
from salary.models import SalaryRecord
from attendance.models import Attendance
from approval.models import ApprovalRequest


class DashboardStatsView(APIView):
    """
    数据仪表盘统计接口

    提供企业运营的核心指标数据：
    - 在职员工总数
    - 本月入职人数
    - 本月离职人数
    - 本月薪资总额
    - 部门人数分布
    - 近6月薪资趋势

    权限：仅 HR/Admin 可访问
    """
    permission_classes = [IsHROrAdmin]

    def get(self, request):
        """获取仪表盘统计数据"""
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)

        # 1. 在职员工总数
        total_employees = EmployeeProfile.objects.filter(
            status='active'
        ).count()

        # 2. 本月入职人数
        new_hires_this_month = EmployeeProfile.objects.filter(
            status='active',
            hire_date__gte=first_day_of_month,
            hire_date__lte=today
        ).count()

        # 3. 本月离职人数
        resigned_this_month = EmployeeProfile.objects.filter(
            status='resigned',
            resigned_date__gte=first_day_of_month,
            resigned_date__lte=today
        ).count()

        # 4. 本月薪资总额（已发布的薪资记录）
        month_str = today.strftime('%Y-%m')
        total_salary_this_month = SalaryRecord.objects.filter(
            month=month_str,
            status='published'
        ).aggregate(
            total=Coalesce(Sum('final_salary'), Value(0, output_field=DecimalField()))
        )['total'] or 0

        # 5. 部门人数分布
        department_distribution = EmployeeProfile.objects.filter(
            status='active'
        ).values(
            'department_id',
            'department__name'
        ).annotate(
            employee_count=Count('id')
        ).order_by('-employee_count')

        department_data = [
            {
                'department_id': item['department_id'] or 0,
                'department_name': item['department__name'] or '未分配部门',
                'employee_count': item['employee_count']
            }
            for item in department_distribution
        ]

        # 6. 近6月薪资趋势
        salary_trend = []
        current_month = today.replace(day=1)
        for i in range(5, -1, -1):
            # 计算目标月份：当前月向前推 i 个月
            target_month_num = current_month.month - 1 - i
            target_year = current_month.year
            if target_month_num < 0:
                target_year -= 1
                target_month_num += 12
            target_month = current_month.replace(year=target_year, month=target_month_num + 1)

            month_str = target_month.strftime('%Y-%m')

            month_stats = SalaryRecord.objects.filter(
                month=month_str,
                status='published'
            ).aggregate(
                count=Count('id'),
                total_amount=Sum('final_salary')
            )

            salary_trend.append({
                'month': month_str,
                'count': month_stats['count'] or 0,
                'total_amount': float(month_stats['total_amount'] or 0)
            })

        # 7. 本月考勤异常统计（按部门分组）
        first_day = today.replace(day=1)
        attendance_anomalies = Attendance.objects.filter(
            date__gte=first_day,
            date__lte=today,
            status__in=['late', 'early', 'absent']
        ).values(
            'user__profile__department__name'
        ).annotate(
            late_count=Count('id', filter=models.Q(status='late')),
            early_count=Count('id', filter=models.Q(status='early')),
            absent_count=Count('id', filter=models.Q(status='absent')),
            total_count=Count('id')
        ).order_by('-total_count')

        anomaly_data = [
            {
                'department': item['user__profile__department__name'] or '未分配部门',
                'late': item['late_count'],
                'early': item['early_count'],
                'absent': item['absent_count'],
                'total': item['total_count']
            }
            for item in attendance_anomalies
        ]

        # 8. 近6月入离职趋势
        hire_resign_trend = []
        current_month = today.replace(day=1)
        for i in range(5, -1, -1):
            # 计算目标月份：当前月向前推 i 个月
            target_month_num = current_month.month - 1 - i
            target_year = current_month.year
            if target_month_num < 0:
                target_year -= 1
                target_month_num += 12
            target_month = current_month.replace(year=target_year, month=target_month_num + 1)

            month_start = target_month
            month_end = target_month.replace(day=28) + timedelta(days=4)
            month_end = month_end - timedelta(days=month_end.day)

            month_str = target_month.strftime('%Y-%m')

            # 统计入职人数
            hire_count = EmployeeProfile.objects.filter(
                hire_date__gte=month_start,
                hire_date__lte=month_end
            ).count()

            # 统计离职人数
            resign_count = EmployeeProfile.objects.filter(
                status='resigned',
                resigned_date__gte=month_start,
                resigned_date__lte=month_end
            ).count()

            hire_resign_trend.append({
                'month': month_str,
                'hire_count': hire_count,
                'resign_count': resign_count
            })

        # 9. 部门加班统计（本月）
        overtime_by_department = ApprovalRequest.objects.filter(
            request_type='overtime',
            status='approved',
            start_time__gte=first_day_of_month,
            start_time__lte=timezone.now()
        ).values(
            'user__profile__department__name'
        ).annotate(
            overtime_hours=Sum('hours'),
            overtime_count=Count('id')
        ).order_by('-overtime_hours')

        overtime_data = [
            {
                'department': item['user__profile__department__name'] or '未分配部门',
                'overtime_hours': float(item['overtime_hours'] or 0),
                'overtime_count': item['overtime_count']
            }
            for item in overtime_by_department
        ]

        # 10. 部门请假统计（本月）
        # 先获取所有请假记录，手动计算时长
        leave_requests = ApprovalRequest.objects.filter(
            request_type='leave',
            status='approved',
            start_time__gte=first_day_of_month,
            start_time__lte=timezone.now()
        ).select_related('user__profile__department')

        # 按部门汇总请假数据
        leave_dict = {}
        for req in leave_requests:
            # 检查用户是否有profile和部门
            try:
                profile = req.user.profile
                dept = profile.department.name if profile.department else '未分配部门'
            except EmployeeProfile.DoesNotExist:
                dept = '未分配部门'

            if dept not in leave_dict:
                leave_dict[dept] = {'days': 0, 'count': 0}
            # 计算请假时长（天数）
            duration = req.end_time - req.start_time
            leave_hours = duration.total_seconds() / 3600  # 转换为小时
            leave_days = leave_hours / 24  # 转换为天
            leave_dict[dept]['days'] += leave_days
            leave_dict[dept]['count'] += 1

        leave_data = [
            {
                'department': dept,
                'leave_days': round(data['days'], 1),
                'leave_count': data['count']
            }
            for dept, data in leave_dict.items()
        ]
        leave_data.sort(key=lambda x: x['leave_days'], reverse=True)

        # 11. 员工留存率
        total_profiles = EmployeeProfile.objects.count()
        active_profiles = EmployeeProfile.objects.filter(status='active').count()
        retention_rate = (active_profiles / total_profiles * 100) if total_profiles > 0 else 0

        return Response({
            'code': 0,
            'data': {
                'total_employees': total_employees,
                'new_hires_this_month': new_hires_this_month,
                'resigned_this_month': resigned_this_month,
                'total_salary_this_month': float(total_salary_this_month),
                'department_distribution': department_data,
                'salary_trend': salary_trend,
                'attendance_anomalies': anomaly_data,
                'hire_resign_trend': hire_resign_trend,
                'overtime_by_department': overtime_data,
                'leave_by_department': leave_data,
                'retention_rate': round(retention_rate, 2)
            }
        })
