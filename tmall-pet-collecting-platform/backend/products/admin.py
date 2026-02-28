from django.contrib import admin
from .models import Product, CrawlLog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """商品管理后台"""
    list_display = ['id', 'title', 'price', 'sales', 'shop', 'brand', 'batch_no', 'crawl_time']
    list_filter = ['brand', 'category', 'shop', 'batch_no', 'crawl_time']
    search_fields = ['title', 'shop', 'brand']
    ordering = ['-crawl_time']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(CrawlLog)
class CrawlLogAdmin(admin.ModelAdmin):
    """采集日志管理后台"""
    list_display = ['id', 'task_id', 'status', 'mode', 'source_type', 'items_collected', 'created_at']
    list_filter = ['status', 'mode', 'source_type', 'created_at']
    search_fields = ['task_id']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
