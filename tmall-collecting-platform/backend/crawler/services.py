"""
Crawler Services - 爬虫服务层
提供爬虫任务的启动、状态查询等功能，替代 Celery 异步任务
"""
import logging
import uuid
from datetime import datetime
from threading import Thread

from django.utils import timezone

from products.models import Product, CrawlLog

logger = logging.getLogger('crawler')


class CrawlerService:
    """
    爬虫服务类

    使用后台线程执行爬虫任务，替代 Celery + Redis 架构
    适用于少量数据采集场景（约 200 条）
    """

    @staticmethod
    def start_crawl(mode='normal', keywords=None, max_pages=None):
        """
        启动爬虫采集任务

        Args:
            mode: 采集模式 ('normal': 标准模式, 'demo': 演示模式, 'batch': 分批采集)
            keywords: 搜索关键词（单个字符串）
            max_pages: 采集页数限制 (仅 normal 模式有效)

        Returns:
            str: 任务 ID (UUID)
        """
        # 生成任务 ID
        task_id = str(uuid.uuid4())

        # 创建 CrawlLog 记录
        log = CrawlLog.objects.create(
            task_id=task_id,
            status='running',
            mode=mode,
            keywords=keywords or '',
            source_type='mtop_api',
            start_time=timezone.now()
        )

        logger.info(f"创建爬虫任务: {task_id}, 模式: {mode}, 关键词: {keywords}, 页数: {max_pages}")

        # 启动后台线程执行采集
        thread = Thread(
            target=CrawlerService._run_crawler,
            args=(task_id, mode, keywords or '高达模型', max_pages),
            daemon=True
        )
        thread.start()

        return task_id

    @staticmethod
    def get_status(task_id):
        """
        获取任务状态

        Args:
            task_id: 任务 ID

        Returns:
            dict: 任务状态信息，如果任务不存在返回 None
        """
        try:
            log = CrawlLog.objects.get(task_id=task_id)

            # 判断是否正在运行
            is_running = log.status == 'running'

            # 计算进度
            if is_running:
                progress = '50%'
            elif log.status == 'success':
                progress = '100%'
            else:
                progress = '失败'

            return {
                'task_id': task_id,
                'is_running': is_running,
                'status': log.status,
                'items_collected': log.items_collected,
                'items_success': log.items_success,
                'items_failed': log.items_failed,
                'start_time': log.start_time.isoformat() if log.start_time else None,
                'end_time': log.end_time.isoformat() if log.end_time else None,
                'error_message': log.error_message,
                'progress': progress,
                'batch_no': log.log_content.split('批次号: ')[1].split('\n')[0] if log.log_content and '批次号: ' in log.log_content else None
            }

        except CrawlLog.DoesNotExist:
            return None

    @staticmethod
    def _run_crawler(task_id, mode, keywords, max_pages=None):
        """
        后台线程中执行爬虫采集

        Args:
            task_id: 任务 ID
            mode: 采集模式
            keywords: 搜索关键词（单个字符串）
            max_pages: 采集页数限制
        """
        from users.models import SystemConfig
        from crawler.spiders.taobao_mtop_api import TaobaoMtopAPI

        log = CrawlLog.objects.get(task_id=task_id)

        try:
            logger.info(f"任务 {task_id} 开始执行采集")

            # 1. 获取 Cookie
            cookie = SystemConfig.get_value('taobao_cookie', '')
            if not cookie:
                raise Exception("Cookie 未配置，请先在系统配置中设置淘宝 Cookie")

            # 2. 初始化爬虫 API
            api = TaobaoMtopAPI(cookie=cookie)

            # 3. 确定采集页数
            if max_pages:
                pages = max_pages
            elif mode == 'normal':
                pages = 1
            elif mode == 'demo':
                pages = 3
            else:  # batch
                pages = 5

            # 4. 执行采集
            keyword = keywords if keywords else "高达模型"
            logger.info(f"任务 {task_id} 搜索关键词: {keyword}, 页数: {pages}")

            result = api.search(keyword=keyword, max_pages=pages)

            # 5. 保存商品数据到数据库
            products_saved = 0
            batch_no = datetime.now().strftime('%Y%m%d%H%M%S')

            for item in result.get('products', []):
                try:
                    Product.objects.create(
                        product_id=item.get('product_id', ''),
                        title=item.get('title', ''),
                        price=item.get('price', '0'),
                        price_unit=item.get('price_unit', ''),
                        price_desc=item.get('price_desc', ''),
                        sales=int(item.get('sales', 0)) if item.get('sales', '').isdigit() else 0,
                        shop=item.get('shop', ''),
                        seller_nick=item.get('seller_nick', ''),
                        shop_tags=item.get('shop_tags', ''),
                        region=item.get('region', ''),
                        tags=item.get('tags', ''),
                        product_attributes=item.get('product_attributes'),
                        image_url=item.get('image_url', ''),
                        detail_url=item.get('detail_url', ''),
                        brand=item.get('brand', ''),
                        category=item.get('category', ''),
                        batch_no=batch_no,
                        crawl_time=timezone.now()
                    )
                    products_saved += 1
                except Exception as e:
                    logger.warning(f"保存商品失败: {e}, 商品: {item.get('title', 'Unknown')}")

            # 6. 更新日志状态
            if products_saved == 0:
                # 没有采集到任何数据，标记为失败
                log.status = 'failed'
                log.items_collected = 0
                log.items_success = 0
                log.items_failed = 1
                log.end_time = timezone.now()
                error_msg = result.get('logs', ['未采集到任何数据'])[-1] if result.get('logs') else '未采集到任何数据，请检查Cookie配置'
                log.error_message = error_msg
                log.log_content = '\n'.join(result.get('logs', []))
                log.save()

                logger.error(f"任务 {task_id} 失败: 未采集到任何数据")
            else:
                # 成功采集到数据
                log.status = 'success'
                log.items_collected = products_saved
                log.items_success = products_saved
                log.items_failed = 0
                log.end_time = timezone.now()
                log.log_content = '\n'.join(result.get('logs', []))
                log.log_content = f"批次号: {batch_no}\n" + log.log_content
                log.save()

                logger.info(f"任务 {task_id} 完成, 成功保存 {products_saved} 个商品, 批次号: {batch_no}")

        except Exception as e:
            logger.error(f"任务 {task_id} 失败: {str(e)}")

            # 更新为失败状态
            log.status = 'failed'
            log.end_time = timezone.now()
            log.error_message = str(e)
            log.save()

    @staticmethod
    def get_running_tasks():
        """
        获取正在运行的任务列表

        Returns:
            list: 正在运行的任务列表
        """
        running_logs = CrawlLog.objects.filter(status='running').order_by('-start_time')
        return [
            {
                'task_id': log.task_id,
                'mode': log.mode,
                'start_time': log.start_time.isoformat() if log.start_time else None
            }
            for log in running_logs
        ]
