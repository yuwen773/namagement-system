"""
收藏模块 - 序列化器定义

本模块定义收藏相关的 DRF 序列化器。
"""
from rest_framework import serializers
from .models import UserFavorite
from recipes.models import Recipe
from recipes.serializers import RecipeListSerializer


class FavoriteCreateSerializer(serializers.Serializer):
    """
    收藏创建序列化器

    用于创建收藏记录时验证输入数据
    """
    recipe_id = serializers.IntegerField(
        min_value=1,
        help_text='菜谱ID'
    )

    def validate_recipe_id(self, value):
        """
        验证菜谱是否存在

        Args:
            value: 菜谱ID

        Returns:
            int: 验证通过的菜谱ID

        Raises:
            ValidationError: 菜谱不存在时
        """
        if not Recipe.objects.filter(id=value).exists():
            raise serializers.ValidationError('菜谱不存在')
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    """
    收藏序列化器

    用于返回收藏记录详情
    """
    recipe = RecipeListSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserFavorite
        fields = ['id', 'recipe', 'created_at']
        read_only_fields = ['id', 'created_at']


class FavoriteListSerializer(serializers.ModelSerializer):
    """
    收藏列表序列化器

    用于返回用户的收藏列表
    """
    id = serializers.IntegerField(read_only=True)
    recipe_id = serializers.IntegerField(source='recipe.id', read_only=True)
    recipe_name = serializers.CharField(source='recipe.name', read_only=True)
    recipe_image = serializers.CharField(source='recipe.image_url', read_only=True)
    cuisine_type = serializers.CharField(source='recipe.cuisine_type', read_only=True)
    difficulty = serializers.CharField(source='recipe.difficulty', read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time', read_only=True)
    view_count = serializers.IntegerField(source='recipe.view_count', read_only=True)
    favorite_count = serializers.IntegerField(source='recipe.favorite_count', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserFavorite
        fields = [
            'id', 'recipe_id', 'recipe_name', 'recipe_image',
            'cuisine_type', 'difficulty', 'cooking_time',
            'view_count', 'favorite_count', 'created_at'
        ]
