# 录制爬虫系统实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现一个基于 Playwright 的可录制回放爬虫系统，集成到现有 Django 管理后台，支持录制用户操作并自动批量采集数据。

**Architecture:** 使用 Playwright 进行浏览器自动化，通过监听用户操作记录选择器，生成 JSON 配置文件，执行器读取配置批量执行采集任务。

**Tech Stack:** Django + DRF, Playwright, Vue 3 + Element Plus

---

## Task 1: 创建爬虫配置文件存储目录和基础结构

**Files:**
- Create: `backend/apps/crawler/recorder/`
- Create: `backend/apps/crawler/recorder/__init__.py`
- Create: `backend/apps/crawler/recorder/config_manager.py`

**Step 1: 创建目录结构**

```bash
mkdir -p backend/apps/crawler/recorder
```

**Step 2: 创建 __init__.py**

```python
"""
录制爬虫模块
"""
```

**Step 3: 创建 config_manager.py**

```python
"""
配置文件管理器 - 负责录制配置的创建、保存和加载
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置文件管理器"""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            base_dir = Path(__file__).parent
            config_dir = base_dir / 'configs'
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def create_config(self, name: str) -> Dict[str, Any]:
        """创建新的录制配置"""
        config = {
            'version': '1.0',
            'name': name,
            'created_at': datetime.now().isoformat() + 'Z',
            'steps': [],
            'list_config': {
                'item_selector': '',
                'pagination': {
                    'type': 'click',
                    'selector': '',
                    'max_pages': 500
                }
            },
            'detail_config': {
                'entry': {
                    'type': 'click',
                    'selector': ''
                },
                'fields': []
            }
        }
        return config

    def save_config(self, config: Dict[str, Any], filename: str = None) -> str:
        """保存配置到文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'config_{timestamp}.json'

        filepath = self.config_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return str(filepath)

    def load_config(self, filename: str) -> Optional[Dict[str, Any]]:
        """加载配置文件"""
        filepath = self.config_dir / filename
        if not filepath.exists():
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_configs(self) -> list:
        """列出所有配置文件"""
        configs = []
        for f in self.config_dir.glob('config_*.json'):
            configs.append({
                'filename': f.name,
                'created_at': f.stat().st_mtime
            })
        return sorted(configs, key=lambda x: x['created_at'], reverse=True)

    def delete_config(self, filename: str) -> bool:
        """删除配置文件"""
        filepath = self.config_dir / filename
        if filepath.exists():
            filepath.unlink()
            return True
        return False
```

**Step 4: 提交**

```bash
git add backend/apps/crawler/recorder/
git commit -m "feat: 添加录制爬虫配置管理器基础结构"
```

---

## Task 2: 创建任务状态管理器

**Files:**
- Create: `backend/apps/crawler/recorder/task_manager.py`

**Step 1: 创建 task_manager.py**

```python
"""
任务状态管理器 - 负责爬虫任务的暂停、继续、断点续传
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import uuid


class TaskStatus:
    """任务状态常量"""
    PENDING = 'pending'
    RUNNING = 'running'
    PAUSED = 'paused'
    COMPLETED = 'completed'
    FAILED = 'failed'


class TaskManager:
    """任务状态管理器"""

    def __init__(self, status_dir: str = None):
        if status_dir is None:
            base_dir = Path(__file__).parent
            status_dir = base_dir / 'status'
        self.status_dir = Path(status_dir)
        self.status_dir.mkdir(parents=True, exist_ok=True)

    def create_task(self, config_file: str, name: str = None) -> str:
        """创建新任务"""
        task_id = str(uuid.uuid4())[:8]

        task_status = {
            'task_id': task_id,
            'name': name or f'任务_{task_id}',
            'config_file': config_file,
            'status': TaskStatus.PENDING,
            'progress': {
                'current_page': 1,
                'total_pages': 500,
                'items_collected': 0,
                'failed_items': 0
            },
            'timing': {
                'started_at': None,
                'paused_at': None,
                'resumed_at': None,
                'completed_at': None,
                'total_runtime_seconds': 0
            },
            'interval_config': {
                'initial': 2,
                'increment': 1,
                'max': 10,
                'current': 2
            },
            'error_log': [],
            'last_item_index': 0,
            'last_detail_url': None
        }

        self.save_task_status(task_id, task_status)
        return task_id

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        filepath = self.status_dir / f'task_{task_id}.json'
        if not filepath.exists():
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_task_status(self, task_id: str, status: Dict[str, Any]) -> None:
        """保存任务状态"""
        filepath = self.status_dir / f'task_{task_id}.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)

    def update_progress(self, task_id: str, **kwargs) -> None:
        """更新任务进度"""
        status = self.get_task_status(task_id)
        if status:
            status['progress'].update(kwargs)
            self.save_task_status(task_id, status)

    def update_timing(self, task_id: str, **kwargs) -> None:
        """更新时间信息"""
        status = self.get_task_status(task_id)
        if status:
            status['timing'].update(kwargs)
            self.save_task_status(task_id, status)

    def add_error(self, task_id: str, error: Dict[str, Any]) -> None:
        """添加错误日志"""
        status = self.get_task_status(task_id)
        if status:
            status['error_log'].append({
                'timestamp': datetime.now().isoformat() + 'Z',
                **error
            })
            self.save_task_status(task_id, status)

    def start_task(self, task_id: str) -> bool:
        """开始任务"""
        status = self.get_task_status(task_id)
        if status and status['status'] == TaskStatus.PENDING:
            status['status'] = TaskStatus.RUNNING
            status['timing']['started_at'] = datetime.now().isoformat() + 'Z'
            self.save_task_status(task_id, status)
            return True
        return False

    def pause_task(self, task_id: str) -> bool:
        """暂停任务"""
        status = self.get_task_status(task_id)
        if status and status['status'] == TaskStatus.RUNNING:
            status['status'] = TaskStatus.PAUSED
            status['timing']['paused_at'] = datetime.now().isoformat() + 'Z'
            self.save_task_status(task_id, status)
            return True
        return False

    def resume_task(self, task_id: str) -> bool:
        """继续任务"""
        status = self.get_task_status(task_id)
        if status and status['status'] == TaskStatus.PAUSED:
            status['status'] = TaskStatus.RUNNING
            status['timing']['resumed_at'] = datetime.now().isoformat() + 'Z'
            self.save_task_status(task_id, status)
            return True
        return False

    def complete_task(self, task_id: str) -> bool:
        """完成任务"""
        status = self.get_task_status(task_id)
        if status:
            status['status'] = TaskStatus.COMPLETED
            status['timing']['completed_at'] = datetime.now().isoformat() + 'Z'
            self.save_task_status(task_id, status)
            return True
        return False

    def fail_task(self, task_id: str, error_message: str) -> bool:
        """任务失败"""
        status = self.get_task_status(task_id)
        if status:
            status['status'] = TaskStatus.FAILED
            status['timing']['completed_at'] = datetime.now().isoformat() + 'Z'
            status['error_message'] = error_message
            self.save_task_status(task_id, status)
            return True
        return False

    def list_tasks(self) -> list:
        """列出所有任务"""
        tasks = []
        for f in self.status_dir.glob('task_*.json'):
            with open(f, 'r', encoding='utf-8') as file:
                task = json.load(file)
                tasks.append(task)
        return sorted(tasks, key=lambda x: x.get('timing', {}).get('started_at', ''), reverse=True)

    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        filepath = self.status_dir / f'task_{task_id}.json'
        if filepath.exists():
            filepath.unlink()
            return True
        return False
```

