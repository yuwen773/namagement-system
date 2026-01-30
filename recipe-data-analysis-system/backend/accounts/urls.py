"""
用户认证路由模块

定义用户认证相关的 URL 路由。
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 用户注册
    path('register/', views.register, name='register'),

    # 用户登录
    path('login/', views.login, name='login'),

    # 健康检查
    path('health/', views.health_check, name='health_check'),
]
