"""
预测模块 URL 配置
"""

from django.urls import path
from .views import (
    MoviePredictionView,
    PredictionHistoryView,
    PredictionAlgorithmsView,
)

urlpatterns = [
    # 影片预测接口
    path('movie/<int:movie_id>/', MoviePredictionView.as_view(), name='movie-prediction'),
    # 历史数据接口
    path('movie/<int:movie_id>/history/', PredictionHistoryView.as_view(), name='prediction-history'),
    # 算法列表接口
    path('algorithms/', PredictionAlgorithmsView.as_view(), name='prediction-algorithms'),
]
