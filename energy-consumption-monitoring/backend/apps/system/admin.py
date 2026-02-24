from django.contrib import admin

from apps.system.models import Bill, Notice, OperationLog, RechargeRecord


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "room",
        "energy_type",
        "bill_period",
        "usage",
        "amount",
        "status",
        "due_date",
        "created_at",
    )
    list_filter = ("status", "energy_type", "bill_period", "due_date")
    search_fields = ("room__room_number", "room__floor__building__name", "bill_period")


@admin.register(RechargeRecord)
class RechargeRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "room",
        "amount",
        "payment_method",
        "recharge_time",
        "operator",
        "created_at",
    )
    list_filter = ("payment_method", "recharge_time")
    search_fields = ("room__room_number", "remark")


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
