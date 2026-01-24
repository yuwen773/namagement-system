from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaryCalculateViewSet, SalaryRecordViewSet

router = DefaultRouter()
router.register(r'calculate', SalaryCalculateViewSet, basename='salary-calculate')
router.register(r'records', SalaryRecordViewSet, basename='salary-record')

urlpatterns = [
    path('', include(router.urls)),
]
