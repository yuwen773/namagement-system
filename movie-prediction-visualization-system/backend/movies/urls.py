from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieTypeViewSet, MovieViewSet

router = DefaultRouter()
router.register(r'types', MovieTypeViewSet, basename='movie-type')
router.register(r'', MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
]
