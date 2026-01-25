from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerformanceReviewViewSet, PerformanceTemplateViewSet

router = DefaultRouter()
router.register(r'performance/reviews', PerformanceReviewViewSet, basename='performance-review')
router.register(r'performance/templates', PerformanceTemplateViewSet, basename='performance-template')

urlpatterns = [
    path('', include(router.urls)),
]
