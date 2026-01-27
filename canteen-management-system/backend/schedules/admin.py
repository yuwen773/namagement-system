from django.contrib import admin
from .models import Shift, Schedule, ShiftSwapRequest


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    """班次定义管理界面"""
    list_display = ['id', 'name', 'start_time', 'end_time', 'created_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['start_time']

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'start_time', 'end_time')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """排班计划管理界面"""
    list_display = ['id', 'employee_name', 'shift_name', 'work_date', 'is_swapped', 'created_at']
    list_filter = ['shift', 'work_date', 'is_swapped', 'created_at']
    search_fields = ['employee__name', 'employee__phone']
    ordering = ['-work_date', 'shift__start_time']
    date_hierarchy = 'work_date'

    def employee_name(self, obj):
        return obj.employee.name
    employee_name.short_description = '员工'

    def shift_name(self, obj):
        return obj.shift.name
    shift_name.short_description = '班次'

    fieldsets = (
        ('排班信息', {
            'fields': ('employee', 'shift', 'work_date', 'is_swapped')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']


@admin.register(ShiftSwapRequest)
class ShiftSwapRequestAdmin(admin.ModelAdmin):
    """调班申请管理界面"""
    list_display = [
        'id', 'requester_name', 'original_info', 'target_info',
        'status', 'approver_name', 'created_at'
    ]
    list_filter = ['status', 'target_date', 'created_at']
    search_fields = ['requester__name', 'reason', 'approval_remark']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def requester_name(self, obj):
        return obj.requester.name
    requester_name.short_description = '发起人'

    def original_info(self, obj):
        return f'{obj.original_schedule.work_date} {obj.original_schedule.shift.name}'
    original_info.short_description = '原定排班'

    def target_info(self, obj):
        return f'{obj.target_date} {obj.target_shift.name}'
    target_info.short_description = '目标排班'

    def approver_name(self, obj):
        return obj.approver.name if obj.approver else '-'
    approver_name.short_description = '审批人'

    fieldsets = (
        ('申请信息', {
            'fields': ('requester', 'original_schedule', 'target_date', 'target_shift', 'reason')
        }),
        ('审批信息', {
            'fields': ('status', 'approver', 'approval_remark')
        }),
        ('时间信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
