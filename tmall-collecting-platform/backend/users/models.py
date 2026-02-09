from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """用户模型 - 扩展Django默认用户"""
    class Role(models.TextChoices):
        ADMIN = 'admin', '管理员'
        USER = 'user', '普通用户'

    class Status(models.TextChoices):
        ACTIVE = 'active', '启用'
        FROZEN = 'frozen', '冻结'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='角色'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name='状态'
    )
    avatar = models.URLField(max_length=500, blank=True, null=True, verbose_name='头像URL')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class SystemConfig(models.Model):
    """系统配置模型 - 存储系统级配置"""

    class ConfigType(models.TextChoices):
        CRAWLER = 'crawler', '爬虫配置'
        SYSTEM = 'system', '系统配置'
        API = 'api', 'API配置'

    key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    value = models.TextField(verbose_name='配置值')
    config_type = models.CharField(
        max_length=20,
        choices=ConfigType.choices,
        default=ConfigType.CRAWLER,
        verbose_name='配置类型'
    )
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name='描述')
    is_encrypted = models.BooleanField(default=False, verbose_name='是否加密')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_configs',
        verbose_name='更新者'
    )

    class Meta:
        db_table = 'system_configs'
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'
        ordering = ['config_type', 'key']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['config_type']),
        ]

    def __str__(self):
        return f"{self.get_config_type_display()}.{self.key}"

    @classmethod
    def get_value(cls, key, default=None):
        """获取配置值"""
        try:
            config = cls.objects.get(key=key)
            return config.value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_value(cls, key, value, config_type='crawler', description='', updated_by=None):
        """设置配置值"""
        config, created = cls.objects.get_or_create(
            key=key,
            defaults={
                'value': value,
                'config_type': config_type,
                'description': description,
                'updated_by': updated_by
            }
        )
        if not created:
            config.value = value
            config.updated_by = updated_by
            config.save()
        return config
