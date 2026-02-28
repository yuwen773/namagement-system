from django.db import models
import uuid


class Product(models.Model):
    """商品模型 - 存储天猫宠物用品数据"""

    # 宠物类型选项
    PET_TYPE_CHOICES = [
        ('cat', '猫咪'),
        ('dog', '狗狗'),
        ('aquatic', '水族'),
        ('small_pet', '小宠物'),
        ('other', '其他'),
    ]
    # 用途分类选项
    PET_USE_CHOICES = [
        ('food', '食品'),
        ('supplies', '用品'),
        ('toy', '玩具'),
        ('healthcare', '医疗保健'),
        ('grooming', '清洁护理'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='UUID')
    product_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='天猫商品ID')
    title = models.CharField(max_length=500, verbose_name='商品标题')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格（元）')
    price_unit = models.CharField(max_length=20, blank=True, null=True, verbose_name='价格单位')
    price_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='价格描述')
    sales = models.IntegerField(default=0, verbose_name='销量')
    shop = models.CharField(max_length=200, verbose_name='店铺名称')
    seller_nick = models.CharField(max_length=100, blank=True, null=True, verbose_name='卖家昵称')
    shop_tags = models.CharField(max_length=500, blank=True, null=True, verbose_name='店铺标签')
    region = models.CharField(max_length=100, blank=True, null=True, verbose_name='地区')
    tags = models.CharField(max_length=500, blank=True, null=True, verbose_name='商品标签')
    product_attributes = models.JSONField(blank=True, null=True, verbose_name='商品属性')
    image_url = models.URLField(max_length=1000, blank=True, null=True, verbose_name='商品图片URL')
    detail_url = models.URLField(max_length=1000, verbose_name='商品详情页URL')
    brand = models.CharField(max_length=100, blank=True, null=True, verbose_name='品牌')
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='类目')
    # 在 category 字段后添加新字段
    pet_type = models.CharField(
        max_length=20,
        choices=PET_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name='宠物类型'
    )
    pet_use = models.CharField(
        max_length=20,
        choices=PET_USE_CHOICES,
        null=True,
        blank=True,
        verbose_name='用途分类'
    )
    batch_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='采集批次号')
    crawl_time = models.DateTimeField(verbose_name='采集时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'products'
        verbose_name = '宠物商品'
        verbose_name_plural = '宠物商品'
        ordering = ['-crawl_time']
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['title']),
            models.Index(fields=['price']),
            models.Index(fields=['sales']),
            models.Index(fields=['shop']),
            models.Index(fields=['brand']),
            models.Index(fields=['category']),
            models.Index(fields=['pet_type']),
            models.Index(fields=['pet_use']),
            models.Index(fields=['batch_no']),
            models.Index(fields=['region']),
            models.Index(fields=['-crawl_time']),
        ]

    def __str__(self):
        return f"{self.title} - ¥{self.price}"


class PriceHistory(models.Model):
    """商品历史价格模型 - 记录商品价格变化历史"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='历史记录ID')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='price_history',
        verbose_name='商品'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='历史价格（元）')
    sales = models.IntegerField(default=0, verbose_name='历史销量')
    record_date = models.DateField(verbose_name='记录日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'price_history'
        verbose_name = '商品历史价格'
        verbose_name_plural = '商品历史价格'
        ordering = ['-record_date']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['-record_date']),
            models.Index(fields=['product', '-record_date']),
        ]
        unique_together = ['product', 'record_date']

    def __str__(self):
        return f"{self.product.title} - {self.record_date} - ¥{self.price}"


class CrawlLog(models.Model):
    """采集日志模型 - 记录爬虫任务执行情况"""

    class Status(models.TextChoices):
        PENDING = 'pending', '等待中'
        RUNNING = 'running', '进行中'
        SUCCESS = 'success', '成功'
        FAILED = 'failed', '失败'
        CANCELLED = 'cancelled', '已取消'

    class SourceType(models.TextChoices):
        MTOP_API = 'mtop_api', '淘宝 mtop API'
        REAL_API = 'real_api', '真实API (g_page_config)'
        JSON_API = 'json', '旧版JSON API'
        PLAYWRIGHT = 'playwright', 'Playwright渲染'
        DEMO = 'demo', '演示模式'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='日志ID')
    task_id = models.CharField(max_length=100, unique=True, verbose_name='Celery任务ID')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='状态'
    )
    mode = models.CharField(max_length=20, verbose_name='采集模式', help_text='normal: 标准模式, demo: 演示模式, batch: 分批采集')
    keywords = models.CharField(max_length=500, blank=True, null=True, verbose_name='搜索关键词')
    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        blank=True,
        null=True,
        verbose_name='采集来源'
    )
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='开始时间')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='结束时间')
    items_collected = models.IntegerField(default=0, verbose_name='采集数量')
    items_success = models.IntegerField(default=0, verbose_name='成功数量')
    items_failed = models.IntegerField(default=0, verbose_name='失败数量')
    log_content = models.TextField(blank=True, null=True, verbose_name='日志内容')
    error_message = models.TextField(blank=True, null=True, verbose_name='错误信息')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'crawl_logs'
        verbose_name = '采集日志'
        verbose_name_plural = '采集日志'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task_id']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"任务 {self.task_id} - {self.get_status_display()}"
