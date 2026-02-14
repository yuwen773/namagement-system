from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'password_confirm', 'email']
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
        """创建用户（明文存储密码）"""
        validated_data.pop('password_confirm')
        # 设置默认值
        validated_data.setdefault('real_name', '')
        validated_data.setdefault('phone', '')
        # 明文存储密码
        user = UserProfile(**validated_data)
        user.save()
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
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({'username': '用户不存在'})

        # 检查用户是否已删除
        if user.is_deleted:
            raise serializers.ValidationError({'username': '用户账号已注销'})

        # 检查用户是否被禁用
        if not user.is_active:
            raise serializers.ValidationError({'username': '用户已被禁用，请联系管理员'})

        # 验证密码（明文比对）
        if user.password != password:
            raise serializers.ValidationError({'password': '密码错误'})

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
