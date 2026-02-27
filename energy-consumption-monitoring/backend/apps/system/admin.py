from django.contrib import admin

from apps.system.models import Notice, OperationLog


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "notice_type",
        "priority",
        "is_published",
        "publish_time",
        "target_role",
        "publisher",
        "created_at",
    )
    list_filter = ("notice_type", "priority", "is_published", "target_role")
    search_fields = ("title", "content")


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "resource",
        "ip_address",
        "create_time",
    )
    list_filter = ("action", "create_time")
    search_fields = ("resource", "ip_address", "request_path")
