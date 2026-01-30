"""
用户认证序列化器模块

包含用户注册、登录等相关的序列化器。
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器

    处理用户注册请求的数据验证和创建。
    验证规则：
    - 用户名必填，3-20个字符
    - 密码必填，至少8位
    - 邮箱可选，需符合邮箱格式
    - 用户名唯一性检查
    """

    username = serializers.CharField(
        max_length=50,
        min_length=3,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'blank': '用户名不能为空',
            'min_length': '用户名至少需要3个字符',
            'max_length': '用户名不能超过50个字符'
        },
        help_text='用户登录名，3-20个字符'
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        required=True,
        write_only=True,
        error_messages={
            'required': '密码不能为空',
            'blank': '密码不能为空',
            'min_length': '密码至少需要8个字符'
        },
        help_text='用户密码，至少8个字符',
        style={'input_type': 'password'}
    )

    password_confirm = serializers.CharField(
        max_length=128,
        min_length=8,
        required=True,
        write_only=True,
        error_messages={
            'required': '确认密码不能为空',
            'blank': '确认密码不能为空'
        },
        help_text='确认密码，需与密码一致',
        style={'input_type': 'password'}
    )

    email = serializers.EmailField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            'invalid': '邮箱格式不正确'
        },
        help_text='用户邮箱（可选）'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email']
        extra_kwargs = {
            'email': {'required': False}
        }

    def validate_username(self, value):
        """
        验证用户名唯一性

        Args:
            value: 用户名

        Returns:
            str: 验证通过的用户名

        Raises:
            serializers.ValidationError: 用户名已存在
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已被注册')
        return value

    def validate_email(self, value):
        """
        验证邮箱唯一性

        Args:
            value: 邮箱地址

        Returns:
            str: 验证通过的邮箱

        Raises:
            serializers.ValidationError: 邮箱已存在
        """
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def validate_password(self, value):
        """
        验证密码强度

        Args:
            value: 密码

        Returns:
            str: 验证通过的密码

        Raises:
            serializers.ValidationError: 密码强度不足
        """
        try:
            validate_password(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e.messages[0]) if e.messages else '密码强度不足')
        return value

    def validate(self, attrs):
        """
        联合验证：确认密码是否一致

        Args:
            attrs: 所有字段数据

        Returns:
            dict: 验证通过的数据

        Raises:
            serializers.ValidationError: 两次密码不一致
        """
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({'password_confirm': '两次输入的密码不一致'})

        return attrs

    def create(self, validated_data):
        """
        创建用户和用户资料

        Args:
            validated_data: 验证通过的数据

        Returns:
            User: 创建的用户实例
        """
        # 移除确认密码字段（不需要保存到数据库）
        validated_data.pop('password_confirm', None)

        # 创建用户
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        # 创建用户资料（使用默认值）
        UserProfile.objects.create(
            user=user,
            nickname=validated_data['username'],  # 默认昵称为用户名
            bio='',
            avatar_url=''
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用户基础序列化器

    用于返回用户基本信息（不含敏感数据）。
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'created_at']
        read_only_fields = fields


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户资料序列化器

    用于序列化用户资料信息。
    """
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'username', 'nickname', 'phone', 'bio', 'avatar_url', 'created_at']
        read_only_fields = ['user_id', 'username', 'created_at']
