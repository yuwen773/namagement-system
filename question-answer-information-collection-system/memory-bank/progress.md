# 项目进度

| 阶段 | 状态 | 日期 |
|------|------|------|
| 第一阶段：项目初始化与后端基础架构 | ✅ | 2026-02-07 |
| 第二阶段：用户认证模块 | ✅ | 2026-02-07 |
| 第三阶段：爬虫模块 | ✅ | 2026-02-07 |
| - 步骤 7：问答数据模型 | ✅ | |
| - 步骤 8：数据清洗工具 | ✅ | |
| - 步骤 9：360问答爬虫 | ✅ | |
| - 步骤 10：Celery异步任务 | ✅ | |
| - 步骤 11：爬虫状态API | ✅ | |
| 第四阶段：数据管理API | ✅ | 2026-02-07 |
| 第五阶段：前端基础架构 | ⏳ | |
| 第六阶段：前端页面开发 | ⏳ | |
| 第七阶段：数据采集 | ⏳ | |
| 第八阶段：部署与交付 | ⏳ | |

---

## 已创建文件清单

### 后端

| 文件 | 说明 |
|------|------|
| `apps/accounts/models.py` | User 模型 |
| `apps/accounts/views.py` | 认证视图 |
| `apps/accounts/urls.py` | 认证路由 |
| `apps/crawler/models.py` | Question/Tag 模型 |
| `apps/crawler/items.py` | Scrapy Item 定义 |
| `apps/crawler/utils.py` | DataCleaner 数据清洗 |
| `apps/crawler/pipelines.py` | 数据处理管道 |
| `apps/crawler/settings.py` | Scrapy 配置 |
| `apps/crawler/tasks.py` | Celery 任务 |
| `apps/crawler/spiders/wenda_spider.py` | 混合模式爬虫 |
| `apps/crawler/spiders/wenda_api_spider.py` | 纯 API 爬虫 |
| `apps/api/views.py` | API 视图 |
| `apps/api/urls.py` | API 路由 |
| `apps/api/serializers.py` | 序列化器 |
| `qa_project/celery.py` | Celery 配置 |
| `qa_project/exceptions.py` | 异常处理 |
| `crawl.py` | 爬虫启动脚本 |
| `requirements.txt` | 依赖清单 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `qa_project/settings.py` | Django 配置 |
| `qa_project/urls.py` | 主路由 |
