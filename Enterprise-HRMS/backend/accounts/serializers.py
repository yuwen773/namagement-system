from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


def get_user_edit_request_model():
    """延迟导入 UserEditRequest，避免循环导入"""
    from .models import UserEditRequest
    return UserEditRequest


class PasswordStrengthValidator:
    """
    自定义密码强度验证器
    要求：至少8位，包含字母、数字、特殊字符
    """
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        import re

        errors = []

        # 检查最小长度
        if len(password) < self.min_length:
            errors.append(f'密码长度至少需要 {self.min_length} 个字符')

        # 检查是否包含字母
        if not re.search(r'[a-zA-Z]', password):
            errors.append('密码必须包含字母')

        # 检查是否包含数字
        if not re.search(r'\d', password):
            errors.append('密码必须包含数字')

        # 检查是否包含特殊字符
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('密码必须包含特殊字符')

        if errors:
            raise serializers.ValidationError(errors)

    def get_help_text(self):
        return '密码必须至少8位，包含字母、数字和特殊字符'


# 创建自定义密码验证器实例
password_strength_validator = PasswordStrengthValidator()


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_strength_validator.validate],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'real_name', 'phone', 'email']

    def validate(self, attrs):
        """
        验证两次密码是否一致
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': '两次密码不一致'
            })
        return attrs

    def validate_username(self, value):
        """
        验证用户名唯一性
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已被注册')
        return value

    def validate_phone(self, value):
        """
        验证手机号格式和唯一性
        """
        import re
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已被注册')
        return value

    def validate_email(self, value):
        """
        验证邮箱唯一性
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value

    def create(self, validated_data):
        """
        创建用户
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            **validated_data,
            role='employee',  # 默认角色为普通员工
            is_active=True    # 默认激活
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器（用于响应）
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'phone', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录序列化器，添加 real_name 和 role 到 token 响应中
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        # 添加自定义字段
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['real_name'] = self.user.real_name
        data['role'] = self.user.role

        return data


class AdminResetPasswordSerializer(serializers.ModelSerializer):
    """
    管理员重置用户密码序列化器
    """
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_strength_validator.validate],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['new_password']


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表序列化器（轻量版，用于用户管理列表）
    """
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'phone', 'email', 'role', 'is_active', 'status', 'date_joined']

    def get_status(self, obj):
        """返回用户状态文本"""
        return '正常' if obj.is_active else '禁用'


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """
    用户角色更新序列化器
    """
    class Meta:
        model = User
        fields = ['role']

    def validate_role(self, value):
        """验证角色值"""
        valid_roles = ['employee', 'hr', 'admin']
        if value not in valid_roles:
            raise serializers.ValidationError(f'无效的角色，可选值: {valid_roles}')
        return value


class UserStatusUpdateSerializer(serializers.ModelSerializer):
    """
    用户状态更新序列化器
    """
    class Meta:
        model = User
        fields = ['is_active']


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    用户自主修改密码序列化器
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_strength_validator.validate],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password2']

    def validate(self, attrs):
        """验证两次新密码是否一致"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                'new_password2': '两次新密码不一致'
            })
        return attrs

    def validate_old_password(self, value):
        """验证旧密码"""
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError('旧密码不正确')
        return value

    def validate_new_password(self, value):
        """验证新密码不能与旧密码相同"""
        user = self.context.get('request').user
        if user.check_password(value):
            raise serializers.ValidationError('新密码不能与旧密码相同')
        return value


class UserEditRequestCreateSerializer(serializers.ModelSerializer):
    """
    创建信息修改申请序列化器
    """
    class Meta:
        model = get_user_edit_request_model()
        fields = ['edit_type', 'new_value', 'reason']

    def validate_new_value(self, value):
        """验证新值的唯一性（手机号/邮箱）"""
        edit_type = self.initial_data.get('edit_type')
        if edit_type == 'phone':
            import re
            if not re.match(r'^1[3-9]\d{9}$', value):
                raise serializers.ValidationError('手机号格式不正确')
            if User.objects.filter(phone=value).exists():
                raise serializers.ValidationError('该手机号已被注册')
        elif edit_type == 'email':
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError('该邮箱已被注册')
        return value


