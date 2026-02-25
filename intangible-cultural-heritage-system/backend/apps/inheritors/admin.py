from django.contrib import admin

from .models import Inheritor


@admin.register(Inheritor)
class InheritorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "heritage_item", "region", "level", "updated_at")
    list_filter = ("level", "gender", "region")
    search_fields = ("name", "heritage_item__name")
