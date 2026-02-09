"""
Playwright浏览器模块
通过浏览器自动化获取天猫商品数据
作为API降级方案
"""
import logging
import random
import time
from typing import List, Dict, Optional, Callable
from urllib.parse import quote

from playwright.sync_api import sync_playwright, Page, Browser
from playwright_stealth import stealth

from ..config import SpiderConfig
from ..proxy import ProxyManager

logger = logging.getLogger('crawler')


class TmallPlaywright:
    """
    天猫Playwright浏览器爬虫

    功能：
    1. 启动浏览器
    2. 模拟搜索操作
    3. 滚动加载更多
    4. 解析页面获取商品数据
    """

    # 搜索URL
    SEARCH_URL = "https://s.taobao.com/search?q={keyword}&page={page}"

    # User-Agent列表
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

    def __init__(
        self,
        config: SpiderConfig = None,
        proxy_manager: ProxyManager = None,
        progress_callback: Callable = None
    ):
        """
        初始化Playwright爬虫

        Args:
            config: 爬虫配置
            proxy_manager: 代理管理器
            progress_callback: 进度回调函数
        """
        self.config = config or SpiderConfig()
        self.proxy_manager = proxy_manager
        self.progress_callback = progress_callback

        self.playwright = None
        self.browser = None
        self.context = None

        self.items_collected = 0
        self.items_failed = 0
        self.logs: List[str] = []

    def _log(self, message: str):
        """记录日志"""
        self.logs.append(message)
        logger.info(f"[TmallPlaywright] {message}")

    def _update_progress(self, progress: str, stage: str, items: int = None):
        """更新进度"""
        if self.progress_callback:
            try:
                self.progress_callback(progress, stage, items or self.items_collected, self.logs[-5:])
            except Exception as e:
                logger.warning(f"更新进度失败: {e}")

    def _get_random_ua(self) -> str:
        """获取随机User-Agent"""
        return random.choice(self.USER_AGENTS)

    def _start_browser(self):
        """启动浏览器"""
        self._log("启动浏览器...")

        self.playwright = sync_playwright().start()

        # 浏览器配置
        browser_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--window-size=1920,1080',
        ]

        # 启动浏览器
        self.browser = self.playwright.chromium.launch(
            headless=self.config.headless,
            args=browser_args
        )

        # 创建浏览器上下文
        self.context = self.browser.new_context(
            viewport={'width': self.config.viewport_width, 'height': self.config.viewport_height},
            user_agent=self._get_random_ua(),
            locale='zh-CN',
        )

        self._log("浏览器启动成功")

    def _stop_browser(self):
        """停止浏览器"""
        if self.context:
            self.context.close()
            self.context = None

        if self.browser:
            self.browser.close()
            self.browser = None

        if self.playwright:
            self.playwright.stop()
            self.playwright = None

        self._log("浏览器已关闭")

    def _navigate_to_search(self, page: Page, keyword: str, page_num: int = 1):
        """
        导航到搜索结果页面

        Args:
            page: Page对象
            keyword: 搜索关键词
            page_num: 页码
        """
        url = self.SEARCH_URL.format(
            keyword=quote(keyword),
            page=page_num
        )

        self._log(f"访问: {url}")

        # 设置反检测
        stealth(page)

        # 访问页面
        page.goto(url, wait_until='networkidle', timeout=30000)

        # 随机等待
        time.sleep(random.uniform(1, 2))

    def _scroll_to_load(self, page: Page, scroll_times: int = 3):
        """
        滚动页面加载更多内容

        Args:
            page: Page对象
            scroll_times: 滚动次数
        """
        self._log(f"开始滚动加载 (共{scroll_times}次)")

        for i in range(scroll_times):
            # 滚动到页面底部
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(random.uniform(1, 2))

            # 尝试点击"加载更多"按钮
            try:
                load_more = page.query_selector('text=加载更多')
                if load_more:
                    load_more.click()
                    time.sleep(random.uniform(1, 2))
            except Exception:
                pass

            self._log(f"完成第{i + 1}次滚动")

    def _extract_products(self, page: Page) -> List[Dict]:
        """
        从页面提取商品数据

        Args:
            page: Page对象

        Returns:
            商品列表
        """
        products = []

        # 尝试多种选择器
        selectors = [
            '.items .item',
            '.search-item',
            '.item--middle',
            '[data-category=" auctions"]',
        ]

        for selector in selectors:
            try:
                items = page.query_selector_all(selector)
                if items:
                    self._log(f"使用选择器 '{selector}' 找到 {len(items)} 个商品")
                    break
            except Exception:
                continue

        if not items:
            self._log("未找到商品元素，尝试页面解析...")
            return []

        for item in items:
            try:
                product = self._parse_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                self._log(f"解析商品失败: {e}")
                continue

        return products

    def _parse_item(self, item) -> Optional[Dict]:
        """
        解析单个商品元素

        Args:
            item: 商品元素

        Returns:
            商品数据字典
        """
        try:
            # 标题
            title = ''
            title_elem = item.query_selector('.title, .item-title, .title a, [class*="title"]')
            if title_elem:
                title = title_elem.inner_text().strip()

            # 价格
            price = ''
            price_elem = item.query_selector('.price, .item-price, [class*="price"]')
            if price_elem:
                price = price_elem.inner_text().strip()
                price = price.replace('¥', '').replace('￥', '').strip()

            # 销量
            sales = ''
            sales_elem = item.query_selector('.sales, .item-sales, [class*="sales"]')
            if sales_elem:
                sales = sales_elem.inner_text().strip()
                sales = sales.replace('人付款', '').replace('+', '').strip()

            # 店铺
            shop = ''
            shop_elem = item.query_selector('.shop, .shop-name, [class*="shop"]')
            if shop_elem:
                shop = shop_elem.inner_text().strip()

            # 图片
            image_url = ''
            img_elem = item.query_selector('img')
            if img_elem:
                image_url = img_elem.get_attribute('src') or ''
                if not image_url:
                    image_url = img_elem.get_attribute('data-src') or ''

            # 详情链接
            detail_url = ''
            link_elem = item.query_selector('a')
            if link_elem:
                detail_url = link_elem.get_attribute('href') or ''

            if title:
                return {
                    'title': title[:200],
                    'price': price or '0',
                    'sales': sales or '0',
                    'shop': shop,
                    'image_url': image_url,
                    'detail_url': f"https:{detail_url}" if detail_url.startswith('//') else detail_url,
                    'brand': '',
                }

        except Exception as e:
            self._log(f"解析商品元素失败: {e}")

        return None

    def _extract_from_page_source(self, page: Page) -> List[Dict]:
        """
        从页面源码中提取数据（备选方案）

        Args:
            page: Page对象

        Returns:
            商品列表
        """
        products = []

        try:
            # 获取页面HTML
            html = page.content()

            # 尝试提取JSON数据
            import re
            import json

            # 查找g_page_config中的数据
            pattern = r'g_page_config\s*=\s*(\{[^<]+\});'
            match = re.search(pattern, html)
            if match:
                config = json.loads(match.group(1))
                items = config.get('mods', {}).get('itemlist', {}).get('data', {}).get('items', [])
                for item in items:
                    product = {
                        'title': item.get('title', ''),
                        'price': str(item.get('view_price', '0')),
                        'sales': str(item.get('view_sales', '0')),
                        'shop': item.get('nick', ''),
                        'image_url': item.get('pic_url', ''),
                        'detail_url': 'https:' + item.get('detail_url', '') if item.get('detail_url') else '',
                        'brand': item.get('brand', ''),
                    }
                    products.append(product)

                self._log(f"从页面源码提取到 {len(products)} 个商品")

        except Exception as e:
            self._log(f"从源码提取失败: {e}")

        return products

    def search(
        self,
        keyword: str,
        page: int = 1,
        max_pages: int = None
    ) -> Dict:
        """
        搜索商品

        Args:
            keyword: 搜索关键词
            page: 起始页码
            max_pages: 最大采集页数

        Returns:
            搜索结果
        """
        max_pages = max_pages or self.config.max_pages
        all_products = []
        success_count = 0
        fail_count = 0

        self._log(f"开始Playwright搜索: {keyword}, 页数: {max_pages}")

        try:
            # 启动浏览器
            self._start_browser()

            for current_page in range(page, page + max_pages):
                # 更新进度
                progress = f"{int((current_page - page) / max_pages * 100)}%"
                self._update_progress(progress, f'采集 {keyword} 第{current_page}页', success_count)

                # 创建新页面
                page_obj = self.context.new_page()
                stealth(page_obj)

                # 导航到搜索页
                self._navigate_to_search(page_obj, keyword, current_page)

                # 滚动加载
                self._scroll_to_load(page_obj, scroll_times=3)

                # 提取商品
                products = self._extract_products(page_obj)

                if products:
                    all_products.extend(products)
                    success_count += len(products)
                    self._log(f"第{current_page}页获取 {len(products)} 个商品")
                else:
                    # 尝试从源码提取
                    products = self._extract_from_page_source(page_obj)
                    if products:
                        all_products.extend(products)
                        success_count += len(products)
                        self._log(f"第{current_page}页(源码)获取 {len(products)} 个商品")
                    else:
                        fail_count += 44
                        self._log(f"第{current_page}页未找到商品")

                # 关闭页面
                page_obj.close()

                # 请求间隔
                time.sleep(self.config.delay_between_requests)

        except Exception as e:
            self._log(f"Playwright搜索异常: {e}")
            fail_count = 44 * max_pages

        finally:
            # 停止浏览器
            self._stop_browser()

        # 最终进度
        self._update_progress('100%', '采集完成', success_count)

        self.items_collected = success_count
        self.items_failed = fail_count

        return {
            'success': success_count,
            'failed': fail_count,
            'products': all_products,
            'source': 'playwright',
            'logs': self.logs
        }

    def test_connection(self) -> Dict:
        """
        测试浏览器连接

        Returns:
            测试结果
        """
        self._log("测试Playwright连接...")

        try:
            self._start_browser()

            page = self.context.new_page()
            stealth(page)

            # 访问首页测试
            page.goto('https://www.tmall.com/', wait_until='networkidle', timeout=30000)
            time.sleep(2)

            title = page.title()

            self._stop_browser()

            return {
                'success': True,
                'message': 'Playwright连接正常',
                'title': title
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Playwright测试异常: {str(e)}'
            }
