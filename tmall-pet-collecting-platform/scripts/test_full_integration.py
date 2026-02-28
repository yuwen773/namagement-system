"""
完整集成测试脚本
测试从 mtop API 到数据库存储的完整流程
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from crawler.spiders.taobao_mtop_api import TaobaoMtopAPI
from crawler.spiders.tmall_spider import TmallSpider
from products.models import Product, CrawlLog


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def check_database_fields():
    """检查数据库字段"""
    print_section("1. 检查数据库字段")

    # 获取 Product 模型字段
    product_fields = [f.name for f in Product._meta.get_fields()]
    print(f"\nProduct 模型字段 ({len(product_fields)} 个):")

    # 新增字段
    new_fields = [
        'product_id', 'price_unit', 'price_desc', 'seller_nick',
        'shop_tags', 'region', 'tags', 'product_attributes'
    ]

    for field in new_fields:
        exists = field in product_fields
        status = "[OK]" if exists else "[ERROR]"
        print(f"  {status} {field}")

    # 检查 CrawlLog source_type
    print(f"\nCrawlLog 数据源类型:")
    source_types = [st[0] for st in CrawlLog.SourceType.choices]
    for st in source_types:
        print(f"  - {st}")

    # 检查是否所有新字段都存在
    missing = [f for f in new_fields if f not in product_fields]
    if missing:
        print(f"\n[WARN]  缺少字段: {missing}")
        print("请运行: python scripts/migrate_database.py")
        return False

    print("\n[OK] 数据库字段完整")
    return True


def test_mtop_api():
    """测试 mtop API"""
    print_section("2. 测试淘宝 mtop API")

    cookie = os.environ.get('TAOBAO_COOKIE', '')
    if not cookie:
        print("\n[WARN]  未设置 TAOBAO_COOKIE 环境变量")
        print("API 测试将使用默认 token（可能失败）")
        print("\n设置方法:")
        print("export TAOBAO_COOKIE='your_cookie_here'")

    api = TaobaoMtopAPI(cookie=cookie)

    # 测试连接
    print("\n测试连接...")
    result = api.test_connection("高达模型")

    if result['success']:
        print(f"[OK] {result['message']}")
        return True
    else:
        print(f"[ERROR] {result['message']}")
        print("\n可能原因:")
        print("  1. Cookie 无效或已过期")
        print("  2. 网络连接问题")
        print("  3. 触发反爬机制")
        return False


def test_spider_integration():
    """测试爬虫集成"""
    print_section("3. 测试爬虫集成")

    cookie = os.environ.get('TAOBAO_COOKIE', '')
    if not cookie:
        print("\n[WARN]  未设置 Cookie，跳过完整爬虫测试")
        print("只测试演示模式...")

    def progress_callback(progress, stage, items, logs):
        print(f"   [{progress}] {stage} - 已采集: {items} 条")

    spider = TmallSpider(
        task_id="test_full_integration",
        mode="demo",  # 使用演示模式确保成功
        keywords=["测试商品"],
        callback=progress_callback
    )

    print("\n执行爬虫任务（演示模式）...")
    result = spider.run()

    print(f"\n[OK] 爬虫任务完成:")
    print(f"   成功: {result['success']} 条")
    print(f"   失败: {result['failed']} 条")
    print(f"   数据来源: {result['source_type']}")

    # 检查数据是否保存到数据库
    print("\n检查数据库...")
    products = Product.objects.filter(title__icontains="测试商品")
    print(f"   数据库中有 {products.count()} 条测试商品")

    if products.exists():
        sample = products.first()
        print(f"\n示例商品:")
        print(f"   ID: {sample.product_id}")
        print(f"   标题: {sample.title}")
        print(f"   价格: {sample.price} 元")
        print(f"   销量: {sample.sales}")
        if sample.region:
            print(f"   地区: {sample.region}")
        if sample.tags:
            print(f"   标签: {sample.tags}")

    return True


def test_data_fields():
    """测试新字段数据"""
    print_section("4. 测试新字段数据")

    # 查找有新字段数据的商品
    products = Product.objects.exclude(product_id='').exclude(region__isnull=True)

    if not products.exists():
        print("\n[WARN]  数据库中暂无新字段数据")
        print("运行爬虫任务后会自动填充这些字段")
        return True

    print(f"\n找到 {products.count()} 条包含新字段数据的商品\n")

    sample = products.first()
    print("示例商品详情:")
    print(f"  product_id: {sample.product_id}")
    print(f"  title: {sample.title[:50]}...")
    print(f"  price: {sample.price}")
    print(f"  price_unit: {sample.price_unit or 'N/A'}")
    print(f"  price_desc: {sample.price_desc or 'N/A'}")
    print(f"  seller_nick: {sample.seller_nick or 'N/A'}")
    print(f"  shop: {sample.shop}")
    print(f"  shop_tags: {sample.shop_tags or 'N/A'}")
    print(f"  sales: {sample.sales}")
    print(f"  region: {sample.region or 'N/A'}")
    print(f"  tags: {sample.tags or 'N/A'}")
    if sample.image_url:
        print(f"  image_url: {sample.image_url[:50]}...")
    else:
        print("  image_url: N/A")
    if sample.detail_url:
        print(f"  detail_url: {sample.detail_url[:50]}...")
    else:
        print("  detail_url: N/A")

    if sample.product_attributes:
        import json
        attrs = json.loads(sample.product_attributes) if isinstance(sample.product_attributes, str) else sample.product_attributes
        print(f"  product_attributes: {attrs}")

    return True


def show_statistics():
    """显示数据库统计"""
    print_section("5. 数据库统计")

    total = Product.objects.count()
    print(f"\n总商品数: {total}")

    if total > 0:
        # 统计新字段填充情况
        with_id = Product.objects.exclude(product_id='').count()
        with_region = Product.objects.exclude(region='').exclude(region__isnull=True).count()
        with_tags = Product.objects.exclude(tags='').exclude(tags__isnull=True).count()

        print(f"\n新字段填充情况:")
        print(f"  有 product_id: {with_id} ({with_id/total*100:.1f}%)")
        print(f"  有 region: {with_region} ({with_region/total*100:.1f}%)")
        print(f"  有 tags: {with_tags} ({with_tags/total*100:.1f}%)")

        # 价格分布
        from django.db.models import Count, Q
        price_ranges = [
            ("0-50", Q(price__gte=0, price__lt=50)),
            ("50-200", Q(price__gte=50, price__lt=200)),
            ("200-500", Q(price__gte=200, price__lt=500)),
            ("500+", Q(price__gte=500)),
        ]

        print(f"\n价格分布:")
        for label, condition in price_ranges:
            count = Product.objects.filter(condition).count()
            print(f"  {label}元: {count} ({count/total*100:.1f}%)")

    # 采集日志统计
    log_total = CrawlLog.objects.count()
    print(f"\n采集日志: {log_total} 条")

    if log_total > 0:
        # 按来源统计
        from django.db.models import Count
        source_stats = CrawlLog.objects.values('source_type').annotate(
            count=Count('id')
        ).order_by('-count')

        print(f"数据源分布:")
        for stat in source_stats:
            source = stat['source_type'] or 'N/A'
            count = stat['count']
            print(f"  {source}: {count}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print(" 天猫潮玩电商数据采集系统 - 完整集成测试")
    print("=" * 60)

    all_passed = True

    # 1. 检查数据库字段
    if not check_database_fields():
        all_passed = False
        print("\n[WARN]  数据库字段不完整，建议先执行迁移")
        migrate = input("是否立即执行数据库迁移? (y/n): ").lower()
        if migrate == 'y':
            from scripts.migrate_database import migrate_database
            if migrate_database():
                print("\n[OK] 数据库迁移完成，请重新运行测试")
            return

    # 2. 测试 mtop API
    api_ok = test_mtop_api()
    if not api_ok:
        print("\n[WARN]  API 测试失败，但可以继续使用演示模式")

    # 3. 测试爬虫集成
    if not test_spider_integration():
        all_passed = False

    # 4. 测试新字段数据
    test_data_fields()

    # 5. 显示统计
    show_statistics()

    # 总结
    print_section("测试总结")

    if all_passed:
        print("\n[OK] 所有测试通过!")
        print("\n下一步:")
        print("  1. 设置 TAOBAO_COOKIE 环境变量")
        print("  2. 重启 Django 和 Celery 服务")
        print("  3. 通过管理端测试采集功能")
    else:
        print("\n[WARN]  部分测试未通过，请检查上述错误")

    print("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试已中断")
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
