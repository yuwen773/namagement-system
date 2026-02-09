# 爬虫模块说明文档

## 1. 模块概述

爬虫模块位于 `backend/apps/crawler/`，负责从 360问答 (wenda.so.com) 采集问答数据。采用 **Scrapy + Playwright + Celery** 技术栈，支持异步任务调度、断点续传和数据清洗。

### 目录结构

```
crawler/
├── models.py          # Tag / Question 数据模型
├── tasks.py           # Celery 异步任务
├── spiders/
│   ├── wenda_spider.py      # 混合模式爬虫
│   └── wenda_api_spider.py  # 纯API模式爬虫
├── pipelines.py       # 数据处理管道
├── utils.py           # DataCleaner / DuplicateChecker
├── settings.py        # Scrapy 配置
├── items.py           # QuestionItem 定义
└── views.py           # API 视图
```

---

## 2. 数据模型

### Tag (标签模型)

| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField(50) | 标签名，唯一 |
| created_at | DateTimeField | 创建时间 |

### Question (问答模型)

| 字段 | 类型 | 说明 |
|------|------|------|
| title | CharField(255) | 问题标题 |
| description | TextField | 问题描述 |
| answer_content | TextField | 回答内容 |
| answer_time | DateTimeField | 回答时间 |
| answerer | CharField(100) | 回答者 |
| tags | ManyToManyField | 关联标签 |
| source_url | URLField | 来源链接(唯一) |
| created_at / updated_at | DateTimeField | 入库/更新时间 |

---

## 3. 两种爬虫模式对比

### WendaSpider (混合模式) - `wenda_spider.py`

**特点**: 优先使用 API，API 失效时自动降级为 Playwright

```
启动流程:
    start_requests()
        ↓
    [优先] JsonRequest → parse_api()
        ↓
    [成功] 解析JSON数据 → yield QuestionItem
        ↓
    [失败] errback → fallback_to_playwright()
        ↓
    [降级] Request + PageMethod → parse_playwright()
        ↓
    解析HTML → yield QuestionItem
```

**配置特点**:
- `DOWNLOAD_DELAY`: 3秒
- `CONCURRENT_REQUESTS`: 1
- `AUTOTHROTTLE_ENABLED`: True
- `PLAYWRIGHT_LAUNCH_OPTIONS`: headless=True

### WendaAPISpider (纯API模式) - `wenda_api_spider.py`

**特点**: 直接调用 JSON API，无需浏览器渲染

**配置特点**:
- `DOWNLOAD_DELAY`: 2秒
- `CONCURRENT_REQUESTS`: 2
- `FEEDS`: 输出到 `output.jsonlines`
- 无 Playwright 依赖

### 对比总结

| 特性 | WendaSpider (混合) | WendaAPISpider (纯API) |
|------|-------------------|------------------------|
| 依赖 | Scrapy + Playwright | 仅 Scrapy |
| 速度 | 较慢(浏览器渲染) | 快(直接API) |
| 稳定性 | 高(自动降级) | 依赖API可用性 |
| 适用场景 | API不稳定时 | 大规模采集 |
| 反爬能力 | 强(JS渲染) | 较弱 |

---

## 4. Celery 任务流程

### 任务列表 (`tasks.py`)

| 任务函数 | 功能 |
|---------|------|
| `run_spider_task(mode, limit, resume, api_only)` | 启动爬虫，初始化状态，执行采集 |
| `get_task_status(task_id)` | 获取任务当前状态 |
| `get_task_progress(task_id)` | 获取进度详情 (collected, failed, page) |
| `get_task_logs(task_id)` | 获取错误日志 |
| `get_resume_info(mode)` | 获取断点信息 (last_page, last_id) |
| `stop_spider(task_id)` | 终止任务 |
| `cleanup_expired_tasks()` | 清理过期任务 (TTL < 1小时) |

### run_spider_task 执行流程

```python
def run_spider_task(self, mode='demo', limit=20, resume=False, api_only=False):
    # 1. 初始化任务状态到 Redis
    initial_status = {
        'task_id': task_id,
        'mode': mode,
        'limit': limit,
        'status': 'running',
        'progress': 0,
        'collected': 0,
        'failed': 0,
        'start_time': timezone.now().isoformat(),
        'message': '任务启动中...',
    }
    redis_client.setex(status_key, 86400, json.dumps(initial_status))

    # 2. 构造 Scrapy 命令 (内嵌 Python 脚本)
    cmd_args = [
        sys.executable,
        '-c',
        '''
        # 动态选择爬虫类
        if api_only:
            from apps.crawler.spiders import WendaAPISpider
        else:
            from apps.crawler.spiders import WendaSpider

        # 创建 CrawlerProcess
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(CustomSpider, mode=mode, limit=limit, resume=resume)
        process.start()
        '''
    ]

    # 3. 执行爬虫 (subprocess.run, timeout=3600)
    result = subprocess.run(cmd_args, capture_output=True, timeout=3600)

    # 4. 更新最终状态
    final_status = {
        'status': 'completed' if result.returncode == 0 else 'failed',
        'collected': collected,
        'end_time': timezone.now().isoformat(),
    }

    return final_status
```

---

## 5. 断点续传机制

### Redis Key 设计

