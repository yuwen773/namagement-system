"""
Analytics 模块 - URL 配置

本模块定义数据分析相关的 API 路由
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # 菜系分布分析
    path('cuisines/', views.CuisineDistributionView.as_view(), name='cuisine-distribution'),
    # 难度等级统计
    path('difficulty/', views.DifficultyStatsView.as_view(), name='difficulty-stats'),
    # 口味偏好分析
    path('flavors/', views.FlavorPreferenceView.as_view(), name='flavor-preference'),
    # 食材使用频率统计
    path('ingredients/', views.IngredientFrequencyView.as_view(), name='ingredient-frequency'),
]
