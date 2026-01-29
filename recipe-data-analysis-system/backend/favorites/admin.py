"""
收藏模块 - Django Admin 配置

本模块配置用户收藏模型在 Django Admin 后台的显示方式。
"""
from django.contrib import admin
from .models import UserFavorite


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    """用户收藏管理界面"""

    list_display = [
        'id',
        'user',
        'recipe',
        'created_at'
    ]

    list_filter = [
        'created_at'
    ]

    search_fields = [
        'user__username',
        'recipe__name'
    ]

    readonly_fields = [
        'created_at'
    ]

    ordering = ['-created_at']

    # 每页显示数量
    list_per_page = 20

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'recipe')
