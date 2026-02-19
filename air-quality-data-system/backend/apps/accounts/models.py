from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class PlaintextUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = password or ""
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)


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
                message="手机号格式不正确，应为6-20位数字，可包含空格和+-()符号",
            )
        ],
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    objects = PlaintextUserManager()

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
