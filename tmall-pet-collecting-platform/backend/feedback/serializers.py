from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """反馈详情序列化器"""
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'user_username', 'title', 'content', 'contact', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'created_at']


class FeedbackListSerializer(serializers.ModelSerializer):
    """反馈列表序列化器"""
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user_username', 'title', 'status', 'created_at']


class FeedbackUpdateSerializer(serializers.ModelSerializer):
    """反馈状态更新序列化器"""

    class Meta:
        model = Feedback
        fields = ['status']
