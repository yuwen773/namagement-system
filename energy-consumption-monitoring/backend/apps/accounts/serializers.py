
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from apps.accounts.models import UserProfile, UserRole


User = get_user_model()


def _ensure_profile(user):
    profile = getattr(user, "profile", None)
    if profile is None:
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "role": UserRole.USER,
                "alarm_subscriptions": {
                    "balance_insufficient": True,
                    "abnormal_usage": True,
                },
            },
        )
    if not profile.alarm_subscriptions:
        profile.alarm_subscriptions = {
            "balance_insufficient": True,
            "abnormal_usage": True,
        }
        profile.save(update_fields=["alarm_subscriptions", "updated_at"])
    return profile


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    bind_rooms = serializers.SerializerMethodField()
    alarm_subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone",
            "avatar",
            "bind_rooms",
            "alarm_subscriptions",
            "date_joined",
        )

    def get_role(self, obj):
        return _ensure_profile(obj).role

    def get_phone(self, obj):
        return _ensure_profile(obj).phone

    def get_avatar(self, obj):
        return _ensure_profile(obj).avatar

    def get_bind_rooms(self, obj):
        return _ensure_profile(obj).bind_rooms

    def get_alarm_subscriptions(self, obj):
        return _ensure_profile(obj).alarm_subscriptions


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6, trim_whitespace=False)
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=6,
        trim_whitespace=False,
    )
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=32)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "两次输入的密码不一致"})
        return attrs

    def create(self, validated_data):
        phone = validated_data.pop("phone", "")
        password = validated_data.pop("password")
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(password=password, **validated_data)
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "role": UserRole.USER,
                "alarm_subscriptions": {
                    "balance_insufficient": True,
                    "abnormal_usage": True,
                },
            },
        )
        if phone:
            profile.phone = phone
            profile.save(update_fields=["phone"])
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs.get("username"),
            password=attrs.get("password"),
        )
        if user is None:
            raise serializers.ValidationError("用户名或密码错误")
        if not user.is_active:
            raise serializers.ValidationError("用户已被禁用")
        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, min_length=6, trim_whitespace=False)
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=6,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "两次输入的新密码不一致"})
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError({"new_password": "新密码不能与旧密码相同"})
        return attrs
