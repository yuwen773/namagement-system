from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.buildings.models import Building, Campus, Floor, Room
from apps.buildings.serializers import (
    BuildingSerializer,
    BuildingTreeSerializer,
    CampusSerializer,
    FloorSerializer,
    RoomSerializer,
)
from energy_monitoring.permissions import IsAdminOrReadOnly


class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campus.objects.all().order_by("id")
    serializer_class = CampusSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.select_related("campus").prefetch_related("floors__rooms")
    serializer_class = BuildingSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "code"]
    ordering_fields = ["id", "name", "created_at"]
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        area_type = self.request.query_params.get("area_type")
        if area_type:
            queryset = queryset.filter(area_type=area_type)
        campus_id = self.request.query_params.get("campus_id")
        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        return queryset

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request):
        queryset = Campus.objects.prefetch_related("buildings__floors__rooms").order_by("id")
        serializer = BuildingTreeSerializer(queryset, many=True)
        return Response(serializer.data)


class FloorViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Floor.objects.select_related("building", "building__campus").prefetch_related("rooms")
    serializer_class = FloorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "building__name"]
    ordering_fields = ["id", "floor_number", "created_at"]
    ordering = ["id"]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = super().get_queryset()
        building_id = self.request.query_params.get("building_id")
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        return queryset


class RoomViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Room.objects.select_related("floor", "floor__building", "floor__building__campus")
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["room_number", "department", "floor__name", "floor__building__name"]
    ordering_fields = ["id", "room_number", "created_at"]
    ordering = ["id"]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = super().get_queryset()
        floor_id = self.request.query_params.get("floor_id")
        if floor_id:
            queryset = queryset.filter(floor_id=floor_id)
        building_id = self.request.query_params.get("building_id")
        if building_id:
            queryset = queryset.filter(floor__building_id=building_id)
        return queryset
