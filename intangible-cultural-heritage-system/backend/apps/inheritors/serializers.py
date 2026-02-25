from rest_framework import serializers

from apps.heritage.models import HeritageItem
from apps.regions.models import Region

from .models import Inheritor


class RegionBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("id", "country_code", "country_name", "continent")


class InheritorHeritageBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeritageItem
        fields = ("id", "name", "level")


class InheritorReadSerializer(serializers.ModelSerializer):
    heritage_item = InheritorHeritageBriefSerializer(read_only=True)
    region = RegionBriefSerializer(read_only=True)

    class Meta:
        model = Inheritor
        fields = (
            "id",
            "name",
            "heritage_item",
            "region",
            "gender",
            "level",
            "area",
            "description",
            "created_at",
            "updated_at",
        )


class InheritorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inheritor
        fields = (
            "id",
            "name",
            "heritage_item",
            "region",
            "gender",
            "level",
            "area",
            "description",
        )
