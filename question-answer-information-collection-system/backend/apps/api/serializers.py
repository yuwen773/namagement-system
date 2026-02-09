"""
问答数据 API 序列化器

提供 Question 和 Answer 数据的序列化/反序列化支持。
"""

from rest_framework import serializers
from apps.crawler.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    """答案序列化器"""
    class Meta:
        model = Answer
        fields = [
            'id',
            'content',
            'answerer',
            'answer_time',
            'source_order',
            'created_at',
        ]
        read_only_fields = ['created_at']


class QuestionSerializer(serializers.ModelSerializer):
    """问题序列化器"""
    answers = AnswerSerializer(many=True, read_only=True)
    answer_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'question_id',
            'title',
            'description',
            'category',
            'publish_time',
            'location',
            'answer_count',
            'crawl_page',
            'source_url',
            'answers',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class QuestionListSerializer(serializers.ModelSerializer):
    """问题列表序列化器（简化版，不包含答案详情）"""
    class Meta:
        model = Question
        fields = [
            'id',
            'question_id',
            'title',
            'category',
            'publish_time',
            'location',
            'answer_count',
            'created_at',
        ]
