
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from apps.accounts.models import UserProfile, UserRole
from apps.buildings.models import Room
from apps.system.models import Notice, OperationLog


User = get_user_model()

DEFAULT_ALARM_SUBSCRIPTIONS = {
    "balance_insufficient": True,
    "abnormal_usage": True,
}


def _ensure_profile(user):
    profile = getattr(user, "profile", None)
    if profile is None:
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "role": UserRole.USER,
                "alarm_subscriptions": DEFAULT_ALARM_SUBSCRIPTIONS.copy(),
            },
        )
    if not profile.alarm_subscriptions:
        profile.alarm_subscriptions = DEFAULT_ALARM_SUBSCRIPTIONS.copy()
        profile.save(update_fields=["alarm_subscriptions", "updated_at"])
    return profile


class UserManagementSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        min_length=6,
        trim_whitespace=False,
    )
    role = serializers.ChoiceField(choices=UserRole.choices, required=False)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=32)
    avatar = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)
    bind_rooms = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        allow_empty=True,
    )
    balance = serializers.DecimalField(max_digits=14, decimal_places=2, required=False)
    alarm_subscriptions = serializers.DictField(
        child=serializers.BooleanField(),
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "role",
            "phone",
            "avatar",
            "bind_rooms",
            "balance",
            "alarm_subscriptions",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")

    def validate_bind_rooms(self, value):
        room_ids = sorted(set(int(item) for item in value))
        room_count = Room.objects.filter(id__in=room_ids).count()
        if room_count != len(room_ids):
            raise serializers.ValidationError("存在无效的房间ID。")
        return room_ids

    def validate_alarm_subscriptions(self, value):
        payload = DEFAULT_ALARM_SUBSCRIPTIONS.copy()
        payload.update(value)
        return payload

    def _apply_profile(self, user, profile_data):
        profile = _ensure_profile(user)
        for key, value in profile_data.items():
            setattr(profile, key, value)
        if profile_data:
            profile.save(update_fields=[*profile_data.keys(), "updated_at"])
        return profile

    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile = _ensure_profile(instance)
        data["role"] = profile.role
        data["phone"] = profile.phone
        data["avatar"] = profile.avatar
        data["bind_rooms"] = profile.bind_rooms
        data["balance"] = profile.balance
        data["alarm_subscriptions"] = profile.alarm_subscriptions or DEFAULT_ALARM_SUBSCRIPTIONS.copy()
        return data

    def create(self, validated_data):
        profile_data = {
            "role": validated_data.pop("role", UserRole.USER),
            "phone": validated_data.pop("phone", None),
            "avatar": validated_data.pop("avatar", None),
            "bind_rooms": validated_data.pop("bind_rooms", []),
            "balance": validated_data.pop("balance", Decimal("0.00")),
            "alarm_subscriptions": validated_data.pop(
                "alarm_subscriptions",
                DEFAULT_ALARM_SUBSCRIPTIONS.copy(),
            ),
        }
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError({"password": "创建用户时必须提供密码。"})
        user = User.objects.create_user(password=password, **validated_data)
        self._apply_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = {}
        for field_name in ("role", "phone", "avatar", "bind_rooms", "balance", "alarm_subscriptions"):
            if field_name in validated_data:
                profile_data[field_name] = validated_data.pop(field_name)

        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        self._apply_profile(instance, profile_data)
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, min_length=6, trim_whitespace=False)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "两次输入的新密码不一致。"})
        return attrs


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")
        read_only_fields = ("id",)


class UserNoticeSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source="publisher.username", read_only=True)

    class Meta:
        model = Notice
        fields = (
            "id",
            "title",
            "content",
            "category",
            "notice_type",
            "priority",
            "publish_time",
            "is_published",
            "target_role",
            "publisher_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class AdminNoticeSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source="publisher.username", read_only=True)

    class Meta:
        model = Notice
        fields = (
            "id",
            "title",
            "content",
            "category",
            "notice_type",
            "priority",
            "publish_time",
            "is_published",
            "target_role",
            "publisher",
            "publisher_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "publisher", "created_at", "updated_at")


class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = (
            "id",
            "title",
            "content",
            "category",
            "publish_time",
        )
        read_only_fields = fields


class AdminTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = (
            "id",
            "title",
            "content",
            "category",
            "publish_time",
            "is_published",
            "target_role",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class OperationLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = OperationLog
        fields = (
            "id",
            "user",
            "user_name",
            "action",
            "resource",
            "ip_address",
            "user_agent",
            "request_method",
            "request_path",
            "create_time",
        )
        read_only_fields = fields


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    role = serializers.ChoiceField(choices=UserRole.choices, read_only=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=32)
    avatar = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)
    bind_rooms = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        read_only=True,
    )
    balance = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    alarm_subscriptions = serializers.DictField(child=serializers.BooleanField(), read_only=True)

    def to_representation(self, instance):
        profile = _ensure_profile(instance)
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "role": profile.role,
            "phone": profile.phone,
            "avatar": profile.avatar,
            "bind_rooms": profile.bind_rooms,
            "balance": profile.balance,
            "alarm_subscriptions": profile.alarm_subscriptions or DEFAULT_ALARM_SUBSCRIPTIONS.copy(),
        }

    def update(self, instance, validated_data):
        profile = _ensure_profile(instance)
        for field_name in ("email", "first_name", "last_name"):
            if field_name in validated_data:
                setattr(instance, field_name, validated_data[field_name])
        instance.save(update_fields=["email", "first_name", "last_name"])

        profile_updates = {}
        if "phone" in validated_data:
            profile_updates["phone"] = validated_data["phone"]
        if "avatar" in validated_data:
            profile_updates["avatar"] = validated_data["avatar"]
        for key, value in profile_updates.items():
            setattr(profile, key, value)
        if profile_updates:
            profile.save(update_fields=[*profile_updates.keys(), "updated_at"])
        return instance


class ProfileBindRoomsSerializer(serializers.Serializer):
    room_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )

    def validate_room_ids(self, value):
        room_ids = sorted(set(int(item) for item in value))
        room_count = Room.objects.filter(id__in=room_ids).count()
        if room_count != len(room_ids):
            raise serializers.ValidationError("存在无效的房间ID。")
        return room_ids


class ProfileAlarmSubscriptionSerializer(serializers.Serializer):
    balance_insufficient = serializers.BooleanField(required=False)
    abnormal_usage = serializers.BooleanField(required=False)

    def to_representation(self, instance):
        payload = DEFAULT_ALARM_SUBSCRIPTIONS.copy()
        if isinstance(instance, dict):
            payload.update(instance)
        return payload
