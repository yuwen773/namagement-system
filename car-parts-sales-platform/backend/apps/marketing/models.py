"""
营销管理模型

包含优惠券、用户优惠券、促销活动、Banner 轮播图等模型
"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Promotion(models.Model):
    """
    促销活动模型
    """
    # 促销类型
    class Type(models.TextChoices):
        FLASH_SALE = 'flash_sale', '限时秒杀'
        BUNDLE = 'bundle', '组合优惠'
        SPECIAL_OFFER = 'special_offer', '特价活动'
        SEASONAL = 'seasonal', '季节性促销'

    name = models.CharField('促销活动名称', max_length=100)
    description = models.TextField('活动描述', blank=True, default='')

    # 活动类型
    promotion_type = models.CharField(
        '促销类型',
        max_length=20,
        choices=Type.choices,
        default=Type.SPECIAL_OFFER
    )

    # 关联商品（多个商品）
    products = models.ManyToManyField(
        'products.Product',
        related_name='promotions',
        verbose_name='关联商品',
        blank=True
    )

    # 关联优惠券
    coupon = models.ForeignKey(
        'Coupon',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='promotions',
        verbose_name='关联优惠券'
    )

    # 活动时间
    start_time = models.DateTimeField('活动开始时间')
    end_time = models.DateTimeField('活动结束时间')

    # 促销折扣（可选，用于直接折扣）
    discount_rate = models.DecimalField(
        '折扣率',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(9.9)],
        help_text='例如：8.5 表示 8.5 折'
    )

    # 促销金额（可选，用于直减）
    discount_amount = models.DecimalField(
        '优惠金额',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='直接减免的金额'
    )

    # 活动图片
    image = models.URLField('活动图片', blank=True, default='')

    # 排序权重
    sort_order = models.IntegerField('排序权重', default=0)

    # 状态
    is_active = models.BooleanField('是否启用', default=True, db_index=True)

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'promotions'
        verbose_name = '促销活动'
        verbose_name_plural = '促销活动管理'
        ordering = ['-sort_order', '-created_at']

    def __str__(self):
        return self.name

    @property
    def is_valid(self):
        """活动是否有效"""
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time


class Banner(models.Model):
    """
    Banner 轮播图模型
    """
    # 展示位置
    class Position(models.TextChoices):
        HOME = 'home', '首页'
        CATEGORY = 'category', '分类页'
        PRODUCT = 'product', '商品页'
        ACTIVITY = 'activity', '活动页'

    title = models.CharField('标题', max_length=100)
    subtitle = models.CharField('副标题', max_length=200, blank=True, default='')

    # Banner 图片
    image = models.URLField('Banner 图片')

    # 链接类型
    class LinkType(models.TextChoices):
        NONE = 'none', '无链接'
        PRODUCT = 'product', '商品详情'
        CATEGORY = 'category', '分类页'
        ACTIVITY = 'activity', '活动页'
        URL = 'url', '外部链接'

    link_type = models.CharField(
        '链接类型',
        max_length=20,
        choices=LinkType.choices,
        default=LinkType.NONE
    )
    link_value = models.CharField('链接值', max_length=500, blank=True, default='')

    # 展示位置
    position = models.CharField(
        '展示位置',
        max_length=20,
        choices=Position.choices,
        default=Position.HOME
    )

    # 排序权重
    sort_order = models.IntegerField('排序权重', default=0)

    # 状态
    is_active = models.BooleanField('是否启用', default=True, db_index=True)

    # 开始和结束时间
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'banners'
        verbose_name = 'Banner 轮播图'
        verbose_name_plural = 'Banner 轮播图管理'
        ordering = ['position', '-sort_order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_valid(self):
        """Banner 是否有效"""
        if not self.is_active:
            return False
        now = timezone.now()
        if self.start_time and now < self.start_time:
            return False
        if self.end_time and now > self.end_time:
            return False
        return True
