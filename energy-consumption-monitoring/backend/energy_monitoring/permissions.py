from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.accounts.models import UserRole


def is_admin_user(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profile = getattr(user, "profile", None)
    return bool(profile and profile.role == UserRole.ADMIN)


class IsAdmin(BasePermission):
    message = "仅管理员可执行该操作。"

    def has_permission(self, request, view):
        return is_admin_user(request.user)


class IsAdminOrReadOnly(BasePermission):
    message = "仅管理员可执行写操作。"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return is_admin_user(request.user)


class IsOwnerOrAdmin(BasePermission):
    message = "仅资源所有者或管理员可访问。"

    def has_object_permission(self, request, view, obj):
        if is_admin_user(request.user):
            return True
        owner = getattr(obj, "user", None)
        return owner == request.user
