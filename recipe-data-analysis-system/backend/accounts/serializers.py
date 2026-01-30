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


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    更新用户资料序列化器

    用于更新用户个人资料信息。
    验证规则：
    - 昵称：可选，最大50个字符
    - 个人简介：可选，最大500个字符
    - 头像 URL：可选，需符合 URL 格式
    - 手机号：可选，需符合手机号格式且唯一
    """

    nickname = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': '昵称不能超过50个字符'
        },
        help_text='用户显示的昵称'
    )

    bio = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': '个人简介不能超过500个字符'
        },
        help_text='用户自我介绍'
    )

    avatar_url = serializers.URLField(
        max_length=500,
        required=False,
        allow_blank=True,
        error_messages={
            'invalid': '头像 URL 格式不正确'
        },
        help_text='用户头像图片地址'
    )

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            'max_length': '手机号不能超过20个字符'
        },
        help_text='用户手机号码'
    )

    class Meta:
        model = UserProfile
        fields = ['nickname', 'phone', 'bio', 'avatar_url']

    def validate_phone(self, value):
        """
        验证手机号格式和唯一性

        Args:
            value: 手机号

        Returns:
            str: 验证通过的手机号

        Raises:
            serializers.ValidationError: 手机号格式不正确或已被使用
        """
        import re

        # 如果为空或 None，直接返回
        if not value:
            return value

        # 验证手机号格式（支持中国大陆手机号）
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')

        # 检查手机号是否已被其他用户使用
        # 排除当前用户的资料
        if self.instance and hasattr(self.instance, 'id'):
            if UserProfile.objects.exclude(id=self.instance.id).filter(phone=value).exists():
                raise serializers.ValidationError('该手机号已被使用')
        elif UserProfile.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已被使用')

        return value


class LoginSerializer(serializers.Serializer):
    """
    用户登录序列化器

    处理用户登录请求的数据验证。
    验证规则：
    - 用户名必填
    - 密码必填
    - 验证用户名和密码是否匹配
    - 验证账户是否激活
    """

    username = serializers.CharField(
        max_length=50,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'blank': '用户名不能为空'
        },
        help_text='用户登录名'
    )

    password = serializers.CharField(
        max_length=128,
        required=True,
        write_only=True,
        error_messages={
            'required': '密码不能为空',
            'blank': '密码不能为空'
        },
        help_text='用户密码',
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """
        验证用户名和密码是否正确

        Args:
            attrs: 包含 username 和 password 的字典

        Returns:
            dict: 验证通过的数据，包含 user 实例

        Raises:
            serializers.ValidationError: 用户名或密码错误、账户未激活
        """
        from django.contrib.auth import authenticate

        username = attrs.get('username')
        password = attrs.get('password')

        # 使用 Django 的 authenticate 函数验证用户名和密码
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('用户名或密码错误')

        if not user.is_active:
            raise serializers.ValidationError('该账户已被禁用，请联系管理员')

        # 将验证通过的用户实例添加到返回数据中
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    修改密码序列化器

    处理用户修改密码请求的数据验证。
    验证规则：
    - 旧密码必填，需与当前密码一致
    - 新密码必填，至少8位，需通过密码强度验证
    - 确认新密码必填，需与新密码一致
    """

    old_password = serializers.CharField(
        max_length=128,
        required=True,
        write_only=True,
        error_messages={
            'required': '旧密码不能为空',
            'blank': '旧密码不能为空'
        },
        help_text='当前使用的密码',
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        max_length=128,
        min_length=8,
        required=True,
        write_only=True,
        error_messages={
            'required': '新密码不能为空',
            'blank': '新密码不能为空',
            'min_length': '新密码至少需要8个字符'
        },
        help_text='新的密码，至少8个字符',
        style={'input_type': 'password'}
    )

    new_password_confirm = serializers.CharField(
        max_length=128,
        min_length=8,
        required=True,
        write_only=True,
        error_messages={
            'required': '确认新密码不能为空',
            'blank': '确认新密码不能为空'
        },
        help_text='确认新密码，需与新密码一致',
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        """
        验证旧密码是否正确

        Args:
            value: 旧密码

        Returns:
            str: 验证通过的旧密码

        Raises:
            serializers.ValidationError: 旧密码不正确
        """
        # 从上下文中获取用户实例
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError('无法获取用户信息')

        # 验证旧密码是否正确
        if not user.check_password(value):
            raise serializers.ValidationError('旧密码不正确')

        return value

    def validate_new_password(self, value):
        """
        验证新密码强度

        Args:
            value: 新密码

        Returns:
            str: 验证通过的新密码

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
        联合验证：新密码和确认新密码是否一致

        Args:
            attrs: 所有字段数据

        Returns:
            dict: 验证通过的数据

        Raises:
            serializers.ValidationError: 两次新密码不一致
        """
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        old_password = attrs.get('old_password')

        if new_password != new_password_confirm:
            raise serializers.ValidationError({'new_password_confirm': '两次输入的新密码不一致'})

        # 验证新密码不能与旧密码相同
        if new_password == old_password:
            raise serializers.ValidationError({'new_password': '新密码不能与旧密码相同'})

        return attrs

    def save(self):
        """
        保存新密码

        Returns:
            User: 更新后的用户实例
        """
        user = self.context.get('user')
        new_password = self.validated_data.get('new_password')

        # 设置新密码（会自动加密）
        user.set_password(new_password)
        user.save()

        return user