**Step 2: 提交**

```bash
git add backend/apps/crawler/recorder/task_manager.py
git commit -m "feat: 添加任务状态管理器"
```

---

## Task 3: 创建 Playwright 录制器核心类

**Files:**
- Create: `backend/apps/crawler/recorder/recorder.py`

**Step 1: 创建 recorder.py**

```python
"""
Playwright 录制器 - 监听用户操作并记录选择器
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Callable, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext


class Recorder:
    """Playwright 录制器"""

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.steps: List[Dict[str, Any]] = []
        self.step_id = 0
        self.is_recording = False

        # 回调函数
        self.on_step_recorded: Optional[Callable] = None
        self.on_data_extracted: Optional[Callable] = None

    async def start(self, url: str = None) -> None:
        """启动录制"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await self.context.new_page()

        # 绑定事件监听
        await self._bind_event_listeners()

        self.is_recording = True
        self.steps = []
        self.step_id = 0

        if url:
            await self.page.goto(url)

    async def _bind_event_listeners(self) -> None:
        """绑定事件监听器"""
        # 点击事件
        self.page.on('click', lambda: None)  # 占位，实际通过 JS 注入

        # 注入录制脚本
        await self.page.evaluate('''
            window.__recorderSteps = [];
            window.__recorderCallback = null;

            // 监听点击
            document.addEventListener('click', function(e) {
                const target = e.target;
                let selector = '';

                // 尝试生成选择器
                if (target.id) {
                    selector = '#' + target.id;
                } else if (target.className && typeof target.className === 'string') {
                    selector = target.tagName.toLowerCase() + '.' + target.className.split(' ').join('.');
                } else {
                    // 使用最近父级的 ID 或类名
                    let path = [];
                    let node = target;
                    while (node && node !== document.body) {
                        let s = node.tagName.toLowerCase();
                        if (node.id) {
                            s += '#' + node.id;
                            path.unshift(s);
                            break;
                        } else if (node.className && typeof node.className === 'string') {
                            s += '.' + node.className.split(' ')[0];
                        }
                        path.unshift(s);
                        node = node.parentElement;
                    }
                    selector = path.join(' > ');
                }

                window.__recorderSteps.push({
                    type: 'click',
                    selector: selector,
                    tagName: target.tagName,
                    text: target.innerText ? target.innerText.substring(0, 50) : ''
                });

                if (window.__recorderCallback) {
                    window.__recorderCallback({
                        type: 'click',
                        selector: selector
                    });
                }
            }, true);

            // 监听滚动
            let lastScroll = 0;
            window.addEventListener('scroll', function() {
                const currentScroll = window.pageYOffset;
                window.__recorderSteps.push({
                    type: 'scroll',
                    distance: currentScroll - lastScroll,
                    position: currentScroll
                });
                lastScroll = currentScroll;
            });

            // 监听输入
            document.addEventListener('input', function(e) {
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                    let selector = '';
                    if (e.target.id) {
                        selector = '#' + e.target.id;
                    } else if (e.target.name) {
                        selector = '[name="' + e.target.name + '"]';
                    } else {
                        selector = e.target.tagName.toLowerCase();
                    }

                    window.__recorderSteps.push({
                        type: 'input',
                        selector: selector,
                        value: e.target.value
                    });
                }
            }, true);
        ''')

    async def get_steps(self) -> List[Dict[str, Any]]:
        """获取录制的步骤"""
        steps = await self.page.evaluate('window.__recorderSteps')
        return steps or []

    async def clear_steps(self) -> None:
        """清空步骤"""
        await self.page.evaluate('window.__recorderSteps = []')
        self.steps = []
        self.step_id = 0

    async def stop(self) -> List[Dict[str, Any]]:
        """停止录制"""
        self.is_recording = False
        steps = await self.get_steps()

        if self.browser:
            await self.browser.close()

        return steps

    async def navigate(self, url: str) -> None:
        """导航到 URL"""
        self.step_id += 1
        step = {
            'id': self.step_id,
            'type': 'navigate',
            'url': url
        }
        self.steps.append(step)
        await self.page.goto(url)

    async def click(self, selector: str) -> None:
        """点击元素"""
        self.step_id += 1
        step = {
            'id': self.step_id,
            'type': 'click',
            'selector': selector
        }
        self.steps.append(step)
        await self.page.click(selector)

    async def wait_for_selector(self, selector: str, timeout: int = 10000) -> None:
        """等待元素出现"""
        self.step_id += 1
        step = {
            'id': self.step_id,
            'type': 'wait',
            'condition': 'selector_visible',
            'target': selector,
            'timeout': timeout
        }
        self.steps.append(step)
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def wait_for_timeout(self, timeout: int) -> None:
        """等待指定时间"""
        self.step_id += 1
        step = {
            'id': self.step_id,
            'type': 'wait',
            'condition': 'timeout',
            'timeout': timeout
        }
        self.steps.append(step)
        await self.page.wait_for_timeout(timeout)

    async def extract_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """提取数据"""
        results = []

        if config.get('type') == 'list':
            # 提取列表数据
            items = await self.page.query_selector_all(config['selector'])

            for idx, item in enumerate(items):
                row = {}
                for field in config.get('fields', []):
                    if field.get('attribute') == 'text':
                        text = await item.text_content()
                        row[field['name']] = text.strip() if text else ''
                    else:
                        el = await item.query_selector(field['selector'])
                        if el:
                            if field.get('attribute') == 'text':
                                text = await el.text_content()
                                row[field['name']] = text.strip() if text else ''
                            else:
                                row[field['name']] = await el.get_attribute(field['attribute'])
                results.append(row)

        return results

    async def screenshot(self, path: str = None) -> bytes:
        """截图"""
        return await self.page.screenshot(path=path)

    @property
    def current_url(self) -> str:
        """当前 URL"""
        return self.page.url if self.page else ''
```

