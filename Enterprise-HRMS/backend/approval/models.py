from django.db import models
from django.conf import settings


class ApprovalRequest(models.Model):
    """
    审批请求模型
    支持请假申请和加班申请两种类型
    """

    # 申请类型
    TYPE_CHOICES = [
        ('leave', '请假'),
        ('overtime', '加班'),
    ]

    # 请假类型
    LEAVE_TYPE_CHOICES = [
        ('sick', '病假'),
        ('personal', '事假'),
        ('annual', '年假'),
    ]

    # 审批状态
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
    ]

    # 申请人
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='approval_requests',
        verbose_name='申请人'
    )

    # 申请类型
    request_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='申请类型'
    )

    # 请假类型（仅请假时使用）
    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='请假类型'
    )

    # 开始时间
    start_time = models.DateTimeField(verbose_name='开始时间')

    # 结束时间
    end_time = models.DateTimeField(verbose_name='结束时间')

    # 申请原因
    reason = models.TextField(verbose_name='申请原因')

    # 加班时长（小时）- 仅加班时使用
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name='加班时长'
    )

    # 审批状态
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='审批状态'
    )

    # 审批人
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_requests',
        verbose_name='审批人'
    )

    # 审批原因
    approver_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='审批意见'
    )

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '审批请求'
        verbose_name_plural = '审批请求'

    def __str__(self):
        return f"{self.user.real_name} - {self.get_request_type_display()} - {self.get_status_display()}"
