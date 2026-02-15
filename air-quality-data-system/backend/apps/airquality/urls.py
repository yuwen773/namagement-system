from django.urls import path

from .views import (
    AQIDistributionView,
    AirQualityOverviewViewSet,
    CityComparisonView,
    CityDetailView,
    CityTrendView,
    CorrelationAnalysisView,
    DataImportUploadView,
    HistoricalDataViewSet,
    ImportTaskDetailView,
    ImportTaskListView,
    ImportTaskLogListView,
    StationDetailView,
    StationTrendView,
)

overview_list_view = AirQualityOverviewViewSet.as_view({"get": "list"})
overview_top_cities_view = AirQualityOverviewViewSet.as_view({"get": "top_cities"})

historical_list_view = HistoricalDataViewSet.as_view({"get": "list"})
historical_export_view = HistoricalDataViewSet.as_view({"get": "export"})

urlpatterns = [
    path("admin/data-import/", DataImportUploadView.as_view(), name="admin-data-import-upload"),
    path("admin/data-import/tasks/", ImportTaskListView.as_view(), name="admin-data-import-task-list"),
    path(
        "admin/data-import/tasks/<str:task_id>/",
        ImportTaskDetailView.as_view(),
        name="admin-data-import-task-detail",
    ),
    path(
        "admin/data-import/tasks/<str:task_id>/logs/",
        ImportTaskLogListView.as_view(),
        name="admin-data-import-task-logs",
    ),
    path("overview/", overview_list_view, name="overview-list"),
    path("overview/top-cities/", overview_top_cities_view, name="overview-top-cities"),
    path("cities/<str:code>/", CityDetailView.as_view(), name="city-detail"),
    path("cities/<str:code>/trend/", CityTrendView.as_view(), name="city-trend"),
    path("stations/<str:code>/", StationDetailView.as_view(), name="station-detail"),
    path("stations/<str:code>/trend/", StationTrendView.as_view(), name="station-trend"),
    path("historical-data/", historical_list_view, name="historical-data-list"),
    path("historical-data/export/", historical_export_view, name="historical-data-export"),
    path("analysis/compare/", CityComparisonView.as_view(), name="analysis-city-compare"),
    path("analysis/correlation/", CorrelationAnalysisView.as_view(), name="analysis-correlation"),
    path("analysis/distribution/", AQIDistributionView.as_view(), name="analysis-distribution"),
]
