from django.core.management.base import BaseCommand
from datetime import datetime
from decimal import Decimal
import random
from django.db.models import Max


class Command(BaseCommand):
    help = '为票房为0的电影生成票房数据'

    # 电影类型对应的票房范围（万元）
    TYPE_BOX_OFFICE_RANGES = {
        'Action': (500, 50000),
        'Comedy': (300, 30000),
        'Drama': (100, 20000),
        'Horror': (50, 15000),
        'Thriller': (100, 20000),
        'Romance': (200, 25000),
        'Sci-Fi': (1000, 80000),
        'Fantasy': (800, 60000),
        'Adventure': (500, 45000),
        'Animation': (300, 35000),
        'Documentary': (10, 5000),
        'Crime': (200, 25000),
        'Mystery': (100, 18000),
        'Family': (200, 20000),
        'War': (100, 15000),
        'Music': (50, 8000),
        'Biography': (50, 10000),
        'Sport': (50, 8000),
        'Western': (50, 5000),
        'History': (30, 8000),
        'Musical': (50, 8000),
        'Short': (1, 500),
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--min-box-office',
            type=float,
            default=10,
            help='最小票房（万元）'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅显示要更新的电影，不实际执行'
        )

    def handle(self, *args, **options):
        from movies.models import Movie

        min_box_office = options['min_box_office']
        dry_run = options['dry_run']

        # 获取票房为0的电影
        movies = Movie.objects.filter(box_office_total=0).order_by('-release_date')

        if not movies.exists():
            self.stdout.write(self.style.WARNING("没有票房为0的电影"))
            return

        self.stdout.write(f"找到 {movies.count()} 部票房为0的电影")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN 模式：仅显示预览"))
            for movie in movies[:20]:
                box_office = self.calculate_box_office(movie)
                self.stdout.write(f"  {movie.id}: {movie.title} -> {box_office:.2f}万元")
            if movies.count() > 20:
                self.stdout.write(f"  ... 还有 {movies.count() - 20} 部")
            return

        # 更新票房数据
        updated = 0
        for movie in movies:
            box_office = self.calculate_box_office(movie)
            if box_office >= min_box_office:
                movie.box_office_total = Decimal(str(box_office))
                movie.save(update_fields=['box_office_total'])
                updated += 1

                if updated % 100 == 0:
                    self.stdout.write(f"已更新 {updated} 部电影...")

        self.stdout.write(self.style.SUCCESS(f"完成！共更新 {updated} 部电影的票房数据"))

    def calculate_box_office(self, movie):
        """根据电影特征计算票房"""
        # 获取类型名称
        type_name = movie.type.name if movie.type else 'Drama'

        # 获取基础票房范围
        base_min, base_max = self.TYPE_BOX_OFFICE_RANGES.get(
            type_name, (100, 15000)
        )

        # 根据年份调整
        year = movie.release_date.year if movie.release_date else 2020
        if year >= 2020:
            year_factor = 1.5
        elif year >= 2015:
            year_factor = 1.2
        elif year >= 2010:
            year_factor = 1.0
        elif year >= 2000:
            year_factor = 0.7
        else:
            year_factor = 0.4

        base_min *= year_factor
        base_max *= year_factor

        # 随机生成票房
        box_office = random.uniform(base_min, base_max)

        # 添加一些随机性（对数分布，偏向低票房）
        import math
        box_office = base_min * math.exp(random.uniform(0, math.log(base_max / base_min + 1)))

        return round(box_office, 2)
