from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """公告管理后台"""

    list_display = ['title', 'priority_display', 'status_display', 'is_pinned', 'created_by', 'published_at', 'created_at']
    list_filter = ['status', 'priority', 'is_pinned']
    search_fields = ['title', 'content']
    ordering = ['-is_pinned', '-priority', '-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by']

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'content', 'priority', 'status', 'is_pinned')
        }),
        ('元信息', {
            'fields': ('id', 'created_by', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """保存时自动设置创建人"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def priority_display(self, obj):
        """优先级显示"""
        return obj.get_priority_display()
    priority_display.short_description = '优先级'

    def status_display(self, obj):
        """状态显示"""
        return obj.get_status_display()
    status_display.short_description = '状态'
