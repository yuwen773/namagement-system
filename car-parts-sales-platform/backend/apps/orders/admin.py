"""
订单管理 - Django Admin 配置
"""
from django.contrib import admin
from .models import Order, OrderItem, ReturnRequest


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单管理后台"""

    list_display = [
        'order_no', 'user', 'status', 'total_amount',
        'pay_amount', 'express_company', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['order_no', 'user__phone', 'user__nickname', 'recipient_name', 'recipient_phone']
    readonly_fields = [
        'order_no', 'user', 'total_amount', 'discount_amount',
        'pay_amount', 'created_at', 'updated_at', 'paid_at',
        'shipped_at', 'completed_at'
    ]
    fieldsets = (
        ('基本信息', {
            'fields': ('order_no', 'user', 'status')
        }),
        ('收货信息', {
            'fields': (
                'recipient_name', 'recipient_phone',
                'recipient_province', 'recipient_city',
                'recipient_district', 'recipient_address'
            )
        }),
        ('金额信息', {
            'fields': ('total_amount', 'discount_amount', 'shipping_fee', 'pay_amount', 'coupon')
        }),
        ('物流信息', {
            'fields': ('express_company', 'tracking_number')
        }),
        ('其他', {
            'fields': ('remark', 'created_at', 'updated_at', 'paid_at', 'shipped_at', 'completed_at')
        }),
    )
    ordering = ['-created_at']

    def has_add_permission(self, request):
        """禁止通过后台手动创建订单"""
        return False

    def has_delete_permission(self, request, obj=None):
        """只有超级用户可以删除订单"""
        return request.user.is_superuser


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """订单商品管理后台"""

    list_display = [
        'id', 'order', 'product_name', 'product_price',
        'quantity', 'subtotal', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['order__order_no', 'product_name']
    readonly_fields = ['order', 'product', 'subtotal', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        """禁止通过后台手动创建订单商品"""
        return False

    def has_change_permission(self, request, obj=None):
        """订单商品不可修改"""
        return False

    def has_delete_permission(self, request, obj=None):
        """只有超级用户可以删除订单商品"""
        return request.user.is_superuser


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    """退换货申请管理后台"""

    list_display = [
        'id', 'order', 'request_type', 'status',
        'reason_preview', 'created_at', 'processed_at'
    ]
    list_filter = ['status', 'request_type', 'created_at']
    search_fields = ['order__order_no', 'order__user__phone', 'reason']
    readonly_fields = ['order', 'request_type', 'reason', 'evidence_images', 'created_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('order', 'request_type', 'status')
        }),
        ('申请详情', {
            'fields': ('reason', 'evidence_images')
        }),
        ('处理信息', {
            'fields': ('admin_note', 'processed_at')
        }),
        ('时间', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']

    def reason_preview(self, obj):
        """原因预览（截取前50字符）"""
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    reason_preview.short_description = '退换货原因'

    def has_add_permission(self, request):
        """禁止通过后台手动创建退换货申请"""
        return False

    def has_delete_permission(self, request, obj=None):
        """只有超级用户可以删除退换货申请"""
        return request.user.is_superuser
