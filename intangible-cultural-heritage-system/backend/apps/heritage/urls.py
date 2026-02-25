from rest_framework.routers import SimpleRouter

from .views import HeritageItemViewSet

router = SimpleRouter()
router.register(r"heritage", HeritageItemViewSet, basename="heritage")

urlpatterns = router.urls
