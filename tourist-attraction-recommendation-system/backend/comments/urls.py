from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, FavoriteViewSet

router = DefaultRouter()
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register('', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
