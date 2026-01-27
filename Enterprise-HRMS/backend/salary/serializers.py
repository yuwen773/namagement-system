from rest_framework import serializers
from .models import SalaryRecord, SalaryException


class SalaryCalculateSerializer(serializers.Serializer):
    """薪资计算请求序列化器"""
    user_id = serializers.IntegerField(required=True, min_value=1, label='员工ID')
    month = serializers.CharField(required=True, max_length=7, label='月份',
                                  help_text='格式: YYYY-MM')

    def validate_month(self, value):
        """验证月份格式"""
        if len(value) != 7 or value[4] != '-':
            raise serializers.ValidationError('月份格式必须为 YYYY-MM')
        try:
            int(value[:4])
            int(value[5:7])
        except ValueError:
            raise serializers.ValidationError('月份格式无效')
        return value


class SalaryCalculateResultSerializer(serializers.Serializer):
    """薪资计算结果序列化器"""
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    real_name = serializers.CharField()
    month = serializers.CharField()
    base_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    overtime_hours = serializers.DecimalField(max_digits=6, decimal_places=1)
    overtime_pay = serializers.DecimalField(max_digits=10, decimal_places=2)
    late_count = serializers.IntegerField()
    early_count = serializers.IntegerField()
    attendance_deduction = serializers.DecimalField(max_digits=10, decimal_places=2)
    final_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    workday_count = serializers.IntegerField()
    present_count = serializers.IntegerField()


class SalaryRecordSerializer(serializers.ModelSerializer):
    """薪资记录详情序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    real_name = serializers.CharField(source='user.real_name', read_only=True)
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = SalaryRecord
        fields = [
            'id', 'user', 'username', 'real_name', 'department_name',
            'month', 'base_salary', 'overtime_hours', 'overtime_pay',
            'late_count', 'early_count', 'attendance_deduction',
            'final_salary', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_department_name(self, obj):
        """获取部门名称"""
        try:
            profile = obj.user.employeeprofile
            if profile.department:
                return profile.department.name
        except Exception:
            pass
        return None


class SalaryRecordListSerializer(serializers.ModelSerializer):
    """薪资记录列表序列化器"""
    real_name = serializers.CharField(source='user.real_name', read_only=True)

    class Meta:
        model = SalaryRecord
        fields = ['id', 'real_name', 'month', 'base_salary', 'final_salary', 'status', 'created_at']


class SalaryExceptionSerializer(serializers.ModelSerializer):
    """薪资异常详情序列化器"""
    exception_type_display = serializers.CharField(
        source='get_exception_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    reported_by_name = serializers.CharField(
        source='reported_by.real_name',
        read_only=True
    )
    assigned_to_name = serializers.CharField(
        source='assigned_to.real_name',
        read_only=True
    )
    employee_name = serializers.CharField(
        source='salary_record.user.real_name',
        read_only=True
    )
    month = serializers.CharField(
        source='salary_record.month',
        read_only=True
    )

    class Meta:
        model = SalaryException
        fields = [
            'id', 'salary_record', 'employee_name', 'month',
            'exception_type', 'exception_type_display',
            'description', 'status', 'status_display',
            'reported_by', 'reported_by_name',
            'assigned_to', 'assigned_to_name',
            'resolution', 'adjustment_amount',
            'resolved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SalaryExceptionListSerializer(serializers.ModelSerializer):
    """薪资异常列表序列化器"""
    exception_type_display = serializers.CharField(
        source='get_exception_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    employee_name = serializers.CharField(
        source='salary_record.user.real_name',
        read_only=True
    )
    month = serializers.CharField(
        source='salary_record.month',
        read_only=True
    )

    class Meta:
        model = SalaryException
        fields = [
            'id', 'employee_name', 'month',
            'exception_type', 'exception_type_display',
            'status', 'status_display',
            'adjustment_amount', 'created_at'
        ]


class SalaryExceptionCreateSerializer(serializers.ModelSerializer):
    """创建薪资异常序列化器"""

    class Meta:
        model = SalaryException
        fields = [
            'salary_record', 'exception_type',
            'description', 'reported_by'
        ]

    def create(self, validated_data):
        # 自动设置 reported_by 为当前用户
        validated_data['reported_by'] = self.context['request'].user
        return super().create(validated_data)


class SalaryExceptionResolveSerializer(serializers.ModelSerializer):
    """处理薪资异常序列化器"""

    class Meta:
        model = SalaryException
        fields = ['resolution', 'adjustment_amount', 'status']
