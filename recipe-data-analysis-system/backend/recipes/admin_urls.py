"""
菜谱模块 - 管理员路由配置

定义管理员专用的菜谱管理 URL 路由。
"""
from django.urls import path
from . import views

app_name = 'admin_recipes'

urlpatterns = [
    # 管理员 - 菜谱管理列表
    path('', views.admin_recipe_list, name='admin_recipe_list'),

    # 管理员 - 创建菜谱
    path('create/', views.admin_create_recipe, name='admin_create_recipe'),

    # 管理员 - 批量导入菜谱
    path('import/', views.admin_import_recipes, name='admin_import_recipes'),

    # 管理员 - 更新菜谱
    path('<int:recipe_id>/update/', views.admin_update_recipe, name='admin_update_recipe'),

    # 管理员 - 删除菜谱
    path('<int:recipe_id>/delete/', views.admin_delete_recipe, name='admin_delete_recipe'),
]
