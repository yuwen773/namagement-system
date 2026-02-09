"""
天猫API调用模块
通过天猫/淘宝搜索接口获取商品数据
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
from ..proxy import ProxyManager, ProxyInfo

logger = logging.getLogger('crawler')


class TmallAPI:
    """
    天猫/淘宝搜索API调用类

    功能：
    1. 构建搜索请求参数
    2. 发送HTTP请求获取JSON数据
    3. 解析商品信息
    """

    # 请求头，模拟浏览器（基于2026年最新浏览器特征）
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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

    # 淘宝搜索API端点
    SEARCH_API = "https://s.taobao.com/search"

    def __init__(
        self,
        config: SpiderConfig = None,
        proxy_manager: ProxyManager = None,
        progress_callback: Callable = None,
        cookie: str = None
    ):
        """
        初始化天猫API

        Args:
            config: 爬虫配置
            proxy_manager: 代理管理器
            progress_callback: 进度回调函数
            cookie: 可选的Cookie字符串
        """
        self.config = config or SpiderConfig()
        self.proxy_manager = proxy_manager
        self.progress_callback = progress_callback

        # 创建session并配置重试
        self.session = self._create_session()

        # 设置Cookie
        if cookie:
            self.session.headers.update({'Cookie': cookie})

        # 统计信息
        self.items_collected = 0
        self.items_failed = 0
        self.logs: List[str] = []

    def _create_session(self) -> requests.Session:
        """创建requests session并配置重试策略"""
        session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=self.config.retry_times,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # 设置默认请求头
        session.headers.update(self.DEFAULT_HEADERS)

        return session

    def _log(self, message: str):
        """记录日志"""
        self.logs.append(message)
        logger.info(f"[TmallAPI] {message}")

    def _update_progress(self, progress: str, stage: str, items: int = None):
        """更新进度"""
        if self.progress_callback:
            try:
                self.progress_callback(progress, stage, items or self.items_collected, self.logs[-5:])
            except Exception as e:
                logger.warning(f"更新进度失败: {e}")

    def _get_proxy_url(self) -> Optional[Dict]:
        """获取代理配置"""
        if not self.proxy_manager:
            return None

        proxy = self.proxy_manager.get_proxy()
        if not proxy:
            return None

        return {
            'http': proxy.url,
            'https': proxy.url,
        }

    def _make_request(
        self,
        url: str,
        params: Dict = None,
        headers: Dict = None,
        timeout: int = None
    ) -> Optional[requests.Response]:
        """
        发送HTTP请求

        Args:
            url: 请求URL
            params: URL参数
            headers: 请求头
            timeout: 超时时间

        Returns:
            Response对象，失败返回None
        """
        timeout = timeout or self.config.request_timeout

        try:
            # 获取代理
            proxies = self._get_proxy_url()

            # 合并请求头
            request_headers = self.DEFAULT_HEADERS.copy()
            if headers:
                request_headers.update(headers)

            # 发送请求
            response = self.session.get(
                url,
                params=params,
                headers=request_headers,
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
            self._log(f"HTTP错误: {e.response.status_code} - {url}")
            return None
        except requests.exceptions.RequestException as e:
            self._log(f"请求异常: {e}")
            return None

    def _parse_json_response(self, response: requests.Response) -> Optional[Dict]:
        """
        解析JSON响应

        Args:
            response: Response对象

        Returns:
            解析后的字典，失败返回None
        """
        try:
            # 方法1: 直接解析JSON
            return response.json()

        except json.JSONDecodeError:
            pass

        try:
            # 方法2: 从HTML中提取g_page_config数据（淘宝天猫搜索页面主要方式）
            html = response.text

            # 检测是否被重定向到登录页
            if '登录页面' in html or '全登陆不允许iframe嵌入' in html:
                self._log("检测到登录页面，Cookie可能已失效")
                return None

            # 尝试提取g_page_config中的数据（主要的商品数据源）
            pattern = r'g_page_config\s*=\s*(\{.*?\});'
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    config_json = match.group(1)
                    # 处理可能的尾随分号和额外字符
                    config_json = config_json.rstrip(';').strip()
                    return json.loads(config_json)
                except json.JSONDecodeError as e:
                    self._log(f"g_page_config JSON解析失败: {e}")

            # 尝试其他可能的JSON数据位置
            # 查找包含itemlist或auctions的script标签
            script_pattern = r'<script[^>]*>(.*?)</script>'
            for script_match in re.finditer(script_pattern, html, re.DOTALL):
                script_content = script_match.group(1)
                if 'itemlist' in script_content or 'auctions' in script_content:
                    # 尝试提取JSON
                    try:
                        # 查找JSON对象
                        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                        for json_match in re.finditer(json_pattern, script_content):
                            try:
                                data = json.loads(json_match.group(0))
                                if 'itemlist' in str(data) or 'auctions' in str(data):
                                    return data
                            except json.JSONDecodeError:
                                continue
                    except Exception:
                        continue

            # 尝试提取window.__data__等全局变量
            data_patterns = [
                r'window\.__data__\s*=\s*(\{.*?\});',
                r'var\s+pageData\s*=\s*(\{.*?\});',
                r'__NEXT_DATA__\s*=\s*(\{.*?\})',
            ]

            for pattern in data_patterns:
                match = re.search(pattern, html, re.DOTALL)
                if match:
                    try:
                        return json.loads(match.group(1))
                    except json.JSONDecodeError:
                        continue

            self._log("无法从响应中提取JSON数据")
            return None

        except (json.JSONDecodeError, re.error) as e:
            self._log(f"JSON解析错误: {e}")
            return None

    def _extract_products_from_json(self, data: Dict) -> List[Dict]:
        """
        从JSON数据中提取商品列表

        淘宝/天猫搜索结果的数据结构：
        g_page_config.mods.itemlist.data.auctions 或 items

        Args:
            data: 解析后的JSON数据

        Returns:
            商品列表
        """
        products = []

        try:
            # 主要路径：g_page_config.mods.itemlist.data.auctions（新版淘宝）
            if 'mods' in data and isinstance(data['mods'], dict):
                mods = data['mods']

                # 尝试 itemlist.auctions（新版）
                if 'itemlist' in mods:
                    itemlist_data = mods['itemlist'].get('data', {})
                    # auctions 或 items 字段
                    auctions = itemlist_data.get('auctions') or itemlist_data.get('items')
                    if auctions and isinstance(auctions, list):
                        self._log(f"从 itemlist.auctions 找到 {len(auctions)} 个商品")
                        for item in auctions:
                            product = self._normalize_product(item)
                            if product:
                                products.append(product)
                        return products

                # 尝试 searchlist.data.items
                if 'searchlist' in mods:
                    searchlist_data = mods['searchlist'].get('data', {})
                    items = searchlist_data.get('items', [])
                    if items and isinstance(items, list):
                        self._log(f"从 searchlist.items 找到 {len(items)} 个商品")
                        for item in items:
                            product = self._normalize_product(item)
                            if product:
                                products.append(product)
                        return products

                # 尝试其他可能的mods字段
                for mod_name, mod_data in mods.items():
                    if isinstance(mod_data, dict) and 'data' in mod_data:
                        items = mod_data['data'].get('items') or mod_data['data'].get('auctions')
                        if items and isinstance(items, list):
                            self._log(f"从 mods.{mod_name} 找到 {len(items)} 个商品")
                            for item in items:
                                product = self._normalize_product(item)
                                if product:
                                    products.append(product)
                            return products

            # 备用路径1：直接在根级别的 items
            if 'items' in data and isinstance(data['items'], list):
                self._log(f"从根级别 items 找到 {len(data['items'])} 个商品")
                for item in data['items']:
                    product = self._normalize_product(item)
                    if product:
                        products.append(product)
                return products

            # 备用路径2：在 result 下
            if 'result' in data:
                result = data['result']
                if isinstance(result, list):
                    self._log(f"从 result 找到 {len(result)} 个商品")
                    for item in result:
                        if isinstance(item, (list, dict)):
                            product = self._normalize_product(item)
                            if product:
                                products.append(product)
                    return products

            # 如果都没找到，记录数据结构
            keys_list = list(data.keys()) if isinstance(data, dict) else 'not a dict'
            self._log(f"未找到商品数据，数据结构: {keys_list}")

        except Exception as e:
            self._log(f"提取商品失败: {e}")

        return products

    def _normalize_product(self, item) -> Optional[Dict]:
        """
        标准化商品数据

        淘宝/天猫商品字段映射：
        - raw_title -> title
        - view_price -> price
        - view_sales -> sales
        - nick -> shop
        - pic_url -> image_url
        - detail_url -> detail_url

        Args:
            item: 原始商品数据

        Returns:
            标准化后的商品数据
        """
        try:
            if isinstance(item, list):
                # 列表格式（旧版）：[title, price, sales, shop, ...]
                if len(item) >= 4:
                    return {
                        'title': str(item[0]) if item[0] else '',
                        'price': str(item[1]) if len(item) > 1 else '0',
                        'sales': str(item[2]) if len(item) > 2 else '0',
                        'shop': str(item[3]) if len(item) > 3 else '',
                        'image_url': str(item[4]) if len(item) > 4 else '',
                        'detail_url': str(item[5]) if len(item) > 5 else '',
                        'brand': '',
                    }
                return None

            if isinstance(item, dict):
                # 字典格式（新版淘宝）
                # 标题：raw_title（原始标题，带关键词高亮标记）或 title
                raw_title = item.get('raw_title', '') or item.get('title', '') or item.get('name', '')

                # 价格：view_price（显示价格）
                price = item.get('view_price', '') or item.get('price', '') or item.get('real_price', '0')

                # 销量：view_sales（显示销量，如"2000+人付款"）
                sales = item.get('view_sales', '') or item.get('sales', '') or item.get('view_sales_text', '') or '0'

                # 店铺：nick（卖家昵称）
                shop = item.get('nick', '') or item.get('shop', '') or item.get('shop_name', '') or ''

                # 图片：pic_url（主图地址）
                image_url = item.get('pic_url', '') or item.get('image_url', '') or ''

                # 详情链接：detail_url
                detail_url = item.get('detail_url', '') or item.get('item_url', '') or ''

                # 其他可选字段
                brand = item.get('brand', '') or item.get('supplier', '') or ''
                item_loc = item.get('item_loc', '') or item.get('location', '') or ''  # 发货地

                # 清理标题中的高亮标记（淘宝会在关键词周围添加<span>标签）
                import re
                if raw_title:
                    raw_title = re.sub(r'<span[^>]*>|</span>', '', raw_title)
                    raw_title = re.sub(r'<[^>]+>', '', raw_title)  # 移除所有HTML标签
                    raw_title = ' '.join(raw_title.split())  # 清理多余空格

                # 处理图片URL（添加https前缀）
                if image_url and not image_url.startswith('http'):
                    image_url = 'https:' + image_url if image_url.startswith('//') else 'https://' + image_url

                # 处理详情URL
                if detail_url and not detail_url.startswith('http'):
                    detail_url = 'https:' + detail_url if detail_url.startswith('//') else 'https://' + detail_url

                # 至少要有标题和价格
                if not raw_title and not price:
                    return None

                return {
                    'title': raw_title[:200],  # 限制长度
                    'price': str(price),
                    'sales': str(sales),
                    'shop': shop,
                    'image_url': image_url,
                    'detail_url': detail_url,
                    'brand': brand,
                    'item_loc': item_loc,  # 发货地
                }

            return None

        except Exception as e:
            self._log(f"标准化商品数据失败: {e}")
            return None

    def _build_search_params(self, keyword: str, page: int = 1) -> Dict:
        """
        构建搜索请求参数

        淘宝/天猫搜索参数说明：
        - q: 搜索关键词（URL编码）
        - s: 分页偏移量，每页44条，公式：(page-1)*44
        - sort: 排序方式（sale-desc=销量降序，price-asc=价格升序）
        - imgfile: 是否有图
        - js: JavaScript支持
        - ie: 编码方式
        - initiative_id: 初始化ID（可选）

        Args:
            keyword: 搜索关键词
            page: 页码（从1开始）

        Returns:
            请求参数字典
        """
        # 淘宝搜索API参数（基于实际抓包分析）
        params = {
            'q': keyword,           # 搜索关键词
            's': (page - 1) * 44,   # 分页偏移，每页44条商品
            'sort': 'sale-desc',    # 按销量降序排序
            'imgfile': '',          # 是否有图（空=全部）
            'js': '1',              # JavaScript支持
            'stats_click': 'search_radio_all:1',  # 统计点击
            'initiative_id': 'staobaoz_20250101',  # 初始化ID（可调整日期）
            'ie': 'utf8',           # 编码方式
            'bcoffset': '0',        # 偏移量1
            'ntoffset': '0',        # 偏移量2
            'p4ppushleft': '1,48',  # 推广参数
        }

        return params

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
            搜索结果，包含商品列表和统计信息
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

            # 构建请求URL和参数
            url = self.SEARCH_API
            params = self._build_search_params(keyword, current_page)

            self._log(f"请求URL: {url}?{urlencode(params)}")

            # 发送请求
            response = self._make_request(url, params=params)

            if not response:
                fail_count += 44
                self._log(f"第{current_page}页请求失败")
                continue

            # 解析响应
            data = self._parse_json_response(response)

            if not data:
                self._log(f"第{current_page}页解析失败")
                fail_count += 44
                continue

            # 提取商品
            products = self._extract_products_from_json(data)

            if products:
                all_products.extend(products)
                success_count += len(products)
                self._log(f"第{current_page}页获取 {len(products)} 个商品")
            else:
                fail_count += 44
                self._log(f"第{current_page}页未找到商品")

            # 请求间隔
            time.sleep(self.config.delay_between_requests)

        # 最终进度
        self._update_progress('100%', '搜索完成', success_count)

        self.items_collected = success_count
        self.items_failed = fail_count

        return {
            'success': success_count,
            'failed': fail_count,
            'products': all_products,
            'source': 'api',
            'logs': self.logs
        }

    def search_with_fallback(
        self,
        keyword: str,
        page: int = 1,
        max_pages: int = None
    ) -> Dict:
        """
        搜索商品（带降级策略）

        如果API失败，返回标记由调用方决定是否降级

        Args:
            keyword: 搜索关键词
            page: 起始页码
            max_pages: 最大采集页数

        Returns:
            搜索结果
        """
        result = self.search(keyword, page, max_pages)

        # 如果API获取失败，返回特殊标记
        if result['success'] == 0:
            result['fallback_needed'] = True

        return result

    def test_connection(self) -> Dict:
        """
        测试API连接

        Returns:
            测试结果
        """
        self._log("测试API连接...")

        try:
            # 尝试访问搜索页面
            params = self._build_search_params('高达模型', 1)
            response = self._make_request(self.SEARCH_API, params=params)

            if response and response.status_code == 200:
                data = self._parse_json_response(response)

                if data:
                    return {
                        'success': True,
                        'message': 'API连接正常',
                        'data': data
                    }

            return {
                'success': False,
                'message': 'API连接失败或无数据返回',
                'response_code': response.status_code if response else None
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'测试异常: {str(e)}'
            }
