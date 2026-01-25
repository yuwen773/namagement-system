from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    扩展用户模型，添加 phone 和 role 字段
    """
    ROLE_CHOICES = [
        ('employee', '普通员工'),
        ('hr', '人事专员'),
        ('admin', '管理员'),
    ]

    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name='角色'
    )
    real_name = models.CharField(max_length=50, verbose_name='真实姓名')
    email = models.EmailField(unique=True, verbose_name='邮箱')

    # 设置手机号和邮箱为必填
    REQUIRED_FIELDS = ['phone', 'email', 'real_name']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.real_name or self.username


class UserEditRequest(models.Model):
    """
    用户信息修改申请表
    用于员工提交手机号、邮箱等信息的修改申请，HR/Admin 审批通过后自动更新
    """
    EDIT_TYPE_CHOICES = [
        ('phone', '手机号'),
        ('email', '邮箱'),
        ('emergency_contact', '紧急联系人'),
    ]

    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已通过'),
        ('rejected', '已驳回'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='edit_requests',
        verbose_name='申请人'
    )
    edit_type = models.CharField(
        max_length=20,
        choices=EDIT_TYPE_CHOICES,
        verbose_name='修改类型'
    )
    old_value = models.CharField(max_length=255, blank=True, verbose_name='原值')
    new_value = models.CharField(max_length=255, verbose_name='新值')
    reason = models.TextField(blank=True, verbose_name='修改原因')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='状态'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_requests',
        verbose_name='审批人'
    )
    reviewer_comment = models.TextField(blank=True, verbose_name='审批意见')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='审批时间')

    class Meta:
        db_table = 'accounts_usereditrequest'
        verbose_name = '信息修改申请'
        verbose_name_plural = '信息修改申请'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.real_name} - {self.get_edit_type_display()} - {self.get_status_display()}"
