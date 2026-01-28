from django.db import models
from employees.models import EmployeeProfile


class LeaveRequest(models.Model):
    """
    请假申请模型
    """
    class LeaveType(models.TextChoices):
        """请假类型"""
        SICK = 'SICK', '病假'
        PERSONAL = 'PERSONAL', '事假'
        COMPENSATORY = 'COMPENSATORY', '调休'

    class Status(models.TextChoices):
        """审批状态"""
        PENDING = 'PENDING', '待审批'
        APPROVED = 'APPROVED', '已通过'
        REJECTED = 'REJECTED', '已驳回'

    # 基本信息字段
    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='leave_requests',
        verbose_name='员工'
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LeaveType.choices,
        verbose_name='请假类型'
    )
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    reason = models.TextField(verbose_name='请假原因')

    # 审批信息字段
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='审批状态'
    )
    approver = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves',
        verbose_name='审批人'
    )
    approval_remark = models.TextField(
        blank=True,
        verbose_name='审批意见'
    )

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'leaves_leave_request'
        verbose_name = '请假申请'
        verbose_name_plural = '请假申请'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['start_time']),
        ]

    def __str__(self):
        return f'{self.employee.name} - {self.get_leave_type_display()}({self.start_time.date()})'

    @property
    def leave_duration_days(self):
        """
        计算请假天数（包含开始和结束日期）
        """
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return max(1, delta.days + 1)
        return 0
