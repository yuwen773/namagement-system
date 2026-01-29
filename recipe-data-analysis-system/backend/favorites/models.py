"""
收藏模块 - 模型定义

本模块定义收藏相关的数据库模型，包括：
- UserFavorite: 用户收藏表，存储用户对菜谱的收藏关系
"""
from django.db import models


class UserFavorite(models.Model):
    """
    用户收藏表

    存储用户对菜谱的收藏关系，一个用户可以收藏多个菜谱，
    一个菜谱也可以被多个用户收藏。

    Attributes:
        user: 关联的用户（外键）
        recipe: 关联的菜谱（外键）
        created_at: 收藏时间
    """

    # ===== 关联关系 =====
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='用户',
        help_text='收藏该菜谱的用户'
    )

    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='菜谱',
        help_text='被收藏的菜谱'
    )

    # ===== 时间戳 =====
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='收藏时间',
        help_text='用户收藏该菜谱的时间'
    )

    # ===== Meta 信息 =====
    class Meta:
        db_table = 'user_favorites'
        verbose_name = '用户收藏'
        verbose_name_plural = '用户收藏'
        ordering = ['-created_at']

        # 联合唯一约束：同一用户不能重复收藏同一菜谱
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]

        # 索引定义
        indexes = [
            models.Index(fields=['user']),                    # 用户ID索引（用于查询用户的收藏）
            models.Index(fields=['recipe']),                  # 菜谱ID索引（用于查询收藏该菜谱的用户）
            models.Index(fields=['-created_at']),             # 收藏时间索引（用于按时间排序）
        ]

    def __str__(self):
        """字符串表示"""
        return f"{self.user.username} 收藏了 {self.recipe.name}"
