from rest_framework import serializers

from .models import Region


class RegionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            "id",
            "country_code",
            "country_name",
            "continent",
            "latitude",
            "longitude",
        )


class RegionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            "id",
            "country_code",
            "country_name",
            "continent",
            "latitude",
            "longitude",
        )
