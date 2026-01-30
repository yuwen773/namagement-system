"""
菜谱模块 - 序列化器定义

本模块定义菜谱相关的序列化器，包括：
- RecipeSerializer: 菜谱基本信息序列化器
- RecipeListSerializer: 菜谱列表序列化器
- RecipeImageUploadSerializer: 菜谱图片上传序列化器
"""
from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """
    菜谱基本信息序列化器

    用于菜谱的详情展示和创建/更新操作
    """

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'cuisine_type', 'scene_type', 'target_audience',
            'difficulty', 'cooking_time', 'image_url', 'steps', 'flavor_tags',
            'view_count', 'favorite_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'view_count', 'favorite_count', 'created_at', 'updated_at']


class RecipeListSerializer(serializers.ModelSerializer):
    """
    菜谱列表序列化器

    用于菜谱列表的展示，包含较少字段以提升性能
    """

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'cuisine_type', 'scene_type', 'difficulty',
            'cooking_time', 'image_url', 'flavor_tags', 'view_count',
            'favorite_count', 'created_at'
        ]


class RecipeImageUploadSerializer(serializers.Serializer):
    """
    菜谱图片上传序列化器

    用于验证图片上传请求
    """

    image = serializers.ImageField(
        help_text='图片文件，支持 jpg、jpeg、png、webp 格式',
        allow_empty_file=False,
        required=True
    )

    def validate_image(self, value):
        """
        验证图片文件

        Args:
            value: 上传的图片文件

        Returns:
            ImageField: 验证后的图片文件

        Raises:
            ValidationError: 图片格式或大小不符合要求
        """
        # 检查文件大小（Django 默认限制 2.5MB，约 2621440 字节）
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError('图片大小不能超过 5MB')

        # 检查文件扩展名
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        import os
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError('仅支持 jpg、jpeg、png、webp 格式的图片')

        return value


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    菜谱食材关联序列化器

    用于展示菜谱的食材列表
    """

    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'amount', 'sort_order']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """
    菜谱详情序列化器

    继承自 RecipeSerializer，增加食材列表等详细信息
    """

    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True
    )
    flavor_list = serializers.ListField(
        source='get_flavor_list',
        read_only=True
    )

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['ingredients', 'flavor_list']
