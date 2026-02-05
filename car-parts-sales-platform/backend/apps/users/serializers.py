from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserAddress, BrowsingHistory


class UserSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    class Meta:
        model = User
        fields = ('id', 'phone', 'nickname', 'avatar', 'email', 'points', 'status', 'created_at')
        read_only_fields = ('id', 'points', 'status', 'created_at')


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器（注册）"""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('phone', 'password', 'password_confirm', 'nickname', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname', ''),
            email=validated_data.get('email', '')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器 - 明文密码验证（根据用户要求）"""
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not phone:
            raise serializers.ValidationError({'phone': '手机号不能为空'})

        if not password:
            raise serializers.ValidationError({'password': '密码不能为空'})

        # 直接查询用户并明文比较密码
        try:
            user = User.objects.get(phone=phone)
            if user.password != password:  # 明文密码比较
                raise serializers.ValidationError({'non_field_errors': ['用户名或密码错误']})

            if user.status != 'active':
                raise serializers.ValidationError({'non_field_errors': ['账户已被禁用']})
        except User.DoesNotExist:
            raise serializers.ValidationError({'non_field_errors': ['用户名或密码错误']})

        # 生成 token
        refresh = RefreshToken.for_user(user)
        attrs['token'] = str(refresh.access_token)
        attrs['refresh'] = str(refresh)
        attrs['user'] = user
        return attrs


class UserAddressSerializer(serializers.ModelSerializer):
    """收货地址序列化器"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'recipient_name', 'phone', 'province', 'city',
                  'district', 'address', 'is_default', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class UserAddressCreateSerializer(serializers.ModelSerializer):
    """收货地址创建序列化器"""
    class Meta:
        model = UserAddress
        fields = ('recipient_name', 'phone', 'province', 'city', 'district',
                  'address', 'is_default')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return UserAddress.objects.create(**validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """用户资料更新序列化器"""
    class Meta:
        model = User
        fields = ('nickname', 'avatar', 'email')


class BrowsingHistorySerializer(serializers.ModelSerializer):
    """浏览历史序列化器"""
    class Meta:
        model = BrowsingHistory
        fields = ('id', 'product_id', 'product_name', 'product_image', 'product_price', 'viewed_at')
        read_only_fields = ('id', 'viewed_at')
