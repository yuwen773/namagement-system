from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

ADMIN_DIV_CODE_VALIDATOR = RegexValidator(
    regex=r"^\d{6}$", message="Administrative division code must be exactly 6 digits."
)


class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=12, unique=True, validators=[ADMIN_DIV_CODE_VALIDATOR]
    )
    level = models.CharField(max_length=20)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.name}({self.code})"


class City(models.Model):
    province = models.ForeignKey(
        Province, on_delete=models.PROTECT, related_name="cities"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=12, unique=True, validators=[ADMIN_DIV_CODE_VALIDATOR]
    )
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.name}({self.code})"


class MonitoringStation(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="stations")
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)
    station_type = models.CharField(max_length=50)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.name}({self.code})"


class AirQualityData(models.Model):
    class QualityLevel(models.TextChoices):
        EXCELLENT = "EXCELLENT", "Excellent"
        GOOD = "GOOD", "Good"
        LIGHT_POLLUTION = "LIGHT_POLLUTION", "Light pollution"
        MODERATE_POLLUTION = "MODERATE_POLLUTION", "Moderate pollution"
        HEAVY_POLLUTION = "HEAVY_POLLUTION", "Heavy pollution"
        SEVERE_POLLUTION = "SEVERE_POLLUTION", "Severe pollution"

    station = models.ForeignKey(
        MonitoringStation, on_delete=models.PROTECT, related_name="air_quality_records"
    )
    monitor_time = models.DateTimeField(db_index=True)

    aqi = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(500)]
    )
    pm25 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    pm10 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    so2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    no2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    co = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    o3 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    quality_level = models.CharField(
        max_length=20, choices=QualityLevel.choices, blank=True
    )

    class Meta:
        ordering = ["-monitor_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["station", "monitor_time"], name="uq_airq_station_monitor_time"
            )
        ]

    @staticmethod
    def _calc_quality_level(aqi: int) -> str:
        # HJ 633-2012 boundaries (inclusive intervals).
        if aqi <= 50:
            return AirQualityData.QualityLevel.EXCELLENT
        if aqi <= 100:
            return AirQualityData.QualityLevel.GOOD
        if aqi <= 150:
            return AirQualityData.QualityLevel.LIGHT_POLLUTION
        if aqi <= 200:
            return AirQualityData.QualityLevel.MODERATE_POLLUTION
        if aqi <= 300:
            return AirQualityData.QualityLevel.HEAVY_POLLUTION
        return AirQualityData.QualityLevel.SEVERE_POLLUTION

    def save(self, *args, **kwargs):
        self.quality_level = self._calc_quality_level(int(self.aqi))
        super().save(*args, **kwargs)
