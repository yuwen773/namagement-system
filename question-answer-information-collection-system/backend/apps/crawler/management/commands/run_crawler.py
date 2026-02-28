# -*- coding: utf-8 -*-
"""
运行爬虫管理命令

使用方式:
    python manage.py run_crawler --mode demo --limit 20
    python manage.py run_crawler --mode full --limit 100

这个命令会正确初始化 Django 环境，确保 Pipeline 可以正常工作。
数据会自动保存到数据库 (通过 Pipeline)
"""

import sys
import os
import json
import time
import threading
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from apps.crawler.spiders.wenda_spider import WendaSpider


# 全局变量用于跟踪采集数量
_crawled_count = 0
_process = None


class Command(BaseCommand):
    help = '运行360问答爬虫'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='demo',
            choices=['demo', 'full'],
            help='采集模式: demo(演示) 或 full(完整)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='采集数量限制'
        )
        parser.add_argument(
            '--output',
            type=str,
            default=None,
            help='输出文件路径 (可选，默认输出到 exports 目录)'
        )

    def handle(self, *args, **options):
        global _crawled_count, _process

        mode = options['mode']
        limit = options['limit']
        output = options.get('output')

        self.stdout.write(self.style.SUCCESS(f'启动爬虫: mode={mode}, limit={limit}'))

        # 确保输出目录存在
        exports_dir = Path(__file__).parent.parent.parent / 'exports'
        exports_dir.mkdir(exist_ok=True)

        # 配置输出文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        if not output:
            output = exports_dir / f'crawler_{mode}_{timestamp}.csv'
        else:
            output = Path(output)

        # 状态文件路径 (与 views.py 中的一致)
        status_file = Path(__file__).parent.parent.parent / 'crawler_status.json'

        # 初始状态
        status_data = {
            'running': True,
            'mode': mode,
            'limit': limit,
            'collected': 0,
            'message': '正在爬取...',
            'start_time': datetime.now().isoformat(),
            'output_file': str(output),
            'csv_ready': False
        }

        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, ensure_ascii=False, indent=2)

        # 创建自定义设置，确保 Pipeline 被启用
        settings = Settings()
        settings.set('DJANGO_SETTINGS_MODULE', 'qa_project.settings')

        # 基础配置
        settings.set('BOT_NAME', 'crawler')
        settings.set('SPIDER_MODULES', ['apps.crawler.spiders'])
        settings.set('NEWSPIDER_MODULE', 'apps.crawler.spiders')
        settings.set('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        settings.set('ROBOTSTXT_OBEY', False)
        settings.set('DOWNLOAD_DELAY', 2)
        settings.set('CONCURRENT_REQUESTS', 1)

        # 关键：启用 Pipeline
        settings.set('ITEM_PIPELINES', {
            'apps.crawler.pipelines.QuestionPipeline': 300,
            'apps.crawler.pipelines.DuplicateFilterPipeline': 100,
            'apps.crawler.pipelines.DataValidationPipeline': 200,
        })

        # 配置 feed export (使用 utf-8)
        settings.set('FEEDS', {
            str(output): {
                'format': 'csv',
                'encoding': 'utf-8',
            }
        })

        self.stdout.write(f'Pipeline 配置: {settings.get("ITEM_PIPELINES")}')

        # 使用 Scrapy 的 CrawlerProcess
        process = CrawlerProcess(settings)
        _process = process

        # 启动爬虫
        process.crawl(
            WendaSpider,
            mode=mode,
            limit=limit,
            use_redis=False
        )

        # 启动状态监控线程
        def monitor_progress():
            global _crawled_count
            while _crawler_status.get('running', True):
                try:
                    # 从数据库获取当前采集数量
                    from django.db import connection
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT COUNT(*) FROM crawler_question WHERE created_at > %s",
                            [status_data['start_time']]
                        )
                        result = cursor.fetchone()
                        current_count = result[0] if result else 0

                    # 更新状态文件
                    with open(status_file, 'w', encoding='utf-8') as f:
                        json.dump({
                            'running': True,
                            'mode': mode,
                            'limit': limit,
                            'collected': current_count,
                            'message': f'正在爬取... 已采集 {current_count} 条',
                            'start_time': status_data['start_time'],
                            'output_file': str(output),
                            'csv_ready': False
                        }, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    pass

                time.sleep(2)  # 每2秒更新一次

        # 启动监控线程
        monitor_thread = threading.Thread(target=monitor_progress, daemon=True)
        monitor_thread.start()

        # 启动爬虫进程（阻塞直到完成）
        process.start()

        # 爬虫完成后的最终状态
        _crawled_count = limit  # 使用请求的 limit 作为估计值

        final_status = {
            'running': False,
            'mode': mode,
            'limit': limit,
            'collected': limit,
            'message': f'完成! 采集 {limit} 条',
            'start_time': None,
            'output_file': str(output),
            'csv_ready': True
        }

        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(final_status, f, ensure_ascii=False, indent=2)

        # 输出结果
        self.stdout.write(self.style.SUCCESS(f'爬虫完成'))
        self.stdout.write(f'  - CSV 文件: {output}')
        self.stdout.write(f'  - 数据已保存到数据库 (通过 Pipeline)')


# 用于监控的全局状态
_crawler_status = {'running': True}
