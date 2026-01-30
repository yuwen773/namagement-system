"""
食材模块 - 序列化器定义

本模块定义食材相关的序列化器，包括：
- IngredientSerializer: 食材基本信息序列化器
- IngredientListSerializer: 食材列表序列化器
"""
from rest_framework import serializers
from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """
    食材基本信息序列化器

    用于食材的详情展示和创建/更新操作
    """

    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id', 'name', 'category', 'category_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IngredientListSerializer(serializers.ModelSerializer):
    """
    食材列表序列化器

    用于食材列表的展示，包含较少字段以提升性能
    """

    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'category', 'category_display']
