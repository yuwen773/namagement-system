from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    用户账号管理后台
    """
    list_display = ['id', 'username', 'role', 'status', 'employee_id', 'created_at']
    list_filter = ['role', 'status', 'created_at']
    search_fields = ['username', 'id']
    list_per_page = 20
    ordering = ['-created_at']

    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'password')
        }),
        ('角色与状态', {
            'fields': ('role', 'status', 'employee_id')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']
