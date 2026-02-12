from django.urls import path
from .views import (
    AttractionHotView,
    MonthlyReportView,
    DashboardView,
    UserManageView,
    UserStatusView
)

urlpatterns = [
    # 景点热度统计
    path('hot/', AttractionHotView.as_view(), name='statistics-hot'),

    # 月度数据统计
    path('monthly/', MonthlyReportView.as_view(), name='statistics-monthly'),

    # 数据看板
    path('dashboard/', DashboardView.as_view(), name='statistics-dashboard'),

    # 用户管理列表
    path('users/', UserManageView.as_view(), name='statistics-users'),

    # 用户状态管理
    path('users/<int:user_id>/status/', UserStatusView.as_view(), name='statistics-user-status'),
]
