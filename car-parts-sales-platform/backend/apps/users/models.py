from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """自定义用户管理器，支持 phone 作为唯一标识"""

    def create_user(self, phone, password=None, **extra_fields):
        """创建普通用户 - 明文存储密码（开发环境）"""
        if not phone:
            raise ValueError('手机号必须提供')
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.password = password  # 明文存储，不加密
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """
    用户模型 - 扩展 Django 内置的 AbstractUser
    """
    phone = models.CharField('手机号', max_length=11, unique=True, db_index=True)
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    avatar = models.URLField('头像URL', blank=True, null=True, default='')
    points = models.IntegerField('积分', default=0)
    status = models.CharField(
        '状态',
        max_length=20,
        choices=[
            ('active', '正常'),
            ('banned', '禁用'),
        ],
        default='active',
        db_index=True
    )
    created_at = models.DateTimeField('注册时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    # 重写必要字段，移除 username，使用 phone 作为唯一标识
    username = None  # 移除 username 字段
    USERNAME_FIELD = 'phone'  # 使用手机号作为登录标识
    REQUIRED_FIELDS = []  # 创建 superuser 时不需要额外字段

    # 使用自定义管理器
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return f'{self.phone} ({self.nickname or self.first_name or "用户"})'


class UserAddress(models.Model):
    """
    用户收货地址模型
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='所属用户'
    )
    recipient_name = models.CharField('收货人姓名', max_length=50)
    phone = models.CharField('收货人手机号', max_length=11)
    province = models.CharField('省份', max_length=50, blank=True, default='')
    city = models.CharField('城市', max_length=50, blank=True, default='')
    district = models.CharField('区县', max_length=50, blank=True, default='')
    address = models.CharField('详细地址', max_length=255)
    is_default = models.BooleanField('是否默认地址', default=False, db_index=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user_addresses'
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址管理'
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        default_mark = '【默认】' if self.is_default else ''
        return f'{default_mark}{self.province}{self.city}{self.district}{self.address}'

    def save(self, *args, **kwargs):
        """设置默认地址逻辑：只有一个默认地址时，之前的默认地址会被取消"""
        if self.is_default:
            # 取消该用户其他默认地址
            UserAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
