from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    """公告序列化器"""
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
