from __future__ import annotations

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.articles.models import Article, ArticleCategory
from apps.articles.serializers import (
    ArticleCategorySerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
)
from utils.exception_handler import ValidationError
from utils.response import APIResponse


def _parse_int_query_param(request, field: str, default: int, min_value: int, max_value: int) -> int:
    raw_value = request.query_params.get(field, str(default))
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        raise ValidationError(f"格式错误，应为整数，范围 {min_value}-{max_value}", field=field)
    if value < min_value or value > max_value:
        raise ValidationError(f"超出范围，应为 {min_value}-{max_value}", field=field)
    return value


class ArticleViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Article.objects.filter(status=Article.Status.PUBLISHED).select_related("category")
        category_id = request.query_params.get("category_id")
        if category_id:
            try:
                category_id_int = int(category_id)
            except ValueError:
                raise ValidationError("格式错误，应为整数", field="category_id")
            queryset = queryset.filter(category_id=category_id_int)
        queryset = queryset.filter(is_announcement=False).order_by("-created_at", "-id")

        page = _parse_int_query_param(request, "page", 1, 1, 100_000)
        page_size = _parse_int_query_param(request, "page_size", 20, 1, 200)

        total = queryset.count()
        items = queryset[(page - 1) * page_size : page * page_size]
        data = ArticleListSerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)

    def retrieve(self, request, pk=None):
        article = (
            Article.objects.filter(pk=pk, status=Article.Status.PUBLISHED, is_announcement=False)
            .select_related("category")
            .first()
        )
        if article is None:
            return APIResponse.error(404, "文章不存在")
        return APIResponse.success(data=ArticleDetailSerializer(article).data)


class ArticleCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = ArticleCategory.objects.all().order_by("sort", "id")
        return APIResponse.success(data=ArticleCategorySerializer(categories, many=True).data)


class AnnouncementListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        limit = _parse_int_query_param(request, "limit", 5, 5, 10)
        queryset = (
            Article.objects.filter(status=Article.Status.PUBLISHED, is_announcement=True)
            .select_related("category")
            .order_by("sort_order", "-created_at", "-id")
        )[:limit]
        data = ArticleListSerializer(queryset, many=True).data
        return APIResponse.success(data=data)
