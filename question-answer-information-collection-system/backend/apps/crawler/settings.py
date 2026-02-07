"""
Scrapy 设置文件

配置爬虫的各项参数，包括下载延迟、代理、重试、Playwright 等。
"""

# -*- coding: utf-8 -*-

# Scrapy settings for crawler project

BOT_NAME = 'crawler'

SPIDER_MODULES = ['apps.crawler.spiders']
NEWSPIDER_MODULE = 'apps.crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
DOWNLOAD_DELAY = 3
# randomize download delay between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = False

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 代理中间件
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # User-Agent 旋转
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'apps.crawler.pipelines.QuestionPipeline': 300,
    'apps.crawler.pipelines.DuplicateFilterPipeline': 100,
    'apps.crawler.pipelines.DataValidationPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The recommended number of concurrent requests Scrapy should be used against at each remote server
AUTOTHROTTLE_TARGET_CONCURRENTITY = 1.0
# Enable showing the overall HTTP code, which should be between 100 and 599
AUTOTHROTTLE_HTTP_CODE_RANGE = '200-599'

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware
# HTTPCACHE_ENABLED = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
FEED_EXPORT_ENCODING = 'utf-8'

# =============================================================================
# Playwright Settings
# =============================================================================

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Enable Playwright for JavaScript rendering
PLAYWRIGHT_ENABLED = True
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,
    'args': [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--window-size=1920,1080',
        '--start-maximized',
    ]
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000  # 60 seconds

# Playwright browser channels (for different browser versions)
# PLAYWRIGHT_BROWSER_CHANNEL = 'chrome'

# Page methods to execute on each request
PLAYWRIGHT_PAGE_METHODS = [
    # Wait for network idle before extracting data
    'page.wait_for_load_state("networkidle")',
]

# =============================================================================
# Proxy Settings
# =============================================================================

# Rotating proxies list (add your proxies here)
ROTATING_PROXY_LIST = [
    # 格式: protocol://ip:port 或 protocol://user:pass@ip:port
    # 示例（需要替换为真实的代理）:
    # 'http://127.0.0.1:7890',
    # 'socks5://127.0.0.1:1080',
]

# Proxy pool settings
PROXY_MODE = 'randomly_select_one_proxy'

# Ban detection settings
BAN_DETECTION = {
    'check_status': False,  # Check if response status is a ban
    'check_words': [  # Keywords that indicate a ban
        '访问频率过快',
        '请输入验证码',
        '系统繁忙',
        'Too Many Requests',
        '403 Forbidden',
    ],
    'ban_code': None,  # HTTP status code that indicates a ban
    'ban_url_regex': None,  # URL pattern that indicates a ban
}

# =============================================================================
# Captcha Handling (2Captcha Integration)
# =============================================================================

# 2Captcha API key (set in environment variables)
# 2CAPTCHA_API_KEY = os.environ.get('2CAPTCHA_API_KEY')

# Captcha types and their selectors
CAPTCHA_TYPES = {
    'geetest': {
        'site_key_selector': '[data-sitekey]',
        'page_url': 'https://wenda.so.com/',
    },
    'image': {
        'captcha_image_selector': '.captcha-image, #captcha-img',
    }
}

# Enable automatic captcha solving
CAPTCHA_SOLVING_ENABLED = False  # Set to True when API key is configured

# =============================================================================
# Retry Settings
# =============================================================================

RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
RETRY_PRIORITY_ADJUSTMENT = -2

# =============================================================================
# Logging Settings
# =============================================================================

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# Log to file (optional)
# LOG_FILE = 'logs/crawler.log'

# =============================================================================
# Memory and Performance Settings
# =============================================================================

# Maximum number of concurrent items per domain (default: 100)
# CONCURRENT_ITEMS = 100

# Disable Telnet console (for security)
TELNETCONSOLE_ENABLED = False

# Close spider after idle time (in seconds)
# CLOSESPIDER_IDLE = 3600

# Close spider after certain number of items
# CLOSESPIDER_ITEMCOUNT = 10000

# =============================================================================
# User-Agent List (for rotation)
# =============================================================================

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
]

# =============================================================================
# Django Integration Settings
# =============================================================================

# Django settings module for scrapy settings
DJANGO_SETTINGS_MODULE = 'qa_project.settings'

# Enable Django item export
FEED_EXPORTERS = {
    'json': 'scrapy.exporters.JsonItemExporter',
    'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
}

# Default output file
FEED_FORMAT = 'jsonlines'
FEED_URI = 'output.jsonlines'
