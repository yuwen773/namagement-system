from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    ChangePasswordView,
    DeleteAccountView,
)

urlpatterns = [
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    # 登录
    path('login/', LoginView.as_view(), name='login'),
    # 刷新 Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 个人信息
    path('profile/', UserProfileView.as_view(), name='profile'),
    # 修改密码
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    # 注销账号
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
