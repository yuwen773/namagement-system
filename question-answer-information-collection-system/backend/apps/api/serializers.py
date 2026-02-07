"""
问答数据 API 序列化器

提供 Question 和 Tag 数据的序列化/反序列化支持。
"""

from rest_framework import serializers
from apps.crawler.models import Question, Tag


class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at', 'question_count']

    def get_question_count(self, obj):
        return obj.questions.count()


class QuestionSerializer(serializers.ModelSerializer):
    """问答数据序列化器"""
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )

    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'description',
            'answer_content',
            'answer_time',
            'answerer',
            'tags',
            'tags_ids',
            'source_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
