"""
Serializers for crawler module.
爬虫模块的数据序列化器
"""
from rest_framework import serializers
from products.models import CrawlLog


class CrawlLogSerializer(serializers.ModelSerializer):
    """
    采集日志序列化器
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    mode_display = serializers.CharField(source='get_mode_display', read_only=True)
    duration_seconds = serializers.SerializerMethodField()

    class Meta:
        model = CrawlLog
        fields = [
            'id',
            'task_id',
            'status',
            'status_display',
            'mode',
            'mode_display',
            'keywords',
            'source_type',
            'start_time',
            'end_time',
            'duration_seconds',
            'items_collected',
            'items_success',
            'items_failed',
            'log_content',
            'error_message',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def get_duration_seconds(self, obj):
        """获取任务执行时长（秒）"""
        if obj.start_time and obj.end_time:
            delta = obj.end_time - obj.start_time
            return int(delta.total_seconds())
        return None


class CrawlLogListSerializer(serializers.ModelSerializer):
    """
    采集日志列表序列化器（简化版）
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    duration_seconds = serializers.SerializerMethodField()

    class Meta:
        model = CrawlLog
        fields = [
            'id',
            'task_id',
            'status',
            'status_display',
            'mode',
            'keywords',
            'source_type',
            'start_time',
            'duration_seconds',
            'items_collected',
            'items_success',
            'items_failed',
            'created_at',
        ]
        read_only_fields = fields

    def get_duration_seconds(self, obj):
        """获取任务执行时长（秒）"""
        if obj.start_time and obj.end_time:
            delta = obj.end_time - obj.start_time
            return int(delta.total_seconds())
        return None


class CrawlerStartSerializer(serializers.Serializer):
    """
    启动爬虫请求序列化器
    """
    mode = serializers.ChoiceField(
        choices=['normal', 'demo', 'batch'],
        default='normal',
        help_text="采集模式：normal（标准模式，默认3页）"
    )
    keywords = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="搜索关键词（单个）"
    )
    max_pages = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=3,
        help_text="采集页数限制，最多3页"
    )

    def validate(self, attrs):
        """验证参数组合"""
        # 如果是 normal 模式，必须提供 max_pages
        if attrs.get('mode') == 'normal':
            if 'max_pages' not in attrs:
                attrs['max_pages'] = 1  # 默认 1 页
        return attrs


class TaskStatusSerializer(serializers.Serializer):
    """
    任务状态响应序列化器
    """
    task_id = serializers.CharField()
    status = serializers.CharField()
    progress = serializers.CharField(required=False)
    current_stage = serializers.CharField(required=False)
    items_collected = serializers.IntegerField(required=False)
    logs = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    error = serializers.CharField(required=False)


class CrawlerStatsSerializer(serializers.Serializer):
    """
    爬虫统计信息序列化器
    """
    total_tasks = serializers.IntegerField()
    running_tasks = serializers.IntegerField()
    success_tasks = serializers.IntegerField()
    failed_tasks = serializers.IntegerField()
    total_items_collected = serializers.IntegerField()
    average_duration = serializers.FloatField()
