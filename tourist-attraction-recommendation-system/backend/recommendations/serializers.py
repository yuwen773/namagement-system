"""
推荐应用序列化器
"""

from rest_framework import serializers
from attractions.models import Attraction


class AttractionRecommendSerializer(serializers.ModelSerializer):
    """景点推荐序列化器"""

    hot_score = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Attraction
        fields = [
            'id', 'name', 'description', 'address', 'category',
            'category_display', 'region', 'opening_hours', 'cover_image',
            'view_count', 'hot_score', 'created_at'
        ]

    def get_hot_score(self, obj):
        """获取热度分数"""
        # 从上下文中获取已计算的 hot_score
        hot_score = self.context.get('hot_score')
        if hot_score is not None:
            return hot_score
        # 如果没有，动态计算
        from .services import calculate_hot_score
        return calculate_hot_score(obj)

    def to_representation(self, instance):
        """自定义输出"""
        data = super().to_representation(instance)
        # 处理图片URL
        if instance.cover_image:
            request = self.context.get('request')
            if request:
                data['cover_image'] = request.build_absolute_uri(instance.cover_image.url)
            else:
                data['cover_image'] = instance.cover_image.url
        return data
