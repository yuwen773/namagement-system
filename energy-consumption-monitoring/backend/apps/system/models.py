from django.conf import settings
from django.db import models


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
