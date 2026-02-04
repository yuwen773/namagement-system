"""
认证模块 URL Configuration
单独的认证路由，避免与用户管理路由混淆
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet

router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
