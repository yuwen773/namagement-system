from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


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

    def create_superuser(self, username, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    """用户模型"""

    ROLE_CHOICES = (
        ('ADMIN', '管理员'),
        ('USER', '普通用户'),
    )

    username = models.CharField('用户名', max_length=50, unique=True)
    real_name = models.CharField('真实姓名', max_length=50, blank=True, null=True)
    email = models.EmailField('邮箱', max_length=100, blank=True, null=True)
    phone = models.CharField('联系电话', max_length=20, blank=True, null=True)
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='USER')
    is_active = models.BooleanField('是否激活', default=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'ADMIN'
