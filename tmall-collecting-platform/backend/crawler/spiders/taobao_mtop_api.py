"""
淘宝 mtop API 爬虫实现
基于 docs/reference/crawler.py 的参考实现，集成到系统中

API特点：
1. 使用 mtop.relationrecommend.wirelessrecommend.recommend 接口
2. 支持 JSONP 响应解析
3. 完整的签名机制（MD5）
4. 多页数据采集支持
"""
import hashlib
import json
import logging
import random
import time
from typing import Dict, List, Optional, Callable
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import SpiderConfig
from ..proxy import ProxyManager

logger = logging.getLogger('crawler')


class TaobaoMtopAPI:
    """
    淘宝 mtop API 爬虫

    基于参考实现，集成到当前系统中

    特性：
    1. 完整的签名算法实现
    2. Cookie token 自动提取
    3. 多页数据采集
    4. 自动参数更新（bcoffset, ntoffset等）
    """

    # API 配置
    BASE_URL = "https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/"
    APP_KEY = "12574478"

    # 默认请求头
    DEFAULT_HEADERS = {
        'referer': 'https://new-s.taobao.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

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
            progress_callback: 进度回调函数
            cookie: Cookie 字符串（从浏览器获取）
        """
        self.config = config or SpiderConfig()
        self.proxy_manager = proxy_manager
        self.progress_callback = progress_callback

        # 创建 session
        self.session = requests.Session()
        self._setup_session()

        # 设置 Cookie
        self.cookie = cookie or ''
        if self.cookie:
            self.session.headers.update({'Cookie': self.cookie})
            logger.info("已设置自定义Cookie")

        # token 缓存
        self._token = None

        # 统计
        self.items_collected = 0
        self.items_failed = 0
        self.logs: List[str] = []

    def _setup_session(self):
        """配置 session"""
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
        logger.info(f"[TaobaoMtopAPI] {message}")

    def _update_progress(self, progress: str, stage: str, items: int = None):
        """更新进度"""
        if self.progress_callback:
            try:
                self.progress_callback(
                    progress,
                    stage,
                    items or self.items_collected,
                    self.logs[-5:]
                )
            except Exception as e:
                logger.warning(f"进度更新失败: {e}")

    def _extract_token(self) -> str:
        """
        从 Cookie 中提取 _m_h5_tk token

        Token 格式: xxx_xxx，取下划线前的部分

        Returns:
            token 字符串
        """
        if self._token:
            return self._token

        if not self.cookie:
            # 使用默认 token
            self._token = "7707921f826e40e21ed8d016e79ad351"
            logger.info("使用默认 token")
            return self._token

        # 从 Cookie 中提取
        for item in self.cookie.split(';'):
            item = item.strip()
            if item.startswith('_m_h5_tk='):
                token_value = item.split('=')[1]
                self._token = token_value.split('_')[0]
                logger.info(f"从 Cookie 提取到 token: {self._token[:8]}...")
                return self._token

        # 未找到，使用默认值
        logger.warning("未能从 Cookie 中提取 token，使用默认值")
        self._token = "7707921f826e40e21ed8d016e79ad351"
        return self._token

    def _calculate_sign(self, data: str, timestamp: str) -> str:
        """
        计算 mtop API 签名

        签名算法: md5(token + "&" + timestamp + "&" + appKey + "&" + data)

        Args:
            data: 请求参数中的 data 字段（已 JSON 序列化）
            timestamp: 时间戳字符串

        Returns:
            32位 MD5 签名字符串
        """
        token = self._extract_token()
        sign_str = token + "&" + timestamp + "&" + self.APP_KEY + "&" + data
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    def _parse_jsonp_response(self, response_text: str) -> Optional[Dict]:
        """
        解析 JSONP 响应

        Args:
            response_text: JSONP 格式的响应文本，如 "mtopjsonp6({...})"

        Returns:
            解析后的数据字典，失败返回 None
        """
        try:
            # 移除 JSONP 回调函数名
            if 'mtopjsonp' in response_text:
                start = response_text.find('(')
                end = response_text.rfind(')')
                if start != -1 and end != -1:
                    json_str = response_text[start + 1:end]
                    return json.loads(json_str)
            return json.loads(response_text)
        except (json.JSONDecodeError, ValueError) as e:
            self._log(f"JSONP 解析失败: {e}")
            return None

    def _get_proxy(self) -> Optional[Dict]:
        """获取代理配置"""
        if not self.proxy_manager:
            return None

        proxy = self.proxy_manager.get_proxy()
        if proxy:
            return {'http': proxy.url, 'https': proxy.url}
        return None

    def _build_search_params(
        self,
        keyword: str,
        page: int = 1,
        total_results: str = "4800",
        bcoffset: str = "",
        ntoffset: str = "",
        source_s: str = "0"
    ) -> Dict:
        """
        构建搜索参数

        Args:
            keyword: 搜索关键词
            page: 页码
            total_results: 总结果数
            bcoffset: BC偏移量
            ntoffset: NT偏移量
            source_s: 来源标识

        Returns:
            查询参数字典
        """
        timestamp = str(int(time.time() * 1000))

        # 搜索参数
        search_params = {
            "device": "HMA-AL00",
            "from": "nt_history",
            "index": "4",
            "isBeta": "false",
            "m": "pc",
            "n": 48,
            "page": page,
            "pageSize": 48,
            "q": keyword,
            "sort": "_coefp",
            "style": "list",
            "tab": "all",
            "totalPage": 100,
            "totalResults": total_results,
            "bcoffset": bcoffset,
            "ntoffset": ntoffset,
            "sourceS": source_s,
        }

        # 构建 data 参数
        data_param = json.dumps({
            "appId": "34385",
            "params": json.dumps(search_params, ensure_ascii=False)
        }, separators=(',', ':'))

        # 计算签名
        sign = self._calculate_sign(data_param, timestamp)

        return {
            'jsv': '2.7.4',
            'appKey': self.APP_KEY,
            't': timestamp,
            'sign': sign,
            'api': 'mtop.relationrecommend.wirelessrecommend.recommend',
            'v': '2.0',
            'timeout': '10000',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'callback': 'mtopjsonp6',
            'data': data_param,
        }

    def _clean_html(self, text: str) -> str:
        """移除 HTML 标签"""
        if not text:
            return ""
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def _extract_item_data(self, item: Dict) -> Optional[Dict]:
        """
        从单个商品数据中提取关键字段

        Args:
            item: 商品数据字典

        Returns:
            标准化后的商品数据
        """
        try:
            # 基本信息
            item_id = item.get('item_id', '')
            title = self._clean_html(item.get('title', ''))

            # 价格信息
            price = item.get('price', '')
            price_show = item.get('priceShow', {})
            price_unit = price_show.get('unit', '') if price_show else ''
            price_desc = price_show.get('priceDesc', '') if price_show else ''

            # 销量和地区
            real_sales = item.get('realSales', '')
            procity = item.get('procity', '')

            # 图片和链接
            pic_path = item.get('pic_path', '')
            auction_url = item.get('auctionURL', '')

            # 店铺信息
            shop_info = item.get('shopInfo', {})
            shop_title = shop_info.get('title', '') if isinstance(shop_info, dict) else ''
            shop_tag = item.get('shopTag', '')

            # 标签
            icons = item.get('icons', [])
            icon_tags = []
            for icon in icons:
                text = icon.get('text', '') if isinstance(icon, dict) else ''
                if text:
                    icon_tags.append(text)
            tags = ', '.join(icon_tags)

            # 商品属性
            structured_usp = item.get('structuredUSPInfo', [])
            usp_list = []
            for usp in structured_usp:
                if isinstance(usp, dict):
                    prop_name = usp.get('propertyName', '')
                    prop_value = usp.get('propertyValueName', '')
                    if prop_name and prop_value:
                        usp_list.append(f"{prop_name}:{prop_value}")
            properties = ' | '.join(usp_list)

            # 验证必填字段
            if not title and not price:
                return None

            return {
                'product_id': item_id,
                'title': title or '未知商品',
                'price': str(price),
                'price_unit': price_unit,
                'price_desc': price_desc,
                'seller_nick': item.get('nick', ''),
                'shop': shop_title or item.get('nick', ''),
                'shop_tags': shop_tag,
                'sales': str(real_sales),
                'region': procity,
                'tags': tags,
                'product_attributes': properties,
                'image_url': pic_path,
                'detail_url': auction_url,
                'brand': '',  # API 不直接提供品牌信息
                'category': '',  # API 不直接提供类目信息
            }

        except Exception as e:
            self._log(f"提取商品数据失败: {e}")
            return None

    def fetch_page(
        self,
        keyword: str,
        page: int = 1,
        total_results: str = "4800",
        bcoffset: str = "",
        ntoffset: str = "",
        source_s: str = "0"
    ) -> Optional[Dict]:
        """
        获取单页数据

        Args:
            keyword: 搜索关键词
            page: 页码
            total_results: 总结果数
            bcoffset: BC偏移量
            ntoffset: NT偏移量
            source_s: 来源标识

        Returns:
            响应数据字典，失败时返回None
        """
        try:
            params = self._build_search_params(
                keyword, page, total_results, bcoffset, ntoffset, source_s
            )

            proxies = self._get_proxy()

            response = self.session.get(
                self.BASE_URL,
                params=params,
                proxies=proxies,
                timeout=30
            )
            response.raise_for_status()

            # 解析 JSONP 响应
            data = self._parse_jsonp_response(response.text)
            return data

        except requests.exceptions.RequestException as e:
            self._log(f"请求失败: {e}")
            return None
        except Exception as e:
            self._log(f"获取页面失败: {e}")
            return None

    def search(
        self,
        keyword: str,
        max_pages: int = 3
    ) -> Dict:
        """
        搜索商品（多页）

        Args:
            keyword: 搜索关键词
            max_pages: 最大页数

        Returns:
            搜索结果
        """
        all_products = []
        success_count = 0
        fail_count = 0

        total_results = "4800"
        bcoffset = ""
        ntoffset = ""
        source_s = "0"

        self._log(f"开始搜索: {keyword}, 页数: {max_pages}")

        for page in range(1, max_pages + 1):
            # 更新进度
            progress = f"{int((page / max_pages) * 100)}%"
            self._update_progress(progress, f'搜索 {keyword} 第{page}页', success_count)

            # 获取当前页数据
            result = self.fetch_page(
                keyword=keyword,
                page=page,
                total_results=total_results,
                bcoffset=bcoffset,
                ntoffset=ntoffset,
                source_s=source_s
            )

            if not result:
                fail_count += 48
                self._log(f"第 {page} 页获取失败")
                break

            # 检查响应状态
            ret = result.get('ret', [])
            if ret and 'FAIL' in str(ret[0]):
                fail_count += 48
                self._log(f"第 {page} 页 API 返回错误: {ret[0]}")
                break

            # 从 mainInfo 中提取下一页需要的参数
            main_info = result.get('data', {}).get('mainInfo', {})
            if main_info:
                total_results = main_info.get('totalResults', total_results)
                bcoffset = main_info.get('bcoffset', bcoffset)
                ntoffset = main_info.get('ntoffset', ntoffset)
                source_s = main_info.get('sourceS', source_s)

            # 提取商品数据
            items_array = result.get('data', {}).get('itemsArray', [])
            if not items_array:
                self._log(f"第 {page} 页没有商品数据")
                break

            # 标准化商品数据
            for item in items_array:
                product = self._extract_item_data(item)
                if product:
                    all_products.append(product)
                    success_count += 1

            self._log(f"第 {page} 页获取到 {len(items_array)} 个商品，累计 {success_count} 个")

            # 请求间隔
            if page < max_pages:
                delay = random.uniform(1.5, 3.0)
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
            'source': 'taobao_mtop_api',
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
            result = self.fetch_page(keyword, page=1)

            if not result:
                return {
                    'success': False,
                    'message': '请求失败，请检查网络连接和Cookie'
                }

            # 检查响应状态
            ret = result.get('ret', [])
            if ret and 'FAIL' in str(ret[0]):
                return {
                    'success': False,
                    'message': f'API 返回错误: {ret[0]}'
                }

            items_array = result.get('data', {}).get('itemsArray', [])

            return {
                'success': True,
                'message': f'连接正常，获取到 {len(items_array)} 个商品',
                'sample_products': items_array[:2] if items_array else []
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'测试异常: {str(e)}'
            }

    def __del__(self):
        """析构函数"""
        try:
            if hasattr(self, 'session'):
                self.session.close()
        except Exception:
            pass