**Step 2: 提交**

```bash
git add backend/apps/crawler/recorder/recorder.py
git commit -m "feat: 添加 Playwright 录制器核心类"
```

---

## Task 4: 创建执行器核心类

**Files:**
- Create: `backend/apps/crawler/recorder/runner.py`

**Step 1: 创建 runner.py**

```python
"""
爬虫执行器 - 读取配置并执行采集任务
"""
import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from playwright.async_api import async_playwright, Browser, Page, BrowserContext

from .task_manager import TaskManager
from .config_manager import ConfigManager


class Runner:
    """爬虫执行器"""

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.task_manager = TaskManager()
        self.config_manager = ConfigManager()

        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        self.config: Dict[str, Any] = {}
        self.status: Dict[str, Any] = {}

        # 回调函数
        self.on_progress: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        self.on_complete: Optional[Callable] = None

        # 控制标志
        self._is_paused = False
        self._should_stop = False

    async def start(self) -> bool:
        """开始执行任务"""
        # 加载配置和状态
        self.status = self.task_manager.get_task_status(self.task_id)
        if not self.status:
            return False

        config_file = self.status.get('config_file')
        self.config = self.config_manager.load_config(config_file)
        if not self.config:
            return False

        # 启动浏览器
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await self.context.new_page()

        # 开始任务
        self.task_manager.start_task(self.task_id)

        try:
            await self._run()
        except Exception as e:
            self.task_manager.fail_task(self.task_id, str(e))
            if self.on_error:
                self.on_error(str(e))
        finally:
            await self._cleanup()

        return True

    async def _run(self) -> None:
        """执行采集主循环"""
        # 获取起始位置
        current_page = self.status['progress']['current_page']
        current_interval = self.status['interval_config']['current']

        # 访问首页
        first_step = next((s for s in self.config.get('steps', []) if s.get('type') == 'navigate'), None)
        if first_step:
            await self.page.goto(first_step['url'])
            await asyncio.sleep(2)

        # 翻页循环
        max_pages = self.config.get('list_config', {}).get('pagination', {}).get('max_pages', 500)

        for page_num in range(current_page, max_pages + 1):
            # 检查暂停
            while self._is_paused:
                await asyncio.sleep(1)

            # 检查停止
            if self._should_stop:
                break

            # 提取列表数据
            list_config = self.config.get('list_config', {})
            items = await self._extract_list(list_config)

            # 遍历每条数据
            for idx, item in enumerate(items):
                # 检查暂停
                while self._is_paused:
                    await asyncio.sleep(1)

                if self._should_stop:
                    break

                # 进入详情页
                detail_url = item.get('url')
                if detail_url:
                    await self._process_detail(detail_url, item)

                    # 更新进度
                    items_collected = self.status['progress']['items_collected'] + 1
                    self.task_manager.update_progress(
                        self.task_id,
                        current_page=page_num,
                        items_collected=items_collected,
                        last_item_index=idx
                    )

                    # 更新间隔
                    current_interval = min(
                        current_interval + 1,
                        self.status['interval_config']['max']
                    )
                    self.status['interval_config']['current'] = current_interval

                    if self.on_progress:
                        self.on_progress(page_num, items_collected)

            # 翻页
            if page_num < max_pages:
                await self._click_next_page(list_config)
                await asyncio.sleep(current_interval)

        # 完成任务
        self.task_manager.complete_task(self.task_id)
        if self.on_complete:
            self.on_complete()

    async def _extract_list(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """提取列表数据"""
        results = []

        item_selector = config.get('item_selector')
        if not item_selector:
            return results

        try:
            items = await self.page.query_selector_all(item_selector)

            for item in items:
                row = {}

                # 提取各字段
                for field in config.get('fields', []):
                    field_name = field.get('name')
                    field_selector = field.get('selector')

                    if field.get('type') == 'attribute':
                        el = await item.query_selector(field_selector)
                        if el:
                            row[field_name] = await el.get_attribute(field.get('attribute', ''))
                    else:
                        # 默认提取文本
                        if field_selector:
                            el = await item.query_selector(field_selector)
                            if el:
                                text = await el.text_content()
                                row[field_name] = text.strip() if text else ''
                        else:
                            text = await item.text_content()
                            row[field_name] = text.strip() if text else ''

                results.append(row)

        except Exception as e:
            self.task_manager.add_error(self.task_id, {
                'page': self.status['progress']['current_page'],
                'error': f'列表提取失败: {str(e)}'
            })

        return results

    async def _process_detail(self, url: str, list_item: Dict[str, Any]) -> None:
        """处理详情页"""
        detail_config = self.config.get('detail_config', {})

        try:
            # 打开新页面访问详情
            detail_page = await self.context.new_page()
            await detail_page.goto(url)
            await detail_page.wait_for_load_state('networkidle')

            # 提取详情数据
            detail_data = {}
            for field in detail_config.get('fields', []):
                field_name = field.get('name')
                field_selector = field.get('selector')

                if field.get('type') == 'list':
                    # 列表字段（如回答列表）
                    items = await detail_page.query_selector_all(field_selector)
                    rows = []
                    for item in items:
                        row = {}
                        for sub_field in field.get('fields', []):
                            sub_name = sub_field.get('name')
                            sub_selector = sub_field.get('selector')

                            el = await item.query_selector(sub_selector)
                            if el:
                                if sub_field.get('attribute') == 'text':
                                    text = await el.text_content()
                                    row[sub_name] = text.strip() if text else ''
                                else:
                                    row[sub_name] = await el.get_attribute(sub_field.get('attribute', ''))
                        rows.append(row)
                    detail_data[field_name] = rows
                else:
                    # 单个字段
                    el = await detail_page.query_selector(field_selector)
                    if el:
                        if field.get('attribute') == 'text':
                            text = await el.text_content()
                            detail_data[field_name] = text.strip() if text else ''
                        else:
                            detail_data[field_name] = await el.get_attribute(field.get('attribute', ''))

            # 保存到数据库（TODO: 调用现有模型）
            await self._save_to_database(list_item, detail_data)

            await detail_page.close()

        except Exception as e:
            self.task_manager.add_error(self.task_id, {
                'page': self.status['progress']['current_page'],
                'error': f'详情页处理失败: {str(e)}',
                'url': url
            })

    async def _save_to_database(self, list_item: Dict, detail_data: Dict) -> None:
        """保存到数据库"""
        # TODO: 实现数据库保存逻辑
        # 使用现有的 Question 和 Answer 模型
        pass

    async def _click_next_page(self, config: Dict[str, Any]) -> bool:
        """点击下一页"""
        pagination = config.get('pagination', {})
        selector = pagination.get('selector')

        if not selector:
            return False

        try:
            await self.page.click(selector)
            await self.page.wait_for_load_state('networkidle')
            return True
        except Exception as e:
            self.task_manager.add_error(self.task_id, {
                'page': self.status['progress']['current_page'],
                'error': f'翻页失败: {str(e)}'
            })
            return False

    async def pause(self) -> None:
        """暂停任务"""
        self._is_paused = True
        self.task_manager.pause_task(self.task_id)

    async def resume(self) -> None:
        """继续任务"""
        self._is_paused = False
        self.task_manager.resume_task(self.task_id)

    async def stop(self) -> None:
        """停止任务"""
        self._should_stop = True
        self._is_paused = False

    async def _cleanup(self) -> None:
        """清理资源"""
        if self.browser:
            await self.browser.close()
```

