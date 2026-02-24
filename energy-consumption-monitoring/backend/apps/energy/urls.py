from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.energy.views import EnergyDataViewSet, EnergyStatisticsViewSet

router = DefaultRouter()
router.register("energy-data", EnergyDataViewSet, basename="energy-data")
router.register("energy-statistics", EnergyStatisticsViewSet, basename="energy-statistics")

urlpatterns = [
    path("", include(router.urls)),
]
