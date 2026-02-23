"""
Django Management Command: 导入 360 问答 CSV 数据

使用方法:
    python manage.py import_csv --file=script/360q&a/360_qa.csv
    python manage.py import_csv --file=script/360q&a/360_qa.csv --dry-run
    python manage.py import_csv --file=script/360q&a/360_qa.csv --batch-size=200
"""
import os
import sys
import time

from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError

from apps.crawler.management.utils.csv_importer import CSVImporter


class Command(BaseCommand):
    help = '从 CSV 文件导入 360 问答数据到数据库'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_progress_length = 0

    def add_arguments(self, parser):
        """添加命令行参数"""
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='CSV 文件路径（相对于项目根目录或绝对路径）'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='批量插入大小（默认: 100）'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='预览模式，不实际写入数据库'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='详细输出模式'
        )

    def handle(self, *args, **options):
        """命令处理逻辑"""
        file_path = options['file']
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        verbose = options['verbose']

        # 处理文件路径
        if not os.path.isabs(file_path):
            # 相对于项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            file_path = os.path.join(project_root, '..', file_path)
            file_path = os.path.abspath(file_path)

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise CommandError(f"CSV 文件不存在: {file_path}")

        # 打印配置信息
        if verbose:
            self.stdout.write(self.style.SUCCESS("=" * 60))
            self.stdout.write(self.style.SUCCESS("360 问答 CSV 数据导入工具"))
            self.stdout.write(self.style.SUCCESS("=" * 60))
            self.stdout.write(f"文件: {file_path}")
            self.stdout.write(f"批量大小: {batch_size}")
            self.stdout.write(f"模式: {'预览模式（不写入数据库）' if dry_run else '正式导入'}")
            self.stdout.write("")

        # 创建导入器
        importer = CSVImporter(file_path, batch_size=batch_size)

        # 统计开始时间
        start_time = time.time()

        try:
            # 执行导入
            result = importer.bulk_import(
                dry_run=dry_run,
                verbose=verbose,
                progress_callback=self._progress_callback if not verbose else None
            )

            # 统计结束时间
            elapsed_time = time.time() - start_time

            # 打印结果
            if not verbose:
                # 非详细模式，清除进度行
                self._clear_progress()

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("=" * 60))
            self.stdout.write(self.style.SUCCESS("导入完成"))
            self.stdout.write(self.style.SUCCESS("=" * 60))
            self.stdout.write(f"  总计: {result.total} 条")
            self.stdout.write(self.style.SUCCESS(f"  成功: {result.success} 条"))
            if result.skipped > 0:
                self.stdout.write(self.style.WARNING(f"  跳过: {result.skipped} 条 (重复数据)"))
            if result.failed > 0:
                self.stdout.write(self.style.ERROR(f"  失败: {result.failed} 条"))
            self.stdout.write(f"  耗时: {elapsed_time:.2f} 秒")

            if result.errors:
                self.stdout.write("")
                self.stdout.write(self.style.ERROR("错误详情:"))
                for error in result.errors[:10]:
                    self.stdout.write(self.style.ERROR(f"  - {error}"))
                if len(result.errors) > 10:
                    self.stdout.write(self.style.WARNING(f"  ... 还有 {len(result.errors) - 10} 条错误"))

            # 如果是预览模式，额外提示
            if dry_run:
                self.stdout.write("")
                self.stdout.write(self.style.WARNING(">>> 这是预览模式，没有数据被写入数据库"))
                self.stdout.write(self.style.WARNING(">>> 去掉 --dry-run 参数以执行实际导入"))

        except FileNotFoundError as e:
            raise CommandError(str(e))
        except ValueError as e:
            raise CommandError(f"数据格式错误: {e}")
        except DatabaseError as e:
            raise CommandError(f"数据库错误: {e}")
        except Exception as e:
            raise CommandError(f"导入失败: {e}")

    def _progress_callback(self, processed: int, total: int, result):
        """进度回调函数"""
        progress = int((processed / total) * 100) if total > 0 else 0
        bar_length = 50
        filled = int((progress / 100) * bar_length)
        bar = '=' * filled + '>' + ' ' * (bar_length - filled - 1) if filled < bar_length else '=' * bar_length

        # 构建进度行
        progress_line = f"\r[{bar}] {progress:3}% ({processed}/{total}) | 已导入: {result.success} | 跳过: {result.skipped} | 错误: {result.failed}"

        # 输出进度（覆盖之前的输出）
        self.stdout.write(progress_line, ending='')
        self.stdout.flush()

        self.last_progress_length = len(progress_line)

    def _clear_progress(self):
        """清除进度行"""
        if self.last_progress_length > 0:
            self.stdout.write('\r' + ' ' * self.last_progress_length + '\r', ending='')
            self.stdout.flush()
