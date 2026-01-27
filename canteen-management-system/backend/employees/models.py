from django.db import models


class EmployeeProfile(models.Model):
    """
    员工业务档案模型
    用于排班、考勤、薪资等业务操作
    与用户账号（User）是可选关联关系
    """
    class Gender(models.TextChoices):
        MALE = 'MALE', '男'
        FEMALE = 'FEMALE', '女'

    class Position(models.TextChoices):
        CHEF = 'CHEF', '厨师'
        PASTRY = 'PASTRY', '面点'
        PREP = 'PREP', '切配'
        CLEANER = 'CLEANER', '保洁'
        SERVER = 'SERVER', '服务员'
        MANAGER = 'MANAGER', '经理'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', '在职'
        INACTIVE = 'INACTIVE', '离职'
        LEAVE_WITHOUT_PAY = 'LEAVE_WITHOUT_PAY', '停薪留职'

    # 基础信息
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        default=Gender.MALE,
        verbose_name='性别'
    )
    phone = models.CharField(max_length=20, verbose_name='联系方式')
    id_card = models.CharField(max_length=18, unique=True, null=True, blank=True, verbose_name='身份证号')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭住址')

    # 岗位信息
    position = models.CharField(
        max_length=20,
        choices=Position.choices,
        verbose_name='岗位'
    )
    entry_date = models.DateField(verbose_name='入职时间')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name='在职状态'
    )

    # 资质证书
    health_certificate_no = models.CharField(max_length=50, null=True, blank=True, verbose_name='健康证号')
    health_certificate_expiry = models.DateField(null=True, blank=True, verbose_name='健康证有效期')
    health_certificate_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='健康证图片地址')
    chef_certificate_level = models.CharField(max_length=20, null=True, blank=True, verbose_name='厨师等级证')

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'employee_profiles'
        verbose_name = '员工档案'
        verbose_name_plural = '员工档案'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_position_display()})'
