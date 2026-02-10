from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoxOfficeRecordViewSet, BoxOfficeStatsView

router = DefaultRouter()
router.register(r'boxoffice', BoxOfficeRecordViewSet, basename='boxoffice')

urlpatterns = [
    path('', include(router.urls)),
    path('boxoffice/stats/', BoxOfficeStatsView.as_view(), name='boxoffice-stats'),
]
