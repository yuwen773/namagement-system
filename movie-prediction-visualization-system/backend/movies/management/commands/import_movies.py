from django.core.management.base import BaseCommand
import pandas as pd
import sys
import os

# 添加 scripts 路径
# __file__ = .../commands/import_movies.py
# commands = dirname(__file__)
# management = dirname(commands)
# movies = dirname(management)
# backend = dirname(movies)
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
scripts_dir = os.path.join(backend_dir, 'scripts')
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from data_utils import *


class Command(BaseCommand):
    help = '导入电影数据（从 tmdb CSV 文件）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--movies-file',
            type=str,
            default='data/tmdb_5000_movies.csv',
            help='电影数据文件路径'
        )
        parser.add_argument(
            '--credits-file',
            type=str,
            default='data/tmdb_5000_credits-1.csv',
            help='演职员数据文件路径'
        )
        parser.add_argument(
            '--metadata-file',
            type=str,
            default='data/movies_metadata.csv',
            help='元数据文件路径（可选，用于增强）'
        )

    def handle(self, *args, **options):
        from movies.models import Movie, MovieType

        stats = ImportStats()

        self.stdout.write(self.style.HTTP_INFO("开始导入电影数据..."))

        # 读取数据
        try:
            movies_df = pd.read_csv(options['movies_file'])
            credits_df = pd.read_csv(options['credits_file'])
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f"文件未找到: {e}"))
            return

        metadata_df = None
        if options['metadata_file'] and os.path.exists(options['metadata_file']):
            metadata_df = pd.read_csv(options['metadata_file'])
            self.stdout.write(f"读取 metadata: {len(metadata_df)} 条")

        self.stdout.write(f"读取到 {len(movies_df)} 条电影记录")

        # 第一阶段：创建所有类型
        self.stdout.write(self.style.HTTP_INFO("\n=== 第一阶段：导入影片类型 ==="))
        self.import_movie_types(movies_df, stats)

        # 第二阶段：合并数据并导入电影
        self.stdout.write(self.style.HTTP_INFO("\n=== 第二阶段：导入影片数据 ==="))
        self.import_movies(movies_df, credits_df, metadata_df, stats)

        # 输出统计
        self.stdout.write(stats.summary())
        stats.print_errors()

    def import_movie_types(self, movies_df, stats):
        """导入影片类型"""
        from movies.models import MovieType

        all_genres = set()
        for genres_json in movies_df['genres']:
            genres = extract_genres(genres_json)
            all_genres.update(genres)

        for genre_name in all_genres:
            obj, created = MovieType.objects.get_or_create(name=genre_name)
            if created:
                stats.add_success()
            else:
                stats.add_skipped()

        self.stdout.write(f"影片类型导入完成：{stats.success} 个新类型")

    def import_movies(self, movies_df, credits_df, metadata_df, stats):
        """导入影片数据"""
        from movies.models import Movie, MovieType

        # 合并 credits
        merged = movies_df.merge(credits_df, left_on='id', right_on='movie_id', how='left')

        # 合并 metadata（如果存在）
        if metadata_df is not None:
            # 只合并 metadata 中有 poster_path 的记录以增强数据
            merged = merged.merge(
                metadata_df[['id', 'poster_path', 'imdb_id', 'popularity',
                             'vote_average', 'vote_count', 'tagline',
                             'production_companies', 'production_countries',
                             'spoken_languages', 'homepage', 'belongs_to_collection',
                             'original_language', 'original_title']],
                on='id',
                how='left',
                suffixes=('', '_meta')
            )

        for idx, row in merged.iterrows():
            # 验证数据
            is_valid, reason = is_valid_movie(row)
            if not is_valid:
                stats.add_failed(reason, row.get('id'))
                continue

            try:
                # 检查是否已存在
                existing = Movie.objects.filter(title=str(row['title'])).first()
                if existing:
                    stats.add_skipped()
                    continue

                # 获取类型
                genre_names = extract_genres(row.get('genres', '[]'))
                genre_obj = None
                if genre_names:
                    genre_obj = MovieType.objects.filter(name=genre_names[0]).first()

                # 创建电影
                movie = Movie.objects.create(
                    title=str(row['title']),
                    director=extract_director(row.get('crew', '[]')),
                    actors=extract_actors(row.get('cast', '[]')),
                    release_date=parse_release_date(row.get('release_date')),
                    duration=int(row['runtime']) if pd.notna(row['runtime']) else 90,
                    type=genre_obj,
                    poster_url=get_poster_url(row.get('poster_path')),
                    description=build_enhanced_description(row),
                    box_office_total=convert_revenue_to_rmb(row.get('revenue', 0)),
                    status=map_status(str(row.get('status', 'Released'))),
                )
                stats.add_success()

                if stats.success % 100 == 0:
                    self.stdout.write(f"已导入 {stats.success} 部电影...")

            except Exception as e:
                stats.add_failed(str(e), row.get('id'))

        self.stdout.write(self.style.SUCCESS(f"影片导入完成：{stats.success} 部"))
