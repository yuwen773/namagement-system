from django.db import models
from django.core.exceptions import ValidationError
from employees.models import EmployeeProfile


class SalaryRecord(models.Model):
    """薪资记录模型"""

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', '草稿'
        PUBLISHED = 'PUBLISHED', '已发布'
        APPEALED = 'APPEALED', '申诉中'
        ADJUSTED = 'ADJUSTED', '已调整'

    # 基本信息字段
    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='salary_records',
        verbose_name='员工'
    )
    year_month = models.CharField(max_length=7, verbose_name='年月', help_text='格式: YYYY-MM')

    # 薪资组成字段
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='基本工资')
    position_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='岗位津贴')
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='加班费')
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='扣款')
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='实发工资')

    # 统计字段
    work_days = models.IntegerField(default=0, verbose_name='出勤天数')
    late_count = models.IntegerField(default=0, verbose_name='迟到次数')
    missing_count = models.IntegerField(default=0, verbose_name='缺卡次数')
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='加班时长(小时)')

    # 状态和备注
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'salary_records'
        verbose_name = '薪资记录'
        verbose_name_plural = '薪资记录'
        # 确保同一员工在同一月份只有一条薪资记录
        unique_together = [['employee', 'year_month']]
        ordering = ['-year_month', '-created_at']
        indexes = [
            models.Index(fields=['employee', 'year_month']),
            models.Index(fields=['year_month']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.year_month} 薪资"

    def clean(self):
        """验证数据"""
        if self.overtime_pay < 0:
            raise ValidationError({'overtime_pay': '加班费不能为负数'})
        if self.deductions < 0:
            raise ValidationError({'deductions': '扣款不能为负数'})

    def save(self, *args, **kwargs):
        self.full_clean()
        # 自动计算实发工资
        self.total_salary = self.base_salary + self.position_allowance + self.overtime_pay - self.deductions
        super().save(*args, **kwargs)


class Appeal(models.Model):
    """异常申诉模型"""

    class AppealType(models.TextChoices):
        ATTENDANCE = 'ATTENDANCE', '考勤申诉'
        SALARY = 'SALARY', '薪资申诉'

    class Status(models.TextChoices):
        PENDING = 'PENDING', '待审批'
        APPROVED = 'APPROVED', '已通过'
        REJECTED = 'REJECTED', '已驳回'

    # 基本信息字段
    appeal_type = models.CharField(max_length=20, choices=AppealType.choices, verbose_name='申诉类型')
    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='appeals',
        verbose_name='申诉员工'
    )
    target_id = models.IntegerField(verbose_name='目标记录ID', help_text='考勤记录ID或薪资记录ID')

    # 申诉信息
    reason = models.TextField(verbose_name='申诉原因')

    # 审批信息
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='审批状态')
    approver = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_appeals',
        verbose_name='审批人'
    )
    approval_remark = models.TextField(blank=True, null=True, verbose_name='审批意见')

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'appeals'
        verbose_name = '异常申诉'
        verbose_name_plural = '异常申诉'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee', 'status']),
            models.Index(fields=['appeal_type', 'status']),
            models.Index(fields=['target_id']),
        ]

    def __str__(self):
        return f"{self.get_appeal_type_display()} - {self.employee.name} - {self.get_status_display()}"
