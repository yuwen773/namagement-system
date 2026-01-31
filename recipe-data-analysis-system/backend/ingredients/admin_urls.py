"""
食材模块 - 管理员路由配置

定义管理员专用的食材管理 URL 路由。
"""
from django.urls import path
from . import views

app_name = 'admin_ingredients'

urlpatterns = [
    # 管理员 - 食材管理列表
    path('', views.admin_ingredient_list, name='admin_ingredient_list'),

    # 管理员 - 创建食材
    path('create/', views.admin_create_ingredient, name='admin_create_ingredient'),

    # 管理员 - 更新食材
    path('<int:ingredient_id>/update/', views.admin_update_ingredient, name='admin_update_ingredient'),

    # 管理员 - 删除食材
    path('<int:ingredient_id>/delete/', views.admin_delete_ingredient, name='admin_delete_ingredient'),
]
