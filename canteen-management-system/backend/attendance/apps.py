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
        """更新考勤记录的 created_at 为最近7天内"""
        from datetime import datetime, timedelta
        import random

        from attendance.models import AttendanceRecord

        records = list(AttendanceRecord.objects.all())
        if not records:
            return

        now = datetime.now()

        for record in records:
            # 生成 0-7 天内的随机偏移
            days_offset = random.randint(0, 7)
            hours_offset = random.randint(0, 23)
            minutes_offset = random.randint(0, 59)

            record.created_at = now - timedelta(
                days=days_offset,
                hours=hours_offset,
                minutes=minutes_offset
            )

        # 批量更新
        AttendanceRecord.objects.bulk_update(records, ['created_at'])
        print(f"[Attendance] 已更新 {len(records)} 条考勤记录的时间为最近7天内")
