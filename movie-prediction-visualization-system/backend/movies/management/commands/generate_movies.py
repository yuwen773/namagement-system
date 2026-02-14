from django.core.management.base import BaseCommand
from datetime import date, timedelta
import random
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
scripts_dir = os.path.join(backend_dir, 'scripts')
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from data_generator import *


class Command(BaseCommand):
    help = '生成电影数据（5000+部，2025-2026年）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5000,
            help='生成电影数量'
        )
        parser.add_argument(
            '--start-date',
            type=str,
            default='2025-01-01',
            help='上映开始日期'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            default='2026-12-31',
            help='上映结束日期'
        )

    def handle(self, *args, **options):
        from movies.models import Movie, MovieType

        count = options['count']
        start_date = date.fromisoformat(options['start_date'])
        end_date = date.fromisoformat(options['end_date'])

        self.stdout.write(self.style.HTTP_INFO(f"开始生成 {count} 部电影..."))

        # 确保电影类型存在
        self.ensure_movie_types()

        # 生成上映日期（均匀分布）
        release_dates = get_release_dates(count, start_date, end_date)

        # 获取类型映射
        genre_map = {g.name: g for g in MovieType.objects.all()}

        # 批量创建电影
        movies_to_create = []
        existing_titles = set(Movie.objects.values_list('title', flat=True))

        for i, release_date in enumerate(release_dates):
            # 生成电影数据
            movie_data = generate_movie_data(release_date)

            # 检查是否重复
            if movie_data['title'] in existing_titles:
                # 生成新的
                movie_data['title'] = f"{movie_data['title']} {random.randint(1,999)}"

            existing_titles.add(movie_data['title'])

            movies_to_create.append(Movie(
                title=movie_data['title'],
                director=movie_data['director'],
                actors=movie_data['actors'],
                release_date=movie_data['release_date'],
                duration=movie_data['duration'],
                type=genre_map.get(movie_data['type_name']),
                box_office_total=movie_data['box_office_total'],
                status='RELEASED',
            ))

            if (i + 1) % 500 == 0:
                Movie.objects.bulk_create(movies_to_create, ignore_conflicts=True)
                self.stdout.write(f"已生成 {i + 1} 部电影...")
                movies_to_create = []
                existing_titles = set(Movie.objects.values_list('title', flat=True))

        # 插入剩余
        if movies_to_create:
            Movie.objects.bulk_create(movies_to_create, ignore_conflicts=True)

        total = Movie.objects.count()
        self.stdout.write(self.style.SUCCESS(f"电影生成完成！共 {total} 部"))

    def ensure_movie_types(self):
        """确保电影类型存在"""
        from movies.models import MovieType

        types = [t[0] for t in MOVIE_TYPES]
        for t in types:
            MovieType.objects.get_or_create(name=t)

        self.stdout.write(f"电影类型已准备: {len(types)} 个")
