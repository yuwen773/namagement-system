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
