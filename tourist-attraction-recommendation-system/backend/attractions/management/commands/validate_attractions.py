"""
景点数据验证命令

使用方法:
    python manage.py validate_attractions              # 完整验证
    python manage.py validate_attractions --quick      # 快速统计
    python manage.py validate_attractions --issues     # 只显示问题数据
"""

from django.core.management.base import BaseCommand
from django.db import models
from attractions.models import Attraction


class Command(BaseCommand):
    help = '验证景点数据质量'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quick',
            action='store_true',
            help='快速统计模式'
        )
        parser.add_argument(
            '--issues',
            action='store_true',
            help='只显示有问题的数据'
        )

    def handle(self, *args, **options):
        self.quick = options['quick']
        self.show_issues = options['issues']

        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(self.style.NOTICE('景点数据质量验证报告'))
        self.stdout.write(self.style.NOTICE('=' * 60))

        if self.quick:
            self._quick_stats()
        elif self.show_issues:
            self._show_issues()
        else:
            self._full_report()

    def _quick_stats(self):
        """快速统计"""
        total = Attraction.objects.filter(is_deleted=False).count()
        self.stdout.write(f'总景点数: {total}')

        # 按分类统计
        self.stdout.write('\n分类分布:')
        for cat in ['自然风光', '人文古迹', '主题乐园', '其他']:
            count = Attraction.objects.filter(category=cat, is_deleted=False).count()
            self.stdout.write(f'  {cat}: {count}')

    def _full_report(self):
        """完整报告"""
        self._print_basic_stats()
        self._print_category_stats()
        self._print_data_quality()
        self._print_top_attractions()
        self._print_geographic_stats()

    def _print_basic_stats(self):
        """基本统计"""
        total = Attraction.objects.filter(is_deleted=False).count()
        deleted = Attraction.objects.filter(is_deleted=True).count()

        self.stdout.write('\n[1] 基本统计')
        self.stdout.write(f'  有效记录: {total}')
        self.stdout.write(f'  已删除: {deleted}')
        self.stdout.write(f'  总计: {total + deleted}')

    def _print_category_stats(self):
        """分类统计"""
        self.stdout.write('\n[2] 景点分类分布')
        self.stdout.write('-' * 40)

        categories = Attraction.objects.filter(
            is_deleted=False
        ).values('category').annotate(count=models.Count('id'))

        total = sum(item['count'] for item in categories)

        for item in sorted(categories, key=lambda x: x['count'], reverse=True):
            cat = item['category']
            count = item['count']
            pct = count / total * 100 if total > 0 else 0
            bar = '█' * int(pct / 2)
            self.stdout.write(f'  {cat:8s}: {count:5d} ({pct:5.1f}%) {bar}')

        self.stdout.write(f'  {"总计":8s}: {total:5d}')

    def _print_data_quality(self):
        """数据质量"""
        self.stdout.write('\n[3] 数据完整度')
        self.stdout.write('-' * 40)

        total = Attraction.objects.filter(is_deleted=False).count()

        # 有描述
        with_desc = Attraction.objects.filter(
            is_deleted=False
        ).exclude(description='').count()
        pct = with_desc / total * 100 if total > 0 else 0
        self.stdout.write(f'  有描述: {with_desc}/{total} ({pct:.1f}%)')

        # 有坐标
        with_coords = Attraction.objects.filter(
            is_deleted=False,
            latitude__isnull=False
        ).count()
        pct = with_coords / total * 100 if total > 0 else 0
        self.stdout.write(f'  有坐标: {with_coords}/{total} ({pct:.1f}%)')

        # 有图片
        with_image = Attraction.objects.filter(
            is_deleted=False
        ).exclude(cover_image='').count()
        pct = with_image / total * 100 if total > 0 else 0
        self.stdout.write(f'  有图片: {with_image}/{total} ({pct:.1f}%)')

        # 5A级
        five_a = Attraction.objects.filter(
            is_deleted=False,
            level='5A'
        ).count()
        pct = five_a / total * 100 if total > 0 else 0
        self.stdout.write(f'  5A级: {five_a}/{total} ({pct:.1f}%)')

        # 高浏览量
        high_views = Attraction.objects.filter(
            is_deleted=False,
            view_count__gte=1000
        ).count()
        self.stdout.write(f'  高浏览量(>=1000): {high_views}')

    def _print_top_attractions(self):
        """热门景点"""
        self.stdout.write('\n[4] Top 10 热门景点')
        self.stdout.write('-' * 40)

        top10 = Attraction.objects.filter(
            is_deleted=False
        ).order_by('-view_count')[:10]

        for i, attr in enumerate(top10, 1):
            views = f'{attr.view_count:,}'
            name = attr.name[:20] + '..' if len(attr.name) > 20 else attr.name
            region = attr.region[:10] if attr.region else '未知'
            self.stdout.write(f'  {i:2d}. {name:22s} ({region:10s}) - {views} 浏览')

    def _print_geographic_stats(self):
        """地理分布"""
        self.stdout.write('\n[5] 地区分布 Top 15')
        self.stdout.write('-' * 40)

        regions = Attraction.objects.filter(
            is_deleted=False
        ).values('region').annotate(count=models.Count('id'))

        for i, item in enumerate(sorted(regions, key=lambda x: x['count'], reverse=True)[:15], 1):
            region = item['region'][:15] if item['region'] else '未知'
            count = item['count']
            self.stdout.write(f'  {i:2d}. {region:15s}: {count:4d} 个景点')

    def _show_issues(self):
        """显示问题数据"""
        self.stdout.write('\n[问题数据报告]')
        self.stdout.write('=' * 60)

        issues = {
            '无描述': Attraction.objects.filter(is_deleted=False, description='').count(),
            '无坐标': Attraction.objects.filter(is_deleted=False, latitude__isnull=True).count(),
            '无分类': Attraction.objects.filter(is_deleted=False, category='其他').count(),
            '浏览量为0': Attraction.objects.filter(is_deleted=False, view_count=0).count(),
        }

        for issue, count in issues.items():
            self.stdout.write(f'\n{issue}: {count} 条')

        # 显示无描述的景点样例
        no_desc = Attraction.objects.filter(
            is_deleted=False, description=''
        )[:20]
        if no_desc:
            self.stdout.write('\n无描述景点样例:')
            for attr in no_desc:
                self.stdout.write(f'  - {attr.name} ({attr.region})')

        self.stdout.write(self.style.SUCCESS('\n验证完成!'))


# 修复导入
try:
    from django.db import models
except ImportError:
    pass
