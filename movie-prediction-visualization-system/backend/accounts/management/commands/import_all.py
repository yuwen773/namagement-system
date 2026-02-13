from django.core.management.base import BaseCommand
from django.core import management
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = '一键执行所有数据导入（地域→影院→电影→票房）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cinema-count',
            type=int,
            default=200,
            help='生成影院数量'
        )
        parser.add_argument(
            '--skip-movies',
            action='store_true',
            help='跳过电影导入'
        )
        parser.add_argument(
            '--skip-boxoffice',
            action='store_true',
            help='跳过票房生成'
        )
        parser.add_argument(
            '--start-date',
            type=str,
            default='2023-01-01',
            help='票房数据开始日期'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2025-12-31',
            help='票房数据结束日期'
        )

    def handle(self, *args, **options):
        start_time = timezone.now()

        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(self.style.SUCCESS("    电影票房预测系统 - 数据导入工具"))
        self.stdout.write(self.style.SUCCESS("=" * 50))
        self.stdout.write(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write("")

        try:
            # ============ 阶段1: 导入地域和影院 ============
            self.stdout.write(self.style.HTTP_INFO("\n【1/4】导入地域和影院数据..."))
            management.call_command('import_cinemas', '--cinema-count', str(options['cinema_count']))
            self.stdout.write(self.style.SUCCESS("[OK] 地域和影院数据导入完成"))

            # ============ 阶段2: 导入电影 ============
            if not options['skip_movies']:
                self.stdout.write(self.style.HTTP_INFO("\n【2/4】导入电影数据..."))
                management.call_command('import_movies')
                self.stdout.write(self.style.SUCCESS("[OK] 电影数据导入完成"))
            else:
                self.stdout.write(self.style.WARNING("[SKIP] 跳过电影导入"))

            # ============ 阶段3: 生成票房 ============
            if not options['skip_boxoffice']:
                self.stdout.write(self.style.HTTP_INFO("\n【3/4】生成票房记录..."))
                management.call_command(
                    'generate_boxoffice',
                    '--start-date', options['start_date'],
                    '--end-date', options['end_date']
                )
                self.stdout.write(self.style.SUCCESS("[OK] 票房记录生成完成"))
            else:
                self.stdout.write(self.style.WARNING("[SKIP] 跳过票房生成"))

            # ============ 阶段4: 数据统计 ============
            self.stdout.write(self.style.HTTP_INFO("\n【4/4】数据统计..."))
            self.print_statistics()

            # ============ 完成 ============
            end_time = timezone.now()
            duration = (end_time - start_time).total_seconds()

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("=" * 50))
            self.stdout.write(self.style.SUCCESS(f"导入完成！耗时: {duration:.1f}秒"))
            self.stdout.write(self.style.SUCCESS("=" * 50))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n导入失败: {str(e)}"))
            raise

    def print_statistics(self):
        """打印导入后的数据统计"""
        from movies.models import Movie, MovieType
        from cinemas.models import Region, Cinema
        from boxoffice.models import BoxOfficeRecord

        stats = {
            '影片类型': MovieType.objects.count(),
            '影片总数': Movie.objects.count(),
            '有票房影片': Movie.objects.filter(box_office_total__gt=0).count(),
            '地域总数': Region.objects.count(),
            '影院总数': Cinema.objects.filter(is_active=True).count(),
            '票房记录': BoxOfficeRecord.objects.count(),
        }

        self.stdout.write("\n┌────────────────────────────────────┐")
        self.stdout.write("│           数据统计                  │")
        self.stdout.write("├────────────────────────────────────┤")
        for key, value in stats.items():
            self.stdout.write(f"│ {key:12s}: {value:>12}      │")
        self.stdout.write("└────────────────────────────────────┘")