**Step 2: 提交**

```bash
git add backend/apps/crawler/recorder/runner.py
git commit -m "feat: 添加爬虫执行器核心类"
```

---

## Task 5: 创建 Django API 视图

**Files:**
- Create: `backend/apps/crawler/recorder/views.py`
- Modify: `backend/apps/crawler/urls.py`

**Step 1: 创建 views.py**

```python
"""
录制爬虫 API 视图
"""
import json
import os
from pathlib import Path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from .recorder import Recorder
from .config_manager import ConfigManager
from .task_manager import TaskManager, TaskStatus


recorder = Recorder(headless=False)
config_manager = ConfigManager()
task_manager = TaskManager()


@csrf_exempt
@require_http_methods(["POST"])
def start_recording(request):
    """启动录制"""
    try:
        body = json.loads(request.body)
        url = body.get('url', 'https://wenda.so.com/c/')

        # 启动录制器
        import asyncio
        asyncio.get_event_loop().run_until_complete(recorder.start(url))

        return JsonResponse({
            'code': 0,
            'message': '录制已启动',
            'data': {
                'current_url': recorder.current_url
            }
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': f'启动失败: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def stop_recording(request):
    """停止录制并保存配置"""
    try:
        body = json.loads(request.body)
        name = body.get('name', '未命名配置')

        # 停止录制
        import asyncio
        steps = asyncio.get_event_loop().run_until_complete(recorder.stop())

        # 创建配置
        config = config_manager.create_config(name)
        config['steps'] = steps

        # 保存配置
        filepath = config_manager.save_config(config)

        return JsonResponse({
            'code': 0,
            'message': '录制已保存',
            'data': {
                'config_file': os.path.basename(filepath),
                'steps_count': len(steps)
            }
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': f'保存失败: {str(e)}'
        })


@require_http_methods(["GET"])
def get_recording_steps(request):
    """获取当前录制步骤"""
    try:
        import asyncio
        steps = asyncio.get_event_loop().run_until_complete(recorder.get_steps())

        return JsonResponse({
            'code': 0,
            'data': steps
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })


@require_http_methods(["GET"])
def list_configs(request):
    """列出所有配置"""
    configs = config_manager.list_configs()
    return JsonResponse({
        'code': 0,
        'data': configs
    })


@csrf_exempt
@require_http_methods(["POST"])
def get_config(request):
    """获取指定配置"""
    try:
        body = json.loads(request.body)
        filename = body.get('filename')

        config = config_manager.load_config(filename)
        if config:
            return JsonResponse({
                'code': 0,
                'data': config
            })
        return JsonResponse({
            'code': -1,
            'message': '配置不存在'
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })


@csrf_exempt
@require_http_methods(["POST"])
def delete_config(request):
    """删除配置"""
    try:
        body = json.loads(request.body)
        filename = body.get('filename')

        success = config_manager.delete_config(filename)
        return JsonResponse({
            'code': 0 if success else -1,
            'message': '删除成功' if success else '删除失败'
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })


@csrf_exempt
@require_http_methods(["POST"])
def create_task(request):
    """创建采集任务"""
    try:
        body = json.loads(request.body)
        config_file = body.get('config_file')
        name = body.get('name')

        if not config_file:
            return JsonResponse({
                'code': -1,
                'message': '请选择配置文件'
            })

        task_id = task_manager.create_task(config_file, name)

        return JsonResponse({
            'code': 0,
            'message': '任务创建成功',
            'data': {
                'task_id': task_id
            }
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })


@require_http_methods(["GET"])
def list_tasks(request):
    """列出所有任务"""
    tasks = task_manager.list_tasks()

    # 简化返回数据
    task_list = []
    for task in tasks:
        task_list.append({
            'task_id': task['task_id'],
            'name': task.get('name'),
            'config_file': task['config_file'],
            'status': task['status'],
            'progress': task['progress'],
            'created_at': task.get('timing', {}).get('started_at')
        })

    return JsonResponse({
        'code': 0,
        'data': task_list
    })


@require_http_methods(["GET"])
def get_task_status(request, task_id):
    """获取任务状态"""
    status = task_manager.get_task_status(task_id)

    if status:
        return JsonResponse({
            'code': 0,
            'data': status
        })
    return JsonResponse({
        'code': -1,
        'message': '任务不存在'
    })


@csrf_exempt
@require_http_methods(["POST"])
def start_task(request, task_id):
    """开始执行任务"""
    try:
        # TODO: 启动后台任务执行
        return JsonResponse({
            'code': 0,
            'message': '任务已启动'
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })


@csrf_exempt
@require_http_methods(["POST"])
def pause_task(request, task_id):
    """暂停任务"""
    try:
        task_manager.pause_task(task_id)
        return JsonResponse({
            'code': 0,
            'message': '任务已暂停'
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })


@csrf_exempt
@require_http_methods(["POST"])
def resume_task(request, task_id):
    """继续任务"""
    try:
        task_manager.resume_task(task_id)
        return JsonResponse({
            'code': 0,
            'message': '任务已继续'
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })


@csrf_exempt
@require_http_methods(["POST"])
def stop_task(request, task_id):
    """停止任务"""
    try:
        task_manager.fail_task(task_id, '用户主动停止')
        return JsonResponse({
            'code': 0,
            'message': '任务已停止'
        })
    except Exception as e:
        return JsonResponse({
            'code': -1,
            'message': str(e)
        })
```

