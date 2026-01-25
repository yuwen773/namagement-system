from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, CustomTokenObtainPairView, CurrentUserView, AdminResetPasswordView,
    ChangePasswordView, UserListView, UserRoleUpdateView, UserStatusUpdateView,
    UserEditRequestViewSet, RolePermissionViewSet, SystemConfigViewSet
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/reset-password/', AdminResetPasswordView.as_view(), name='reset_password'),
    path('users/<int:user_id>/role/', UserRoleUpdateView.as_view(), name='update_role'),
    path('users/<int:user_id>/status/', UserStatusUpdateView.as_view(), name='update_status'),
]

# ViewSet 路由
router = DefaultRouter()
router.register(r'edit-requests', UserEditRequestViewSet, basename='edit-request')
router.register(r'permissions', RolePermissionViewSet, basename='permission')
router.register(r'system-config', SystemConfigViewSet, basename='system-config')

urlpatterns += router.urls
