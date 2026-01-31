"""
食材模块 - 序列化器定义

本模块定义食材相关的序列化器，包括：
- IngredientSerializer: 食材基本信息序列化器
- IngredientListSerializer: 食材列表序列化器
- IngredientCreateSerializer: 食材创建序列化器
- IngredientUpdateSerializer: 食材更新序列化器
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


class IngredientCreateSerializer(serializers.ModelSerializer):
    """
    食材创建序列化器

    用于管理员创建食材
    """
    class Meta:
        model = Ingredient
        fields = ['name', 'category']
        extra_kwargs = {
            'name': {'required': True, 'help_text': '食材名称'},
            'category': {'required': True, 'help_text': '食材分类'},
        }

    def validate(self, attrs):
        """验证食材名称的唯一性"""
        name = attrs.get('name')

        # 检查食材名称是否已存在
        if Ingredient.objects.filter(name=name).exists():
            raise serializers.ValidationError(f'食材名称 "{name}" 已存在')

        return attrs


class IngredientUpdateSerializer(serializers.ModelSerializer):
    """
    食材更新序列化器

    用于管理员更新食材
    """
    class Meta:
        model = Ingredient
        fields = ['name', 'category']
        extra_kwargs = {
            'name': {'required': False},
            'category': {'required': False},
        }

    def validate(self, attrs):
        """验证食材名称的唯一性（排除自身）"""
        instance = self.instance
        name = attrs.get('name', instance.name)

        # 检查食材名称是否已存在（排除当前实例）
        if Ingredient.objects.filter(name=name).exclude(id=instance.id).exists():
            raise serializers.ValidationError(f'食材名称 "{name}" 已存在')

        return attrs
