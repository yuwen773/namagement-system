
from rest_framework import serializers

from apps.devices.models import Device, EnergyType


class EnergyTypeField(serializers.PrimaryKeyRelatedField):
    """自定义能源类型字段，支持ID或code"""

    def to_internal_value(self, data):
        # 支持字符串 code
        if isinstance(data, str):
            try:
                return EnergyType.objects.get(code=data)
            except EnergyType.DoesNotExist:
                self.fail('does_not_exist')
        # 默认行为：处理整数 ID
        return super().to_internal_value(data)

    def to_representation(self, value):
        """输出时返回 code 字符串而不是 ID"""
        # value 可能是模型实例或 PKOnlyObject
        if isinstance(value, EnergyType):
            return value.code
        # 如果是 PKOnlyObject（只有 pk 属性），需要查询数据库
        pk = getattr(value, 'pk', value)  # 获取主键
        try:
            energy_type = EnergyType.objects.get(pk=pk)
            return energy_type.code
        except EnergyType.DoesNotExist:
            return str(pk)


class EnergyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyType
        fields = (
            "id",
            "name",
            "code",
            "unit",
            "icon",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class DeviceSerializer(serializers.ModelSerializer):
    energy_type = EnergyTypeField(queryset=EnergyType.objects.all())
    energy_type_detail = EnergyTypeSerializer(source="energy_type", read_only=True)
    room_name = serializers.CharField(source="room.room_number", read_only=True)
    floor_name = serializers.CharField(source="room.floor.name", read_only=True)
    building_name = serializers.CharField(
        source="room.floor.building.name",
        read_only=True,
    )
    campus_name = serializers.CharField(
        source="room.floor.building.campus.name",
        read_only=True,
    )

    class Meta:
        model = Device
        fields = (
            "id",
            "device_id",
            "name",
            "energy_type",
            "energy_type_detail",
            "room",
            "room_name",
            "floor_name",
            "building_name",
            "campus_name",
            "model",
            "status",
            "last_data_time",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class DeviceDetailSerializer(DeviceSerializer):
    latest_data = serializers.SerializerMethodField()

    class Meta(DeviceSerializer.Meta):
        fields = DeviceSerializer.Meta.fields + ("latest_data",)

    def get_latest_data(self, obj):
        latest_record = obj.energy_data.order_by("-timestamp", "-id").first()
        if latest_record is None:
            return None
        return {
            "id": latest_record.id,
            "timestamp": latest_record.timestamp,
            "value": latest_record.value,
            "voltage": latest_record.voltage,
            "current": latest_record.current,
            "power": latest_record.power,
            "flow_rate": latest_record.flow_rate,
        }
