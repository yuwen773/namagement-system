from django.conf import settings
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


class Achievement(models.Model):
    code = models.CharField(max_length=64, unique=True, verbose_name="achievement code")
    name = models.CharField(max_length=128, verbose_name="achievement name")
    description = models.CharField(max_length=255, blank=True, default="", verbose_name="description")
    icon = models.CharField(max_length=64, blank=True, default="", verbose_name="icon")
    points = models.PositiveIntegerField(default=0, verbose_name="points")
    is_active = models.BooleanField(default=True, verbose_name="is active")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="sort order")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_achievements"
        verbose_name = "achievement"
        verbose_name_plural = "achievements"
        ordering = ["sort_order", "id"]
        indexes = [
            models.Index(fields=["is_active", "sort_order"], name="idx_achievement_active_sort"),
        ]

    def __str__(self) -> str:
        return f"{self.code}:{self.name}"


class UserAchievement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_achievements",
        verbose_name="user",
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="user_achievements",
        verbose_name="achievement",
    )
    unlocked = models.BooleanField(default=False, verbose_name="unlocked")
    progress = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="progress")
    unlocked_at = models.DateTimeField(blank=True, null=True, verbose_name="unlocked at")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="metadata")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_user_achievements"
        verbose_name = "user achievement"
        verbose_name_plural = "user achievements"
        constraints = [
            models.UniqueConstraint(fields=["user", "achievement"], name="uk_user_achv_user_achv"),
        ]
        indexes = [
            models.Index(fields=["user", "unlocked"], name="idx_user_achv_user_unlock"),
        ]

    def __str__(self) -> str:
        return f"user={self.user_id},achievement={self.achievement_id},unlocked={self.unlocked}"
