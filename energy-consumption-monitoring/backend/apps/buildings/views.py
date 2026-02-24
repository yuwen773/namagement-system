from drf_spectacular.utils import extend_schema, extend_schema_view
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


@extend_schema_view(
    list=extend_schema(summary="获取校区列表"),
    retrieve=extend_schema(summary="获取校区详情"),
)
class CampusViewSet(viewsets.ReadOnlyModelViewSet):
    """校区只读接口。"""

    queryset = Campus.objects.all().order_by("id")
    serializer_class = CampusSerializer


@extend_schema_view(
    list=extend_schema(summary="获取建筑列表"),
    retrieve=extend_schema(summary="获取建筑详情"),
    create=extend_schema(summary="创建建筑"),
    update=extend_schema(summary="更新建筑"),
    partial_update=extend_schema(summary="部分更新建筑"),
    destroy=extend_schema(summary="删除建筑"),
    tree=extend_schema(
        summary="获取建筑树",
        description="按校区-楼宇-楼层-房间输出完整树结构。",
        responses={200: BuildingTreeSerializer(many=True)},
    ),
)
class BuildingViewSet(viewsets.ModelViewSet):
    """建筑 CRUD 与树形结构接口。"""

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
        """返回校区-建筑-楼层-房间树形数据。"""
        queryset = Campus.objects.prefetch_related("buildings__floors__rooms").order_by("id")
        serializer = BuildingTreeSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="获取楼层列表"),
    create=extend_schema(summary="创建楼层"),
)
class FloorViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """楼层列表与创建接口。"""

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


@extend_schema_view(
    list=extend_schema(summary="获取房间列表"),
    create=extend_schema(summary="创建房间"),
)
class RoomViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """房间列表与创建接口。"""

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
