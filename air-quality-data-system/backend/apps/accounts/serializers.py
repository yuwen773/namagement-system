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
    username = serializers.CharField(
        max_length=150,
        error_messages={"required": "请输入用户名", "blank": "用户名不能为空"}
    )
    password = serializers.CharField(
        max_length=128,
        error_messages={"required": "请输入密码", "blank": "密码不能为空"}
    )


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=3,
        max_length=20,
        error_messages={
            "required": "请输入用户名",
            "blank": "用户名不能为空",
            "min_length": "用户名长度至少需要3位",
            "max_length": "用户名长度不能超过20位"
        }
    )
    password = serializers.CharField(
        min_length=6,
        max_length=20,
        write_only=True,
        error_messages={
            "required": "请输入密码",
            "blank": "密码不能为空",
            "min_length": "密码长度至少需要6位",
            "max_length": "密码长度不能超过20位"
        }
    )
    email = serializers.EmailField(
        error_messages={
            "required": "请输入邮箱地址",
            "blank": "邮箱地址不能为空",
            "invalid": "请输入有效的邮箱地址"
        }
    )
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={"max_length": "手机号长度不能超过20位"}
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被注册，请更换其他用户名")
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
    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={"max_length": "手机号长度不能超过20位"}
    )
    email = serializers.EmailField(
        error_messages={"required": "请输入邮箱地址", "blank": "邮箱地址不能为空", "invalid": "请输入有效的邮箱地址"}
    )
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        error_messages={"required": "请选择用户角色", "invalid_choice": "用户角色无效"}
    )
    status = serializers.BooleanField(
        error_messages={"required": "请选择用户状态"}
    )

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
