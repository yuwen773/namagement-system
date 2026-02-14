from django.db import models
from django.utils import timezone


class Region(models.Model):
    """地域模型（省份/城市）"""

    LEVEL_CHOICES = (
        ('PROVINCE', '省份'),
        ('CITY', '城市'),
    )

    name = models.CharField('地域名称', max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父级地域'
    )
    level = models.CharField(
        '层级',
        max_length=20,
        choices=LEVEL_CHOICES,
        default='PROVINCE'
    )
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        db_table = 'regions'
        verbose_name = '地域'
        verbose_name_plural = '地域管理'

    def __str__(self):
        return self.name


class Cinema(models.Model):
    """影院模型"""

    name = models.CharField('影院名称', max_length=200)
    address = models.CharField('地址', max_length=500, blank=True, null=True)
    phone = models.CharField('联系电话', max_length=50, blank=True, null=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cinemas',
        verbose_name='所属区域'
    )
    screen_count = models.IntegerField('屏幕数量', default=1)
    seats_count = models.IntegerField('座位数量', default=100)
    is_active = models.BooleanField('是否营业', default=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'cinemas'
        verbose_name = '影院'
        verbose_name_plural = '影院管理'

    def __str__(self):
        return self.name
