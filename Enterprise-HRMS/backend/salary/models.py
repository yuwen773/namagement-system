from django.db import models
from django.conf import settings


class SalaryRecord(models.Model):
    """薪资记录模型"""

    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='salary_records',
        verbose_name='员工'
    )
    month = models.CharField(
        max_length=7,
        verbose_name='薪资月份',
        help_text='格式: YYYY-MM'
    )
    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='基本工资'
    )
    overtime_hours = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        verbose_name='加班小时数'
    )
    overtime_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='加班费'
    )
    late_count = models.IntegerField(
        default=0,
        verbose_name='迟到次数'
    )
    early_count = models.IntegerField(
        default=0,
        verbose_name='早退次数'
    )
    attendance_deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='考勤扣款'
    )
    final_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='实发工资'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'salary_salaryrecord'
        unique_together = ['user', 'month']
        ordering = ['-month', '-created_at']
        verbose_name = '薪资记录'
        verbose_name_plural = '薪资记录'

    def __str__(self):
        return f'{self.user.real_name} - {self.month}'


class SalaryException(models.Model):
    """
    薪资异常处理记录
    用于记录和处理薪资计算中的异常情况，如员工申诉、数据错误等
    """
    EXCEPTION_TYPE_CHOICES = [
        ('salary_error', '薪资计算错误'),
        ('attendance_error', '考勤数据错误'),
        ('overtime_missing', '加班记录缺失'),
        ('deduction_error', '扣款异常'),
        ('employee_appeal', '员工申诉'),
        ('other', '其他'),
    ]

    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('closed', '已关闭'),
    ]

    salary_record = models.ForeignKey(
        SalaryRecord,
        on_delete=models.CASCADE,
        related_name='exceptions',
        verbose_name='关联薪资记录'
    )
    exception_type = models.CharField(
        max_length=20,
        choices=EXCEPTION_TYPE_CHOICES,
        verbose_name='异常类型'
    )
    description = models.TextField(
        verbose_name='异常描述'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='处理状态'
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reported_exceptions',
        verbose_name='上报人'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_exceptions',
        verbose_name='处理人'
    )
    resolution = models.TextField(
        blank=True,
        default='',
        verbose_name='处理方案'
    )
    adjustment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='调整金额'
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='解决时间'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'salary_exception'
        ordering = ['-created_at']
        verbose_name = '薪资异常'
        verbose_name_plural = '薪资异常处理'

    def __str__(self):
        return f'异常 #{self.id} - {self.get_exception_type_display()}'
