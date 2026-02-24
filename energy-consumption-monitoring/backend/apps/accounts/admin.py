from django.contrib import admin

from apps.accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "phone",
        "role",
        "bind_rooms",
        "alarm_subscriptions",
        "created_at",
        "updated_at",
    )
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "phone")
