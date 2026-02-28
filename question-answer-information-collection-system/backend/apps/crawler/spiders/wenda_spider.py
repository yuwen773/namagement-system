"""
360问答爬虫 (混合模式)

基于 script\360q&a\crawler.py 的正确实现移植到 Scrapy 框架。
使用 HTML 解析方式，访问 /c/?pn={pn} 获取问答列表。
支持断点续传、Playwright 降级等反爬机制。
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
from scrapy.http import Request, Response, HtmlResponse
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod
from scrapy.exceptions import DropItem

from apps.crawler.items import QuestionItem
from apps.crawler.utils import DataCleaner

logger = logging.getLogger(__name__)


class WendaSpider(scrapy.Spider):
    """
    360问答爬虫

    基于 script\360q&a\crawler.py 的正确实现：
    - URL: https://wenda.so.com/c/?pn={pn}
    - 选择器: ul.question-list li
    - 支持降级到 Playwright 浏览器渲染模式
    """

    name = 'wenda_360'
    allowed_domains = ['wenda.so.com', '360.cn']

    # 基础 URL (与 crawler.py 一致)
    BASE_URL = "https://wenda.so.com"

    # 爬虫配置
    custom_settings = {
        'DOWNLOAD_DELAY': 2,          # 请求延迟（秒）- 与 crawler.py 的 delay 参数对应
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # 随机延迟
        'RETRY_TIMES': 3,             # 重试次数 - 与 crawler.py 的 max_retries 对应
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],  # 重试状态码
        'CONCURRENT_REQUESTS': 1,     # 并发请求数（避免封禁）
        'AUTOTHROTTLE_ENABLED': True, # 自动限速
        'AUTOTHROTTLE_START_DELAY': 2,
        'AUTOTHROTTLE_MAX_DELAY': 8,
        'AUTOTHROTTLE_TARGET_CONCURRENTITY': 1.0,
        'ROBOTSTXT_OBEY': False,      # 不遵守 robots.txt（测试用）
        'USER_AGENT_ROTATE': True,    # 开启 UA 旋转
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': True,
        },
    }

    # 默认请求头（从 crawler.py 移植）
    DEFAULT_HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://wenda.so.com/",
        "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Microsoft Edge";v="144"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    }

    def __init__(self, mode: str = 'demo', limit: int = 20, use_redis: bool = False, *args, **kwargs):
        """
        初始化爬虫

        Args:
            mode: 采集模式 ('demo' 或 'full')
            limit: 采集数量限制
            use_redis: 是否使用 Redis 进行断点续传 (默认 False)
        """
        super().__init__(*args, **kwargs)
        self.mode = mode
        # 确保参数类型正确（命令行传入的参数是字符串）
        if isinstance(limit, str):
            self.limit = int(limit)
        else:
            self.limit = limit

        # 确保 use_redis 参数类型正确
        if isinstance(use_redis, str):
            self.use_redis = use_redis.lower() in ('true', '1', 'yes', 'on')
        else:
            self.use_redis = use_redis

        # 演示模式限制
        self.demo_limit = 20

        # 状态追踪
        self.collected_count = 0
        self.failed_count = 0

        # 清洗工具
        self.cleaner = DataCleaner()

        # Redis 断点记录 key (仅当 use_redis=True 时使用)
        self.redis_key_prefix = 'crawler:wenda:'
        self.redis_enabled = self.use_redis

        logger.info(f"初始化爬虫: mode={mode}, limit={limit}, use_redis={self.use_redis}")

    def start_requests(self) -> Generator[Request, None, None]:
        """
        生成初始请求

        基于 crawler.py 的正确实现：
        - 第1页: https://wenda.so.com/c/
        - 第2页+: https://wenda.so.com/c/?pn={pn}
        """
        # 从 Redis 读取断点（如果启用）
        if self.redis_enabled:
            last_page = self._get_redis('last_page', 1)
            self.logger.info(f"断点续传: 起始页={last_page}")
        else:
            last_page = 1
            self.logger.info(f"从头开始爬取: 起始页={last_page}")

        # 构造第一页的 URL
        # 第1页: pn=0 -> /c/
        # 第2页: pn=1 -> /c/?pn=1
        yield self._create_page_request(last_page)

    def _create_page_request(self, page_num: int, use_playwright: bool = False,
                              retry_count: int = 0) -> Request:
        """
        创建页面请求

        Args:
            page_num: 页码 (1=第1页, 2=第2页, ...)
            use_playwright: 是否使用 Playwright 模式
            retry_count: 重试次数

        Returns:
            Request 对象
        """
        # pn 参数从 0 开始: pn=0 -> 第1页, pn=1 -> 第2页
        pn = page_num - 1
        if pn == 0:
            url = f"{self.BASE_URL}/c/"
        else:
            url = f"{self.BASE_URL}/c/?pn={pn}"

        self.logger.debug(f"创建请求: {url} (第{page_num}页)")

        if use_playwright:
            # Playwright 浏览器模式
            return Request(
                url=url,
                callback=self.parse_playwright_html,
                errback=self.handle_error,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_selector', 'ul.question-list li', timeout=15000),
                        PageMethod('wait_for_timeout', 1000),
                    ],
                    'page': page_num,
                    'retry_count': retry_count,
                },
                headers=self.DEFAULT_HEADERS.copy()
            )
        else:
            # 普通 HTTP 请求模式
            return Request(
                url=url,
                callback=self.parse_html,
                errback=self.handle_error,
                meta={
                    'page': page_num,
                    'retry_count': retry_count,
                },
                headers=self.DEFAULT_HEADERS.copy()
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
        # 如果未启用 Redis，直接返回默认值
        if not self.redis_enabled:
            return default

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
        # 如果未启用 Redis，直接返回
        if not self.redis_enabled:
            return

        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            r.set(f"{self.redis_key_prefix}{key}", str(value))
        except Exception as e:
            self.logger.warning(f"Redis 保存失败: {e}")

    def parse_html(self, response: Response) -> Generator[QuestionItem, None, None]:
        """
        HTML 解析器（与 crawler.py 逻辑一致）

        解析 https://wenda.so.com/c/ 页面的问答列表
        """
        page = response.meta.get('page', 1)
        self.logger.info(f"解析第 {page} 页: URL={response.url}, 状态={response.status}")

        # 检查 HTML 是否异常短（可能被反爬拦截）
        html_length = len(response.text)
        if html_length < 10000:
            self.logger.warning(f"HTML 异常短: {html_length} 字符，尝试 Playwright 模式")
            yield from self.fallback_to_playwright(response)
            return

        # 检查是否为空页
        if self._is_empty_page(response.text):
            self.logger.warning(f"第 {page} 页为空页，停止采集")
            return

        # 解析问题列表
        questions = self._parse_question_list(response.text, page)

        if not questions:
            self.logger.warning(f"第 {page} 页解析为 0 条问题，尝试 Playwright 模式")
            yield from self.fallback_to_playwright(response)
            return

        self.logger.info(f"第 {page} 页解析到 {len(questions)} 条问题")

        # 处理每条问答
        for q in questions:
            if self.mode == 'demo' and self.collected_count >= self.demo_limit:
                self.logger.info(f"演示模式已达到限制 {self.demo_limit} 条")
                break

            if self.collected_count >= self.limit:
                self.logger.info(f"已达到采集限制: {self.limit}")
                break

            item = self._build_question_item(q)
            if item:
                yield item
                self.collected_count += 1

        # 保存断点
        self._save_redis('last_page', page + 1)

        # 判断是否继续采集
        if self.mode == 'full' and self.collected_count < self.limit:
            next_page = page + 1
            yield self._create_page_request(next_page)

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

    def _is_empty_page(self, html: str) -> bool:
        """
        检查是否为空白页（无问题数据）

        与 crawler.py 中的 _is_empty_page 方法一致
        """
        # 检查 HTML 是否异常短
        MIN_HTML_LENGTH = 10000
        if len(html) < MIN_HTML_LENGTH:
            return True

        selector = Selector(text=html)

        # 方法1: 检查是否有问题列表
        question_items = selector.css('ul.question-list li')
        if question_items:
            return False

        # 方法2: 检查是否有任何 data-askid 的 li
        data_items = selector.css('li[data-askid]')
        if data_items:
            return False

        # 方法3: 检查是否有问题链接
        question_links = selector.css('a[href^="/q/"]')
        if question_links:
            return False

        # 方法4: 检查 pagination 元素是否存在
        pagination = selector.css('.pagination, #list-page')
        if pagination:
            return False

        # 方法5: 检查是否有 "已解决" 或问题库相关的文本
        page_text = selector.xpath('//body//text()').getall()
        page_text = ''.join(page_text)
        if '已解决' in page_text or '问题库' in page_text:
            return False

        # 如果以上都没有，判定为空页
        return True

    def _parse_question_list(self, html: str, page_num: int) -> list:
        """
        解析问题列表页面

        与 crawler.py 中的 parse_question_list 方法一致

        Args:
            html: HTML 内容
            page_num: 页码

        Returns:
            问题列表，每项包含: id, title, category, answer_count, time, location, pn
        """
        self.logger.debug(f"开始解析第 {page_num} 页问题列表")
        selector = Selector(text=html)
        questions = []

        # 查找问题列表
        question_items = selector.css("ul.question-list li")

        # 如果没找到，尝试备用选择器
        if not question_items:
            question_items = selector.css("li[data-askid]")

        if not question_items:
            self.logger.warning(f"第 {page_num} 页: 未找到问题列表项")
            return []

        for item in question_items:
            try:
                question = self._parse_question_item(item, page_num)
                if question:
                    questions.append(question)
            except Exception as e:
                self.logger.error(f"解析问题项失败: {e}", exc_info=True)
                continue

        self.logger.debug(f"第 {page_num} 页解析完成: {len(questions)} 条问题")
        return questions

    def _parse_question_item(self, item_selector, page_num: int = 1) -> Optional[dict]:
        """
        解析单个问题项

        与 crawler.py 中的 _parse_question_item 方法一致

        Args:
            item_selector: Scrapy Selector 对象
            page_num: 页码

        Returns:
            问题字典
        """
        # 提取问题 ID - 从 data-askid 属性获取
        qid = item_selector.css('::attr(data-askid)').get()

        # 备用: 从 href 中获取
        if not qid:
            href = item_selector.css('a[href^="/q/"]::attr(href)').get()
            if href:
                qid_match = re.search(r'/q/(\d+)', href)
                qid = qid_match.group(1) if qid_match else ''

        # 提取问题标题 - 查找有 target="_blank" 的链接
        title = item_selector.css('a[target="_blank"]::text').get()
        if not title:
            title = item_selector.css('a[href^="/q/"]::text').get()

        if title:
            title = title.strip()

        # 提取分类
        category = item_selector.css('a.js-question-cate::text').get()
        if category:
            category = category.strip()

        # 从 data-ans 属性获取回答数
        answer_count = 0
        data_ans = item_selector.css('::attr(data-ans)').get()
        if data_ans:
            try:
                answer_count = int(data_ans)
            except ValueError:
                pass

        # 从 div.fr 中提取回答个数、时间、地点
        info_text = item_selector.css('div.fr::text').getall()
        info_text = ''.join(info_text).strip()

        # 解析回答个数（备用方法）
        ans_match = re.search(r'(\d+)个回答', info_text)
        if ans_match and answer_count == 0:
            answer_count = int(ans_match.group(1))

        # 解析时间
        time_str = ''
        time_match = re.search(r'(\d{4}\.\d{2}\.\d{2})', info_text)
        if time_match:
            time_str = time_match.group(1)

        # 解析地点
        location = ''
        loc_match = re.search(r'·\s*(\S+)', info_text)
        if loc_match:
            location = loc_match.group(1).strip()

        return {
            'id': qid,
            'title': title,
            'category': category,
            'answer_count': answer_count,
            'time': time_str,
            'location': location,
            'pn': page_num,
        }

    def _build_question_item(self, q: dict) -> Optional[QuestionItem]:
        """
        构建 QuestionItem

        Args:
            q: 从 _parse_question_item 返回的问题字典

        Returns:
            QuestionItem 或 None
        """
        try:
            qid = q.get('id', '')
            title = q.get('title', '')

            # 必填字段验证
            if not qid or not title:
                self.logger.debug(f"数据缺失，跳过: id={qid}, title={title[:30] if title else None}")
                return None

            # 构造详情页 URL
            source_url = f"{self.BASE_URL}/q/{qid}"

            # 清洗标题
            title = self.cleaner.clean_html(title)
            title = self.cleaner.normalize_text(title)

            # 提取可选字段（与 items.py 中的字段名一致）
            category = q.get('category', '')
            answer_count = q.get('answer_count', 0)
            time_str = q.get('time', '')  # 格式: YYYY.MM.DD
            location = q.get('location', '')
            page_num = q.get('pn', 1)

            # 构建 Item（使用正确的字段名）
            item = QuestionItem()
            item['question_id'] = qid
            item['title'] = title
            item['source_url'] = source_url
            item['crawl_time'] = datetime.now().isoformat()

            # 可选字段
            if category:
                item['category'] = category
            if answer_count:
                item['answer_count'] = answer_count
            if time_str:
                item['publish_time'] = time_str
            if location:
                item['location'] = location
            if page_num:
                item['crawl_page'] = page_num

            # 答案列表（列表页暂无答案，设为空列表）
            item['answer_list'] = []

            return item

        except Exception as e:
            self.logger.error(f"构建 Item 失败: {e}")
            return None

    def fallback_to_playwright(self, response_or_failure) -> Generator[Request, None, None]:
        """
        降级到 Playwright 模式

        当 HTTP 请求失败时，切换到浏览器渲染模式
        """
        # 从 meta 获取或设置默认值
        meta = getattr(response_or_failure, 'meta', {}) or {}
        page = meta.get('page', 1)
        retry_count = meta.get('retry_count', 0)

        self.logger.warning(f"HTTP 模式失效，降级到 Playwright 模式 (第{page}页)")

        # 使用正确的 URL 构造 Playwright 请求
        yield self._create_page_request(page, use_playwright=True, retry_count=retry_count)

    def parse_playwright_html(self, response: HtmlResponse) -> Generator[QuestionItem, None, None]:
        """
        Playwright HTML 解析器

        使用浏览器渲染后解析，与 parse_html 逻辑一致
        """
        page = response.meta.get('page', 1)
        self.logger.info(f"Playwright 解析第 {page} 页: {response.url}")

        # 使用相同的解析逻辑
        html = response.text

        # 检查是否为空页
        if self._is_empty_page(html):
            self.logger.warning(f"第 {page} 页为空页（Playwright），停止采集")
            return

        # 解析问题列表
        questions = self._parse_question_list(html, page)

        if not questions:
            self.logger.warning(f"第 {page} 页 Playwright 解析为 0 条问题")
            return

        self.logger.info(f"第 {page} 页 Playwright 解析到 {len(questions)} 条问题")

        # 处理每条问答
        for q in questions:
            if self.mode == 'demo' and self.collected_count >= self.demo_limit:
                self.logger.info(f"演示模式已达到限制 {self.demo_limit} 条")
                break

            if self.collected_count >= self.limit:
                self.logger.info(f"已达到采集限制: {self.limit}")
                break

            item = self._build_question_item(q)
            if item:
                yield item
                self.collected_count += 1

        # 保存断点
        self._save_redis('last_page', page + 1)

        # 继续采集下一页
        if self.mode == 'full' and self.collected_count < self.limit:
            next_page = page + 1
            yield self._create_page_request(next_page, use_playwright=True)

    def _parse_question_element(self, q) -> Optional[QuestionItem]:
        """
        解析单个问答元素（已废弃，使用 _parse_question_item 代替）

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
        生成下一页请求（已废弃，使用 _create_page_request 代替）

        Args:
            page: 页码
            use_playwright: 是否使用 Playwright 模式
        """
        yield self._create_page_request(page, use_playwright=use_playwright)

    def handle_error(self, failure) -> Generator[Request, None, None]:
        """
        处理请求错误

        Args:
            failure: 错误对象
        """
        meta = failure.request.meta
        retry_count = meta.get('retry_count', 0)
        page = meta.get('page', 1)
        use_playwright = meta.get('playwright', False)

        self.logger.error(f"请求失败: {failure.value}, 重试次数: {retry_count}")

        if retry_count < 3:
            # 延迟后重试
            time.sleep(random.uniform(2, 5))
            # 失败后自动升级到 Playwright 模式
            yield self._create_page_request(page, use_playwright=True, retry_count=retry_count + 1)
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

        # 保存最终统计到 Redis（如果启用）
        if self.redis_enabled:
            stats = {
                'total': self.collected_count,
                'failed': self.failed_count,
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
