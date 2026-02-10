from django.db import models


class Attraction(models.Model):
    """景点模型"""
    CATEGORY_CHOICES = [
        ('自然风光', '自然风光'),
        ('人文古迹', '人文古迹'),
        ('主题乐园', '主题乐园'),
        ('其他', '其他'),
    ]

    name = models.CharField('景点名称', max_length=100)
    description = models.TextField('景点简介', default='', blank=True)
    address = models.CharField('地址', max_length=200, default='')
    category = models.CharField('类别', max_length=20, choices=CATEGORY_CHOICES, default='其他')
    region = models.CharField('地区', max_length=50, default='')
    opening_hours = models.CharField('开放时间', max_length=100, default='')
    cover_image = models.ImageField('封面图', upload_to='attractions/', blank=True, null=True)
    images = models.JSONField('轮播图', default=list, blank=True)
    view_count = models.IntegerField('浏览量', default=0)
    is_deleted = models.BooleanField('是否删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'attractions'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
