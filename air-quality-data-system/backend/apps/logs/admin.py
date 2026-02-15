from django.contrib import admin

from .models import ErrorLog, ImportTask, ImportTaskLog, OperationLog


@admin.register(OperationLog)
class OperationLogAdmin(admin.ModelAdmin):
    list_display = ("id", "operation_type", "user", "ip_address", "operation_time")
    list_filter = ("operation_type",)
    search_fields = ("operation_type", "operation_content", "ip_address")


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ("id", "error_type", "occurred_at")
    list_filter = ("error_type",)
    search_fields = ("error_type", "error_message")


@admin.register(ImportTask)
class ImportTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task_id",
        "file_name",
        "file_type",
        "status",
        "total_count",
        "success_count",
        "failed_count",
        "initiator",
        "start_time",
        "end_time",
    )
    list_filter = ("status", "file_type")
    search_fields = ("task_id", "file_name")


@admin.register(ImportTaskLog)
class ImportTaskLogAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "row_number", "created_at")
    list_filter = ("task",)
    search_fields = ("error_reason", "raw_data_snippet")

