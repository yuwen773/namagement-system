from django.urls import re_path

from .views import LoginView, LogoutView, ProfileView, RefreshTokenView

urlpatterns = [
    re_path(r"^login/?$", LoginView.as_view(), name="auth-login"),
    re_path(r"^refresh/?$", RefreshTokenView.as_view(), name="auth-refresh"),
    re_path(r"^logout/?$", LogoutView.as_view(), name="auth-logout"),
    re_path(r"^me/?$", ProfileView.as_view(), name="auth-me"),
]
