"""
推荐应用 URL 配置

URL 路由:
- GET /api/recommendations/popular/ - 热门推荐
- GET /api/recommendations/personalized/ - 个性化推荐
- GET /api/recommendations/similar/{attraction_id}/ - 相似推荐
"""

from django.urls import path
from .views import (
    PopularRecommendView,
    PersonalizedRecommendView,
    SimilarRecommendView
)

app_name = 'recommendations'

urlpatterns = [
    path('popular/', PopularRecommendView.as_view(), name='popular'),
    path('personalized/', PersonalizedRecommendView.as_view(), name='personalized'),
    path('similar/<int:attraction_id>/', SimilarRecommendView.as_view(), name='similar'),
]
