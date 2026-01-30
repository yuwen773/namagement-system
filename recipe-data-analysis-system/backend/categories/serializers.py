"""
分类模块 - 序列化器定义

本模块定义分类相关的序列化器，包括：
- CategorySerializer: 分类基本信息序列化器
- CategoryListSerializer: 分类列表序列化器
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
