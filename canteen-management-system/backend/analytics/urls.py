"""
统计分析应用 URL 路由配置
"""
from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    # 人员统计接口
    path("employees/", views.employee_statistics, name="employee_statistics"),

    # 考勤统计接口
    path("attendance/", views.attendance_statistics, name="attendance_statistics"),

    # 薪资统计接口
    path("salaries/", views.salary_statistics, name="salary_statistics"),

    # 总览统计接口（Dashboard 首页）
    path("overview/", views.overview_statistics, name="overview_statistics"),
]
