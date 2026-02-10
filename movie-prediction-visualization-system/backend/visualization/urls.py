from django.urls import path
from .views import (
    BoxOfficeTop10View,
    TodayBoxOfficeView,
    WeeklyChampionView,
    TypeBoxOfficeView,
    RegionBoxOfficeView,
    TimeSeriesView,
    DashboardView,
)

urlpatterns = [
    path('stats/top10/', BoxOfficeTop10View.as_view(), name='stats-top10'),
    path('stats/today/', TodayBoxOfficeView.as_view(), name='stats-today'),
    path('stats/champion/', WeeklyChampionView.as_view(), name='stats-champion'),
    path('stats/type/', TypeBoxOfficeView.as_view(), name='stats-type'),
    path('stats/region/', RegionBoxOfficeView.as_view(), name='stats-region'),
    path('stats/timeseries/', TimeSeriesView.as_view(), name='stats-timeseries'),
    path('stats/dashboard/', DashboardView.as_view(), name='stats-dashboard'),
]
