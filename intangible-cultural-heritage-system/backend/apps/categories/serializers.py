from rest_framework import serializers

from .models import Category


class CategoryParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "code", "level")


class CategoryReadSerializer(serializers.ModelSerializer):
    parent = CategoryParentSerializer(read_only=True)
    parent_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "code",
            "level",
            "parent",
            "parent_id",
            "created_at",
            "updated_at",
        )


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "code", "level", "parent")
