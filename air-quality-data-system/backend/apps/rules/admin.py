from django.contrib import admin

from .models import ProtectionRule


@admin.register(ProtectionRule)
class ProtectionRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "rule_name", "population_type", "min_aqi", "max_aqi", "is_enabled")
    list_filter = ("population_type", "is_enabled")
    search_fields = ("rule_name", "advice")
