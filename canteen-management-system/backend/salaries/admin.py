from django.contrib import admin
from .models import SalaryRecord, Appeal


@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    """薪资记录管理界面"""
    list_display = [
        'id', 'employee_name', 'employee_position', 'year_month',
        'base_salary', 'position_allowance', 'overtime_pay', 'deductions',
        'total_salary', 'status', 'work_days', 'late_count', 'missing_count',
        'overtime_hours', 'created_at'
    ]
    list_filter = ['status', 'year_month', 'employee__position', 'created_at']
    search_fields = ['employee__name', 'employee__phone', 'remark']
    date_hierarchy = 'created_at'
    ordering = ['-year_month', '-created_at']

    fieldsets = (
        ('基本信息', {
            'fields': ('employee', 'year_month', 'status')
        }),
        ('薪资组成', {
            'fields': ('base_salary', 'position_allowance', 'overtime_pay', 'deductions', 'total_salary')
        }),
        ('统计数据', {
            'fields': ('work_days', 'late_count', 'missing_count', 'overtime_hours')
        }),
        ('备注', {
            'fields': ('remark',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at', 'total_salary']

    def employee_name(self, obj):
        """员工姓名"""
        return obj.employee.name
    employee_name.short_description = '员工姓名'

    def employee_position(self, obj):
        """员工岗位"""
        return obj.employee.get_position_display()
    employee_position.short_description = '岗位'


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    """异常申诉管理界面"""
    list_display = [
        'id', 'appeal_type_display', 'employee_name', 'target_info',
        'status', 'approver_name', 'created_at'
    ]
    list_filter = ['appeal_type', 'status', 'created_at']
    search_fields = ['employee__name', 'reason', 'approval_remark']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('申诉信息', {
            'fields': ('appeal_type', 'employee', 'target_id', 'reason')
        }),
        ('审批信息', {
            'fields': ('status', 'approver', 'approval_remark')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def appeal_type_display(self, obj):
        """申诉类型显示"""
        return obj.get_appeal_type_display()
    appeal_type_display.short_description = '申诉类型'

    def employee_name(self, obj):
        """员工姓名"""
        return obj.employee.name
    employee_name.short_description = '申诉员工'

    def target_info(self, obj):
        """目标记录信息"""
        return f"{obj.get_appeal_type_display()} (ID: {obj.target_id})"
    target_info.short_description = '目标记录'

    def approver_name(self, obj):
        """审批人姓名"""
        return obj.approver.name if obj.approver else '-'
    approver_name.short_description = '审批人'
