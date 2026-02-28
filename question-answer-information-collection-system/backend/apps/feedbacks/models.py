from django.db import models


class Feedback(models.Model):
    """用户反馈建议模型"""
    FEEDBACK_TYPE_CHOICES = [
        ('feature', '功能建议'),
        ('bug', 'Bug反馈'),
        ('other', '其他'),
    ]

    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已完成'),
        ('ignored', '已忽略'),
    ]

    # 基础字段
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='详细描述')
    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPE_CHOICES,
        default='other',
        verbose_name='反馈类型'
    )

    # 状态字段
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='处理状态'
    )
    admin_reply = models.TextField(blank=True, null=True, verbose_name='管理员回复')
    replied_at = models.DateTimeField(blank=True, null=True, verbose_name='回复时间')
    replied_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replied_feedbacks',
        verbose_name='回复人'
    )

    # 关联用户
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='提交用户'
    )

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '反馈建议'
        verbose_name_plural = '反馈建议列表'
        ordering = ['-created_at']
        db_table = 'feedbacks'

    def __str__(self):
        return f"{self.user.username} - {self.title}"
