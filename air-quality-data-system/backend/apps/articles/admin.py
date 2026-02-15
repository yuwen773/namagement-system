from django.contrib import admin

from .models import Article, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sort")
    search_fields = ("name",)
    ordering = ("sort", "id")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "status",
        "is_announcement",
        "sort_order",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "is_announcement", "category")
    search_fields = ("title", "content")

