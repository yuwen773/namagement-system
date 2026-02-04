"""
系统管理序列化器

包含系统配置、消息通知、操作日志的序列化器
"""
from rest_framework import serializers
from .models import SystemConfig, Message, OperationLog


class SystemConfigSerializer(serializers.ModelSerializer):
    """系统配置序列化器"""

    class Meta:
        model = SystemConfig
        fields = [
            'id', 'key', 'value', 'description', 'category',
            'is_editable', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemConfigListSerializer(serializers.ModelSerializer):
    """系统配置列表序列化器（简化版）"""

    class Meta:
        model = SystemConfig
        fields = ['id', 'key', 'value', 'description', 'category', 'is_editable']


class MessageSerializer(serializers.ModelSerializer):
    """站内消息序列化器"""

    # 显示字段
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    recipient_name = serializers.CharField(source='recipient.nickname', read_only=True, default=None)

    class Meta:
        model = Message
        fields = [
            'id', 'recipient', 'recipient_name', 'title', 'content',
            'message_type', 'message_type_display', 'status', 'status_display',
            'sent_at', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'sent_at', 'read_at', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """创建消息序列化器"""

    class Meta:
        model = Message
        fields = ['id', 'recipient', 'title', 'content', 'message_type']
        extra_kwargs = {
            'recipient': {'required': False, 'allow_null': True},
            'title': {'required': True, 'max_length': 200},
            'content': {'required': True},
            'message_type': {'required': True},
        }


class MessageListSerializer(serializers.ModelSerializer):
    """消息列表序列化器（简化版）"""

    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'title', 'message_type', 'message_type_display',
            'status', 'status_display', 'sent_at', 'read_at', 'created_at'
        ]


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""

    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    operator_name = serializers.CharField(source='operator.nickname', read_only=True, default=None)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = OperationLog
        fields = [
            'id', 'operator', 'operator_name', 'action_type', 'action_type_display',
            'object_type', 'object_id', 'detail', 'ip_address',
            'status', 'status_display', 'error_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class OperationLogListSerializer(serializers.ModelSerializer):
    """操作日志列表序列化器（简化版）"""

    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    operator_name = serializers.CharField(source='operator.nickname', read_only=True, default=None)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = OperationLog
        fields = [
            'id', 'operator', 'operator_name', 'action_type', 'action_type_display',
            'object_type', 'detail', 'status', 'status_display', 'created_at'
        ]
