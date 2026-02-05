from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response import ApiResponse
from .models import User, UserAddress, BrowsingHistory
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserAddressSerializer,
    UserAddressCreateSerializer,
    UserProfileUpdateSerializer,
    BrowsingHistorySerializer,
)


class AuthViewSet(viewsets.ViewSet):
    """认证视图集"""
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册"""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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

    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        return ApiResponse.success(
            data={
                'token': token,
                'user': UserSerializer(user).data
            },
            message='登录成功'
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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ApiResponse.success(
            data=UserSerializer(request.user).data,
            message='资料更新成功'
        )

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """修改密码"""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return ApiResponse.error(message='请提供原密码和新密码')

        # 验证原密码（当前为明文存储）
        if request.user.password != old_password:
            return ApiResponse.error(message='原密码错误')

        # 更新密码
        request.user.password = new_password
        request.user.save()

        return ApiResponse.success(message='密码修改成功')


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

    @action(detail=True, methods=['post'], url_path='set-default')
    def set_default(self, request, pk=None):
        """设为默认地址"""
        address = self.get_object()
        address.is_default = True
        address.save()
        return ApiResponse.success(
            data=UserAddressSerializer(address).data,
            message='已设为默认地址'
        )


class BrowsingHistoryViewSet(viewsets.ViewSet):
    """浏览历史视图集"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BrowsingHistory.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def list_history(self, request):
        """获取浏览历史列表"""
        queryset = self.get_queryset()
        serializer = BrowsingHistorySerializer(queryset, many=True)
        return ApiResponse.success(data=serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """添加浏览记录"""
        product_id = request.data.get('product_id')
        product_name = request.data.get('product_name')
        product_image = request.data.get('product_image', '')
        product_price = request.data.get('product_price')

        if not product_id or not product_name:
            return ApiResponse.error(message='商品ID和商品名称不能缺少')

        # 删除该用户对此商品的旧浏览记录（去重）
        BrowsingHistory.objects.filter(
            user=request.user,
            product_id=product_id
        ).delete()

        # 创建新的浏览记录
        history = BrowsingHistory.objects.create(
            user=request.user,
            product_id=product_id,
            product_name=product_name,
            product_image=product_image,
            product_price=product_price
        )

        return ApiResponse.success(
            data=BrowsingHistorySerializer(history).data,
            message='浏览记录已添加'
        )

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """清空浏览历史"""
        count, _ = self.get_queryset().delete()
        return ApiResponse.success(
            data={'deleted_count': count},
            message=f'已清空 {count} 条浏览记录'
        )
