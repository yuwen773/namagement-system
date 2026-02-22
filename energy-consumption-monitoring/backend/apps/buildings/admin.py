from django.contrib import admin

from apps.buildings.models import Building, Campus, Floor, Room


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "capacity", "created_at", "updated_at")
    search_fields = ("name", "code")


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "campus",
        "area_type",
        "floors_count",
        "created_at",
        "updated_at",
    )
    list_filter = ("area_type", "campus")
    search_fields = ("name", "code", "address")


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "floor_number", "building", "created_at", "updated_at")
    list_filter = ("building",)
    search_fields = ("name", "building__name")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_number", "room_type", "floor", "department", "created_at")
    list_filter = ("room_type", "floor__building")
    search_fields = ("room_number", "department", "floor__name", "floor__building__name")
