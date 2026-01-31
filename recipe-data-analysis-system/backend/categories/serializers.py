"""
分类模块 - 序列化器定义

本模块定义分类相关的序列化器，包括：
- CategorySerializer: 分类基本信息序列化器
- CategoryListSerializer: 分类列表序列化器
- CategoryCreateSerializer: 分类创建序列化器
- CategoryUpdateSerializer: 分类更新序列化器
"""
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    分类基本信息序列化器

    用于分类的详情展示和创建/更新操作
    """

    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_display', 'sort_order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategoryListSerializer(serializers.ModelSerializer):
    """
    分类列表序列化器

    用于分类列表的展示，只包含必要字段
    """

    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_display', 'sort_order']


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    分类创建序列化器

    用于管理员创建分类
    """
    class Meta:
        model = Category
        fields = ['name', 'type', 'sort_order']
        extra_kwargs = {
            'name': {'required': True, 'help_text': '分类名称'},
            'type': {'required': True, 'help_text': '分类类型'},
            'sort_order': {'required': False, 'default': 0, 'help_text': '排序序号，默认为0'},
        }

    def validate(self, attrs):
        """验证分类名称在同一类型下的唯一性"""
        name = attrs.get('name')
        category_type = attrs.get('type')

        # 检查同一类型下是否已存在同名分类
        if Category.objects.filter(type=category_type, name=name).exists():
            raise serializers.ValidationError(f'分类类型 "{category_type}" 下已存在名称为 "{name}" 的分类')

        return attrs


class CategoryUpdateSerializer(serializers.ModelSerializer):
    """
    分类更新序列化器

    用于管理员更新分类
    """
    class Meta:
        model = Category
        fields = ['name', 'type', 'sort_order']
        extra_kwargs = {
            'name': {'required': False},
            'type': {'required': False},
            'sort_order': {'required': False},
        }

    def validate(self, attrs):
        """验证分类名称在同一类型下的唯一性（排除自身）"""
        instance = self.instance
        name = attrs.get('name', instance.name)
        category_type = attrs.get('type', instance.type)

        # 检查同一类型下是否已存在同名分类（排除当前实例）
        if Category.objects.filter(type=category_type, name=name).exclude(id=instance.id).exists():
            raise serializers.ValidationError(f'分类类型 "{category_type}" 下已存在名称为 "{name}" 的分类')

        return attrs
