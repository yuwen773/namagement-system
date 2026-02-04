"""
营销管理 - Django Admin 配置
"""
from django.contrib import admin
from .models import Coupon, UserCoupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """优惠券管理后台"""

    list_display = [
        'name', 'discount_type', 'min_amount',
        'discount_amount', 'total_quantity',
        'issued_quantity', 'is_active', 'valid_from', 'valid_until'
    ]
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['name', 'description']
    readonly_fields = ['issued_quantity', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('优惠配置', {
            'fields': ('discount_type', 'min_amount', 'discount_amount', 'discount_rate')
        }),
        ('有效期', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('发放限制', {
            'fields': ('total_quantity', 'per_user_limit', 'issued_quantity')
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ['-created_at']


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    """用户优惠券管理后台"""

    list_display = [
        'user', 'coupon', 'status', 'obtained_at', 'used_at'
    ]
    list_filter = ['status', 'obtained_at', 'used_at']
    search_fields = ['user__phone', 'user__nickname', 'coupon__name']
    readonly_fields = ['user', 'coupon', 'obtained_at']
    ordering = ['-obtained_at']
