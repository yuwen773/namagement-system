# 考勤记录时间自动更新设计方案

## 需求背景

管理端的统计分析功能（考勤趋势分析、岗位考勤排行）在时隔一段时间后会出现图表无数据的情况。原因是测试阶段系统不会 24 小时运行，数据库中的考勤记录时间较早，超出了默认的"最近 7 天"查询范围。

## 解决方案

在每次 Django 系统启动时，自动将所有考勤记录的 `created_at` 时间更新为最近 7 天内的随机时间。

## 设计方案

### 1. 实现位置

在 `backend/apps/attendance/apps.py` 中重写 `AppConfig.ready()` 方法。

### 2. 实现逻辑

```python
def ready(self):
    """Django 启动时自动更新考勤记录时间"""
    from apps.attendance.models import AttendanceRecord
    from datetime import datetime, timedelta
    import random

    # 只在开发环境执行
    if settings.DEBUG:
        self._update_attendance_times()

def _update_attendance_times(self):
    """更新考勤记录的 created_at 为最近7天内"""
    records = AttendanceRecord.objects.all()
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
```

### 3. 配置开关

在 `settings.py` 中添加配置项控制是否执行：

```python
# 开发环境配置
AUTO_UPDATE_ATTENDANCE_TIMES = DEBUG  # 或显式设置
```

### 4. 关键约束

- 仅在 `DEBUG=True` 时执行，避免影响生产数据
- 只更新 `created_at` 时间字段，不改变其他业务数据
- 使用批量更新 (`bulk_update`) 提高性能

## 影响范围

- `backend/apps/attendance/apps.py` - 添加 ready() 方法
- `backend/config/settings.py` - 添加配置项（可选）

## 测试要点

1. 验证服务重启后考勤记录时间确实被更新
2. 验证前端考勤统计图表能正常显示数据
3. 验证生产环境 (`DEBUG=False`) 不会执行更新
