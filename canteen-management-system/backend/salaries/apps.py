from django.apps import AppConfig


class SalariesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "salaries"

    def ready(self):
        """Django 启动时自动更新薪资记录的年月（仅开发环境）"""
        from django.conf import settings
        if settings.DEBUG:
            self._update_salary_year_month()

    def _update_salary_year_month(self):
        """更新薪资记录的 year_month 为最近3个月内，删除多余记录"""
        from datetime import datetime, timedelta
        import random

        from salaries.models import SalaryRecord

        # 获取最近3个月的月份列表
        now = datetime.now()
        months = []
        for i in range(3):
            month_date = now.replace(day=1) - timedelta(days=i * 32)
            month_str = month_date.strftime('%Y-%m')
            months.append(month_str)

        total_updated = 0
        total_deleted = 0

        # 获取所有员工ID
        employee_ids = SalaryRecord.objects.values_list('employee_id', flat=True).distinct()

        # 对每个员工单独处理
        for employee_id in employee_ids:
            # 获取该员工的所有记录，按创建时间降序
            records = list(SalaryRecord.objects.filter(
                employee_id=employee_id
            ).order_by('-created_at'))

            # 只保留前3条记录
            records_to_keep = records[:3]
            records_to_delete = records[3:]

            # 删除多余记录
            if records_to_delete:
                delete_ids = [r.id for r in records_to_delete]
                deleted_count, _ = SalaryRecord.objects.filter(id__in=delete_ids).delete()
                total_deleted += deleted_count

            # 为保留的记录分配不重复的月份
            random.shuffle(months)
            for i, record in enumerate(records_to_keep):
                target_month = months[i % len(months)]
                # 尝试更新，如果月份已被使用则跳过
                try:
                    record.year_month = target_month
                    record.save(update_fields=['year_month'])
                    total_updated += 1
                except Exception:
                    # 如果更新失败（如唯一约束冲突），尝试下一个月份
                    for alt_month in months:
                        if alt_month != target_month:
                            try:
                                record.year_month = alt_month
                                record.save(update_fields=['year_month'])
                                total_updated += 1
                                break
                            except Exception:
                                continue

        import sys
        sys.stdout.flush()
        print(f"[Salaries] 已更新 {total_updated} 条薪资记录的 year_month 为最近3个月内，删除了 {total_deleted} 条多余记录")
        sys.stdout.flush()