class UserEditRequestSerializer(serializers.ModelSerializer):
    """
    信息修改申请详情序列化器
    """
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    edit_type_display = serializers.CharField(source='get_edit_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.real_name', read_only=True, allow_null=True)

    class Meta:
        model = get_user_edit_request_model()
        fields = [
            'id', 'user', 'user_name', 'edit_type', 'edit_type_display',
            'old_value', 'new_value', 'reason', 'status', 'status_display',
            'reviewer', 'reviewer_name', 'reviewer_comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'old_value', 'status', 'reviewer', 'created_at', 'updated_at']


class UserEditRequestListSerializer(serializers.ModelSerializer):
    """
    信息修改申请列表序列化器（轻量版）
    """
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    edit_type_display = serializers.CharField(source='get_edit_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = get_user_edit_request_model()
        fields = [
            'id', 'user', 'user_name', 'edit_type', 'edit_type_display',
            'old_value', 'new_value', 'reason', 'status', 'status_display', 'created_at'
        ]


class UserEditRequestActionSerializer(serializers.ModelSerializer):
    """
    审批操作序列化器
    """
    class Meta:
        model = get_user_edit_request_model()
        fields = ['reviewer_comment']


# 延迟导入 RolePermission 模型
def get_role_permission_model():
    """延迟导入 RolePermission，避免循环导入"""
    from .models import RolePermission
    return RolePermission


class RolePermissionSerializer(serializers.ModelSerializer):
    """
    角色权限配置序列化器
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = get_role_permission_model()
        fields = [
            'id', 'role', 'role_display',
            'menu_permissions', 'button_permissions',
            'data_permission', 'attendance_permission', 'salary_permission',
            'can_access_datacenter', 'can_access_performance',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'role', 'created_at', 'updated_at']


class RolePermissionUpdateSerializer(serializers.ModelSerializer):
    """
    角色权限更新序列化器
    """
    class Meta:
        model = get_role_permission_model()
        fields = [
            'menu_permissions', 'button_permissions',
            'data_permission', 'attendance_permission', 'salary_permission',
            'can_access_datacenter', 'can_access_performance'
        ]


# 延迟导入 SystemConfig 模型
def get_system_config_model():
    """延迟导入 SystemConfig，避免循环导入"""
    from .models import SystemConfig
    return SystemConfig


class SystemConfigSerializer(serializers.ModelSerializer):
    """
    系统配置序列化器
    """
    class Meta:
        model = get_system_config_model()
        fields = [
            'id',
            # 注册配置
            'require_registration_approval',
            # 密码策略配置
            'password_min_length',
            'password_require_uppercase',
            'password_require_lowercase',
            'password_require_number',
            'password_require_special',
            # 登录安全配置
            'max_login_attempts',
            'login_lockout_duration',
            'session_timeout',
            # 其他配置
            'allow_multiple_sessions',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemConfigUpdateSerializer(serializers.ModelSerializer):
    """
    系统配置更新序列化器
    """
    class Meta:
        model = get_system_config_model()
        fields = [
            # 注册配置
            'require_registration_approval',
            # 密码策略配置
            'password_min_length',
            'password_require_uppercase',
            'password_require_lowercase',
            'password_require_number',
            'password_require_special',
            # 登录安全配置
            'max_login_attempts',
            'login_lockout_duration',
            'session_timeout',
            # 其他配置
            'allow_multiple_sessions'
        ]

    def validate_password_min_length(self, value):
        """验证密码最小长度"""
        if value < 6:
            raise serializers.ValidationError('密码最小长度不能小于6位')
        if value > 32:
            raise serializers.ValidationError('密码最小长度不能大于32位')
        return value

    def validate_max_login_attempts(self, value):
        """验证最大登录尝试次数"""
        if value < 3:
            raise serializers.ValidationError('最大登录尝试次数不能小于3次')
        if value > 20:
            raise serializers.ValidationError('最大登录尝试次数不能大于20次')
        return value

    def validate_login_lockout_duration(self, value):
        """验证锁定时间"""
        if value < 5:
            raise serializers.ValidationError('锁定时间不能小于5分钟')
        if value > 1440:  # 24小时
            raise serializers.ValidationError('锁定时间不能大于1440分钟（24小时）')
        return value

    def validate_session_timeout(self, value):
        """验证会话超时时间"""
        if value < 10:
            raise serializers.ValidationError('会话超时时间不能小于10分钟')
        if value > 1440:  # 24小时
            raise serializers.ValidationError('会话超时时间不能大于1440分钟（24小时）')
        return value
