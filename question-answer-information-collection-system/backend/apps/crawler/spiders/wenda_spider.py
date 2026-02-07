"""
360问答爬虫 (混合模式)

优先使用 JSON API 模式，API 失效时自动降级为 Playwright 浏览器渲染模式。
支持断点续传、代理轮换、验证码处理等反爬机制。
"""

import json
import re
import time
import random
import logging
from datetime import datetime
from urllib.parse import urljoin, parse_qs, urlparse
from typing import Generator, Dict, Any, Optional

import scrapy
from scrapy.http import Request, Response, HtmlResponse, JsonRequest
from scrapy_playwright.page import PageMethod
from scrapy.exceptions import DropItem

from apps.crawler.items import QuestionItem
from apps.crawler.utils import DataCleaner

logger = logging.getLogger(__name__)


class WendaSpider(scrapy.Spider):
    """
    360问答爬虫

    混合模式：
    1. 优先模式 - httpx 调用隐藏 JSON API
    2. 降级模式 - Playwright 浏览器渲染
    """

    name = 'wenda_360'
    allowed_domains = ['wenda.so.com', '360.cn']
    start_urls = ['https://wenda.so.com/']

    # 爬虫配置
    custom_settings = {
        'DOWNLOAD_DELAY': 3,          # 请求延迟（秒）
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # 随机延迟
        'RETRY_TIMES': 5,             # 重试次数
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],  # 重试状态码
        'CONCURRENT_REQUESTS': 1,     # 并发请求数（避免封禁）
        'AUTOTHROTTLE_ENABLED': True, # 自动限速
        'AUTOTHROTTLE_START_DELAY': 3,
        'AUTOTHROTTLE_MAX_DELAY': 10,
        'AUTOTHROTTLE_TARGET_CONCURRENTITY': 1.0,
        'ROBOTSTXT_OBEY': True,       # 遵守 robots.txt
        'USER_AGENT_ROTATE': True,    # 开启 UA 旋转
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': True,
        },
    }

    def __init__(self, mode: str = 'demo', limit: int = 20, *args, **kwargs):
        """
        初始化爬虫

        Args:
            mode: 采集模式 ('demo' 或 'full')
            limit: 采集数量限制
        """
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.limit = limit

        # 演示模式限制
        self.demo_limit = 20

        # 状态追踪
        self.collected_count = 0
        self.failed_count = 0
        self.api_mode = True  # 优先使用 API 模式

        # 清洗工具
        self.cleaner = DataCleaner()

        # Redis 断点记录 key
        self.redis_key_prefix = 'crawler:wenda:'

        logger.info(f"初始化爬虫: mode={mode}, limit={limit}")

    def start_requests(self) -> Generator[Request, None, None]:
        """
        生成初始请求

        优先使用 JSON API，失败后降级为 Playwright
        """
        # 从 Redis 读取断点
        last_page = self._get_redis('last_page', 1)
        last_id = self._get_redis('last_id', '')

        self.logger.info(f"断点续传: page={last_page}, last_id={last_id}")

        # 构造搜索 URL（示例：搜索 Python 相关问题）
        base_url = 'https://wenda.so.com/search/list'

        params = {
            'q': 'python',  # 搜索关键词
            'pn': last_page,  # 页码
            'ps': 20,  # 每页数量
            'sort': 'time',  # 按时间排序
        }

        # 优先尝试 JSON API
        api_url = f"{base_url}?{self._encode_params(params)}"

        yield JsonRequest(
            url=api_url,
            callback=self.parse_api,
            errback=self.fallback_to_playwright,
            meta={
                'playwright': False,
                'page': last_page,
                'retry_count': 0,
            },
            headers={
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Referer': 'https://wenda.so.com/',
            }
        )

    def _encode_params(self, params: dict) -> str:
        """URL 参数编码"""
        parts = []
        for key, value in params.items():
            parts.append(f"{key}={value}")
        return '&'.join(parts)

    def _get_redis(self, key: str, default: Any = None) -> Any:
        """
        从 Redis 读取断点

        Args:
            key: 键名
            default: 默认值

        Returns:
            值或默认值
        """
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            value = r.get(f"{self.redis_key_prefix}{key}")
            return int(value) if value else default
        except Exception as e:
            self.logger.warning(f"Redis 连接失败: {e}")
            return default

    def _save_redis(self, key: str, value: Any) -> None:
        """保存断点到 Redis"""
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            r.set(f"{self.redis_key_prefix}{key}", str(value))
        except Exception as e:
            self.logger.warning(f"Redis 保存失败: {e}")

    def parse_api(self, response: Response) -> Generator[QuestionItem, None, None]:
        """
        JSON API 解析器

        处理 API 返回的 JSON 数据
        """
        self.logger.info(f"API 响应状态: {response.status}")

        # 检查响应状态
        if response.status != 200:
            self.logger.warning(f"API 返回非 200 状态: {response.status}")
            yield from self.fallback_to_playwright(response)
            return

        try:
            data = response.json()
            self.logger.info(f"API 返回数据结构: {type(data)}")

            # 解析数据 - 根据实际 API 结构调整
            questions = self._extract_from_api_response(data)

            if not questions:
                self.logger.warning("API 返回数据为空，尝试 Playwright 模式")
                yield from self.fallback_to_playwright(response)
                return

            # 处理每条问答
            for q in questions:
                if self.mode == 'demo' and self.collected_count >= self.demo_limit:
                    break

                if self.collected_count >= self.limit:
                    self.logger.info(f"达到采集限制: {self.limit}")
                    break

                item = self._build_question_item(q)
                if item:
                    yield item
                    self.collected_count += 1

            # 保存断点
            page = response.meta.get('page', 1)
            self._save_redis('last_page', page + 1)

            # 判断是否继续采集
            if self.mode == 'full' and self.collected_count < self.limit:
                # 构造下一页请求
                next_page = page + 1
                yield from self._get_next_page_request(next_page)

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 解析失败: {e}")
            yield from self.fallback_to_playwright(response)

    def _extract_from_api_response(self, data: dict) -> list:
        """
        从 API 响应中提取问答数据

        Args:
            data: API 返回的 JSON 数据

        Returns:
            问答数据列表
        """
        questions = []

        # 根据实际 API 结构调整解析逻辑
        # 这里需要根据抓包分析的 API 响应结构调整
        if isinstance(data, dict):
            # 常见结构
            if 'data' in data:
                items = data['data'].get('list', data['data'].get('result', []))
            elif 'result' in data:
                items = data['result'].get('data', data['result'].get('list', []))
            elif 'questions' in data:
                items = data['questions']
            else:
                items = data.get('list', [])

            for item in items:
                if isinstance(item, dict):
                    questions.append(item)

        elif isinstance(data, list):
            questions = data

        return questions

    def _build_question_item(self, q: dict) -> Optional[QuestionItem]:
        """
        构建 QuestionItem

        Args:
            q: 原始问答数据

        Returns:
            QuestionItem 或 None
        """
        try:
            # 提取字段 - 根据实际 API 结构调整字段名
            title = q.get('title') or q.get('question_title', '')
            answer_content = q.get('answer') or q.get('answer_content', q.get('answer_text', ''))
            source_url = q.get('url') or q.get('source_url', q.get('link', ''))

            # 必填字段验证
            if not title or not answer_content or not source_url:
                self.logger.debug(f"数据缺失，跳过: title={title[:30] if title else None}")
                return None

            # 清洗数据
            title = self.cleaner.clean_html(title)
            title = self.cleaner.normalize_text(title)

            answer_content = self.cleaner.clean_html(answer_content)
            answer_content = self.cleaner.normalize_text(answer_content)

            # 提取可选字段
            description = q.get('description') or q.get('question_desc', '')
            if description:
                description = self.cleaner.clean_html(description)
                description = self.cleaner.normalize_text(description)

            answerer = q.get('answerer') or q.get('answer_user', '')
            answer_time = q.get('answer_time') or q.get('answer_date', '')

            # 处理标签
            tags = q.get('tags', [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(',') if t.strip()]

            # 构建 Item
            item = QuestionItem(
                title=title,
                answer_content=answer_content,
                source_url=source_url,
                description=description or None,
                answerer=answerer or None,
                answer_time=answer_time or None,
                tags=tags,
                crawl_time=datetime.now().isoformat()
            )

            return item

        except Exception as e:
            self.logger.error(f"构建 Item 失败: {e}")
            return None

    def fallback_to_playwright(self, response_or_failure) -> Generator[Request, None, None]:
        """
        降级到 Playwright 模式

        当 API 失效、被封禁或返回异常时，切换到浏览器渲染模式
        """
        if self.api_mode:
            self.logger.warning("API 模式失效，降级到 Playwright 模式")
            self.api_mode = False

        # 从 meta 获取或设置默认值
        meta = getattr(response_or_failure, 'meta', {}) or {}
        page = meta.get('page', 1)
        retry_count = meta.get('retry_count', 0)

        # 构造搜索 URL
        search_url = f'https://wenda.so.com/search/list?q=python&pn={page}'

        yield Request(
            url=search_url,
            callback=self.parse_playwright,
            errback=self.handle_error,
            meta={
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_selector', '.question-list, .result-list', timeout=15000),
                    PageMethod('wait_for_timeout', 2000),  # 等待懒加载
                    PageMethod('evaluate', 'window.scrollTo(0, document.body.scrollHeight / 2)'),  # 滚动加载
                    PageMethod('wait_for_timeout', 1000),
                ],
                'page': page,
                'retry_count': retry_count + 1,
            },
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        )

    def parse_playwright(self, response: HtmlResponse) -> Generator[QuestionItem, None, None]:
        """
        Playwright HTML 解析器

        处理浏览器渲染后的 HTML 页面
        """
        page = response.meta.get('page', 1)
        self.logger.info(f"Playwright 解析页面: {response.url}")

        # 提取问答列表 - 根据实际页面结构调整选择器
        # 360问答可能的 CSS 选择器
        selectors = [
            '.question-item',
            '.result-item',
            '.wenda-item',
            '.js-wenda-item',
            '.question-list li',
            '.search-result li',
        ]

        questions = []
        for selector in selectors:
            questions = response.css(selector)
            if questions:
                self.logger.info(f"使用选择器: {selector}, 找到 {len(questions)} 条")
                break

        if not questions:
            self.logger.warning(f"页面未找到问答内容: {response.url}")
            # 可能是验证码页面
            if 'captcha' in response.url or '验证码' in response.text:
                self.logger.error("检测到验证码页面，需要人工处理")
                # 这里可以触发 2Captcha API 调用
            return

        for q in questions:
            if self.mode == 'demo' and self.collected_count >= self.demo_limit:
                break

            if self.collected_count >= self.limit:
                break

            item = self._parse_question_element(q)
            if item:
                yield item
                self.collected_count += 1

        # 保存断点
        self._save_redis('last_page', page + 1)

        # 继续采集下一页
        if self.mode == 'full' and self.collected_count < self.limit:
            yield from self._get_next_page_request(page + 1, use_playwright=True)

    def _parse_question_element(self, q) -> Optional[QuestionItem]:
        """
        解析单个问答元素

        Args:
            q: scrapy Selector 对象

        Returns:
            QuestionItem 或 None
        """
        try:
            # 提取标题和链接
            title_elem = q.css('.title a::text, .question-title a::text, h3 a::text').get()
            if not title_elem:
                title_elem = q.css('.title::text, .question-title::text').get()

            link_elem = q.css('.title a::attr(href), .question-title a::attr(href), h3 a::attr(href)').get()

            if not title_elem or not link_elem:
                return None

            title = self.cleaner.normalize_text(title_elem.strip())
            source_url = urljoin('https://wenda.so.com/', link_elem.strip())

            # 提取描述/摘要
            description = q.css('.desc::text, .summary::text, .description::text').get()
            if description:
                description = self.cleaner.normalize_text(description.strip())

            # 提取回答内容
            answer = q.css('.answer::text, .answer-content::text, .best-answer::text').get()
            if answer:
                answer = self.cleaner.normalize_text(answer.strip())
            else:
                answer = ''  # 回答可能为空

            # 提取回答者
            answerer = q.css('.answerer::text, .answer-user::text').get()
            if answerer:
                answerer = self.cleaner.normalize_text(answerer.strip())

            # 提取回答时间
            answer_time = q.css('.answer-time::text, .time::text').get()
            if answer_time:
                answer_time = answer_time.strip()

            # 提取标签
            tags = q.css('.tag::text, .tags span::text').getall()
            tags = [self.cleaner.normalize_text(t.strip()) for t in tags if t.strip()]

            # 构建 Item
            item = QuestionItem(
                title=title,
                answer_content=answer or '',
                source_url=source_url,
                description=description or None,
                answerer=answerer or None,
                answer_time=answer_time or None,
                tags=tags,
                crawl_time=datetime.now().isoformat()
            )

            return item

        except Exception as e:
            self.logger.error(f"解析问答元素失败: {e}")
            return None

    def _get_next_page_request(self, page: int, use_playwright: bool = False) -> Generator[Request, None, None]:
        """
        生成下一页请求

        Args:
            page: 页码
            use_playwright: 是否使用 Playwright 模式
        """
        if self.mode == 'demo' and self.collected_count >= self.demo_limit:
            return

        if self.collected_count >= self.limit:
            return

        if use_playwright or not self.api_mode:
            url = f'https://wenda.so.com/search/list?q=python&pn={page}'
            yield Request(
                url=url,
                callback=self.parse_playwright,
                errback=self.handle_error,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_selector', '.question-list, .result-list', timeout=15000),
                        PageMethod('wait_for_timeout', 2000),
                        PageMethod('evaluate', 'window.scrollTo(0, document.body.scrollHeight / 2)'),
                        PageMethod('wait_for_timeout', 1000),
                    ],
                    'page': page,
                }
            )
        else:
            params = {
                'q': 'python',
                'pn': page,
                'ps': 20,
                'sort': 'time',
            }
            api_url = f"https://wenda.so.com/search/list?{self._encode_params(params)}"
            yield JsonRequest(
                url=api_url,
                callback=self.parse_api,
                errback=self.fallback_to_playwright,
                meta={
                    'playwright': False,
                    'page': page,
                },
                headers={
                    'Accept': 'application/json, text/plain, */*',
                }
            )

    def handle_error(self, failure) -> Generator[Request, None, None]:
        """
        处理请求错误

        Args:
            failure: 错误对象
        """
        meta = failure.request.meta
        retry_count = meta.get('retry_count', 0)
        page = meta.get('page', 1)

        self.logger.error(f"请求失败: {failure.value}, 重试次数: {retry_count}")

        if retry_count < 5:
            # 延迟后重试
            time.sleep(random.uniform(5, 10))
            yield from self._get_next_page_request(page, use_playwright=True)
        else:
            self.failed_count += 1
            self.logger.error(f"重试次数耗尽，跳过页面: {page}")

    def closed(self, reason: str) -> None:
        """
        爬虫关闭时调用

        Args:
            reason: 关闭原因
        """
        self.logger.info(
            f"爬虫关闭: reason={reason}, "
            f"采集={self.collected_count}, "
            f"失败={self.failed_count}"
        )

        # 保存最终统计
        stats = {
            'total': self.collected_count,
            'failed': self.failed_count,
            'mode': 'api' if self.api_mode else 'playwright',
            'closed_reason': reason,
            'finish_time': datetime.now().isoformat()
        }

        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            # 兼容旧版 Redis/redis-py
            for k, v in stats.items():
                r.hset(f"{self.redis_key_prefix}stats", k, str(v))
        except Exception as e:
            self.logger.warning(f"保存统计失败: {e}")
