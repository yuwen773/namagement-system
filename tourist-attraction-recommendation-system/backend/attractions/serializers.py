from rest_framework import serializers
from .models import Attraction


def get_cover_image_url(obj):
    """获取封面图 URL，处理外部 URL 和本地文件"""
    # 直接从 __dict__ 获取原始值，避免 ImageField 的自动处理
    raw_value = obj.__dict__.get('cover_image')

    if not raw_value:
        return None

    # 如果是外部 URL，直接返回
    if isinstance(raw_value, str) and raw_value.startswith('http'):
        return raw_value

    # 如果是本地文件路径，使用 ImageField 的 url 方法
    cover = obj.cover_image
    if cover:
        try:
            return cover.url
        except (ValueError, FileNotFoundError):
            return None

    return None


class AttractionListSerializer(serializers.ModelSerializer):
    """景点列表序列化器（简化字段）"""
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'description', 'category', 'region',
            'cover_image', 'view_count', 'created_at',
            # 新增字段
            'latitude', 'longitude', 'rating_percentage',
            'guide_count', 'ranking', 'level'
        ]

    def get_cover_image(self, obj):
        return get_cover_image_url(obj)


class AttractionDetailSerializer(serializers.ModelSerializer):
    """景点详情序列化器（完整字段）"""
    cover_image = serializers.SerializerMethodField()

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

    def get_cover_image(self, obj):
        return get_cover_image_url(obj)


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
