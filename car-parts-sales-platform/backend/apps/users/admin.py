from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理后台配置"""
    list_display = ('phone', 'nickname', 'email', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active', 'status', 'created_at')
    search_fields = ('phone', 'nickname', 'email')
    ordering = ('-created_at',)

    fieldsets = (
        ('基本信息', {'fields': ('phone', 'password')}),
        ('个人信息', {'fields': ('nickname', 'avatar', 'email', 'first_name', 'last_name')}),
        ('积分与状态', {'fields': ('points', 'status')}),
        ('权限', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('时间信息', {'fields': ('created_at', 'last_login')}),
    )

    add_fieldsets = (
        ('创建用户', {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'nickname'),
        }),
    )

    readonly_fields = ('created_at', 'last_login')

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.readonly_fields
        return self.readonly_fields


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """收货地址管理后台配置"""
    list_display = ('user', 'recipient_name', 'phone', 'address', 'is_default', 'created_at')
    list_filter = ('is_default', 'created_at')
    search_fields = ('recipient_name', 'phone', 'address', 'user__phone')
    ordering = ('-is_default', '-created_at')
    raw_id_fields = ('user',)
