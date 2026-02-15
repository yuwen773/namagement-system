from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器

    用于处理用户注册请求，验证并创建新用户账号。

    字段说明：
        username: 用户名（必填，唯一）
        password: 密码（必填，最少6位）
        password_confirm: 确认密码（必填，需与密码一致）
        email: 邮箱地址（选填）
        real_name: 真实姓名（选填）
        phone: 手机号码（选填）

    验证规则：
        - 两次密码输入必须一致
        - 密码长度不能少于6位
        - 用户名必须唯一
    """
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        help_text='用户密码，最少6位字符'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        help_text='确认密码，必须与密码字段一致'
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'real_name', 'phone']
        extra_kwargs = {
            'email': {'required': False, 'help_text': '邮箱地址'},
            'real_name': {'required': False, 'help_text': '真实姓名'},
            'phone': {'required': False, 'help_text': '手机号码'},
        }

    def validate(self, attrs):
        """
        验证两次密码输入是否一致

        Args:
            attrs: 待验证的字段字典

        Returns:
            dict: 验证通过后的字段字典（已移除 password_confirm）

        Raises:
            ValidationError: 当两次密码输入不一致时
        """
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': '两次密码输入不一致'})
        return attrs

    def create(self, validated_data):
        """
        创建新用户

        Args:
            validated_data: 验证通过后的数据字典

        Returns:
            User: 创建的用户对象
        """
        # 强制设置角色为普通用户
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            real_name=validated_data.get('real_name'),
            phone=validated_data.get('phone'),
            role='USER',
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器

    用于处理用户登录请求，验证用户凭据并返回用户信息。

    字段说明：
        username: 用户名（必填）
        password: 密码（必填）

    验证规则：
        - 用户名和密码不能为空
        - 用户名必须存在
        - 密码必须正确
        - 用户账号必须是启用状态
    """
    username = serializers.CharField(help_text='用户名')
    password = serializers.CharField(help_text='密码', write_only=True)

    def validate(self, attrs):
        """
        验证用户登录凭据

        Args:
            attrs: 包含 username 和 password 的字典

        Returns:
            dict: 验证通过后的字段字典，包含 user 对象

        Raises:
            ValidationError: 当用户名或密码错误、用户被禁用、或字段为空时
        """
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
    """
    用户信息序列化器

    用于序列化用户完整信息，主要用于管理员查看用户列表和详情。

    字段说明：
        id: 用户ID（只读）
        username: 用户名（只读）
        real_name: 真实姓名
        email: 邮箱地址
        phone: 手机号码
        role: 用户角色（只读）
        is_active: 账号状态（只读）
        created_at: 创建时间（只读）
        updated_at: 更新时间（只读）

    权限说明：
        普通字段可更新，只读字段仅用于展示
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'email', 'phone', 'role', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'role', 'is_active', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户个人信息序列化器

    用于序列化当前用户的个人信息，用于个人中心展示和更新。

    字段说明：
        id: 用户ID（只读）
        username: 用户名（只读）
        real_name: 真实姓名
        email: 邮箱地址
        phone: 手机号码
        role: 用户角色（只读）
        created_at: 创建时间（只读）

    使用场景：
        - 用户个人中心信息展示
        - 用户个人信息更新
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'email', 'phone', 'role', 'created_at']
        read_only_fields = ['id', 'username', 'role', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    """
    修改密码序列化器

    用于处理用户修改密码请求，验证并更新用户密码。

    字段说明：
        old_password: 原密码（必填）
        new_password: 新密码（必填，最少6位）

    验证规则：
        - 原密码必须正确
        - 新密码长度不能少于6位
    """
    old_password = serializers.CharField(
        required=True,
        help_text='原密码',
        write_only=True
    )
    new_password = serializers.CharField(
        required=True,
        min_length=6,
        help_text='新密码，最少6位字符',
        write_only=True
    )

    def validate_new_password(self, value):
        """
        验证新密码长度

        Args:
            value: 新密码值

        Returns:
            str: 验证通过的新密码

        Raises:
            ValidationError: 当密码长度少于6位时
        """
        if len(value) < 6:
            raise serializers.ValidationError('新密码长度不能少于6位')
        return value


class TokenResponseSerializer(serializers.Serializer):
    """
    Token 响应序列化器

    用于序列化登录成功后返回的 Token 信息和用户信息。

    字段说明：
        access_token: 访问令牌（JWT）
        refresh_token: 刷新令牌（JWT）
        user: 用户信息对象
    """
    access_token = serializers.CharField(help_text='JWT 访问令牌，用于API认证')
    refresh_token = serializers.CharField(help_text='JWT 刷新令牌，用于获取新的访问令牌')
    user = UserSerializer(help_text='当前登录用户信息')
