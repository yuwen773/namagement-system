"""
景点图片批量更新命令

用法: python manage.py update_attraction_images [--dry-run]
"""
from django.core.management.base import BaseCommand
from attractions.models import Attraction
from attractions.images_config import (
    ATTRACTION_IMAGES,
    CATEGORY_DEFAULT_IMAGES,
    get_category_default_images
)


class Command(BaseCommand):
    help = '批量更新景点图片'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅预览不实际更新',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # 获取所有未删除的景点
        attractions = Attraction.objects.filter(is_deleted=False)
        total = attractions.count()

        self.stdout.write(f'共找到 {total} 个景点')

        updated_count = 0
        skipped_count = 0

        for attraction in attractions:
            name = attraction.name
            category = attraction.category

            # 1. 尝试精确匹配
            if name in ATTRACTION_IMAGES:
                images = ATTRACTION_IMAGES[name]
                cover_image = images.get('cover')
                gallery = images.get('gallery', [])
                match_type = '精确匹配'
            else:
                # 2. 使用类别默认图
                images = get_category_default_images(category)
                cover_image = images.get('cover')
                gallery = images.get('gallery', [])
                match_type = f'类别: {category}'

            if dry_run:
                self.stdout.write(
                    f'[DRY-RUN] {name}: {match_type} -> {cover_image}'
                )
                skipped_count += 1
            else:
                attraction.cover_image = cover_image
                attraction.images = gallery
                attraction.save(update_fields=['cover_image', 'images'])
                updated_count += 1

        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'\n[DRY-RUN] 共 {skipped_count} 个景点待更新')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\n成功更新 {updated_count} 个景点')
            )
