from django.db import models

from apps.buildings.models import Building, Campus
from apps.devices.models import Device, EnergyType


class ForecastTargetType(models.TextChoices):
    CAMPUS = "CAMPUS", "Campus"
    BUILDING = "BUILDING", "Building"
    METER = "METER", "Meter"


class EnergyForecast(models.Model):
    target_type = models.CharField(
        max_length=16,
        choices=ForecastTargetType.choices,
        verbose_name="target type",
    )
    target_id = models.CharField(max_length=64, verbose_name="target id")
    energy_type = models.ForeignKey(
        EnergyType,
        on_delete=models.PROTECT,
        related_name="forecasts",
        verbose_name="energy type",
    )
    forecast_date = models.DateField(verbose_name="forecast date")
    forecast_value = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="forecast value")
    horizon_days = models.PositiveIntegerField(default=7, verbose_name="horizon days")
    model_version = models.CharField(max_length=64, default="linear-v1", verbose_name="model version")
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="forecasts",
        verbose_name="campus",
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="forecasts",
        verbose_name="building",
    )
    meter = models.ForeignKey(
        Device,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="forecasts",
        verbose_name="meter",
    )
    room_id = models.BigIntegerField(blank=True, null=True, verbose_name="room id")
    department = models.CharField(max_length=128, blank=True, null=True, verbose_name="department")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_energy_forecasts"
        verbose_name = "energy forecast"
        verbose_name_plural = "energy forecasts"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "target_type",
                    "target_id",
                    "energy_type",
                    "forecast_date",
                    "horizon_days",
                ],
                name="uk_em_energy_forecast_target_type_id_date",
            )
        ]
        indexes = [
            models.Index(fields=["target_type", "target_id"], name="idx_forecast_target"),
            models.Index(fields=["forecast_date"], name="idx_forecast_date"),
            models.Index(fields=["energy_type"], name="idx_forecast_energy_type"),
            models.Index(fields=["campus"], name="idx_forecast_campus"),
            models.Index(fields=["building"], name="idx_forecast_building"),
            models.Index(fields=["meter"], name="idx_forecast_meter"),
        ]

    def __str__(self) -> str:
        return f"{self.target_type}:{self.target_id}@{self.forecast_date}"
