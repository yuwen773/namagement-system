"""
Playwright 录制器核心类 - 负责浏览器操作录制和步骤生成
"""
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from playwright.async_api import async_playwright, Browser, Page, BrowserContext


class Recorder:
    """Playwright 录制器核心类"""

    def __init__(self, headless: bool = False):
        """初始化录制器

        Args:
            headless: 是否使用无头模式，默认为 False（有头模式）
        """
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._steps: List[Dict[str, Any]] = []
        self._is_recording = False

    async def start(self, url: str = None) -> None:
        """启动录制，创建浏览器实例

        Args:
            url: 初始导航 URL，可选
        """
        self.playwright = await async_playwright().start()

        # 启动 Chromium 浏览器
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )

        # 创建浏览器上下文
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # 创建新页面
        self.page = await self.context.new_page()

        # 注入录制脚本
        await self._inject_recorder_script()

        # 绑定事件监听
        await self._bind_event_listeners()

        # 标记为正在录制
        self._is_recording = True

        # 如果提供了 URL，则导航到该 URL
        if url:
            await self.navigate(url)

    async def stop(self) -> List[Dict[str, Any]]:
        """停止录制，返回录制的步骤列表

        Returns:
            录制的步骤列表
        """
        if not self._is_recording:
            return self._steps

        # 关闭浏览器
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self._is_recording = False

        return self._steps.copy()

    async def navigate(self, url: str) -> None:
        """导航到 URL

        Args:
            url: 目标 URL
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.goto(url, wait_until='domcontentloaded')
        # 重新注入脚本（页面导航后需要重新注入）
        await self._inject_recorder_script()
        await self._bind_event_listeners()

    async def click(self, selector: str) -> None:
        """点击元素

        Args:
            selector: 元素选择器
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.click(selector)
        await self.page.wait_for_timeout(100)  # 等待操作完成

    async def wait_for_selector(self, selector: str, timeout: int = 10000) -> None:
        """等待元素出现

        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒），默认 10000
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.wait_for_selector(selector, timeout=timeout)

    async def wait_for_timeout(self, timeout: int) -> None:
        """等待指定时间

        Args:
            timeout: 等待时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.wait_for_timeout(timeout)

    async def get_steps(self) -> List[Dict[str, Any]]:
        """获取录制的步骤

        Returns:
            步骤列表
        """
        return self._steps.copy()

    async def clear_steps(self) -> None:
        """清空步骤"""
        self._steps = []

    async def screenshot(self, path: str = None) -> bytes:
        """截图

        Args:
            path: 保存路径，如果为 None 则只返回字节数据

        Returns:
            截图的字节数据
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        screenshot_bytes = await self.page.screenshot(full_page=True)

        if path:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'wb') as f:
                f.write(screenshot_bytes)

        return screenshot_bytes

    @property
    def current_url(self) -> str:
        """获取当前 URL

        Returns:
            当前页面 URL
        """
        if not self.page:
            return ""
        return self.page.url

    async def _inject_recorder_script(self) -> None:
        """注入录制脚本到页面"""
        script = '''
        (function() {
            // 初始化步骤数组
            window.__recorderSteps = window.__recorderSteps || [];

            // 生成唯一选择器
            window.__generateSelector = function(element) {
                if (!element) return '';

                // 优先使用 id
                if (element.id) {
                    return '#' + element.id;
                }

                // 使用 data-* 属性
                for (let attr of element.attributes) {
                    if (attr.name.startsWith('data-')) {
                        return '[' + attr.name + '="' + attr.value + '"]';
                    }
                }

                // 使用 class（取前两个）
                if (element.className && typeof element.className === 'string') {
                    const classes = element.className.trim().split(/\\s+/).filter(c => c);
                    if (classes.length > 0) {
                        return element.tagName.toLowerCase() + '.' + classes.slice(0, 2).join('.');
                    }
                }

                // 使用 name 属性
                if (element.name) {
                    return element.tagName.toLowerCase() + '[name="' + element.name + '"]';
                }

                // 回退到路径选择器
                let path = [];
                let current = element;
                while (current && current !== document.body) {
                    let selector = current.tagName.toLowerCase();
                    if (current.id) {
                        selector += '#' + current.id;
                        path.unshift(selector);
                        break;
                    } else if (current.className && typeof current.className === 'string') {
                        const classes = current.className.trim().split(/\\s+/).filter(c => c);
                        if (classes.length > 0) {
                            selector += '.' + classes[0];
                        }
                    }
                    path.unshift(selector);
                    current = current.parentElement;
                }
                return path.join(' > ');
            };

            // 记录步骤
            window.__recordStep = function(type, data) {
                const step = {
                    type: type,
                    timestamp: new Date().toISOString(),
                    ...data
                };
                window.__recorderSteps.push(step);

                // 触发自定义事件以便 Python 端捕获
                window.dispatchEvent(new CustomEvent('recorder-step', { detail: step }));
            };

            // 监听点击事件
            document.addEventListener('click', function(e) {
                const target = e.target;
                if (!target || target === document.body || target === document.documentElement) return;

                const selector = window.__generateSelector(target);
                const text = target.innerText ? target.innerText.substring(0, 50) : '';
                const tagName = target.tagName.toLowerCase();

                window.__recordStep('click', {
                    selector: selector,
                    tagName: tagName,
                    text: text,
                    x: e.clientX,
                    y: e.clientY
                });
            }, true);

            // 监听输入事件
            document.addEventListener('input', function(e) {
                const target = e.target;
                if (!target || !['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) return;
                if (target.type === 'password' || target.type === 'hidden') return;

                const selector = window.__generateSelector(target);
                const value = target.value || '';

                window.__recordStep('input', {
                    selector: selector,
                    tagName: target.tagName.toLowerCase(),
                    value: value
                });
            }, true);

            // 监听滚动事件（节流）
            let scrollTimeout = null;
            document.addEventListener('scroll', function(e) {
                if (scrollTimeout) return;

                scrollTimeout = setTimeout(function() {
                    scrollTimeout = null;

                    window.__recordStep('scroll', {
                        x: window.scrollX,
                        y: window.scrollY,
                        scrollTop: document.documentElement.scrollTop,
                        scrollLeft: document.documentElement.scrollLeft
                    });
                }, 500);
            }, true);

            // 监听键盘事件
            document.addEventListener('keydown', function(e) {
                // 只记录特殊键
                if (['Enter', 'Escape', 'Tab', 'ArrowDown', 'ArrowUp', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                    window.__recordStep('keyboard', {
                        key: e.key,
                        code: e.code,
                        ctrlKey: e.ctrlKey,
                        shiftKey: e.shiftKey,
                        altKey: e.altKey
                    });
                }
            }, true);

            console.log('Recorder script injected');
        })();
        '''
        await self.page.evaluate(script)

    async def _bind_event_listeners(self) -> None:
        """绑定事件监听器以捕获步骤"""
        if not self.page:
            return

        # 设置事件处理器来捕获 Python 端的步骤
        def handle_route(route):
            route.continue_()

        # 创建自定义事件处理器
        async def handle_recorder_step(step):
            self._steps.append(step)

        # 通过 page.evaluate 获取步骤
        await self.page.expose_function('py_record_step', lambda step: self._steps.append(step))

    async def sync_steps(self) -> None:
        """同步页面的步骤到 Python 端"""
        if not self.page:
            return

        # 从页面获取步骤
        steps = await self.page.evaluate('window.__recorderSteps || []')
        if steps and len(steps) > len(self._steps):
            self._steps = steps

    async def get_page_title(self) -> str:
        """获取页面标题

        Returns:
            页面标题
        """
        if not self.page:
            return ""
        return await self.page.title()

    async def get_element_info(self, selector: str) -> Optional[Dict[str, Any]]:
        """获取元素信息

        Args:
            selector: 元素选择器

        Returns:
            元素信息字典
        """
        if not self.page:
            return None

        try:
            element = await self.page.query_selector(selector)
            if not element:
                return None

            info = await element.evaluate('''
                (el) => {
                    return {
                        tagName: el.tagName.toLowerCase(),
                        text: el.innerText ? el.innerText.substring(0, 100) : '',
                        id: el.id || null,
                        className: el.className || '',
                        href: el.href || null,
                        src: el.src || null,
                        visible: el.offsetParent !== null
                    };
                }
            ''')
            return info
        except Exception:
            return None

    async def evaluate(self, script: str):
        """在页面上下文中执行 JavaScript

        Args:
            script: JavaScript 代码

        Returns:
            执行结果
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        return await self.page.evaluate(script)

    async def fill(self, selector: str, value: str) -> None:
        """填写表单字段

        Args:
            selector: 元素选择器
            value: 要填写的值
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.fill(selector, value)

    async def select_option(self, selector: str, value: str) -> None:
        """选择下拉选项

        Args:
            selector: 选择器
            value: 选项值
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.select_option(selector, value)

    async def hover(self, selector: str) -> None:
        """悬停在元素上

        Args:
            selector: 元素选择器
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.hover(selector)

    async def scroll_to_element(self, selector: str) -> None:
        """滚动到元素

        Args:
            selector: 元素选择器
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        await self.page.locator(selector).scroll_into_view_if_needed()

    async def get_html(self, selector: str = None) -> str:
        """获取页面或元素的 HTML

        Args:
            selector: 元素选择器，如果为 None 则获取整个页面 HTML

        Returns:
            HTML 字符串
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")

        if selector:
            element = await self.page.query_selector(selector)
            if element:
                return await element.inner_html()
            return ""
        return await self.page.content()

    async def close(self) -> None:
        """关闭浏览器（别名）"""
        await self.stop()

    def is_recording(self) -> bool:
        """检查是否正在录制

        Returns:
            是否正在录制
        """
        return self._is_recording
