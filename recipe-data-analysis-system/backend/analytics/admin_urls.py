"""
Analytics 模块 - 管理员路由配置

定义管理员专用的数据分析 URL 路由。
"""
from django.urls import path
from . import views

app_name = 'admin_analytics'

urlpatterns = [
    # 管理员 - 菜系深度分析
    path('cuisines/', views.AdminCuisineAnalysisView.as_view(), name='admin_cuisine_analysis'),
    # 管理员 - 难度深度分析
    path('difficulty/', views.AdminDifficultyAnalysisView.as_view(), name='admin_difficulty_analysis'),
    # 管理员 - 热门菜谱分析
    path('hot/', views.AdminHotRecipeAnalysisView.as_view(), name='admin_hot_recipe_analysis'),
    # 管理员 - 食材关联分析
    path('ingredient-pairs/', views.AdminIngredientPairsAnalysisView.as_view(), name='admin_ingredient_pairs_analysis'),
]
