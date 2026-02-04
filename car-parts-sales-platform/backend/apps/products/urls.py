"""
商品模块 URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductImageViewSet, ProductAttributeViewSet

# 创建路由实例
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'images', ProductImageViewSet, basename='product-image')
router.register(r'attributes', ProductAttributeViewSet, basename='product-attribute')

urlpatterns = [
    path('', include(router.urls)),
]
