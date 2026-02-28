from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    """公告序列化器（完整版）"""
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'priority', 'priority_display',
            'status', 'status_display', 'is_pinned', 'created_by',
            'created_by_name', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']


class AnnouncementListSerializer(serializers.ModelSerializer):
    """公告列表序列化器（精简版）"""
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'priority', 'priority_display',
            'status', 'status_display', 'is_pinned',
            'created_at', 'published_at'
        ]


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    """公告创建序列化器"""

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority', 'is_pinned', 'status']

    def validate_title(self, value):
        """验证标题不能为空"""
        if not value or not value.strip():
            raise serializers.ValidationError("公告标题不能为空")
        return value.strip()

    def validate_content(self, value):
        """验证内容不能为空"""
        if not value or not value.strip():
            raise serializers.ValidationError("公告内容不能为空")
        return value.strip()
