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
        获取默认权限配置（严格按照 docs/requirements.md 配置）
        """
        defaults = {
            # 普通员工 (6个页面)
            'employee': {
                # 首页、个人信息、部门岗位、考勤、申请中心、薪资绩效
                'menu_permissions': [
                    'employeeDashboard',  # 首页
                    'profile',            # 个人信息编辑
                    'departments',        # 部门信息（只读）
                    'posts',              # 岗位信息（只读）
                    'attendance',         # 考勤中心
                    'approval',           # 申请中心
                    'salary',             # 薪资明细查询
                    'myPerformance',      # 绩效评分查看
                    'notices'             # 公告列表
                ],
                'button_permissions': ['checkIn', 'checkOut', 'applyLeave', 'applyOvertime', 'viewSalary'],
                'data_permission': 'self',
                'attendance_permission': 'self',
                'salary_permission': 'self',
                'can_access_datacenter': False,
                'can_access_performance': True,
            },
            # 人事专员 (7个页面)
            'hr': {
                # 人事工作台、员工档案、组织岗位、入离职、考勤管理、绩效管理、薪资管理
                'menu_permissions': [
                    'dashboard',          # 人事工作台
                    'employees',          # 员工档案管理
                    'departments',        # 部门信息管理
                    'posts',              # 岗位信息管理
                    'onboarding',         # 入职管理
                    'resignation',        # 离职管理
                    'attendance',         # 考勤管理
                    'approval',           # 审批中心
                    'salary',             # 薪资管理
                    'salaryException',    # 异常处理
                    'performanceReview',  # 绩效评估
                    'performanceTemplate',# 绩效模板
                    'notices'             # 公告查看
                ],
                'button_permissions': [
                    'createEmployee',     # 创建员工
                    'editEmployee',       # 编辑员工
                    'deleteEmployee',     # 删除员工
                    'approveLeave',       # 审批请假
                    'approveOvertime',    # 审批加班
                    'calculateSalary',    # 计算薪资
                    'publishSalary',      # 发布薪资
                    'createNotice'        # 创建公告（HR可发布公告）
                ],
                'data_permission': 'all',
                'attendance_permission': 'all',
                'salary_permission': 'all',
                'can_access_datacenter': True,
                'can_access_performance': True,
            },
            # 系统管理员 (5个页面)
            'admin': {
                # 系统管理首页、用户账号、角色权限、数据中心、系统公告
                'menu_permissions': [
                    'dashboard',          # 系统管理首页
                    'users',              # 用户账号管理
                    'permissionConfig',   # 角色与权限配置
                    'securityConfig',     # 安全配置
                    'dataCenter',         # 数据中心
                    'noticeManagement',   # 系统公告管理
                    'salaryException',    # 薪资异常处理（管理员也可访问）
                    'profile'             # 个人信息
                ],
                'button_permissions': [
                    'manageUsers',        # 管理用户
                    'resetPassword',      # 重置密码
                    'configurePermissions',# 配置权限
                    'viewSalary'          # 查看薪资
                ],
                'data_permission': 'all',
                'attendance_permission': 'all',
                'salary_permission': 'all',
                'can_access_datacenter': True,
                'can_access_performance': True,
            },
        }
        return defaults.get(role, defaults['employee'])


class SystemConfig(models.Model):
    """
    系统配置模型
    用于存储登录/注册规则、密码策略等系统级配置
    """
    # 注册配置
    require_registration_approval = models.BooleanField(
        default=False,
        verbose_name='注册需审批',
        help_text='新用户注册后是否需要管理员审批才能登录'
    )

    # 密码策略配置
    password_min_length = models.PositiveIntegerField(
        default=6,
        verbose_name='密码最小长度',
        help_text='密码最小长度要求'
    )
    password_require_uppercase = models.BooleanField(
        default=False,
        verbose_name='需要大写字母',
        help_text='密码是否需要包含大写字母'
    )
    password_require_lowercase = models.BooleanField(
        default=True,
        verbose_name='需要小写字母',
        help_text='密码是否需要包含小写字母'
    )
    password_require_number = models.BooleanField(
        default=True,
        verbose_name='需要数字',
        help_text='密码是否需要包含数字'
    )
    password_require_special = models.BooleanField(
        default=False,
        verbose_name='需要特殊字符',
        help_text='密码是否需要包含特殊字符'
    )

    # 登录安全配置
    max_login_attempts = models.PositiveIntegerField(
        default=5,
        verbose_name='最大登录尝试次数',
        help_text='连续登录失败后锁定账户的次数'
    )
    login_lockout_duration = models.PositiveIntegerField(
        default=30,
        verbose_name='锁定时间(分钟)',
        help_text='账户锁定时间（分钟）'
    )
    session_timeout = models.PositiveIntegerField(
        default=120,
        verbose_name='会话超时(分钟)',
        help_text='用户无操作后会话超时时间（分钟）'
    )

    # 其他配置
    allow_multiple_sessions = models.BooleanField(
        default=True,
        verbose_name='允许多端登录',
        help_text='是否允许同一账户在多个设备同时登录'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'accounts_systemconfig'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'

    def __str__(self):
        return f"系统配置 (ID: {self.id})"

    @classmethod
    def get_config(cls):
        """
        获取系统配置，如果不存在则创建默认配置
        """
        config, created = cls.objects.get_or_create(id=1, defaults={
            'password_min_length': 6,
            'password_require_uppercase': False,
            'password_require_lowercase': True,
            'password_require_number': True,
            'password_require_special': False,
            'max_login_attempts': 5,
            'login_lockout_duration': 30,
            'session_timeout': 120,
            'allow_multiple_sessions': True,
        })
        return config
