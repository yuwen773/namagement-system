from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """反馈建议序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    replied_by_username = serializers.CharField(source='replied_by.username', read_only=True)

    feedback_type_display = serializers.CharField(source='get_feedback_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'title', 'content', 'feedback_type', 'feedback_type_display',
            'status', 'status_display', 'admin_reply', 'replied_at', 'replied_by',
            'replied_by_username', 'user', 'username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'replied_at', 'replied_by', 'username', 'replied_by_username']
