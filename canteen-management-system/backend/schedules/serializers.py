from rest_framework import serializers
from .models import Shift, Schedule, ShiftSwapRequest
from employees.models import EmployeeProfile


class ShiftSerializer(serializers.ModelSerializer):
    """班次定义序列化器"""

    class Meta:
        model = Shift
        fields = ['id', 'name', 'start_time', 'end_time', 'created_at']
        read_only_fields = ['id', 'created_at']


class ShiftListSerializer(serializers.ModelSerializer):
    """班次列表序列化器（简化版）"""

    class Meta:
        model = Shift
        fields = ['id', 'name', 'start_time', 'end_time']


class ScheduleSerializer(serializers.ModelSerializer):
    """排班计划序列化器"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)
    start_time = serializers.TimeField(source='shift.start_time', read_only=True)
    end_time = serializers.TimeField(source='shift.end_time', read_only=True)
    position_display = serializers.CharField(source='employee.get_position_display', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'employee', 'employee_name', 'employee_position', 'position_display',
            'shift', 'shift_name', 'start_time', 'end_time',
            'work_date', 'is_swapped'
        ]
        read_only_fields = ['id', 'is_swapped']


class ScheduleListSerializer(serializers.ModelSerializer):
    """排班列表序列化器（简化版）"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)
    position_display = serializers.CharField(source='employee.get_position_display', read_only=True)
    start_time = serializers.TimeField(source='shift.start_time', read_only=True)
    end_time = serializers.TimeField(source='shift.end_time', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'employee_name', 'shift_name', 'position_display',
            'start_time', 'end_time', 'work_date', 'is_swapped'
        ]


