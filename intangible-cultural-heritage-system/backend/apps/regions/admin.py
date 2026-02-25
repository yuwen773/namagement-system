from django.contrib import admin

from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "country_code",
        "country_name",
        "continent",
        "latitude",
        "longitude",
    )
    search_fields = ("country_code", "country_name")
    list_filter = ("continent",)
