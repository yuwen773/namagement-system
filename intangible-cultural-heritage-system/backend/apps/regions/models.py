from django.core.validators import RegexValidator
from django.db import models


class Region(models.Model):
    ISO_3166_NAME_MAP = {
        "CHINA": "CN",
        "PEOPLE'S REPUBLIC OF CHINA": "CN",
        "UNITED STATES": "US",
        "UNITED STATES OF AMERICA": "US",
        "JAPAN": "JP",
        "SOUTH KOREA": "KR",
        "REPUBLIC OF KOREA": "KR",
        "FRANCE": "FR",
        "GERMANY": "DE",
        "ITALY": "IT",
        "SPAIN": "ES",
        "UNITED KINGDOM": "GB",
    }

    country_code = models.CharField(
        max_length=3,
        unique=True,
        validators=[RegexValidator(regex=r"^[A-Z]{2,3}$")],
    )
    country_name = models.CharField(max_length=128, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    continent = models.CharField(max_length=64, blank=True, default="")

    class Meta:
        db_table = "regions"
        ordering = ["country_name"]
        indexes = [
            models.Index(fields=["country_code"], name="region_code_idx"),
            models.Index(fields=["country_name"], name="region_name_idx"),
        ]

    def __str__(self):
        return f"{self.country_name} ({self.country_code})"

    @classmethod
    def normalize_country_code(cls, country_name):
        if not country_name:
            return ""
        return cls.ISO_3166_NAME_MAP.get(country_name.strip().upper(), "")
