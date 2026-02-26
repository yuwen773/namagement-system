from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    USER_ROLE = [
        ("admin", "管理员"),
        ("user", "普通用户"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
    )
    role = models.CharField(
        max_length=16,
        choices=USER_ROLE,
        default="user",
        db_index=True,
        verbose_name="角色",
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        verbose_name="邮箱",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="手机号",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="账号状态",
    )
    last_login_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="最后登录时间",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_profiles"
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"

    def __str__(self):
        return f"{self.user.username} ({self.role})"


def get_default_role(user):
    if user.is_superuser or user.is_staff:
        return "admin"
    return "user"


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"role": get_default_role(user)},
    )
    return profile.role


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return
    UserProfile.objects.get_or_create(
        user=instance,
        defaults={"role": get_default_role(instance)},
    )
