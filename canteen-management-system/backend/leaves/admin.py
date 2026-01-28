from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    """请假申请管理界面"""

    list_display = [
        'id',
        'employee_name',
        'leave_type_display',
        'start_time',
        'end_time',
        'leave_duration',
        'status_display',
        'approver_name',
        'created_at',
    ]

    list_filter = [
        'leave_type',
        'status',
        'created_at',
        'start_time',
    ]

    search_fields = [
        'employee__name',
        'employee__phone',
        'reason',
        'approval_remark',
    ]

    date_hierarchy = 'start_time'

    fieldsets = (
        ('基本信息', {
            'fields': ('employee', 'leave_type', 'start_time', 'end_time', 'reason'),
            'classes': ('wide',),
        }),
        ('审批信息', {
            'fields': ('status', 'approver', 'approval_remark'),
            'classes': ('wide',),
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'leave_duration']

    def employee_name(self, obj):
        """员工姓名"""
        return obj.employee.name
    employee_name.short_description = '员工姓名'
    employee_name.admin_order_field = 'employee__name'

    def leave_type_display(self, obj):
        """请假类型显示"""
        return obj.get_leave_type_display()
    leave_type_display.short_description = '请假类型'
    leave_type_display.admin_order_field = 'leave_type'

    def status_display(self, obj):
        """审批状态显示"""
        return obj.get_status_display()
    status_display.short_description = '审批状态'
    status_display.admin_order_field = 'status'

    def approver_name(self, obj):
        """审批人姓名"""
        return obj.approver.name if obj.approver else '-'
    approver_name.short_description = '审批人'

    def leave_duration(self, obj):
        """请假天数"""
        return f'{obj.leave_duration_days} 天'
    leave_duration.short_description = '请假天数'
