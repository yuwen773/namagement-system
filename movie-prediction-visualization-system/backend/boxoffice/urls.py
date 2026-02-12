from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoxOfficeRecordViewSet, BoxOfficeStatsView

router = DefaultRouter()
router.register(r'', BoxOfficeRecordViewSet, basename='boxoffice')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', BoxOfficeStatsView.as_view(), name='boxoffice-stats'),
]
