"""
天猫商品爬虫
支持 API + Playwright 混合采集策略
"""
import logging
import random
import time
from decimal import Decimal, InvalidOperation
from typing import List, Dict, Callable, Optional

from django.utils import timezone
from products.models import Product, CrawlLog

from ..config import SpiderConfig, load_config_from_env
from ..proxy import create_proxy_manager
from .tmall_api import TmallAPI
from .tmall_playwright import TmallPlaywright
from .tmall_real_api import TmallRealAPI
from .taobao_mtop_api import TaobaoMtopAPI

logger = logging.getLogger('crawler')


class TmallSpider:
    """
    天猫潮玩商品爬虫

    采集策略：
    1. 优先使用 API 采集（高效）
    2. API 失败时降级到 Playwright
    3. 支持演示模式、代理IP
    """

    def __init__(
        self,
        task_id: str,
        mode: str = 'demo',
        keywords: Optional[List[str]] = None,
        config: SpiderConfig = None,
        callback: Optional[Callable] = None
    ):
        """
        初始化爬虫

        Args:
            task_id: 任务ID
            mode: 采集模式 ('demo': 演示, 'api': API, 'playwright': 浏览器, 'hybrid': 混合)
            keywords: 搜索关键词列表
            config: 爬虫配置
            callback: 进度回调函数
        """
        self.task_id = task_id
        self.mode = mode
        self.keywords = keywords or ['高达模型', '盲盒', '手办', '潮玩']
        self.callback = callback

        # 加载配置
        self.config = config or load_config_from_env()

        # 如果是演示模式
        if mode == 'demo':
            self.config.demo_mode = True

        # 设置最大页数
        self.max_pages = 2 if mode == 'demo' else self.config.max_pages

        # 初始化组件
        self.proxy_manager = None
        self.api = None
        self.playwright = None

        # 统计信息
        self.items_collected = 0
        self.items_failed = 0
        self.logs = []
        self.source_type = 'unknown'

    def _log(self, message: str):
        """记录日志"""
        self.logs.append(message)
        logger.info(f"[{self.task_id}] {message}")

    def _update_progress(self, progress: str, stage: str):
        """更新进度"""
        if self.callback:
            try:
                recent_logs = self.logs[-5:] if self.logs else []
                self.callback(progress, stage, self.items_collected, recent_logs)
            except Exception as e:
                logger.warning(f"更新进度失败: {e}")

    def _init_components(self):
        """初始化组件"""
        import os

        # 初始化代理管理器
        if self.config.use_proxy:
            self.proxy_manager = create_proxy_manager({
                'proxy_list': self.config.proxy_list
            })
            self._log("代理管理器已初始化")

        # 获取Cookie（优先从数据库，其次从环境变量）
        cookie = None
        try:
            from users.models import SystemConfig
            cookie = SystemConfig.get_value('taobao_cookie', '')
            if cookie:
                self._log("从数据库读取 Cookie")
        except Exception as e:
            self._log(f"从数据库读取 Cookie 失败: {e}")

        if not cookie:
            cookie = os.environ.get('TAOBAO_COOKIE', '')
            if cookie:
                self._log("从环境变量读取 Cookie")

        # 初始化淘宝 mtop API（最新API，优先）
        if cookie:
            self.mtop_api = TaobaoMtopAPI(
                config=self.config,
                proxy_manager=self.proxy_manager,
                progress_callback=self._progress_wrapper,
                cookie=cookie
            )
            self._log("淘宝 mtop API 已初始化（使用Cookie）")
        else:
            self.mtop_api = None
            self._log("未设置Cookie，淘宝 mtop API 不可用")

        # 初始化真实API（备用）
        if cookie:
            self.real_api = TmallRealAPI(
                config=self.config,
                proxy_manager=self.proxy_manager,
                progress_callback=self._progress_wrapper,
                cookie=cookie
            )
            self._log("真实API已初始化（使用Cookie）")
        else:
            self.real_api = None
            self._log("未设置Cookie，真实API不可用")

        # 初始化旧版API（备用）
        self.api = TmallAPI(
            config=self.config,
            proxy_manager=self.proxy_manager,
            progress_callback=self._progress_wrapper
        )

        # 初始化Playwright
        self.playwright = TmallPlaywright(
            config=self.config,
            proxy_manager=self.proxy_manager,
            progress_callback=self._progress_wrapper
        )

    def _progress_wrapper(self, progress: str, stage: str, items: int, logs: List[str]):
        """进度回调包装"""
        self.items_collected = items
        self._update_progress(progress, stage)

    def _extract_price(self, price_str: str) -> Optional[Decimal]:
        """提取价格"""
        if not price_str:
            return None

        price_str = str(price_str).replace('¥', '').replace('￥', '').replace('元', '').strip()

        try:
            return Decimal(str(price_str)).quantize(Decimal('0.01'))
        except (InvalidOperation, ValueError):
            return None

    def _extract_sales(self, sales_str: str) -> int:
        """提取销量"""
        if not sales_str:
            return 0

        sales_str = str(sales_str).replace('付款', '').replace('+', '').replace('人付款', '').strip()

        if '万' in sales_str:
            try:
                return int(float(sales_str.replace('万', '')) * 10000)
            except ValueError:
                pass

        try:
            return int(sales_str)
        except ValueError:
            return 0

    def _clean_title(self, title: str) -> str:
        """清理商品标题"""
        if not title:
            return '未知商品'

        title = ' '.join(title.split())

        import re
        title = re.sub(r'<[^>]+>', '', title)

        return title[:200]

    def _generate_demo_data(self, keyword: str, page: int) -> List[Dict]:
        """生成演示数据"""
        self._log(f"生成演示数据: {keyword}, 第 {page} 页")

        shops = ['潮玩旗舰店', '模型专家', '手办天堂', '玩具世界', '正版潮玩店']

        return [
            {
                'title': f'{keyword}相关商品 - 精选手办{page}-{i}',
                'price': str(random.randint(50, 500)),
                'sales': str(random.randint(10, 5000)),
                'shop': random.choice(shops),
                'image_url': 'https://via.placeholder.com/200',
                'detail_url': 'https://detail.tmall.com/item.htm?id=123456',
                'brand': '演示品牌',
            }
            for i in range(1, 21)
        ]

    def _save_products(self, products: List[Dict], keyword: str) -> int:
        """保存商品数据到数据库"""
        saved_count = 0
        batch_no = timezone.now().strftime('%Y%m%d%H%M%S')

        for product_data in products:
            try:
                title = self._clean_title(product_data.get('title', ''))
                price = self._extract_price(product_data.get('price', '0'))
                sales = self._extract_sales(product_data.get('sales', '0'))

                if not title or not price:
                    self.items_failed += 1
                    continue

                # 检查是否已存在（使用 product_id 或 title+shop）
                product_id = product_data.get('product_id', '')
                shop = product_data.get('shop', '')

                exists = False
                if product_id:
                    exists = Product.objects.filter(product_id=product_id).exists()
                elif title and shop:
                    exists = Product.objects.filter(title=title, shop=shop).exists()

                if exists:
                    continue

                # 准备商品属性 JSON 数据
                product_attributes = product_data.get('product_attributes')
                if product_attributes and isinstance(product_attributes, str):
                    # 如果是字符串，尝试解析或构建 JSON
                    try:
                        import json
                        # 如果是 "prop1:value1 | prop2:value2" 格式
                        if '|' in product_attributes:
                            attrs = {}
                            for item in product_attributes.split('|'):
                                if ':' in item:
                                    key, value = item.split(':', 1)
                                    attrs[key.strip()] = value.strip()
                            product_attributes = attrs
                        else:
                            product_attributes = {'raw': product_attributes}
                    except Exception:
                        product_attributes = {'raw': product_attributes}

                # 创建商品记录
                Product.objects.create(
                    product_id=product_id or f"tmp_{batch_no}_{saved_count}",
                    title=title,
                    price=price,
                    price_unit=product_data.get('price_unit', ''),
                    price_desc=product_data.get('price_desc', ''),
                    sales=sales,
                    shop=shop,
                    seller_nick=product_data.get('seller_nick', ''),
                    shop_tags=product_data.get('shop_tags', ''),
                    region=product_data.get('region', ''),
                    tags=product_data.get('tags', ''),
                    product_attributes=product_attributes,
                    image_url=product_data.get('image_url', ''),
                    detail_url=product_data.get('detail_url', ''),
                    brand=product_data.get('brand', '') or keyword,
                    category=product_data.get('category', '') or '潮玩',
                    batch_no=batch_no,
                    crawl_time=timezone.now(),
                )

                saved_count += 1
                self.items_collected += 1

            except Exception as e:
                self._log(f"保存商品失败: {e}")
                self.items_failed += 1

        return saved_count

    def run_api(self, keyword: str) -> Dict:
        """使用API采集"""
        self._log(f"使用API采集: {keyword}")

        result = self.api.search(keyword, max_pages=self.max_pages)

        return result

    def run_playwright(self, keyword: str) -> Dict:
        """使用Playwright采集"""
        self._log(f"使用Playwright采集: {keyword}")

        result = self.playwright.search(keyword, max_pages=self.max_pages)

        return result

    def run_demo(self, keyword: str) -> Dict:
        """演示模式"""
        self._log(f"演示模式采集: {keyword}")

        total_saved = 0

        for page in range(1, self.max_pages + 1):
            progress = f"{int((page / self.max_pages) * 100)}%"
            self._update_progress(progress, f'演示 {keyword} 第{page}页')

            products = self._generate_demo_data(keyword, page)

            if products:
                saved = self._save_products(products, keyword)
                total_saved += saved
                self._log(f"第{page}页保存成功: {saved}条")

            time.sleep(random.uniform(0.5, 1.5))

        return {
            'success': total_saved,
            'failed': 0,
            'source': 'demo',
            'products': [],
            'logs': self.logs
        }

    def run_hybrid(self, keyword: str) -> Dict:
        """
        混合模式：淘宝 mtop API -> 真实API -> 旧版API -> Playwright -> 演示数据

        降级策略：
        1. 优先使用淘宝 mtop API（最新推荐接口）
        2. 失败则使用真实API（基于g_page_config解析）
        3. 失败则使用旧版API
        4. 失败则使用Playwright浏览器
        5. 最后使用演示数据
        """
        self._log(f"混合模式采集: {keyword}")

        # 步骤1: 尝试淘宝 mtop API（最新推荐接口）
        if self.mtop_api:
            self._log("步骤1: 尝试淘宝 mtop API（推荐接口）...")
            mtop_result = self.mtop_api.search(keyword, max_pages=self.max_pages)

            if mtop_result['success'] > 0:
                self._log(f"淘宝 mtop API 采集成功: {mtop_result['success']}条")
                self.source_type = 'mtop_api'

                # 保存商品
                saved = self._save_products(mtop_result['products'], keyword)
                self._log(f"保存 mtop API 数据: {saved}条")

                return {
                    'success': saved,
                    'failed': mtop_result.get('failed', 0),
                    'source': 'mtop_api',
                    'logs': self.logs
                }

            self._log("淘宝 mtop API 失败或无数据")

        # 步骤2: 尝试真实API
        if self.real_api:
            self._log("步骤2: 尝试真实API（g_page_config解析）...")
            real_api_result = self.real_api.search(keyword, max_pages=self.max_pages)

            if real_api_result['success'] > 0:
                self._log(f"真实API采集成功: {real_api_result['success']}条")
                self.source_type = 'real_api'

                # 保存商品
                saved = self._save_products(real_api_result['products'], keyword)
                self._log(f"保存真实API数据: {saved}条")

                return {
                    'success': saved,
                    'failed': real_api_result.get('failed', 0),
                    'source': 'real_api',
                    'logs': self.logs
                }

            self._log("真实API失败或无数据")

        # 步骤3: 尝试旧版API
        self._log("步骤3: 尝试旧版API...")
        self._update_progress('50%', '尝试旧版API')

        api_result = self.run_api(keyword)

        if api_result['success'] > 0:
            self._log(f"旧版API采集成功: {api_result['success']}条")
            self.source_type = 'api'

            # 保存商品
            saved = self._save_products(api_result['products'], keyword)
            self._log(f"保存旧版API数据: {saved}条")

            return {
                'success': saved,
                'failed': api_result.get('failed', 0),
                'source': 'api',
                'logs': self.logs
            }

        # 步骤4: API失败，降级到Playwright
        self._log("API采集失败，降级到Playwright...")
        self._update_progress('70%', '切换到Playwright')

        pw_result = self.run_playwright(keyword)

        if pw_result['success'] > 0:
            self._log(f"Playwright采集成功: {pw_result['success']}条")
            self.source_type = 'playwright'

            # 保存商品
            saved = self._save_products(pw_result['products'], keyword)
            self._log(f"保存Playwright数据: {saved}条")

            return {
                'success': saved,
                'failed': pw_result.get('failed', 0),
                'source': 'playwright',
                'logs': self.logs
            }

        # 步骤5: 所有采集方式都失败，使用演示数据
        self._log("所有采集方式都失败，使用演示数据")
        self._update_progress('90%', '降级到演示模式')

        demo_result = self.run_demo(keyword)
        self.source_type = 'demo'

        return {
            'success': demo_result['success'],
            'failed': 0,
            'source': 'demo',
            'logs': self.logs
        }

    def run(self) -> Dict:
        """执行爬虫任务"""
        self._log("=== 开始爬虫任务 ===")
        self._log(f"模式: {self.mode}, 关键词: {self.keywords[:1]}, 最大页数: {self.max_pages}")

        total_saved = 0

        try:
            # 初始化组件
            if self.mode != 'demo':
                self._init_components()

            # 采集第一个关键词
            keyword = self.keywords[0]

            if self.mode == 'demo':
                result = self.run_demo(keyword)
            elif self.mode == 'api':
                result = self.run_api(keyword)
            elif self.mode == 'playwright':
                result = self.run_playwright(keyword)
            else:  # hybrid 或其他
                result = self.run_hybrid(keyword)

            total_saved = result['success']
            self.source_type = result.get('source', 'unknown')

            # 最终进度更新
            self._update_progress('100%', '采集完成')

            self._log("=== 爬虫任务完成 ===")
            self._log(f"总计保存: {total_saved}条, 失败: {self.items_failed}条")
            self._log(f"数据来源: {self.source_type}")

            return {
                'success': total_saved,
                'failed': self.items_failed,
                'source_type': self.source_type,
                'logs': self.logs
            }

        except Exception as e:
            self._log(f"爬虫执行异常: {e}")
            raise

    def __del__(self):
        """析构函数，确保资源释放"""
        try:
            if self.playwright:
                self.playwright._stop_browser()
        except Exception:
            pass

        try:
            if hasattr(self, 'real_api') and self.real_api:
                if hasattr(self.real_api, 'session'):
                    self.real_api.session.close()
        except Exception:
            pass

        try:
            if hasattr(self, 'api') and self.api:
                if hasattr(self.api, 'session'):
                    self.api.session.close()
        except Exception:
            pass
