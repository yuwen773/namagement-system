from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    扩展用户模型，添加 phone 和 role 字段
    """
    ROLE_CHOICES = [
        ('employee', '普通员工'),
        ('hr', '人事专员'),
        ('admin', '管理员'),
    ]

    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name='角色'
    )
    real_name = models.CharField(max_length=50, verbose_name='真实姓名')
    email = models.EmailField(unique=True, verbose_name='邮箱')

    # 设置手机号和邮箱为必填
    REQUIRED_FIELDS = ['phone', 'email', 'real_name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.real_name or self.username


class UserEditRequest(models.Model):
    """
    用户信息修改申请表
    用于员工提交手机号、邮箱等信息的修改申请，HR/Admin 审批通过后自动更新
    """
    EDIT_TYPE_CHOICES = [
        ('phone', '手机号'),
        ('email', '邮箱'),
        ('emergency_contact', '紧急联系人'),
    ]

    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='edit_requests',
        verbose_name='申请人'
    )
    edit_type = models.CharField(
        max_length=20,
        choices=EDIT_TYPE_CHOICES,
        verbose_name='修改类型'
    )
    old_value = models.CharField(max_length=255, blank=True, verbose_name='原值')
    new_value = models.CharField(max_length=255, verbose_name='新值')
    reason = models.TextField(blank=True, verbose_name='修改原因')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='状态'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_requests',
        verbose_name='审批人'
    )
    reviewer_comment = models.TextField(blank=True, verbose_name='审批意见')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='审批时间')

    class Meta:
        db_table = 'accounts_usereditrequest'
        verbose_name = '信息修改申请'
        verbose_name_plural = '信息修改申请'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.real_name} - {self.get_edit_type_display()} - {self.get_status_display()}"


class RolePermission(models.Model):
    """
    角色权限配置模型
    用于配置各角色的菜单权限、按钮权限和数据权限
    """
    ROLE_CHOICES = [
        ('employee', '普通员工'),
        ('hr', '人事专员'),
        ('admin', '管理员'),
    ]

    DATA_PERMISSION_CHOICES = [
        ('all', '全部数据'),
        ('department', '本部门数据'),
        ('self', '仅本人'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name='角色'
    )

    # 菜单权限配置 - JSON字段存储可访问的菜单路由列表
    menu_permissions = models.JSONField(
        default=list,
        verbose_name='菜单权限',
        help_text='可访问的菜单路由列表'
    )

    # 按钮权限配置 - JSON字段存储可显示的按钮列表
    button_permissions = models.JSONField(
        default=list,
        verbose_name='按钮权限',
        help_text='可显示的操作按钮列表'
    )

    # 数据权限配置
    data_permission = models.CharField(
        max_length=20,
        choices=DATA_PERMISSION_CHOICES,
        default='self',
        verbose_name='数据权限',
        help_text='可访问的数据范围'
    )

    # 考勤数据权限
    attendance_permission = models.CharField(
        max_length=20,
        choices=DATA_PERMISSION_CHOICES,
        default='self',
        verbose_name='考勤数据权限'
    )

    # 薪资数据权限
    salary_permission = models.CharField(
        max_length=20,
        choices=DATA_PERMISSION_CHOICES,
        default='self',
        verbose_name='薪资数据权限'
    )

    # 是否可访问数据中心
    can_access_datacenter = models.BooleanField(
        default=False,
        verbose_name='可访问数据中心'
    )

    # 是否可访问绩效管理
    can_access_performance = models.BooleanField(
        default=False,
        verbose_name='可访问绩效管理'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'accounts_rolepermission'
        verbose_name = '角色权限配置'
        verbose_name_plural = '角色权限配置'

    def __str__(self):
        return f"{self.get_role_display()} 权限配置"

    @classmethod
    def get_default_permissions(cls, role):
        """
        获取默认权限配置
        """
        defaults = {
            'employee': {
                'menu_permissions': ['dashboard', 'attendance', 'salary', 'approval', 'notices', 'myPerformance', 'profile'],
                'button_permissions': ['checkIn', 'checkOut', 'applyLeave', 'applyOvertime', 'viewSalary'],
                'data_permission': 'self',
                'attendance_permission': 'self',
                'salary_permission': 'self',
                'can_access_datacenter': False,
                'can_access_performance': True,
            },
            'hr': {
                'menu_permissions': ['dashboard', 'employees', 'departments', 'posts', 'attendance', 'attendanceStatistics', 'salary', 'approval', 'onboarding', 'notices', 'noticeManagement', 'performanceReview', 'dataCenter', 'profile'],
                'button_permissions': ['createEmployee', 'editEmployee', 'deleteEmployee', 'approveLeave', 'approveOvertime', 'calculateSalary', 'publishSalary', 'createNotice'],
                'data_permission': 'department',
                'attendance_permission': 'all',
                'salary_permission': 'all',
                'can_access_datacenter': True,
                'can_access_performance': True,
            },
            'admin': {
                'menu_permissions': ['dashboard', 'employees', 'departments', 'posts', 'attendance', 'attendanceStatistics', 'salary', 'approval', 'onboarding', 'users', 'notices', 'noticeManagement', 'performanceReview', 'dataCenter', 'profile', 'permissionConfig'],
                'button_permissions': ['createEmployee', 'editEmployee', 'deleteEmployee', 'approveLeave', 'approveOvertime', 'calculateSalary', 'publishSalary', 'createNotice', 'manageUsers', 'resetPassword', 'configurePermissions'],
                'data_permission': 'all',
                'attendance_permission': 'all',
                'salary_permission': 'all',
                'can_access_datacenter': True,
                'can_access_performance': True,
            },
        }
        return defaults.get(role, defaults['employee'])
