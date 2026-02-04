"""
推荐管理模型

包含推荐规则、推荐商品等模型
"""
from django.db import models
from django.utils import timezone


class RecommendationRule(models.Model):
    """
    推荐规则模型

    用于定义不同类型的商品推荐规则，如：
    - hot: 热门推荐（基于销量和浏览量）
    - new: 新品推荐（基于创建时间）
    - collaborative: 协同过滤推荐（基于用户行为）
    """
    # 规则类型
    class RuleType(models.TextChoices):
        HOT = 'hot', '热门推荐'
        NEW = 'new', '新品推荐'
        PERSONALIZED = 'personalized', '个性化推荐'
        CATEGORY = 'category', '分类推荐'

    name = models.CharField('规则名称', max_length=100)
    rule_type = models.CharField(
        '规则类型',
        max_length=20,
        choices=RuleType.choices,
        default=RuleType.HOT
    )
    description = models.TextField('规则描述', blank=True, default='')

    # 配置参数（JSON格式，用于存储规则特定配置）
    # 例如：{"min_sales": 100, "days": 30} 表示30天内销量超过100的商品
    config = models.JSONField('配置参数', default=dict, blank=True)

    # 优先级（数字越大优先级越高）
    priority = models.IntegerField('优先级', default=0, db_index=True)

    # 限制数量（该规则最多返回多少个商品）
    limit = models.IntegerField('限制数量', default=10)

    # 状态
    is_active = models.BooleanField('是否启用', default=True, db_index=True)

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'recommendation_rules'
        verbose_name = '推荐规则'
        verbose_name_plural = '推荐规则管理'
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"


class RecommendedProduct(models.Model):
    """
    推荐商品模型

    用于手动配置推荐商品，管理员可以将特定商品关联到推荐规则中
    """
    rule = models.ForeignKey(
        RecommendationRule,
        on_delete=models.CASCADE,
        related_name='recommended_products',
        verbose_name='推荐规则'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='recommendations',
        verbose_name='商品'
    )

    # 排序权重（数字越大越靠前）
    sort_order = models.IntegerField('排序权重', default=0)

    # 备注（管理员可记录推荐理由）
    remark = models.CharField('备注', max_length=200, blank=True, default='')

    # 时间字段
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        db_table = 'recommended_products'
        verbose_name = '推荐商品'
        verbose_name_plural = '推荐商品管理'
        ordering = ['-sort_order', '-created_at']
        # 确保同一规则下商品不重复
        unique_together = [['rule', 'product']]

    def __str__(self):
        return f"{self.rule.name} - {self.product.name}"
