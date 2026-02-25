# 项目进度

## 核心功能 ✅ 已完成

| 模块 | 状态 | 说明 |
|------|------|------|
| 后端基础架构 | ✅ | Django 5.2 + DRF + MySQL + Redis |
| 用户认证 | ✅ | JWT登录、注册（UI+验证）、UserViewSet、角色(admin/user) |
| 爬虫模块 | ✅ | Scrapy + Playwright + Celery异步任务 + 断点续传 |
| 数据API | ✅ | Question CRUD、统计接口、爬虫控制接口 |
| 前端页面 | ✅ | 登录、仪表盘、数据中心、用户管理、个人中心 |
| 权限控制 | ✅ | 角色路由保护、Pinia状态管理 |

## 待完成

| 阶段 | 任务 |
|------|------|
| 数据采集 | ✅ | 添加测试数据(10条问题+13条答案) |
| 部署 | Docker Compose配置、生产环境构建、init_db.sql脚本 |

## 代码结构

```
backend/
├── qa_project/       # 主项目配置
├── apps/
│   ├── accounts/    # 认证模块 (models, views, serializers, backends)
│   ├── crawler/      # 爬虫 (spiders, tasks, pipelines)
│   └── api/          # REST API
frontend/src/
├── api/              # Axios封装
├── components/       # ECharts, 布局组件
├── router/           # 路由守卫
├── stores/           # Pinia认证状态
└── views/            # 页面组件
```

## API 概览

| 端点 | 功能 |
|------|------|
| POST `/api/auth/login/` | 登录获取JWT |
| GET/POST `/api/auth/users/` | 用户列表/创建 |
| GET `/api/questions/` | 问答列表(分页/搜索) |
| GET `/api/statistics/` | 数据统计 |
| POST `/api/crawler/start/` | 启动爬虫任务 |
