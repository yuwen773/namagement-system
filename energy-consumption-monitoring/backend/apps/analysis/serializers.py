
from rest_framework import serializers

from apps.analysis.models import Achievement, UserAchievement

class BaseAnalysisQuerySerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    device_id = serializers.CharField(required=False)
    energy_type = serializers.CharField(required=False)
    campus_id = serializers.IntegerField(required=False, min_value=1)
    building_id = serializers.IntegerField(required=False, min_value=1)
    room_id = serializers.IntegerField(required=False, min_value=1)

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("start_date 不能晚于 end_date。")
        return attrs


class TrendQuerySerializer(BaseAnalysisQuerySerializer):
    period = serializers.ChoiceField(choices=["day", "month", "year"], default="day")


class DistributionQuerySerializer(BaseAnalysisQuerySerializer):
    type = serializers.ChoiceField(choices=["area", "energy_type"], default="area")


class RankingQuerySerializer(BaseAnalysisQuerySerializer):
    type = serializers.ChoiceField(choices=["building", "room", "department"], default="building")
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=10)


class ComparisonQuerySerializer(BaseAnalysisQuerySerializer):
    period = serializers.ChoiceField(choices=["day", "month", "year"], default="month")
    anchor_date = serializers.DateField(required=False)
    view = serializers.ChoiceField(
        choices=["summary", "radar", "trend", "history_rank"],
        default="summary",
        required=False,
    )
    type = serializers.ChoiceField(choices=["school", "building", "similar"], required=False)


class ForecastQuerySerializer(BaseAnalysisQuerySerializer):
    target = serializers.ChoiceField(choices=["campus", "building", "meter"], default="building")
    target_id = serializers.CharField(required=False)
    model_version = serializers.CharField(required=False)
    period = serializers.ChoiceField(choices=["7d", "30d"], default="7d")


class RealTimePowerQuerySerializer(BaseAnalysisQuerySerializer):
    hours = serializers.IntegerField(required=False, min_value=1, max_value=168, default=24)
    interval_minutes = serializers.ChoiceField(choices=[5, 10, 15, 30, 60], default=15)


class HourlyDistributionQuerySerializer(BaseAnalysisQuerySerializer):
    pass


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            "id",
            "code",
            "name",
            "description",
            "icon",
            "points",
            "is_active",
            "sort_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserAchievementSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="achievement.id", read_only=True)
    code = serializers.CharField(source="achievement.code", read_only=True)
    name = serializers.CharField(source="achievement.name", read_only=True)
    desc = serializers.CharField(source="achievement.description", read_only=True)
    icon = serializers.CharField(source="achievement.icon", read_only=True)

    class Meta:
        model = UserAchievement
        fields = [
            "id",
            "code",
            "name",
            "desc",
            "icon",
            "unlocked",
            "progress",
            "unlocked_at",
            "metadata",
        ]
