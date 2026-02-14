from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, CinemaViewSet

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'', CinemaViewSet, basename='cinema')

urlpatterns = [
    path('', include(router.urls)),
]
