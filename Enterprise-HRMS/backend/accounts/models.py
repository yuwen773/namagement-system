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
