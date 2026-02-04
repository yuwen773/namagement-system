"""
内容管理模型

包含改装案例、常见问题等模型
"""
from django.db import models
from django.utils import timezone


class ModificationCase(models.Model):
    """
    改装案例模型

    用于展示汽车改装案例，包含标题、内容、图片等信息
    """
    # 状态
    class Status(models.TextChoices):
        DRAFT = 'draft', '草稿'
        PUBLISHED = 'published', '已发布'

    title = models.CharField('标题', max_length=200)
    summary = models.CharField('摘要', max_length=500, blank=True, default='')
    content = models.TextField('内容')

    # 封面图片
    cover_image = models.CharField('封面图片URL', max_length=500, blank=True, default='')

    # 作者
    author = models.CharField('作者', max_length=100, blank=True, default='')

    # 状态
    status = models.CharField(
        '状态',
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True
    )

    # 浏览量
    view_count = models.IntegerField('浏览量', default=0)

    # 排序权重
    sort_order = models.IntegerField('排序权重', default=0)

    # 时间字段
    published_at = models.DateTimeField('发布时间', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'modification_cases'
        verbose_name = '改装案例'
        verbose_name_plural = '改装案例管理'
        ordering = ['-sort_order', '-published_at', '-created_at']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """
    常见问题模型（FAQ）

    用于管理用户常见问题和解答
    """
    # 分类
    class Category(models.TextChoices):
        ORDER = 'order', '订单问题'
        PAYMENT = 'payment', '支付问题'
        SHIPPING = 'shipping', '物流问题'
        PRODUCT = 'product', '商品问题'
        RETURN = 'return', '退换货问题'
        ACCOUNT = 'account', '账户问题'
        OTHER = 'other', '其他问题'

    question = models.CharField('问题', max_length=500)
    answer = models.TextField('答案')

    # 分类
    category = models.CharField(
        '分类',
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        db_index=True
    )

    # 排序
    sort_order = models.IntegerField('排序', default=0)

    # 是否启用
    is_active = models.BooleanField('是否启用', default=True, db_index=True)

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'faqs'
        verbose_name = '常见问题'
        verbose_name_plural = '常见问题管理'
        ordering = ['category', 'sort_order', '-created_at']

    def __str__(self):
        return self.question
