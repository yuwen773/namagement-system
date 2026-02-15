from __future__ import annotations

from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminUser
from apps.airquality.models import City
from apps.airquality.services import (
    calc_quality_level_from_aqi,
    clamp_aqi,
    get_city_hourly_trend,
    get_city_latest_snapshot,
)
from apps.rules.models import ProtectionRule
from apps.rules.serializers import ProtectionRuleSerializer
from apps.rules.services import RuleMatcherService
from utils.exception_handler import ValidationError
from utils.response import APIResponse


def _parse_int_payload(value, field: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValidationError("格式错误，应为整数", field=field)


def _parse_bool_payload(value, field: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes"}:
            return True
        if normalized in {"false", "0", "no"}:
            return False
    raise ValidationError("格式错误，应为布尔值", field=field)


def _raise_serializer_validation_error(errors: dict):
    first_field, first_errors = next(iter(errors.items()))
    if isinstance(first_errors, (list, tuple)) and first_errors:
        message = str(first_errors[0])
    else:
        message = str(first_errors)
    raise ValidationError(message=message, field=str(first_field))


@extend_schema_view(
    get=extend_schema(
        tags=["User - Protection"],
        summary="获取防护指南",
        description="根据城市当前 AQI 与趋势预测，返回分人群防护建议和未来预警信息。",
        responses=OpenApiTypes.OBJECT,
    )
)
class ProtectionGuideView(APIView):
    """Public endpoint for AQI-based protection advice and short-term forecast warning."""

    permission_classes = [AllowAny]

    @staticmethod
    def _predict_aqi(current_aqi: int, trend_points: list[dict]) -> dict:
        usable_points = [item["aqi"] for item in trend_points if item.get("aqi") is not None]
        if len(usable_points) < 2:
            predicted_6h = current_aqi
            predicted_12h = current_aqi
            avg_change_per_hour = 0.0
        else:
            avg_change_per_hour = (usable_points[-1] - usable_points[0]) / (len(usable_points) - 1)
            predicted_6h = clamp_aqi(int(round(current_aqi + avg_change_per_hour * 6)))
            predicted_12h = clamp_aqi(int(round(current_aqi + avg_change_per_hour * 12)))

        delta_12h = predicted_12h - current_aqi
        if delta_12h >= 10:
            trend = "RISING"
        elif delta_12h <= -10:
            trend = "FALLING"
        else:
            trend = "STABLE"

        return {
            "trend": trend,
            "average_hourly_change": round(float(avg_change_per_hour), 2),
            "predicted_aqi_6h": predicted_6h,
            "predicted_aqi_12h": predicted_12h,
            "predicted_quality_level_6h": calc_quality_level_from_aqi(predicted_6h),
            "predicted_quality_level_12h": calc_quality_level_from_aqi(predicted_12h),
        }

    def get(self, request):
        city_code = (request.query_params.get("city_code") or "").strip()
        if not city_code:
            return APIResponse.error(400, "city_code 为必填参数")

        city = City.objects.select_related("province").filter(code=city_code).first()
        if city is None:
            return APIResponse.error(404, "城市不存在")

        snapshot = get_city_latest_snapshot(city)
        if snapshot is None or snapshot.get("aqi") is None:
            return APIResponse.error(404, "该城市暂无实时监测数据")

        current_aqi = int(snapshot["aqi"])
        matcher = RuleMatcherService()
        trend_points = get_city_hourly_trend(city, hours=24)
        prediction = self._predict_aqi(current_aqi, trend_points)

        warning_reference_aqi = max(
            prediction["predicted_aqi_6h"], prediction["predicted_aqi_12h"], current_aqi
        )
        warning_advice = matcher.match(warning_reference_aqi, ProtectionRule.PopulationType.SENSITIVE)

        payload = {
            "city": {
                "city_code": city.code,
                "city_name": city.name,
                "province_code": city.province.code,
                "province_name": city.province.name,
            },
            "current": {
                "monitor_time": snapshot["monitor_time"],
                "aqi": current_aqi,
                "quality_level": snapshot["quality_level"],
            },
            "advice": {
                "general": matcher.match(current_aqi, ProtectionRule.PopulationType.GENERAL),
                "sensitive": matcher.match(current_aqi, ProtectionRule.PopulationType.SENSITIVE),
                "children": matcher.match(current_aqi, ProtectionRule.PopulationType.CHILDREN),
                "elderly": matcher.match(current_aqi, ProtectionRule.PopulationType.ELDERLY),
                "patients": matcher.match(current_aqi, ProtectionRule.PopulationType.PATIENTS),
            },
            "forecast": {
                **prediction,
                "warning_reference_aqi": warning_reference_aqi,
                "warning_advice": warning_advice,
            },
        }
        return APIResponse.success(data=payload)


@extend_schema_view(
    get=extend_schema(
        tags=["Admin - Rules"],
        summary="查询防护规则",
        description="管理员查询防护规则列表，支持人群、启用状态、关键字过滤。",
        responses=OpenApiTypes.OBJECT,
    ),
    post=extend_schema(
        tags=["Admin - Rules"],
        summary="新增防护规则",
        description="管理员新增一条防护规则。",
        responses=OpenApiTypes.OBJECT,
    ),
    put=extend_schema(
        tags=["Admin - Rules"],
        summary="更新防护规则",
        description="管理员更新单条规则，或按 ids 批量更新启用状态。",
        responses=OpenApiTypes.OBJECT,
    ),
    delete=extend_schema(
        tags=["Admin - Rules"],
        summary="删除防护规则",
        description="管理员按 id 或 ids 删除防护规则。",
        responses=OpenApiTypes.OBJECT,
    ),
)
class ProtectionRuleManageView(APIView):
    """Admin CRUD endpoint for protection rule configuration and batch enable toggles."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = ProtectionRule.objects.all()

        population_type = (request.query_params.get("population_type") or "").strip()
        if population_type:
            queryset = queryset.filter(population_type=population_type)

        is_enabled = request.query_params.get("is_enabled")
        if is_enabled is not None:
            queryset = queryset.filter(is_enabled=_parse_bool_payload(is_enabled, field="is_enabled"))

        keyword = (request.query_params.get("keyword") or "").strip()
        if keyword:
            queryset = queryset.filter(Q(rule_name__icontains=keyword) | Q(advice__icontains=keyword))

        queryset = queryset.order_by("population_type", "min_aqi", "id")
        return APIResponse.success(data=ProtectionRuleSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = ProtectionRuleSerializer(data=request.data)
        if not serializer.is_valid():
            _raise_serializer_validation_error(serializer.errors)
        instance = serializer.save()
        return APIResponse.success(data=ProtectionRuleSerializer(instance).data)

    def put(self, request):
        batch_ids = request.data.get("ids")
        if isinstance(batch_ids, list):
            if "is_enabled" not in request.data:
                raise ValidationError("批量更新时必须提供 is_enabled", field="is_enabled")
            is_enabled = _parse_bool_payload(request.data.get("is_enabled"), field="is_enabled")
            normalized_ids = []
            for raw in batch_ids:
                value = _parse_int_payload(raw, field="ids")
                if value > 0 and value not in normalized_ids:
                    normalized_ids.append(value)
            if not normalized_ids:
                raise ValidationError("至少提供一个有效 id", field="ids")

            updated_count = ProtectionRule.objects.filter(id__in=normalized_ids).update(
                is_enabled=is_enabled
            )
            return APIResponse.success(data={"updated_count": updated_count}, message="批量更新完成")

        rule_id = _parse_int_payload(request.data.get("id"), field="id")
        instance = ProtectionRule.objects.filter(id=rule_id).first()
        if instance is None:
            return APIResponse.error(404, "防护规则不存在")

        serializer = ProtectionRuleSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            _raise_serializer_validation_error(serializer.errors)
        serializer.save()
        return APIResponse.success(data=serializer.data)

    def delete(self, request):
        single_id = request.data.get("id")
        id_list = request.data.get("ids")
        if single_id is None and not id_list:
            raise ValidationError("至少提供 id 或 ids", field="id")

        if single_id is not None:
            rule_id = _parse_int_payload(single_id, field="id")
            queryset = ProtectionRule.objects.filter(id=rule_id)
            if not queryset.exists():
                return APIResponse.error(404, "防护规则不存在")
            deleted_count, _ = queryset.delete()
            return APIResponse.success(data={"deleted_count": deleted_count}, message="删除成功")

        if not isinstance(id_list, list):
            raise ValidationError("格式错误，应为整数数组", field="ids")
        normalized_ids = []
        for raw in id_list:
            value = _parse_int_payload(raw, field="ids")
            if value > 0 and value not in normalized_ids:
                normalized_ids.append(value)
        if not normalized_ids:
            raise ValidationError("至少提供一个有效 id", field="ids")

        deleted_count, _ = ProtectionRule.objects.filter(id__in=normalized_ids).delete()
        return APIResponse.success(data={"deleted_count": deleted_count}, message="批量删除完成")
