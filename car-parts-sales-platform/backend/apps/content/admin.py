"""
内容管理 - Django Admin 配置
"""
from django.contrib import admin
from .models import ModificationCase, FAQ


@admin.register(ModificationCase)
class ModificationCaseAdmin(admin.ModelAdmin):
    """改装案例管理后台"""

    list_display = [
        'title', 'author', 'status', 'view_count',
        'sort_order', 'published_at', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'published_at']
    search_fields = ['title', 'summary', 'content', 'author']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'summary', 'author', 'status')
        }),
        ('内容', {
            'fields': ('content', 'cover_image')
        }),
        ('配置', {
            'fields': ('sort_order', 'view_count', 'published_at')
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ['-sort_order', '-created_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """常见问题管理后台"""

    list_display = [
        'question', 'category', 'sort_order',
        'is_active', 'created_at'
    ]
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('question', 'answer', 'category')
        }),
        ('配置', {
            'fields': ('sort_order', 'is_active')
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ['category', 'sort_order', '-created_at']
