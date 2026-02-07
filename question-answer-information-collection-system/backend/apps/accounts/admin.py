from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """用户管理后台配置"""

    list_display = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']
    list_per_page = 20

    # _fieldsets 用于组织详情页字段分组
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('个人信息', {
            'fields': ('email', 'first_name', 'last_name')
        }),
        ('权限控制', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('时间信息', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('last_login', 'date_joined')


# 移除 Django 默认的 Group 注册（如果不需要）
admin.site.unregister(Group)
