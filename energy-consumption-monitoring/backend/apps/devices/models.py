from django.db import models

from apps.buildings.models import Room


class EnergyCode(models.TextChoices):
    WATER = "WATER", "Water"
    ELECTRICITY = "ELECTRICITY", "Electricity"
    GAS = "GAS", "Gas"


class DeviceStatus(models.TextChoices):
    ONLINE = "ONLINE", "Online"
    OFFLINE = "OFFLINE", "Offline"
    FAULT = "FAULT", "Fault"


class EnergyType(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="energy name")
    code = models.CharField(
        max_length=32,
        unique=True,
        choices=EnergyCode.choices,
        verbose_name="energy code",
    )
    unit = models.CharField(max_length=32, verbose_name="unit")
    icon = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="icon",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_energy_types"
        verbose_name = "energy type"
        verbose_name_plural = "energy types"

    def __str__(self) -> str:
        return f"{self.name}({self.code})"


class Device(models.Model):
    device_id = models.CharField(max_length=64, unique=True, verbose_name="device id")
    name = models.CharField(max_length=128, verbose_name="device name")
    energy_type = models.ForeignKey(
        EnergyType,
        on_delete=models.PROTECT,
        related_name="devices",
        verbose_name="energy type",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        related_name="devices",
        blank=True,
        null=True,
        verbose_name="room",
    )
    model = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name="device model",
    )
    status = models.CharField(
        max_length=16,
        choices=DeviceStatus.choices,
        default=DeviceStatus.OFFLINE,
        verbose_name="device status",
    )
    last_data_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="last data time",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_devices"
        verbose_name = "device"
        verbose_name_plural = "devices"
        indexes = [
            models.Index(fields=["energy_type"], name="idx_em_devices_energy_type_id"),
            models.Index(fields=["room"], name="idx_em_devices_room_id"),
            models.Index(fields=["status"], name="idx_em_devices_status"),
        ]

    def __str__(self) -> str:
        return f"{self.name}({self.device_id})"