```
Key 格式: qa_crawler:{type}:{identifier}

qa_crawler:progress:{task_id}  → 任务进度
qa_crawler:status:{task_id}    → 任务状态
qa_crawler:resume:{mode}       → 断点信息
qa_crawler:{spider}:stats      → 爬虫统计
```

### 断点存储 (`wenda_spider.py`)

```python
class WendaSpider(scrapy.Spider):
    def __init__(self, ...):
        self.redis_key_prefix = 'crawler:wenda:'

    def _get_redis(self, key: str, default: Any = None) -> Any:
        """从 Redis 读取断点"""
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        value = r.get(f"{self.redis_key_prefix}{key}")
        return int(value) if value else default

    def _save_redis(self, key: str, value: Any) -> None:
        """保存断点到 Redis"""
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        r.set(f"{self.redis_key_prefix}{key}", str(value))
```

### 断点续传流程

```
1. 任务启动时:
   start_requests()
   → _get_redis('last_page', 1)  读取断点页码
   → _get_redis('last_id', '')   读取断点ID

2. 采集过程中:
   每页采集完成
   → _save_redis('last_page', page + 1)  保存下一页页码

3. 任务中断/重启时:
   → 从 Redis 读取 last_page
   → 从该页继续采集

4. 爬虫关闭时 (closed):
   → 保存最终统计到 Redis Hash
   → 记录 finish_time 和采集模式
```

---

## 6. 数据清洗流程

### Pipeline 架构 (`pipelines.py`)

```
process_item(item)
    │
    ├─ 1. DataCleaner.clean_item()
    │     ├─ clean_html()  → 移除HTML标签
    │     ├─ normalize_text() → 文本规范化
    │     └─ truncate_text() → 字段截断
    │
    ├─ 2. validate_data() → 验证必填字段
    │
    ├─ 3. DuplicateChecker.is_duplicate()
    │     └─ 检查 title/source_url 是否重复
    │
    ├─ 4. 添加到缓冲池 (BATCH_SIZE = 100)
    │
    └─ 5. _flush_buffer() → 批量入库
          └─ _batch_insert() → Django ORM 批量写入
```

### DataCleaner 核心方法 (`utils.py`)

```python
class DataCleaner:
    def clean_html(self, text: str) -> str:
        """移除 HTML 标签"""
        text = unescape(text)        # HTML 实体转义
        text = self.HTML_TAG_PATTERN.sub('', text)  # 移除标签
        return text.strip()

    def normalize_text(self, text: str) -> str:
        """文本规范化"""
        # 替换 HTML 实体
        for entity, char in self.HTML_ENTITIES.items():
            text = text.replace(entity, char)
        # 合并多余空格
        text = re.sub(r'[ \t]+', ' ', text)
        # 合并多余换行
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()

    def clean_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """完整清洗流程"""
        cleaned = {}
        for key, value in item.items():
            if key in ['title', 'description', 'answer_content', 'answerer']:
                value = self.clean_html(value)
                value = self.normalize_text(value)
                if key in self.MAX_LENGTHS:
                    value = self.truncate_text(value, self.MAX_LENGTHS[key])
            cleaned[key] = value
        return cleaned
```

---

## 7. API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/crawler/start/` | POST | 启动爬虫任务 |
| `/api/crawler/status/<task_id>/` | GET | 获取任务状态 |
| `/api/crawler/progress/<task_id>/` | GET | 获取任务进度 |
| `/api/crawler/logs/<task_id>/` | GET | 获取任务日志 |
| `/api/crawler/resume/` | GET | 获取断点信息 |
| `/api/crawler/stop/<task_id>/` | POST | 停止爬虫 |
| `/api/crawler/cleanup/` | POST | 清理过期任务 |

### 使用示例

```javascript
// 启动爬虫
POST /api/crawler/start/
{
  "mode": "full",      // demo 或 full
  "limit": 100,        // 采集数量限制
  "api_only": false,   // 是否纯API模式
  "resume": false      // 是否断点续传
}

// 查询进度
GET /api/crawler/progress/{task_id}/
// 返回: { "timestamp": "...", "current_page": 5, "collected": 87, "failed": 2 }
```

---

## 8. 配置项 (`settings.py`)

```python
# 请求控制
DOWNLOAD_DELAY = 3           # 请求间隔(秒)
CONCURRENT_REQUESTS = 1      # 并发数
AUTOTHROTTLE_ENABLED = True  # 自动限速

# 重试配置
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 反爬配置
USER_AGENT_ROTATE = True     # UA轮换
USER_AGENT_LIST = [...]      # UA列表

# Pipeline 配置
ITEM_PIPELINES = {
    'apps.crawler.pipelines.DuplicateFilterPipeline': 100,
    'apps.crawler.pipelines.DataValidationPipeline': 200,
    'apps.crawler.pipelines.QuestionPipeline': 300,
}
```

---

## 9. 关键文件路径

| 文件 | 路径 |
|------|------|
| models.py | `backend/apps/crawler/models.py` |
| tasks.py | `backend/apps/crawler/tasks.py` |
| WendaSpider | `backend/apps/crawler/spiders/wenda_spider.py` |
| WendaAPISpider | `backend/apps/crawler/spiders/wenda_api_spider.py` |
| pipelines.py | `backend/apps/crawler/pipelines.py` |
| utils.py | `backend/apps/crawler/utils.py` |
| settings.py | `backend/apps/crawler/settings.py` |
| items.py | `backend/apps/crawler/items.py` |
