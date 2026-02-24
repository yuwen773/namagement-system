
from rest_framework import serializers

from apps.energy.models import EnergyData, EnergyStatistics


class EnergyDataSerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(source="device.device_id", read_only=True)
    energy_type_code = serializers.CharField(source="energy_type.code", read_only=True)

    class Meta:
        model = EnergyData
        fields = (
            "id",
            "device",
            "device_code",
            "energy_type",
            "energy_type_code",
            "timestamp",
            "value",
            "voltage",
            "current",
            "power",
            "flow_rate",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "device_code", "energy_type_code")

    def validate(self, attrs):
        device = attrs.get("device")
        energy_type = attrs.get("energy_type")
        if device and energy_type and device.energy_type_id != energy_type.id:
            raise serializers.ValidationError(
                {"energy_type": "能源类型必须与设备绑定的能源类型一致。"}
            )
        return attrs


class EnergyDataBatchSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    records = serializers.JSONField(required=False)
    format = serializers.ChoiceField(
        choices=["csv", "excel", "json"],
        required=False,
    )

    def validate(self, attrs):
        if not attrs.get("file") and not attrs.get("records"):
            raise serializers.ValidationError("请上传文件或提供 records JSON 数据。")
        return attrs


class EnergyStatisticsSerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(source="device.device_id", read_only=True)
    energy_type_code = serializers.CharField(source="energy_type.code", read_only=True)

    class Meta:
        model = EnergyStatistics
        fields = (
            "id",
            "device",
            "device_code",
            "energy_type",
            "energy_type_code",
            "period_type",
            "period_date",
            "total_value",
            "peak_value",
            "peak_time",
            "avg_value",
            "cost",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "device_code",
            "energy_type_code",
        )
