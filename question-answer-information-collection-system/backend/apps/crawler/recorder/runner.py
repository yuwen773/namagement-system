"""
爬虫执行器核心类

负责执行采集任务的核心逻辑，包括：
- Playwright 浏览器管理
- 列表页数据提取
- 详情页数据提取
- 数据保存到数据库
- 任务状态管理（暂停/继续/停止）
- 智能间隔控制
"""

import asyncio
import logging
import random
import re
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin

from playwright.async_api import async_playwright, Browser, Page, Playwright

from apps.crawler.recorder.config_manager import ConfigManager
from apps.crawler.recorder.task_manager import TaskManager, TaskStatus
from apps.crawler.models import Question, Answer

logger = logging.getLogger(__name__)


class Runner:
    """爬虫执行器核心类"""

    BASE_URL = "https://wenda.so.com"

    def __init__(self, task_id: str):
        """
        初始化执行器

        Args:
            task_id: 任务ID (UUID格式)
        """
        self.task_id = task_id

        # 初始化管理器
        self.task_manager = TaskManager()
        self.config_manager = ConfigManager()

        # 任务状态
        self.status = None
        self.config = None

        # Playwright 对象
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

        # 间隔控制
        self.interval_config = {
            'initial': 2,      # 初始间隔 2秒
            'increment': 1,   # 每次增加 1秒
            'max': 10,        # 最大 10秒
            'current': 2      # 当前间隔
        }

        # 运行控制标志
        self._is_running = False
        self._is_paused = False
        self._should_stop = False

        # User-Agent 列表
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        ]

        # 加载任务配置
        self._load_task()

    def _get_user_agent(self) -> str:
        """
        获取随机 User-Agent

        Returns:
            随机选择的 User-Agent 字符串
        """
        return random.choice(self.user_agents)

    def _load_task(self) -> None:
        """加载任务配置"""
        self.status = self.task_manager.get_task_status(self.task_id)
        if not self.status:
            raise ValueError(f"Task {self.task_id} not found")

        config_file = self.status.get('config_file')
        self.config = self.config_manager.load_config(config_file)
        if not self.config:
            raise ValueError(f"Config {config_file} not found")

        # 加载间隔配置
        interval = self.status.get('interval_config', {})
        if interval:
            self.interval_config.update(interval)

    async def start(self) -> bool:
        """
        开始执行任务

        Returns:
            是否成功启动
        """
        try:
            # 启动任务
            self.task_manager.start_task(self.task_id)

            # 初始化 Playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            self.page = await self.browser.new_page()

            # 设置 User-Agent
            await self.page.set_extra_http_headers({
                'User-Agent': self._get_user_agent()
            })

            # 设置运行标志
            self._is_running = True
            self._is_paused = False
            self._should_stop = False

            logger.info(f"Task {self.task_id} started")

            # 执行采集主循环
            await self._run()

            # 完成任务（标记任务完成状态）
            self.task_manager.complete_task(self.task_id)
            logger.info(f"Task {self.task_id} completed")

            return True

        except Exception as e:
            logger.error(f"Task {self.task_id} failed: {e}")
            self.task_manager.fail_task(self.task_id, str(e))
            await self._cleanup()
            return False

    async def _run(self) -> None:
        """执行采集主循环"""
        current_page = self.status.get('progress', {}).get('current_page', 1)
        max_pages = self.config.get('list_config', {}).get('pagination', {}).get('max_pages', 500)

        logger.info(f"Starting crawl from page {current_page}, max pages: {max_pages}")

        try:
            while not self._should_stop:
                # 检查暂停状态
                while self._is_paused and not self._should_stop:
                    await asyncio.sleep(0.5)

                if self._should_stop:
                    break

                # 检查是否达到最大页数
                if current_page > max_pages:
                    logger.info(f"Reached max pages: {max_pages}")
                    break

                # 构建列表页 URL
                list_url = self._build_list_url(current_page)

                try:
                    # 提取列表数据
                    list_items = await self._extract_list({
                        'url': list_url,
                        'page': current_page
                    })

                    if not list_items:
                        logger.warning(f"No items found on page {current_page}, stopping")
                        break

                    # 处理每个列表项
                    for item in list_items:
                        if self._should_stop:
                            break

                        # 检查暂停状态
                        while self._is_paused and not self._should_stop:
                            await asyncio.sleep(0.5)

                        if self._should_stop:
                            break

                        try:
                            # 获取详情页 URL
                            detail_url = item.get('detail_url')
                            if not detail_url:
                                continue

                            # 处理详情页
                            await self._process_detail(detail_url, item)

                        except Exception as e:
                            logger.error(f"Failed to process detail: {e}")
                            self.task_manager.add_error(self.task_id, f"Detail error: {e}")
                            self.task_manager.update_progress(
                                self.task_id,
                                failed_items=self.status.get('progress', {}).get('failed_items', 0) + 1
                            )

                        # 智能间隔
                        await self._smart_interval()

                    # 更新页码
                    current_page += 1
                    self.task_manager.update_progress(self.task_id, current_page=current_page)

                    # 点击下一页
                    if not await self._click_next_page({'page': current_page}):
                        logger.info("No more pages available")
                        break

                except Exception as e:
                    logger.error(f"Error on page {current_page}: {e}")
                    self.task_manager.add_error(self.task_id, f"Page {current_page} error: {e}")
                    current_page += 1

        except Exception as e:
            logger.error(f"Fatal error in _run: {e}")
            self.task_manager.add_error(self.task_id, f"Fatal error: {e}")
            raise
        finally:
            # 确保资源清理
            await self._cleanup()

    def _build_list_url(self, page: int) -> str:
        """
        构建列表页 URL

        Args:
            page: 页码

        Returns:
            列表页 URL
        """
        if page == 1:
            return f"{self.BASE_URL}/c/"
        else:
            # pn 参数从 0 开始: pn=0 -> 第1页, pn=1 -> 第2页
            pn = page - 1
            return f"{self.BASE_URL}/c/?pn={pn}"

    async def _extract_list(self, config: Dict) -> List[Dict]:
        """
        提取列表数据

        Args:
            config: 提取配置，包含 url 和 page

        Returns:
            列表数据项
        """
        url = config.get('url')
        page = config.get('page', 1)

        logger.info(f"Extracting list from page {page}: {url}")

        try:
            # 访问列表页
            await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)

            # 等待列表加载
            await self.page.wait_for_selector('ul.question-list li', timeout=15000)

            # 提取问题列表
            items = await self.page.evaluate('''
                () => {
                    const results = [];
                    const listItems = document.querySelectorAll('ul.question-list li');

                    listItems.forEach((item, index) => {
                        // 提取问题ID
                        const askId = item.getAttribute('data-askid');

                        // 提取标题
                        const titleLink = item.querySelector('a[target="_blank"]');
                        const title = titleLink ? titleLink.textContent.trim() : '';

                        // 提取分类
                        const categoryElem = item.querySelector('a.js-question-cate');
                        const category = categoryElem ? categoryElem.textContent.trim() : '';

                        // 提取回答数
                        const dataAns = item.getAttribute('data-ans');
                        const answerCount = dataAns ? parseInt(dataAns) : 0;

                        // 从 div.fr 中提取时间和地点
                        const infoElem = item.querySelector('div.fr');
                        const infoText = infoElem ? infoElem.textContent : '';

                        // 解析时间 (格式: YYYY.MM.DD)
                        const timeMatch = infoText.match(/(\\d{4}\\.\\d{2}\\.\\d{2})/);
                        const time = timeMatch ? timeMatch[1] : '';

                        // 解析地点
                        const locMatch = infoText.match(/·\\s*(\\S+)/);
                        const location = locMatch ? locMatch[1].trim() : '';

                        // 构造详情页 URL
                        const detailUrl = askId ? `https://wenda.so.com/q/${askId}` : '';

                        if (askId && title) {
                            results.push({
                                id: askId,
                                title: title,
                                category: category,
                                answer_count: answerCount,
                                time: time,
                                location: location,
                                detail_url: detailUrl,
                                page: """ + str(page) + """
                            });
                        }
                    });

                    return results;
                }
            ''')

            logger.info(f"Extracted {len(items)} items from page {page}")
            return items

        except Exception as e:
            logger.error(f"Failed to extract list from page {page}: {e}")
            return []

    async def _process_detail(self, url: str, list_item: Dict) -> None:
        """
        处理详情页

        Args:
            url: 详情页 URL
            list_item: 列表页提取的基础数据
        """
        logger.info(f"Processing detail: {url}")

        try:
            # 打开新标签页访问详情页
            detail_page = await self.browser.new_page()
            await detail_page.set_extra_http_headers({
                'User-Agent': self._get_user_agent()
            })

            try:
                await detail_page.goto(url, wait_until='domcontentloaded', timeout=30000)

                # 等待页面加载完成（使用 Playwright 显式等待）
                await detail_page.wait_for_load_state('networkidle', timeout=15000)

                # 提取详情数据
                detail_data = await detail_page.evaluate('''
                    () => {
                        // 提取问题描述
                        const descElem = document.querySelector('.question-desc, .q-con .text');
                        const description = descElem ? descElem.textContent.trim() : '';

                        // 提取答案列表
                        const answerItems = document.querySelectorAll('.answer-item, .answer-list li, .best-answer');
                        const answers = [];

                        answerItems.forEach((item, index) => {
                            // 提取答案内容
                            const contentElem = item.querySelector('.answer-content, .content, .reply-text');
                            const content = contentElem ? contentElem.textContent.trim() : '';

                            // 提取回答者
                            const answererElem = item.querySelector('.answerer, .user-name, .author');
                            const answerer = answererElem ? answererElem.textContent.trim() : '';

                            // 提取回答时间
                            const timeElem = item.querySelector('.time, .answer-time');
                            const timeText = timeElem ? timeElem.textContent.trim() : '';

                            if (content) {
                                answers.push({
                                    content: content,
                                    answerer: answerer,
                                    time: timeText,
                                    order: index + 1
                                });
                            }
                        });

                        return {
                            description: description,
                            answers: answers
                        };
                    }
                ''')

                # 保存到数据库
                await self._save_to_database(list_item, detail_data)

            finally:
                await detail_page.close()

        except Exception as e:
            logger.error(f"Failed to process detail {url}: {e}")
            raise

    async def _save_to_database(self, list_item: Dict, detail_data: Dict) -> None:
        """
        保存到数据库

        Args:
            list_item: 列表页提取的基础数据
            detail_data: 详情页提取的完整数据
        """
        try:
            # 获取详情页URL
            url = list_item.get('detail_url', '')

            # 1. 从 URL 提取 question_id
            match = re.search(r'/q/(\d+)', url)
            question_id = match.group(1) if match else list_item.get('id')

            if not question_id:
                logger.warning(f"Cannot extract question_id from URL: {url}")
                return

            # 转换时间格式 (YYYY.MM.DD -> date)
            time_str = list_item.get('time', '')
            publish_time = None
            if time_str:
                try:
                    publish_time = datetime.strptime(time_str, '%Y.%m.%d').date()
                except ValueError:
                    pass

            # 2. 创建或更新 Question
            # 使用 asyncio.to_thread 处理同步 Django ORM
            await asyncio.to_thread(
                self._save_question,
                question_id=question_id,
                list_item=list_item,
                detail_data=detail_data,
                url=url,
                publish_time=publish_time
            )

            logger.info(f"Saved question {question_id} to database")

        except Exception as e:
            logger.error(f"Failed to save to database: {e}")
            # 不抛出异常，避免中断爬取流程

    def _save_question(
        self,
        question_id: str,
        list_item: Dict,
        detail_data: Dict,
        url: str,
        publish_time
    ) -> None:
        """
        同步保存问题到数据库（内部方法）

        Args:
            question_id: 问题ID
            list_item: 列表页数据
            detail_data: 详情页数据
            url: 详情页URL
            publish_time: 发布时间
        """
        from django.db import close_old_connections

        try:
            # 构建 Question 默认值
            # title 从列表项获取，description 从详情页获取
            question_defaults = {
                'title': list_item.get('title', ''),
                'description': detail_data.get('description', ''),
                'category': list_item.get('category', ''),
                'source_url': url,
                'answer_count': len(detail_data.get('answers', [])),
                'publish_time': publish_time,
                'location': list_item.get('location', ''),
                'crawl_page': list_item.get('page', 1),
            }

            # 创建或更新 Question
            question, created = Question.objects.update_or_create(
                question_id=question_id,
                defaults=question_defaults
            )

            # 3. 保存答案
            self._save_answers(question, detail_data)

        finally:
            # 关闭旧连接，避免异步环境下的连接问题
            close_old_connections()

    def _save_answers(self, question: Question, detail_data: Dict) -> None:
        """
        保存答案到数据库（内部方法）

        Args:
            question: Question 实例
            detail_data: 详情页数据
        """
        answers_data = detail_data.get('answers', [])

        for answer_data in answers_data:
            try:
                # 转换时间格式
                answer_time = None
                time_text = answer_data.get('time', '')
                if time_text:
                    try:
                        # 尝试多种常见时间格式
                        for fmt in ['%Y.%m.%d', '%Y-%m-%d', '%Y/%m/%d']:
                            try:
                                answer_time = datetime.strptime(time_text, fmt)
                                break
                            except ValueError:
                                continue
                    except Exception:
                        pass

                Answer.objects.update_or_create(
                    question=question,
                    source_order=answer_data.get('order', 1),
                    defaults={
                        'content': answer_data.get('content', ''),
                        'answerer': answer_data.get('answerer', ''),
                        'answer_time': answer_time,
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to save answer: {e}")
                continue

    async def _click_next_page(self, config: Dict) -> bool:
        """
        点击下一页

        Args:
            config: 配置信息

        Returns:
            是否成功点击下一页
        """
        try:
            # 尝试点击分页按钮
            next_button = await self.page.query_selector('.pagination .next, #list-page .next, a:has-text("下一页")')

            if next_button:
                # 检查是否禁用
                is_disabled = await next_button.get_attribute('class')
                if 'disabled' in (is_disabled or ''):
                    return False

                await next_button.click()
                await self.page.wait_for_load_state('domcontentloaded')
                return True

            return False

        except Exception as e:
            logger.debug(f"Failed to click next page: {e}")
            return False

    async def pause(self) -> None:
        """暂停任务"""
        if self._is_running and not self._is_paused:
            self._is_paused = True
            self.task_manager.pause_task(self.task_id)
            logger.info(f"Task {self.task_id} paused")

    async def resume(self) -> None:
        """继续任务"""
        if self._is_running and self._is_paused:
            self._is_paused = False
            self.task_manager.resume_task(self.task_id)
            logger.info(f"Task {self.task_id} resumed")

    async def stop(self) -> None:
        """停止任务"""
        self._should_stop = True
        self._is_running = False
        await self._cleanup()
        logger.info(f"Task {self.task_id} stopped")

    async def _smart_interval(self) -> None:
        """智能间隔控制"""
        current = self.interval_config['current']
        max_interval = self.interval_config['max']
        increment = self.interval_config['increment']

        # 添加随机波动 (±0.5秒)
        interval = current + random.uniform(-0.5, 0.5)
        interval = max(1, interval)  # 最小1秒

        await asyncio.sleep(interval)

        # 逐渐增加间隔
        if current < max_interval:
            self.interval_config['current'] = min(current + increment, max_interval)
            # 更新到任务状态
            self.task_manager.update_progress(
                self.task_id,
                last_item_index=self.status.get('progress', {}).get('last_item_index', 0) + 1
            )

    async def _complete(self) -> None:
        """完成任务"""
        await self._cleanup()
        self.task_manager.complete_task(self.task_id)
        logger.info(f"Task {self.task_id} completed")

    async def _cleanup(self) -> None:
        """清理资源"""
        self._is_running = False

        if self.page:
            await self.page.close()
            self.page = None

        if self.browser:
            await self.browser.close()
            self.browser = None

        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
