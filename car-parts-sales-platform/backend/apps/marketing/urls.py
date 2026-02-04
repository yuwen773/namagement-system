"""
营销模块 URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, UserCouponViewSet

# 创建路由实例
router = DefaultRouter()
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'user-coupons', UserCouponViewSet, basename='user-coupon')

urlpatterns = [
    path('', include(router.urls)),
]
