from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.buildings.views import BuildingViewSet, CampusViewSet, FloorViewSet, RoomViewSet

router = DefaultRouter()
router.register("campuses", CampusViewSet, basename="campus")
router.register("buildings", BuildingViewSet, basename="building")
router.register("floors", FloorViewSet, basename="floor")
router.register("rooms", RoomViewSet, basename="room")

urlpatterns = [
    path("", include(router.urls)),
]
