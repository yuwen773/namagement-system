from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "status", "is_deleted", "is_staff")
    list_filter = ("role", "status", "is_deleted", "is_staff", "is_superuser")
    search_fields = ("username", "email", "phone")
