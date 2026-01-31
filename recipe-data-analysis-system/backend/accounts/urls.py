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

    # 获取当前用户信息（需要认证）
    path('me/', views.me, name='me'),

    # 修改密码（需要认证）
    path('password/', views.change_password, name='change_password'),

    # 角色检查（需要认证，用于测试权限）
    path('role-check/', views.role_check, name='role_check'),

    # 管理员统计（仅管理员可访问）
    path('admin/stats/', views.admin_stats, name='admin_stats'),

    # 用户列表（仅管理员可访问）
    path('admin/users/', views.user_list, name='user_list'),

    # 封禁/解封用户（仅管理员可访问）
    path('admin/users/<int:user_id>/ban/', views.ban_user, name='ban_user'),
    path('admin/users/<int:user_id>/unban/', views.unban_user, name='unban_user'),

    # 健康检查
    path('health/', views.health_check, name='health_check'),
]
