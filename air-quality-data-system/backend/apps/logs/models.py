from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class OperationLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="operation_logs"
    )
    operation_type = models.CharField(max_length=50)
    operation_content = models.TextField()
    ip_address = models.CharField(max_length=45)
    operation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-operation_time", "-id"]

    def __str__(self):
        return f"{self.operation_type} by {self.user_id} @ {self.operation_time}"


class ErrorLog(models.Model):
    error_type = models.CharField(max_length=100)
    error_message = models.TextField()
    stack_trace = models.TextField()
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at", "-id"]

    def __str__(self):
        return f"{self.error_type} @ {self.occurred_at}"


class ImportTask(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        RUNNING = "RUNNING", "RUNNING"
        SUCCESS = "SUCCESS", "SUCCESS"
        FAILED = "FAILED", "FAILED"

    task_id = models.CharField(max_length=64, unique=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    success_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    failed_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="import_tasks"
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-start_time", "-id"]

    def __str__(self):
        return f"{self.task_id} ({self.status})"


class ImportTaskLog(models.Model):
    task = models.ForeignKey(ImportTask, on_delete=models.CASCADE, related_name="logs")
    row_number = models.IntegerField(validators=[MinValueValidator(1)])
    error_reason = models.TextField()
    raw_data_snippet = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.task.task_id} row {self.row_number}"
