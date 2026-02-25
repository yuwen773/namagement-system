from django.conf import settings
from django.db import models


class ImportJob(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    file_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )
    total_rows = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="import_jobs",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "import_jobs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"], name="import_job_status_idx"),
            models.Index(fields=["created_by"], name="import_job_creator_idx"),
        ]

    def __str__(self):
        return f"{self.file_name} ({self.status})"


class ImportError(models.Model):
    import_job = models.ForeignKey(
        ImportJob,
        on_delete=models.CASCADE,
        related_name="errors",
    )
    row_number = models.PositiveIntegerField()
    field_name = models.CharField(max_length=128, blank=True, default="")
    error_message = models.TextField()
    raw_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "import_errors"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["import_job", "row_number"], name="import_error_row_idx"),
        ]

    def __str__(self):
        return f"Job {self.import_job_id} row {self.row_number}"
