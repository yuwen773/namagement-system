from django.contrib import admin

from apps.devices.models import Device, EnergyType


@admin.register(EnergyType)
class EnergyTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "unit", "icon", "created_at", "updated_at")
    search_fields = ("name", "code", "unit")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device_id",
        "name",
        "energy_type",
        "room",
        "status",
        "last_data_time",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "energy_type", "room__floor__building")
    search_fields = (
        "device_id",
        "name",
        "model",
        "room__room_number",
        "room__floor__name",
        "room__floor__building__name",
    )
