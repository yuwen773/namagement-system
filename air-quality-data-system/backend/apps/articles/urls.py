from django.urls import path

from .views import (
    AnnouncementListView,
    ArticleCategoryView,
    ArticleManageView,
    ArticleViewSet,
    CategoryManageView,
)

article_list_view = ArticleViewSet.as_view({"get": "list"})
article_detail_view = ArticleViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("admin/articles/", ArticleManageView.as_view(), name="admin-article-manage"),
    path("admin/categories/", CategoryManageView.as_view(), name="admin-category-manage"),
    path("articles/", article_list_view, name="article-list"),
    path("articles/<int:pk>/", article_detail_view, name="article-detail"),
    path("categories/", ArticleCategoryView.as_view(), name="article-category-list"),
    path("announcements/", AnnouncementListView.as_view(), name="announcement-list"),
]
