"""
推荐管理 - Django Admin 配置
"""
from django.contrib import admin
from .models import RecommendationRule, RecommendedProduct


@admin.register(RecommendationRule)
class RecommendationRuleAdmin(admin.ModelAdmin):
    """推荐规则管理后台"""

    list_display = [
        'name', 'rule_type', 'priority', 'limit',
        'is_active', 'created_at'
    ]
    list_filter = ['rule_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'rule_type')
        }),
        ('规则配置', {
            'fields': ('config', 'priority', 'limit', 'is_active')
        }),
        ('时间', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ['-priority', '-created_at']


@admin.register(RecommendedProduct)
class RecommendedProductAdmin(admin.ModelAdmin):
    """推荐商品管理后台"""

    list_display = [
        'rule', 'product', 'sort_order', 'remark', 'created_at'
    ]
    list_filter = ['rule', 'created_at']
    search_fields = ['rule__name', 'product__name', 'remark']
    readonly_fields = ['created_at']
    fieldsets = (
        ('关联信息', {
            'fields': ('rule', 'product')
        }),
        ('配置', {
            'fields': ('sort_order', 'remark')
        }),
        ('时间', {
            'fields': ('created_at',)
        }),
    )
    ordering = ['-sort_order', '-created_at']
