from rest_framework import serializers
from .models import SalaryRecord


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
        fields = ['id', 'real_name', 'month', 'base_salary', 'final_salary', 'status']
