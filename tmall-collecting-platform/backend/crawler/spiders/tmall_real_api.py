"""
天猫真实爬虫API实现
基于2026年淘宝/天猫搜索页面的实际结构实现
"""
import json
import logging
import random
import re
import time
from typing import List, Dict, Optional, Callable
from urllib.parse import urlencode, quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import SpiderConfig
from ..proxy import ProxyManager

logger = logging.getLogger('crawler')


class TmallRealAPI:
    """
    天猫/淘宝真实爬虫API

    2026年版本特性：
    1. 支持g_page_config数据解析
    2. 完整的反爬策略处理
    3. 智能重试和降级
    4. 详细的错误日志
    """

    # 2026年最新的请求头
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.taobao.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    # 淘宝搜索URL
    SEARCH_URL = "https://s.taobao.com/search"

    def __init__(
        self,
        config: SpiderConfig = None,
        proxy_manager: ProxyManager = None,
        progress_callback: Callable = None,
        cookie: str = None
    ):
        """
        初始化

        Args:
            config: 爬虫配置
            proxy_manager: 代理管理器
            progress_callback: 进度回调
            cookie: Cookie字符串（可选，建议使用非登录状态的Cookie）
        """
        self.config = config or SpiderConfig()
        self.proxy_manager = proxy_manager
        self.progress_callback = progress_callback

        # 创建session
        self.session = requests.Session()
        self._setup_session()

        # 设置Cookie
        if cookie:
            self.session.headers.update({'Cookie': cookie})
            logger.info("已设置自定义Cookie")

        # 统计
        self.items_collected = 0
        self.items_failed = 0
        self.logs: List[str] = []

    def _setup_session(self):
        """配置session"""
        # 设置默认请求头
        self.session.headers.update(self.DEFAULT_HEADERS)

        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _log(self, message: str):
        """记录日志"""
        self.logs.append(message)
        logger.info(f"[TmallRealAPI] {message}")

    def _update_progress(self, progress: str, stage: str, items: int = None):
        """更新进度"""
        if self.progress_callback:
            try:
                self.progress_callback(progress, stage, items or self.items_collected, self.logs[-5:])
            except Exception as e:
                logger.warning(f"进度更新失败: {e}")

    def _get_proxy(self) -> Optional[Dict]:
        """获取代理配置"""
        if not self.proxy_manager:
            return None

        proxy = self.proxy_manager.get_proxy()
        if proxy:
            return {'http': proxy.url, 'https': proxy.url}
        return None

    def _make_request(
        self,
        url: str,
        params: Dict = None,
        timeout: int = 30
    ) -> Optional[requests.Response]:
        """
        发送HTTP请求

        Args:
            url: 请求URL
            params: URL参数
            timeout: 超时时间

        Returns:
            Response对象，失败返回None
        """
        try:
            proxies = self._get_proxy()

            response = self.session.get(
                url,
                params=params,
                proxies=proxies,
                timeout=timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            return response

        except requests.exceptions.Timeout:
            self._log(f"请求超时: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            self._log(f"HTTP错误: {e.response.status_code}")
            # 检测是否被重定向到登录页
            if 'login' in e.response.url or e.response.status_code == 302:
                self._log("检测到登录重定向，Cookie可能已失效")
            return None
        except requests.exceptions.RequestException as e:
            self._log(f"请求异常: {e}")
            return None

    def _extract_g_page_config(self, html: str) -> Optional[Dict]:
        """
        从HTML中提取g_page_config数据

        这是淘宝搜索结果页面的主要数据源

        Args:
            html: 页面HTML

        Returns:
            解析后的配置字典，失败返回None
        """
        try:
            # 方法1: 标准格式 g_page_config = {...};
            pattern = r'g_page_config\s*=\s*(\{.*?\});'
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    config_str = match.group(1).rstrip(';').strip()
                    return json.loads(config_str)
                except json.JSONDecodeError:
                    pass

            # 方法2: 可能没有尾随分号
            pattern = r'g_page_config\s*=\s*(\{.*?\})\s*(?:</script>|var)'
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass

            # 方法3: 查找整个script块
            script_pattern = r'<script[^>]*>.*?g_page_config\s*=\s*(\{.*?\}).*?</script>'
            match = re.search(script_pattern, html, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass

            self._log("未找到g_page_config数据")
            return None

        except Exception as e:
            self._log(f"提取g_page_config失败: {e}")
            return None

    def _extract_auctions(self, g_page_config: Dict) -> List[Dict]:
        """
        从g_page_config中提取商品列表

        Args:
            g_page_config: 解析后的配置字典

        Returns:
            商品列表
        """
        auctions = []

        try:
            # 标准路径: mods.itemlist.data.auctions
            if 'mods' in g_page_config:
                mods = g_page_config['mods']

                # 尝试itemlist
                if 'itemlist' in mods:
                    itemlist = mods['itemlist']
                    if isinstance(itemlist, dict) and 'data' in itemlist:
                        data = itemlist['data']
                        # 优先auctions，备用items
                        if 'auctions' in data:
                            auctions = data['auctions']
                        elif 'items' in data:
                            auctions = data['items']

                # 尝试searchlist
                if not auctions and 'searchlist' in mods:
                    searchlist = mods['searchlist']
                    if isinstance(searchlist, dict) and 'data' in searchlist:
                        auctions = searchlist['data'].get('items', [])

            if auctions and isinstance(auctions, list):
                self._log(f"从g_page_config提取到 {len(auctions)} 个商品")
                return auctions

            self._log("g_page_config中未找到商品数据")
            return []

        except Exception as e:
            self._log(f"提取auctions失败: {e}")
            return []

    def _normalize_product(self, auction: Dict) -> Optional[Dict]:
        """
        标准化商品数据

        淘宝商品字段说明：
        - raw_title: 原始标题（可能含高亮标记）
        - view_price: 显示价格
        - view_sales: 显示销量（如"2000+人付款"）
        - nick: 卖家昵称
        - pic_url: 商品图片
        - detail_url: 详情页链接
        - item_loc: 发货地

        Args:
            auction: 原始商品数据

        Returns:
            标准化后的商品数据
        """
        try:
            # 提取标题
            title = auction.get('raw_title', '') or auction.get('title', '')
            if title:
                # 清理HTML标签和高亮标记
                title = re.sub(r'<span[^>]*>|</span>', '', title)
                title = re.sub(r'<[^>]+>', '', title)
                title = ' '.join(title.split()).strip()[:200]

            # 提取价格
            price = auction.get('view_price', '0')

            # 提取销量
            sales = auction.get('view_sales', '') or auction.get('view_sales_text', '0')

            # 提取店铺
            shop = auction.get('nick', '')

            # 提取图片URL
            image_url = auction.get('pic_url', '')
            if image_url and not image_url.startswith('http'):
                image_url = 'https:' + image_url if image_url.startswith('//') else 'https://' + image_url

            # 提取详情URL
            detail_url = auction.get('detail_url', '')
            if detail_url and not detail_url.startswith('http'):
                detail_url = 'https:' + detail_url if detail_url.startswith('//') else 'https://' + detail_url

            # 提取发货地
            item_loc = auction.get('item_loc', '')

            # 验证必填字段
            if not title and not price:
                return None

            return {
                'title': title,
                'price': str(price),
                'sales': str(sales),
                'shop': shop,
                'image_url': image_url,
                'detail_url': detail_url,
                'brand': '',  # 淘宝搜索结果不直接提供品牌信息
                'item_loc': item_loc,
            }

        except Exception as e:
            self._log(f"标准化商品失败: {e}")
            return None

    def _build_search_params(self, keyword: str, page: int = 1) -> Dict:
        """
        构建搜索参数

        Args:
            keyword: 搜索关键词
            page: 页码

        Returns:
            参数字典
        """
        return {
            'q': keyword,
            's': (page - 1) * 44,  # 每页44条
            'sort': 'sale-desc',    # 销量降序
            'imgfile': '',
            'js': '1',
            'stats_click': 'search_radio_all:1',
            'initiative_id': f'staobaoz_{time.strftime("%Y%m%d")}',
            'ie': 'utf8',
            'bcoffset': '0',
            'ntoffset': '0',
            'p4ppushleft': '1,48',
        }

    def _check_login_page(self, html: str) -> bool:
        """检测是否被重定向到登录页"""
        login_indicators = [
            '登录页面',
            '全登陆不允许iframe嵌入',
            'login.taobao.com',
            'logins Taobao'
        ]
        return any(indicator in html for indicator in login_indicators)

    def _check_captcha(self, html: str) -> bool:
        """检测是否有验证码"""
        captcha_indicators = [
            '验证码',
            'captcha',
            '滑块',
            'slideVerify'
        ]
        return any(indicator in html for indicator in captcha_indicators)

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
            max_pages: 最大页数

        Returns:
            搜索结果
        """
        max_pages = max_pages or self.config.max_pages
        all_products = []
        success_count = 0
        fail_count = 0

        self._log(f"开始搜索: {keyword}, 页数: {max_pages}")

        for current_page in range(page, page + max_pages):
            # 更新进度
            progress = f"{int((current_page - page) / max_pages * 100)}%"
            self._update_progress(progress, f'搜索 {keyword} 第{current_page}页', success_count)

            # 构建请求
            params = self._build_search_params(keyword, current_page)
            self._log(f"请求: {self.SEARCH_URL}?{urlencode(params)}")

            # 发送请求
            response = self._make_request(self.SEARCH_URL, params=params)

            if not response:
                fail_count += 44
                self._log(f"第{current_page}页请求失败")
                continue

            # 检查HTML内容
            html = response.text

            # 检测登录页
            if self._check_login_page(html):
                self._log("检测到登录页，Cookie可能已失效，请更新Cookie")
                fail_count += 44
                break

            # 检测验证码
            if self._check_captcha(html):
                self._log("检测到验证码，请稍后重试或使用浏览器获取新Cookie")
                fail_count += 44
                break

            # 提取g_page_config
            g_page_config = self._extract_g_page_config(html)

            if not g_page_config:
                fail_count += 44
                self._log(f"第{current_page}页无法提取数据")
                continue

            # 提取商品列表
            auctions = self._extract_auctions(g_page_config)

            if not auctions:
                fail_count += 44
                self._log(f"第{current_page}页未找到商品")
                continue

            # 标准化商品数据
            for auction in auctions:
                product = self._normalize_product(auction)
                if product:
                    all_products.append(product)
                    success_count += 1

            self._log(f"第{current_page}页成功获取 {len(auctions)} 个商品")

            # 请求间隔（重要！避免触发反爬）
            delay = random.uniform(3, 8)  # 3-8秒随机延迟
            self._log(f"等待 {delay:.1f} 秒...")
            time.sleep(delay)

        # 最终进度
        self._update_progress('100%', '搜索完成', success_count)

        self.items_collected = success_count
        self.items_failed = fail_count

        return {
            'success': success_count,
            'failed': fail_count,
            'products': all_products,
            'source': 'tmall_real_api',
            'logs': self.logs
        }

    def test_connection(self, keyword: str = "高达模型") -> Dict:
        """
        测试连接

        Args:
            keyword: 测试搜索关键词

        Returns:
            测试结果
        """
        self._log("测试连接...")

        try:
            params = self._build_search_params(keyword, 1)
            response = self._make_request(self.SEARCH_URL, params=params)

            if not response:
                return {
                    'success': False,
                    'message': '请求失败，请检查网络连接'
                }

            html = response.text

            # 检测登录页
            if self._check_login_page(html):
                return {
                    'success': False,
                    'message': '检测到登录页，请更新Cookie'
                }

            # 检测验证码
            if self._check_captcha(html):
                return {
                    'success': False,
                    'message': '检测到验证码，请稍后重试'
                }

            # 尝试提取数据
            g_page_config = self._extract_g_page_config(html)

            if g_page_config:
                auctions = self._extract_auctions(g_page_config)
                return {
                    'success': True,
                    'message': f'连接正常，获取到 {len(auctions)} 个商品',
                    'sample_products': auctions[:2] if auctions else []
                }

            return {
                'success': False,
                'message': '无法提取数据，页面结构可能已变化'
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'测试异常: {str(e)}'
            }
