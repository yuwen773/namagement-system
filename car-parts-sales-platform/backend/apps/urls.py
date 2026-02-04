"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 各模块的路由将在对应的 apps 中定义
# 这里统一引用所有模块的 urls

urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('users/', include('apps.users.urls')),
    path('products/', include('apps.products.urls')),
    path('orders/', include('apps.orders.urls')),
    path('marketing/', include('apps.marketing.urls')),
    path('recommendations/', include('apps.recommendations.urls')),
    path('content/', include('apps.content.urls')),
    path('system/', include('apps.system.urls')),
]
