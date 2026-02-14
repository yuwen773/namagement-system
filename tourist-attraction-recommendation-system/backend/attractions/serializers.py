from rest_framework import serializers
from .models import Attraction


class AttractionListSerializer(serializers.ModelSerializer):
    """景点列表序列化器（简化字段）"""

    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'description', 'address', 'category', 'region',
            'cover_image', 'view_count', 'created_at',
            # 新增字段
            'latitude', 'longitude', 'rating_percentage',
            'guide_count', 'ranking', 'level'
        ]


class AttractionDetailSerializer(serializers.ModelSerializer):
    """景点详情序列化器（完整字段）"""

    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'description', 'address', 'category', 'region',
            'opening_hours', 'cover_image', 'images', 'view_count',
            'is_deleted', 'created_at', 'updated_at',
            # 新增字段
            'latitude', 'longitude', 'rating_percentage',
            'guide_count', 'ranking', 'level'
        ]


class AttractionCreateUpdateSerializer(serializers.ModelSerializer):
    """景点创建/更新序列化器"""

    class Meta:
        model = Attraction
        fields = [
            'name', 'description', 'address', 'category', 'region',
            'opening_hours', 'cover_image', 'images',
            # 新增字段
            'latitude', 'longitude', 'rating_percentage',
            'guide_count', 'ranking', 'level'
        ]
        # 设置字段为可选
        extra_kwargs = {
            'region': {'required': False, 'allow_blank': True, 'default': ''},
            'opening_hours': {'required': False, 'allow_blank': True, 'default': ''},
            'cover_image': {'required': False},
            'images': {'required': False},
            'rating_percentage': {'required': False, 'default': 0.0},
            'latitude': {'required': False},
            'longitude': {'required': False},
            'guide_count': {'required': False, 'default': 0},
            'ranking': {'required': False},
            'level': {'required': False, 'allow_blank': True},
            'description': {'required': False, 'allow_blank': True},
        }

    def validate(self, attrs):
        # 确保必填字段有默认值
        attrs.setdefault('region', '')
        attrs.setdefault('opening_hours', '')
        attrs.setdefault('rating_percentage', 0.0)
        attrs.setdefault('guide_count', 0)
        attrs.setdefault('level', '')
        return super().validate(attrs)

    def create(self, validated_data):
        # 确保有默认值
        validated_data.setdefault('region', '')
        validated_data.setdefault('opening_hours', '')
        validated_data.setdefault('rating_percentage', 0.0)
        validated_data.setdefault('guide_count', 0)
        validated_data.setdefault('level', '')
        validated_data.setdefault('latitude', None)
        validated_data.setdefault('longitude', None)
        validated_data.setdefault('ranking', None)

        return super().create(validated_data)
