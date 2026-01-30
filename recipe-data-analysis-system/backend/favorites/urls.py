"""
收藏模块 - URL 配置

定义收藏相关的 API 路由。
"""
from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    # 收藏/取消收藏菜谱
    path('', views.FavoriteViewSet.as_view({'post': 'create', 'get': 'list'}), name='favorite-list'),
    # 检查收藏状态
    path('check/<int:recipe_id>/', views.check_favorite_status, name='favorite-check'),
    # 取消收藏（通过 URL 路径）
    path('<int:recipe_id>/', views.FavoriteDetailView.as_view(), name='favorite-detail'),
]
