from django.db import models

from apps.categories.models import Category
from apps.regions.models import Region


class HeritageItem(models.Model):
    LEVEL_NATIONAL = "national"
    LEVEL_PROVINCIAL = "provincial"
    LEVEL_CITY_COUNTY = "city_county"
    LEVEL_CHOICES = [
        (LEVEL_NATIONAL, "National"),
        (LEVEL_PROVINCIAL, "Provincial"),
        (LEVEL_CITY_COUNTY, "City/County"),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="heritage_items",
    )
    level = models.CharField(max_length=32, choices=LEVEL_CHOICES, db_index=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="heritage_items",
    )
    area = models.CharField(max_length=128, blank=True, default="")
    protection_unit = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "heritage_items"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["name"], name="heritage_name_idx"),
            models.Index(fields=["category"], name="heritage_category_idx"),
            models.Index(fields=["region"], name="heritage_region_idx"),
        ]

    def __str__(self):
        return self.name
