from datetime import timedelta

from django.core.cache import cache
from django.db.models import Avg, Count, Max, Q, Sum
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.buildings.models import Building, Campus, Floor, Room
from apps.buildings.serializers import (
    BuildingHeatmapQuerySerializer,
    BuildingSerializer,
    BuildingTreeSerializer,
    CampusSerializer,
    FloorSerializer,
    RoomSerializer,
)
from apps.energy.models import EnergyData
from energy_monitoring.permissions import IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(summary="获取校区列表"),
    retrieve=extend_schema(summary="获取校区详情"),
)
class CampusViewSet(viewsets.ReadOnlyModelViewSet):
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
        description="按校区-建筑-楼层-房间输出完整树结构。",
        responses={200: BuildingTreeSerializer(many=True)},
    ),
    heatmap=extend_schema(
        summary="获取校区建筑热力图数据",
        parameters=[BuildingHeatmapQuerySerializer],
    ),
)
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

    @action(detail=False, methods=["get"], url_path="heatmap")
    def heatmap(self, request):
        query = BuildingHeatmapQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        params = query.validated_data

        campus_id = params.get("campus_id")
        days = int(params.get("days", 7))
        energy_type = params.get("energy_type")

        cache_key = f"heatmap:{campus_id or 'all'}:{energy_type or 'all'}:{days}"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        end_time = timezone.now()
        start_time = end_time - timedelta(days=days)

        building_queryset = Building.objects.select_related("campus").order_by("campus_id", "id")
        if campus_id:
            building_queryset = building_queryset.filter(campus_id=campus_id)

        energy_queryset = EnergyData.objects.filter(timestamp__gte=start_time, timestamp__lte=end_time)
        if campus_id:
            energy_queryset = energy_queryset.filter(device__room__floor__building__campus_id=campus_id)

        if energy_type:
            if str(energy_type).isdigit():
                energy_queryset = energy_queryset.filter(energy_type_id=int(energy_type))
            else:
                energy_queryset = energy_queryset.filter(energy_type__code__iexact=str(energy_type).strip())

        summary_rows = energy_queryset.values("device__room__floor__building_id").annotate(
            total_value=Sum("value"),
            avg_power=Avg("power"),
            max_power=Max("power"),
            data_count=Count("id"),
            device_count=Count("device_id", distinct=True),
        )
        summary_map = {
            row["device__room__floor__building_id"]: {
                "total_value": float(row["total_value"] or 0),
                "avg_power": float(row["avg_power"] or 0),
                "max_power": float(row["max_power"] or 0),
                "data_count": int(row["data_count"] or 0),
                "device_count": int(row["device_count"] or 0),
                "latest_power": None,
                "latest_power_time": None,
            }
            for row in summary_rows
        }

        latest_time_rows = (
            energy_queryset.exclude(power__isnull=True)
            .values("device__room__floor__building_id")
            .annotate(latest_power_time=Max("timestamp"))
        )
        latest_time_map = {
            row["device__room__floor__building_id"]: row["latest_power_time"]
            for row in latest_time_rows
        }

        if latest_time_map:
            latest_candidates = (
                energy_queryset.exclude(power__isnull=True)
                .filter(timestamp__in=list(set(latest_time_map.values())))
                .values("device__room__floor__building_id", "timestamp", "power")
                .order_by("device__room__floor__building_id", "-timestamp", "-id")
            )
            for row in latest_candidates:
                building_id = row["device__room__floor__building_id"]
                target_ts = latest_time_map.get(building_id)
                if target_ts is None or row["timestamp"] != target_ts:
                    continue
                summary = summary_map.get(building_id)
                if summary is None or summary["latest_power"] is not None:
                    continue
                summary["latest_power"] = float(row["power"] or 0)
                summary["latest_power_time"] = row["timestamp"]

        campus_offsets = {}
        buildings = []
        max_total = 0.0

        for item in building_queryset.values("id", "name", "code", "campus_id", "campus__name", "area_type"):
            summary = summary_map.get(item["id"], {})
            total_value = float(summary.get("total_value") or 0)
            max_total = max(max_total, total_value)

            idx = campus_offsets.get(item["campus_id"], 0)
            campus_offsets[item["campus_id"]] = idx + 1

            buildings.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "code": item["code"],
                    "campus_id": item["campus_id"],
                    "campus_name": item["campus__name"],
                    "area_type": item["area_type"],
                    "total_value": round(total_value, 6),
                    "avg_power": round(float(summary.get("avg_power") or 0), 3),
                    "max_power": round(float(summary.get("max_power") or 0), 3),
                    "latest_power": round(float(summary.get("latest_power") or 0), 3)
                    if summary.get("latest_power") is not None
                    else None,
                    "latest_power_time": (
                        summary.get("latest_power_time").isoformat()
                        if summary.get("latest_power_time")
                        else None
                    ),
                    "data_count": int(summary.get("data_count") or 0),
                    "device_count": int(summary.get("device_count") or 0),
                    "position": {"x": idx % 8, "y": idx // 8},
                }
            )

        for row in buildings:
            heat_index = round(row["total_value"] / max_total * 100, 2) if max_total > 0 else 0
            row["heat_index"] = heat_index
            if heat_index >= 75:
                row["heat_level"] = "high"
            elif heat_index >= 40:
                row["heat_level"] = "normal"
            elif heat_index > 0:
                row["heat_level"] = "low"
            else:
                row["heat_level"] = "none"

        payload = {
            "range_days": days,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "campus_id": campus_id,
            "energy_type": energy_type,
            "buildings": buildings,
        }
        cache.set(cache_key, payload, timeout=60)
        return Response(payload)

@extend_schema_view(
    list=extend_schema(summary="获取楼层列表"),
    create=extend_schema(summary="创建楼层"),
)
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


@extend_schema_view(
    list=extend_schema(summary="获取房间列表"),
    create=extend_schema(summary="创建房间"),
)
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
