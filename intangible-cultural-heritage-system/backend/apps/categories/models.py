from django.db import models


class Category(models.Model):
    LEVEL_NATIONAL = "national"
    LEVEL_PROVINCIAL = "provincial"
    LEVEL_CITY_COUNTY = "city_county"
    LEVEL_CHOICES = [
        (LEVEL_NATIONAL, "National"),
        (LEVEL_PROVINCIAL, "Provincial"),
        (LEVEL_CITY_COUNTY, "City/County"),
    ]

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=64, unique=True)
    level = models.CharField(max_length=32, choices=LEVEL_CHOICES, db_index=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["name"], name="category_name_idx"),
            models.Index(fields=["code"], name="category_code_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.level})"
