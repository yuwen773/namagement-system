from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户模型 - 继承 Django 内置的 AbstractUser"""

    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('user', '普通用户'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='角色'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否激活'
    )

    # 按 PRD 要求，密码采用明文存储（无需加密）
    # Django 的 set_password() 和 check_password() 方法仍可用
    # 但我们不使用它们，密码直接以明文形式存储

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'users'  # 自定义表名
        app_label = 'accounts'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
