"""
Scrapy middlewares for crawler module.
爬虫中间件：反爬虫机制实现
"""
import logging
import random
from typing import Iterator
from urllib.parse import urlparse

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware as ScrapyRetryMiddleware
from scrapy.exceptions import NotConfigured
from scrapy.http import Request, Response
from scrapy.utils.response import response_status_message
from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)

logger = logging.getLogger('crawler')


class TmallAntiSpiderMiddleware:
    """
    天猫反爬虫中间件

    功能：
    1. 随机 User-Agent
    2. 随机请求延迟
    3. 模拟真实浏览器行为
    4. 处理封禁和验证
    """

    def __init__(self, settings):
        self.settings = settings
        self.ua_list = settings.get('USER_AGENT_LIST', [])
        self.delay_min = settings.get('CRAWLER_DELAY_MIN', 1)
        self.delay_max = settings.get('CRAWLER_DELAY_MAX', 3)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request: Request, spider):
        """处理请求，添加反爬虫措施"""
        # 随机 User-Agent
        if self.ua_list:
            request.headers['User-Agent'] = random.choice(self.ua_list)

        # 添加其他模拟真实浏览器的请求头
        request.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        # 添加延迟标记
        if not request.meta.get('download_delay'):
            request.meta['download_delay'] = random.uniform(self.delay_min, self.delay_max)

        return None

    def process_response(self, request: Request, response: Response, spider):
        """处理响应，检测反爬虫"""
        # 检测是否被重定向到验证页面
        if 'verify' in response.url.lower() or 'captcha' in response.url.lower():
            logger.warning(f"检测到验证页面: {response.url}")
            # 可以在这里添加处理验证的逻辑，或更换代理

        # 检测 HTTP 状态码
        if response.status == 403:
            logger.warning(f"访问被禁止 (403): {request.url}")
        elif response.status == 429:
            logger.warning(f"请求过于频繁 (429): {request.url}")

        return response


class RetryMiddleware(ScrapyRetryMiddleware):
    """
    自定义重试中间件

    功能：
    1. 扩展 Scrapy 的重试机制
    2. 记录重试日志
    3. 支持代理切换
    """

    EXCEPTIONS_TO_RETRY = (
        defer.TimeoutError,
        TimeoutError,
        DNSLookupError,
        ConnectionRefusedError,
        ConnectionDone,
        ConnectError,
        ConnectionLost,
        TCPTimedOutError,
        # 添加更多异常类型
    )

    def __init__(self, settings):
        super().__init__(settings)
        self.retry_times = settings.getint('RETRY_TIMES', 3)
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))

    def process_response(self, request: Request, response: Response, spider):
        """处理响应，判断是否需要重试"""
        # 检查是否需要重试
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return response

    def process_exception(self, request: Request, exception: Exception, spider):
        """处理异常，判断是否需要重试"""
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self._retry(request, exception, spider)

        return None

    def _retry(self, request: Request, reason, spider):
        """执行重试逻辑"""
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.retry_times:
            logger.debug(f"重试请求 {retries}/{self.retry_times}: {request.url} - 原因: {reason}")

            # 创建重试请求
            retry_request = request.copy()
            retry_request.meta['retry_times'] = retries
            retry_request.priority = request.priority + 1

            # 可以在这里更换代理
            # retry_request.meta['proxy'] = self._get_next_proxy()

            return retry_request
        else:
            logger.error(f"重试次数已达上限: {request.url}")

        return None


class ProxyMiddleware:
    """
    代理中间件

    功能：
    1. 从代理池获取代理
    2. 检测代理可用性
    3. 自动切换失效代理
    """

    def __init__(self, settings):
        self.settings = settings
        self.proxy_list = []
        self.current_proxy_index = 0
        self.failed_proxies = set()

        # 初始化代理池
        self._init_proxy_pool()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _init_proxy_pool(self):
        """初始化代理池"""
        # 这里可以从环境变量或配置文件读取代理列表
        proxy_list_str = self.settings.get('PROXY_LIST', '')
        if proxy_list_str:
            if isinstance(proxy_list_str, str):
                self.proxy_list = [p.strip() for p in proxy_list_str.split(',') if p.strip()]
            else:
                self.proxy_list = list(proxy_list_str)

        logger.info(f"代理池初始化完成，共 {len(self.proxy_list)} 个代理")

    def _get_next_proxy(self) -> str:
        """获取下一个可用代理"""
        if not self.proxy_list:
            return None

        # 尝试获取未失效的代理
        for _ in range(len(self.proxy_list)):
            proxy = self.proxy_list[self.current_proxy_index]
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)

            if proxy not in self.failed_proxies:
                return proxy

        # 如果所有代理都失效了，重置失效列表
        logger.warning("所有代理都已失效，重置失效列表")
        self.failed_proxies.clear()
        return self.proxy_list[0] if self.proxy_list else None

    def process_request(self, request: Request, spider):
        """处理请求，添加代理"""
        proxy = self._get_next_proxy()

        if proxy:
            request.meta['proxy'] = proxy
            request.meta['proxy_index'] = self.current_proxy_index
            logger.debug(f"使用代理: {proxy}")

    def process_response(self, request: Request, response: Response, spider):
        """处理响应，检测代理是否失效"""
        proxy = request.meta.get('proxy')

        # 检测代理失效
        if proxy and response.status in [403, 407, 429]:
            logger.warning(f"代理可能失效: {proxy}, 状态码: {response.status}")
            self.failed_proxies.add(proxy)

        return response

    def process_exception(self, request: Request, exception: Exception, spider):
        """处理异常，检测代理是否失效"""
        proxy = request.meta.get('proxy')

        # 检测代理连接异常
        if proxy and isinstance(exception, (
            ConnectError,
            ConnectionRefusedError,
            TCPTimedOutError,
            TimeoutError
        )):
            logger.warning(f"代理连接失败: {proxy}, 异常: {exception}")
            self.failed_proxies.add(proxy)


class RandomDelayMiddleware:
    """
    随机延迟中间件

    功能：
    1. 为每个请求添加随机延迟
    2. 模拟人类操作间隔
    """

    def __init__(self, settings):
        self.delay_min = settings.getfloat('RANDOM_DELAY_MIN', 1.0)
        self.delay_max = settings.getfloat('RANDOM_DELAY_MAX', 3.0)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request: Request, spider):
        """处理请求，添加延迟元数据"""
        delay = random.uniform(self.delay_min, self.delay_max)
        request.meta['download_delay'] = delay

        return None
