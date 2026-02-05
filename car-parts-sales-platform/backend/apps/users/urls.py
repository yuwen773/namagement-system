"""
用户模块 URL Configuration

用户管理相关路由（不包含认证接口）
认证接口已分离到 auth_urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, UserAddressViewSet, BrowsingHistoryViewSet

# 为 UserViewSet 使用单独的路由器，避免与其他 ViewSet 冲突
user_router = SimpleRouter()
user_router.register(r'', UserViewSet, basename='user')

# 其他资源使用 SimpleRouter，避免覆盖 UserViewSet 的 list 视图
resource_router = SimpleRouter()
resource_router.register(r'addresses', UserAddressViewSet, basename='address')
resource_router.register(r'browsing-history', BrowsingHistoryViewSet, basename='browsing-history')

urlpatterns = [
    path('', include(resource_router.urls)),
    path('', include(user_router.urls)),
]