**Step 2: 查看并修改 urls.py**

先查看现有的 URL 配置：

```bash
grep -n "path" backend/apps/crawler/urls.py | head -20
```

然后添加新的 URL 路由：

```python
# 在 urlpatterns 中添加
path('recorder/', include('apps.crawler.recorder_urls')),
```

**Step 3: 创建 recorder_urls.py**

```python
"""
录制爬虫 URL 配置
"""
from django.urls import path
from . import views

app_name = 'recorder'

urlpatterns = [
    # 录制相关
    path('start/', views.start_recording, name='start_recording'),
    path('stop/', views.stop_recording, name='stop_recording'),
    path('steps/', views.get_recording_steps, name='get_steps'),

    # 配置管理
    path('configs/', views.list_configs, name='list_configs'),
    path('config/', views.get_config, name='get_config'),
    path('config/delete/', views.delete_config, name='delete_config'),

    # 任务管理
    path('tasks/', views.list_tasks, name='list_tasks'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<str:task_id>/', views.get_task_status, name='get_task_status'),
    path('task/<str:task_id>/start/', views.start_task, name='start_task'),
    path('task/<str:task_id>/pause/', views.pause_task, name='pause_task'),
    path('task/<str:task_id>/resume/', views.resume_task, name='resume_task'),
    path('task/<str:task_id>/stop/', views.stop_task, name='stop_task'),
]
```

**Step 4: 提交**

```bash
git add backend/apps/crawler/recorder/views.py backend/apps/crawler/recorder/urls.py
git commit -m "feat: 添加录制爬虫 Django API 视图"
```

---

## Task 6: 添加数据保存逻辑

**Files:**
- Modify: `backend/apps/crawler/recorder/runner.py`

**Step 1: 修改 runner.py 中的 _save_to_database 方法**

```python
async def _save_to_database(self, list_item: Dict, detail_data: Dict) -> None:
    """保存到数据库"""
    from apps.crawler.models import Question, Answer

    # 从 URL 提取 question_id
    url = detail_data.get('source_url', '')
    import re
    match = re.search(r'/q/(\d+)', url)
    question_id = match.group(1) if match else None

    if not question_id:
        return

    # 创建或更新问题
    question, created = Question.objects.update_or_create(
        question_id=question_id,
        defaults={
            'title': detail_data.get('question_title', list_item.get('title', '')),
            'description': detail_data.get('question_content', ''),
            'category': detail_data.get('category', ''),
            'source_url': url,
            'answer_count': len(detail_data.get('answers', [])),
        }
    )

    # 保存答案
    answers_data = detail_data.get('answers', [])
    for idx, answer_data in enumerate(answers_data, 1):
        Answer.objects.update_or_create(
            question=question,
            source_order=idx,
            defaults={
                'content': answer_data.get('content', ''),
                'answerer': answer_data.get('answerer', ''),
                'answer_time': answer_data.get('time'),  # 需要转换格式
            }
        )
```

**Step 2: 提交**

```bash
git add backend/apps/crawler/recorder/runner.py
git commit -m "feat: 添加数据保存逻辑"
```

---

## Task 7: 创建前端录制管理页面

**Files:**
- Create: `frontend/src/views/crawler/Recorder.vue`

**Step 1: 创建 Recorder.vue**

```vue
<template>
  <div class="recorder-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>录制爬虫</span>
          <el-button type="primary" @click="startRecording" :loading="isRecording" v-if="!isRecording">
            开始录制
          </el-button>
          <el-button type="danger" @click="stopRecording" v-else>
            停止录制
          </el-button>
        </div>
      </template>

      <div class="recorder-content">
        <div class="browser-preview">
          <iframe v-if="iframeUrl" :src="iframeUrl" frameborder="0"></iframe>
          <div v-else class="placeholder">
            <el-empty description="点击"开始录制"启动浏览器" />
          </div>
        </div>

        <div class="steps-panel">
          <h4>录制步骤</h4>
          <el-timeline>
            <el-timeline-item
              v-for="(step, index) in recordedSteps"
              :key="index"
              :timestamp="step.type"
              placement="top"
            >
              <el-card>
                <p><strong>类型:</strong> {{ step.type }}</p>
                <p v-if="step.selector"><strong>选择器:</strong> {{ step.selector }}</p>
                <p v-if="step.url"><strong>URL:</strong> {{ step.url }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-card>

    <!-- 保存配置对话框 -->
    <el-dialog v-model="showSaveDialog" title="保存配置" width="400px">
      <el-form :model="configForm" label-width="80px">
        <el-form-item label="配置名称">
          <el-input v-model="configForm.name" placeholder="请输入配置名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSaveDialog = false">取消</el-button>
        <el-button type="primary" @click="saveConfig">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { startRecording, stopRecording, getRecordingSteps, saveRecording } from '@/api/crawler'

const isRecording = ref(false)
const iframeUrl = ref('')
const recordedSteps = ref([])
const showSaveDialog = ref(false)
const configForm = ref({ name: '' })
let pollTimer = null

const startRecord = async () => {
  try {
    const res = await startRecording()
    if (res.code === 0) {
      isRecording.value = true
      iframeUrl.value = res.data.current_url
      ElMessage.success('录制已启动')

      // 开始轮询步骤
      pollTimer = setInterval(fetchSteps, 2000)
    }
  } catch (error) {
    ElMessage.error('启动失败')
  }
}

const stopRecord = async () => {
  try {
    const res = await stopRecording()
    if (res.code === 0) {
      isRecording.value = false
      clearInterval(pollTimer)
      showSaveDialog.value = true
      ElMessage.success('录制已停止')
    }
  } catch (error) {
    ElMessage.error('停止失败')
  }
}

const fetchSteps = async () => {
  try {
    const res = await getRecordingSteps()
    if (res.code === 0) {
      recordedSteps.value = res.data
    }
  } catch (error) {
    // 忽略轮询错误
  }
}

const saveConfig = async () => {
  try {
    const res = await saveRecording({ name: configForm.value.name })
    if (res.code === 0) {
      ElMessage.success('配置已保存')
      showSaveDialog.value = false
      configForm.value.name = ''
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
  }
})
</script>

<style scoped>
.recorder-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.recorder-content {
  display: flex;
  gap: 20px;
}

.browser-preview {
  flex: 1;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.browser-preview iframe {
  width: 100%;
  height: 100%;
}

.placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.steps-panel {
  width: 350px;
  max-height: 600px;
  overflow-y: auto;
}
</style>
```

