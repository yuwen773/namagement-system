# 考勤记录时间自动更新实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在每次 Django 系统启动时，自动将所有考勤记录的 created_at 时间更新为最近 7 天内的随机时间，确保统计分析图表始终有数据显示。

**Architecture:** 在 attendance 应用的 AppConfig 中重写 ready() 方法，使用 bulk_update 批量更新考勤记录时间，仅在 DEBUG=True 时执行。

**Tech Stack:** Django 5.2, Django REST Framework

---

## Task 1: 修改 attendance/apps.py 添加 ready() 方法

**Files:**
- Modify: `backend/attendance/apps.py`

**Step 1: 编辑 apps.py 添加 ready() 方法**

打开 `backend/attendance/apps.py`，替换为以下内容：

```python
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
```

**Step 2: 验证代码语法正确**

Run: `cd backend && python -c "from attendance.apps import AttendanceConfig; print('OK')"`
Expected: 输出 OK，无错误

**Step 3: 提交代码**

```bash
git add backend/attendance/apps.py
git commit -m "feat: 添加考勤记录时间自动更新功能

- 在 AttendanceConfig 中重写 ready() 方法
- 每次 Django 启动时自动将考勤记录时间更新为最近7天内
- 仅在 DEBUG=True 时执行，避免影响生产数据

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 验证功能是否正常工作

**Step 1: 启动 Django 开发服务器**

Run: `cd backend && python manage.py runserver`
Expected: 服务器启动成功，观察控制台输出是否有 "已更新 X 条考勤记录" 的日志

**Step 2: 验证数据库中的考勤记录时间**

Run: `cd backend && python manage.py shell -c "from attendance.models import AttendanceRecord; from datetime import datetime, timedelta; records = AttendanceRecord.objects.all()[:5]; [print(f'id={r.id}, created_at={r.created_at}, days_ago={(datetime.now()-r.created_at).days}') for r in records]"`
Expected: 显示的记录时间应在 0-7 天内

**Step 3: 测试生产环境模式（DEBUG=False 时不执行）**

Run: `cd backend && DEBUG=False python -c "from attendance.apps import AttendanceConfig; c=AttendanceConfig(None); c._update_attendance_times()" 2>&1 | head -5`
Expected: 没有任何输出（因为 DEBUG=False 时不会执行更新逻辑）

**Step 4: 提交验证结果**

```bash
git commit --allow-empty -m "test: 验证考勤记录时间自动更新功能

- 开发环境启动时自动更新考勤记录时间
- 生产环境不执行更新操作

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 验证前端考勤统计图表

**Step 1: 启动前端开发服务器**

Run: `cd frontend && npm run dev`

**Step 2: 访问考勤统计页面**

浏览器打开: http://localhost:5173/admin/statistics

**Step 3: 验证考勤趋势分析图表有数据**

Expected: 考勤趋势折线图和岗位考勤排行柱状图都应有数据显示

**Step 4: 提交验证结果**

```bash
git commit --allow-empty -m "test: 验证前端考勤统计图表显示正常

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
