from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """仅管理员可访问"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsUserOrAdmin(permissions.BasePermission):
    """用户本人或管理员可访问"""
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            # 管理员可以访问所有用户资源
            if request.user.is_admin:
                return True
            # 普通用户只能访问自己的资源
            return obj.id == request.user.id
        return False
