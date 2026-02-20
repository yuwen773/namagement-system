from django.db import models


class Notice(models.Model):
    """公告模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告列表'
        ordering = ['-created_at']
        db_table = 'notices'

    def __str__(self):
        return self.title
