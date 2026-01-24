from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    """公告详情序列化器"""
    published_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            'id', 'title', 'content', 'is_pinned', 'is_published',
            'published_by', 'published_by_name', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['published_by', 'published_at', 'created_at', 'updated_at']

    def get_published_by_name(self, obj):
        """处理发布人名称（兼容 null 情况）"""
        if obj.published_by:
            return obj.published_by.real_name
        return None


class NoticeListSerializer(serializers.ModelSerializer):
    """公告列表序列化器（轻量版）"""
    published_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            'id', 'title', 'content', 'is_pinned', 'is_published',
            'published_by_name', 'published_at', 'created_at'
        ]

    def get_published_by_name(self, obj):
        """处理发布人名称（兼容 null 情况）"""
        if obj.published_by:
            return obj.published_by.real_name
        return None


class NoticeCreateSerializer(serializers.ModelSerializer):
    """创建公告序列化器"""
    
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_pinned']
    
    def create(self, validated_data):
        # 创建时默认为未发布状态
        validated_data['is_published'] = False
        return super().create(validated_data)


class NoticePublishSerializer(serializers.Serializer):
    """发布公告序列化器"""
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        instance.publish(user)
        return instance
