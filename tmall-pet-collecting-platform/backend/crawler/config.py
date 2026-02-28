"""
爬虫配置模块
统一管理爬虫的所有配置参数
"""
import os
from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SpiderConfig:
    """
    爬虫配置类

    包含所有爬虫运行所需的配置参数
    """
    # ===== 基础配置 =====
    name: str = "pet_tmall_spider"  # 爬虫名称
    log_level: str = "INFO"  # 日志级别

    # ===== 采集配置 =====
    demo_mode: bool = False  # 演示模式
    max_pages: int = 2  # 最大采集页数
    items_per_page: int = 20  # 每页商品数量

    # ===== 关键词配置 =====
    default_keywords: List[str] = field(default_factory=lambda: [
        '猫粮',
        '狗粮',
        '猫砂',
        '宠物零食',
        '宠物玩具',
        '宠物用品',
        '宠物窝',
        '宠物牵引绳',
        '宠物笼子',
        '宠物食具',
        '宠物自动饮水机',
        '宠物爬架',
        '猫爬架'
    ])

    # ===== 请求配置 =====
    request_timeout: int = 30  # 请求超时时间(秒)
    retry_times: int = 3  # 重试次数
    retry_delay: int = 5  # 重试间隔(秒)
    delay_between_requests: float = 1.0  # 请求间延迟(秒)

    # ===== 代理配置 =====
    use_proxy: bool = False  # 是否使用代理
    proxy_list: List[Dict] = field(default_factory=list)  # 代理列表
    proxy_api: str = ""  # 代理API地址

    # ===== Playwright配置 =====
    headless: bool = True  # 无头模式
    browser_type: str = "chromium"  # 浏览器类型
    viewport_width: int = 1920  # 视口宽度
    viewport_height: int = 1080  # 视口高度

    # ===== 数据配置 =====
    batch_size: int = 100  # 批量保存大小
    duplicate_check: bool = True  # 是否检查重复

    # ===== API配置 =====
    tmall_api_base: str = "https://s.taobao.com/search"
    tmall_pc_url: str = "https://s.taobao.com/search?q="

    def get_page_url(self, keyword: str, page: int = 1) -> str:
        """
        获取搜索结果页面URL

        Args:
            keyword: 搜索关键词
            page: 页码

        Returns:
            str: 完整的搜索URL
        """
        # 淘宝/天猫搜索URL格式
        base_url = self.tmall_pc_url
        params = {
            'q': keyword,
            's': (page - 1) * 44  # 淘宝每页44个商品
        }

        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f"{base_url}{query_string}"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'demo_mode': self.demo_mode,
            'max_pages': self.max_pages,
            'default_keywords': self.default_keywords,
            'request_timeout': self.request_timeout,
            'retry_times': self.retry_times,
            'use_proxy': self.use_proxy,
            'headless': self.headless,
            'batch_size': self.batch_size,
        }


def load_config_from_env() -> SpiderConfig:
    """
    从环境变量加载配置

    支持的环境变量：
    - CRAWLER_DEMO_MODE: 演示模式
    - CRAWLER_MAX_PAGES: 最大页数
    - CRAWLER_USE_PROXY: 使用代理
    - CRAWLER_HEADLESS: 无头模式
    - CRAWLER_REQUEST_TIMEOUT: 请求超时
    """
    config = SpiderConfig()

    # 演示模式
    if os.environ.get('CRAWLER_DEMO_MODE', '').lower() == 'true':
        config.demo_mode = True

    # 最大页数
    max_pages = os.environ.get('CRAWLER_MAX_PAGES')
    if max_pages:
        try:
            config.max_pages = int(max_pages)
        except ValueError:
            pass

    # 使用代理
    use_proxy = os.environ.get('CRAWLER_USE_PROXY', '').lower()
    if use_proxy == 'true':
        config.use_proxy = True

    # 无头模式
    headless = os.environ.get('CRAWLER_HEADLESS', '').lower()
    if headless == 'false':
        config.headless = False

    # 请求超时
    timeout = os.environ.get('CRAWLER_REQUEST_TIMEOUT')
    if timeout:
        try:
            config.request_timeout = int(timeout)
        except ValueError:
            pass

    return config


# 默认配置实例
default_config = SpiderConfig()


class ConfigManager:
    """
    配置管理器

    提供配置的加载、保存和动态更新功能
    """

    def __init__(self, config: SpiderConfig = None):
        """
        初始化配置管理器

        Args:
            config: 初始配置，如果不提供则使用默认配置
        """
        self.config = config or default_config

    def update(self, **kwargs):
        """
        更新配置项

        Args:
            **kwargs: 配置项键值对
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

    def get(self, key: str, default=None):
        """
        获取配置项

        Args:
            key: 配置项名称
            default: 默认值

        Returns:
            配置值
        """
        return getattr(self.config, key, default)

    def save_to_file(self, filepath: str):
        """
        保存配置到文件

        Args:
            filepath: 文件路径
        """
        import json

        config_dict = self.config.to_dict()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, ensure_ascii=False, indent=2)

        logger = __import__('logging').getLogger('crawler')
        logger.info(f"配置已保存到: {filepath}")

    @classmethod
    def load_from_file(cls, filepath: str) -> 'ConfigManager':
        """
        从文件加载配置

        Args:
            filepath: 文件路径

        Returns:
            ConfigManager: 配置管理器实例
        """
        import json

        with open(filepath, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)

        config = SpiderConfig()
        for key, value in config_dict.items():
            if hasattr(config, key):
                setattr(config, key, value)

        return cls(config)
