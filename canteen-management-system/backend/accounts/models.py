from django.db import models


class User(models.Model):
    """
    系统用户账号模型
    用于系统登录，与员工档案（EmployeeProfile）是可选关联
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', '管理员'
        EMPLOYEE = 'EMPLOYEE', '普通员工'

    class Status(models.TextChoices):
        ENABLED = 'ENABLED', '启用'
        DISABLED = 'DISABLED', '禁用'

    username = models.CharField(max_length=50, unique=True, verbose_name='登录账号')
    password = models.CharField(max_length=255, verbose_name='登录密码')
    employee_id = models.BigIntegerField(null=True, blank=True, verbose_name='关联员工档案ID')
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        verbose_name='角色类型'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ENABLED,
        verbose_name='账号状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'users'
        verbose_name = '用户账号'
        verbose_name_plural = '用户账号'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @classmethod
    def verify_password(cls, username, password):
        """
        验证用户名和密码
        返回用户对象或None
        """
        try:
            user = cls.objects.get(username=username, status=cls.Status.ENABLED)
            if user.password == password:  # 开发阶段明文比对
                return user
        except cls.DoesNotExist:
            pass
        return None
