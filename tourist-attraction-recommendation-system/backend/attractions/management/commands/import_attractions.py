"""
景点数据导入命令

使用方法:
    python manage.py import_attractions              # 导入所有数据集
    python manage.py import_attractions --clear       # 先清空再导入
    python manage.py import_attractions --file dataset2  # 只导入数据集2
    python manage.py import_attractions --file dataset1  # 只导入数据集5A级
    python manage.py import_attractions --dry-run    # 试运行（不写入数据库）
"""

import os
import sys
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings
from attractions.models import Attraction
from attractions.data_cleaner import AttractionDataCleaner

# 路径配置 - 使用 Django BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 向上找到项目根目录
while not os.path.exists(os.path.join(BASE_DIR, 'manage.py')):
    BASE_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT = BASE_DIR
DATA_DIR = os.path.join(PROJECT_ROOT, '..', 'data')
DATA_DIR = os.path.normpath(DATA_DIR)


class Command(BaseCommand):
    help = '从 Excel 文件导入景点数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            choices=['dataset1', 'dataset2', 'all'],
            default='all',
            help='指定导入的数据集: dataset1(5A级景区), dataset2(旅游景点描述), all(全部，默认)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='导入前清空现有景点数据'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='试运行模式，只显示处理结果，不写入数据库'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=500,
            help='批量导入的批次大小（默认500）'
        )

    def handle(self, *args, **options):
        self.options = options
        self.dry_run = options['dry_run']
        self.batch_size = options['batch_size']

        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(self.style.NOTICE('景点数据导入工具'))
        self.stdout.write(self.style.NOTICE('=' * 60))

        # 检查数据目录
        if not os.path.exists(DATA_DIR):
            raise CommandError(f'数据目录不存在: {DATA_DIR}')

        # 清空数据（如果指定）
        if options['clear'] and not self.dry_run:
            self._clear_data()

        # 导入数据集
        target = options['file']
        if target in ['all', 'dataset2']:
            self.import_dataset2()

        if target in ['all', 'dataset1']:
            self.import_dataset1()

        # 统计结果
        if not self.dry_run:
            self._print_summary()

        self.stdout.write(self.style.SUCCESS('\n导入完成!'))

    def _clear_data(self):
        """清空现有数据"""
        count = Attraction.objects.count()
        if count > 0:
            Attraction.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'已清空 {count} 条现有记录'))

    def import_dataset2(self):
        """导入数据集2 - 全国旅游景点及描述.xls"""
        filename = '全国旅游景点及描述（部分，可词云或聚类分析）.xls'
        file_path = os.path.join(DATA_DIR, filename)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'文件不存在，跳过: {filename}'))
            return

        self.stdout.write(self.style.NOTICE(f'\n[1/2] 导入数据集2: {filename}'))
        self.stdout.write('-' * 60)

        try:
            # 读取数据
            self.stdout.write(f'  读取数据文件...')
            df = pd.read_excel(file_path)
            original_count = len(df)
            self.stdout.write(f'    原始记录数: {original_count}')

            # 清洗数据
            self.stdout.write(f'  清洗数据...')
            cleaned = AttractionDataCleaner.clean_dataset2(df)

            # 去除空名称记录
            cleaned = cleaned[cleaned['name'] != '']
            after_empty = len(cleaned)
            self.stdout.write(f'    去除空名称后: {after_empty}')

            # 去重
            cleaned, dup_removed = AttractionDataCleaner.remove_duplicates(cleaned)
            self.stdout.write(f'    去除重复后: {len(cleaned)} (移除 {dup_removed} 条)')

            if self.dry_run:
                self.stdout.write(self.style.WARNING('  [DRY-RUN] 跳过数据库写入'))
                self._preview_data(cleaned.head(10))
                return

            # 批量导入
            imported = self._batch_import(cleaned, 'dataset2')
            self.stdout.write(self.style.SUCCESS(f'  成功导入 {imported} 条记录'))

        except Exception as e:
            raise CommandError(f'导入数据集2失败: {str(e)}')

    def import_dataset1(self):
        """导入数据集1 - 全国5A级景区.xlsx"""
        filename = '全国5A级景区.xlsx'
        file_path = os.path.join(DATA_DIR, filename)

        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'文件不存在，跳过: {filename}'))
            return

        self.stdout.write(self.style.NOTICE(f'\n[2/2] 导入数据集1: {filename}'))
        self.stdout.write('-' * 60)

        try:
            # 读取数据
            self.stdout.write(f'  读取数据文件...')
            df = pd.read_excel(file_path)
            original_count = len(df)
            self.stdout.write(f'    原始记录数: {original_count}')

            # 清洗数据
            self.stdout.write(f'  清洗数据...')
            cleaned = AttractionDataCleaner.clean_dataset1(df)

            # 去除空名称记录
            cleaned = cleaned[cleaned['name'] != '']
            self.stdout.write(f'    清洗后记录数: {len(cleaned)}')

            if self.dry_run:
                self.stdout.write(self.style.WARNING('  [DRY-RUN] 跳过数据库写入'))
                self._preview_data(cleaned.head(10))
                return

            # 导入（更新已存在的，插入新的）
            imported, updated = self._upsert_attractions(cleaned)
            self.stdout.write(self.style.SUCCESS(f'  成功导入 {imported} 条新记录，更新 {updated} 条现有记录'))

        except Exception as e:
            raise CommandError(f'导入数据集1失败: {str(e)}')

    def _batch_import(self, df, source):
        """批量导入记录"""
        imported = 0
        objects = []

        for _, row in df.iterrows():
            try:
                obj = Attraction(
                    name=row['name'][:100],
                    description=row['description'][:2000],
                    address=row['address'][:200],
                    category=row.get('category', '其他')[:20],
                    region=row.get('region', '')[:50],
                    opening_hours=row.get('opening_hours', '全天开放')[:100],
                    cover_image=row.get('cover_image', ''),
                    images=row.get('images', []),
                    view_count=row.get('view_count', 0),
                    latitude=row.get('latitude'),
                    longitude=row.get('longitude'),
                    rating_percentage=row.get('rating_percentage', 0.0),
                    guide_count=row.get('guide_count', 0),
                    ranking=row.get('ranking'),
                    level=row.get('level', ''),
                )
                objects.append(obj)
            except Exception as e:
                self.stderr.write(f'  跳过记录 "{row.get("name", "未知")}": {str(e)}')

        # 分批写入数据库
        with transaction.atomic():
            for i in range(0, len(objects), self.batch_size):
                batch = objects[i:i + self.batch_size]
                Attraction.objects.bulk_create(batch, ignore_conflicts=True)
                imported += len(batch)

                if (i + self.batch_size) % 1000 == 0 or i + self.batch_size >= len(objects):
                    self.stdout.write(f'    已处理 {min(i + self.batch_size, len(objects))}/{len(objects)} 条')

        return imported

    def _upsert_attractions(self, df):
        """更新或插入记录（用于5A级景区）"""
        imported = 0
        updated = 0

        for _, row in df.iterrows():
            name = row['name']
            if not name:
                continue

            # 检查是否已存在
            existing = Attraction.objects.filter(name=name).first()

            if existing:
                # 更新现有记录
                existing.level = '5A'
                if not existing.region and row.get('region'):
                    existing.region = row.get('region')
                if not existing.latitude and row.get('latitude'):
                    existing.latitude = row.get('latitude')
                if not existing.longitude and row.get('longitude'):
                    existing.longitude = row.get('longitude')
                existing.save()
                updated += 1
            else:
                # 创建新记录
                Attraction.objects.create(
                    name=name[:100],
                    description=row.get('description', '')[:2000],
                    address=row.get('address', '')[:200],
                    category=row.get('category', '其他')[:20],
                    region=row.get('region', '')[:50],
                    opening_hours=row.get('opening_hours', '全天开放')[:100],
                    cover_image=row.get('cover_image', ''),
                    images=row.get('images', []),
                    view_count=row.get('view_count', 0),
                    latitude=row.get('latitude'),
                    longitude=row.get('longitude'),
                    rating_percentage=row.get('rating_percentage', 0.0),
                    guide_count=row.get('guide_count', 0),
                    ranking=row.get('ranking'),
                    level='5A',
                )
                imported += 1

        return imported, updated

    def _preview_data(self, df):
        """预览数据（前几条）"""
        self.stdout.write('\n  数据预览（前5条）:')
        for idx, row in df.head(5).iterrows():
            self.stdout.write(f'    - {row["name"][:30]} ({row.get("category", "N/A")})')

    def _print_summary(self):
        """打印统计摘要"""
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.NOTICE('数据统计'))
        self.stdout.write('=' * 60)

        total = Attraction.objects.count()
        self.stdout.write(f'  总景点数: {total}')

        # 分类统计
        self.stdout.write('\n  分类分布:')
        for cat in ['自然风光', '人文古迹', '主题乐园', '其他']:
            count = Attraction.objects.filter(category=cat).count()
            self.stdout.write(f'    {cat}: {count}')

        # 有5A标识的
        five_a = Attraction.objects.filter(level='5A').count()
        self.stdout.write(f'    5A级景区: {five_a}')

        # 有坐标的
        with_coords = Attraction.objects.filter(latitude__isnull=False).count()
        self.stdout.write(f'\n  有地理坐标: {with_coords}/{total}')

        # 有描述的
        with_desc = Attraction.objects.exclude(description='').count()
        self.stdout.write(f'  有景点描述: {with_desc}/{total}')

        # Top 10 热门
        self.stdout.write('\n  Top 10 热门景点:')
        top10 = Attraction.objects.order_by('-view_count')[:10]
        for i, attr in enumerate(top10, 1):
            self.stdout.write(f'    {i}. {attr.name[:25]} ({attr.view_count:,} 浏览)')
