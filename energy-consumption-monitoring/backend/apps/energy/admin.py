from django.contrib import admin

from apps.energy.models import EnergyData, EnergyStatistics


@admin.register(EnergyData)
class EnergyDataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device",
        "energy_type",
        "timestamp",
        "value",
        "voltage",
        "current",
        "power",
        "flow_rate",
        "created_at",
    )
    list_filter = ("energy_type", "device", "timestamp")
    search_fields = ("device__device_id", "device__name")


@admin.register(EnergyStatistics)
class EnergyStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device",
        "energy_type",
        "period_type",
        "period_date",
        "total_value",
        "peak_value",
        "avg_value",
        "cost",
        "created_at",
    )
    list_filter = ("period_type", "energy_type", "period_date")
    search_fields = ("device__device_id", "device__name")
