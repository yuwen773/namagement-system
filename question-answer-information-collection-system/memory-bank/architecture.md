# 系统架构

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5.2 + DRF |
| 数据库 | MySQL 8.0 (3307) |
| 任务队列 | Celery + Redis (6379) |
| 前端 | Vue 3 + Pinia + Element Plus + ECharts |
| 爬虫 | Scrapy + Playwright (双模式) |

## 核心约定

- **密码**：明文存储（自定义认证后端）
- **响应格式**：`{ code: 0, data: {...}, total: n }`
- **角色**：`admin`(全权限) / `user`(查看)

## 关键文件

| 文件 | 作用 |
|------|------|
| `apps/accounts/models.py` | User模型（明文密码） |
| `apps/accounts/backends.py` | PlainPasswordBackend认证 |
| `apps/crawler/tasks.py` | Celery异步爬虫任务 |
| `apps/crawler/spiders/*.py` | 360问答爬虫(Playwright/API双模式) |
| `src/utils/request.js` | Axios封装(Token自动携带) |
| `src/stores/auth.js` | Pinia认证状态 |
| `src/components/ECharts.vue` | 图表组件(resize+内存管理) |

## 启动

```bash
# 启动Redis
redis-server

# 后端
cd backend && python manage.py runserver

# 前端
cd frontend && npm run dev
```
