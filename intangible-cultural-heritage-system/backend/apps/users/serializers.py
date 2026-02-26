import re

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, get_user_role

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        request = self.context.get("request")
        user = authenticate(
            request=request,
            username=attrs.get("username"),
            password=attrs.get("password"),
        )

        if user is None:
            raise serializers.ValidationError("用户名或密码错误")
        if not user.is_active:
            raise serializers.ValidationError("用户已被禁用")

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

    def create(self, validated_data):
        """创建新用户"""
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data["email"]

        # 创建用户
        user = User.objects.create_user(username=username, password=password)

        # 创建用户档案并设置邮箱
        UserProfile.objects.create(user=user, email=email, role="user")

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

    def create(self, validated_data):
        """创建用户并设置档案"""
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", "user")
        email = validated_data.pop("email", None)

        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, role=role, email=email)
        return user

    def update(self, instance, validated_data):
        """更新用户和档案"""
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", None)
        email = validated_data.pop("email", None)

        # 更新用户基本信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # 更新用户档案
        profile = instance.profile
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
    """重置密码序列化器"""

    user_id = serializers.IntegerField()
    new_password = serializers.CharField(min_length=6)

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
        """重置用户密码"""
        user_id = self.validated_data["user_id"]
        new_password = self.validated_data["new_password"]
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        return user
