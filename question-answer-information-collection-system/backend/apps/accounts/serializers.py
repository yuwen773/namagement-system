from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """自定义 Token 响应，包含用户信息"""

    def validate(self, attrs):
        data = super().validate(attrs)
        # 添加用户信息到响应
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义 Token 响应视图，添加 code 字段"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # 包装响应数据，添加 code 字段
        response.data = {
            'code': 0,
            'data': response.data,
            'message': '登录成功'
        }
        return response


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'role', 'is_active', 'date_joined']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器（注册用）- 明文密码存储"""

    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被使用")
        return value

    def create(self, validated_data):
        # 明文存储密码，不使用 create_user() 的哈希处理
        user = User(**validated_data)
        # 直接设置密码，不哈希
        user.password = validated_data['password']
        user.role = validated_data.get('role', 'user')
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""

    class Meta:
        model = User
        fields = ['username', 'email']
