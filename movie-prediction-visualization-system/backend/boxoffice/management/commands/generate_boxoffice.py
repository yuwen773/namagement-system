from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
from decimal import Decimal
import random
from boxoffice.models import BoxOfficeRecord

class Command(BaseCommand):
    help = '生成票房记录数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start-date',
            type=str,
            default='2023-01-01',
            help='开始日期 (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2025-12-31',
            help='结束日期 (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='批量插入大小'
        )

    def handle(self, *args, **options):
        from movies.models import Movie
        from cinemas.models import Cinema
        from boxoffice.models import BoxOfficeRecord

        start_date = datetime.strptime(options['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(options['end_date'], '%Y-%m-%d').date()
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
            if stats['movies_processed'] % 100 == 0:
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
        show_days = random.randint(30, 90)

        # 确定电影实际上映期间
        movie_start = max(movie.release_date, start_date) if movie.release_date else start_date
        movie_end = min(movie_start + timedelta(days=show_days), end_date)

        if movie_start >= movie_end:
            return records

        # 计算每日衰减系数总和
        decay_sum = sum([self.decay_factor(i) for i in range(show_days)])

        current_day = 0
        current_date = movie_start

        while current_date <= movie_end and current_day < show_days:
            # 计算当日总票房
            daily_total = int(float(total_box_office_yuan) * self.decay_factor(current_day) / decay_sum)

            if daily_total > 0:
                # 分配到影院
                cinema_records = self.distribute_to_cinemas(
                    daily_total, movie, cinemas, current_date
                )
                records.extend(cinema_records)

            current_date += timedelta(days=1)
            current_day += 1

        return records

    def decay_factor(self, day):
        """票房衰减系数"""
        return 0.85 ** (day / 7)  # 每周衰减15%

    def distribute_to_cinemas(self, daily_total, movie, cinemas, record_date):
        """将当日票房分配到影院"""
        # 根据热度选择影院数量
        popularity = getattr(movie, 'popularity', 10) if hasattr(movie, 'popularity') else 10
        if popularity > 50:
            num_cinemas = random.randint(8, 15)
        elif popularity > 20:
            num_cinemas = random.randint(4, 8)
        else:
            num_cinemas = random.randint(1, 3)

        # 按座位数排序，优先选择大影院
        sorted_cinemas = sorted(cinemas, key=lambda c: c.seats_count, reverse=True)
        selected = sorted_cinemas[:min(num_cinemas, len(sorted_cinemas))]

        records = []
        remaining = daily_total

        for i, cinema in enumerate(selected):
            if i == len(selected) - 1:
                amount = remaining
            else:
                ratio = cinema.seats_count / sum(c.seats_count for c in selected)
                amount = int(daily_total * ratio)
                remaining -= amount

            # 计算场次和人次
            is_weekend = record_date.weekday() in [5, 6]
            base_screenings = cinema.screen_count * 0.6
            weekend_mult = 1.5 if is_weekend else 1.0
            screenings = int(base_screenings * weekend_mult)
            screenings = max(1, min(screenings, cinema.screen_count))

            # 观影人次（平均票价35-45元）
            avg_price = random.uniform(35, 45)
            audience = max(0, int(amount / avg_price))

            records.append(BoxOfficeRecord(
                movie=movie,
                cinema=cinema,
                record_date=record_date,
                daily_box_office=amount,
                screening_count=screenings,
                audience_count=audience
            ))

        return records
