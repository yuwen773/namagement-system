from django.conf import settings
from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_published = models.BooleanField(default=False, verbose_name='发布状态')
    is_top = models.BooleanField(default=False, verbose_name='置顶')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements',
        verbose_name='发布人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'announcements'
        ordering = ['-is_top', '-created_at']
        verbose_name = '通知公告'
        verbose_name_plural = '通知公告'

    def __str__(self):
        return self.title
