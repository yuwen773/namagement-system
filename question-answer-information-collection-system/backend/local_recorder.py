"""
本地录制器 - 独立运行的录制工具

使用方法:
1. 确保已安装依赖: pip install playwright
2. 安装浏览器: playwright install chromium
3. 运行脚本: python local_recorder.py

功能:
- 启动浏览器并录制用户操作
- 自动生成元素选择器
- 导出 JSON 配置文件
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 检查 Playwright 是否安装
try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
except ImportError:
    print("错误: 请先安装 Playwright")
    print("运行: pip install playwright")
    print("然后: playwright install chromium")
    sys.exit(1)


class LocalRecorder:
    """本地录制器 - 在用户本地浏览器中运行"""

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._steps: List[Dict[str, Any]] = []
        self._is_recording = False
        self._start_url = ""

    async def start(self, url: str = None) -> None:
        """启动录制器"""
        print("\n" + "=" * 50)
        print("  问答信息采集系统 - 本地录制器")
        print("=" * 50)
        print("\n启动浏览器...")

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )

        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        self.page = await self.context.new_page()

        # 使用 Playwright 事件监听器来捕获点击
        self.page.on("click", self._on_click)

        # 注入录制脚本（用于生成选择器）
        await self._inject_recorder_script()

        self._is_recording = True
        self._start_url = url or "https://wenda.so.com/c/"

        print(f"浏览器已启动，导航到: {self._start_url}")
        print("\n录制说明:")
        print("  - 点击页面元素: 自动记录点击操作")
        print("  - 输入内容: 自动记录输入操作")
        print("  - 滚动页面: 自动记录滚动操作")
        print("  - 导航: URL 变化时自动记录")
        print("\n操作完成后，请关闭浏览器窗口完成录制")
        print("-" * 50 + "\n")

        # 监听页面关闭事件
        self.page.on("close", self._on_page_close)

        # 监听页面导航事件
        self.page.on("framenavigated", self._on_frame_navigated)

        if url:
            await self.page.goto(url, wait_until='domcontentloaded')
            await self._inject_recorder_script()
            # 等待脚本加载
            await asyncio.sleep(1)

    async def _on_click(self, element):
        """捕获点击事件"""
        try:
            # 获取元素信息
            tag_name = await element.evaluate("el => el.tagName.toLowerCase()")
            text = await element.evaluate("el => el.innerText ? el.innerText.substring(0, 50) : ''")

            # 生成选择器
            selector = await element.evaluate('''el => {
                if (el.id) return '#' + el.id;
                if (el.className && typeof el.className === 'string') {
                    const classes = el.className.trim().split(/\\s+/).filter(c => c);
                    if (classes.length > 0) return el.tagName.toLowerCase() + '.' + classes.slice(0, 2).join('.');
                }
                for (let attr of el.attributes) {
                    if (attr.name.startsWith('data-')) return '[' + attr.name + '="' + attr.value + '"]';
                }
                return el.tagName.toLowerCase();
            }''')

            # 记录步骤
            step = {
                'type': 'click',
                'timestamp': datetime.now().isoformat() + 'Z',
                'selector': selector,
                'tagName': tag_name,
                'text': text,
                'url': self.page.url if self.page else ''
            }
            self._steps.append(step)
            print(f"点击 recorded: {tag_name} - {selector}")

        except Exception as e:
            print(f"记录点击失败: {e}")

    async def _on_frame_navigated(self, frame):
        """页面导航后重新注入脚本"""
        if self._is_recording and frame == self.page.main_frame:
            # 记录导航步骤
            step = {
                'type': 'navigate',
                'timestamp': datetime.now().isoformat() + 'Z',
                'url': self.page.url,
                'description': '页面导航'
            }
            self._steps.append(step)
            print(f"导航 recorded: {self.page.url}")

            # 重新注入脚本
            await self._inject_recorder_script()

    async def _on_page_close(self):
        """页面关闭时自动保存步骤"""
        if self._is_recording:
            print("\n检测到浏览器关闭，正在保存录制...")
            # 页面已关闭，无法同步，直接使用本地缓存的步骤
            self._is_recording = False
            await self._cleanup_resources()
            print(f"\n录制完成! 共记录 {len(self._steps)} 个步骤")

    async def stop(self) -> List[Dict[str, Any]]:
        """停止录制"""
        if not self._is_recording:
            return self._steps

        # 同步最后一批步骤
        await self.sync_steps()

        print(f"\n录制完成! 共记录 {len(self._steps)} 个步骤")

        # 清理资源
        await self._cleanup_resources()

        self._is_recording = False

        return self._steps.copy()

    async def _cleanup_resources(self) -> None:
        """清理浏览器资源"""
        try:
            if self.browser:
                await self.browser.close()
        except Exception as e:
            print(f"关闭浏览器时出错: {e}")
        finally:
            self.browser = None

        try:
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"停止 Playwright 时出错: {e}")
        finally:
            self.playwright = None

        self.context = None
        self.page = None

    async def sync_steps(self) -> None:
        """同步页面的步骤"""
        if not self.page:
            return

        try:
            steps = await self.page.evaluate('window.__recorderSteps || []')
            if steps:
                # 合并步骤，去重
                existing_hashes = set()
                new_steps = []
                for step in self._steps:
                    h = f"{step.get('type')}_{step.get('selector')}_{step.get('timestamp')}"
                    existing_hashes.add(h)
                    new_steps.append(step)

                for step in steps:
                    h = f"{step.get('type')}_{step.get('selector')}_{step.get('timestamp')}"
                    if h not in existing_hashes:
                        new_steps.append(step)

                self._steps = new_steps
        except Exception as e:
            print(f"同步步骤时出错: {e}")

    async def _inject_recorder_script(self) -> None:
        """注入录制脚本"""
        script = '''
        (function() {
            window.__recorderSteps = window.__recorderSteps || [];

            window.__generateSelector = function(element) {
                if (!element) return '';

                if (element.id) {
                    return '#' + element.id;
                }

                for (let attr of element.attributes) {
                    if (attr.name.startsWith('data-')) {
                        return '[' + attr.name + '="' + attr.value + '"]';
                    }
                }

                if (element.className && typeof element.className === 'string') {
                    const classes = element.className.trim().split(/\\s+/).filter(c => c);
                    if (classes.length > 0) {
                        return element.tagName.toLowerCase() + '.' + classes.slice(0, 2).join('.');
                    }
                }

                if (element.name) {
                    return element.tagName.toLowerCase() + '[name="' + element.name + '"]';
                }

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

            window.__recordStep = function(type, data) {
                const step = {
                    type: type,
                    timestamp: new Date().toISOString(),
                    ...data
                };
                window.__recorderSteps.push(step);
                console.log('Recorded step:', type, data);
            };

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

            document.addEventListener('keydown', function(e) {
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

            // 监听 URL 变化
            let lastUrl = location.href;
            new MutationObserver(function() {
                const url = location.href;
                if (url !== lastUrl) {
                    lastUrl = url;
                    window.__recordStep('navigate', {
                        url: url,
                        title: document.title
                    });
                }
            }).observe(document, { subtree: true, childList: true });

            console.log('Recorder script injected');
        })();
        '''
        try:
            await self.page.evaluate(script)
        except Exception as e:
            print(f"注入脚本时出错: {e}")

    def is_recording(self) -> bool:
        return self._is_recording


def save_config(steps: List[Dict[str, Any]], config_name: str = None) -> str:
    """保存配置到 JSON 文件"""
    if not config_name:
        config_name = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    output_dir = Path("recordings")
    output_dir.mkdir(exist_ok=True)

    config = {
        "name": config_name,
        "created_at": datetime.now().isoformat(),
        "version": "1.0",
        "steps": steps
    }

    filepath = output_dir / f"{config_name}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    return str(filepath)


async def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='本地录制器')
    parser.add_argument('--url', '-u', type=str, default='https://wenda.so.com/',
                        help='起始 URL (默认: https://wenda.so.com/)')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    parser.add_argument('--name', '-n', type=str, default=None, help='配置文件名')

    args = parser.parse_args()

    recorder = LocalRecorder(headless=args.headless)

    try:
        await recorder.start(url=args.url)

        # 等待用户操作，直到页面关闭
        while recorder.is_recording() and recorder.page:
            await asyncio.sleep(1)
            # 定期同步步骤
            await recorder.sync_steps()

    except KeyboardInterrupt:
        print("\n用户中断，正在保存录制...")
        steps = await recorder.stop()
        if steps:
            filepath = save_config(steps, args.name)
            print(f"\n配置已保存到: {filepath}")
    except Exception as e:
        print(f"错误: {e}")
        await recorder._cleanup_resources()
        sys.exit(1)

    # 保存配置
    steps = recorder._steps
    if steps:
        filepath = save_config(steps, args.name)
        print(f"\n配置已保存到: {filepath}")
        print("\n可以将此配置文件导入系统使用。")
    else:
        print("\n未记录到任何步骤。")


if __name__ == "__main__":
    asyncio.run(main())
