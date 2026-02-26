# 非物质文化遗产数据可视化系统

一个基于 Django + Vue 3 的非物质文化遗产数据管理与可视化平台，提供数据驾驶舱、世界地图分布、项目管理和数据导入等功能。

## 项目简介

本系统旨在管理和可视化全球非物质文化遗产数据，包括：
- **驾驶舱总览**：统计数据、地图分布、分类占比、国家排行
- **数据管理**：非遗项目、传承人、分类字典的 CRUD 操作
- **数据导入**：支持 Excel/CSV 批量导入，包含数据清洗和验证
- **权限控制**：管理员（全权限）和普通用户（只读）双角色

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Element Plus + ECharts + Tailwind CSS + Vite |
| 后端 | Django 5.2 + Django REST Framework + SimpleJWT |
| 数据库 | MySQL 8.0 (UTF8MB4) |

## 功能特性

### 用户端（所有用户）
- 登录/登出（JWT 认证）
- 驾驶舱数据可视化
  - 统计卡片（项目数、传承人数、类别数、覆盖国家数）
  - 世界地图分布（ECharts 地图）
  - 类别占比（饼图）
  - 国家排行（条形图）
- 非遗项目查询（支持筛选、分页）
- 传承人查询（支持筛选、分页）
- 项目详情查看

### 管理端（仅管理员）
- 非遗项目管理（新增、编辑、删除）
- 传承人管理（新增、编辑、删除）
- 分类字典管理（树形结构）
- 数据批量导入（Excel/CSV）
- 导入记录查看与错误下载

## 快速开始

### 环境要求
- Python 3.12+
- Node.js 18+
- MySQL 8.0+

### 后端设置

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件填入数据库配置

# 初始化数据库
mysql -u root -p < sql/init_db.sql

# 运行迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

后端服务运行在 `http://127.0.0.1:8000`

### 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务运行在 `http://localhost:5173`

### 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | password123 | 管理员 |
| user | password123 | 普通用户 |

## 目录结构

```
intangible-cultural-heritage-system/
├── backend/                 # Django 后端
│   ├── apps/
│   │   ├── users/          # 用户认证与权限
│   │   ├── heritage/       # 非遗项目管理
│   │   ├── inheritors/     # 传承人管理
│   │   ├── categories/     # 分类字典管理
│   │   ├── regions/        # 地区管理
│   │   ├── dashboard/      # 驾驶舱聚合接口
│   │   └── importer/       # 数据导入服务
│   ├── utils/              # 工具函数
│   └── .env.example        # 环境变量模板
├── frontend/               # Vue 3 前端
│   └── src/
│       ├── api/            # API 请求封装
│       ├── stores/         # Pinia 状态管理
│       ├── router/         # 路由配置
│       ├── views/          # 页面组件
│       ├── layouts/        # 布局组件
│       └── components/     # 公共组件
├── docs/                   # 项目文档
├── memory-bank/            # 知识库文档
├── sql/                    # 数据库脚本
└── README.md
```

## API 接口

### 认证接口
```
POST /api/v1/auth/login/     # 用户登录
POST /api/v1/auth/refresh/   # 刷新 Token
POST /api/v1/auth/logout/    # 用户登出
GET  /api/v1/auth/me/        # 获取当前用户信息
```

### 数据接口
```
GET    /api/v1/heritage/     # 获取项目列表
POST   /api/v1/heritage/     # 创建项目
PUT    /api/v1/heritage/{id}/ # 更新项目
DELETE /api/v1/heritage/{id}/ # 删除项目

GET    /api/v1/inheritors/   # 获取传承人列表
POST   /api/v1/inheritors/   # 创建传承人
PUT    /api/v1/inheritors/{id}/ # 更新传承人
DELETE /api/v1/inheritors/{id}/ # 删除传承人
```

### 驾驶舱接口
```
GET /api/v1/dashboard/overview/           # 总览统计
GET /api/v1/dashboard/map-distribution/   # 地图分布
GET /api/v1/dashboard/category-distribution/ # 分类占比
GET /api/v1/dashboard/country-ranking/    # 国家排行
```

## 测试

```bash
# 后端接口测试
cd backend
python test_phase_9_10.py      # 驾驶舱和认证测试
python test_phase_11.py        # 列表页面测试
python test_phase_12.py        # 管理功能测试

# 前端自动化测试
python test_frontend_simple.py # Playwright 前端测试
```

## 测试覆盖

| 类型 | 用例数 |
|------|--------|
| 后端 API | 64 |
| 前端自动化 | 9 |
| 安全检查 | 5 项检查 |

## 相关文档

- [产品需求文档](memory-bank/PRD.md)
- [实施计划](memory-bank/implementation-plan.md)
- [系统架构](memory-bank/architecture.md)
- [开发进度](memory-bank/progress.md)
- [API 文档](docs/api-reference.md)
- [安全检查报告](docs/test/security-audit-report.md)
- [前端测试计划](docs/test/frontend-test-plan.md)

## 配置说明

### 环境变量

后端支持通过 `.env` 文件配置（参考 `backend/.env.example`）：

```bash
# Django 配置
DEBUG=False
SECRET_KEY=your-secret-key

# 数据库配置
DB_NAME=heritage_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306

# CORS 配置
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## 开发命令

```bash
# 后端
cd backend && python manage.py runserver
cd backend && python manage.py migrate
cd backend && python manage.py createsuperuser

# 前端
cd frontend && npm run dev
cd frontend && npm run build
```

## 部署说明

> 本系统为开发版本，生产部署前请：
> 1. 设置 `DEBUG=False`
> 2. 配置 `ALLOWED_HOSTS`
> 3. 使用环境变量管理敏感信息
> 4. 配置 HTTPS
> 5. 设置防火墙规则

## 许可证

本项目仅用于学习和演示目的。

---

**开发状态**: 阶段十三完成
**最后更新**: 2026-02-26
