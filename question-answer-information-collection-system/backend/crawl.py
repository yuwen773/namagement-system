"""
爬虫启动脚本

提供便捷的命令行接口来启动爬虫。
支持演示模式和全量模式，支持混合模式和纯API模式。

使用示例：
    python crawl.py --mode demo                    # 演示模式（20条）
    python crawl.py --mode full --limit 10000      # 全量采集
    python crawl.py --mode demo --api-only         # 纯API模式（无需Playwright）
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
django.setup()


def run_spider(mode: str = 'demo', limit: int = 20, api_only: bool = False):
    """
    启动爬虫

    Args:
        mode: 采集模式 ('demo' 或 'full')
        limit: 采集数量限制
        api_only: 是否使用纯API模式（无需Playwright）
    """
    from scrapy.crawler import CrawlerProcess
    from scrapy.settings import Settings

    # 导入爬虫模块
    if api_only:
        from apps.crawler.spiders import WendaAPISpider as SpiderClass
        print("[INFO] 使用纯 API 模式爬虫")
    else:
        from apps.crawler.spiders import WendaSpider as SpiderClass

    import apps.crawler.settings as my_settings

    # 创建爬虫设置
    crawler_settings = Settings()

    # 从模块加载设置
    for key in dir(my_settings):
        if key.isupper():
            crawler_settings.set(key, getattr(my_settings, key))

    # 如果使用纯API模式，禁用Playwright相关设置
    if api_only:
        crawler_settings.set('DOWNLOAD_HANDLERS', {})
        crawler_settings.set('TWISTED_REACTOR', None)
        crawler_settings.set('PLAYWRIGHT_ENABLED', False)

    # 配置 CrawlerProcess
    process = CrawlerProcess(settings=crawler_settings)

    # 启动爬虫
    process.crawl(SpiderClass, mode=mode, limit=limit)
    process.start()


def demo_crawl(api_only: bool = False):
    """演示采集（20条）"""
    print("=" * 50)
    print("启动演示采集模式（20条数据）")
    if api_only:
        print("模式: 纯 API（无需浏览器）")
    print("=" * 50)
    run_spider(mode='demo', limit=20, api_only=api_only)


def full_crawl(limit: int = 10000, api_only: bool = False):
    """全量采集"""
    print("=" * 50)
    print(f"启动全量采集模式（最多 {limit} 条数据）")
    if api_only:
        print("模式: 纯 API（无需浏览器）")
    print("=" * 50)
    run_spider(mode='full', limit=limit, api_only=api_only)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='360问答爬虫启动脚本')
    parser.add_argument(
        '--mode',
        choices=['demo', 'full'],
        default='demo',
        help='采集模式: demo(演示,20条) 或 full(全量)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='采集数量限制'
    )
    parser.add_argument(
        '--api-only',
        action='store_true',
        help='使用纯API模式（无需Playwright浏览器渲染）'
    )

    args = parser.parse_args()

    if args.mode == 'demo':
        demo_crawl(api_only=args.api_only)
    else:
        full_crawl(args.limit, api_only=args.api_only)
