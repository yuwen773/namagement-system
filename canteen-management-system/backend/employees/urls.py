from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeProfileViewSet, UnassignedEmployeeViewSet

router = DefaultRouter()
router.register(r'unassigned', UnassignedEmployeeViewSet, basename='unassigned-employee')
router.register(r'', EmployeeProfileViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]
