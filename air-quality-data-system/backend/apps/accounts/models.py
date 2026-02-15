from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """
    Project requirement (per implementation plan): store passwords in plaintext and
    validate in plaintext. This is intentionally insecure and MUST NOT be used in
    production systems.
    """

    class Role(models.TextChoices):
        USER = "USER", "USER"
        ADMIN = "ADMIN", "ADMIN"

    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[0-9+\-() ]{6,20}$",
                message="Phone must be 6-20 chars: digits, spaces, + - ( ) only.",
            )
        ],
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def set_password(self, raw_password):
        # Override Django hashing: store plaintext.
        self.password = raw_password or ""

    def check_password(self, raw_password):
        # Override Django hashing: validate plaintext.
        return (raw_password or "") == (self.password or "")

    def save(self, *args, **kwargs):
        # Keep built-in flags aligned with project fields.
        self.is_active = bool(self.status) and not bool(self.is_deleted)
        if self.is_superuser or self.is_staff:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)
