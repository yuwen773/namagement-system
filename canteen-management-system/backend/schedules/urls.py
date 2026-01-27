from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShiftViewSet, ScheduleViewSet, ShiftSwapRequestViewSet

# 创建路由器
router = DefaultRouter()

# 注册视图集
router.register(r'shifts', ShiftViewSet, basename='shift')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'shift-requests', ShiftSwapRequestViewSet, basename='shift-request')

urlpatterns = [
    path('', include(router.urls)),
]
