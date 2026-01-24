from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, PostViewSet

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="department")
router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
