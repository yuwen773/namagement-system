from rest_framework import serializers
from .models import LeaveRequest
from employees.models import EmployeeProfile


class LeaveRequestSerializer(serializers.ModelSerializer):
    """
    请假申请详情序列化器（用于 CRUD）
    """
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.name', read_only=True)
    leave_duration_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id',
            'employee',
            'employee_name',
            'employee_position',
            'leave_type',
            'leave_type_display',
            'start_time',
            'end_time',
            'reason',
            'status',
            'status_display',
            'approver',
            'approver_name',
            'approval_remark',
            'leave_duration_days',
            'created_at',
            'updated_at',
        ]

    def validate(self, data):
        """
        验证请假时间
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("结束时间必须大于开始时间")

        return data


class LeaveRequestListSerializer(serializers.ModelSerializer):
    """
    请假申请列表序列化器（简化版）
    """
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    leave_duration_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id',
            'employee_name',
            'employee_position',
            'leave_type',
            'leave_type_display',
            'start_time',
            'end_time',
            'status',
            'status_display',
            'leave_duration_days',
            'created_at',
        ]


class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    """
    请假申请创建序列化器
    """
    class Meta:
        model = LeaveRequest
        fields = [
            'employee',
            'leave_type',
            'start_time',
            'end_time',
            'reason',
        ]

    def validate(self, data):
        """
        验证请假时间
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("结束时间必须大于开始时间")

        return data


class LeaveRequestApprovalSerializer(serializers.Serializer):
    """
    请假审批序列化器
    """
    approve = serializers.BooleanField(required=True, help_text="是否批准")
    approval_remark = serializers.CharField(required=False, allow_blank=True, help_text="审批意见")


class LeaveRequestMySerializer(serializers.ModelSerializer):
    """
    我的请假申请序列化器（员工查看自己的请假记录）
    """
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.name', read_only=True)
    leave_duration_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id',
            'leave_type',
            'leave_type_display',
            'start_time',
            'end_time',
            'reason',
            'status',
            'status_display',
            'approver_name',
            'approval_remark',
            'leave_duration_days',
            'created_at',
            'updated_at',
        ]
