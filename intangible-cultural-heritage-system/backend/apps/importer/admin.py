from django.contrib import admin

from .models import ImportError, ImportJob


class ImportErrorInline(admin.TabularInline):
    model = ImportError
    extra = 0
    readonly_fields = ("row_number", "field_name", "error_message", "raw_data")


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file_name",
        "status",
        "total_rows",
        "success_count",
        "error_count",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("file_name", "created_by__username")
    inlines = (ImportErrorInline,)


@admin.register(ImportError)
class ImportErrorAdmin(admin.ModelAdmin):
    list_display = ("id", "import_job", "row_number", "field_name")
    search_fields = ("import_job__file_name", "field_name", "error_message")
