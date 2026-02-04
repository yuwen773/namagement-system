"""
用户模块 URL Configuration

用户管理相关路由（不包含认证接口）
认证接口已分离到 auth_urls.py
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserAddressViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    # 地址管理接口
    path('addresses/', UserAddressViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='address-list'),
    path('addresses/<int:pk>/', UserAddressViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='address-detail'),
    path('addresses/<int:pk>/set-default/', UserAddressViewSet.as_view({
        'post': 'set_default'
    }), name='address-set-default'),
]