class ScheduleDetailSerializer(serializers.ModelSerializer):
    """排班详情序列化器（包含完整信息）"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    position_display = serializers.CharField(source='employee.get_position_display', read_only=True)
    employee_phone = serializers.CharField(source='employee.phone', read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)
    start_time = serializers.TimeField(source='shift.start_time', read_only=True)
    end_time = serializers.TimeField(source='shift.end_time', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'employee', 'employee_name', 'employee_position', 'position_display',
            'employee_phone', 'shift', 'shift_name', 'start_time', 'end_time',
            'work_date', 'is_swapped'
        ]
        read_only_fields = ['id', 'is_swapped']


class BatchScheduleSerializer(serializers.Serializer):
    """批量排班序列化器"""
    employee_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text='员工ID列表'
    )
    shift_id = serializers.IntegerField(help_text='班次ID')
    start_date = serializers.DateField(help_text='开始日期')
    end_date = serializers.DateField(help_text='结束日期')
    force_update = serializers.BooleanField(
        required=False,
        default=True,
        help_text='是否强制更新已存在的排班（默认true）'
    )

    def validate_employee_ids(self, value):
        """验证员工ID是否存在"""
        existing_ids = EmployeeProfile.objects.filter(id__in=value).values_list('id', flat=True)
        invalid_ids = set(value) - set(existing_ids)
        if invalid_ids:
            raise serializers.ValidationError(f'员工ID不存在: {list(invalid_ids)}')
        return value

    def validate_shift_id(self, value):
        """验证班次ID是否存在"""
        if not Shift.objects.filter(id=value).exists():
            raise serializers.ValidationError(f'班次ID不存在: {value}')
        return value

    def validate(self, data):
        """验证日期范围"""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('开始日期不能晚于结束日期')
        return data


class ShiftSwapRequestSerializer(serializers.ModelSerializer):
    """调班申请序列化器"""
    requester_name = serializers.CharField(source='requester.name', read_only=True)
    original_schedule_date = serializers.DateField(source='original_schedule.work_date', read_only=True)
    original_shift_name = serializers.CharField(source='original_schedule.shift.name', read_only=True)
    original_shift_time = serializers.SerializerMethodField(read_only=True)
    original_schedule_info = serializers.SerializerMethodField(read_only=True)
    target_shift_name = serializers.CharField(source='target_shift.name', read_only=True)
    target_shift_time = serializers.SerializerMethodField(read_only=True)
    target_schedule_info = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.name', read_only=True)
    approval_time = serializers.DateTimeField(source='updated_at', read_only=True)

    def get_original_shift_time(self, obj):
        """获取原班次时间"""
        if obj.original_schedule and obj.original_schedule.shift:
            shift = obj.original_schedule.shift
            return f"{shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')}"
        return ''

    def get_target_shift_time(self, obj):
        """获取目标班次时间"""
        if obj.target_shift:
            return f"{obj.target_shift.start_time.strftime('%H:%M')} - {obj.target_shift.end_time.strftime('%H:%M')}"
        return ''

    def get_original_schedule_info(self, obj):
        """获取原班次信息"""
        return f"{obj.original_schedule_date} {obj.original_shift_name}"

    def get_target_schedule_info(self, obj):
        """获取目标班次信息"""
        return f"{obj.target_date} {obj.target_shift_name}"

    class Meta:
        model = ShiftSwapRequest
        fields = [
            'id', 'requester', 'requester_name', 'original_schedule',
            'original_schedule_date', 'original_shift_name', 'original_shift_time',
            'target_date', 'target_shift', 'target_shift_name', 'target_shift_time',
            'reason', 'status', 'status_display', 'approver', 'approver_name',
            'approval_remark', 'approval_time', 'created_at'
        ]
        read_only_fields = [
            'id', 'status', 'approver', 'approval_remark', 'created_at'
        ]


class ShiftSwapRequestListSerializer(serializers.ModelSerializer):
    """调班申请列表序列化器（简化版）"""
    requester_name = serializers.CharField(source='requester.name', read_only=True)
    original_schedule_date = serializers.DateField(source='original_schedule.work_date', read_only=True)
    original_shift_name = serializers.CharField(source='original_schedule.shift.name', read_only=True)
    original_shift_time = serializers.SerializerMethodField(read_only=True)
    target_shift_name = serializers.CharField(source='target_shift.name', read_only=True)
    target_shift_time = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.name', read_only=True)
    approval_time = serializers.DateTimeField(source='updated_at', read_only=True)

    def get_original_shift_time(self, obj):
        """获取原班次时间"""
        if obj.original_schedule and obj.original_schedule.shift:
            shift = obj.original_schedule.shift
            return f"{shift.start_time.strftime('%H:%M')} - {shift.end_time.strftime('%H:%M')}"
        return ''

    def get_target_shift_time(self, obj):
        """获取目标班次时间"""
        if obj.target_shift:
            return f"{obj.target_shift.start_time.strftime('%H:%M')} - {obj.target_shift.end_time.strftime('%H:%M')}"
        return ''

    class Meta:
        model = ShiftSwapRequest
        fields = [
            'id', 'requester_name', 'original_schedule_date', 'original_shift_name',
            'original_shift_time', 'target_date', 'target_shift_name', 'target_shift_time',
            'status', 'status_display', 'reason', 'approver_name', 'approval_remark',
            'approval_time', 'created_at'
        ]


class ShiftSwapApprovalSerializer(serializers.Serializer):
    """调班审批序列化器"""
    approve = serializers.BooleanField(help_text='是否批准（true=批准，false=拒绝）')
    approval_remark = serializers.CharField(required=False, allow_blank=True, help_text='审批意见')

    def validate_approve(self, value):
        if value:
            return 'APPROVED'
        return 'REJECTED'


class CalendarViewSerializer(serializers.Serializer):
    """日历视图序列化器"""
    start_date = serializers.DateField(help_text='开始日期')
    end_date = serializers.DateField(help_text='结束日期')
    employee_id = serializers.IntegerField(required=False, help_text='员工ID（可选，用于筛选特定员工）')

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('开始日期不能晚于结束日期')
        return data
