from datetime import date, datetime, time
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Attendance
from .serializers import (
    AttendanceSerializer,
    AttendanceListSerializer,
    CheckInSerializer,
    CheckOutSerializer,
    AttendanceStatsSerializer
)


class AttendanceViewSet(viewsets.ModelViewSet):
    """考勤记录 ViewSet"""
    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return AttendanceListSerializer
        return AttendanceSerializer

    def get_queryset(self):
        """根据用户角色和查询参数过滤"""
        user = self.request.user

        # 普通员工只能查看自己的记录
        if user.role == 'employee':
            return Attendance.objects.filter(user=user)

        # 人事和管理员可以查看所有或指定用户的记录
        queryset = Attendance.objects.all()

        # 筛选日期
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(date=date_param)

        # 筛选用户
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

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
