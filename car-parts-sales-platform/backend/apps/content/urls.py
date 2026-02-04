"""
内容模块 URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ModificationCaseViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'cases', ModificationCaseViewSet, basename='modification-case')
router.register(r'faqs', FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
]
