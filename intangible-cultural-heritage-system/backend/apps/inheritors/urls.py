from rest_framework.routers import SimpleRouter

from .views import InheritorViewSet

router = SimpleRouter()
router.register(r"inheritors", InheritorViewSet, basename="inheritor")

urlpatterns = router.urls
