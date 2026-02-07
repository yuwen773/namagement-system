# 系统架构

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5.2 + DRF |
| 数据库 | MySQL 8.0 (3307) |
| 任务队列 | Celery + Redis |
| 前端 | Vue 3 + Element Plus + ECharts |
| 爬虫 | Scrapy + Playwright |

## 数据库模型

### Question (问答)
| 字段 | 类型 | 说明 |
|------|------|------|
| title | CharField(255) | 问题标题 |
| description | TextField | 问题描述 |
| answer_content | TextField | 回答内容 |
| answer_time | DateTimeField | 回答时间 |
| answerer | CharField(100) | 回答者 |
| source_url | URLField(255) | 来源链接（唯一） |
| tags | ManyToManyField | 关联标签 |
| created_at | DateTimeField | 入库时间 |

### Tag (标签)
| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField(50) | 标签名（唯一） |

**索引**: title, created_at, answerer, source_url

## 文件结构

```
backend/
├── manage.py
├── qa_project/
│   ├── settings.py     # Django 配置（含 Celery 配置）
│   ├── urls.py        # 路由
│   ├── exceptions.py   # 统一异常处理
│   └── celery.py       # Celery 应用配置
├── apps/
│   ├── accounts/       # 用户认证模块
│   │   ├── models.py   # User 模型
│   │   ├── views.py   # 认证视图
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── crawler/       # 爬虫模块
│   │   ├── models.py  # Tag, Question 模型
│   │   ├── items.py   # Scrapy Item 定义
│   │   ├── utils.py   # DataCleaner, DuplicateChecker
│   │   ├── pipelines.py # QuestionPipeline 数据处理管道
│   │   ├── settings.py # Scrapy 配置
│   │   ├── tasks.py   # Celery 爬虫任务
│   │   ├── spiders/   # 爬虫模块
│   │   │   ├── __init__.py
│   │   │   ├── wenda_spider.py      # 混合模式爬虫
│   │   │   └── wenda_api_spider.py  # 纯 API 模式爬虫
│   │   └── apps.py
│   └── api/           # 数据API
├── crawl.py           # 爬虫启动脚本
├── requirements.txt   # 依赖清单
└── test_celery.py    # Celery 配置测试脚本
```

## 用户角色

| 角色 | 权限 |
|------|------|
| admin | 所有权限 |
| user | 查看、搜索 |

---

## 爬虫模块详细说明

### 文件作用

#### `items.py` - 数据结构定义
定义 Scrapy Item，对应 Django Question 模型：
- **QuestionItem**: 爬虫采集的数据结构
- **create_question_item()**: 便捷工厂函数

#### `utils.py` - 数据清洗工具
提供数据清洗功能：
- **DataCleaner**: HTML 标签移除、文本规范化、验证
- **DuplicateChecker**: 重复数据检测
- **clean_html() / normalize_text()**: 便捷函数

#### `pipelines.py` - 数据处理管道
集成到 Scrapy Pipeline：
- **QuestionPipeline**: 主管道，批量入库
- **DuplicateFilterPipeline**: 重复过滤
- **DataValidationPipeline**: 数据验证

#### `settings.py` - Scrapy 配置
爬虫运行参数：
- User-Agent 轮换列表
- 下载延迟（3-8秒随机）
- 自动限速（Autothrottle）
- 代理轮换配置
- Playwright 设置

#### `spiders/wenda_spider.py` - 混合模式爬虫
核心爬虫逻辑：
- **优先模式**: JSON API 请求（高效）
- **降级模式**: Playwright 浏览器渲染（反爬对抗）
- **断点续传**: Redis 存储采集进度
- **反爬机制**: UA轮换、延迟、重试

#### `spiders/wenda_api_spider.py` - 纯 API 爬虫
备用爬虫，无需浏览器：
- 直接调用目标 API
- 适合网络环境无法安装 Playwright 时使用
- 采集效率更高

#### `crawl.py` - 启动脚本
提供命令行接口：
- `python crawl.py --mode demo` (演示20条)
- `python crawl.py --mode full --limit 10000` (全量采集)

### 数据流向

```
请求目标网站
    ↓
[JSON API] 或 [Playwright 渲染]
    ↓
parse() 解析响应
    ↓
Item 发送到 Pipeline
    ↓
QuestionPipeline.process_item()
    ↓
DataCleaner 清洗数据
    ↓
DuplicateChecker 过滤重复
    ↓
批量写入 MySQL (每100条)
    ↓
Tag 关联处理
```

### 采集模式对比

| 模式 | 优点 | 缺点 |
|------|------|------|
| JSON API | 速度快10倍、资源占用低 | 容易被封、无JS渲染 |
| Playwright | 可执行JS、绕过简单反爬 | 速度慢、资源占用高 |
| 混合模式 | 优先API、失效降级 | 实现复杂 |