**Step 2: 创建 API 接口文件**

```javascript
// frontend/src/api/crawler.js

import request from '@/utils/request'

export function startRecording(data) {
  return request({
    url: '/api/crawler/recorder/start/',
    method: 'post',
    data
  })
}

export function stopRecording(data) {
  return request({
    url: '/api/crawler/recorder/stop/',
    method: 'post',
    data
  })
}

export function getRecordingSteps() {
  return request({
    url: '/api/crawler/recorder/steps/',
    method: 'get'
  })
}

export function saveRecording(data) {
  return request({
    url: '/api/crawler/recorder/stop/',
    method: 'post',
    data
  })
}

export function listConfigs() {
  return request({
    url: '/api/crawler/recorder/configs/',
    method: 'get'
  })
}

export function listTasks() {
  return request({
    url: '/api/crawler/recorder/tasks/',
    method: 'get'
  })
}

export function createTask(data) {
  return request({
    url: '/api/crawler/recorder/task/create/',
    method: 'post',
    data
  })
}

export function getTaskStatus(taskId) {
  return request({
    url: `/api/crawler/recorder/task/${taskId}/`,
    method: 'get'
  })
}

export function startTask(taskId) {
  return request({
    url: `/api/crawler/recorder/task/${taskId}/start/`,
    method: 'post'
  })
}

export function pauseTask(taskId) {
  return request({
    url: `/api/crawler/recorder/task/${taskId}/pause/`,
    method: 'post'
  })
}

export function resumeTask(taskId) {
  return request({
    url: `/api/crawler/recorder/task/${taskId}/resume/`,
    method: 'post'
  })
}

export function stopTask(taskId) {
  return request({
    url: `/api/crawler/recorder/task/${taskId}/stop/`,
    method: 'post'
  })
}
```

**Step 3: 提交**

```bash
git add frontend/src/views/crawler/Recorder.vue frontend/src/api/crawler.js
git commit -m "feat: 添加前端录制管理页面"
```

---

## Task 8: 创建任务管理页面

**Files:**
- Create: `frontend/src/views/crawler/TaskManager.vue`

**Step 1: 创建 TaskManager.vue**

```vue
<template>
  <div class="task-manager">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>采集任务</span>
          <el-button type="primary" @click="showCreateDialog = true">
            创建任务
          </el-button>
        </div>
      </template>

      <el-table :data="tasks" v-loading="loading">
        <el-table-column prop="task_id" label="任务ID" width="100" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="config_file" label="配置文件" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="进度" width="200">
          <template #default="{ row }">
            <el-progress
              :percentage="getProgressPercent(row.progress)"
              :status="row.progress.failed_items > 0 ? 'exception' : ''"
            />
            <span class="progress-text">
              {{ row.progress.items_collected }} / {{ row.progress.total_pages * 20 }} 条
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="primary"
              size="small"
              @click="startTask(row.task_id)"
            >
              开始
            </el-button>
            <el-button
              v-if="row.status === 'running'"
              type="warning"
              size="small"
              @click="pauseTask(row.task_id)"
            >
              暂停
            </el-button>
            <el-button
              v-if="row.status === 'paused'"
              type="success"
              size="small"
              @click="resumeTask(row.task_id)"
            >
              继续
            </el-button>
            <el-button
              v-if="row.status === 'running' || row.status === 'paused'"
              type="danger"
              size="small"
              @click="stopTask(row.task_id)"
            >
              停止
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建任务对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建采集任务" width="400px">
      <el-form :model="taskForm" label-width="80px">
        <el-form-item label="任务名称">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="配置文件">
          <el-select v-model="taskForm.config_file" placeholder="请选择配置文件">
            <el-option
              v-for="config in configs"
              :key="config.filename"
              :label="config.filename"
              :value="config.filename"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createTask">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listTasks, listConfigs, createTask, startTask, pauseTask, resumeTask, stopTask } from '@/api/crawler'

const loading = ref(false)
const tasks = ref([])
const configs = ref([])
const showCreateDialog = ref(false)
const taskForm = ref({ name: '', config_file: '' })

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await listTasks()
    if (res.code === 0) {
      tasks.value = res.data
    }
  } finally {
    loading.value = false
  }
}

const fetchConfigs = async () => {
  const res = await listConfigs()
  if (res.code === 0) {
    configs.value = res.data
  }
}

const handleCreateTask = async () => {
  if (!taskForm.value.config_file) {
    ElMessage.warning('请选择配置文件')
    return
  }

  const res = await createTask(taskForm.value)
  if (res.code === 0) {
    ElMessage.success('任务创建成功')
    showCreateDialog.value = false
    taskForm.value = { name: '', config_file: '' }
    fetchTasks()
  }
}

const getStatusType = (status) => {
  const types = {
    pending: 'info',
    running: 'primary',
    paused: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待执行',
    running: '运行中',
    paused: '已暂停',
    completed: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}

const getProgressPercent = (progress) => {
  const total = progress.total_pages * 20
  if (total === 0) return 0
  return Math.round((progress.items_collected / total) * 100)
}

const handleStartTask = async (taskId) => {
  const res = await startTask(taskId)
  if (res.code === 0) {
    ElMessage.success('任务已启动')
    fetchTasks()
  }
}

const handlePauseTask = async (taskId) => {
  const res = await pauseTask(taskId)
  if (res.code === 0) {
    ElMessage.success('任务已暂停')
    fetchTasks()
  }
}

const handleResumeTask = async (taskId) => {
  const res = await resumeTask(taskId)
  if (res.code === 0) {
    ElMessage.success('任务已继续')
    fetchTasks()
  }
}

const handleStopTask = async (taskId) => {
  const res = await stopTask(taskId)
  if (res.code === 0) {
    ElMessage.success('任务已停止')
    fetchTasks()
  }
}

onMounted(() => {
  fetchTasks()
  fetchConfigs()
})
</script>

<style scoped>
.task-manager {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-text {
  font-size: 12px;
  color: #666;
}
</style>
```

