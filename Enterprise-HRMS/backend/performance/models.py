from django.db import models
from HRMS.settings import ROLE_CHOICES


class PerformanceReview(models.Model):
    """
    绩效评估表
    """
    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='performance_reviews',
        limit_choices_to={'is_active': True}
    )
    review_period = models.CharField(
        max_length=20,
        help_text='评估周期 (如: 2025-Q1, 2025-01)'
    )
    reviewer = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviewed_performances',
        limit_choices_to={'role__in': ['hr', 'admin']}
    )
    score = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        help_text='评分 (1-5分)'
    )
    strengths = models.TextField(
        blank=True,
        default='',
        help_text='优点'
    )
    improvements = models.TextField(
        blank=True,
        default='',
        help_text='改进建议'
    )
    goals = models.TextField(
        blank=True,
        default='',
        help_text='设定目标'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', '草稿'),
            ('published', '已发布'),
        ],
        default='draft',
        help_text='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '绩效评估'
        verbose_name_plural = '绩效评估'
        # 同一员工同一评估周期只能有一条评估记录
        unique_together = ['employee', 'review_period']

    def __str__(self):
        return f'{self.employee.real_name} - {self.review_period}'
