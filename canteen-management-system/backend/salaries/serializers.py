from rest_framework import serializers
from .models import SalaryRecord, Appeal
from employees.models import EmployeeProfile


class SalaryRecordSerializer(serializers.ModelSerializer):
    """薪资记录详情序列化器"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.position', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SalaryRecord
        fields = [
            'id', 'employee', 'employee_name', 'employee_position',
            'year_month', 'base_salary', 'position_allowance',
            'overtime_pay', 'deductions', 'total_salary',
            'work_days', 'late_count', 'missing_count', 'overtime_hours',
            'status', 'status_display', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SalaryRecordListSerializer(serializers.ModelSerializer):
    """薪资记录列表序列化器"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.get_position_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SalaryRecord
        fields = [
            'id', 'employee', 'employee_name', 'employee_position',
            'year_month', 'total_salary', 'status', 'status_display',
            'work_days', 'late_count', 'created_at'
        ]


class SalaryRecordCreateSerializer(serializers.ModelSerializer):
    """薪资记录创建序列化器"""

    class Meta:
        model = SalaryRecord
        fields = [
            'employee', 'year_month', 'base_salary', 'position_allowance',
            'overtime_pay', 'deductions', 'work_days', 'late_count',
            'missing_count', 'overtime_hours', 'status', 'remark'
        ]

    def validate(self, attrs):
        """验证数据"""
        # 检查同一员工在同一月份是否已存在薪资记录
        employee = attrs.get('employee')
        year_month = attrs.get('year_month')

        # 如果是更新操作，排除当前记录
        instance = self.instance
        queryset = SalaryRecord.objects.filter(employee=employee, year_month=year_month)
        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError(f"员工 {employee.name} 在 {year_month} 的薪资记录已存在")

        # 验证金额字段不能为负数
        if attrs.get('overtime_pay', 0) < 0:
            raise serializers.ValidationError({'overtime_pay': '加班费不能为负数'})
        if attrs.get('deductions', 0) < 0:
            raise serializers.ValidationError({'deductions': '扣款不能为负数'})

        return attrs


class SalaryGenerateSerializer(serializers.Serializer):
    """薪资生成请求序列化器"""
    year_month = serializers.CharField(max_length=7, help_text='格式: YYYY-MM')
    employee_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='员工ID列表，不提供则生成所有员工'
    )


class SalaryAdjustSerializer(serializers.Serializer):
    """薪资调整序列化器"""
    base_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    position_allowance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    overtime_pay = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    deductions = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    reason = serializers.CharField(required=True, help_text='调整原因（必填）')

    def validate(self, attrs):
        """验证调整金额"""
        if attrs.get('overtime_pay', 0) < 0:
            raise serializers.ValidationError({'overtime_pay': '加班费不能为负数'})
        if attrs.get('deductions', 0) < 0:
            raise serializers.ValidationError({'deductions': '扣款不能为负数'})
        return attrs


class AppealSerializer(serializers.ModelSerializer):
    """异常申诉详情序列化器"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_position = serializers.CharField(source='employee.get_position_display', read_only=True)
    appeal_type_display = serializers.CharField(source='get_appeal_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.name', read_only=True)

    class Meta:
        model = Appeal
        fields = [
            'id', 'appeal_type', 'appeal_type_display', 'employee', 'employee_name',
            'employee_position', 'target_id', 'reason', 'status', 'status_display',
            'approver', 'approver_name', 'approval_remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AppealListSerializer(serializers.ModelSerializer):
    """异常申诉列表序列化器"""
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    appeal_type_display = serializers.CharField(source='get_appeal_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.name', read_only=True)

    class Meta:
        model = Appeal
        fields = [
            'id', 'appeal_type', 'appeal_type_display', 'employee', 'employee_name',
            'target_id', 'reason', 'status', 'status_display',
            'approver', 'approver_name', 'created_at'
        ]


class AppealCreateSerializer(serializers.ModelSerializer):
    """异常申诉创建序列化器"""

    class Meta:
        model = Appeal
        fields = ['appeal_type', 'employee', 'target_id', 'reason']

    def validate_target_id(self, value):
        """验证目标记录ID是否存在"""
        appeal_type = self.initial_data.get('appeal_type')
        if appeal_type == 'ATTENDANCE':
            from attendance.models import AttendanceRecord
            if not AttendanceRecord.objects.filter(id=value).exists():
                raise serializers.ValidationError('考勤记录不存在')
        elif appeal_type == 'SALARY':
            if not SalaryRecord.objects.filter(id=value).exists():
                raise serializers.ValidationError('薪资记录不存在')
        return value


class AppealApprovalSerializer(serializers.Serializer):
    """异常申诉审批序列化器"""
    approve = serializers.BooleanField(required=True, help_text='是否批准')
    approval_remark = serializers.CharField(required=False, allow_blank=True, help_text='审批意见')


class MyAppealSerializer(serializers.ModelSerializer):
    """我的申诉序列化器（员工查看自己的申诉）"""
    appeal_type_display = serializers.CharField(source='get_appeal_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approver_name = serializers.CharField(source='approver.name', read_only=True)

    class Meta:
        model = Appeal
        fields = [
            'id', 'appeal_type', 'appeal_type_display', 'target_id', 'reason',
            'status', 'status_display', 'approver_name', 'approval_remark',
            'created_at', 'updated_at'
        ]
