from rest_framework import serializers

from .models import User


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "role",
            "status",
            "is_deleted",
            "date_joined",
            "last_login",
        ]
        read_only_fields = fields


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=20)
    password = serializers.CharField(min_length=6, max_length=20, write_only=True)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data.get("phone") or None,
            role=User.Role.USER,
            status=True,
            is_deleted=False,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "role",
            "status",
            "is_deleted",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "is_staff", "is_superuser", "date_joined", "last_login"]
