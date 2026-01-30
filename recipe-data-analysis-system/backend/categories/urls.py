"""
分类模块 - URL 配置

定义分类相关的 API 路由
"""
from django.urls import path
from .views import category_list, category_by_type

app_name = 'categories'

urlpatterns = [
    # 分类列表（支持类型筛选）
    path('', category_list, name='list'),
    # 按类型获取分类
    path('<str:category_type>/', category_by_type, name='by-type'),
]
