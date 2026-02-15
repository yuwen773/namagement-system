from django.urls import path

from .views import UserManageView

urlpatterns = [
    path("admin/users/", UserManageView.as_view(), name="admin-user-manage"),
]
