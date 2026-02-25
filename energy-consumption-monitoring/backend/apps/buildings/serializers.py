
from rest_framework import serializers

from apps.buildings.models import Building, Campus, Floor, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "floor",
            "room_number",
            "room_type",
            "area",
            "department",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class FloorSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = (
            "id",
            "building",
            "floor_number",
            "name",
            "rooms",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class BuildingSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source="campus.name", read_only=True)
    floors = FloorSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = (
            "id",
            "campus",
            "campus_name",
            "name",
            "code",
            "area_type",
            "address",
            "floors_count",
            "floors",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ("id", "name", "code", "capacity", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class BuildingTreeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "room_number", "room_type", "department")


class BuildingTreeFloorSerializer(serializers.ModelSerializer):
    rooms = BuildingTreeRoomSerializer(many=True, read_only=True)

    class Meta:
        model = Floor
        fields = ("id", "name", "floor_number", "rooms")


class BuildingTreeBuildingSerializer(serializers.ModelSerializer):
    floors = BuildingTreeFloorSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = ("id", "name", "code", "area_type", "floors")


class BuildingTreeSerializer(serializers.ModelSerializer):
    buildings = BuildingTreeBuildingSerializer(many=True, read_only=True)

    class Meta:
        model = Campus
        fields = ("id", "name", "code", "buildings")


class BuildingHeatmapQuerySerializer(serializers.Serializer):
    campus_id = serializers.IntegerField(required=False, min_value=1)
    energy_type = serializers.CharField(required=False)
    days = serializers.IntegerField(required=False, min_value=1, max_value=365, default=7)
