"""
菜谱模块 - 模型定义

本模块定义菜谱相关的数据库模型，包括：
- Recipe: 菜谱主表，存储菜谱的基本信息
"""
from django.db import models


class Recipe(models.Model):
    """
    菜谱主表

    存储菜谱的基本信息，包括名称、分类、难度、时长等
    """

    # ===== 基础信息 =====
    name = models.CharField(
        max_length=200,
        verbose_name='菜谱名称',
        help_text='菜谱的名称，如"宫保鸡丁"'
    )

    # ===== 分类字段 =====
    cuisine_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='菜系分类',
        help_text='所属菜系，如"川菜"、"粤菜"等'
    )

    scene_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='场景分类',
        help_text='适用场景，如"早餐"、"午餐"、"晚餐"等'
    )

    target_audience = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='适用人群',
        help_text='适用人群，如"儿童"、"老人"、"孕妇"等'
    )

    # ===== 难度与时长 =====
    DIFFICULTY_CHOICES = [
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    ]
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name='难度等级',
        help_text='烹饪难度等级：简单、中等、困难'
    )

    cooking_time = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='烹饪时长（分钟）',
        help_text='完成这道菜所需的时间，单位为分钟'
    )

    # ===== 图片与步骤 =====
    image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='成品图片URL',
        help_text='菜谱成品图的URL地址'
    )

    steps = models.TextField(
        blank=True,
        verbose_name='制作步骤',
        help_text='菜谱的详细制作步骤，可使用JSON格式存储结构化数据'
    )

    # ===== 口味标签 =====
    # 口味标签用逗号分隔存储，如"辣,甜,酸"
    flavor_tags = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='口味标签',
        help_text='口味标签，多个标签用逗号分隔，如"辣,甜,酸"'
    )

    # ===== 统计字段 =====
    view_count = models.IntegerField(
        default=0,
        verbose_name='点击量',
        help_text='菜谱被点击浏览的次数'
    )

    favorite_count = models.IntegerField(
        default=0,
        verbose_name='收藏量',
        help_text='菜谱被收藏的次数'
    )

    # ===== 时间戳 =====
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='菜谱创建的时间'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='菜谱最后更新的时间'
    )

    # ===== Meta 信息 =====
    class Meta:
        db_table = 'recipes'
        verbose_name = '菜谱'
        verbose_name_plural = '菜谱'
        ordering = ['-created_at']

        # 索引定义
        indexes = [
            models.Index(fields=['name']),                    # 菜谱名称索引（用于搜索）
            models.Index(fields=['cuisine_type']),            # 菜系分类索引（用于筛选）
            models.Index(fields=['difficulty']),              # 难度等级索引（用于筛选）
            models.Index(fields=['scene_type']),              # 场景分类索引（用于筛选）
            models.Index(fields=['view_count']),              # 点击量索引（用于排序）
            models.Index(fields=['favorite_count']),          # 收藏量索引（用于排序）
            models.Index(fields=['-created_at']),             # 创建时间索引（用于排序）
        ]

    def __str__(self):
        """字符串表示"""
        return self.name

    def get_flavor_list(self):
        """
        获取口味标签列表

        Returns:
            list: 口味标签列表
        """
        if self.flavor_tags:
            return [tag.strip() for tag in self.flavor_tags.split(',') if tag.strip()]
        return []

    def set_flavor_list(self, flavor_list):
        """
        设置口味标签列表

        Args:
            flavor_list (list): 口味标签列表
        """
        self.flavor_tags = ','.join(flavor_list) if flavor_list else ''


class RecipeIngredient(models.Model):
    """
    菜谱-食材关联表

    存储菜谱与食材的多对多关联关系，以及用量信息
    """

    # ===== 关联关系 =====
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='菜谱',
        help_text='关联的菜谱'
    )

    ingredient = models.ForeignKey(
        'ingredients.Ingredient',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='食材',
        help_text='关联的食材'
    )

    # ===== 用量信息 =====
    amount = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='用量描述',
        help_text='食材用量，如"200g"、"2个"、"适量"等'
    )

    # ===== 排序 =====
    sort_order = models.IntegerField(
        default=0,
        verbose_name='排序序号',
        help_text='食材在菜谱中的显示顺序'
    )

    # ===== 时间戳 =====
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    # ===== Meta 信息 =====
    class Meta:
        db_table = 'recipe_ingredients'
        verbose_name = '菜谱食材关联'
        verbose_name_plural = '菜谱食材关联'
        ordering = ['recipe', 'sort_order']

        # 联合唯一约束：同一菜谱不能重复添加同一食材
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

        # 索引定义
        indexes = [
            models.Index(fields=['recipe']),                 # 菜谱ID索引（用于查询菜谱的食材）
            models.Index(fields=['ingredient']),             # 食材ID索引（用于查询使用该食材的菜谱）
        ]

    def __str__(self):
        """字符串表示"""
        return f"{self.recipe.name} - {self.ingredient.name} ({self.amount or '未指定用量'})"
