from django.contrib import admin

from apps.alarms.models import Alarm, AlarmRule


@admin.register(AlarmRule)
class AlarmRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "energy_type",
        "condition_type",
        "threshold_value",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("condition_type", "energy_type", "is_active")
    search_fields = ("name",)


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device",
        "rule",
        "alarm_type",
        "alarm_value",
        "alarm_time",
        "status",
        "handler",
        "handle_time",
        "created_at",
    )
    list_filter = ("alarm_type", "status", "alarm_time")
    search_fields = ("device__device_id", "device__name", "remark")
