from rest_framework.routers import SimpleRouter

from .views import RegionViewSet

router = SimpleRouter()
router.register(r"regions", RegionViewSet, basename="region")

urlpatterns = router.urls
