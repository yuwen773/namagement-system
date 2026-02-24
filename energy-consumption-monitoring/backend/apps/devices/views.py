from django.db.models import Exists, OuterRef, Q, Subquery
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.buildings.models import Room
from apps.devices.models import Device, EnergyType
from apps.devices.serializers import (
    DeviceDetailSerializer,
    DeviceSerializer,
    EnergyTypeSerializer,
)
from apps.energy.models import EnergyData
from energy_monitoring.permissions import IsAdmin, IsAdminOrReadOnly


class EnergyTypeViewSet(viewsets.ModelViewSet):
    queryset = EnergyType.objects.all().order_by("id")
    serializer_class = EnergyTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "code"]
    ordering_fields = ["id", "name", "code", "created_at"]
    ordering = ["id"]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related(
        "energy_type",
        "room",
        "room__floor",
        "room__floor__building",
        "room__floor__building__campus",
    ).all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["device_id", "name", "model"]
    ordering_fields = ["id", "device_id", "name", "status", "last_data_time", "created_at"]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DeviceDetailSerializer
        return DeviceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        room_id = self.request.query_params.get("room_id")
        if room_id:
            queryset = queryset.filter(room_id=room_id)

        energy_type = self.request.query_params.get("energy_type")
        if energy_type:
            if str(energy_type).isdigit():
                queryset = queryset.filter(energy_type_id=int(energy_type))
            else:
                queryset = queryset.filter(energy_type__code__iexact=energy_type)

        status_value = self.request.query_params.get("status")
        if status_value:
            queryset = queryset.filter(status=status_value)

        return queryset

    @action(detail=False, methods=["get"], url_path="data-status")
    def data_status(self, request):
        queryset = self.get_queryset().annotate(
            has_data=Exists(EnergyData.objects.filter(device_id=OuterRef("pk"))),
            latest_timestamp=Subquery(
                EnergyData.objects.filter(device_id=OuterRef("pk"))
                .order_by("-timestamp")
                .values("timestamp")[:1]
            ),
        )
        payload = [
            {
                "id": device.id,
                "device_id": device.device_id,
                "name": device.name,
                "status": device.status,
                "has_data": device.has_data,
                "last_data_time": device.latest_timestamp or device.last_data_time,
            }
            for device in queryset
        ]
        return Response(payload)

    @action(
        detail=True,
        methods=["post"],
        url_path="bind-room",
        permission_classes=[IsAdmin],
    )
    def bind_room(self, request, pk=None):
        device = self.get_object()
        room_id = request.data.get("room_id")
        if room_id in (None, "", "null"):
            device.room = None
            device.save(update_fields=["room", "updated_at"])
            return Response(DeviceDetailSerializer(device).data)

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response(
                {"message": "房间不存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        device.room = room
        device.save(update_fields=["room", "updated_at"])
        return Response(DeviceDetailSerializer(device).data)
