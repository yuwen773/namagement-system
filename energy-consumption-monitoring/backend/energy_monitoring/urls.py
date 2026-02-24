"""energy_monitoring URL Configuration."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.buildings.urls")),
    path("api/", include("apps.devices.urls")),
    path("api/", include("apps.energy.urls")),
    path("api/", include("apps.analysis.urls")),
    path("api/", include("apps.alarms.urls")),
    path("api/", include("apps.system.urls")),
]
