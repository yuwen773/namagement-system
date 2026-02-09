# 系统架构

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 5.2 + DRF |
| 数据库 | MySQL 8.0 (端口 3307) |
| 任务队列 | Celery + Redis (端口 6379) |
| 前端 | Vue 3 + Pinia + Element Plus + ECharts |
| 爬虫 | Scrapy + Playwright |

## 目录结构

```
backend/
├── qa_project/       # Django 主项目配置
├── apps/
│   ├── accounts/     # 用户认证 (User 模型、JWT)
│   ├── crawler/      # 爬虫模块 (Question/Tag 模型、Celery 任务)
│   └── api/          # 数据 API (问答 CRUD、统计)
frontend/
├── src/
│   ├── main.js       # 应用入口
│   ├── router/       # 路由 + 导航守卫
│   ├── stores/       # Pinia 状态管理
│   ├── utils/        # 请求工具 (request.js, auth.js)
│   ├── api/          # API 接口模块 (users.js, questions.js)
│   └── views/        # 页面组件 (Login, Dashboard, DataCenter, Profile, UserManagement)
```

## 核心文件

| 文件路径 | 作用 |
|----------|------|
| `apps/accounts/models.py` | User 模型 |
| `apps/accounts/views.py` | 认证视图 (登录/注册/用户信息) |
| `apps/crawler/models.py` | Question、Tag 数据模型 |
| `apps/crawler/tasks.py` | Celery 异步采集任务 |
| `apps/api/views.py` | 问答 CRUD、统计 API |
| `src/stores/auth.js` | 登录状态、Token 管理 |
| `src/views/DataCenter.vue` | 数据列表页面 |
| `src/views/Profile.vue` | 个人中心页面 |

## API 端点

| 模块 | 端点 | 方法 | 说明 |
|------|------|------|------|
| 认证 | `/api/auth/login/` | POST | 登录 |
| 认证 | `/api/auth/register/` | POST | 注册 |
| 认证 | `/api/auth/me/` | GET | 当前用户 |
| 认证 | `/api/auth/change-password/` | POST | 修改密码 |
| 问答 | `/api/questions/` | GET/DELETE | 列表/删除 |
| 统计 | `/api/statistics/trend/` | GET | 问答趋势 |
| 爬虫 | `/api/crawler/start/` | POST | 启动采集 |

## 用户角色

| 角色 | 权限 |
|------|------|
| admin | 所有权限（含爬虫、用户管理、数据删除） |
| user | 查看、搜索、数据详情 |

## 启动命令

```bash
# 后端
redis-server
python manage.py runserver

# 前端
cd frontend && npm run dev
```
