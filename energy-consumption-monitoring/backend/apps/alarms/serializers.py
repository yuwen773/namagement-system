
from rest_framework import serializers

from apps.alarms.models import Alarm, AlarmRule, AlarmStatus
from apps.devices.serializers import DeviceSerializer, EnergyTypeSerializer


class AlarmRuleSerializer(serializers.ModelSerializer):
    energy_type_detail = EnergyTypeSerializer(source="energy_type", read_only=True)

    class Meta:
        model = AlarmRule
        fields = (
            "id",
            "name",
            "energy_type",
            "energy_type_detail",
            "condition_type",
            "threshold_value",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class AlarmSerializer(serializers.ModelSerializer):
    device_detail = DeviceSerializer(source="device", read_only=True)
    rule_name = serializers.CharField(source="rule.name", read_only=True)
    handler_name = serializers.CharField(source="handler.username", read_only=True)

    class Meta:
        model = Alarm
        fields = (
            "id",
            "device",
            "device_detail",
            "rule",
            "rule_name",
            "alarm_type",
            "alarm_value",
            "alarm_time",
            "status",
            "handler",
            "handler_name",
            "handle_time",
            "remark",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "handler",
            "handle_time",
            "created_at",
            "updated_at",
        )


class AlarmHandleSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[AlarmStatus.PROCESSED, AlarmStatus.IGNORED],
        default=AlarmStatus.PROCESSED,
    )
    remark = serializers.CharField(required=False, allow_blank=True, max_length=500)
