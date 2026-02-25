from django.urls import re_path

from .views import DashboardMapDistributionView, DashboardOverviewView

urlpatterns = [
    re_path(r"^dashboard/overview/?$", DashboardOverviewView.as_view(), name="dashboard-overview"),
    re_path(
        r"^dashboard/map-distribution/?$",
        DashboardMapDistributionView.as_view(),
        name="dashboard-map-distribution",
    ),
]
