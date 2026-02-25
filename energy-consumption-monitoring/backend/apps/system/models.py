from django.conf import settings
from django.db import models

from apps.buildings.models import Room
from apps.devices.models import EnergyType


class BillStatus(models.TextChoices):
    UNPAID = "UNPAID", "Unpaid"
    PAID = "PAID", "Paid"


class NoticeType(models.TextChoices):
    NOTICE = "NOTICE", "Notice"
    ANNOUNCEMENT = "ANNOUNCEMENT", "Announcement"
    KNOWLEDGE = "KNOWLEDGE", "Knowledge"


class NoticePriority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    URGENT = "URGENT", "Urgent"


class NoticeTargetRole(models.TextChoices):
    ALL = "ALL", "All"
    ADMIN = "ADMIN", "Admin"
    USER = "USER", "User"


class Bill(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bills",
        verbose_name="room",
    )
    energy_type = models.ForeignKey(
        EnergyType,
        on_delete=models.PROTECT,
        related_name="bills",
        verbose_name="energy type",
    )
    bill_period = models.CharField(max_length=7, verbose_name="bill period")
    usage = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=0,
        verbose_name="usage",
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="amount",
    )
    status = models.CharField(
        max_length=16,
        choices=BillStatus.choices,
        default=BillStatus.UNPAID,
        verbose_name="status",
    )
    due_date = models.DateField(blank=True, null=True, verbose_name="due date")
    paid_time = models.DateTimeField(blank=True, null=True, verbose_name="paid time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_bills"
        verbose_name = "bill"
        verbose_name_plural = "bills"
        constraints = [
            models.UniqueConstraint(
                fields=["room", "energy_type", "bill_period"],
                name="uk_em_bills_room_energy_period",
            )
        ]
        indexes = [
            models.Index(fields=["status"], name="idx_em_bills_status"),
            models.Index(fields=["due_date"], name="idx_em_bills_due_date"),
        ]

    def __str__(self) -> str:
        return f"{self.room_id}-{self.energy_type_id}-{self.bill_period}"


class RechargeRecord(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="recharge_records",
        verbose_name="room",
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="amount")
    payment_method = models.CharField(max_length=32, verbose_name="payment method")
    recharge_time = models.DateTimeField(verbose_name="recharge time")
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="operator_user_id",
        related_name="recharge_records",
        verbose_name="operator",
    )
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name="remark")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_recharge_records"
        verbose_name = "recharge record"
        verbose_name_plural = "recharge records"
        indexes = [
            models.Index(fields=["room"], name="idx_recharge_records_room"),
            models.Index(
                fields=["recharge_time"],
                name="idx_recharge_records_time",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.room_id}-{self.amount}-{self.recharge_time}"


class Notice(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    content = models.TextField(verbose_name="content")
    category = models.CharField(max_length=32, blank=True, null=True, verbose_name="category")
    notice_type = models.CharField(
        max_length=16,
        choices=NoticeType.choices,
        default=NoticeType.NOTICE,
        verbose_name="notice type",
    )
    priority = models.CharField(
        max_length=16,
        choices=NoticePriority.choices,
        default=NoticePriority.MEDIUM,
        verbose_name="priority",
    )
    publish_time = models.DateTimeField(blank=True, null=True, verbose_name="publish time")
    is_published = models.BooleanField(default=False, verbose_name="is published")
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="publisher_user_id",
        related_name="published_notices",
        verbose_name="publisher",
    )
    target_role = models.CharField(
        max_length=16,
        choices=NoticeTargetRole.choices,
        default=NoticeTargetRole.ALL,
        verbose_name="target role",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_notices"
        verbose_name = "notice"
        verbose_name_plural = "notices"
        indexes = [
            models.Index(fields=["notice_type"], name="idx_em_notices_notice_type"),
            models.Index(fields=["publish_time"], name="idx_em_notices_publish_time"),
            models.Index(fields=["is_published"], name="idx_em_notices_is_published"),
        ]

    def __str__(self) -> str:
        return self.title


class OperationLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="operation_logs",
        verbose_name="user",
    )
    action = models.CharField(max_length=64, verbose_name="action")
    resource = models.CharField(max_length=128, verbose_name="resource")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="ip address")
    user_agent = models.CharField(max_length=512, blank=True, null=True, verbose_name="user agent")
    request_method = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        verbose_name="request method",
    )
    request_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="request path",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        db_table = "em_operation_logs"
        verbose_name = "operation log"
        verbose_name_plural = "operation logs"
        indexes = [
            models.Index(fields=["user"], name="idx_em_operation_logs_user_id"),
            models.Index(fields=["action"], name="idx_em_operation_logs_action"),
            models.Index(
                fields=["create_time"],
                name="idx_operation_logs_time",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.action}-{self.resource}-{self.create_time}"
