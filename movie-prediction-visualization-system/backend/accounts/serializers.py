from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'real_name', 'phone']
        extra_kwargs = {
            'email': {'required': False},
            'real_name': {'required': False},
            'phone': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': '两次密码输入不一致'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            real_name=validated_data.get('real_name'),
            phone=validated_data.get('phone'),
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('用户已被禁用')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('用户名和密码不能为空')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'email', 'phone', 'role', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'role', 'is_active', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """用户个人信息序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'email', 'phone', 'role', 'created_at']
        read_only_fields = ['id', 'username', 'role', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('新密码长度不能少于6位')
        return value


class TokenResponseSerializer(serializers.Serializer):
    """Token 响应序列化器"""
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserSerializer()
