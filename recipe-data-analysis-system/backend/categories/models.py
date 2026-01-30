"""
分类模型

包含菜谱的各种分类标签，如菜系、场景、人群、口味等。
"""

from django.db import models
from utils.constants import CategoryType


class Category(models.Model):
    """
    分类表

    用于存储菜谱的各种分类标签，支持多种分类类型。
    分类类型包括：菜系（川菜、粤菜等）、场景（早餐、午餐等）、
    人群（儿童、老人等）、口味（辣、甜等）。

    字段:
        id: 主键
        name: 分类名称
        type: 分类类型 (cuisine/scene/crowd/taste)
        sort_order: 排序序号，数值越小越靠前
        created_at: 创建时间
        updated_at: 更新时间
    """

    # 分类名称
    name = models.CharField(
        max_length=50,
        verbose_name='分类名称',
        help_text='分类的显示名称，如"川菜"、"早餐"等'
    )

    # 分类类型
    type = models.CharField(
        max_length=20,
        choices=CategoryType.CHOICES,
        verbose_name='分类类型',
        help_text='分类类型：菜系/场景/人群/口味',
        db_index=True
    )

    # 排序序号
    sort_order = models.IntegerField(
        default=0,
        verbose_name='排序序号',
        help_text='数值越小越靠前，默认为0'
    )

    # 创建时间
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    # 更新时间
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        db_table = 'categories'
        verbose_name = '分类'
        verbose_name_plural = '分类'
        # 默认按类型和排序序号排列
        ordering = ['type', 'sort_order', 'id']
        # 联合唯一约束：同一类型下分类名称唯一
        unique_together = [['type', 'name']]
        # 索引
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['sort_order']),
        ]

    def __str__(self):
        """返回分类的字符串表示"""
        return f'{self.get_type_display()} - {self.name}'

    @classmethod
    def get_by_type(cls, category_type):
        """
        获取指定类型的所有分类

        Args:
            category_type: 分类类型 (cuisine/scene/crowd/taste)

        Returns:
            QuerySet: 指定类型的分类列表
        """
        return cls.objects.filter(type=category_type).order_by('sort_order', 'id')

    @classmethod
    def get_cuisines(cls):
        """获取所有菜系分类"""
        return cls.get_by_type(CategoryType.CUISINE)

    @classmethod
    def get_scenes(cls):
        """获取所有场景分类"""
        return cls.get_by_type(CategoryType.SCENE)

    @classmethod
    def get_crowds(cls):
        """获取所有人群分类"""
        return cls.get_by_type(CategoryType.CROWD)

    @classmethod
    def get_tastes(cls):
        """获取所有口味分类"""
        return cls.get_by_type(CategoryType.TASTE)
