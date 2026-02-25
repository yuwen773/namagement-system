from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.analysis.views import AchievementViewSet, AnalysisViewSet

router = DefaultRouter()
router.register("analysis", AnalysisViewSet, basename="analysis")
router.register("analysis/achievements", AchievementViewSet, basename="analysis-achievement")

urlpatterns = [
    path("", include(router.urls)),
]
