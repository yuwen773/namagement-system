"""
淘宝 mtop API 测试脚本
用于验证爬虫集成是否正常工作
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from crawler.spiders.taobao_mtop_api import TaobaoMtopAPI


def test_api():
    """测试 mtop API"""
    print("=" * 60)
    print("淘宝 mtop API 测试")
    print("=" * 60)

    # 获取 Cookie
    cookie = os.environ.get('TAOBAO_COOKIE', '')

    if not cookie:
        print("\n[WARN]  未设置 TAOBAO_COOKIE 环境变量")
        print("请设置环境变量后再测试:")
        print("export TAOBAO_COOKIE='your_cookie_here'")
        print("\n将使用默认 token 进行测试（可能失败）...")

    # 初始化 API
    api = TaobaoMtopAPI(cookie=cookie)

    # 测试连接
    print("\n1. 测试连接...")
    result = api.test_connection("高达模型")

    if result['success']:
        print(f"[OK] {result['message']}")
        if result.get('sample_products'):
            print(f"\n示例商品数据:")
            for i, product in enumerate(result['sample_products'], 1):
                title = product.get('title', 'N/A')[:50]
                price = product.get('price', 'N/A')
                print(f"  {i}. {title}... - 价格: price}")
    else:
        print(f"[ERROR] {result['message']}")
        print("\n可能的原因:")
        print("  1. Cookie 无效或已过期")
        print("  2. 网络连接问题")
        print("  3. 触发反爬机制")
        return False

    # 搜索商品
    print("\n2. 搜索商品（2页）...")
    search_result = api.search("高达模型", max_pages=2)

    print(f"[OK] 搜索完成:")
    print(f"   成功: {search_result['success']} 条")
    print(f"   失败: {search_result['failed']} 条")
    print(f"   总计: {len(search_result['products'])} 条")

    # 显示部分商品
    if search_result['products']:
        print(f"\n3. 商品预览（前5条）:")
        for i, product in enumerate(search_result['products'][:5], 1):
            print(f"\n  [{i}] {product['title'][:40]}...")
            print(f"      价格: 价格: product['price']}")
            print(f"      销量: {product['sales']}")
            print(f"      店铺: {product['shop']}")
            if product.get('region'):
                print(f"      地区: {product['region']}")
            if product.get('tags'):
                print(f"      标签: {product['tags']}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

    return True


def test_integration():
    """测试与 TmallSpider 的集成"""
    print("\n" + "=" * 60)
    print("集成测试：TmallSpider + mtop API")
    print("=" * 60)

    cookie = os.environ.get('TAOBAO_COOKIE', '')

    if not cookie:
        print("\n[WARN]  未设置 Cookie，跳过集成测试")
        return False

    from crawler.spiders.tmall_spider import TmallSpider

    print("\n1. 创建 TmallSpider（混合模式）...")

    def progress_callback(progress, stage, items, logs):
        print(f"   进度: {progress} | {stage} | 已采集: {items} 条")

    spider = TmallSpider(
        task_id="test_integration",
        mode="hybrid",
        keywords=["高达模型"],
        callback=progress_callback
    )

    print("\n2. 执行采集任务...")
    result = spider.run()

    print(f"\n[OK] 采集完成:")
    print(f"   成功: {result['success']} 条")
    print(f"   失败: {result['failed']} 条")
    print(f"   数据来源: {result['source_type']}")

    print("\n" + "=" * 60)
    print("集成测试完成！")
    print("=" * 60)

    return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='淘宝 mtop API 测试')
    parser.add_argument('--integration', action='store_true', help='测试与 TmallSpider 的集成')
    args = parser.parse_args()

    try:
        if args.integration:
            test_integration()
        else:
            test_api()
    except KeyboardInterrupt:
        print("\n\n测试已中断")
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
