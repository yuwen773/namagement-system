import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, get_user_role

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        request = self.context.get("request")
        username = attrs.get("username")
        password = attrs.get("password")

        # 直接查询用户并明文校验密码
        try:
            user = User.objects.get(username=username)
            # 明文密码比较
            if user.password != password:
                raise serializers.ValidationError("用户名或密码错误")
        except User.DoesNotExist:
            raise serializers.ValidationError("用户名或密码错误")

        if not user.is_active:
            raise serializers.ValidationError("用户已被禁用")

        # 更新最后登录时间
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.last_login_time = timezone.now()
        profile.save()

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "role": get_user_role(user),
            },
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    """用户注册序列化器"""

    username = serializers.CharField(
        min_length=3, max_length=20, help_text="用户名(3-20个字符)"
    )
    password = serializers.CharField(
        min_length=6, write_only=True, help_text="密码(至少6个字符)"
    )
    email = serializers.EmailField(required=True, help_text="邮箱地址")

    def validate_username(self, value):
        """验证用户名唯一性和格式"""
        # 检查用户名格式: 只允许字母、数字、下划线
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "用户名只能包含字母、数字和下划线"
            )

        # 检查用户名是否已存在
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被注册")

        return value

    def validate_email(self, value):
        """验证邮箱唯一性"""
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value

    def validate_password(self, value):
        """验证密码强度"""
        validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        """创建新用户（明文密码）"""
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]

        try:
            # First check if user exists (atomic check)
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("该用户名已被注册")

            # 创建用户，直接设置明文密码
            user = User(username=username)
            user.password = password  # 明文存储
            user.save()

            # Create profile with get_or_create (defensive)
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={"email": email, "role": "user"}
            )
            if profile.email != email:
                profile.email = email
                profile.save()

        except IntegrityError:
            raise serializers.ValidationError("创建用户失败，请稍后重试")

        return user


class CheckUsernameSerializer(serializers.Serializer):
    """检查用户名是否可用"""

    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被注册")
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError("用户名只能包含字母、数字和下划线")
        return value


class CheckEmailSerializer(serializers.Serializer):
    """检查邮箱是否可用"""

    email = serializers.EmailField()

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value


class UserSerializer(serializers.ModelSerializer):
    """用户列表展示序列化器(只读)"""

    role = serializers.CharField(source="profile.role", read_only=True)
    email = serializers.EmailField(source="profile.email", read_only=True)
    is_active = serializers.BooleanField(source="profile.is_active", read_only=True)
    last_login_time = serializers.DateTimeField(
        source="profile.last_login_time", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "role",
            "email",
            "is_active",
            "last_login_time",
            "date_joined",
        ]


class UserManageSerializer(serializers.ModelSerializer):
    """用户管理序列化器(创建/更新)"""

    role = serializers.ChoiceField(
        choices=UserProfile.USER_ROLE, default="user", required=False
    )
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "role", "email", "password"]
        read_only_fields = ["id"]

    def validate_email(self, value):
        """验证邮箱唯一性(更新时排除自己)"""
        if value and value.strip():
            instance = self.instance
            queryset = UserProfile.objects.filter(email=value)
            if instance:
                queryset = queryset.exclude(user_id=instance.id)
            if queryset.exists():
                raise serializers.ValidationError("该邮箱已被使用")
        return value.strip() if value else None

    def validate_username(self, value):
        """验证用户名唯一性(更新时排除自己)"""
        instance = self.instance
        queryset = User.objects.filter(username=value)
        if instance:
            queryset = queryset.exclude(id=instance.id)
        if queryset.exists():
            raise serializers.ValidationError("该用户名已被使用")
        return value

    @transaction.atomic
    def create(self, validated_data):
        """创建用户并设置档案（明文密码）"""
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", "user")
        email = validated_data.pop("email", None)

        try:
            user = User(**validated_data)
            if password:
                user.password = password  # 明文存储密码
            user.save()

            UserProfile.objects.get_or_create(
                user=user,
                defaults={"role": role, "email": email}
            )
        except IntegrityError:
            raise serializers.ValidationError("创建用户失败，请稍后重试")

        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        """更新用户和档案（明文密码）"""
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", None)
        email = validated_data.pop("email", None)

        # 更新用户基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = password  # 明文存储密码
        instance.save()

        # 使用 get_or_create 获取用户档案（防御性编程）
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        if role is not None:
            profile.role = role
        if email is not None:
            profile.email = email if email.strip() else None
        profile.save()

        return instance


class UpdateStatusSerializer(serializers.Serializer):
    """更新用户状态序列化器"""

    user_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    is_active = serializers.BooleanField()

    def validate_user_ids(self, value):
        """验证用户ID是否存在"""
        existing_ids = User.objects.filter(id__in=value).values_list(
            "id", flat=True
        )
        invalid_ids = set(value) - set(existing_ids)
        if invalid_ids:
            raise serializers.ValidationError(
                f"以下用户ID不存在: {', '.join(map(str, invalid_ids))}"
            )
        return value


class UpdateRoleSerializer(serializers.Serializer):
    """更新用户角色序列化器"""

    user_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )
    role = serializers.ChoiceField(choices=UserProfile.USER_ROLE)

    def validate_user_ids(self, value):
        """验证用户ID是否存在"""
        existing_ids = User.objects.filter(id__in=value).values_list(
            "id", flat=True
        )
        invalid_ids = set(value) - set(existing_ids)
        if invalid_ids:
            raise serializers.ValidationError(
                f"以下用户ID不存在: {', '.join(map(str, invalid_ids))}"
            )
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """重置密码序列化器（明文密码）"""

    user_id = serializers.IntegerField()
    new_password = serializers.CharField()

    def validate_user_id(self, value):
        """验证用户ID是否存在"""
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("用户不存在")
        return value

    def validate_new_password(self, value):
        """验证密码强度"""
        validate_password(value)
        return value

    def save(self):
        """重置用户密码（明文存储）"""
        user_id = self.validated_data["user_id"]
        new_password = self.validated_data["new_password"]
        user = User.objects.get(id=user_id)
        user.password = new_password  # 明文存储密码
        user.save()
        return user
