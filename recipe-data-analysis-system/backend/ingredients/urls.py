"""
食材模块 - URL 路由配置

定义食材相关的 API 路由
"""
from django.urls import path
from . import views

app_name = 'ingredients'

urlpatterns = [
    # 食材列表接口
    path('', views.ingredient_list, name='ingredient-list'),
]
