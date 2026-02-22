from rest_framework import serializers

from .models import AirQualityData, MonitoringStation


class ProvinceCitySerializer(serializers.Serializer):
    province_code = serializers.CharField()
    province_name = serializers.CharField()
    city_code = serializers.CharField()
    city_name = serializers.CharField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    aqi = serializers.FloatField(allow_null=True)
    pm25 = serializers.FloatField(allow_null=True)
    pm10 = serializers.FloatField(allow_null=True)
    so2 = serializers.FloatField(allow_null=True)
    no2 = serializers.FloatField(allow_null=True)
    co = serializers.FloatField(allow_null=True)
    o3 = serializers.FloatField(allow_null=True)
    quality_level = serializers.CharField(allow_blank=True)


class HistoricalAirQualitySerializer(serializers.ModelSerializer):
    province_code = serializers.CharField(source="station.city.province.code", read_only=True)
    province_name = serializers.CharField(source="station.city.province.name", read_only=True)
    city_code = serializers.CharField(source="station.city.code", read_only=True)
    city_name = serializers.CharField(source="station.city.name", read_only=True)
    station_code = serializers.CharField(source="station.code", read_only=True)
    station_name = serializers.CharField(source="station.name", read_only=True)
    quality_level_display = serializers.CharField(source="get_quality_level_display", read_only=True)

    class Meta:
        model = AirQualityData
        fields = [
            "id",
            "province_code",
            "province_name",
            "city_code",
            "city_name",
            "station_code",
            "station_name",
            "monitor_time",
            "aqi",
            "pm25",
            "pm10",
            "so2",
            "no2",
            "co",
            "o3",
            "quality_level",
            "quality_level_display",
        ]
        read_only_fields = fields


class AirQualityDataManageSerializer(serializers.ModelSerializer):
    province_code = serializers.CharField(source="station.city.province.code", read_only=True)
    province_name = serializers.CharField(source="station.city.province.name", read_only=True)
    city_code = serializers.CharField(source="station.city.code", read_only=True)
    city_name = serializers.CharField(source="station.city.name", read_only=True)
    station_code = serializers.CharField(source="station.code", read_only=True)
    station_name = serializers.CharField(source="station.name", read_only=True)
    quality_level_display = serializers.CharField(source="get_quality_level_display", read_only=True)
    station_id = serializers.PrimaryKeyRelatedField(
        source="station", queryset=MonitoringStation.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = AirQualityData
        fields = [
            "id",
            "province_code",
            "province_name",
            "city_code",
            "city_name",
            "station_id",
            "station_code",
            "station_name",
            "monitor_time",
            "aqi",
            "pm25",
            "pm10",
            "so2",
            "no2",
            "co",
            "o3",
            "quality_level",
            "quality_level_display",
        ]
        read_only_fields = [
            "id",
            "province_code",
            "province_name",
            "city_code",
            "city_name",
            "station_code",
            "station_name",
            "quality_level",
            "quality_level_display",
        ]
