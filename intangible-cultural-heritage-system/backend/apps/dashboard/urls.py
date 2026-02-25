from django.urls import re_path

from .views import DashboardOverviewView

urlpatterns = [
    re_path(r"^dashboard/overview/?$", DashboardOverviewView.as_view(), name="dashboard-overview"),
]
