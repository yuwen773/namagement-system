# 项目进度

| 阶段 | 状态 | 日期 |
|------|------|------|
| 第一阶段：项目初始化与后端基础架构 | ✅ | 2026-02-07 |
| 第二阶段：用户认证模块 | ✅ | 2026-02-07 |
| 第三阶段：爬虫模块 | | |
| - 步骤 7：问答数据模型 | ✅ | |
| - 步骤 8：数据清洗工具 | ✅ | 2026-02-07 |
| - 步骤 9：360问答爬虫 | ✅ | 2026-02-07 |
| - 步骤 10：Celery异步任务 | ✅ | 2026-02-07 |
| - 步骤 11：爬虫状态API | ⏳ | |
| 第四阶段：数据管理API | ⏳ | |
| 第五阶段：前端基础架构 | ⏳ | |
| 第六阶段：前端页面开发 | ⏳ | |
| 第七阶段：数据采集 | ⏳ | |
| 第八阶段：部署与交付 | ⏳ | |

## 步骤9完成记录 (2026-02-07)

### 创建的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| items.py | `apps/crawler/items.py` | 定义 QuestionItem 数据结构 |
| wenda_spider.py | `apps/crawler/spiders/wenda_spider.py` | 混合模式爬虫（JSON API + Playwright） |
| wenda_api_spider.py | `apps/crawler/spiders/wenda_api_spider.py` | 纯 API 模式爬虫（备用） |
| settings.py | `apps/crawler/settings.py` | Scrapy 配置（代理、限速、Playwright） |
| __init__.py | `apps/crawler/spiders/__init__.py` | Spiders 包初始化 |
| crawl.py | `backend/crawl.py` | 爬虫启动脚本 |
| requirements.txt | `backend/requirements.txt` | 依赖清单 |
| test_spider.py | `backend/test_spider.py` | 单元测试脚本 |

### 功能特性

1. **混合采集模式**
   - 优先使用 JSON API 模式（高效）
   - API 失效时自动降级为 Playwright 浏览器渲染

2. **反爬机制**
   - User-Agent 轮换
   - 请求延迟（3-8秒随机）
   - 自动限速（Autothrottle）
   - 代理轮换支持
   - 断点续传（Redis 存储进度）

3. **数据处理**
   - HTML 标签清洗
   - 文本规范化
   - 重复检测
   - 批量入库（每100条）

### 验证结果

- ✅ 单元测试全部通过
- ✅ QuestionItem 数据结构正确
- ✅ DataCleaner 清洗逻辑正常
- ⚠️ 网络限制：当前环境无法直连 wenda.so.com（需代理/VPN）

### 运行命令

```bash
# 演示模式（20条）
python crawl.py --mode demo

# 全量模式
python crawl.py --mode full --limit 10000

# 纯 API 模式（无需 Playwright）
scrapy crawl wenda_api -o output.json
```

### 注意事项

1. 运行前需启动 Redis 服务（断点续用）
2. Playwright 需单独安装：`playwright install chromium`
3. 若网络无法访问目标网站，需配置代理

---

## 步骤10完成记录 (2026-02-07)

### 创建的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| celery.py | `qa_project/celery.py` | Celery 应用配置（broker、任务序列化、时区） |
| tasks.py | `apps/crawler/tasks.py` | Celery 任务模块（run_spider_task、进度追踪、断点续传） |
| test_celery.py | `backend/test_celery.py` | Celery 配置测试脚本 |

### 修改的文件

| 文件 | 变更 |
|------|------|
| `qa_project/__init__.py` | 添加 Celery 应用加载 |
| `qa_project/settings.py` | 添加 Celery 配置（BROKER_URL、RESULT_BACKEND等） |

### 功能特性

1. **异步任务执行**
   - `run_spider_task(mode, limit, resume, api_only)` - 主任务入口
   - 支持演示模式（limit=20）和全量模式（limit=10000）
   - 自动重试机制（最多5次，指数退避）

2. **进度追踪**
   - Redis 存储实时进度（每50条更新）
   - 细粒度状态：`running`, `completed`, `failed`, `timeout`, `stopped`
   - 包含 timestamp、current_page、collected、failed_count

3. **断点续传**
   - Redis Key: `qa_crawler:progress:{task_id}` - 任务进度
   - Redis Key: `qa_crawler:status:{task_id}` - 任务状态
   - Redis Key: `qa_crawler:resume:{mode}` - 采集断点

4. **任务管理**
   - `get_task_status(task_id)` - 查询状态
   - `get_task_progress(task_id)` - 查询进度
   - `get_task_logs(task_id)` - 获取错误日志
   - `stop_spider(task_id)` - 终止任务

### 验证结果

- ✅ Celery 应用导入成功
- ✅ Redis 连接成功（localhost:6379）
- ✅ 8 个任务正确注册
- ✅ 异步任务提交成功（任务 ID: dadc333a-38af-47ec-b987-f3a02673c2ee）
- ✅ Redis 读写测试通过

### 运行命令

```bash
# 启动 Celery Worker（必须）
celery -A qa_project worker -l info

# 启动 Celery Beat（可选，定时任务）
celery -A qa_project beat -l info

# 提交爬虫任务
from crawler.tasks import run_spider_task
run_spider_task.delay(mode='demo', limit=20, api_only=True)
```

### 注意事项

1. **必须启动 Redis 服务**：Redis 是 Celery Broker 和断点存储的核心
2. **必须启动 Celery Worker**：否则任务会挂起无法执行
3. **配置变化**：
   - `CELERY_BROKER_URL = 'redis://localhost:6379/0'`
   - `CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'`
   - 时区设置为 `Asia/Shanghai`
