from django.db import models
from employees.models import EmployeeProfile


class Shift(models.Model):
    """
    班次定义模型
    定义食堂的各个班次及其时间段
    """
    name = models.CharField(max_length=20, verbose_name='班次名称', help_text='如：早班/中班/晚班/全天')
    start_time = models.TimeField(verbose_name='上班开始时间')
    end_time = models.TimeField(verbose_name='下班结束时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'shifts'
        verbose_name = '班次定义'
        verbose_name_plural = '班次定义'
        ordering = ['start_time']

    def __str__(self):
        return f'{self.name} ({self.start_time} - {self.end_time})'


class Schedule(models.Model):
    """
    排班计划模型
    为员工在指定日期安排班次
    """
    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='员工'
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='班次'
    )
    work_date = models.DateField(verbose_name='排班日期', db_index=True)
    is_swapped = models.BooleanField(default=False, verbose_name='是否已调班')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'schedules'
        verbose_name = '排班计划'
        verbose_name_plural = '排班计划'
        ordering = ['-work_date', 'shift__start_time']
        # 防止同一员工在同一日期重复排班
        unique_together = [['employee', 'work_date']]

    def __str__(self):
        return f'{self.employee.name} - {self.work_date} - {self.shift.name}'


class ShiftSwapRequest(models.Model):
    """
    调班申请模型
    员工发起调班申请，管理员审批后自动更新排班
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', '待审批'
        APPROVED = 'APPROVED', '已批准'
        REJECTED = 'REJECTED', '已拒绝'

    requester = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='swap_requests',
        verbose_name='发起员工'
    )
    original_schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='swap_requests',
        verbose_name='原定排班'
    )
    target_date = models.DateField(verbose_name='期望调整日期')
    target_shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name='target_swap_requests',
        verbose_name='期望调整班次'
    )
    reason = models.TextField(null=True, blank=True, verbose_name='申请原因')
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
        related_name='approved_swap_requests',
        verbose_name='审批管理员'
    )
    approval_remark = models.TextField(null=True, blank=True, verbose_name='审批意见')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'shift_swap_requests'
        verbose_name = '调班申请'
        verbose_name_plural = '调班申请'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.requester.name} - {self.original_schedule.work_date} 调班申请 - {self.get_status_display()}'
