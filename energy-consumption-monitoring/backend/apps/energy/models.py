from django.db import models

from apps.devices.models import Device, EnergyType


class PeriodType(models.TextChoices):
    DAY = "DAY", "Day"
    MONTH = "MONTH", "Month"
    YEAR = "YEAR", "Year"


class EnergyData(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="energy_data",
        verbose_name="device",
    )
    energy_type = models.ForeignKey(
        EnergyType,
        on_delete=models.PROTECT,
        related_name="energy_data",
        verbose_name="energy type",
    )
    timestamp = models.DateTimeField(verbose_name="timestamp")
    value = models.DecimalField(max_digits=18, decimal_places=6, verbose_name="value")
    voltage = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="voltage",
    )
    current = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="current",
    )
    power = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="power",
    )
    flow_rate = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        blank=True,
        null=True,
        verbose_name="flow rate",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_energy_data"
        verbose_name = "energy data"
        verbose_name_plural = "energy data"
        constraints = [
            models.UniqueConstraint(
                fields=["device", "energy_type", "timestamp"],
                name="uk_energy_data_dev_type_ts",
            )
        ]
        indexes = [
            models.Index(fields=["timestamp"], name="idx_energy_data_ts"),
            models.Index(
                fields=["device", "timestamp"],
                name="idx_energy_data_dev_ts",
            ),
            models.Index(
                fields=["energy_type", "timestamp"],
                name="idx_energy_data_type_ts",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.device.device_id}@{self.timestamp}"


class EnergyStatistics(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="energy_statistics",
        verbose_name="device",
    )
    energy_type = models.ForeignKey(
        EnergyType,
        on_delete=models.PROTECT,
        related_name="energy_statistics",
        verbose_name="energy type",
    )
    period_type = models.CharField(
        max_length=16,
        choices=PeriodType.choices,
        verbose_name="period type",
    )
    period_date = models.DateField(verbose_name="period date")
    total_value = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=0,
        verbose_name="total value",
    )
    peak_value = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="peak value",
    )
    peak_time = models.DateTimeField(blank=True, null=True, verbose_name="peak time")
    avg_value = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="avg value",
    )
    cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="cost",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_energy_statistics"
        verbose_name = "energy statistic"
        verbose_name_plural = "energy statistics"
        constraints = [
            models.UniqueConstraint(
                fields=["device", "energy_type", "period_type", "period_date"],
                name="uk_energy_stats_unique_period",
            )
        ]
        indexes = [
            models.Index(
                fields=["period_date"],
                name="idx_energy_stats_period_date",
            ),
            models.Index(
                fields=["period_type", "period_date"],
                name="idx_energy_stats_type_date",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.device.device_id}-{self.period_type}-{self.period_date}"
