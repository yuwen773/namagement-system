from rest_framework import serializers

from .models import Article, ArticleCategory


class ArticleCategorySerializer(serializers.ModelSerializer):
    """用于用户端的分类序列化器，包含文章计数"""
    article_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ArticleCategory
        fields = ["id", "name", "sort", "article_count"]
        read_only_fields = fields

    def get_article_count(self, obj):
        """获取该分类下已发布的非公告文章数量"""
        return Article.objects.filter(
            category=obj,
            status=Article.Status.PUBLISHED,
            is_announcement=False
        ).count()


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


class ArticleCategoryManageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        error_messages={
            "required": "请输入分类名称",
            "blank": "分类名称不能为空",
            "max_length": "分类名称长度不能超过100字"
        }
    )
    sort = serializers.IntegerField(
        required=False,
        error_messages={"invalid": "排序值格式错误，请输入整数"}
    )

    class Meta:
        model = ArticleCategory
        fields = ["id", "name", "sort"]

    def validate_name(self, value):
        """检查分类名称是否已存在"""
        instance = self.instance
        queryset = ArticleCategory.objects.filter(name=value)
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("该分类名称已存在，请使用其他名称")
        return value


class ArticleManageSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=ArticleCategory.objects.all(),
        error_messages={
            "required": "请选择文章分类",
            "null": "请选择文章分类",
            "does_not_exist": "所选分类不存在，请重新选择有效的分类"
        }
    )
    category_name = serializers.CharField(source="category.name", read_only=True)
    title = serializers.CharField(
        max_length=255,
        error_messages={
            "required": "请输入文章标题",
            "blank": "文章标题不能为空",
            "max_length": "标题过长，请控制在255字以内"
        }
    )
    content = serializers.CharField(
        error_messages={"required": "请输入文章内容", "blank": "文章内容不能为空"}
    )
    status = serializers.ChoiceField(
        choices=[True, False],
        error_messages={"required": "请选择文章状态", "invalid_choice": "文章状态无效"}
    )
    is_announcement = serializers.BooleanField(
        required=False,
        error_messages={"invalid": "是否公告格式错误"}
    )
    sort_order = serializers.IntegerField(
        required=False,
        error_messages={"invalid": "排序值格式错误，请输入整数"}
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "category_id",
            "category_name",
            "content",
            "status",
            "is_announcement",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "category_name", "created_at", "updated_at"]
