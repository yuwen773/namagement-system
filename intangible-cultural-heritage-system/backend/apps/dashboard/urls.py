from django.urls import re_path

from .views import (
    DashboardCategoryDistributionView,
    DashboardCountryRankingView,
    DashboardKeywordCloudView,
    DashboardLevelDistributionView,
    DashboardMapDistributionView,
    DashboardOverviewView,
    DashboardTrendView,
)

urlpatterns = [
    re_path(r"^dashboard/overview/?$", DashboardOverviewView.as_view(), name="dashboard-overview"),
    re_path(
        r"^dashboard/map-distribution/?$",
        DashboardMapDistributionView.as_view(),
        name="dashboard-map-distribution",
    ),
    re_path(
        r"^dashboard/category-distribution/?$",
        DashboardCategoryDistributionView.as_view(),
        name="dashboard-category-distribution",
    ),
    re_path(
        r"^dashboard/country-ranking/?$",
        DashboardCountryRankingView.as_view(),
        name="dashboard-country-ranking",
    ),
    re_path(
        r"^dashboard/trend/?$",
        DashboardTrendView.as_view(),
        name="dashboard-trend",
    ),
    re_path(
        r"^dashboard/level-distribution/?$",
        DashboardLevelDistributionView.as_view(),
        name="dashboard-level-distribution",
    ),
    re_path(
        r"^dashboard/keyword-cloud/?$",
        DashboardKeywordCloudView.as_view(),
        name="dashboard-keyword-cloud",
    ),
]
