from django.conf import settings
from django.db import models

from apps.devices.models import Device, EnergyType


class ConditionType(models.TextChoices):
    THRESHOLD = "THRESHOLD", "Threshold"
    MUTATION = "MUTATION", "Mutation"


class AlarmType(models.TextChoices):
    THRESHOLD = "THRESHOLD", "Threshold"
    MUTATION = "MUTATION", "Mutation"
    OFFLINE = "OFFLINE", "Offline"


class AlarmStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PROCESSED = "PROCESSED", "Processed"
    IGNORED = "IGNORED", "Ignored"


class AlarmRule(models.Model):
    name = models.CharField(max_length=128, verbose_name="rule name")
    energy_type = models.ForeignKey(
        EnergyType,
        on_delete=models.PROTECT,
        related_name="alarm_rules",
        verbose_name="energy type",
    )
    condition_type = models.CharField(
        max_length=16,
        choices=ConditionType.choices,
        verbose_name="condition type",
    )
    threshold_value = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        verbose_name="threshold value",
    )
    is_active = models.BooleanField(default=True, verbose_name="is active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_alarm_rules"
        verbose_name = "alarm rule"
        verbose_name_plural = "alarm rules"
        indexes = [
            models.Index(
                fields=["energy_type"],
                name="idx_alarm_rules_energy_type",
            ),
            models.Index(fields=["is_active"], name="idx_em_alarm_rules_is_active"),
        ]

    def __str__(self) -> str:
        return self.name


class Alarm(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="alarms",
        verbose_name="device",
    )
    rule = models.ForeignKey(
        AlarmRule,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="alarms",
        verbose_name="alarm rule",
    )
    alarm_type = models.CharField(
        max_length=16,
        choices=AlarmType.choices,
        verbose_name="alarm type",
    )
    alarm_value = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="alarm value",
    )
    alarm_time = models.DateTimeField(verbose_name="alarm time")
    status = models.CharField(
        max_length=16,
        choices=AlarmStatus.choices,
        default=AlarmStatus.PENDING,
        verbose_name="status",
    )
    handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="handler_user_id",
        related_name="handled_alarms",
        verbose_name="handler",
    )
    handle_time = models.DateTimeField(blank=True, null=True, verbose_name="handle time")
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name="remark")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_alarms"
        verbose_name = "alarm"
        verbose_name_plural = "alarms"
        indexes = [
            models.Index(fields=["device"], name="idx_em_alarms_device_id"),
            models.Index(fields=["rule"], name="idx_em_alarms_rule_id"),
            models.Index(fields=["alarm_time"], name="idx_em_alarms_alarm_time"),
            models.Index(fields=["status"], name="idx_em_alarms_status"),
        ]

    def __str__(self) -> str:
        return f"{self.device.device_id}-{self.alarm_type}-{self.alarm_time}"
