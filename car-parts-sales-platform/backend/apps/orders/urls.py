"""
订单模块 URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, ReturnRequestViewSet, CartViewSet

# 注册路由
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'returns', ReturnRequestViewSet, basename='return-request')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
