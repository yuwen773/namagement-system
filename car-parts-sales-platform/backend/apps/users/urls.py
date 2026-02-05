"""
用户模块 URL Configuration

用户管理相关路由（不包含认证接口）
认证接口已分离到 auth_urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserAddressViewSet, BrowsingHistoryViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'addresses', UserAddressViewSet, basename='address')
router.register(r'browsing-history', BrowsingHistoryViewSet, basename='browsing-history')

urlpatterns = [
    path('', include(router.urls)),
]
