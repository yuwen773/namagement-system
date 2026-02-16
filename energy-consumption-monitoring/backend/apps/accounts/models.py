from django.conf import settings
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "管理员"
    USER = "USER", "普通用户"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
    )
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name="手机号")
    avatar = models.CharField(max_length=255, blank=True, null=True, verbose_name="头像")
    role = models.CharField(
        max_length=16,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name="角色",
    )
    bind_rooms = models.JSONField(
        default=list,
        blank=True,
        verbose_name="绑定房间",
        help_text="阶段2.3临时存储房间ID列表，阶段2.4完成后升级为ManyToMany到buildings.Room",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "em_user_profiles"
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"
