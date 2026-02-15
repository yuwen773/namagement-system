from __future__ import annotations

from django.db.models import Q
from django.db.models.deletion import ProtectedError
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from apps.articles.models import Article, ArticleCategory
from apps.articles.serializers import (
    ArticleCategoryManageSerializer,
    ArticleCategorySerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    ArticleManageSerializer,
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


def _parse_int_payload(value, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError("格式错误，应为整数", field=field)


def _raise_serializer_validation_error(errors: dict):
    first_field, first_errors = next(iter(errors.items()))
    if isinstance(first_errors, (list, tuple)) and first_errors:
        message = str(first_errors[0])
    else:
        message = str(first_errors)
    raise ValidationError(message=message, field=str(first_field))


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


class ArticleManageView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Article.objects.select_related("category").all()

        status = (request.query_params.get("status") or "").strip()
        if status:
            queryset = queryset.filter(status=status)

        category_id = request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=_parse_int_payload(category_id, "category_id"))

        is_announcement = request.query_params.get("is_announcement")
        if is_announcement is not None:
            normalized = str(is_announcement).strip().lower()
            if normalized in {"true", "1", "yes"}:
                queryset = queryset.filter(is_announcement=True)
            elif normalized in {"false", "0", "no"}:
                queryset = queryset.filter(is_announcement=False)
            else:
                raise ValidationError("格式错误，应为布尔值", field="is_announcement")

        keyword = (request.query_params.get("keyword") or "").strip()
        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))

        queryset = queryset.order_by("-created_at", "-id")
        page = _parse_int_query_param(request, "page", 1, 1, 100_000)
        page_size = _parse_int_query_param(request, "page_size", 20, 1, 200)
        total = queryset.count()
        items = queryset[(page - 1) * page_size : page * page_size]
        data = ArticleManageSerializer(items, many=True).data
        return APIResponse.paginate(data=data, total=total, page=page, page_size=page_size)

    def post(self, request):
        serializer = ArticleManageSerializer(data=request.data)
        if not serializer.is_valid():
            _raise_serializer_validation_error(serializer.errors)
        instance = serializer.save()
        return APIResponse.success(data=ArticleManageSerializer(instance).data)

    def put(self, request):
        article_id = _parse_int_payload(request.data.get("id"), "id")
        instance = Article.objects.select_related("category").filter(id=article_id).first()
        if instance is None:
            return APIResponse.error(404, "文章不存在")
        serializer = ArticleManageSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            _raise_serializer_validation_error(serializer.errors)
        serializer.save()
        return APIResponse.success(data=ArticleManageSerializer(instance).data)

    def delete(self, request):
        single_id = request.data.get("id")
        id_list = request.data.get("ids")
        if single_id is None and not id_list:
            raise ValidationError("至少提供 id 或 ids", field="id")

        if single_id is not None:
            article_id = _parse_int_payload(single_id, "id")
            queryset = Article.objects.filter(id=article_id)
            if not queryset.exists():
                return APIResponse.error(404, "文章不存在")
            deleted_count, _ = queryset.delete()
            return APIResponse.success(data={"deleted_count": deleted_count}, message="删除成功")

        if not isinstance(id_list, list):
            raise ValidationError("格式错误，应为整数数组", field="ids")
        normalized_ids = []
        for raw in id_list:
            value = _parse_int_payload(raw, "ids")
            if value > 0 and value not in normalized_ids:
                normalized_ids.append(value)
        if not normalized_ids:
            raise ValidationError("至少提供一个有效 id", field="ids")

        deleted_count, _ = Article.objects.filter(id__in=normalized_ids).delete()
        return APIResponse.success(data={"deleted_count": deleted_count}, message="批量删除完成")


class CategoryManageView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = ArticleCategory.objects.all().order_by("sort", "id")
        return APIResponse.success(data=ArticleCategoryManageSerializer(categories, many=True).data)

    def post(self, request):
        serializer = ArticleCategoryManageSerializer(data=request.data)
        if not serializer.is_valid():
            _raise_serializer_validation_error(serializer.errors)
        instance = serializer.save()
        return APIResponse.success(data=ArticleCategoryManageSerializer(instance).data)

    def put(self, request):
        category_id = _parse_int_payload(request.data.get("id"), "id")
        instance = ArticleCategory.objects.filter(id=category_id).first()
        if instance is None:
            return APIResponse.error(404, "分类不存在")
        serializer = ArticleCategoryManageSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            _raise_serializer_validation_error(serializer.errors)
        serializer.save()
        return APIResponse.success(data=ArticleCategoryManageSerializer(instance).data)

    def delete(self, request):
        single_id = request.data.get("id")
        id_list = request.data.get("ids")
        if single_id is None and not id_list:
            raise ValidationError("至少提供 id 或 ids", field="id")

        if single_id is not None:
            category_id = _parse_int_payload(single_id, "id")
            queryset = ArticleCategory.objects.filter(id=category_id)
            if not queryset.exists():
                return APIResponse.error(404, "分类不存在")
            try:
                deleted_count, _ = queryset.delete()
            except ProtectedError:
                raise ValidationError("该分类下存在文章，无法删除", field="id")
            return APIResponse.success(data={"deleted_count": deleted_count}, message="删除成功")

        if not isinstance(id_list, list):
            raise ValidationError("格式错误，应为整数数组", field="ids")
        normalized_ids = []
        for raw in id_list:
            value = _parse_int_payload(raw, "ids")
            if value > 0 and value not in normalized_ids:
                normalized_ids.append(value)
        if not normalized_ids:
            raise ValidationError("至少提供一个有效 id", field="ids")
        try:
            deleted_count, _ = ArticleCategory.objects.filter(id__in=normalized_ids).delete()
        except ProtectedError:
            raise ValidationError("选中的分类中存在已被文章引用项，无法删除", field="ids")
        return APIResponse.success(data={"deleted_count": deleted_count}, message="批量删除完成")
