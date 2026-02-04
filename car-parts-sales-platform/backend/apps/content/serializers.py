"""
内容管理序列化器
"""
from rest_framework import serializers
from .models import ModificationCase, FAQ


class ModificationCaseListSerializer(serializers.ModelSerializer):
    """改装案例列表序列化器（简洁版）"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ModificationCase
        fields = [
            'id', 'title', 'summary', 'cover_image',
            'author', 'status', 'status_display',
            'view_count', 'published_at', 'created_at'
        ]
        read_only_fields = ['view_count', 'created_at', 'updated_at']


class ModificationCaseDetailSerializer(serializers.ModelSerializer):
    """改装案例详情序列化器（完整版）"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ModificationCase
        fields = [
            'id', 'title', 'summary', 'content',
            'cover_image', 'author', 'status', 'status_display',
            'view_count', 'sort_order', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['view_count', 'created_at', 'updated_at']


class ModificationCaseCreateSerializer(serializers.ModelSerializer):
    """改装案例创建序列化器"""

    class Meta:
        model = ModificationCase
        fields = [
            'title', 'summary', 'content',
            'cover_image', 'author', 'status',
            'sort_order', 'published_at'
        ]


class ModificationCaseUpdateSerializer(serializers.ModelSerializer):
    """改装案例更新序列化器（部分更新时使用）"""

    class Meta:
        model = ModificationCase
        fields = [
            'title', 'summary', 'content',
            'cover_image', 'author', 'status',
            'sort_order', 'published_at'
        ]
        extra_kwargs = {
            'title': {'required': False},
            'summary': {'required': False},
            'content': {'required': False},
            'cover_image': {'required': False},
            'author': {'required': False},
            'status': {'required': False},
            'sort_order': {'required': False},
            'published_at': {'required': False},
        }


class FAQSerializer(serializers.ModelSerializer):
    """常见问题序列化器"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = FAQ
        fields = [
            'id', 'question', 'answer', 'category',
            'category_display', 'sort_order',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
