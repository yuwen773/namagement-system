"""
天猫爬虫测试脚本

用于测试真实爬虫功能

使用方法：
1. 设置Cookie（参考 docs/crawler-cookie-guide.md）
2. 运行脚本：python scripts/test_tmall_crawler.py
"""
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

import logging
from crawler.spiders.tmall_real_api import TmallRealAPI
from crawler.spiders.tmall_api import TmallAPI
from crawler.spiders.config import SpiderConfig

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_real_api():
    """测试真实API"""
    print("=" * 60)
    print("测试天猫真实爬虫API")
    print("=" * 60)

    # 获取Cookie（可以从环境变量或直接设置）
    cookie = os.environ.get('TAOBAO_COOKIE', '')

    if not cookie:
        print("\n⚠️  警告：未设置Cookie！")
        print("请设置环境变量 TAOBAO_COOKIE 或在代码中直接设置")
        print("\n获取Cookie请参考：docs/crawler-cookie-guide.md")
        print("\n将使用测试模式...")

        # 使用测试模式（可能不会成功）
        cookie = ""

    # 创建API实例
    config = SpiderConfig()
    config.max_pages = 1  # 测试只爬1页

    api = TmallRealAPI(
        config=config,
        cookie=cookie
    )

    # 测试连接
    print("\n1️⃣  测试连接...")
    test_result = api.test_connection("高达模型")

    print(f"结果: {'✅ 成功' if test_result['success'] else '❌ 失败'}")
    print(f"消息: {test_result['message']}")

    if not test_result['success']:
        print("\n❌ 连接失败，无法继续测试")
        print("请检查：")
        print("  1. Cookie是否有效")
        print("  2. 网络连接是否正常")
        return

    # 测试搜索
    print("\n2️⃣  测试搜索功能...")
    print("搜索关键词: 高达模型")
    print("搜索页数: 1")

    result = api.search("高达模型", max_pages=1)

    print(f"\n结果: {'✅ 成功' if result['success'] > 0 else '❌ 失败'}")
    print(f"获取商品数: {result['success']}")
    print(f"失败数: {result['failed']}")
    print(f"数据来源: {result['source']}")

    # 显示部分商品
    if result['products']:
        print(f"\n3️⃣  商品示例（前3个）:")
        for i, product in enumerate(result['products'][:3], 1):
            print(f"\n  商品 {i}:")
            print(f"    标题: {product['title'][:50]}...")
            print(f"    价格: ¥{product['price']}")
            print(f"    销量: {product['sales']}")
            print(f"    店铺: {product['shop']}")

    # 显示日志
    print(f"\n4️⃣  运行日志:")
    for log in api.logs[-10:]:  # 显示最后10条
        print(f"  - {log}")

    return result


def test_legacy_api():
    """测试旧版API（可能已失效）"""
    print("\n" + "=" * 60)
    print("测试旧版API（可能已失效）")
    print("=" * 60)

    config = SpiderConfig()
    api = TmallAPI(config=config)

    print("\n1️⃣  测试连接...")
    test_result = api.test_connection()

    print(f"结果: {'✅ 成功' if test_result['success'] else '❌ 失败'}")
    print(f"消息: {test_result['message']}")

    return test_result


def interactive_test():
    """交互式测试"""
    print("=" * 60)
    print("天猫爬虫交互式测试")
    print("=" * 60)

    while True:
        print("\n请选择:")
        print("  1. 测试真实API（推荐）")
        print("  2. 测试旧版API")
        print("  3. 自定义搜索测试")
        print("  0. 退出")

        choice = input("\n请输入选项 (0-3): ").strip()

        if choice == '0':
            print("退出测试")
            break
        elif choice == '1':
            test_real_api()
        elif choice == '2':
            test_legacy_api()
        elif choice == '3':
            keyword = input("请输入搜索关键词: ").strip()
            if keyword:
                pages = input("请输入搜索页数 (默认1): ").strip()
                max_pages = int(pages) if pages.isdigit() else 1

                cookie = os.environ.get('TAOBAO_COOKIE', '')
                api = TmallRealAPI(cookie=cookie)

                print(f"\n搜索: {keyword}, 页数: {max_pages}")
                result = api.search(keyword, max_pages=max_pages)

                print(f"\n结果: {result['success']} 个商品")
        else:
            print("无效选项")


if __name__ == '__main__':
    try:
        # 检查参数
        if len(sys.argv) > 1:
            if sys.argv[1] == 'real':
                test_real_api()
            elif sys.argv[1] == 'legacy':
                test_legacy_api()
            elif sys.argv[1] == 'interactive':
                interactive_test()
            else:
                print("用法:")
                print("  python scripts/test_tmall_crawler.py real        # 测试真实API")
                print("  python scripts/test_tmall_crawler.py legacy      # 测试旧版API")
                print("  python scripts/test_tmall_crawler.py interactive # 交互式测试")
        else:
            # 默认测试真实API
            test_real_api()

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        print(f"\n❌ 测试失败: {e}")
