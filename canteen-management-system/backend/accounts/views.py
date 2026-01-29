from rest_framework import viewsets
from rest_framework.decorators import action

from .models import User, SystemSettings
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    UserListSerializer,
    SystemSettingsSerializer
)
from utils.response import ApiResponse


class UserViewSet(viewsets.ModelViewSet):
    """
    用户账号视图集
    提供用户登录、注册、列表、详情、更新、删除等接口
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """
        根据不同的操作返回不同的序列化器
        """
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        用户登录接口
        POST /api/accounts/login/
        请求体：{"username": "admin", "password": "admin123"}
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = User.verify_password(username, password)
            if user:
                user_data = UserSerializer(user).data
                return ApiResponse.success(data=user_data, message='登录成功')

            return ApiResponse.unauthorized(message='用户名或密码错误')

        return ApiResponse.error(message='请求参数错误', errors=serializer.errors)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        用户注册接口
        POST /api/accounts/register/
        请求体：{"username": "test_user", "password": "123456", "phone": "13800138000", "email": "test@example.com"}
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # 创建新用户，默认角色为 EMPLOYEE
            user = User.objects.create(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],  # 开发阶段明文存储
                role=User.Role.EMPLOYEE,
                status=User.Status.ENABLED
            )
            user_data = UserSerializer(user).data
            return ApiResponse.success(data=user_data, message='注册成功', code=201)

        return ApiResponse.error(message='注册失败', errors=serializer.errors)

    def list(self, request, *args, **kwargs):
        """
        用户列表接口（仅管理员）
        GET /api/accounts/users/
        """
        # TODO: 添加权限验证，只允许管理员访问
        serializer = UserListSerializer(self.queryset, many=True)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def retrieve(self, request, *args, **kwargs):
        """
        用户详情接口
        GET /api/accounts/users/{id}/
        """
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    def create(self, request, *args, **kwargs):
        """
        创建用户接口（管理员）
        POST /api/accounts/users/
        请求体：{"username": "new_user", "password": "123456", "role": "EMPLOYEE", "employee_id": 1}
        """
        # TODO: 添加权限验证，只允许管理员访问
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='创建成功', code=201)

        return ApiResponse.error(message='创建失败', errors=serializer.errors)

    def update(self, request, *args, **kwargs):
        """
        更新用户接口
        PUT /api/accounts/users/{id}/
        """
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='更新成功')

        return ApiResponse.error(message='更新失败', errors=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """
        删除用户接口
        DELETE /api/accounts/users/{id}/
        """
        instance = self.get_object()
        instance.delete()
        return ApiResponse.success(message='删除成功')

    @action(detail=False, methods=['get'], url_path='settings')
    def get_settings(self, request):
        """
        获取系统设置

        GET /api/accounts/settings/

        返回系统当前的考勤规则和薪资计算配置

        Returns:
            {
                "code": 200,
                "message": "获取成功",
                "data": {
                    "grace_period_minutes": 5,
                    "early_leave_grace_minutes": 5,
                    "late_deduction": "20.00",
                    "missing_deduction": "50.00",
                    "days_per_month": "21.75",
                    "hours_per_day": "8.00",
                    "overtime_rate": "1.50"
                }
            }
        """
        settings = SystemSettings.get_settings()
        serializer = SystemSettingsSerializer(settings)
        return ApiResponse.success(data=serializer.data, message='获取成功')

    @action(detail=False, methods=['put', 'patch'], url_path='settings')
    def update_settings(self, request):
        """
        更新系统设置

        PUT /api/accounts/settings/
        PATCH /api/accounts/settings/

        请求参数：
            - grace_period_minutes: 迟到宽限时间（分钟），范围 0-60
            - early_leave_grace_minutes: 早退宽限时间（分钟），范围 0-60
            - late_deduction: 迟到扣款（元/次），范围 0-500
            - missing_deduction: 缺卡扣款（元/次），范围 0-500
            - days_per_month: 月计薪天数，范围 20-23
            - hours_per_day: 日工作小时数，范围 4-12
            - overtime_rate: 加班工资倍率，范围 1-3

        Returns:
            更新后的系统设置数据
        """
        settings = SystemSettings.get_settings()
        serializer = SystemSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(data=serializer.data, message='设置保存成功')

        return ApiResponse.error(message='设置保存失败', errors=serializer.errors)

    @action(detail=False, methods=['get'], url_path='roles')
    def get_roles(self, request):
        """
        获取角色列表

        GET /api/accounts/roles/

        返回系统中可用的角色及其说明

        Returns:
            {
                "code": 200,
                "message": "获取成功",
                "data": [
                    {
                        "value": "ADMIN",
                        "label": "管理员",
                        "description": "拥有系统全部管理权限"
                    },
                    {
                        "value": "EMPLOYEE",
                        "label": "普通员工",
                        "description": "仅可查看和操作个人相关功能"
                    }
                ]
            }
        """
        roles = [
            {
                'value': User.Role.ADMIN,
                'label': User.Role.ADMIN.label,
                'description': '拥有系统全部管理权限，可进行所有操作'
            },
            {
                'value': User.Role.EMPLOYEE,
                'label': User.Role.EMPLOYEE.label,
                'description': '仅可查看和操作个人相关功能'
            }
        ]
        return ApiResponse.success(data=roles, message='获取成功')

    @action(detail=True, methods=['post'], url_path='change_password')
    def change_password(self, request, pk=None):
        """
        修改密码接口

        POST /api/accounts/{id}/change_password/
        请求体：{"old_password": "old123", "new_password": "new123"}

        允许用户修改自己的密码（需要验证旧密码）

        Returns:
            成功时返回 200 状态码
            失败时返回错误信息
        """
        user = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return ApiResponse.error(message='请提供旧密码和新密码')

        # 验证旧密码是否正确
        if user.password != old_password:
            return ApiResponse.unauthorized(message='旧密码错误')

        # 更新密码
        user.password = new_password
        user.save()

        return ApiResponse.success(message='密码修改成功')
