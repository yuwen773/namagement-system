"""
分类模块 - 管理员路由配置

定义管理员专用的分类管理 URL 路由。
"""
from django.urls import path
from . import views

app_name = 'admin_categories'

urlpatterns = [
    # 管理员 - 分类管理列表
    path('', views.admin_category_list, name='admin_category_list'),

    # 管理员 - 创建分类
    path('create/', views.admin_create_category, name='admin_create_category'),

    # 管理员 - 更新分类
    path('<int:category_id>/update/', views.admin_update_category, name='admin_update_category'),

    # 管理员 - 删除分类
    path('<int:category_id>/delete/', views.admin_delete_category, name='admin_delete_category'),
]
