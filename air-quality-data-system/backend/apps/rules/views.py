from __future__ import annotations

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.airquality.models import City
from apps.airquality.services import (
    calc_quality_level_from_aqi,
    clamp_aqi,
    get_city_hourly_trend,
    get_city_latest_snapshot,
)
from apps.rules.models import ProtectionRule
from apps.rules.services import RuleMatcherService
from utils.response import APIResponse


class ProtectionGuideView(APIView):
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
