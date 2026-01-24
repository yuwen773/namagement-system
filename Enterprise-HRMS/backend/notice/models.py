from django.db import models
from django.conf import settings
from django.utils import timezone


class Notice(models.Model):
    """公告模型"""

    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='发布人',
        related_name='published_notices'
    )
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-is_pinned', '-published_at', '-created_at']
        verbose_name = '公告'
        verbose_name_plural = '公告'

    def __str__(self):
        return self.title

    def publish(self, user):
        """发布公告"""
        self.is_published = True
        self.published_by = user
        self.published_at = timezone.now()
        self.save(update_fields=['is_published', 'published_by', 'published_at', 'updated_at'])

    def unpublish(self):
        """撤回公告"""
        self.is_published = False
        self.save(update_fields=['is_published', 'updated_at'])
