from django.contrib import admin
from .models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    """考勤记录管理界面"""

    list_display = [
        'id',
        'employee_name',
        'work_date',
        'shift_name',
        'clock_in_time',
        'clock_out_time',
        'status',
        'is_late',
        'is_early_leave',
        'is_missing',
        'overtime_hours',
        'created_at'
    ]
    list_filter = ['status', 'created_at', 'schedule__work_date']
    search_fields = ['employee__name', 'employee__phone', 'clock_in_location', 'clock_out_location']
    date_hierarchy = 'schedule__work_date'
    readonly_fields = ['created_at', 'updated_at', 'status', 'overtime_hours']

    fieldsets = (
        ('基本信息', {
            'fields': ('employee', 'schedule')
        }),
        ('签到信息', {
            'fields': ('clock_in_time', 'clock_in_location')
        }),
        ('签退信息', {
            'fields': ('clock_out_time', 'clock_out_location')
        }),
        ('考勤状态', {
            'fields': ('status', 'overtime_hours')
        }),
        ('异常处理', {
            'fields': ('correction_remark',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def employee_name(self, obj):
        """员工姓名"""
        return obj.employee.name
    employee_name.short_description = '员工姓名'

    def work_date(self, obj):
        """工作日期"""
        if obj.schedule:
            return obj.schedule.work_date
        return '-'
    work_date.short_description = '工作日期'

    def shift_name(self, obj):
        """班次名称"""
        if obj.schedule and obj.schedule.shift:
            return obj.schedule.shift.name
        return '-'
    shift_name.short_description = '班次'

    def is_late(self, obj):
        """是否迟到"""
        return obj.is_late
    is_late.boolean = True
    is_late.short_description = '迟到'

    def is_early_leave(self, obj):
        """是否早退"""
        return obj.is_early_leave
    is_early_leave.boolean = True
    is_early_leave.short_description = '早退'

    def is_missing(self, obj):
        """是否缺卡"""
        return obj.is_missing
    is_missing.boolean = True
    is_missing.short_description = '缺卡'

