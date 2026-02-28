"""
数据分析工具模块 - 为统计接口提供复杂的数据分析功能
"""
from django.db.models import Count, Avg, Max, Min, StdDev, Sum, Q, F
from django.db.models.functions import Round
from decimal import Decimal
from collections import Counter
import re


class ProductAnalytics:
    """商品数据分析工具"""

    def __init__(self, queryset=None):
        """
        初始化分析器

        Args:
            queryset: 商品查询集，默认为所有商品
        """
        self.queryset = queryset

    @property
    def products(self):
        """获取商品查询集"""
        if self.queryset is None:
            from products.models import Product
            self.queryset = Product.objects.all()
        return self.queryset

    def get_overview(self) -> dict:
        """
        获取增强的数据概览

        Returns:
            包含更丰富统计信息的字典
        """
        products = self.products
        total = products.count()

        # 基础统计
        basic_stats = products.aggregate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            min_price=Min('price'),
            avg_sales=Avg('sales'),
            max_sales=Max('sales'),
            total_sales=Sum('sales')
        )

        # 完整性统计
        completeness = {
            'with_brand': products.exclude(brand__isnull=True).exclude(brand='').count(),
            'with_category': products.exclude(category__isnull=True).exclude(category='').count(),
            'with_region': products.exclude(region__isnull=True).exclude(region='').count(),
            'with_image': products.exclude(image_url__isnull=True).exclude(image_url='').count(),
            'with_sales': products.exclude(sales=0).count(),
        }

        # 转换为百分比
        completeness_pct = {
            f'{k}_pct': v * 100 // total if total > 0 else 0
            for k, v in completeness.items()
        }

        return {
            'total_products': total,
            'total_shops': products.values('shop').distinct().count(),
            'total_brands': products.values('brand').distinct().count(),
            'total_regions': products.values('region').distinct().count(),

            # 价格统计
            'price': {
                'avg': round(float(basic_stats['avg_price'] or 0), 2),
                'max': float(basic_stats['max_price'] or 0),
                'min': float(basic_stats['min_price'] or 0),
                'range': float(basic_stats['max_price'] or 0) - float(basic_stats['min_price'] or 0),
            },

            # 销量统计
            'sales': {
                'avg': round(float(basic_stats['avg_sales'] or 0), 0),
                'max': int(basic_stats['max_sales'] or 0),
                'total': int(basic_stats['total_sales'] or 0),
            },

            # 数据完整性
            'completeness': {
                'with_brand': completeness['with_brand'],
                'with_category': completeness['with_category'],
                'with_region': completeness['with_region'],
                'with_image': completeness['with_image'],
                'with_sales': completeness['with_sales'],
            },
            'completeness_pct': completeness_pct,

            # 近期批次
            'latest_batch': self._get_latest_batch_info(),
        }

    def _get_latest_batch_info(self) -> dict:
        """获取最新批次信息"""
        latest = self.products.order_by('-crawl_time').first()
        if not latest:
            return {}
        return {
            'batch_no': latest.batch_no,
            'crawl_time': latest.crawl_time.isoformat() if latest.crawl_time else None,
        }

    def get_price_distribution(self, ranges=None) -> list:
        """
        获取价格区间分布（基于实际数据优化）

        Args:
            ranges: 自定义价格区间，默认使用智能区间

        Returns:
            价格分布数据列表
        """
        products = self.products
        total = products.count()

        # 如果没有指定区间，使用智能区间
        if ranges is None:
            price_stats = products.aggregate(min=Min('price'), max=Max('price'))
            min_price = float(price_stats['min'] or 0)
            max_price = float(price_stats['max'] or 0)

            # 智能生成区间
            ranges = self._generate_smart_ranges(min_price, max_price)

        data = []
        for label, min_p, max_p in ranges:
            if max_p == float('inf'):
                count = products.filter(price__gte=min_p).count()
            else:
                count = products.filter(price__gte=min_p, price__lt=max_p).count()

            percentage = count * 100 / total if total > 0 else 0

            data.append({
                'range': label,
                'min_price': min_p,
                'max_price': max_p if max_p != float('inf') else None,
                'count': count,
                'percentage': round(percentage, 2)
            })

        return data

    def _generate_smart_ranges(self, min_price: float, max_price: float) -> list:
        """
        根据价格范围智能生成区间

        Args:
            min_price: 最低价格
            max_price: 最高价格

        Returns:
            价格区间列表 [(label, min, max), ...]
        """
        # 预定义的基础区间
        base_ranges = [
            ('0-50', 0, 50),
            ('50-100', 50, 100),
            ('100-200', 100, 200),
            ('200-500', 200, 500),
            ('500-1000', 500, 1000),
            ('1000-2000', 1000, 2000),
            ('2000-5000', 2000, 5000),
        ]

        # 根据最大价格添加区间
        ranges = []
        for label, min_p, max_p in base_ranges:
            if min_p < max_price:
                if max_p <= max_price:
                    ranges.append((label, min_p, max_p))
                else:
                    ranges.append((f'{min_p}-{int(max_price)}', min_p, max_price))
                    break

        # 添加最高区间
        if max_price > 5000:
            ranges.append((f'{int(max_price)}+', max_price, float('inf')))

        return ranges

    def get_sales_distribution(self) -> list:
        """
        获取销量区间分布

        Returns:
            销量分布数据列表
        """
        products = self.products
        total = products.count()

        # 销量区间定义
        ranges = [
            ('无销量', 0, 1),
            ('1-100', 1, 100),
            ('100-500', 100, 500),
            ('500-1000', 500, 1000),
            ('1000-2000', 1000, 2000),
            ('2000-5000', 2000, 5000),
            ('5000+', 5000, float('inf'))
        ]

        data = []
        for label, min_s, max_s in ranges:
            if max_s == float('inf'):
                count = products.filter(sales__gte=min_s).count()
            else:
                count = products.filter(sales__gte=min_s, sales__lt=max_s).count()

            percentage = count * 100 / total if total > 0 else 0

            data.append({
                'range': label,
                'min_sales': min_s,
                'max_sales': max_s if max_s != float('inf') else None,
                'count': count,
                'percentage': round(percentage, 2)
            })

        return data

    def get_brand_analysis(self, top_n=15) -> list:
        """
        获取品牌分析（包含价格、销量等维度）

        Args:
            top_n: 返回前N个品牌

        Returns:
            品牌分析数据列表
        """
        brands = self.products.values('brand').annotate(
            count=Count('id'),
            avg_price=Round(Avg('price'), 2),
            min_price=Min('price'),
            max_price=Max('price'),
            avg_sales=Round(Avg('sales'), 0),
            total_sales=Sum('sales')
        ).order_by('-count')[:top_n]

        data = []
        for brand in brands:
            brand_name = brand['brand'] or '未分类'
            data.append({
                'brand': brand_name,
                'count': brand['count'],
                'price': {
                    'avg': float(brand['avg_price'] or 0),
                    'min': float(brand['min_price'] or 0),
                    'max': float(brand['max_price'] or 0),
                },
                'sales': {
                    'avg': float(brand['avg_sales'] or 0),
                    'total': int(brand['total_sales'] or 0),
                }
            })

        return data

    def get_region_analysis(self, top_n=15) -> list:
        """
        获取地区分析（用于热力图）

        Args:
            top_n: 返回前N个地区

        Returns:
            地区分析数据列表
        """
        regions = self.products.values('region').annotate(
            count=Count('id'),
            avg_price=Round(Avg('price'), 2),
            avg_sales=Round(Avg('sales'), 0),
            shop_count=Count('shop', distinct=True)
        ).order_by('-count')[:top_n]

        data = []
        for region in regions:
            region_name = region['region'] or '未知'
            data.append({
                'region': region_name,
                'count': region['count'],
                'avg_price': float(region['avg_price'] or 0),
                'avg_sales': float(region['avg_sales'] or 0),
                'shop_count': region['shop_count']
            })

        return data

    def get_shop_analysis(self, top_n=20) -> list:
        """
        获取店铺分析（不只是商品数量）

        Args:
            top_n: 返回前N个店铺

        Returns:
            店铺分析数据列表
        """
        shops = self.products.values('shop').annotate(
            count=Count('id'),
            avg_price=Round(Avg('price'), 2),
            avg_sales=Round(Avg('sales'), 0),
            max_price=Max('price'),
            total_sales=Sum('sales')
        ).order_by('-count')[:top_n]

        data = []
        for shop in shops:
            data.append({
                'shop': shop['shop'],
                'count': shop['count'],
                'avg_price': float(shop['avg_price'] or 0),
                'avg_sales': float(shop['avg_sales'] or 0),
                'max_price': float(shop['max_price'] or 0),
                'total_sales': int(shop['total_sales'] or 0),
            })

        return data

    def get_price_sales_correlation(self) -> list:
        """
        获取价格与销量的关联分析（按价格区间）

        Returns:
            价格-销量关联数据
        """
        products = self.products

        # 价格区间
        price_ranges = [
            (0, 50),
            (50, 100),
            (100, 200),
            (200, 500),
            (500, 1000),
            (1000, 2000),
            (2000, float('inf'))
        ]

        data = []
        for min_p, max_p in price_ranges:
            if max_p == float('inf'):
                range_products = products.filter(price__gte=min_p)
                label = f'{min_p}+'
            else:
                range_products = products.filter(price__gte=min_p, price__lt=max_p)
                label = f'{min_p}-{max_p}'

            stats = range_products.aggregate(
                count=Count('id'),
                avg_sales=Round(Avg('sales'), 0)
            )

            data.append({
                'price_range': label,
                'count': stats['count'],
                'avg_sales': float(stats['avg_sales'] or 0)
            })

        return data

    def get_top_products(self, top_n=20, sort_by='sales') -> list:
        """
        获取Top商品（可按不同维度排序）

        Args:
            top_n: 返回前N个商品
            sort_by: 排序字段 (sales/price/-price/crawl_time)

        Returns:
            商品列表
        """
        order_map = {
            'sales': '-sales',
            'price': '-price',
            'price_asc': 'price',
            'newest': '-crawl_time'
        }

        order_field = order_map.get(sort_by, '-sales')

        products = self.products.order_by(order_field)[:top_n]

        data = []
        for p in products:
            data.append({
                'id': str(p.id),
                'title': p.title,
                'price': float(p.price),
                'sales': p.sales,
                'shop': p.shop,
                'brand': p.brand,
                'region': p.region,
                'image_url': p.image_url,
                'crawl_time': p.crawl_time.isoformat() if p.crawl_time else None,
            })

        return data

    def get_attribute_analysis(self) -> dict:
        """
        获取商品属性统计分析

        Returns:
            属性分析数据
        """
        products = self.products.exclude(
            product_attributes__isnull=True
        ).exclude(product_attributes={})

        attr_stats = {}
        for p in products:
            attrs = p.product_attributes
            if isinstance(attrs, dict):
                for key, value in attrs.items():
                    if key not in attr_stats:
                        attr_stats[key] = {}
                    value_str = str(value) if value else '空值'
                    attr_stats[key][value_str] = attr_stats[key].get(value_str, 0) + 1

        # 整理数据
        data = {}
        for attr_name, values in attr_stats.items():
            sorted_values = sorted(values.items(), key=lambda x: -x[1])[:10]
            data[attr_name] = [
                {'value': k, 'count': v}
                for k, v in sorted_values
            ]

        return data

    def get_batch_analysis(self) -> list:
        """
        获取批次分析（了解采集趋势）

        Returns:
            批次分析数据
        """
        batches = self.products.values('batch_no').annotate(
            count=Count('id'),
            avg_price=Round(Avg('price'), 2),
            avg_sales=Round(Avg('sales'), 0),
            first_time=Min('crawl_time'),
            last_time=Max('crawl_time')
        ).order_by('-first_time')

        data = []
        for batch in batches:
            data.append({
                'batch_no': batch['batch_no'],
                'count': batch['count'],
                'avg_price': float(batch['avg_price'] or 0),
                'avg_sales': float(batch['avg_sales'] or 0),
                'first_time': batch['first_time'].isoformat() if batch['first_time'] else None,
                'last_time': batch['last_time'].isoformat() if batch['last_time'] else None,
            })

        return data

    def get_keyword_analysis(self, top_n=30, sample_size=200) -> list:
        """
        获取标题关键词分析

        Args:
            top_n: 返回前N个关键词
            sample_size: 分析的商品样本数量

        Returns:
            关键词列表
        """
        # 提取样本
        products = self.products[:sample_size]

        keywords = []
        for p in products:
            # 提取中文关键词（2-4个字）
            words = re.findall(r'[\u4e00-\u9fa5]{2,4}', p.title)
            keywords.extend(words)

        # 统计词频
        keyword_counter = Counter(keywords)

        # 过滤常见词
        stop_words = {'商品', '店铺', '官方', '正版', '限量', '特价', '促销'}
        for word in stop_words:
            keyword_counter.pop(word, None)

        top_keywords = keyword_counter.most_common(top_n)

        return [
            {'keyword': word, 'count': count}
            for word, count in top_keywords
        ]

    def get_market_insights(self) -> dict:
        """
        获取市场洞察（综合分析）

        Returns:
            市场洞察数据
        """
        products = self.products
        total = products.count()

        # 价格带分布
        price_dist = self.get_price_distribution()
        main_price_range = max(price_dist, key=lambda x: x['count']) if price_dist else None

        # 主力品牌
        brands = self.get_brand_analysis(top_n=1)
        top_brand = brands[0] if brands else None

        # 热门地区
        regions = self.get_region_analysis(top_n=1)
        top_region = regions[0] if regions else None

        # 销量冠军
        top_product = products.order_by('-sales').first()
        avg_price = products.aggregate(avg=Avg('price'))['avg'] or 0

        return {
            'market_size': {
                'total_products': total,
                'total_shops': products.values('shop').distinct().count(),
                'total_sales': int(products.aggregate(total=Sum('sales'))['total'] or 0),
            },
            'price_positioning': {
                'avg_price': float(avg_price),
                'main_range': main_price_range['range'] if main_price_range else 'N/A',
                'main_range_pct': main_price_range['percentage'] if main_price_range else 0,
                'low_end_pct': next((p['percentage'] for p in price_dist if p['min_price'] < 100), 0),
                'high_end_pct': next((p['percentage'] for p in price_dist if p['min_price'] >= 1000), 0),
            },
            'brand_insights': {
                'top_brand': top_brand['brand'] if top_brand else 'N/A',
                'top_brand_count': top_brand['count'] if top_brand else 0,
                'top_brand_avg_price': top_brand['price']['avg'] if top_brand else 0,
                'total_brands': products.values('brand').distinct().count(),
            },
            'regional_distribution': {
                'top_region': top_region['region'] if top_region else 'N/A',
                'top_region_count': top_region['count'] if top_region else 0,
                'total_regions': products.values('region').distinct().count(),
            },
            'product_insights': {
                'top_product_title': top_product.title if top_product else 'N/A',
                'top_product_price': float(top_product.price) if top_product else 0,
                'top_product_sales': top_product.sales if top_product else 0,
                'top_product_shop': top_product.shop if top_product else 'N/A',
            },
            'data_quality': {
                'brand_coverage': int(products.exclude(brand__isnull=True).exclude(brand='').count() * 100 / total) if total > 0 else 0,
                'region_coverage': int(products.exclude(region__isnull=True).exclude(region='').count() * 100 / total) if total > 0 else 0,
                'sales_coverage': int(products.exclude(sales=0).count() * 100 / total) if total > 0 else 0,
            }
        }

    def get_pet_type_distribution(self) -> list:
        """
        获取宠物类型分布统计

        Returns:
            宠物类型分布数据列表
        """
        products = self.products
        total = products.count()

        from products.models import Product
        pet_types = dict(Product.PET_TYPE_CHOICES)
        data = []

        for pet_key, pet_label in pet_types.items():
            count = products.filter(pet_type=pet_key).count()
            percentage = count * 100 / total if total > 0 else 0

            data.append({
                'type': pet_key,
                'label': pet_label,
                'count': count,
                'percentage': round(percentage, 2)
            })

        return data

    def get_pet_use_distribution(self) -> list:
        """
        获取用途分类分布统计

        Returns:
            用途分类分布数据列表
        """
        products = self.products
        total = products.count()

        from products.models import Product
        pet_uses = dict(Product.PET_USE_CHOICES)
        data = []

        for use_key, use_label in pet_uses.items():
            count = products.filter(pet_use=use_key).count()
            percentage = count * 100 / total if total > 0 else 0

            data.append({
                'use': use_key,
                'label': use_label,
                'count': count,
                'percentage': round(percentage, 2)
            })

        return data
