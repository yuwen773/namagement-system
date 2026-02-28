from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserAdminSerializer,
    UserStatusSerializer,
    PasswordChangeSerializer,
    SystemConfigSerializer,
    SystemConfigUpdateSerializer,
    CrawlerConfigSerializer
)
from .permissions import IsAdminUser, IsAdminOrSelf

User = get_user_model()


class APIResponseMixin:
    """统一API响应格式"""

    def success_response(self, data=None, message="操作成功", total=None):
        response_data = {"code": 0, "message": message}
        if data is not None:
            response_data["data"] = data
        if total is not None:
            response_data["total"] = total
        return Response(response_data)

    def error_response(self, message="操作失败", code=-1):
        return Response({"code": code, "message": message}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIResponseMixin, APIView):
    """用户注册"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # 检查用户名是否已存在
            username = serializer.validated_data.get('username')
            if User.objects.filter(username=username).exists():
                return self.error_response("用户名已存在")

            # 创建用户
            user = serializer.save()
            response_data = {
                "id": str(user.id),
                "username": user.username,
                "role": user.role,
                "email": user.email
            }
            return self.success_response(response_data, "注册成功")
        return self.error_response(str(serializer.errors))


class LoginView(APIResponseMixin, APIView):
    """用户登录"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # 明文密码验证（仅限开发/测试环境）
            try:
                user = User.objects.get(username=username)
                if user.password != password:
                    return self.error_response("用户名或密码错误", code=401)
            except User.DoesNotExist:
                return self.error_response("用户名或密码错误", code=401)

            # 检查用户状态
            if user.status == User.Status.FROZEN:
                return self.error_response("账号已被冻结", code=403)

            # 生成 JWT Token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response_data = {
                "access_token": str(access_token),
                "refresh_token": str(refresh),
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "avatar": user.avatar
                }
            }
            return self.success_response(response_data, "登录成功")

        return self.error_response(str(serializer.errors))


class UserProfileView(APIResponseMixin, APIView):
    """用户个人信息"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取个人信息"""
        serializer = UserSerializer(request.user)
        return self.success_response(serializer.data)

    def put(self, request):
        """更新个人信息"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(serializer.data, "更新成功")
        return self.error_response(str(serializer.errors))


class PasswordChangeView(APIResponseMixin, APIView):
    """修改密码"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # 明文密码验证（仅限开发/测试环境）
            if request.user.password != old_password:
                return self.error_response("原密码错误")

            # 设置新密码
            try:
                validate_password(new_password, request.user)
            except ValidationError as e:
                return self.error_response(str(e))

            # 明文密码存储（仅限开发/测试环境）
            request.user.password = new_password
            request.user.save()
            return self.success_response(message="密码修改成功")

        return self.error_response(str(serializer.errors))


class UserListView(APIResponseMixin, generics.ListAPIView):
    """用户列表（管理员）"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserAdminSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.success_response(serializer.data, total=queryset.count())


class UserDetailView(APIResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    """用户详情（管理员）"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserAdminSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(serializer.data, "更新成功")
        return self.error_response(str(serializer.errors))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return self.success_response(message="删除成功")


class UserStatusView(APIResponseMixin, APIView):
    """用户状态管理（冻结/解冻）"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, id):
        """更新用户状态"""
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return self.error_response("用户不存在", code=404)

        serializer = UserStatusSerializer(data=request.data)
        if serializer.is_valid():
            user.status = serializer.validated_data['status']
            user.save()
            return self.success_response(
                {"status": user.status, "status_display": user.get_status_display()},
                f"用户已{user.get_status_display()}"
            )
        return self.error_response(str(serializer.errors))


class UserResetPasswordView(APIResponseMixin, APIView):
    """重置用户密码（管理员）"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, id):
        """重置密码为默认密码 123456"""
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return self.error_response("用户不存在", code=404)

        # 明文密码存储（仅限开发/测试环境）
        user.password = '123456'
        user.save()
        return self.success_response(message="密码已重置为 123456")


