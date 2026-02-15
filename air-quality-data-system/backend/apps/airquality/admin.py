from django.contrib import admin

from .models import AirQualityData, City, MonitoringStation, Province


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "level")
    search_fields = ("name", "code")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "province", "longitude", "latitude")
    list_filter = ("province",)
    search_fields = ("name", "code")


@admin.register(MonitoringStation)
class MonitoringStationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "city", "station_type")
    list_filter = ("city", "station_type")
    search_fields = ("name", "code", "address")


@admin.register(AirQualityData)
class AirQualityDataAdmin(admin.ModelAdmin):
    list_display = ("id", "station", "monitor_time", "aqi", "quality_level")
    list_filter = ("quality_level", "station")
    search_fields = ("station__name", "station__code")
