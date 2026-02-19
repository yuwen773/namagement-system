from django.urls import path

from .views import ErrorLogListView, OperationLogListView, SystemLogListView

urlpatterns = [
    path("admin/logs/operations/", OperationLogListView.as_view(), name="admin-operation-log-list"),
    path("admin/logs/errors/", ErrorLogListView.as_view(), name="admin-error-log-list"),
    path("admin/logs/system/", SystemLogListView.as_view(), name="admin-system-log-list"),
]