class SystemConfigListView(APIResponseMixin, generics.ListAPIView):
    """系统配置列表（管理员）"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SystemConfigSerializer

    def get_queryset(self):
        from .models import SystemConfig
        config_type = self.request.query_params.get('type')
        queryset = SystemConfig.objects.all()
        if config_type:
            queryset = queryset.filter(config_type=config_type)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.success_response(serializer.data, total=queryset.count())


class SystemConfigDetailView(APIResponseMixin, APIView):
    """系统配置详情和更新（管理员）"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, key):
        """获取配置详情"""
        from .models import SystemConfig
        try:
            config = SystemConfig.objects.get(key=key)
            serializer = SystemConfigSerializer(config)
            return self.success_response(serializer.data)
        except SystemConfig.DoesNotExist:
            return self.error_response("配置不存在", code=404)

    def put(self, request, key):
        """更新配置"""
        from .models import SystemConfig
        try:
            config = SystemConfig.objects.get(key=key)
        except SystemConfig.DoesNotExist:
            # 如果配置不存在，创建新配置
            SystemConfig.objects.create(
                key=key,
                value=request.data.get('value', ''),
                config_type=request.data.get('config_type', 'crawler'),
                description=request.data.get('description', ''),
                updated_by=request.user
            )
            return self.success_response(message="配置创建成功")

        serializer = SystemConfigUpdateSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return self.success_response(serializer.data, "配置更新成功")
        return self.error_response(str(serializer.errors))


class CrawlerConfigView(APIResponseMixin, APIView):
    """爬虫配置管理（管理员）"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """获取爬虫配置"""
        from .models import SystemConfig

        cookie = SystemConfig.get_value('taobao_cookie', '')
        cookie_status = 'not_configured'
        last_test_time = None
        test_result = ''

        if cookie:
            cookie_status = 'configured'
            # 获取测试结果
            last_test_time = SystemConfig.get_value('taobao_cookie_test_time')
            test_result = SystemConfig.get_value('taobao_cookie_test_result', '')

        data = {
            'taobao_cookie': cookie[:20] + '...' if cookie and len(cookie) > 20 else cookie,
            'cookie_status': cookie_status,
            'last_test_time': last_test_time,
            'test_result': test_result
        }
        return self.success_response(data)

    def post(self, request):
        """更新爬虫配置"""
        from .models import SystemConfig

        cookie = request.data.get('taobao_cookie', '')

        if not cookie:
            return self.error_response("Cookie 不能为空")

        # 保存 Cookie
        SystemConfig.set_value(
            'taobao_cookie',
            cookie,
            config_type='crawler',
            description='淘宝/天猫 Cookie 用于数据采集',
            updated_by=request.user
        )

        return self.success_response(message="Cookie 配置已更新")


class TestCookieView(APIResponseMixin, APIView):
    """测试 Cookie 连接（管理员）"""
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """测试 Cookie 是否有效"""
        from .models import SystemConfig
        from crawler.spiders.taobao_mtop_api import TaobaoMtopAPI
        from django.utils import timezone

        cookie = SystemConfig.get_value('taobao_cookie', '')

        if not cookie:
            return self.error_response("Cookie 未配置，请先保存 Cookie", code=400)

        try:
            # 测试连接
            api = TaobaoMtopAPI(cookie=cookie)
            result = api.test_connection("高达模型")

            # 保存测试结果
            SystemConfig.set_value(
                'taobao_cookie_test_time',
                str(timezone.now()),
                config_type='crawler',
                description='Cookie 测试时间'
            )

            # 判断错误类型并给出友好提示
            if result['success']:
                SystemConfig.set_value(
                    'taobao_cookie_test_result',
                    'success',
                    config_type='crawler',
                    description='Cookie 测试结果'
                )
                return self.success_response({
                    'test_time': str(timezone.now()),
                    'result': 'success',
                    'message': result['message']
                }, "Cookie 测试成功")
            else:
                error_msg = result['message']
                # 根据错误类型提供更友好的提示
                if 'TOKEN_EXOIRED' in error_msg or 'token' in error_msg.lower():
                    friendly_msg = "Cookie 已过期，请重新从浏览器获取最新的 Cookie"
                elif 'FAIL' in error_msg:
                    friendly_msg = f"Cookie 无效: {error_msg}"
                else:
                    friendly_msg = error_msg

                SystemConfig.set_value(
                    'taobao_cookie_test_result',
                    f'failed: {error_msg}',
                    config_type='crawler',
                    description='Cookie 测试结果'
                )
                return self.error_response(friendly_msg, code=400)

        except Exception as e:
            # 保存测试结果
            SystemConfig.set_value(
                'taobao_cookie_test_time',
                str(timezone.now()),
                config_type='crawler'
            )
            SystemConfig.set_value(
                'taobao_cookie_test_result',
                f'error: {str(e)}',
                config_type='crawler'
            )
            return self.error_response(f"Cookie 测试异常: {str(e)}", code=500)

