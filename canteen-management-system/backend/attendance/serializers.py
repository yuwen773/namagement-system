from rest_framework import serializers
from .models import AttendanceRecord
from employees.models import EmployeeProfile
from schedules.models import Schedule


class AttendanceRecordSerializer(serializers.ModelSerializer):
    """考勤记录详情序列化器"""

    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    shift_name = serializers.CharField(source='schedule.shift.name', read_only=True, allow_null=True)
    work_date = serializers.DateField(source='schedule.work_date', read_only=True, allow_null=True)
    shift_start_time = serializers.TimeField(source='schedule.shift.start_time', read_only=True, allow_null=True)
    shift_end_time = serializers.TimeField(source='schedule.shift.end_time', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_late = serializers.BooleanField(read_only=True)
    is_early_leave = serializers.BooleanField(read_only=True)
    is_missing = serializers.BooleanField(read_only=True)
    overtime_hours = serializers.FloatField(read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            'id',
            'employee',
            'employee_name',
            'employee_position',
            'schedule',
            'shift_name',
            'work_date',
            'shift_start_time',
            'shift_end_time',
            'clock_in_time',
            'clock_in_location',
            'clock_out_time',
            'clock_out_location',
            'status',
            'status_display',
            'is_late',
            'is_early_leave',
            'is_missing',
            'overtime_hours',
            'correction_remark',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class AttendanceRecordListSerializer(serializers.ModelSerializer):
    """考勤记录列表序列化器（简化版）"""

    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    shift_name = serializers.CharField(source='schedule.shift.name', read_only=True, allow_null=True)
    work_date = serializers.DateField(source='schedule.work_date', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            'id',
            'employee_name',
            'employee_position',
            'shift_name',
            'work_date',
            'clock_in_time',
            'clock_out_time',
            'status',
            'status_display',
            'overtime_hours',
        ]


class ClockInSerializer(serializers.Serializer):
    """签到序列化器"""

    schedule_id = serializers.IntegerField(required=False, allow_null=True)
    clock_in_location = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate_schedule_id(self, value):
        """验证排班ID"""
        if value is not None:
            try:
                schedule = Schedule.objects.get(id=value)
                # 可以在这里添加额外的验证，例如检查日期是否为今天
                return schedule
            except Schedule.DoesNotExist:
                raise serializers.ValidationError('排班不存在')
        return value


class ClockOutSerializer(serializers.Serializer):
    """签退序列化器"""

    clock_out_location = serializers.CharField(max_length=200, required=False, allow_blank=True)


class AttendanceStatisticsSerializer(serializers.Serializer):
    """考勤统计序列化器"""

    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    employee_id = serializers.IntegerField(required=False, allow_null=True)


class AttendanceStatisticsResponseSerializer(serializers.Serializer):
    """考勤统计响应序列化器"""

    total_days = serializers.IntegerField(help_text='总天数')
    present_days = serializers.IntegerField(help_text='出勤天数')
    late_count = serializers.IntegerField(help_text='迟到次数')
    early_leave_count = serializers.IntegerField(help_text='早退次数')
    missing_count = serializers.IntegerField(help_text='缺卡次数')
    overtime_hours = serializers.FloatField(help_text='加班时长（小时）')


class AttendanceCorrectionSerializer(serializers.Serializer):
    """考勤异常处理序列化器"""

    status = serializers.ChoiceField(
        choices=AttendanceRecord.Status.choices,
        help_text='修改后的状态'
    )
    correction_remark = serializers.CharField(
        max_length=500,
        required=True,
        help_text='更正备注（必填）'
    )
