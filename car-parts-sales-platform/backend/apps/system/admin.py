"""
系统管理 - Django Admin 配置
"""
from django.contrib import admin
from .models import SystemConfig, Message, OperationLog


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    """系统配置管理后台"""

    list_display = [
        'key', 'description', 'category',
        'is_editable', 'created_at', 'updated_at'
    ]
    list_filter = ['category', 'is_editable', 'created_at']
    search_fields = ['key', 'description', 'value']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('配置信息', {
            'fields': ('key', 'value', 'description', 'category')
        }),
        ('权限', {
            'fields': ('is_editable',)
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ['category', 'key']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """站内消息管理后台"""

    list_display = [
        'title', 'recipient', 'message_type',
        'status', 'sent_at', 'created_at'
    ]
    list_filter = ['message_type', 'status', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['sent_at', 'read_at', 'created_at']
    fieldsets = (
        ('接收者', {
            'fields': ('recipient',)
        }),
        ('内容', {
            'fields': ('title', 'content', 'message_type')
        }),
        ('状态', {
            'fields': ('status', 'sent_at', 'read_at')
        }),
        ('时间', {
            'fields': ('created_at',)
        }),
    )
    ordering = ['-created_at']


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    """操作日志管理后台"""

    list_display = [
        'operator', 'action_type', 'object_type',
        'object_id', 'status', 'created_at'
    ]
    list_filter = ['action_type', 'status', 'object_type', 'created_at']
    search_fields = ['detail', 'object_type', 'object_id', 'ip_address']
    readonly_fields = [
        'operator', 'action_type', 'object_type', 'object_id',
        'detail', 'ip_address', 'user_agent', 'status',
        'error_message', 'created_at'
    ]
    fieldsets = (
        ('操作信息', {
            'fields': ('operator', 'action_type', 'status')
        }),
        ('操作对象', {
            'fields': ('object_type', 'object_id', 'detail')
        }),
        ('来源信息', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('结果', {
            'fields': ('error_message',)
        }),
        ('时间', {
            'fields': ('created_at',)
        }),
    )
    ordering = ['-created_at']
