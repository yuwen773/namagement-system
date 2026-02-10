from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'password_confirm', 'real_name', 'phone', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        """验证用户名唯一性"""
        if UserProfile.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value

    def validate(self, attrs):
        """验证密码一致性"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """验证用户名密码"""
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('用户名和密码必须提供')

        # 检查用户是否存在且未删除
        try:
            user = UserProfile.objects.get(username=username, is_deleted=False)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')

        # 检查用户是否被禁用
        if not user.is_active:
            raise serializers.ValidationError('用户已被禁用')

        # 验证密码
        if not user.check_password(password):
            raise serializers.ValidationError('用户名或密码错误')

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'real_name', 'phone', 'email', 'role', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'role', 'is_active', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""

    class Meta:
        model = UserProfile
        fields = ['real_name', 'phone', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """验证新密码一致性"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次新密码不一致'})
        return attrs
