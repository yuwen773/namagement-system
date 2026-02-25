from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import get_user_role


def is_admin_user(user):
    if not user or not user.is_authenticated:
        return False
    return user.is_superuser or get_user_role(user) == "admin"


class IsAdmin(BasePermission):
    message = "仅管理员可执行该操作。"

    def has_permission(self, request, view):
        return is_admin_user(request.user)


class IsAdminOrReadOnly(BasePermission):
    message = "仅管理员可修改数据。"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return is_admin_user(request.user)
