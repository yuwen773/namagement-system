from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, CustomTokenObtainPairView, AdminResetPasswordView,
    UserListView, UserRoleUpdateView, UserStatusUpdateView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/reset-password/', AdminResetPasswordView.as_view(), name='reset_password'),
    path('users/<int:user_id>/role/', UserRoleUpdateView.as_view(), name='update_role'),
    path('users/<int:user_id>/status/', UserStatusUpdateView.as_view(), name='update_status'),
]
