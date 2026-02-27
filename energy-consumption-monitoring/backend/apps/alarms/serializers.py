
from rest_framework import serializers

from apps.alarms.models import Alarm, AlarmRule, AlarmStatus
from apps.devices.models import EnergyType
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
        extra_kwargs = {
            "energy_type": {"required": True}
        }

    def validate_energy_type(self, value):
        # 支持两种输入方式：
        # 1. 整数 ID（原始行为）
        # 2. 字符串 code（自动转换为 EnergyType 对象）
        if isinstance(value, str):
            try:
                return EnergyType.objects.get(code=value)
            except EnergyType.DoesNotExist:
                raise serializers.ValidationError(f"能源类型代码 '{value}' 不存在")
        return value


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
