from rest_framework import permissions


class IsAdminOrOwnerReadWrite(permissions.BasePermission):
    """管理员或本人可读写"""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 管理员可操作所有反馈
        if request.user.role == 'admin':
            return True
        # 普通用户只能查看和删除自己的反馈
        return obj.user == request.user
