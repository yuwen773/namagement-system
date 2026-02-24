from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.analysis.views import AnalysisViewSet

router = DefaultRouter()
router.register("analysis", AnalysisViewSet, basename="analysis")

urlpatterns = [
    path("", include(router.urls)),
]
