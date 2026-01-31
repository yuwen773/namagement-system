"""
Admin Panel 模块 - 管理员路由配置

本模块定义管理员仪表盘相关的 URL 路由。
"""
from django.urls import path
from .views import DashboardOverviewView, DashboardTrendsView, DashboardBehaviorsView

app_name = 'admin_panel'

urlpatterns = [
    # 数据总览接口
    path('overview/', DashboardOverviewView.as_view(), name='dashboard_overview'),

    # 数据趋势接口
    path('trends/', DashboardTrendsView.as_view(), name='dashboard_trends'),

    # 用户行为统计接口
    path('behaviors/', DashboardBehaviorsView.as_view(), name='dashboard_behaviors'),
]
