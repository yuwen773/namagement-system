from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """自定义用户管理器"""

    def create_user(self, username, password=None, **extra_fields):
        """创建普通用户"""
        if not username:
            raise ValueError('用户名必须提供')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)


class UserProfile(AbstractBaseUser):
    """用户模型"""

    ROLE_CHOICES = (
        ('ADMIN', '管理员'),
        ('USER', '普通用户'),
    )

    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    real_name = models.CharField(max_length=50, blank=True, verbose_name='真实姓名')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    email = models.EmailField(max_length=100, blank=True, verbose_name='邮箱')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER', verbose_name='角色')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 使用自定义管理器
    objects = UserManager()

    # 指定 username 字段为 USERNAME_FIELD
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'accounts_userprofile'
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return self.username
