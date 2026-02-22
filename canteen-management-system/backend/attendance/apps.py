from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "attendance"

    def ready(self):
        """Django 启动时自动更新考勤记录时间（仅开发环境）"""
        from django.conf import settings
        if settings.DEBUG:
            self._update_attendance_times()

    def _update_attendance_times(self):
        """更新所有时间相关字段为最近7天内"""
        from datetime import timedelta
        import random
        from django.utils import timezone

        from attendance.models import AttendanceRecord
        from salaries.models import SalaryRecord, Appeal
        from schedules.models import Schedule, Shift, ShiftSwapRequest
        from leaves.models import LeaveRequest

        now = timezone.now()
        total_updated = 0

        # 1. 更新考勤记录
        attendance_records = list(AttendanceRecord.objects.all())
        for record in attendance_records:
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            minutes_offset = random.randint(0, 59)
            offset = timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)

            if record.created_at:
                record.created_at = now - offset
            if record.clock_in_time:
                record.clock_in_time = now - offset - timedelta(hours=random.randint(1, 8))
            if record.clock_out_time:
                record.clock_out_time = now - offset - timedelta(hours=random.randint(0, 2))

        if attendance_records:
            AttendanceRecord.objects.bulk_update(attendance_records, ['created_at', 'clock_in_time', 'clock_out_time'])
            total_updated += len(attendance_records)

        # 2. 更新薪资记录
        salary_records = list(SalaryRecord.objects.all())
        for record in salary_records:
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            record.created_at = now - timedelta(days=days_offset, hours=hours_offset)

        if salary_records:
            SalaryRecord.objects.bulk_update(salary_records, ['created_at'])
            total_updated += len(salary_records)

        # 3. 更新申诉记录
        appeals = list(Appeal.objects.all())
        for record in appeals:
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            record.created_at = now - timedelta(days=days_offset, hours=hours_offset)

        if appeals:
            Appeal.objects.bulk_update(appeals, ['created_at'])
            total_updated += len(appeals)

        # 4. 更新排班记录
        schedules = list(Schedule.objects.all())
        for record in schedules:
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            record.created_at = now - timedelta(days=days_offset, hours=hours_offset)

        if schedules:
            Schedule.objects.bulk_update(schedules, ['created_at'])
            total_updated += len(schedules)

        # 5. 更新班次记录
        shifts = list(Shift.objects.all())
        for record in shifts:
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            record.created_at = now - timedelta(days=days_offset, hours=hours_offset)

        if shifts:
            Shift.objects.bulk_update(shifts, ['created_at'])
            total_updated += len(shifts)

        # 6. 更新换班申请记录
        swap_requests = list(ShiftSwapRequest.objects.all())
        for record in swap_requests:
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            record.created_at = now - timedelta(days=days_offset, hours=hours_offset)

        if swap_requests:
            ShiftSwapRequest.objects.bulk_update(swap_requests, ['created_at'])
            total_updated += len(swap_requests)

        # 7. 更新请假记录
        leave_requests = list(LeaveRequest.objects.all())
        for record in leave_requests:
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            record.created_at = now - timedelta(days=days_offset, hours=hours_offset)
            # 也更新请假时间
            if record.start_time:
                record.start_time = now - timedelta(days=random.randint(0, 3), hours=random.randint(9, 18))
            if record.end_time:
                record.end_time = now + timedelta(days=random.randint(1, 5), hours=random.randint(9, 18))

        if leave_requests:
            LeaveRequest.objects.bulk_update(leave_requests, ['created_at', 'start_time', 'end_time'])
            total_updated += len(leave_requests)

        import sys
        sys.stdout.flush()
        print(f"[Attendance] 已更新 {total_updated} 条记录的时间为最近7天内")
        sys.stdout.flush()
