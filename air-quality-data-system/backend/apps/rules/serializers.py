from rest_framework import serializers

from .models import ProtectionRule


class ProtectionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectionRule
        fields = [
            "id",
            "rule_name",
            "min_aqi",
            "max_aqi",
            "population_type",
            "advice",
            "is_enabled",
        ]
