from django.db import models
from django.conf import settings
from organization.models import Department, Post


class Attendance(models.Model):
    """考勤记录模型"""

    class Status(models.TextChoices):
        NORMAL = 'normal', '正常'
        LATE = 'late', '迟到'
        EARLY = 'early', '早退'
        LEAVE = 'leave', '休假'
        ABSENT = 'absent', '缺勤'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='用户'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='部门'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='岗位'
    )
    date = models.DateField(
        db_index=True,
        verbose_name='考勤日期'
    )
    check_in_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='签到时间'
    )
    check_out_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='签退时间'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NORMAL,
        verbose_name='考勤状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'attendance_attendance'
        ordering = ['-date', '-created_at']
        unique_together = ['user', 'date']
        verbose_name = '考勤记录'
        verbose_name_plural = '考勤记录'

    def __str__(self):
        return f'{self.user.real_name} - {self.date} - {self.get_status_display()}'

    def calculate_status(self):
        """根据签到签退时间计算考勤状态"""
        from datetime import time

        work_start = time(9, 0)   # 上班时间 09:00
        work_end = time(18, 0)    # 下班时间 18:00

        # 状态判断逻辑
        if self.check_in_time and self.check_out_time:
            # 既有签到又有签退
            if self.check_in_time > work_start and self.check_out_time < work_end:
                # 迟到且早退
                return self.Status.LATE if self.check_in_time > work_start else self.Status.NORMAL
            elif self.check_in_time > work_start:
                return self.Status.LATE
            elif self.check_out_time < work_end:
                return self.Status.EARLY
            else:
                return self.Status.NORMAL
        elif self.check_in_time:
            # 只有签到
            if self.check_in_time > work_start:
                return self.Status.LATE
            return self.Status.NORMAL
        elif self.check_out_time:
            # 只有签退
            if self.check_out_time < work_end:
                return self.Status.EARLY
            return self.Status.NORMAL
        else:
            # 没有打卡记录
            return self.Status.ABSENT

    def save(self, *args, **kwargs):
        """保存时自动计算状态并补充部门岗位信息"""
        # 如果有打卡时间，先计算状态
        if self.check_in_time or self.check_out_time:
            self.status = self.calculate_status()
        
        # 自动补充部门和岗位信息（快照）
        if not self.department or not self.post:
            try:
                # 优先使用 profile 关联名（根据 employee/models.py）
                profile = getattr(self.user, 'profile', None)
                if not profile:
                    # 备选使用 employeeprofile (防止关联名冲突或未定义)
                    profile = getattr(self.user, 'employeeprofile', None)
                
                if profile:
                    if not self.department:
                        self.department = profile.department
                    if not self.post:
                        self.post = profile.post
            except Exception:
                pass

        super().save(*args, **kwargs)
