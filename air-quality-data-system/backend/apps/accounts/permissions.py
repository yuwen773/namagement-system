from __future__ import annotations

from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    message = "请先登录"

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return False
        if getattr(user, "is_deleted", False):
            return False
        return bool(getattr(user, "status", True))


class IsAdminUser(IsAuthenticated):
    message = "仅管理员可访问"

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = request.user
        return bool(
            getattr(user, "is_superuser", False)
            or getattr(user, "is_staff", False)
            or getattr(user, "role", "") == "ADMIN"
        )