**Step 2: 提交**

```bash
git add frontend/src/views/crawler/TaskManager.vue
git commit -m "feat: 添加任务管理页面"
```

---

## Task 9: 添加路由配置

**Files:**
- Modify: `frontend/src/router/index.js`

**Step 1: 添加路由**

```javascript
{
  path: '/crawler/recorder',
  name: 'Recorder',
  component: () => import('@/views/crawler/Recorder.vue'),
  meta: { title: '录制爬虫' }
},
{
  path: '/crawler/tasks',
  name: 'TaskManager',
  component: () => import('@/views/crawler/TaskManager.vue'),
  meta: { title: '任务管理' }
}
```

**Step 2: 提交**

```bash
git add frontend/src/router/index.js
git commit -m "feat: 添加录制爬虫路由配置"
```

---

## Task 10: 优化录制选择器生成

**Files:**
- Modify: `backend/apps/crawler/recorder/recorder.py`

**Step 1: 优化选择器生成逻辑**

```python
async def _bind_event_listeners(self) -> None:
    """绑定事件监听器 - 优化版"""
    await self.page.evaluate('''
        window.__recorderSteps = [];

        // 生成唯一选择器
        function generateSelector(element) {
            if (element.id) {
                return '#' + element.id;
            }

            // 尝试使用 data-* 属性
            for (const attr of element.attributes) {
                ifWith('data- (attr.name.starts') || attr.name === 'class') {
                    const selector = element.tagName.toLowerCase() + '[' + attr.name + '="' + attr.value + '"]';
                    if (document.querySelectorAll(selector).length === 1) {
                        return selector;
                    }
                }
            }

            // 回退到路径选择器
            let path = [];
            let node = element;
            while (node && node !== document.body) {
                let s = node.tagName.toLowerCase();
                if (node.id) {
                    s += '#' + node.id;
                    path.unshift(s);
                    break;
                } else if (node.className && typeof node.className === 'string' && node.className.trim()) {
                    const classes = node.className.trim().split(/\\s+/).slice(0, 2).join('.');
                    if (classes) {
                        s += '.' + classes;
                    }
                }
                // 添加 nth-child 以区分同类型兄弟元素
                const parent = node.parentElement;
                if (parent) {
                    const siblings = Array.from(parent.children).filter(el => el.tagName === node.tagName);
                    if (siblings.length > 1) {
                        const index = siblings.indexOf(node) + 1;
                        s += ':nth-child(' + index + ')';
                    }
                }
                path.unshift(s);
                node = node.parentElement;
            }
            return path.join(' > ');
        }

        // 监听点击
        document.addEventListener('click', function(e) {
            const selector = generateSelector(e.target);
            const text = e.target.innerText ? e.target.innerText.substring(0, 30).trim() : '';

            window.__recorderSteps.push({
                type: 'click',
                selector: selector,
                tagName: e.target.tagName,
                text: text,
                timestamp: new Date().toISOString()
            });
        }, true);

        // 监听滚动
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(function() {
                window.__recorderSteps.push({
                    type: 'scroll',
                    position: window.pageYOffset,
                    timestamp: new Date().toISOString()
                });
            }, 300);
        });
    ''')
```

**Step 2: 提交**

```bash
git add backend/apps/crawler/recorder/recorder.py
git commit -m "feat: 优化录制选择器生成逻辑"
```

---

## Task 11: 添加配置编辑功能

**Files:**
- Create: `backend/apps/crawler/recorder/config_editor.py`

**Step 1: 创建配置编辑器**

