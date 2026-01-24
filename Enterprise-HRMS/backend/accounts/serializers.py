from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class PasswordStrengthValidator:
    """
    自定义密码强度验证器
    要求：至少8位，包含字母、数字、特殊字符
    """
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        import re

        errors = []

        # 检查最小长度
        if len(password) < self.min_length:
            errors.append(f'密码长度至少需要 {self.min_length} 个字符')

        # 检查是否包含字母
        if not re.search(r'[a-zA-Z]', password):
            errors.append('密码必须包含字母')

        # 检查是否包含数字
        if not re.search(r'\d', password):
            errors.append('密码必须包含数字')

        # 检查是否包含特殊字符
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('密码必须包含特殊字符')

        if errors:
            raise serializers.ValidationError(errors)

    def get_help_text(self):
        return '密码必须至少8位，包含字母、数字和特殊字符'


# 创建自定义密码验证器实例
password_strength_validator = PasswordStrengthValidator()


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_strength_validator.validate],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'real_name', 'phone', 'email']

    def validate(self, attrs):
        """
        验证两次密码是否一致
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': '两次密码不一致'
            })
        return attrs

    def validate_username(self, value):
        """
        验证用户名唯一性
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已被注册')
        return value

    def validate_phone(self, value):
        """
        验证手机号格式和唯一性
        """
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已被注册')
        return value

    def validate_email(self, value):
        """
        验证邮箱唯一性
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def create(self, validated_data):
        """
        创建用户
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            **validated_data,
            role='employee',  # 默认角色为普通员工
            is_active=True    # 默认激活
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器（用于响应）
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'phone', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录序列化器，添加 real_name 和 role 到 token 响应中
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        # 添加自定义字段
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['real_name'] = self.user.real_name
        data['role'] = self.user.role

        return data


class AdminResetPasswordSerializer(serializers.ModelSerializer):
    """
    管理员重置用户密码序列化器
    """
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_strength_validator.validate],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['new_password']
