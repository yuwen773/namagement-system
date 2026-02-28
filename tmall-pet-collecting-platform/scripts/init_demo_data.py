"""
初始化演示数据脚本
生成10,000+条潮玩商品数据，满足PRD要求

使用方法：
python scripts/init_demo_data.py
"""
import os
import sys
import django
import random
from decimal import Decimal

# 设置Django环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from products.models import Product
from django.utils import timezone


def generate_demo_products(count=10000):
    """
    生成演示数据

    Args:
        count: 生成数量，默认10000
    """
    print("=" * 60)
    print("初始化演示数据")
    print("=" * 60)

    # 潮玩相关数据
    brands = [
        '万代', '泡泡玛特', '乐高', '孩之宝', '变形金刚',
        'HotToys', 'threezero', '便签', '52TOYS', '摩动核'
    ]

    keywords = [
        '高达模型', '盲盒', '手办', '潮玩', '乐高',
        '变形金刚', '海贼王', '火影忍者', '龙珠', 'EVA',
        '假面骑士', '圣斗士星矢', '初音未来', '洛天依', '宝可梦'
    ]

    shops = [
        '万代官方旗舰店', '泡泡玛特官方店', '乐高官方旗舰店',
        '模玩之家', '手办天堂', '潮玩世界', '玩具反斗城',
        '京东玩具专营店', '天猫超市', '品牌直营店'
    ]

    titles_template = [
        '{brand} {keyword} 精品模型',
        '{keyword} 限定版 收藏级',
        '正版 {brand} {keyword} 手办',
        '{keyword} 纪念版 礼盒装',
        '{brand} {keyword} 拼装模型',
        '热销 {keyword} 现货',
        '{keyword} 新品上市',
        '{brand} {keyword} 典藏版',
        '{keyword} 官方正品',
        '限量版 {keyword} 收藏'
    ]

    locations = [
        '广东广州', '上海', '浙江杭州', '江苏苏州',
        '北京', '广东深圳', '福建厦门', '四川成都'
    ]

    # 批量创建
    batch_size = 500
    created_count = 0
    skipped_count = 0

    for i in range(count):
        # 随机生成商品数据
        brand = random.choice(brands)
        keyword = random.choice(keywords)
        shop = random.choice(shops)
        location = random.choice(locations)

        title_template = random.choice(titles_template)
        title = title_template.format(brand=brand, keyword=keyword)

        # 添加一些变化
        if random.random() > 0.7:
            title += f" {random.choice(['限量', '珍藏', '特惠', '热销', '新品'])}"

        price = Decimal(str(random.uniform(20, 2000))).quantize(Decimal('0.01'))

        # 销量分布：大部分商品销量较低，少数爆款
        sales_roll = random.random()
        if sales_roll > 0.95:
            sales = random.randint(5000, 50000)  # 5%的爆款
        elif sales_roll > 0.8:
            sales = random.randint(1000, 5000)   # 15%的热销
        elif sales_roll > 0.5:
            sales = random.randint(100, 1000)    # 30%的中等销量
        else:
            sales = random.randint(0, 100)       # 50%的低销量

        # 检查是否已存在
        if Product.objects.filter(title=title, shop=shop).exists():
            skipped_count += 1
            continue

        # 创建商品
        Product.objects.create(
            title=title,
            price=price,
            sales=sales,
            shop=shop,
            brand=brand,
            category='潮玩',
            image_url=f'https://picsum.photos/200/200?random={i}',
            detail_url=f'https://detail.tmall.com/item.htm?id={random.randint(100000000, 999999999)}',
            item_loc=location,
            batch_no=timezone.now().strftime('%Y%m%d%H%M%S'),
            crawl_time=timezone.now()
        )

        created_count += 1

        # 进度显示
        if (i + 1) % 1000 == 0:
            print(f"已处理: {i + 1}/{count}, 创建: {created_count}, 跳过: {skipped_count}")

    print("\n" + "=" * 60)
    print("初始化完成！")
    print(f"总计处理: {count}")
    print(f"成功创建: {created_count}")
    print(f"跳过重复: {skipped_count}")
    print(f"数据库总数: {Product.objects.count()}")
    print("=" * 60)


def print_statistics():
    """打印数据统计"""
    print("\n数据统计:")
    print("-" * 60)

    total = Product.objects.count()
    print(f"总商品数: {total}")

    if total > 0:
        # 价格分布
        from django.db.models import Count, Q

        price_ranges = {
            '0-50元': Q(price__lte=50),
            '50-200元': Q(price__gt=50, price__lte=200),
            '200-500元': Q(price__gt=200, price__lte=500),
            '500-1000元': Q(price__gt=500, price__lte=1000),
            '1000元以上': Q(price__gt=1000)
        }

        print("\n价格分布:")
        for range_name, condition in price_ranges.items():
            count = Product.objects.filter(condition).count()
            percentage = (count / total) * 100
            print(f"  {range_name}: {count} ({percentage:.1f}%)")

        # 销量分布
        sales_ranges = {
            '0-100': Q(sales__lte=100),
            '100-1000': Q(sales__gt=100, sales__lte=1000),
            '1000-5000': Q(sales__gt=1000, sales__lte=5000),
            '5000+': Q(sales__gt=5000)
        }

        print("\n销量分布:")
        for range_name, condition in sales_ranges.items():
            count = Product.objects.filter(condition).count()
            percentage = (count / total) * 100
            print(f"  {range_name}: {count} ({percentage:.1f}%)")

        # 品牌分布
        print("\n品牌分布 (Top 10):")
        brands = Product.objects.values('brand').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        for brand in brands:
            percentage = (brand['count'] / total) * 100
            print(f"  {brand['brand'] or '未分类'}: {brand['count']} ({percentage:.1f}%)")

        # 店铺分布
        print("\n店铺分布 (Top 10):")
        shops = Product.objects.values('shop').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        for shop in shops:
            percentage = (shop['count'] / total) * 100
            print(f"  {shop['shop']}: {shop['count']} ({percentage:.1f}%)")

    print("-" * 60)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='初始化演示数据')
    parser.add_argument(
        '--count',
        type=int,
        default=10000,
        help='生成数据数量（默认10000）'
    )
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='仅显示统计信息'
    )

    args = parser.parse_args()

    if args.stats_only:
        print_statistics()
    else:
        # 清空现有数据（可选）
        clear = input(f"是否清空现有数据？当前有 {Product.objects.count()} 条 (y/N): ").strip().lower()
        if clear == 'y':
            print("清空现有数据...")
            Product.objects.all().delete()
            print("已清空")

        # 生成新数据
        generate_demo_products(args.count)

        # 显示统计
        print_statistics()
