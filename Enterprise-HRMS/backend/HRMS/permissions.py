from rest_framework import permissions
from django.conf import settings


class IsAdmin(permissions.BasePermission):
    """
    仅管理员可访问
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == settings.ROLE_ADMIN


class IsHROrAdmin(permissions.BasePermission):
    """
    人事专员或管理员可访问
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in [settings.ROLE_HR, settings.ROLE_ADMIN]


class IsHROrAdminOrReadOnly(permissions.BasePermission):
    """
    人事专员或管理员可写，其他用户只读
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # 只读请求所有认证用户都可以访问
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写请求需要 HR 或 Admin 权限
        return request.user.role in [settings.ROLE_HR, settings.ROLE_ADMIN]


class IsEmployeeOrHROrAdmin(permissions.BasePermission):
    """
    普通员工可访问自己的人事/考勤数据
    人事专员和管理员可访问所有数据
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        # 管理员和人事可以访问所有记录
        if user.role in [settings.ROLE_ADMIN, settings.ROLE_HR]:
            return True
        # 普通员工只能访问自己的记录
        return obj.user == user


class IsOwnerOrHROrAdmin(permissions.BasePermission):
    """
    对象所有者或 HR/Admin 可访问
    用于员工只能查看/编辑自己的个人信息
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role in [settings.ROLE_ADMIN, settings.ROLE_HR]:
            return True
        return obj.user == user
