"""
用户模块 URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet, UserAddressViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
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
