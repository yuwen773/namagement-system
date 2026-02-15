from rest_framework import serializers

from .models import Article, ArticleCategory


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = ["id", "name", "sort"]
        read_only_fields = fields


class ArticleListSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "category_id",
            "category_name",
            "is_announcement",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class ArticleDetailSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "category_id",
            "category_name",
            "content",
            "is_announcement",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
