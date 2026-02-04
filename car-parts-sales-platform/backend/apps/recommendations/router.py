"""
推荐模块路由配置
"""
from rest_framework.routers import DefaultRouter
from .views import RecommendationRuleViewSet, RecommendedProductViewSet

router = DefaultRouter()
router.register(r'rules', RecommendationRuleViewSet, basename='recommendation-rule')
router.register(r'products', RecommendedProductViewSet, basename='recommended-product')
