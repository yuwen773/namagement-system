from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Announcement
        # 移除 author 字段，只保留 author_name
        fields = ['id', 'title', 'content', 'is_published', 'is_top', 'author_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        # 只包含可写字段
        fields = ['title', 'content', 'is_published', 'is_top']
