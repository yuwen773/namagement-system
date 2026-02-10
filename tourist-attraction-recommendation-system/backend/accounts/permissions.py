from rest_framework.permissions import IsAuthenticated


class IsAdmin(IsAuthenticated):
    """管理员权限"""

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.role == 'ADMIN'
