import uuid
from django.db import models
from users.models import User


class Feedback(models.Model):
    """用户反馈模型"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processed', '已处理'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    title = models.CharField(max_length=200, verbose_name='反馈标题')
    content = models.TextField(verbose_name='反馈内容')
    contact = models.CharField(max_length=100, blank=True, verbose_name='联系方式')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'feedback'
        verbose_name = '反馈'
        verbose_name_plural = '反馈'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
