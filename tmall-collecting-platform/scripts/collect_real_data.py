"""
真实数据采集脚本
使用爬虫从天猫采集真实商品数据

使用方法：
1. 设置环境变量 TAOBAO_COOKIE（参考 docs/crawler-cookie-guide.md）
2. 运行脚本：python scripts/collect_real_data.py
"""
import os
import sys
import django
import time

# 设置Django环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

import logging
from crawler.spiders.tmall_spider import TmallSpider

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def collect_real_data(keywords=None, max_pages_per_keyword=3):
    """
    采集真实数据

    Args:
        keywords: 搜索关键词列表，默认使用潮玩相关关键词
        max_pages_per_keyword: 每个关键词采集的页数
    """
    if keywords is None:
        keywords = [
            '高达模型', '盲盒', '手办', '潮玩',
            '泡泡玛特', '乐高', '变形金刚',
            '海贼王', '火影忍者', '龙珠'
        ]

    print("=" * 60)
    print("真实数据采集")
    print("=" * 60)
    print(f"关键词: {', '.join(keywords)}")
    print(f"每个关键词页数: {max_pages_per_keyword}")
    print(f"预计采集: {len(keywords) * max_pages_per_keyword * 44} 条（每页约44条）")
    print("=" * 60)

    # 检查Cookie
    cookie = os.environ.get('TAOBAO_COOKIE', '')
    if not cookie:
        print("\n⚠️  警告：未设置环境变量 TAOBAO_COOKIE")
        print("真实采集需要有效的淘宝Cookie！")
        print("\n获取Cookie请参考：docs/crawler-cookie-guide.md")
        print("\n将尝试采集（可能会失败）...")

    # 统计
    total_success = 0
    total_failed = 0
    results_by_keyword = {}

    # 逐个关键词采集
    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] 采集关键词: {keyword}")
        print("-" * 60)

        # 创建爬虫实例
        spider = TmallSpider(
            task_id=f'collect-{keyword}-{int(time.time())}',
            mode='hybrid',  # 混合模式，自动降级
            keywords=[keyword],
        )

        # 运行爬虫
        try:
            result = spider.run()

            success = result['success']
            failed = result['failed']
            source = result.get('source_type', 'unknown')

            total_success += success
            total_failed += failed

            results_by_keyword[keyword] = {
                'success': success,
                'failed': failed,
                'source': source
            }

            print(f"✅ 成功: {success} 条")
            print(f"❌ 失败: {failed} 条")
            print(f"📦 数据来源: {source}")

            # 显示最新日志
            if spider.logs:
                print("\n最新日志:")
                for log in spider.logs[-3:]:
                    print(f"  - {log}")

        except Exception as e:
            print(f"❌ 采集失败: {e}")
            results_by_keyword[keyword] = {
                'success': 0,
                'failed': 0,
                'source': 'error',
                'error': str(e)
            }

        # 关键词之间的延迟（避免频繁请求）
        if i < len(keywords):
            delay = 10
            print(f"\n⏱️  等待 {delay} 秒后继续...")
            time.sleep(delay)

    # 汇总结果
    print("\n" + "=" * 60)
    print("采集完成！")
    print("=" * 60)
    print(f"总计成功: {total_success} 条")
    print(f"总计失败: {total_failed} 条")
    print(f"成功率: {total_success / (total_success + total_failed) * 100 if (total_success + total_failed) > 0 else 0:.1f}%")

    print("\n各关键词详情:")
    for keyword, result in results_by_keyword.items():
        print(f"  {keyword}: {result['success']} 条 ({result['source']})")

    # 显示数据库统计
    from products.models import Product
    db_count = Product.objects.count()
    print(f"\n数据库当前总数: {db_count} 条")

    return total_success


def interactive_collect():
    """交互式采集"""
    print("=" * 60)
    print("真实数据采集 - 交互模式")
    print("=" * 60)

    # 选择模式
    print("\n请选择采集模式:")
    print("  1. 快速采集（3个关键词，各2页）")
    print("  2. 标准采集（10个关键词，各3页）")
    print("  3. 深度采集（10个关键词，各10页）")
    print("  4. 自定义采集")
    print("  0. 退出")

    choice = input("\n请选择 (0-4): ").strip()

    if choice == '0':
        print("退出")
        return

    configs = {
        '1': {'keywords': ['高达模型', '盲盒', '手办'], 'pages': 2},
        '2': {
            'keywords': ['高达模型', '盲盒', '手办', '潮玩', '泡泡玛特', '乐高', '变形金刚', '海贼王', '火影忍者', '龙珠'],
            'pages': 3
        },
        '3': {
            'keywords': ['高达模型', '盲盒', '手办', '潮玩', '泡泡玛特', '乐高', '变形金刚', '海贼王', '火影忍者', '龙珠'],
            'pages': 10
        },
    }

    if choice in configs:
        config = configs[choice]
        print(f"\n将采集 {len(config['keywords'])} 个关键词，每个 {config['pages']} 页")
        collect_real_data(config['keywords'], config['pages'])

    elif choice == '4':
        # 自定义
        keyword_input = input("请输入关键词（用逗号分隔）: ").strip()
        keywords = [k.strip() for k in keyword_input.split(',') if k.strip()]

        pages_input = input("每个关键词采集几页？(默认3): ").strip()
        pages = int(pages_input) if pages_input.isdigit() else 3

        if keywords:
            print(f"\n将采集 {len(keywords)} 个关键词，每个 {pages} 页")
            collect_real_data(keywords, pages)
        else:
            print("❌ 未输入有效关键词")
    else:
        print("❌ 无效选择")


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == 'interactive':
                interactive_collect()
            else:
                # 自定义关键词
                keywords = sys.argv[1:]
                collect_real_data(keywords, max_pages_per_keyword=3)
        else:
            # 默认标准采集
            collect_real_data()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
    except Exception as e:
        logger.error(f"采集失败: {e}", exc_info=True)
        print(f"\n❌ 采集失败: {e}")
