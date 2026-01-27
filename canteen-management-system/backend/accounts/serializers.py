from rest_framework import serializers
from .models import User


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
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.password = password
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表序列化器（简化版）
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'role_display', 'status', 'status_display', 'created_at']
