from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
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
