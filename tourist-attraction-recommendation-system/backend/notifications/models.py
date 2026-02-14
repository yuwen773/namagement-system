from django.db import models
from accounts.models import UserProfile


class Notification(models.Model):
    TYPE_CHOICES = [
        ('SYSTEM', '系统通知'),
        ('ANNOUNCEMENT', '公告'),
        ('COMMENT', '评论通知'),
    ]

    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES, default='SYSTEM')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    is_read = models.BooleanField('是否已读', default=False)
    is_deleted = models.BooleanField('是否删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
