from rest_framework import serializers
from .models import User, SystemSettings


class LoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """
    username = serializers.CharField(max_length=50, required=True, error_messages={
        'required': '用户名不能为空',
        'blank': '用户名不能为空'
    })
    password = serializers.CharField(max_length=255, required=True, error_messages={
        'required': '密码不能为空',
        'blank': '密码不能为空'
    })


class RegisterSerializer(serializers.Serializer):
    """
    用户注册序列化器
    """
    username = serializers.CharField(max_length=50, required=True, error_messages={
        'required': '用户名不能为空',
        'blank': '用户名不能为空'
    })
    password = serializers.CharField(max_length=255, required=True, error_messages={
        'required': '密码不能为空',
        'blank': '密码不能为空'
    })
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate_username(self, value):
        """
        验证用户名是否已存在
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    用户详情序列化器
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'employee_id',
            'role', 'role_display', 'status', 'status_display',
            'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'password': {'write_only': False},  # 开发阶段不过滤密码
        }

    def update(self, instance, validated_data):
        """
        更新用户信息
        """
        password = validated_data.pop('password', None)
        # 使用 super().update 处理其他字段（包括 status, role 等）
        instance = super().update(instance, validated_data)
        
        # 单独处理密码
        if password:
            instance.password = password
            instance.save()
            
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表序列化器（简化版）
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    employee_id = serializers.IntegerField(read_only=True)
    employee_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'role_display', 'status', 'status_display',
                  'employee_id', 'employee_name', 'created_at']

    def get_employee_name(self, obj):
        """
        获取关联员工的姓名
        """
        if obj.employee_id:
            from employees.models import EmployeeProfile
            try:
                employee = EmployeeProfile.objects.get(id=obj.employee_id)
                return employee.name
            except EmployeeProfile.DoesNotExist:
                return None
        return None


class SystemSettingsSerializer(serializers.ModelSerializer):
    """
    系统设置序列化器
    """
    class Meta:
        model = SystemSettings
        fields = [
            'id',
            'grace_period_minutes',
            'early_leave_grace_minutes',
            'late_deduction',
            'missing_deduction',
            'days_per_month',
            'hours_per_day',
            'overtime_rate',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'grace_period_minutes': {
                'min_value': 0,
                'max_value': 60,
                'error_messages': {
                    'min_value': '宽限时间不能小于0分钟',
                    'max_value': '宽限时间不能超过60分钟'
                }
            },
            'early_leave_grace_minutes': {
                'min_value': 0,
                'max_value': 60,
                'error_messages': {
                    'min_value': '宽限时间不能小于0分钟',
                    'max_value': '宽限时间不能超过60分钟'
                }
            },
            'late_deduction': {
                'min_value': 0,
                'max_value': 500,
                'error_messages': {
                    'min_value': '迟到扣款不能小于0',
                    'max_value': '迟到扣款不能超过500元'
                }
            },
            'missing_deduction': {
                'min_value': 0,
                'max_value': 500,
                'error_messages': {
                    'min_value': '缺卡扣款不能小于0',
                    'max_value': '缺卡扣款不能超过500元'
                }
            },
            'days_per_month': {
                'min_value': 20,
                'max_value': 23,
                'error_messages': {
                    'min_value': '月计薪天数不能小于20天',
                    'max_value': '月计薪天数不能超过23天'
                }
            },
            'hours_per_day': {
                'min_value': 4,
                'max_value': 12,
                'error_messages': {
                    'min_value': '日工作小时数不能小于4小时',
                    'max_value': '日工作小时数不能超过12小时'
                }
            },
            'overtime_rate': {
                'min_value': 1,
                'max_value': 3,
                'error_messages': {
                    'min_value': '加班倍率不能小于1',
                    'max_value': '加班倍率不能超过3'
                }
            }
        }
