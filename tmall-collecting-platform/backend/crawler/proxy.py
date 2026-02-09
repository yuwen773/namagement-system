"""
代理IP管理模块
提供代理IP的获取、验证和轮换功能
"""
import logging
import random
import time
from typing import Optional, List, Dict
from dataclasses import dataclass

logger = logging.getLogger('crawler')


@dataclass
class ProxyInfo:
    """代理信息"""
    ip: str
    port: int
    protocol: str = 'http'  # http, https
    username: Optional[str] = None
    password: Optional[str] = None
    latency: int = 0  # 延迟(ms)
    success_count: int = 0  # 成功次数
    fail_count: int = 0  # 失败次数

    @property
    def url(self) -> str:
        """返回代理URL格式"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.ip}:{self.port}"
        return f"{self.protocol}://{self.ip}:{self.port}"

    @property
    def is_available(self) -> bool:
        """检查代理是否可用"""
        return self.fail_count < 3  # 失败3次后标记为不可用


class ProxyManager:
    """
    代理IP管理器

    功能：
    1. 管理代理IP列表
    2. 提供代理轮换
    3. 记录代理成功率
    """

    def __init__(self, proxy_list: Optional[List[Dict]] = None):
        """
        初始化代理管理器

        Args:
            proxy_list: 代理列表，每项包含 ip, port, protocol 等
        """
        self.proxies: List[ProxyInfo] = []
        self.current_index = 0
        self.failed_proxies: List[str] = []  # 失败代理黑名单

        # 初始化代理列表
        if proxy_list:
            for p in proxy_list:
                self.proxies.append(ProxyInfo(
                    ip=p.get('ip', ''),
                    port=p.get('port', 0),
                    protocol=p.get('protocol', 'http'),
                    username=p.get('username'),
                    password=p.get('password')
                ))

        # 如果没有配置代理，添加一个空代理（直连）
        if not self.proxies:
            logger.info("未配置代理IP，将使用直连方式")

    def add_proxy(self, proxy: Dict):
        """添加代理"""
        self.proxies.append(ProxyInfo(
            ip=proxy.get('ip', ''),
            port=proxy.get('port', 0),
            protocol=proxy.get('protocol', 'http'),
            username=proxy.get('username'),
            password=proxy.get('password')
        ))

    def get_proxy(self) -> Optional[ProxyInfo]:
        """
        获取一个可用的代理

        Returns:
            ProxyInfo: 可用代理，如果没有可用代理返回None（直连）
        """
        if not self.proxies:
            return None

        # 尝试从可用代理中选择
        available = [p for p in self.proxies if p.is_available and p.url not in self.failed_proxies]

        if not available:
            # 如果没有可用代理，清空失败列表重试
            self.failed_proxies.clear()
            available = [p for p in self.proxies if p.is_available]

            if not available:
                logger.warning("所有代理都不可用，将使用直连")
                return None

        # 随机选择一个可用代理
        proxy = random.choice(available)

        # 轮询策略：按顺序选择
        # proxy = self.proxies[self.current_index % len(self.proxies)]
        # self.current_index += 1

        return proxy

    def report_success(self, proxy: ProxyInfo):
        """报告代理使用成功"""
        proxy.success_count += 1
        proxy.latency = proxy.latency or random.randint(50, 200)
        logger.debug(f"代理成功: {proxy.ip}:{proxy.port}")

    def report_failure(self, proxy: ProxyInfo):
        """报告代理使用失败"""
        proxy.fail_count += 1
        self.failed_proxies.append(proxy.url)
        logger.warning(f"代理失败: {proxy.ip}:{proxy.port}, 累计失败: {proxy.fail_count}")

    def get_stats(self) -> Dict:
        """获取代理统计信息"""
        total = len(self.proxies)
        available = len([p for p in self.proxies if p.is_available])

        return {
            'total_proxies': total,
            'available_proxies': available,
            'failed_count': len(self.failed_proxies)
        }

    def rotate_proxy(self, current_proxy: Optional[ProxyInfo]) -> Optional[ProxyInfo]:
        """
        轮换代理

        Args:
            current_proxy: 当前使用的代理

        Returns:
            ProxyInfo: 新的代理
        """
        if current_proxy:
            self.report_failure(current_proxy)

        return self.get_proxy()


class FreeProxyProvider:
    """
    免费代理提供商

    注意：免费代理质量参差不齐，仅供测试使用
    生产环境建议使用付费代理服务
    """

    # 常用的免费代理API
    PROXY_APIS = [
        'https://api.proxyscrape.com/v2/?request=get&proxies=http',
        'https://www.proxy-list.download/api/v1/get?type=http',
    ]

    @staticmethod
    def fetch_from_api(api_url: str, timeout: int = 10) -> List[Dict]:
        """
        从API获取代理列表

        Args:
            api_url: 代理API地址
            timeout: 超时时间

        Returns:
            List[Dict]: 代理列表
        """
        import requests

        try:
            response = requests.get(api_url, timeout=timeout)
            response.raise_for_status()

            # 解析代理列表
            proxies = []
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if not line:
                    continue

                # 格式: ip:port
                if ':' in line:
                    parts = line.split(':')
                    proxies.append({
                        'ip': parts[0],
                        'port': int(parts[1]),
                        'protocol': 'http'
                    })

            logger.info(f"从 {api_url} 获取到 {len(proxies)} 个代理")
            return proxies

        except Exception as e:
            logger.error(f"获取代理失败: {e}")
            return []


def create_proxy_manager(config: Optional[Dict] = None) -> ProxyManager:
    """
    工厂函数：创建代理管理器

    Args:
        config: 配置信息，包含 proxy_list 等

    Returns:
        ProxyManager: 代理管理器实例
    """
    config = config or {}

    # 从配置获取代理列表
    proxy_list = config.get('proxy_list', [])

    # 如果配置了免费代理API，可以从这里获取
    # proxy_api = config.get('proxy_api')
    # if proxy_api:
    #     from crawler.proxy import FreeProxyProvider
    #     api_proxies = FreeProxyProvider.fetch_from_api(proxy_api)
    #     proxy_list.extend(api_proxies)

    return ProxyManager(proxy_list)
