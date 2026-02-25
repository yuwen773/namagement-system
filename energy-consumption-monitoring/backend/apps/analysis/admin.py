from django.contrib import admin

from apps.analysis.models import Achievement, EnergyForecast, UserAchievement


@admin.register(EnergyForecast)
class EnergyForecastAdmin(admin.ModelAdmin):
    list_display = ("id", "target_type", "target_id", "energy_type", "forecast_date", "forecast_value", "horizon_days")
    list_filter = ("target_type", "energy_type", "horizon_days")
    search_fields = ("target_id", "model_version")


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "points", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("code", "name")
    ordering = ("sort_order", "id")


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "achievement", "unlocked", "progress", "unlocked_at")
    list_filter = ("unlocked", "achievement")
    search_fields = ("user__username", "achievement__code", "achievement__name")
