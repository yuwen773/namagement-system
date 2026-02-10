from django.db import models
from django.utils import timezone


class MovieType(models.Model):
    """影片类型模型"""

    name = models.CharField('类型名称', max_length=50, unique=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        db_table = 'movie_types'
        verbose_name = '影片类型'
        verbose_name_plural = '影片类型管理'

    def __str__(self):
        return self.name


class Movie(models.Model):
    """影片模型"""

    STATUS_CHOICES = (
        ('RELEASED', '已上映'),
        ('COMING', '即将上映'),
        ('OFF', '已下映'),
    )

    title = models.CharField('影片名称', max_length=200)
    director = models.CharField('导演', max_length=100, blank=True, null=True)
    actors = models.CharField('主演', max_length=500, blank=True, null=True)
    release_date = models.DateField('上映时间', blank=True, null=True)
    duration = models.IntegerField('片长（分钟）', blank=True, null=True)
    type = models.ForeignKey(
        MovieType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movies',
        verbose_name='类型'
    )
    poster_url = models.CharField('海报URL', max_length=500, blank=True, null=True)
    description = models.TextField('简介', blank=True, null=True)
    box_office_total = models.DecimalField(
        '累计票房（万元）',
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='RELEASED'
    )
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'movies'
        verbose_name = '影片'
        verbose_name_plural = '影片管理'

    def __str__(self):
        return self.title
