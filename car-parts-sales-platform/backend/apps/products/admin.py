from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image_url', 'sort_order']


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ['attr_name', 'attr_value', 'sort_order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    list_editable = ['sort_order', 'is_active']
    ordering = ['sort_order', 'id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'category', 'price', 'original_price',
        'stock_quantity', 'status', 'sales_count', 'is_featured', 'is_new', 'created_at'
    ]
    list_filter = ['status', 'is_featured', 'is_new', 'category']
    search_fields = ['name', 'description']
    list_editable = ['status', 'is_featured', 'is_new']
    list_per_page = 20
    inlines = [ProductImageInline, ProductAttributeInline]
    readonly_fields = ['sales_count', 'view_count', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'category', 'main_image')
        }),
        ('价格与库存', {
            'fields': ('price', 'original_price', 'stock_quantity')
        }),
        ('状态管理', {
            'fields': ('status', 'is_featured', 'is_new')
        }),
        ('统计信息', {
            'fields': ('sales_count', 'view_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['-created_at']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_url', 'sort_order', 'created_at']
    list_filter = ['product']
    search_fields = ['product__name']
    list_per_page = 20


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'attr_name', 'attr_value', 'sort_order', 'created_at']
    list_filter = ['attr_name', 'product']
    search_fields = ['attr_name', 'attr_value', 'product__name']
    list_per_page = 20
