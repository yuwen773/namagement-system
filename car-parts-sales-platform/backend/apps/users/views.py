from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response import ApiResponse
from .models import User, UserAddress
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserAddressSerializer,
    UserAddressCreateSerializer,
    UserProfileUpdateSerializer,
)


class AuthViewSet(viewsets.ViewSet):
    """认证视图集"""
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册"""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 生成 token
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return ApiResponse.success(
                data={
                    'token': str(refresh.access_token),
                    'user': UserSerializer(user).data
                },
                message='注册成功'
            )
        return ApiResponse.error(
            message=serializer.errors.get('non_field_errors', ['注册失败'])[0],
            code=400
        )

    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = serializer.validated_data['token']
            return ApiResponse.success(
                data={
                    'token': token,
                    'user': UserSerializer(user).data
                },
                message='登录成功'
            )
        return ApiResponse.error(
            message=serializer.errors.get('non_field_errors', ['用户名或密码错误'])[0] if serializer.errors.get('non_field_errors') else '登录失败',
            code=400
        )


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 普通用户只能查看自己，管理员可以查看所有
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return ApiResponse.success(data=serializer.data)

    @action(detail=False, methods=['put'])
    def profile(self, request):
        """更新当前用户资料"""
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(
                data=UserSerializer(request.user).data,
                message='资料更新成功'
            )
        return ApiResponse.error(
            message=serializer.errors.get('non_field_errors', ['更新失败'])[0],
            code=400
        )


class UserAddressViewSet(viewsets.ModelViewSet):
    """用户地址视图集"""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserAddressCreateSerializer
        return UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        return ApiResponse.success(
            data=UserAddressSerializer(address).data,
            message='地址创建成功',
            code=201
        )

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """设为默认地址"""
        address = self.get_object()
        address.is_default = True
        address.save()
        return ApiResponse.success(
            data=UserAddressSerializer(address).data,
            message='已设为默认地址'
        )
