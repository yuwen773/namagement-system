"""
URL configuration for accounts app.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserDetailView, UserListView
from .serializers import CustomTokenObtainPairSerializer

# ViewSet 路由
router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')
router.register(r'users', UserListView, basename='users')
router.register(r'me', UserDetailView, basename='me')

urlpatterns = [
    # JWT Token endpoints - 使用自定义序列化器返回用户信息
    path(
        "token/",
        TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer),
        name="token_obtain_pair"
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # 登出（客户端删除 Token 即可，服务器端无需处理）
]

# 添加 ViewSet 路由
urlpatterns += router.urls
