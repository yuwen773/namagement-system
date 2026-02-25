from rest_framework import serializers

from apps.categories.models import Category
from apps.regions.models import Region

from .models import HeritageItem


class CategoryBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "code", "level")


class RegionBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("id", "country_code", "country_name", "continent")


class HeritageItemReadSerializer(serializers.ModelSerializer):
    category = CategoryBriefSerializer(read_only=True)
    region = RegionBriefSerializer(read_only=True)

    class Meta:
        model = HeritageItem
        fields = (
            "id",
            "name",
            "category",
            "level",
            "region",
            "area",
            "protection_unit",
            "description",
            "created_at",
            "updated_at",
        )


class HeritageItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeritageItem
        fields = (
            "id",
            "name",
            "category",
            "level",
            "region",
            "area",
            "protection_unit",
            "description",
        )
