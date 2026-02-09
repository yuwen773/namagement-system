from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """仅管理员可访问"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrSelf(permissions.BasePermission):
    """管理员或用户本人可访问"""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.id == request.user.id
