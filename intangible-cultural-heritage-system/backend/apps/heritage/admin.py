from django.contrib import admin

from .models import HeritageItem


@admin.register(HeritageItem)
class HeritageItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "level",
        "region",
        "updated_at",
    )
    list_filter = ("level", "category", "region")
    search_fields = ("name", "area", "protection_unit")
