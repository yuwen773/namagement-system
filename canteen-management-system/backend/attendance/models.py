from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

from employees.models import EmployeeProfile
from schedules.models import Schedule


class AttendanceRecord(models.Model):
    """考勤记录模型"""

    class Status(models.TextChoices):
        """考勤状态枚举"""
        NORMAL = 'NORMAL', '正常'
        LATE = 'LATE', '迟到'
        EARLY_LEAVE = 'EARLY_LEAVE', '早退'
        MISSING = 'MISSING', '缺卡'
        ABNORMAL = 'ABNORMAL', '异常'

    # 关联信息
    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='员工'
    )
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_records',
        verbose_name='排班'
    )

    # 签到信息
    clock_in_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='签到时间'
    )
    clock_in_location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='签到地点'
    )

    # 签退信息
    clock_out_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='签退时间'
    )
    clock_out_location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='签退地点'
    )

    # 考勤状态
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NORMAL,
        verbose_name='考勤状态'
    )

    # 异常处理
    correction_remark = models.TextField(
        blank=True,
        verbose_name='更正备注'
    )

    # 时间戳
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        db_table = 'attendance_records'
        verbose_name = '考勤记录'
        verbose_name_plural = '考勤记录'
        ordering = ['-clock_in_time']
        # 确保同一员工在同一天只有一条考勤记录
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'schedule'],
                condition=models.Q(schedule__isnull=False),
                name='unique_employee_schedule_attendance'
            )
        ]

    def __str__(self):
        return f'{self.employee.name} - {self.get_status_display()}'

    def clean(self):
        """验证考勤记录"""
        # 签退时间不能早于签到时间
        if self.clock_in_time and self.clock_out_time:
            if self.clock_out_time < self.clock_in_time:
                raise ValidationError({'clock_out_time': '签退时间不能早于签到时间'})

    def save(self, *args, **kwargs):
        """保存时自动判断考勤状态"""
        self.clean()
        # 自动判断考勤状态
        self.status = self._calculate_status()
        super().save(*args, **kwargs)

    def _calculate_status(self):
        """
        根据签到/签退时间和排班信息自动判断考勤状态

        判断规则：
        - 无签到或无签退记录 → MISSING（缺卡）
        - 签到时间 > 班次开始时间 + 5分钟 → LATE（迟到）
        - 签退时间 < 班次结束时间 - 5分钟 → EARLY_LEAVE（早退）
        - 其他 → NORMAL（正常）
        """
        # 检查是否有签到和签退记录
        has_clock_in = self.clock_in_time is not None
        has_clock_out = self.clock_out_time is not None

        # 缺卡判断
        if not has_clock_in or not has_clock_out:
            return self.Status.MISSING

        # 如果没有关联排班，无法判断迟到/早退，返回正常
        if not self.schedule:
            return self.Status.NORMAL

        # 获取班次时间信息
        shift = self.schedule.shift
        work_date = self.schedule.work_date

        # 构建班次开始和结束时间
        from datetime import datetime
        shift_start = datetime.combine(work_date, shift.start_time)
        shift_end = datetime.combine(work_date, shift.end_time)

        # 弹性时间：5分钟
        grace_period = timedelta(minutes=5)

        # 判断迟到：签到时间 > 班次开始时间 + 5分钟
        if self.clock_in_time > shift_start + grace_period:
            return self.Status.LATE

        # 判断早退：签退时间 < 班次结束时间 - 5分钟
        if self.clock_out_time < shift_end - grace_period:
            return self.Status.EARLY_LEAVE

        # 正常
        return self.Status.NORMAL

    def calculate_overtime_hours(self):
        """
        计算加班时长（小时）

        加班定义：签退时间 > 班次结束时间
        返回超过的小时数（保留2位小数）
        """
        if not self.clock_out_time or not self.schedule:
            return 0

        shift = self.schedule.shift
        work_date = self.schedule.work_date

        # 构建班次结束时间
        from datetime import datetime
        shift_end = datetime.combine(work_date, shift.end_time)

        # 计算加班时长
        if self.clock_out_time > shift_end:
            overtime_delta = self.clock_out_time - shift_end
            return round(overtime_delta.total_seconds() / 3600, 2)

        return 0

    @property
    def is_late(self):
        """是否迟到"""
        return self.status == self.Status.LATE

    @property
    def is_early_leave(self):
        """是否早退"""
        return self.status == self.Status.EARLY_LEAVE

    @property
    def is_missing(self):
        """是否缺卡"""
        return self.status == self.Status.MISSING

    @property
    def overtime_hours(self):
        """加班时长"""
        return self.calculate_overtime_hours()
