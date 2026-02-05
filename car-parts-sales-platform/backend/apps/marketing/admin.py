"""
营销管理 - Django Admin 配置
"""
from django.contrib import admin
from .models import Coupon, UserCoupon, Promotion, Banner


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


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """促销活动管理后台"""

    list_display = [
        'name', 'promotion_type', 'coupon', 'start_time',
        'end_time', 'discount_rate', 'discount_amount',
        'sort_order', 'is_active'
    ]
    list_filter = ['promotion_type', 'is_active', 'start_time', 'end_time']
    search_fields = ['name', 'description']
    filter_horizontal = ['products']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'promotion_type', 'is_active')
        }),
        ('关联内容', {
            'fields': ('products', 'coupon')
        }),
        ('活动时间', {
            'fields': ('start_time', 'end_time')
        }),
        ('优惠配置', {
            'fields': ('discount_rate', 'discount_amount')
        }),
        ('展示设置', {
            'fields': ('image', 'sort_order')
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ['-sort_order', '-created_at']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    """Banner 轮播图管理后台"""

    list_display = [
        'title', 'position', 'link_type', 'sort_order',
        'is_active', 'start_time', 'end_time'
    ]
    list_filter = ['position', 'link_type', 'is_active']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'subtitle', 'is_active')
        }),
        ('图片与链接', {
            'fields': ('image', 'link_type', 'link_value')
        }),
        ('展示设置', {
            'fields': ('position', 'sort_order')
        }),
        ('有效时间', {
            'fields': ('start_time', 'end_time')
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ['position', '-sort_order', '-created_at']
