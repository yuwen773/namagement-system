"""
菜谱模块 - 路由配置

定义菜谱相关的 URL 路由。
"""
from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # 菜谱列表
    path('', views.recipe_list, name='recipe_list'),

    # 菜谱搜索
    path('search/', views.recipe_search, name='recipe_search'),

    # 热门菜谱
    path('hot/', views.hot_recipes, name='hot_recipes'),

    # 菜谱详情
    path('<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),

    # 图片上传（通用上传接口）
    path('upload-image/', views.upload_image, name='upload_image'),

    # 菜谱图片上传（指定菜谱ID）
    path('<int:recipe_id>/upload-image/', views.upload_recipe_image, name='upload_recipe_image'),

    # 健康检查
    path('health/', views.health_check, name='health_check'),
]
