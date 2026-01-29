"""
食材模块 - 模型定义

本模块定义食材相关的数据库模型，包括：
- Ingredient: 食材库，存储各种食材的基本信息
"""
from django.db import models
from utils.constants import IngredientCategory


class Ingredient(models.Model):
    """
    食材库

    存储各种食材的基本信息，包括名称、分类等
    """

    # ===== 基础信息 =====
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='食材名称',
        help_text='食材的名称，如"鸡肉"、"土豆"等'
    )

    category = models.CharField(
        max_length=20,
        choices=IngredientCategory.CHOICES,
        default=IngredientCategory.OTHER,
        verbose_name='食材分类',
        help_text='食材所属分类：蔬菜、肉类、海鲜、调料等'
    )

    # ===== 时间戳 =====
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='食材创建的时间'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='食材最后更新的时间'
    )

    # ===== Meta 信息 =====
    class Meta:
        db_table = 'ingredients'
        verbose_name = '食材'
        verbose_name_plural = '食材'
        ordering = ['category', 'name']

        # 索引定义
        indexes = [
            models.Index(fields=['name']),                    # 食材名称索引（用于搜索）
            models.Index(fields=['category']),                # 食材分类索引（用于筛选）
        ]

    def __str__(self):
        """字符串表示"""
        return f"{self.get_category_display()} - {self.name}"
