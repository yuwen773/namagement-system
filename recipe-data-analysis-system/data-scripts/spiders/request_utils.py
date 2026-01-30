# -*- coding: utf-8 -*-
"""
HTTP请求工具模块

功能：
- User-Agent 轮换
- 自动重试机制
- 异常处理
- Session 管理
"""

import time
import random
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# 真实浏览器 User-Agent 列表
USER_AGENTS = [
    # Chrome on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    # Chrome on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    # Firefox on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    # Firefox on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    # Edge on Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    # Safari on macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
]


class RequestUtils:
    """HTTP请求工具类"""

    def __init__(
        self,
        retry_times: int = 3,
        retry_delay: float = 2.0,
        timeout: int = 30,
        min_delay: float = 5.0,
        max_delay: float = 10.0
    ):
        """
        初始化请求工具

        Args:
            retry_times: 重试次数
            retry_delay: 重试延迟（秒）
            timeout: 请求超时时间（秒）
            min_delay: 最小请求间隔（秒）- 增加到5秒
            max_delay: 最大请求间隔（秒）- 增加到10秒
        """
        self.retry_times = retry_times
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0

        # 创建 Session，配置重试策略
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """创建带重试策略的 Session"""
        session = requests.Session()

        # 配置重试策略（不重试 429 错误，因为需要等待更长时间）
        retry_strategy = Retry(
            total=self.retry_times,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],  # 移除 429
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _get_random_ua(self) -> str:
        """获取随机 User-Agent"""
        return random.choice(USER_AGENTS)

    def _get_default_headers(self) -> Dict[str, str]:
        """获取默认请求头"""
        return {
            'User-Agent': self._get_random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        }

    def _respect_delay(self):
        """遵守请求间隔"""
        now = time.time()
        elapsed = now - self.last_request_time

        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed + random.uniform(0, 1)
            time.sleep(sleep_time)
        else:
            # 随机延迟，避免固定模式
            time.sleep(random.uniform(0, 1))

        self.last_request_time = time.time()

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        allow_redirects: bool = True
    ) -> requests.Response:
        """
        发送 GET 请求

        Args:
            url: 请求 URL
            params: URL 参数
            headers: 自定义请求头（会与默认头合并）
            allow_redirects: 是否允许重定向

        Returns:
            Response 对象

        Raises:
            requests.RequestException: 请求失败
        """
        self._respect_delay()

        # 合并请求头
        final_headers = self._get_default_headers()
        if headers:
            final_headers.update(headers)

        try:
            response = self.session.get(
                url,
                params=params,
                headers=final_headers,
                timeout=self.timeout,
                allow_redirects=allow_redirects
            )
            response.raise_for_status()
            return response

        except requests.RequestException as e:
            print(f"请求失败: {url}, 错误: {e}")
            raise

    def download_image(
        self,
        url: str,
        save_path: str,
        headers: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        下载图片

        Args:
            url: 图片 URL
            save_path: 保存路径
            headers: 自定义请求头

        Returns:
            是否下载成功
        """
        self._respect_delay()

        # 合并请求头
        final_headers = self._get_default_headers()
        if headers:
            final_headers.update(headers)

        try:
            response = self.session.get(
                url,
                headers=final_headers,
                timeout=self.timeout,
                stream=True
            )
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True

        except requests.RequestException as e:
            print(f"下载图片失败: {url}, 错误: {e}")
            return False

    def close(self):
        """关闭 Session"""
        self.session.close()


# 全局请求工具实例
_request_utils: Optional[RequestUtils] = None


def get_request_utils() -> RequestUtils:
    """获取全局请求工具实例"""
    global _request_utils
    if _request_utils is None:
        _request_utils = RequestUtils()
    return _request_utils
