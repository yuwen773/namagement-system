"""
360问答数据采集脚本

使用方法:
1. 确保已安装依赖: pip install playwright
2. 安装浏览器: playwright install chromium
3. 运行脚本: python run_crawler.py

功能:
- 访问360问答列表页
- 提取问题标题和链接
- 进入详情页提取回答
- 保存到数据库
"""

import asyncio
import json
import re
import time
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("错误: 请先安装 Playwright")
    print("运行: pip install playwright")
    print("然后: playwright install chromium")
    exit(1)


class WendaCrawler:
    """360问答爬虫"""

    def __init__(self, max_pages: int = 10, max_items: int = 100):
        self.max_pages = max_pages
        self.max_items = max_items
        self.collected_count = 0
        self.failed_count = 0
        self.browser = None
        self.page = None
        self.context = None

        # 间隔配置
        self.interval = 5  # 初始间隔（秒）
        self.max_interval = 15

    async def start(self):
        """启动爬虫"""
        print("=" * 60)
        print("  360问答数据采集器")
        print("=" * 60)
        print(f"采集配置: 最多 {self.max_pages} 页, 最多 {self.max_items} 条数据")
        print()

        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,  # 有头模式，方便观察
            args=['--disable-blink-features=AutomationControlled']
        )

        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        self.page = await self.context.new_page()

        # 访问首页
        print("正在访问360问答...")
        await self.page.goto("https://wenda.so.com/", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # 关闭弹窗
        await self.close_popup()

        # 导航到列表页
        print("导航到列表页...")
        await self.page.goto("https://wenda.so.com/c/", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # 开始采集
        await self.crawl_list_pages()

        # 清理
        await self.browser.close()
        await playwright.stop()

        print()
        print("=" * 60)
        print(f"采集完成! 共采集 {self.collected_count} 条数据")
        print(f"失败: {self.failed_count} 条")
        print("=" * 60)

    async def close_popup(self):
        """关闭弹窗"""
        try:
            close_btn = await self.page.query_selector("span.close")
            if close_btn:
                await close_btn.click()
                await asyncio.sleep(1)
                print("已关闭弹窗")
        except Exception as e:
            pass

    async def crawl_list_pages(self):
        """采集列表页"""
        print(f"\n开始采集列表页...")

        for page_num in range(self.max_pages):
            if self.collected_count >= self.max_items:
                print(f"\n已达到采集上限: {self.max_items} 条")
                break

            print(f"\n--- 第 {page_num + 1} 页 ---")

            # 滚动加载更多
            await self.page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(1)

            # 提取问题列表
            items = await self.extract_list_items()

            if not items:
                print(f"第 {page_num + 1} 页无数据，尝试刷新...")
                await self.page.reload(wait_until="domcontentloaded")
                await asyncio.sleep(2)
                items = await self.extract_list_items()

                if not items:
                    print(f"第 {page_num + 1} 页确实无数据，停止采集")
                    break

            print(f"本页找到 {len(items)} 个问题")

            # 遍历每个问题
            for idx, item in enumerate(items):
                if self.collected_count >= self.max_items:
                    break

                try:
                    # 进入详情页
                    url = item.get('url', '')
                    if not url:
                        print(f"  ✗ 无URL，跳过")
                        continue

                    # 检查URL是否有效
                    if not url.startswith('http'):
                        print(f"  ✗ 无效URL: {url}")
                        continue

                    # 打印URL调试
                    print(f"  URL: {url}")

                    print(f"  [{idx + 1}] 访问: {item.get('title', '')[:30]}...")

                    # 直接在当前页面导航（更稳定）
                    await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(3)  # 等待页面加载

                    # 提取详情
                    detail = await self.extract_detail(self.page)
                    item.update(detail)

                    # 保存到文件
                    await self.save_item(item)

                    self.collected_count += 1
                    print(f"  ✓ 已采集 {self.collected_count} 条")

                    # 返回列表页
                    await self.page.go_back()
                    await asyncio.sleep(2)  # 等待返回

                    # 等待间隔（逐渐增加）
                    wait_time = min(self.interval + random.uniform(0, 2), self.max_interval)
                    print(f"  等待 {wait_time:.1f} 秒...")
                    await asyncio.sleep(wait_time)

                    # 增加间隔
                    self.interval = min(self.interval + 0.5, self.max_interval)

                except Exception as e:
                    self.failed_count += 1
                    print(f"  ✗ 失败: {str(e)[:80]}")
                    # 尝试返回列表页
                    try:
                        await self.page.goto("https://wenda.so.com/c/", wait_until="domcontentloaded")
                        await asyncio.sleep(2)
                    except:
                        pass
                    continue

            # 翻页
            if page_num < self.max_pages - 1 and self.collected_count < self.max_items:
                # 直接用URL翻页
                next_url = f"https://wenda.so.com/c/?pn={page_num + 1}"
                print(f"\n翻到第 {page_num + 2} 页...")
                try:
                    await self.page.goto(next_url, wait_until="domcontentloaded", timeout=30000)
                    await asyncio.sleep(3)
                except Exception as e:
                    print(f"翻页失败: {e}")
                    break

    async def extract_list_items(self) -> List[Dict]:
        """提取列表页问题"""
        items = []

        try:
            # 等待列表加载
            await self.page.wait_for_selector("ul.question-list li", timeout=5000)

            # 获取所有问题项
            li_elements = await self.page.query_selector_all("ul.question-list li")

            for li in li_elements:
                try:
                    # 提取ID
                    askid = await li.get_attribute("data-askid")

                    # 提取标题和链接
                    title_elem = await li.query_selector("p.fl a")
                    title = await title_elem.inner_text() if title_elem else ""
                    href = await title_elem.get_attribute("href") if title_elem else ""

                    # 提取回答数
                    ans_count = await li.get_attribute("data-ans")

                    if title and href:
                        items.append({
                            'question_id': askid or '',
                            'title': title.strip(),
                            'url': href,
                            'answer_count': int(ans_count) if ans_count else 0,
                            'crawl_time': datetime.now().isoformat()
                        })
                except Exception as e:
                    continue

        except Exception as e:
            print(f"提取列表失败: {e}")

        return items

    async def extract_detail(self, page) -> Dict:
        """提取详情页数据"""
        detail = {
            'question_title': '',
            'question_content': '',
            'category': '',
            'tags': [],
            'answers': []
        }

        try:
            # 等待详情加载
            await page.wait_for_selector(".question-box", timeout=5000)

            # 问题标题
            try:
                title_elem = await page.query_selector("h1.title")
                detail['question_title'] = await title_elem.inner_text() if title_elem else ""
            except:
                pass

            # 问题内容
            try:
                content_elem = await page.query_selector(".question-content")
                detail['question_content'] = await content_elem.inner_text() if content_elem else ""
            except:
                pass

            # 分类
            try:
                category_elem = await page.query_selector(".q-tags a")
                detail['category'] = await category_elem.inner_text() if category_elem else ""
            except:
                pass

            # 标签
            try:
                tag_elems = await page.query_selector_all(".q-tags span")
                tags = []
                for tag in tag_elems:
                    tag_text = await tag.inner_text()
                    if tag_text:
                        tags.append(tag_text.strip())
                detail['tags'] = tags
            except:
                pass

            # 回答列表
            try:
                answer_items = await page.query_selector_all(".answer-item")
                for ans in answer_items:
                    try:
                        # 回答内容
                        content_elem = await ans.query_selector(".answer-content")
                        content = await content_elem.inner_text() if content_elem else ""

                        # 回答者
                        answerer_elem = await ans.query_selector(".answerer-name, .user-name")
                        answerer = await answerer_elem.inner_text() if answerer_elem else ""

                        # 回答时间
                        time_elem = await ans.query_selector(".answer-time")
                        answer_time = await time_elem.inner_text() if time_elem else ""

                        if content:
                            detail['answers'].append({
                                'content': content.strip(),
                                'answerer': answerer.strip() if answerer else '',
                                'answer_time': answer_time.strip() if answer_time else ''
                            })
                    except:
                        continue
            except:
                pass

        except Exception as e:
            print(f"  提取详情失败: {e}")

        return detail

    async def save_item(self, item: Dict):
        """保存数据到文件"""
        # 创建输出目录
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # 保存到JSONL文件（每行一个JSON）
        output_file = output_dir / "wenda_data.jsonl"

        # 读取现有数据
        existing_data = []
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        existing_data.append(json.loads(line))

        # 添加新数据
        existing_data.append(item)

        # 写回文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in existing_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')


async def main():
    """主函数"""
    import sys

    # 解析参数
    max_pages = 10
    max_items = 100

    if len(sys.argv) > 1:
        max_pages = int(sys.argv[1])
    if len(sys.argv) > 2:
        max_items = int(sys.argv[2])

    crawler = WendaCrawler(max_pages=max_pages, max_items=max_items)
    await crawler.start()


if __name__ == "__main__":
    asyncio.run(main())
