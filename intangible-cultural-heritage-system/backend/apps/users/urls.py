from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import (
    CheckEmailView,
    CheckUsernameView,
    LoginView,
    LogoutView,
    ProfileView,
    RefreshTokenView,
    RegisterView,
    UserViewSet,
)

# Router for ViewSets
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    re_path(r"^login/?$", LoginView.as_view(), name="auth-login"),
    re_path(r"^refresh/?$", RefreshTokenView.as_view(), name="auth-refresh"),
    re_path(r"^logout/?$", LogoutView.as_view(), name="auth-logout"),
    re_path(r"^me/?$", ProfileView.as_view(), name="auth-me"),
    re_path(r"^register/?$", RegisterView.as_view(), name="auth-register"),
    re_path(r"^check-username/?$", CheckUsernameView.as_view(), name="auth-check-username"),
    re_path(r"^check-email/?$", CheckEmailView.as_view(), name="auth-check-email"),
]

# Add router URLs
urlpatterns += router.urls
