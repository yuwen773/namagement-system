from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """反馈建议管理后台"""
    list_display = ['id', 'title', 'user', 'feedback_type', 'status', 'created_at', 'replied_at']
    list_filter = ['feedback_type', 'status', 'created_at']
    search_fields = ['title', 'content', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'replied_at']

    fieldsets = (
        ('基础信息', {
            'fields': ('title', 'content', 'feedback_type', 'user')
        }),
        ('处理状态', {
            'fields': ('status', 'admin_reply', 'replied_at', 'replied_by')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # 如果管理员添加回复且之前没有回复，记录回复人和时间
        if obj.admin_reply and not obj.replied_at:
            obj.replied_by = request.user
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)
