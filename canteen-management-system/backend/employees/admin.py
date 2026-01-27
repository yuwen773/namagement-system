from django.contrib import admin
from .models import EmployeeProfile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    """
    员工档案管理界面
    """
    list_display = [
        'id', 'name', 'gender', 'phone', 'position',
        'entry_date', 'status', 'created_at'
    ]
    list_filter = ['position', 'status', 'gender', 'created_at']
    search_fields = ['name', 'phone', 'id_card']
    list_per_page = 20

    fieldsets = (
        ('基础信息', {
            'fields': ('name', 'gender', 'phone', 'id_card', 'address')
        }),
        ('岗位信息', {
            'fields': ('position', 'entry_date', 'status')
        }),
        ('资质证书', {
            'fields': ('health_certificate_no', 'health_certificate_expiry',
                      'health_certificate_url', 'chef_certificate_level')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    ordering = ['-created_at']
