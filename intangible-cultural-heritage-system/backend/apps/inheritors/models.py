from django.db import models

from apps.heritage.models import HeritageItem
from apps.regions.models import Region


class Inheritor(models.Model):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    ]

    LEVEL_NATIONAL = "national"
    LEVEL_PROVINCIAL = "provincial"
    LEVEL_CITY_COUNTY = "city_county"
    LEVEL_CHOICES = [
        (LEVEL_NATIONAL, "National"),
        (LEVEL_PROVINCIAL, "Provincial"),
        (LEVEL_CITY_COUNTY, "City/County"),
    ]

    name = models.CharField(max_length=128)
    heritage_item = models.ForeignKey(
        HeritageItem,
        on_delete=models.CASCADE,
        related_name="inheritors",
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="inheritors",
    )
    gender = models.CharField(
        max_length=16,
        choices=GENDER_CHOICES,
        blank=True,
        default="",
    )
    level = models.CharField(
        max_length=32,
        choices=LEVEL_CHOICES,
        blank=True,
        default="",
        db_index=True,
    )
    area = models.CharField(max_length=128, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inheritors"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["heritage_item", "name"],
                name="uniq_inheritor_name_per_heritage",
            ),
        ]
        indexes = [
            models.Index(fields=["name"], name="inheritor_name_idx"),
            models.Index(fields=["heritage_item"], name="inheritor_heritage_idx"),
        ]

    def __str__(self):
        return self.name
