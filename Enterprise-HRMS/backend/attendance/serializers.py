from rest_framework import serializers
from .models import Attendance


class TimeFieldFormatted(serializers.TimeField):
    """格式化的时间字段"""
    def to_representation(self, value):
        if value is None:
            return None
        return value.strftime('%H:%M:%S')


class AttendanceSerializer(serializers.ModelSerializer):
    """考勤记录详情序列化器"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    department_name = serializers.CharField(source='user.employeeprofile.department.name', read_only=True, default=None)
    check_in_time = TimeFieldFormatted()
    check_out_time = TimeFieldFormatted()

    class Meta:
        model = Attendance
        fields = [
            'id', 'user', 'user_name', 'department_name',
            'date', 'check_in_time', 'check_out_time', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']


class AttendanceListSerializer(serializers.ModelSerializer):
    """考勤记录列表序列化器（轻量版）"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    check_in_time = TimeFieldFormatted()
    check_out_time = TimeFieldFormatted()

    class Meta:
        model = Attendance
        fields = [
            'id', 'user', 'user_name', 'date',
            'check_in_time', 'check_out_time', 'status'
        ]
        read_only_fields = ['status']


class CheckInSerializer(serializers.Serializer):
    """签到请求序列化器"""
    pass


class CheckOutSerializer(serializers.Serializer):
    """签退请求序列化器"""
    pass


class AttendanceStatsSerializer(serializers.Serializer):
    """考勤统计序列化器"""
    total_days = serializers.IntegerField()
    normal_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    early_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    leave_days = serializers.IntegerField()
