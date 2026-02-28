from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    PasswordChangeView,
    UserListView,
    UserDetailView,
    UserStatusView,
    UserResetPasswordView,
    SystemConfigListView,
    SystemConfigDetailView,
    CrawlerConfigView,
    TestCookieView
)

app_name = 'users'

urlpatterns = [
    # 认证相关（无需token）
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # 个人信息（需要token）
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),

    # 管理员功能
    path('', UserListView.as_view(), name='user_list'),
    path('<uuid:id>/', UserDetailView.as_view(), name='user_detail'),
    path('<uuid:id>/status/', UserStatusView.as_view(), name='user_status'),
    path('<uuid:id>/reset-password/', UserResetPasswordView.as_view(), name='reset_password'),

    # 系统配置（管理员）
    path('configs/', SystemConfigListView.as_view(), name='config_list'),
    path('configs/crawler/', CrawlerConfigView.as_view(), name='crawler_config'),
    path('configs/crawler/test-cookie/', TestCookieView.as_view(), name='test_cookie'),
    path('configs/<str:key>/', SystemConfigDetailView.as_view(), name='config_detail'),
]
