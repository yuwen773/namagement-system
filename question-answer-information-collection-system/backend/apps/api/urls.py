"""
爬虫 API URL 配置

提供爬虫任务的状态查询、启动、停止、日志获取等接口。
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CrawlerStatusView,
    CrawlerStartView,
    CrawlerStopView,
    CrawlerDownloadView,
    CrawlerProgressView,
    CrawlerLogsView,
    CrawlerResumeView,
    CrawlerOperationLogsView,
    QuestionViewSet,
    QuestionFilterOptionsView,
    StatisticsTrendView,
    StatisticsCategoriesView,
    StatisticsAnswerersView,
    StatisticsOverviewView,
    StatisticsLocationView,
    StatisticsHotQuestionsView,
    StatisticsAnswerDistributionView,
)

app_name = 'crawler'

# DRF 路由器，用于注册 ViewSet
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    # 爬虫状态查询
    path('crawler/status/', CrawlerStatusView.as_view(), name='crawler-status'),

    # 启动爬虫任务
    path('crawler/start/', CrawlerStartView.as_view(), name='crawler-start'),

    # 停止爬虫任务
    path('crawler/stop/', CrawlerStopView.as_view(), name='crawler-stop'),

    # 下载爬取的 CSV 文件
    path('crawler/download/', CrawlerDownloadView.as_view(), name='crawler-download'),

    # 获取任务进度
    path('crawler/progress/<str:task_id>/', CrawlerProgressView.as_view(), name='crawler-progress'),

    # 获取任务日志
    path('crawler/logs/<str:task_id>/', CrawlerLogsView.as_view(), name='crawler-logs'),

    # 获取断点信息
    path('crawler/resume/', CrawlerResumeView.as_view(), name='crawler-resume'),

    # 获取操作日志
    path('crawler/operation-logs/', CrawlerOperationLogsView.as_view(), name='crawler-operation-logs'),

    # 统计分析 API
    path('statistics/overview/', StatisticsOverviewView.as_view(), name='statistics-overview'),
    path('statistics/trend/', StatisticsTrendView.as_view(), name='statistics-trend'),
    path('statistics/categories/', StatisticsCategoriesView.as_view(), name='statistics-categories'),
    path('statistics/answerers/', StatisticsAnswerersView.as_view(), name='statistics-answerers'),
    path('statistics/locations/', StatisticsLocationView.as_view(), name='statistics-locations'),
    path('statistics/hot-questions/', StatisticsHotQuestionsView.as_view(), name='statistics-hot-questions'),
    path('statistics/answer-distribution/', StatisticsAnswerDistributionView.as_view(), name='statistics-answer-distribution'),

    # 问答筛选选项 API
    path('questions/filter-options/', QuestionFilterOptionsView.as_view(), name='question-filter-options'),
]

# 添加 ViewSet 路由
urlpatterns += router.urls
