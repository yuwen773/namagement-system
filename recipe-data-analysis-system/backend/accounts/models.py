"""
用户模型模块

包含用户认证和个人资料相关的数据模型。
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from utils.constants import UserRole


class UserManager(BaseUserManager):
    """用户管理器"""

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        创建普通用户

        Args:
            username: 用户名
            email: 邮箱（可选）
            password: 密码
            **extra_fields: 额外字段

        Returns:
            User: 创建的用户实例
        """
        if not username:
            raise ValueError('用户名必须提供')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        创建超级用户

        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            **extra_fields: 额外字段

        Returns:
            User: 创建的超级用户实例
        """
        extra_fields.setdefault('role', UserRole.ADMIN)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    用户模型

    存储用户认证信息，包括用户名、密码、邮箱等核心字段。
    使用自定义用户模型以支持更灵活的扩展。

    Attributes:
        username: 用户名（唯一）
        email: 邮箱（可选）
        password: 加密后的密码
        role: 用户角色（user/admin）
        is_active: 账户是否激活
        is_staff: 是否为管理员（可访问 Django admin）
        last_login: 最后登录时间
        created_at: 创建时间
        updated_at: 更新时间
    """

    username = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='用户名',
        help_text='用户登录时使用的唯一标识'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='邮箱',
        help_text='用户邮箱地址，可用于登录'
    )
    password = models.CharField(
        max_length=128,
        verbose_name='密码',
        help_text='加密后的用户密码'
    )

    # 用户角色：user（普通用户）或 admin（管理员）
    role = models.CharField(
        max_length=10,
        choices=UserRole.CHOICES,
        default=UserRole.USER,
        db_index=True,
        verbose_name='角色',
        help_text='用户角色类型'
    )

    # 账户状态
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='是否激活',
        help_text='账户是否处于激活状态'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='是否管理员',
        help_text='是否可以访问 Django 管理后台'
    )

    # 时间字段
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='最后登录时间',
        help_text='用户最后一次成功登录的时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='账户创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='账户信息最后更新时间'
    )

    # Django 认证相关配置
    USERNAME_FIELD = 'username'  # 用作用户名的唯一字段
    REQUIRED_FIELDS = ['email']  # 创建超级用户时需要的额外字段

    objects = UserManager()

    def set_password(self, raw_password):
        """
        重写 set_password 方法，直接存储明文密码
        """
        self.password = raw_password

    def check_password(self, raw_password):
        """
        重写 check_password 方法，直接比较明文密码
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        
        return self.password == raw_password

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def get_full_name(self):
        """获取用户全名（返回用户名）"""
        return self.username

    def get_short_name(self):
        """获取用户短名（返回用户名）"""
        return self.username


class UserProfile(models.Model):
    """
    用户资料模型

    存储用户的扩展信息，与 User 模型是一对一关系。
    将核心认证信息与个人资料分离，提高数据管理灵活性。

    Attributes:
        user: 关联的用户（一对一）
        nickname: 昵称
        phone: 手机号
        bio: 个人简介
        avatar_url: 头像 URL
        created_at: 创建时间
        updated_at: 更新时间
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='用户',
        help_text='关联的用户账户'
    )
    nickname = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='昵称',
        help_text='用户显示的昵称'
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='手机号',
        help_text='用户手机号码'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='个人简介',
        help_text='用户自我介绍'
    )
    avatar_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='头像 URL',
        help_text='用户头像图片地址'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        db_table = 'user_profiles'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} 的资料"
