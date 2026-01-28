from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SalaryRecordViewSet, AppealViewSet


# 创建路由器
router = DefaultRouter()

# 注册薪资记录视图集
router.register(r'salaries', SalaryRecordViewSet, basename='salary-record')

# 注册异常申诉视图集
router.register(r'appeals', AppealViewSet, basename='appeal')

# URL 配置
urlpatterns = [
    path('', include(router.urls)),
]