```python
"""
配置编辑器 - 手动编辑和调整录制配置
"""
import json
from typing import Dict, Any, List, Optional


class ConfigEditor:
    """配置编辑器"""

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def load_config(self, filename: str) -> Optional[Dict[str, Any]]:
        """加载配置"""
        return self.config_manager.load_config(filename)

    def save_config(self, config: Dict[str, Any], filename: str) -> str:
        """保存配置"""
        return self.config_manager.save_config(config, filename)

    def add_list_config(self, config: Dict[str, Any],
                        item_selector: str,
                        fields: List[Dict[str, Any]],
                        pagination_selector: str = None,
                        max_pages: int = 500) -> Dict[str, Any]:
        """添加列表提取配置"""
        config['list_config'] = {
            'item_selector': item_selector,
            'fields': fields,
            'pagination': {
                'type': 'click',
                'selector': pagination_selector or '',
                'max_pages': max_pages
            }
        }
        return config

    def add_detail_config(self, config: Dict[str, Any],
                          entry_selector: str,
                          fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """添加详情页配置"""
        config['detail_config'] = {
            'entry': {
                'type': 'click',
                'selector': entry_selector
            },
            'fields': fields
        }
        return config

    def add_field(self, config: Dict[str, Any],
                  field_config: Dict[str, Any],
                  is_list: bool = False,
                  parent_selector: str = None) -> Dict[str, Any]:
        """添加字段配置"""
        target = config.get('detail_config', {}).get('fields', [])

        field = {
            'name': field_config.get('name'),
            'selector': field_config.get('selector'),
            'attribute': field_config.get('attribute', 'text')
        }

        if is_list:
            field['type'] = 'list'
            field['fields'] = field_config.get('sub_fields', [])

        target.append(field)

        if 'detail_config' not in config:
            config['detail_config'] = {'fields': []}
        config['detail_config']['fields'] = target

        return config

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """验证配置"""
        errors = []

        # 检查必要字段
        if not config.get('name'):
            errors.append('配置名称不能为空')

        if 'list_config' not in config:
            errors.append('缺少列表配置')
        else:
            list_config = config['list_config']
            if not list_config.get('item_selector'):
                errors.append('列表选择器不能为空')

        if 'detail_config' not in config:
            errors.append('缺少详情页配置')
        else:
            detail_config = config['detail_config']
            if not detail_config.get('entry', {}).get('selector'):
                errors.append('详情页入口选择器不能为空')

        return errors

    def generate_default_config(self, name: str = '360问答采集') -> Dict[str, Any]:
        """生成默认配置模板"""
        return {
            'version': '1.0',
            'name': name,
            'created_at': '',
            'steps': [],
            'list_config': {
                'item_selector': 'ul.question-list li',
                'fields': [
                    {
                        'name': 'title',
                        'selector': 'a[target="_blank"]',
                        'attribute': 'text'
                    },
                    {
                        'name': 'url',
                        'selector': 'a[target="_blank"]',
                        'attribute': 'href'
                    },
                    {
                        'name': 'answer_count',
                        'selector': '::attr(data-ans)',
                        'attribute': 'value'
                    }
                ],
                'pagination': {
                    'type': 'click',
                    'selector': '.next',
                    'max_pages': 500
                }
            },
            'detail_config': {
                'entry': {
                    'type': 'click',
                    'selector': 'a[target="_blank"]'
                },
                'fields': [
                    {
                        'name': 'question_title',
                        'selector': 'h1.title',
                        'attribute': 'text'
                    },
                    {
                        'name': 'question_content',
                        'selector': '.question-content',
                        'attribute': 'text'
                    },
                    {
                        'name': 'answers',
                        'selector': '.answer-item',
                        'type': 'list',
                        'fields': [
                            {
                                'name': 'content',
                                'selector': '.answer-content',
                                'attribute': 'text'
                            },
                            {
                                'name': 'answerer',
                                'selector': '.answerer-name',
                                'attribute': 'text'
                            },
                            {
                                'name': 'time',
                                'selector': '.answer-time',
                                'attribute': 'text'
                            }
                        ]
                    },
                    {
                        'name': 'category',
                        'selector': '.category-tag',
                        'attribute': 'text'
                    },
                    {
                        'name': 'tags',
                        'selector': '.tag-list span',
                        'attribute': 'text',
                        'type': 'list'
                    }
                ]
            }
        }
```

**Step 2: 提交**

```bash
git add backend/apps/crawler/recorder/config_editor.py
git commit -m "feat: 添加配置编辑器"
```

---

## Task 12: 完善错误处理和重试机制

**Files:**
- Modify: `backend/apps/crawler/recorder/runner.py`

**Step 1: 添加重试机制**

```python
class Runner:
    # ... 现有代码 ...

    async def _click_with_retry(self, selector: str, max_retries: int = 3) -> bool:
        """带重试的点击"""
        for attempt in range(max_retries):
            try:
                await self.page.click(selector)
                return True
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # 指数退避
                    continue
                else:
                    self.task_manager.add_error(self.task_id, {
                        'page': self.status['progress']['current_page'],
                        'error': f'点击失败 (重试{max_retries}次): {str(e)}',
                        'selector': selector
                    })
                    return False
        return False

    async def _extract_with_retry(self, selector: str, max_retries: int = 2) -> Optional[Any]:
        """带重试的数据提取"""
        for attempt in range(max_retries):
            try:
                element = await self.page.query_selector(selector)
                if element:
                    return await element.text_content()
                return None
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                return None
        return None

    async def _detect_anti_crawler(self) -> bool:
        """检测反爬措施"""
        # 检测验证码
        captcha_selectors = ['#captcha', '.captcha', '[class*="captcha"]', '#verify']
        for selector in captcha_selectors:
            element = await self.page.query_selector(selector)
            if element:
                return True

        # 检测 403/429 状态
        if self.page.url in ['403', '429']:
            return True

        # 检测页面内容异常
        text = await self.page.text_content('body') or ''
        if '访问频率过高' in text or '请稍后再试' in text:
            return True

        return False
```

**Step 2: 修改主循环添加错误处理**

```python
async def _run(self) -> None:
    # ... 现有代码 ...

    for page_num in range(current_page, max_pages + 1):
        # 检查暂停
        while self._is_paused:
            await asyncio.sleep(1)

        if self._should_stop:
            break

        # 检测反爬
        if await self._detect_anti_crawler():
            self.task_manager.add_error(self.task_id, {
                'page': page_num,
                'error': '检测到反爬措施，暂停任务'
            })
            await self.pause()
            # 可以在这里添加自动恢复逻辑
            await asyncio.sleep(300)  # 等待 5 分钟后自动继续
            await self.resume()
            continue

        # ... 其余代码 ...
```

**Step 3: 提交**

```bash
git add backend/apps/crawler/recorder/runner.py
git commit -m "feat: 添加错误处理和重试机制"
```

---

## 实施完成总结

以上 12 个任务完成了录制爬虫系统的核心功能：

1. **配置管理器** - JSON 配置的创建、保存、加载
2. **任务管理器** - 任务状态、暂停/继续、断点续传
3. **录制器** - Playwright 监听用户操作、记录选择器
4. **执行器** - 读取配置、执行采集、智能间隔
5. **Django API** - REST 接口
6. **数据保存** - 存入现有 Question/Answer 模型
7. **前端页面** - 录制和任务管理界面
8. **配置编辑** - 手动调整配置
9. **错误处理** - 重试机制、反爬检测

---

**Plan complete and saved to `docs/plans/2026-02-28-recorder-crawler-plan.md`. Two execution options:**

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration
2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
