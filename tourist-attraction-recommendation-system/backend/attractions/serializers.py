from rest_framework import serializers
from .models import Attraction


def get_cover_image_url(obj):
    """获取封面图 URL，处理外部 URL 和本地文件"""
    # 使用原始查询来获取数据库中的原始值，绕过 ImageField 的处理
    from django.db import connection

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT cover_image FROM attractions WHERE id = %s",
                [obj.id]
            )
            row = cursor.fetchone()
            if row and row[0]:
                raw_value = row[0]
                # 如果是外部 URL，直接返回
                if isinstance(raw_value, str) and (raw_value.startswith('http://') or raw_value.startswith('https://')):
                    return raw_value
                # 否则尝试作为本地文件处理
                if raw_value:
                    try:
                        return obj.cover_image.url
                    except:
                        return None
    except Exception:
        pass

    return None


class AttractionListSerializer(serializers.ModelSerializer):
    """景点列表序列化器（简化字段）"""
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'description', 'address', 'category', 'region',
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
