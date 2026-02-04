"""
系统模块 URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SystemConfigViewSet, MessageViewSet, OperationLogViewSet

router = DefaultRouter()
router.register(r'configs', SystemConfigViewSet, basename='system-config')
router.register(r'messages', MessageViewSet, basename='system-message')
router.register(r'logs', OperationLogViewSet, basename='system-log')

urlpatterns = [
    path('', include(router.urls)),
]
