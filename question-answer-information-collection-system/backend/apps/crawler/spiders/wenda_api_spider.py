"""
360问答爬虫 - 纯 API 模式

无需 Playwright，使用 httpx 直接调用 JSON API。
适合在 Playwright 安装失败时使用。

使用方法：
    scrapy crawl wenda_api -o output.json
    python crawl.py --mode demo --api-only
"""

import json
import logging
from datetime import datetime
from typing import Generator, Dict, Any, Optional
from urllib.parse import urljoin

import scrapy
from scrapy.http import Request, Response

from apps.crawler.items import QuestionItem
from apps.crawler.utils import DataCleaner

logger = logging.getLogger(__name__)


class WendaAPISpider(scrapy.Spider):
    """
    360问答爬虫 - 纯 API 模式

    使用 httpx 直接请求 API，无需浏览器渲染。
    效率高，速度快，适合大规模采集。
    """

    name = 'wenda_api'
    allowed_domains = ['wenda.so.com', '360.cn']

    # 爬虫配置
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 429],
        'CONCURRENT_REQUESTS': 2,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 2,
        'AUTOTHROTTLE_MAX_DELAY': 8,
        'ROBOTSTXT_OBEY': True,
        'FEEDS': {
            'output.jsonlines': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'overwrite': True,
            },
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
        self.demo_limit = 20
        self.collected_count = 0
        self.failed_count = 0
        self.cleaner = DataCleaner()
        self.logger.info(f"初始化纯 API 爬虫: mode={mode}, limit={limit}")

    def start_requests(self) -> Generator[Request, None, None]:
        """
        生成初始请求
        """
        last_page = 1
        api_url = f'https://wenda.so.com/api/search/list?pn={last_page}&ps=20&q=python'

        yield Request(
            url=api_url,
            callback=self.parse_api,
            errback=self.handle_error,
            meta={
                'page': last_page,
                'retry_count': 0,
            },
            headers={
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Referer': 'https://wenda.so.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            }
        )

    def parse_api(self, response: Response) -> Generator[QuestionItem, None, None]:
        """
        解析 API 响应
        """
        page = response.meta.get('page', 1)
        self.logger.info(f"API 响应: status={response.status}, url={response.url}")

        if response.status != 200:
            self.logger.warning(f"API 返回非 200 状态: {response.status}")
            yield from self.handle_error(response)
            return

        try:
            data = response.json()
            questions = self._extract_questions(data)

            if not questions:
                self.logger.warning(f"未提取到问答数据 page={page}")
                return

            for q in questions:
                if self.mode == 'demo' and self.collected_count >= self.demo_limit:
                    break
                if self.collected_count >= self.limit:
                    break

                item = self._build_item(q)
                if item:
                    yield item
                    self.collected_count += 1

            # 继续采集下一页
            if self.mode == 'full' and self.collected_count < self.limit:
                next_page = page + 1
                yield from self._get_next_page(next_page)

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 解析失败: {e}")
            self.logger.error(f"响应内容: {response.text[:500]}")

    def _extract_questions(self, data: dict) -> list:
        """从 API 响应中提取问答列表"""
        questions = []

        # 尝试多种可能的响应结构
        if isinstance(data, dict):
            if 'data' in data:
                items = data['data'].get('list', data['data'].get('result', []))
            elif 'result' in data:
                items = data['result'].get('data', data['result'].get('list', []))
            elif 'questions' in data:
                items = data['questions']
            else:
                items = data.get('list', data.get('items', []))

            for item in items:
                if isinstance(item, dict):
                    questions.append(item)

        elif isinstance(data, list):
            questions = data

        return questions

    def _build_item(self, q: dict) -> Optional[QuestionItem]:
        """构建 QuestionItem"""
        try:
            # 提取字段
            title = q.get('title') or q.get('question_title', '')
            answer_content = q.get('answer') or q.get('answer_content', q.get('answer_text', ''))
            source_url = q.get('url') or q.get('source_url', q.get('link', ''))

            if not title or not source_url:
                return None

            # 清洗数据
            title = self.cleaner.normalize_text(title.strip())
            answer_content = self.cleaner.normalize_text(answer_content.strip()) if answer_content else ''

            # 可选字段
            description = q.get('description') or q.get('question_desc', '')
            if description:
                description = self.cleaner.normalize_text(description.strip())

            answerer = q.get('answerer') or q.get('answer_user', '')
            answer_time = q.get('answer_time') or q.get('answer_date', '')

            # 标签
            tags = q.get('tags', [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(',') if t.strip()]

            return QuestionItem(
                title=title,
                answer_content=answer_content or '',
                source_url=source_url,
                description=description or None,
                answerer=answerer or None,
                answer_time=answer_time or None,
                tags=tags,
                crawl_time=datetime.now().isoformat()
            )

        except Exception as e:
            self.logger.error(f"构建 Item 失败: {e}")
            return None

    def _get_next_page(self, page: int) -> Generator[Request, None, None]:
        """生成下一页请求"""
        if self.mode == 'demo' and self.collected_count >= self.demo_limit:
            return
        if self.collected_count >= self.limit:
            return

        api_url = f'https://wenda.so.com/api/search/list?pn={page}&ps=20&q=python'

        yield Request(
            url=api_url,
            callback=self.parse_api,
            errback=self.handle_error,
            meta={
                'page': page,
                'retry_count': 0,
            },
            headers={
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://wenda.so.com/',
            }
        )

    def handle_error(self, failure) -> Generator[Request, None, None]:
        """处理请求错误"""
        meta = failure.request.meta
        page = meta.get('page', 1)
        retry_count = meta.get('retry_count', 0)

        self.logger.error(f"请求失败: {failure.value}, 重试次数: {retry_count}")

        if retry_count < 3:
            yield from self._get_next_page(page)
        else:
            self.failed_count += 1

    def closed(self, reason: str) -> None:
        """爬虫关闭"""
        self.logger.info(f"爬虫关闭: reason={reason}, 采集={self.collected_count}, 失败={self.failed_count}")
