"""
权限检查模块

定义权限检查类和装饰器，用于控制用户访问权限。
"""
from rest_framework import permissions
from utils.constants import UserRole


class IsAdminUser(permissions.BasePermission):
    """
    管理员权限检查类

    只允许管理员角色的用户访问。
    """

    def has_permission(self, request, view):
        """
        检查用户是否有权限访问

        Args:
            request: 请求对象
            view: 视图对象

        Returns:
            bool: 管理员返回 True，否则返回 False
        """
        return request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    管理员或只读权限检查类

    - 管理员可以进行任何操作
    - 普通用户只能进行安全方法（GET、HEAD、OPTIONS）操作
    """

    def has_permission(self, request, view):
        """
        检查用户是否有权限访问

        Args:
            request: 请求对象
            view: 视图对象

        Returns:
            bool: 管理员或只读操作返回 True，否则返回 False
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN
