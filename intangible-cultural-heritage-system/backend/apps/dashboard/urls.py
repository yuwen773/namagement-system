from django.urls import re_path

from .views import (
    DashboardCategoryDistributionView,
    DashboardCountryRankingView,
    DashboardMapDistributionView,
    DashboardOverviewView,
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
]
