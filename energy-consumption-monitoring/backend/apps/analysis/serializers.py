
from rest_framework import serializers


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


class ForecastQuerySerializer(BaseAnalysisQuerySerializer):
    target = serializers.ChoiceField(choices=["campus", "building", "meter"], default="building")
    target_id = serializers.CharField(required=False)
    model_version = serializers.CharField(required=False)
    period = serializers.ChoiceField(choices=["7d", "30d"], default="7d")