---

## Celery 异步任务模块

### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      Django Views                           │
│                  (前端 API 调用入口)                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Celery Tasks                              │
│                   (apps/crawler/tasks.py)                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │ run_spider_task │  │ get_task_status │  │stop_spider │  │
│  └────────┬────────┘  └────────┬────────┘  └─────┬──────┘  │
└───────────┼────────────────────┼────────────────┼─────────┘
            │                    │                │
            ▼                    ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Redis                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────┐ │
│  │ Broker        │  │ Task Status   │  │ Progress       │ │
│  │ (消息队列)    │  │ (qa_crawler:  │  │ (qa_crawler:   │ │
│  │ :6379/0      │  │  status:{id}) │  │  progress:{id})│ │
│  └───────────────┘  └───────────────┘  └────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
│  Celery Worker  │ │   Scrapy    │ │   Django ORM    │
│  (任务执行)     │ │  (爬虫采集)  │ │   (数据入库)    │
└─────────────────┘ └─────────────┘ └─────────────────┘
```

### 文件作用

#### `qa_project/celery.py` - Celery 应用配置
Celery 应用的主入口和配置中心：
- **Celery 实例创建**：创建并配置 `Celery('qa_project')` 实例
- **配置加载**：从 Django settings 自动加载 Celery 配置
- **任务自动发现**：`app.autodiscover_tasks()` 自动发现所有 registered tasks
- **定时任务配置**：Celery Beat 定时清理过期任务
- **任务序列化**：JSON 序列化，配置重试策略

#### `apps/crawler/tasks.py` - Celery 任务模块
核心任务定义和状态管理：

| 任务函数 | 作用 |
|---------|------|
| `run_spider_task(mode, limit, resume, api_only)` | 主爬虫任务，支持演示/全量模式 |
| `get_task_status(task_id)` | 查询任务当前状态（running/completed/failed） |
| `get_task_progress(task_id)` | 查询详细进度（已采数、页数、失败数） |
| `get_task_logs(task_id)` | 获取任务执行日志 |
| `get_resume_info(mode)` | 获取断点续传信息 |
| `stop_spider(task_id)` | 终止正在运行的任务 |
| `cleanup_expired_tasks()` | 清理过期任务数据（定时任务） |

#### Redis Key 设计

| Key Pattern | 用途 | 过期时间 |
|-------------|------|----------|
| `qa_crawler:progress:{task_id}` | 任务进度详情 | 24小时 |
| `qa_crawler:status:{task_id}` | 任务状态信息 | 24小时 |
| `qa_crawler:resume:{mode}` | 采集断点信息 | 持久化 |
| `qa_crawler:error:{task_id}` | 错误日志 | 24小时 |

### Celery 配置要点

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | 消息队列 |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/0` | 结果存储 |
| `CELERY_TASK_TRACK_STARTED` | `True` | 追踪任务开始时间 |
| `CELERY_TIMEZONE` | `Asia/Shanghai` | 时区配置 |
| `CELERY_TASK_AUTORETRY` | `True` | 自动重试 |
| `CELERY_TASK_MAX_RETRIES` | `5` | 最大重试次数 |

### 断点续传流程

```
1. 任务启动
   │
   ▼
2. 初始化 Redis 状态键
   │
   ▼
3. 每采集 50 条 → 更新 Redis progress
   │
   ▼
4. 任务中断 → Redis 保留断点
   │
   ▼
5. resume=True → 从 Redis 读取断点继续
```

### 任务状态流转

```
PENDING → STARTED → RUNNING → (SUCCESS | FAILURE | REVOKED)
                           ↓
                      TIMEOUT / STOPPED
```

---

## 开发注意事项

### 1. 服务启动顺序
```bash
# 1. 启动 Redis（必须，Celery Broker + 断点存储）
redis-server

# 2. 启动 MySQL（必须，数据存储）
# ... MySQL 服务

# 3. 启动 Celery Worker（必须，异步执行爬虫）
celery -A qa_project worker -l info

# 4. 启动 Django 开发服务器（可选，API 服务）
python manage.py runserver
```

### 2. 运行爬虫
```bash
# 直接运行（同步）
python crawl.py --mode demo

# 异步运行（通过 Celery）
from crawler.tasks import run_spider_task
run_spider_task.delay(mode='demo', limit=20, api_only=True)
```

### 3. 网络问题处理
- 若无法直连 wenda.so.com，需配置代理
- 可使用纯 API 模式 `wenda_api` 爬虫
- 演示模式可能因网络限制无法完成

### 4. 数据入库
- 运行爬虫前确保 MySQL 服务运行
- 数据库 `qa_database` 需提前创建
- `django_celery_results` 已配置但使用 Redis 作为结果后端
