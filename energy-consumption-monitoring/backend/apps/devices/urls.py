from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.devices.views import DeviceViewSet, EnergyTypeViewSet

router = DefaultRouter()
router.register("energy-types", EnergyTypeViewSet, basename="energy-type")
router.register("devices", DeviceViewSet, basename="device")

urlpatterns = [
    path("", include(router.urls)),
]
