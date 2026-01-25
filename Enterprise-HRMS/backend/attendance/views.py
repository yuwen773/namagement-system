from datetime import date, datetime, time
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q
from HRMS.permissions import IsEmployeeOrHROrAdmin, IsHROrAdmin
from .models import Attendance
from .serializers import (
    AttendanceSerializer,
    AttendanceListSerializer,
    CheckInSerializer,
    CheckOutSerializer,
    AttendanceStatsSerializer
)


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    考勤记录 ViewSet

    权限说明：
    - check_in, check_out: 所有登录用户可访问（自己打卡）
    - list, retrieve, today, stats: 登录用户可访问（普通员工只能看自己）
    """
    queryset = Attendance.objects.all()
    permission_classes = [IsEmployeeOrHROrAdmin]

    def get_serializer_class(self):
        if self.action == 'list':
            return AttendanceListSerializer
        return AttendanceSerializer

    def get_queryset(self):
        """根据用户角色和查询参数过滤"""
        user = self.request.user

        # 普通员工只能查看自己的记录
        if user.role == 'employee':
            queryset = Attendance.objects.filter(user=user)
        else:
            queryset = Attendance.objects.all()

        # 筛选日期范围 (date_start, date_end)
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        if date_start:
            queryset = queryset.filter(date__gte=date_start)
        if date_end:
            queryset = queryset.filter(date__lte=date_end)

        # 兼容单日查询 (date)
        date_param = self.request.query_params.get('date')
        if date_param and not date_start and not date_end:
            queryset = queryset.filter(date=date_param)

        # 筛选状态 (status)
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        # 筛选用户 (仅 HR/Admin 可用)
        user_id = self.request.query_params.get('user_id')
        if user_id and user.role != 'employee':
            queryset = queryset.filter(user_id=user_id)

        return queryset.order_by('-date', '-check_in_time')

    def list(self, request, *args, **kwargs):
        """考勤记录列表（支持分页）"""
        queryset = self.get_queryset()

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

    @action(detail=False, methods=['post'], url_path='check-in')
    def check_in(self, request):
        """
        签到接口
        POST /api/attendance/check-in/
        """
        user = request.user
        today = date.today()
        now = timezone.localtime().time().replace(microsecond=0)

        # 查找或创建今日考勤记录
        attendance, created = Attendance.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                'check_in_time': now,
                'status': 'normal'
            }
        )

        # 如果已经签过到，更新签到时间（取最早的）
        if not created:
            if attendance.check_in_time is None:
                attendance.check_in_time = now
            elif now < attendance.check_in_time:
                # 如果新的签到时间更早，更新为更早的时间
                attendance.check_in_time = now

        attendance.save()

        # 判断是否迟到
        work_start = time(9, 0)
        is_late = now > work_start

        response_data = {
            'code': 0,
            'data': {
                'attendance_id': attendance.id,
                'check_in_time': now.strftime('%H:%M:%S'),
                'date': str(attendance.date),
                'status': attendance.status,
                'is_late': is_late,
                'message': '签到成功' + ('，您迟到了' if is_late else '')
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='check-out')
    def check_out(self, request):
        """
        签退接口
        POST /api/attendance/check-out/
        """
        user = request.user
        today = date.today()
        now = timezone.localtime().time().replace(microsecond=0)

        # 获取今日考勤记录
        try:
            attendance = Attendance.objects.get(user=user, date=today)
        except Attendance.DoesNotExist:
            return Response({
                'code': 400,
                'message': '今日尚未签到，请先签到'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新签退时间
        if attendance.check_out_time is None:
            attendance.check_out_time = now
        elif now > attendance.check_out_time:
            # 如果新的签退时间更晚，更新为更晚的时间
            attendance.check_out_time = now

        attendance.save()

        # 判断是否早退
        work_end = time(18, 0)
        is_early = now < work_end

        response_data = {
            'code': 0,
            'data': {
                'attendance_id': attendance.id,
                'check_out_time': now.strftime('%H:%M:%S'),
                'date': str(attendance.date),
                'status': attendance.status,
                'is_early': is_early,
                'message': '签退成功' + ('，您早退了' if is_early else '')
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """
        获取今日考勤信息
        GET /api/attendance/today/
        """
        user = request.user
        today = date.today()

        try:
            attendance = Attendance.objects.get(user=user, date=today)
            serializer = AttendanceSerializer(attendance)
            return Response({
                'code': 0,
                'data': serializer.data
            })
        except Attendance.DoesNotExist:
            return Response({
                'code': 0,
                'data': {
                    'has_check_in': False,
                    'has_check_out': False,
                    'status': None
                }
            })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        获取考勤统计
        GET /api/attendance/stats/?month=2024-01
        """
        user = request.user
        month = request.query_params.get('month')

        if not month:
            return Response({
                'code': 400,
                'message': '请指定月份，格式：YYYY-MM'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            year, month_num = map(int, month.split('-'))
        except (ValueError, AttributeError):
            return Response({
                'code': 400,
                'message': '月份格式错误，请使用 YYYY-MM 格式'
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = Attendance.objects.filter(
            user=user,
            date__year=year,
            date__month=month_num
        )

        stats = {
            'total_days': queryset.count(),
            'normal_days': queryset.filter(status='normal').count(),
            'late_days': queryset.filter(status='late').count(),
            'early_days': queryset.filter(status='early').count(),
            'absent_days': queryset.filter(status='absent').count(),
            'leave_days': queryset.filter(status='leave').count(),
        }

        return Response({
            'code': 0,
            'data': stats
        })

    @action(detail=False, methods=['get'], permission_classes=[IsHROrAdmin], url_path='monthly-stats')
    def monthly_stats(self, request):
        """
        获取月度考勤统计（按部门汇总）
        GET /api/attendance/monthly-stats/?month=2024-01&department_id=1
        仅 HR/Admin 可访问
        """
        user = request.user
        month = request.query_params.get('month')
        department_id = request.query_params.get('department_id')

        # 权限检查
        if user.role not in ['hr', 'admin']:
            return Response({
                'code': 403,
                'message': '您没有权限访问此统计'
            }, status=status.HTTP_403_FORBIDDEN)

        if not month:
            return Response({
                'code': 400,
                'message': '请指定月份，格式：YYYY-MM'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            year, month_num = map(int, month.split('-'))
        except (ValueError, AttributeError):
            return Response({
                'code': 400,
                'message': '月份格式错误，请使用 YYYY-MM 格式'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取该月份的工作日天数（简单计算：22天，可根据实际情况调整）
        from calendar import monthrange
        _, days_in_month = monthrange(year, month_num)
        # 粗略估算工作日（约80%的天数）
        total_work_days = int(days_in_month * 0.8)

        # 获取考勤记录
        from employee.models import EmployeeProfile

        queryset = Attendance.objects.filter(
            date__year=year,
            date__month=month_num
        )

        # 按部门筛选
        if department_id:
            profile_ids = EmployeeProfile.objects.filter(
                department_id=department_id
            ).values_list('user_id', flat=True)
            queryset = queryset.filter(user_id__in=profile_ids)

        # 获取所有在职员工（用于计算部门人数）
        active_profiles = EmployeeProfile.objects.filter(status='active')
        if department_id:
            active_profiles = active_profiles.filter(department_id=department_id)

        # 部门统计
        from django.db.models import F

        # 按用户汇总
        user_stats = queryset.values('user_id').annotate(
            total=Count('id'),
            normal=Count('id', filter=Q(status='normal')),
            late=Count('id', filter=Q(status='late')),
            early=Count('id', filter=Q(status='early')),
            absent=Count('id', filter=Q(status='absent')),
            leave=Count('id', filter=Q(status='leave')),
        )

        # 计算汇总数据
        total_employees = active_profiles.count() or 1
        total_records = sum(s['total'] for s in user_stats)
        total_normal = sum(s['normal'] for s in user_stats)
        total_late = sum(s['late'] for s in user_stats)
        total_early = sum(s['early'] for s in user_stats)
        total_absent = sum(s['absent'] for s in user_stats)
        total_leave = sum(s['leave'] for s in user_stats)

        # 部门人员统计
        dept_user_map = {}
        for profile in active_profiles.select_related('department'):
            dept_name = profile.department.get_full_path() if profile.department else '未知部门'
            if dept_name not in dept_user_map:
                dept_user_map[dept_name] = {'count': 0, 'users': set()}
            dept_user_map[dept_name]['count'] += 1
            dept_user_map[dept_name]['users'].add(profile.user_id)

        # 构建返回数据
        stats_data = {
            'month': month,
            'total_work_days': total_work_days,
            'summary': {
                'total_employees': total_employees,
                'total_records': total_records,
                'normal_days': total_normal,
                'late_days': total_late,
                'early_days': total_early,
                'absent_days': total_absent,
                'leave_days': total_leave,
                'attendance_rate': round(total_normal / total_records * 100, 2) if total_records > 0 else 0,
            },
            'by_department': []
        }

        # 按部门分组统计
        for dept_name, dept_info in dept_user_map.items():
            dept_user_ids = dept_info['users']
            dept_queryset = queryset.filter(user_id__in=dept_user_ids)

            dept_total = dept_queryset.count()
            dept_normal = dept_queryset.filter(status='normal').count()
            dept_late = dept_queryset.filter(status='late').count()
            dept_early = dept_queryset.filter(status='early').count()
            dept_absent = dept_queryset.filter(status='absent').count()
            dept_leave = dept_queryset.filter(status='leave').count()

            stats_data['by_department'].append({
                'department': dept_name,
                'employee_count': dept_info['count'],
                'total_records': dept_total,
                'normal_days': dept_normal,
                'late_days': dept_late,
                'early_days': dept_early,
                'absent_days': dept_absent,
                'leave_days': dept_leave,
                'attendance_rate': round(dept_normal / dept_total * 100, 2) if dept_total > 0 else 0,
            })

        # 按部门名称排序
        stats_data['by_department'].sort(key=lambda x: x['department'])

        return Response({
            'code': 0,
            'data': stats_data
        })
