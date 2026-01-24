from django.db import models
from accounts.models import User
from organization.models import Department, Post


class EmployeeProfile(models.Model):
    """
    员工档案模型：关联用户、部门和岗位
    工号格式：EMP{年月}{部门代码}{3位流水}，如 EMP202401TECH001
    """

    STATUS_CHOICES = [
        ('pending', '待入职'),
        ('active', '在职'),
        ('resigned', '已离职'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='关联用户'
    )
    employee_no = models.CharField("工号", max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='所属部门'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.PROTECT,
        related_name='employees',
        verbose_name='岗位'
    )
    hire_date = models.DateField("入职日期")
    salary_base = models.DecimalField(
        "基本工资",
        max_digits=10,
        decimal_places=2,
        help_text="月度基本工资"
    )
    status = models.CharField(
        "状态",
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    resigned_date = models.DateField("离职日期", null=True, blank=True)
    resigned_reason = models.TextField("离职原因", blank=True, default="")
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "员工档案"
        verbose_name_plural = "员工档案"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.real_name} ({self.employee_no})"

    def get_department_code(self):
        """获取部门代码用于生成工号"""
        return self.department.code.upper() if self.department.code else 'UNK'

    def get_full_path(self):
        """获取部门完整路径"""
        return self.department.get_full_path() if self.department else ""
