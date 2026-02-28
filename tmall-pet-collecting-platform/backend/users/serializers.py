from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def create(self, validated_data):
        # 密码明文存储（仅限开发/测试环境）
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'role_display',
            'status', 'status_display', 'avatar', 'phone',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone']


class UserAdminSerializer(serializers.ModelSerializer):
    """管理员用户管理序列化器"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'role_display',
            'status', 'status_display', 'avatar', 'phone',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserStatusSerializer(serializers.Serializer):
    """用户状态更新序列化器"""
    status = serializers.ChoiceField(choices=User.Status.choices)


class PasswordChangeSerializer(serializers.Serializer):
    """密码修改序列化器"""
    old_password = serializers.CharField(max_length=128, required=True, write_only=True)
    new_password = serializers.CharField(max_length=128, required=True, write_only=True, min_length=6)


class SystemConfigSerializer(serializers.ModelSerializer):
    """系统配置序列化器"""
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)

    class Meta:
        from .models import SystemConfig
        model = SystemConfig
        fields = ['id', 'key', 'value', 'config_type', 'description', 'is_encrypted',
                  'created_at', 'updated_at', 'updated_by', 'updated_by_username']
        read_only_fields = ['id', 'created_at', 'updated_at', 'updated_by']

    def to_representation(self, instance):
        """自定义输出，对敏感字段进行脱敏"""
        data = super().to_representation(instance)
        # 对 Cookie 类型的配置进行脱敏
        if instance.key == 'taobao_cookie' and data.get('value'):
            value = data['value']
            if len(value) > 20:
                data['value'] = value[:10] + '...' + value[-10:]
            else:
                data['value'] = '***'
        return data


class SystemConfigUpdateSerializer(serializers.ModelSerializer):
    """系统配置更新序列化器"""

    class Meta:
        from .models import SystemConfig
        model = SystemConfig
        fields = ['value', 'description']


class CrawlerConfigSerializer(serializers.Serializer):
    """爬虫配置序列化器"""

    taobao_cookie = serializers.CharField(required=False, allow_blank=True)
    cookie_status = serializers.CharField(read_only=True)
    last_test_time = serializers.DateTimeField(read_only=True)
    test_result = serializers.CharField(read_only=True)
