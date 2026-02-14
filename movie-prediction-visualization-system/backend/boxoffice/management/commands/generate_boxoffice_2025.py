from django.core.management.base import BaseCommand
from datetime import timedelta
from decimal import Decimal
import random
from boxoffice.models import BoxOfficeRecord


class Command(BaseCommand):
    help = '生成2024-2026年票房记录数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start-date',
            type=str,
            default='2024-12-01',
            help='票房记录开始日期'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2026-12-31',
            help='票房记录结束日期'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=2000,
            help='批量插入大小'
        )

    def handle(self, *args, **options):
        from movies.models import Movie
        from cinemas.models import Cinema
        from datetime import date

        start_date = date.fromisoformat(options['start_date'])
        end_date = date.fromisoformat(options['end_date'])
        batch_size = options['batch_size']

        stats = {'records': 0, 'movies_processed': 0}

        self.stdout.write(f"生成票房记录：{start_date} 到 {end_date}")

        # 获取有票房的电影
        movies = Movie.objects.filter(box_office_total__gt=0)
        cinemas = list(Cinema.objects.filter(is_active=True))

        if not cinemas:
            self.stdout.write(self.style.ERROR("请先导入影院数据！"))
            return

        self.stdout.write(f"处理 {movies.count()} 部电影，{len(cinemas)} 家影院")

        batch_records = []

        for movie in movies:
            stats['movies_processed'] += 1
            if stats['movies_processed'] % 500 == 0:
                self.stdout.write(f"已处理 {stats['movies_processed']} 部电影...")

            # 生成该电影的票房记录
            movie_records = self.generate_movie_records(movie, cinemas, start_date, end_date)
            batch_records.extend(movie_records)

            # 批量插入
            if len(batch_records) >= batch_size:
                BoxOfficeRecord.objects.bulk_create(batch_records, ignore_conflicts=True)
                stats['records'] += len(batch_records)
                batch_records = []

        # 插入剩余记录
        if batch_records:
            BoxOfficeRecord.objects.bulk_create(batch_records, ignore_conflicts=True)
            stats['records'] += len(batch_records)

        self.stdout.write(self.style.SUCCESS(f"完成！生成 {stats['records']} 条票房记录"))

    def generate_movie_records(self, movie, cinemas, start_date, end_date):
        """为单部电影生成票房记录"""
        records = []

        total_box_office_yuan = movie.box_office_total * Decimal('10000')

        # 上映前预热期（30-60天）
        pre_heat_days = random.randint(30, 60)
        # 上映后放映期（30-90天）
        show_days = random.randint(30, 90)

        # 确定电影实际上映期间
        movie_release = movie.release_date if movie.release_date else start_date

        # 预热期：从 start_date 或 上映前60天 开始
        pre_heat_start = max(start_date, movie_release - timedelta(days=pre_heat_days))
        pre_heat_end = movie_release - timedelta(days=1) if movie_release > start_date else start_date - timedelta(days=1)

        # 放映期：从上映日开始
        show_start = movie_release
        show_end = min(movie_release + timedelta(days=show_days), end_date)

        # 生成预热期数据（热度递增）
        if pre_heat_start <= pre_heat_end:
            for day_offset in range((pre_heat_end - pre_heat_start).days + 1):
                current_date = pre_heat_start + timedelta(days=day_offset)
                if current_date < start_date or current_date > end_date:
                    continue

                # 热度递增
                heat_ratio = (day_offset + 1) / pre_heat_days
                daily_heat = int(float(total_box_office_yuan) * 0.001 * heat_ratio)  # 预热期票房很低

                if daily_heat > 0:
                    selected_cinemas = random.sample(cinemas, min(random.randint(2, 5), len(cinemas)))
                    for cinema in selected_cinemas:
                        records.append(BoxOfficeRecord(
                            movie=movie,
                            cinema=cinema,
                            record_date=current_date,
                            daily_box_office=daily_heat // len(selected_cinemas),
                            screening_count=random.randint(1, 3),
                            audience_count=random.randint(10, 100)
                        ))

        # 生成上映期数据（首周高峰，后逐渐衰减）
        if show_start <= show_end:
            # 计算每日衰减系数总和
            show_days_count = (show_end - show_start).days + 1
            decay_sum = sum([self.decay_factor(i) for i in range(show_days_count)])

            current_day = 0
            current_date = show_start

            while current_date <= show_end:
                # 计算当日总票房
                daily_total = int(float(total_box_office_yuan) * self.decay_factor(current_day) / decay_sum)

                if daily_total > 0:
                    # 根据热度选择影院数量
                    if current_day < 7:  # 首周
                        num_cinemas = random.randint(10, 20)
                    elif current_day < 30:
                        num_cinemas = random.randint(6, 12)
                    else:
                        num_cinemas = random.randint(3, 8)

                    num_cinemas = min(num_cinemas, len(cinemas))

                    # 按座位数排序，优先选择大影院
                    sorted_cinemas = sorted(cinemas, key=lambda c: c.seats_count, reverse=True)
                    selected = sorted_cinemas[:num_cinemas]

                    # 分配票房
                    remaining = daily_total
                    for i, cinema in enumerate(selected):
                        if i == len(selected) - 1:
                            amount = remaining
                        else:
                            ratio = cinema.seats_count / sum(c.seats_count for c in selected)
                            amount = int(daily_total * ratio)
                            remaining -= amount

                        # 计算场次和人次
                        is_weekend = current_date.weekday() in [5, 6]
                        base_screenings = cinema.screen_count * 0.6
                        weekend_mult = 1.5 if is_weekend else 1.0
                        screenings = int(base_screenings * weekend_mult)
                        screenings = max(1, min(screenings, cinema.screen_count))

                        avg_price = random.uniform(35, 45)
                        audience = max(0, int(amount / avg_price))

                        records.append(BoxOfficeRecord(
                            movie=movie,
                            cinema=cinema,
                            record_date=current_date,
                            daily_box_office=amount,
                            screening_count=screenings,
                            audience_count=audience
                        ))

                current_date += timedelta(days=1)
                current_day += 1

        return records

    def decay_factor(self, day):
        """票房衰减系数"""
        return 0.85 ** (day / 7)  # 每周衰减15%
