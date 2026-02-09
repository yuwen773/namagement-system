# 爬虫架构简化设计文档

**日期**: 2026-02-08
**作者**: AI + User
**状态**: 已批准

---

## 概述

简化现有爬虫架构，移除 Celery 和 Redis 依赖，直接使用 `TaobaoMtopAPI` 进行数据采集。适用于少量数据采集场景（约 200 条）。

---

## 当前架构

| 组件 | 用途 |
|------|------|
| Django + DRF | API 框架 |
| Celery | 异步任务队列 |
| Redis | 消息代理和结果存储 |
| TaobaoMtopAPI | 核心爬虫类 |

**问题**:
- 需要额外部署 Redis 服务
- 需要运行 Celery Worker 进程
- 架构过于复杂，不符合"少量采集"的使用场景

---

## 目标架构

```
前端请求 → Django API → CrawlerService → 后台线程 → TaobaoMtopAPI
                ↓                              ↓
          返回 task_id                  保存数据到数据库
                ↓                              ↓
          前端轮询状态                    更新 CrawlLog
```

**移除的组件**:
- ❌ Celery
- ❌ Redis

**保留的组件**:
- ✅ Django + DRF
- ✅ TaobaoMtopAPI
- ✅ CrawlLog（简化）
- ✅ MySQL

---

## 数据模型

### CrawlLog（调整后）

```python
class CrawlLog(models.Model):
    """采集日志 - 简化版"""
    id = UUIDField(primary_key=True)
    status = CharField(choices=['running', 'success', 'failed'])
    mode = CharField()  # 'demo' 或 'batch'
    source_type = CharField()  # 'mtop_api', 'playwright'
    items_collected = IntegerField(default=0)
    items_success = IntegerField(default=0)
    items_failed = IntegerField(default=0)
    start_time = DateTimeField()
    end_time = DateTimeField(null=True)
    log_content = TextField(null=True)
    error_message = TextField(null=True)
```

### CrawlTask（新增）

```python
class CrawlTask(models.Model):
    """追踪正在运行的采集任务"""
    id = UUIDField(primary_key=True)
    log = ForeignKey(CrawlLog, on_delete=CASCADE)
    is_running = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
```

---

## API 接口

### 1. 启动采集

```
POST /api/crawler/start/
请求体: {"mode": "demo", "keywords": ["高达"]}
响应: {"code": 0, "data": {"task_id": "uuid"}}
```

### 2. 查询状态

```
GET /api/crawler/status/{task_id}/
响应: {
  "code": 0,
  "data": {
    "task_id": "uuid",
    "is_running": false,
    "status": "success",
    "items_collected": 48
  }
}
```

### 3. 日志列表（保持不变）

```
GET /api/crawler/logs/?page=1&page_size=10
```

---

## 核心实现

### CrawlerService（新增）

```python
# backend/crawler/services.py

class CrawlerService:
    """爬虫服务"""

    @staticmethod
    def start_crawl(mode, keywords):
        """启动采集任务"""
        from threading import Thread
        import uuid

        # 创建日志记录
        log = CrawlLog.objects.create(
            id=uuid.uuid4(),
            status='running',
            mode=mode,
            source_type='mtop_api',
            start_time=timezone.now()
        )

        # 创建任务追踪
        task = CrawlTask.objects.create(
            id=uuid.uuid4(),
            log=log,
            is_running=True
        )

        # 启动后台线程
        thread = Thread(
            target=CrawlerService._run_crawler,
            args=(task.id, mode, keywords)
        )
        thread.start()

        return task.id

    @staticmethod
    def get_status(task_id):
        """获取任务状态"""
        task = CrawlTask.objects.filter(id=task_id).first()
        if not task:
            return None

        log = task.log
        return {
            'task_id': task_id,
            'is_running': task.is_running,
            'status': log.status,
            'items_collected': log.items_collected,
            'progress': '100%' if not task.is_running else '50%'
        }

    @staticmethod
    def _run_crawler(task_id, mode, keywords):
        """后台线程执行采集"""
        from users.models import SystemConfig
        from crawler.spiders.taobao_mtop_api import TaobaoMtopAPI

        task = CrawlTask.objects.get(id=task_id)
        log = task.log

        try:
            # 获取 Cookie
            cookie = SystemConfig.get_value('taobao_cookie', '')
            if not cookie:
                raise Exception("Cookie 未配置")

            # 执行采集
            api = TaobaoMtopAPI(cookie=cookie)
            result = api.search(
                keyword=keywords[0] if keywords else "高达模型",
                max_pages=3 if mode == 'demo' else 5
            )

            # 保存数据
            for item in result['products']:
                Product.objects.create(
                    title=item['title'],
                    price=item['price'],
                    # ...
                )

            # 更新状态
            log.status = 'success'
            log.items_collected = result['success']
            log.end_time = timezone.now()
            log.save()

        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.save()

        finally:
            task.is_running = False
            task.save()
```

### Views 简化

```python
# backend/crawler/views.py

class CrawlerStartView(APIView):
    def post(self, request):
        service = CrawlerService()
        task_id = service.start_crawl(mode, keywords)
        return Response({'code': 0, 'data': {'task_id': task_id}})

class CrawlerStatusView(APIView):
    def get(self, request, task_id):
        service = CrawlerService()
        status = service.get_status(task_id)
        if not status:
            return Response({'code': -1, 'message': '任务不存在'}, status=404)
        return Response({'code': 0, 'data': status})
```

---

## 前端调整

```javascript
// 轮询逻辑
const startPolling = (taskId) => {
  const interval = setInterval(async () => {
    const res = await crawlerApi.getStatus(taskId)

    if (res.data.is_running === false) {
      clearInterval(interval)
      loadLogs()  // 刷新日志列表
    }
  }, 2000)
}
```

---

## 迁移步骤

### 1. 创建新文件
- [ ] `backend/crawler/services.py`
- [ ] `backend/crawler/migrations/000X_crawltask.py`

### 2. 修改文件
- [ ] `backend/crawler/views.py` - 使用 CrawlerService
- [ ] `backend/tmall_project/settings.py` - 移除 Celery 配置
- [ ] `frontend/src/api/crawlerApi.js` - 调整轮询逻辑

### 3. 删除文件
- [ ] `backend/crawler/tasks.py`
- [ ] `backend/tmall_project/celery.py`（如果存在）

### 4. 测试
- [ ] 启动采集任务
- [ ] 等待完成
- [ ] 验证数据保存

---

## 部署变化

**之前需要**:
- Django 服务
- Redis 服务
- Celery Worker

**之后只需要**:
- Django 服务

---

## 文件清单

| 操作 | 文件路径 |
|------|----------|
| 新增 | `backend/crawler/services.py` |
| 修改 | `backend/crawler/models.py` |
| 修改 | `backend/crawler/views.py` |
| 删除 | `backend/crawler/tasks.py` |
| 修改 | `backend/tmall_project/settings.py` |
| 修改 | `frontend/src/api/crawlerApi.js` |

---

## 预期效果

- 🎯 减少 2 个外部依赖（Redis, Celery）
- 🎯 简化部署流程
- 🎯 减少 ~300 行代码
- 🎯 保持相同的功能体验
