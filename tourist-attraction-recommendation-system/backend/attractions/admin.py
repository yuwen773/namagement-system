from django.contrib import admin
from .models import Attraction


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'region', 'view_count', 'is_deleted', 'created_at']
    list_filter = ['category', 'region', 'is_deleted']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
