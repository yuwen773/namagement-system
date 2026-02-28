from django.db import models
from django.conf import settings
import uuid


class Announcement(models.Model):
    """公告模型 - 系统通知公告"""

    class Priority(models.IntegerChoices):
        NORMAL = 1, '普通'
        IMPORTANT = 2, '重要'
        URGENT = 3, '紧急'

    class Status(models.TextChoices):
        DRAFT = 'draft', '草稿'
        PUBLISHED = 'published', '已发布'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='公告ID')
    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.NORMAL,
        verbose_name='优先级'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='状态'
    )
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_announcements',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')

    class Meta:
        db_table = 'announcements'
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ['-is_pinned', '-priority', '-published_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['-is_pinned']),
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def publish(self):
        """发布公告"""
        from django.utils import timezone
        if self.status != self.Status.PUBLISHED:
            self.status = self.Status.PUBLISHED
            self.published_at = timezone.now()
            self.save()

    def unpublish(self):
        """取消发布（转为草稿）"""
        if self.status == self.Status.PUBLISHED:
            self.status = self.Status.DRAFT
            self.save()
