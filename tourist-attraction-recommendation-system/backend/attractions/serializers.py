from rest_framework import serializers
from .models import Attraction


class AttractionListSerializer(serializers.ModelSerializer):
    """景点列表序列化器（简化字段）"""
    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'description', 'category', 'region',
            'cover_image', 'view_count', 'created_at'
        ]


class AttractionDetailSerializer(serializers.ModelSerializer):
    """景点详情序列化器（完整字段）"""
    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'description', 'address', 'category', 'region',
            'opening_hours', 'cover_image', 'images', 'view_count',
            'is_deleted', 'created_at', 'updated_at'
        ]


class AttractionCreateUpdateSerializer(serializers.ModelSerializer):
    """景点创建/更新序列化器"""
    class Meta:
        model = Attraction
        fields = [
            'name', 'description', 'address', 'category', 'region',
            'opening_hours', 'cover_image', 'images'
        ]
