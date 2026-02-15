from django.urls import path

from .views import LoginView, RegisterView, UserManageView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("admin/users/", UserManageView.as_view(), name="admin-user-manage"),
]
