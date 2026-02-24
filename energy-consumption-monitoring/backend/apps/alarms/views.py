from django.db.models import Count, Q
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.alarms.models import Alarm, AlarmRule, AlarmStatus
from apps.alarms.serializers import AlarmHandleSerializer, AlarmRuleSerializer, AlarmSerializer
from energy_monitoring.permissions import IsAdmin, IsAdminOrReadOnly


@extend_schema_view(
    list=extend_schema(summary="获取告警规则列表"),
    retrieve=extend_schema(summary="获取告警规则详情"),
    create=extend_schema(summary="创建告警规则"),
    update=extend_schema(summary="更新告警规则"),
    partial_update=extend_schema(summary="部分更新告警规则"),
    destroy=extend_schema(summary="删除告警规则"),
)
class AlarmRuleViewSet(viewsets.ModelViewSet):
    """告警规则管理接口。"""

    queryset = AlarmRule.objects.select_related("energy_type").all().order_by("id")
    serializer_class = AlarmRuleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "energy_type__name", "energy_type__code"]
    ordering_fields = ["id", "name", "is_active", "created_at"]
    ordering = ["id"]


@extend_schema_view(
    list=extend_schema(summary="获取告警列表"),
    retrieve=extend_schema(summary="获取告警详情"),
    handle=extend_schema(
        summary="处理告警",
        request=AlarmHandleSerializer,
        responses={200: AlarmSerializer},
    ),
    statistics=extend_schema(
        summary="获取告警统计",
        responses={200: OpenApiTypes.OBJECT},
    ),
)
class AlarmViewSet(viewsets.ReadOnlyModelViewSet):
    """告警记录查询与处理接口。"""

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
        """处理单条告警并记录处理信息。"""
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
        """返回告警总量、状态分布与设备 Top10。"""
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
