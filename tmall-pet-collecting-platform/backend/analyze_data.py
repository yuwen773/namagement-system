#!/usr/bin/env python
"""
分析数据库中的商品数据，为统计接口优化提供依据
"""
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from products.models import Product
from django.db.models import Count, Avg, Max, Min, StdDev, Sum
from decimal import Decimal
from collections import Counter
import re


def analyze_data():
    """分析当前数据"""
    products = Product.objects.all()

    print("=" * 60)
    print("数据库概览")
    print("=" * 60)
    print(f"总商品数: {products.count()}")

    # 字段完整性分析
    print("\n字段完整性:")
    total = products.count()
    print(f"  有品牌: {products.exclude(brand__isnull=True).exclude(brand='').count()} ({products.exclude(brand__isnull=True).exclude(brand='').count()*100//total}%)")
    print(f"  有类目: {products.exclude(category__isnull=True).exclude(category='').count()} ({products.exclude(category__isnull=True).exclude(category='').count()*100//total}%)")
    print(f"  有地区: {products.exclude(region__isnull=True).exclude(region='').count()} ({products.exclude(region__isnull=True).exclude(region='').count()*100//total}%)")
    print(f"  有图片: {products.exclude(image_url__isnull=True).exclude(image_url='').count()} ({products.exclude(image_url__isnull=True).exclude(image_url='').count()*100//total}%)")
    print(f"  有商品属性: {products.exclude(product_attributes__isnull=True).exclude(product_attributes={}).count()}")

    # 价格统计
    print("\n价格统计:")
    price_stats = products.aggregate(
        avg=Avg('price'),
        max=Max('price'),
        min=Min('price'),
        std=StdDev('price')
    )
    print(f"  平均价: {price_stats['avg']:.2f}" if price_stats['avg'] else "N/A")
    print(f"  最高价: {price_stats['max']}" if price_stats['max'] else "N/A")
    print(f"  最低价: {price_stats['min']}" if price_stats['min'] else "N/A")
    print(f"  标准差: {price_stats['std']:.2f}" if price_stats['std'] else "N/A")

    # 价格区间分布（更细致）
    print("\n价格区间分布:")
    price_ranges = [
        ('0-50', 0, 50),
        ('50-100', 50, 100),
        ('100-200', 100, 200),
        ('200-500', 200, 500),
        ('500-1000', 500, 1000),
        ('1000-2000', 1000, 2000),
        ('2000-5000', 2000, 5000),
        ('5000+', 5000, float('inf'))
    ]
    for label, min_p, max_p in price_ranges:
        if max_p == float('inf'):
            count = products.filter(price__gte=min_p).count()
        else:
            count = products.filter(price__gte=min_p, price__lt=max_p).count()
        pct = count * 100 // total if total > 0 else 0
        print(f"  {label}: {count} ({pct}%)")

    # 销量统计
    print("\n销量统计:")
    sales_stats = products.aggregate(
        avg=Avg('sales'),
        max=Max('sales'),
        sum=Sum('sales')
    )
    print(f"  平均销量: {sales_stats['avg']:.0f}" if sales_stats['avg'] else "N/A")
    print(f"  最高销量: {sales_stats['max']}" if sales_stats['max'] else "N/A")
    print(f"  总销量: {sales_stats['sum']}" if sales_stats['sum'] else "N/A")

    # 有销量记录的商品
    with_sales = products.exclude(sales=0).count()
    print(f"  有销量记录: {with_sales} ({with_sales*100//total}%)")

    # 店铺统计
    print("\n店铺统计:")
    shop_count = products.values('shop').distinct().count()
    print(f"  店铺数量: {shop_count}")
    print(f"  平均每店商品数: {total // shop_count if shop_count > 0 else 0}")

    # 品牌分布
    print("\n品牌分布 (Top 10):")
    brands = products.values('brand').annotate(
        count=Count('id'),
        avg_price=Avg('price')
    ).order_by('-count')[:10]
    for b in brands:
        brand_name = b['brand'] or '未分类'
        print(f"  {brand_name}: {b['count']}个, 均价{b['avg_price']:.2f}")

    # 地区分布
    print("\n地区分布 (Top 10):")
    regions = products.values('region').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    for r in regions:
        region_name = r['region'] or '未知'
        print(f"  {region_name}: {r['count']}")

    # 提取标题关键词（用于了解热门商品类型）
    print("\n标题关键词分析:")
    keywords = []
    for p in products[:100]:  # 分析前100个
        # 提取中文关键词
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', p.title)
        keywords.extend(words)

    keyword_counter = Counter(keywords)
    top_keywords = keyword_counter.most_common(15)
    for word, count in top_keywords:
        print(f"  {word}: {count}")

    # 批次分析
    print("\n采集批次:")
    batches = products.values('batch_no').annotate(
        count=Count('id')
    ).order_by('-batch_no')[:5]
    for batch in batches:
        print(f"  {batch['batch_no']}: {batch['count']}条")

    # 商品属性分析
    print("\n商品属性统计:")
    attr_stats = {}
    for p in products.exclude(product_attributes__isnull=True).exclude(product_attributes={}):
        attrs = p.product_attributes
        if isinstance(attrs, dict):
            for key in attrs.keys():
                attr_stats[key] = attr_stats.get(key, 0) + 1

    top_attrs = sorted(attr_stats.items(), key=lambda x: -x[1])[:10]
    for attr, count in top_attrs:
        print(f"  {attr}: {count}条记录")

    print("\n" + "=" * 60)


if __name__ == '__main__':
    analyze_data()
