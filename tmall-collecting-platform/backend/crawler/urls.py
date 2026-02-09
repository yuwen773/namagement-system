"""
URL configuration for crawler module.
爬虫模块的路由配置
"""
from django.urls import path
from . import views

app_name = 'crawler'

urlpatterns = [
    # 爬虫控制
    path('start/', views.CrawlerStartView.as_view(), name='crawler-start'),
    path('status/<str:task_id>/', views.CrawlerStatusView.as_view(), name='crawler-status'),
    path('stop/<str:task_id>/', views.CrawlerStopView.as_view(), name='crawler-stop'),

    # 采集日志
    path('logs/', views.CrawlLogListView.as_view(), name='crawl-log-list'),
    path('logs/<uuid:id>/', views.CrawlLogDetailView.as_view(), name='crawl-log-detail'),

    # 爬虫统计
    path('stats/', views.CrawlerStatsView.as_view(), name='crawler-stats'),

    # 系统健康检查
    path('system-health/', views.SystemHealthView.as_view(), name='system-health'),
]
