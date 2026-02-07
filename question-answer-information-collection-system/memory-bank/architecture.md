# 系统架构

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5.2 + DRF |
| 数据库 | MySQL 8.0 (3307) |
| 任务队列 | Celery + Redis |
| 前端 | Vue 3 + Element Plus + ECharts |
| 爬虫 | Scrapy + Playwright |

## 模块结构

```
backend/
├── qa_project/          # Django 主项目
│   ├── settings.py      # 配置
│   ├── urls.py         # 路由
│   └── celery.py        # Celery 配置
├── apps/
│   ├── accounts/        # 用户认证
│   ├── crawler/         # 爬虫模块
│   └── api/             # 数据 API
└── crawl.py             # 爬虫启动脚本
```

## 数据模型

### Question (问答)
- title, description, answer_content, answer_time, answerer
- source_url (唯一索引), tags (多对多)
- created_at, updated_at

### Tag (标签)
- name (唯一)

## API 端点

### 认证模块 `/api/auth/`
| 方法 | 端点 |
|------|------|
| POST | `/api/auth/token/` 获取 Token |
| POST | `/api/auth/register/` 注册 |

### 爬虫控制 `/api/crawler/`
| 方法 | 端点 | 权限 |
|------|------|------|
| GET | `/api/crawler/status/` | 登录 |
| POST | `/api/crawler/start/` | 管理员 |
| POST | `/api/crawler/stop/` | 管理员 |
| GET | `/api/crawler/progress/<id>/` | 登录 |
| GET | `/api/crawler/logs/<id>/` | 登录 |

### 问答数据 `/api/questions/`
| 方法 | 端点 |
|------|------|
| GET | `/api/questions/` (分页+搜索) |
| GET | `/api/questions/<id>/` |
| DELETE | `/api/questions/<id>/` (管理员) |
| GET | `/api/questions/tags/` |

## 用户角色

| 角色 | 权限 |
|------|------|
| admin | 所有权限 |
| user | 查看、搜索 |

## 数据流向

```
爬虫 → Scrapy Pipeline → DataCleaner → MySQL → API → 前端
                    ↓
              Celery + Redis (异步任务)
```

## 服务启动

```bash
# 1. Redis (必须)
redis-server

# 2. MySQL (必须)

# 3. Celery Worker (必须)
celery -A qa_project worker -l info

# 4. Django 开发服务器
python manage.py runserver
```
