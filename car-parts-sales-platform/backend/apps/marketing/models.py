"""
营销管理模型

包含优惠券、用户优惠券等模型
"""
from django.db import models
from django.utils import timezone
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'users.User')


class Coupon(models.Model):
    """
    优惠券模型
    """
    # 优惠类型
    class Type(models.TextChoices):
        FULL_REDUCTION = 'full_reduction', '满减券'
        DISCOUNT = 'discount', '折扣券'

    name = models.CharField('优惠券名称', max_length=100)
    description = models.TextField('优惠券描述', blank=True, default='')

    # 优惠类型和配置
    discount_type = models.CharField(
        '优惠类型',
        max_length=20,
        choices=Type.choices,
        default=Type.FULL_REDUCTION
    )
    min_amount = models.DecimalField('使用门槛', max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField('优惠金额', max_digits=10, decimal_places=2, default=0)
    discount_rate = models.DecimalField('折扣率', max_digits=5, decimal_places=2, null=True, blank=True)

    # 有效期
    valid_from = models.DateTimeField('有效期开始')
    valid_until = models.DateTimeField('有效期结束')

    # 发放限制
    total_quantity = models.IntegerField('发放总量', default=0)
    per_user_limit = models.IntegerField('每人限领数量', default=1)
    issued_quantity = models.IntegerField('已发放数量', default=0)

    # 状态
    is_active = models.BooleanField('是否启用', default=True, db_index=True)

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'coupons'
        verbose_name = '优惠券'
        verbose_name_plural = '优惠券管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class UserCoupon(models.Model):
    """
    用户优惠券模型
    """
    # 使用状态
    class Status(models.TextChoices):
        UNUSED = 'unused', '未使用'
        USED = 'used', '已使用'
        EXPIRED = 'expired', '已过期'

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_coupons',
        verbose_name='所属用户'
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name='user_coupons',
        verbose_name='优惠券'
    )

    # 状态
    status = models.CharField(
        '使用状态',
        max_length=20,
        choices=Status.choices,
        default=Status.UNUSED,
        db_index=True
    )

    # 使用的订单
    used_order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='used_coupons',
        verbose_name='使用的订单'
    )

    # 时间字段
    obtained_at = models.DateTimeField('领取时间', default=timezone.now)
    used_at = models.DateTimeField('使用时间', null=True, blank=True)

    class Meta:
        db_table = 'user_coupons'
        verbose_name = '用户优惠券'
        verbose_name_plural = '用户优惠券管理'
        ordering = ['-obtained_at']

    def __str__(self):
        return f'{self.user.phone} - {self.coupon.name}'
