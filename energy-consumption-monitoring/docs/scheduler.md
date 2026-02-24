# 阶段 6.4 定时任务说明

采用 `cron` 方案（无需 Celery），通过 Django management command 调度：

- 每小时告警检测：
  - `python manage.py run_scheduled_tasks --task hourly`
- 每日凌晨统计与预测：
  - `python manage.py run_scheduled_tasks --task daily`
- 每周报告：
  - `python manage.py run_scheduled_tasks --task weekly`

Linux `crontab` 示例：

```cron
# 每小时第 5 分钟检查告警
5 * * * * cd /path/to/backend && /path/to/python manage.py run_scheduled_tasks --task hourly >> ../tmp/logs/hourly.log 2>&1

# 每天 00:30 生成统计与预测
30 0 * * * cd /path/to/backend && /path/to/python manage.py run_scheduled_tasks --task daily >> ../tmp/logs/daily.log 2>&1

# 每周一 01:00 生成周报
0 1 * * 1 cd /path/to/backend && /path/to/python manage.py run_scheduled_tasks --task weekly >> ../tmp/logs/weekly.log 2>&1
```

周报会输出到 `tmp/reports/weekly-analysis-YYYY-MM-DD.json`。
