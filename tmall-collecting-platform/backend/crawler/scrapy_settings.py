"""
Scrapy settings for crawler module.
Scrapy 爬虫框架配置
"""

import os

# Scrapy 项目配置
BOT_NAME = 'tmall_crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# 命令行工具配置
ROBOTSTXT_OBEY = False  # 不遵守 robots.txt（仅用于学习研究）

# 并发配置
CONCURRENT_REQUESTS = 16  # 并发请求数
DOWNLOAD_DELAY = random.uniform(1, 3)  # 随机延迟

# 自动限速扩展
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# 下载超时
DOWNLOAD_TIMEOUT = 30

# 重试配置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 中间件配置
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'crawler.middlewares.TmallAntiSpiderMiddleware': 543,
}

# pipelines配置
ITEM_PIPELINES = {
    'crawler.pipelines.DataCleaningPipeline': 100,
    'crawler.pipelines.BatchInsertPipeline': 300,
}

# User-Agent 池
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
]

# Playwright 配置
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,  # 无头模式
    'timeout': 30000,
}

PLAYWRIGHT_CONTEXTS = {
    'default': {
        'viewport': {'width': 1920, 'height': 1080},
        'user_agent': USER_AGENT_LIST[0],
    }
}

# 请求头
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.tmall.com/',
}

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(levelname)s %(asctime)s [%(name)s] %(message)s'

# 缓存配置（开发环境启用）
HTTPCACHE_ENABLED = False

# 代理配置（如果需要）
# PROXY_LIST = ['http://proxy1.example.com:8080', 'http://proxy2.example.com:8080']

# 限制采集深度
DEPTH_LIMIT = 1

# 禁用 Cookies（可选，某些场景下减少被识别风险）
COOKIES_ENABLED = True

# DNS 缓存
DNSCACHE_ENABLED = True
