from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.alarms.models import Alarm, AlarmRule, AlarmStatus
from apps.alarms.serializers import AlarmHandleSerializer, AlarmRuleSerializer, AlarmSerializer
from energy_monitoring.permissions import IsAdmin, IsAdminOrReadOnly


class AlarmRuleViewSet(viewsets.ModelViewSet):
    queryset = AlarmRule.objects.select_related("energy_type").all().order_by("id")
    serializer_class = AlarmRuleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "energy_type__name", "energy_type__code"]
    ordering_fields = ["id", "name", "is_active", "created_at"]
    ordering = ["id"]


class AlarmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alarm.objects.select_related("device", "rule", "handler").all().order_by("-alarm_time", "-id")
    serializer_class = AlarmSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["device__device_id", "device__name", "rule__name", "remark"]
    ordering_fields = ["id", "alarm_time", "status", "created_at"]
    ordering = ["-alarm_time", "-id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        if status_value:
            normalized = str(status_value).strip().upper()
            status_map = {
                "PENDING": AlarmStatus.PENDING,
                "PROCESSED": AlarmStatus.PROCESSED,
                "IGNORED": AlarmStatus.IGNORED,
            }
            target_status = status_map.get(normalized)
            if target_status:
                queryset = queryset.filter(status=target_status)

        rule_id = self.request.query_params.get("rule_id")
        if rule_id:
            queryset = queryset.filter(rule_id=rule_id)
        return queryset

    @action(
        detail=True,
        methods=["post"],
        url_path="handle",
        permission_classes=[IsAdmin],
    )
    def handle(self, request, pk=None):
        alarm = self.get_object()
        serializer = AlarmHandleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alarm.status = serializer.validated_data["status"]
        alarm.remark = serializer.validated_data.get("remark", alarm.remark)
        alarm.handler = request.user
        alarm.handle_time = timezone.now()
        alarm.save(update_fields=["status", "remark", "handler", "handle_time", "updated_at"])
        return Response(AlarmSerializer(alarm).data)

    @action(detail=False, methods=["get"], url_path="statistics")
    def statistics(self, request):
        queryset = self.get_queryset()
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        totals = queryset.aggregate(
            total=Count("id"),
            pending=Count("id", filter=Q(status=AlarmStatus.PENDING)),
            processed=Count("id", filter=Q(status=AlarmStatus.PROCESSED)),
            ignored=Count("id", filter=Q(status=AlarmStatus.IGNORED)),
            today=Count("id", filter=Q(alarm_time__gte=today_start)),
        )

        by_type = list(
            queryset.values("alarm_type").annotate(count=Count("id")).order_by("-count", "alarm_type")
        )
        by_device = list(
            queryset.values("device__id", "device__device_id", "device__name")
            .annotate(count=Count("id"))
            .order_by("-count", "device__id")[:10]
        )

        return Response(
            {
                "summary": totals,
                "by_type": by_type,
                "top_devices": by_device,
            }
        )
