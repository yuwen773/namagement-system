"""
订单管理模型

包含订单、订单商品、退换货申请等模型
"""
from django.db import models
from django.utils import timezone
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'users.User')


class Order(models.Model):
    """
    订单模型
    """
    # 订单状态常量
    class Status(models.TextChoices):
        PENDING_PAYMENT = 'pending_payment', '待付款'
        PENDING_SHIPMENT = 'pending_shipment', '待发货'
        SHIPPED = 'shipped', '已发货'
        COMPLETED = 'completed', '已完成'
        CANCELLED = 'cancelled', '已取消'

    # 订单号（唯一）
    order_no = models.CharField('订单号', max_length=32, unique=True, db_index=True)

    # 关联用户
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='所属用户'
    )

    # 收货地址信息（冗余存储，以防地址变更）
    recipient_name = models.CharField('收货人姓名', max_length=50)
    recipient_phone = models.CharField('收货人手机号', max_length=11)
    recipient_province = models.CharField('省份', max_length=50, default='')
    recipient_city = models.CharField('城市', max_length=50, default='')
    recipient_district = models.CharField('区县', max_length=50, default='')
    recipient_address = models.CharField('详细地址', max_length=255)

    # 订单金额
    total_amount = models.DecimalField('订单总额', max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField('优惠金额', max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField('运费', max_digits=10, decimal_places=2, default=0)
    pay_amount = models.DecimalField('实付金额', max_digits=10, decimal_places=2, default=0)

    # 优惠券（可选）
    coupon = models.ForeignKey(
        'marketing.UserCoupon',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='使用的优惠券'
    )

    # 订单状态
    status = models.CharField(
        '订单状态',
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING_PAYMENT,
        db_index=True
    )

    # 物流信息
    express_company = models.CharField('物流公司', max_length=50, blank=True, default='')
    tracking_number = models.CharField('物流单号', max_length=100, blank=True, default='')

    # 备注
    remark = models.TextField('订单备注', blank=True, default='')

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    paid_at = models.DateTimeField('付款时间', null=True, blank=True)
    shipped_at = models.DateTimeField('发货时间', null=True, blank=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)

    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order_no} - {self.get_status_display()}'

    def generate_order_no(self):
        """生成订单号：格式为日期 + 随机数"""
        import random
        import string
        from datetime import datetime

        date_str = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=6))
        return f'{date_str}{random_str}'

    def save(self, *args, **kwargs):
        # 如果订单号为空，自动生成
        if not self.order_no:
            self.order_no = self.generate_order_no()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    订单商品模型
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='所属订单'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='商品'
    )

    # 商品信息（冗余存储，以防商品变更）
    product_name = models.CharField('商品名称', max_length=255)
    product_image = models.URLField('商品图片', blank=True, default='')
    product_price = models.DecimalField('购买单价', max_digits=10, decimal_places=2)

    # 购买数量
    quantity = models.PositiveIntegerField('购买数量', default=1)

    # 小计
    subtotal = models.DecimalField('小计金额', max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        db_table = 'order_items'
        verbose_name = '订单商品'
        verbose_name_plural = '订单商品管理'
        ordering = ['id']

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    def save(self, *args, **kwargs):
        # 自动计算小计
        self.subtotal = self.product_price * self.quantity
        super().save(*args, **kwargs)


class ReturnRequest(models.Model):
    """
    退换货申请模型
    """
    # 申请类型
    class RequestType(models.TextChoices):
        RETURN = 'return', '退货'
        EXCHANGE = 'exchange', '换货'

    # 处理状态
    class Status(models.TextChoices):
        PENDING = 'pending', '待处理'
        APPROVED = 'approved', '已同意'
        REJECTED = 'rejected', '已拒绝'
        COMPLETED = 'completed', '已完成'

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='return_requests',
        verbose_name='关联订单'
    )

    # 申请类型
    request_type = models.CharField(
        '申请类型',
        max_length=20,
        choices=RequestType.choices,
        default=RequestType.RETURN
    )

    # 原因描述
    reason = models.TextField('退换货原因')
    evidence_images = models.JSONField('凭证图片URL列表', blank=True, null=True)

    # 处理状态
    status = models.CharField(
        '处理状态',
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    # 处理意见
    admin_note = models.TextField('处理意见', blank=True, default='')

    # 时间字段
    created_at = models.DateTimeField('申请时间', default=timezone.now, db_index=True)
    processed_at = models.DateTimeField('处理时间', null=True, blank=True)

    class Meta:
        db_table = 'return_requests'
        verbose_name = '退换货申请'
        verbose_name_plural = '退换货管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.order.order_no} - {self.get_request_type_display()} - {self.get_status_display()}'


class Cart(models.Model):
    """
    购物车模型

    每个用户只有一个购物车，购物车关联用户
    """
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='所属用户'
    )

    # 购物车中商品总数量
    total_items = models.PositiveIntegerField('商品总数', default=0)

    # 购物车中商品总金额
    total_price = models.DecimalField('商品总金额', max_digits=10, decimal_places=2, default=0)

    # 创建/更新时间
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'carts'
        verbose_name = '购物车'
        verbose_name_plural = '购物车管理'

    def __str__(self):
        return f'{self.user.nickname or self.user.phone} 的购物车'

    def update_totals(self):
        """更新购物车统计信息"""
        from django.db.models import Sum, Count
        from apps.products.models import Product

        items = self.items.all()
        self.total_items = items.aggregate(total=Count('id'))['total'] or 0

        # 计算总金额（使用商品当前价格）
        total = 0
        for item in items:
            product = item.product
            if product and product.status == 'published':
                total += product.price * item.quantity
            else:
                # 如果商品不存在或已下架，使用购物车记录的价格
                total += item.price * item.quantity

        self.total_price = total
        self.save(update_fields=['total_items', 'total_price', 'updated_at'])


class CartItem(models.Model):
    """
    购物车商品模型

    购物车中的每个商品项
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='所属购物车'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='商品'
    )

    # 商品信息（冗余存储，以防商品变更）
    product_name = models.CharField('商品名称', max_length=255)
    product_image = models.URLField('商品图片', blank=True, default='')
    price = models.DecimalField('商品单价', max_digits=10, decimal_places=2)

    # 数量
    quantity = models.PositiveIntegerField('数量', default=1)

    # 小计
    subtotal = models.DecimalField('小计金额', max_digits=10, decimal_places=2, default=0)

    # 添加时间
    added_at = models.DateTimeField('添加时间', default=timezone.now)

    class Meta:
        db_table = 'cart_items'
        verbose_name = '购物车商品'
        verbose_name_plural = '购物车商品管理'
        ordering = ['-added_at']
        # 同一个购物车中，每个商品只能有一条记录
        unique_together = [['cart', 'product']]

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    def save(self, *args, **kwargs):
        # 自动计算小计
        self.subtotal = self.price * self.quantity
        # 如果没有提供商品信息，从商品模型获取
        if not self.product_name and self.product:
            self.product_name = self.product.name
            self.product_image = self.product.main_image or ''
            self.price = self.product.price
        super().save(*args, **kwargs)

    def get_subtotal(self):
        """获取小计金额"""
        return self.price * self.quantity
