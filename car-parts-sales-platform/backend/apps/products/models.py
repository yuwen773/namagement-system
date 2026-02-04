from django.db import models
from django.utils.html import strip_tags
import django.utils.timezone
from simple_history.models import HistoricalRecords


class Category(models.Model):
    """
    商品分类 - 支持多级分类
    """
    name = models.CharField('分类名称', max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父分类'
    )
    sort_order = models.IntegerField('排序权重', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', default=django.utils.timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name

    @property
    def full_path(self):
        """获取完整分类路径"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class Product(models.Model):
    """
    商品模型
    """
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('pending', '待审核'),
        ('published', '已上架'),
        ('archived', '已下架'),
    ]

    name = models.CharField('商品名称', max_length=200)
    description = models.TextField('商品描述', blank=True)
    price = models.DecimalField('销售价格', max_digits=10, decimal_places=2)
    original_price = models.DecimalField('原价', max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='商品分类'
    )
    stock_quantity = models.IntegerField('库存数量', default=0)
    main_image = models.CharField('主图URL', max_length=500, blank=True)
    status = models.CharField(
        '商品状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    sales_count = models.IntegerField('销量', default=0)
    view_count = models.IntegerField('浏览量', default=0)
    is_featured = models.BooleanField('是否推荐', default=False)
    is_new = models.BooleanField('是否新品', default=False)
    created_at = models.DateTimeField('创建时间', default=django.utils.timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    # history = HistoricalRecords()  # Temporarily disabled for debugging

    class Meta:
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = '商品管理'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def main_image_url(self):
        """获取主图URL，用于序列化"""
        return self.main_image

    @property
    def clean_description(self):
        """获取纯文本描述（去除HTML标签）"""
        return strip_tags(self.description) if self.description else ''


class ProductImage(models.Model):
    """
    商品图片
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='商品'
    )
    image_url = models.CharField('图片URL', max_length=500)
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', default=django.utils.timezone.now)

    class Meta:
        db_table = 'product_images'
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.name} - 图片{self.sort_order}"


class ProductAttribute(models.Model):
    """
    商品属性
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name='商品'
    )
    attr_name = models.CharField('属性名称', max_length=100)
    attr_value = models.CharField('属性值', max_length=500)
    sort_order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', default=django.utils.timezone.now)

    class Meta:
        db_table = 'product_attributes'
        verbose_name = '商品属性'
        verbose_name_plural = '商品属性'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.product.name} - {self.attr_name}: {self.attr_value}"


class Review(models.Model):
    """
    商品评价
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='商品'
    )
    user_id = models.IntegerField('用户ID', db_index=True)
    order_item_id = models.IntegerField('订单项ID', null=True, blank=True, db_index=True)
    rating = models.PositiveSmallIntegerField(
        '评分',
        choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
        default=5
    )
    comment = models.TextField('评价内容', blank=True)
    images = models.JSONField('评价图片', default=list, blank=True)
    is_anonymous = models.BooleanField('匿名评价', default=False)
    created_at = models.DateTimeField('创建时间', default=django.utils.timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = '商品评价'
        verbose_name_plural = '商品评价'
        ordering = ['-created_at']
        # 确保用户对同一订单项只能评价一次
        unique_together = ['product', 'order_item_id']

    def __str__(self):
        return f"{self.product.name} - 评分{self.rating}"
