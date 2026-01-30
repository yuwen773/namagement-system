# 菜谱数据分析系统

> 一个集菜谱展示、收藏与深度数据分析于一体的综合平台

## 项目简介

本项目构建一个包含 **10,000-20,000 条菜谱数据**的综合平台，为普通用户提供菜谱探索功能，为管理员提供强大的数据管理与可视化分析能力。

### 核心功能

| 角色 | 功能 |
|:-----|:-----|
| **普通用户** | 菜谱浏览/搜索、分类查看、收藏管理、数据统计（只读） |
| **管理员** | 用户管理、菜谱 CRUD、分类/食材管理、深度数据分析、数据大盘 |

## 技术栈

| 层级 | 技术选型 |
|:-----|:---------|
| **前端** | Vue 3 + Vite + Element Plus + Tailwind CSS + ECharts + Pinia |
| **后端** | Django 5.2 + Django REST Framework + JWT |
| **数据库** | MySQL 8.0+ (utf8mb4) |
| **数据处理** | Pandas + NumPy |

## 项目结构

```
recipe-data-analysis-system/
├── frontend/               # Vue 3 前端项目
│   ├── src/
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # Pinia 状态管理
│   │   └── views/         # 页面组件
│   ├── .env.local         # 前端环境变量
│   └── package.json
├── backend/               # Django 后端项目
│   ├── config/            # Django 配置
│   ├── utils/             # 公共工具模块
│   ├── accounts/          # 用户认证模块
│   ├── recipes/           # 菜谱模块
│   ├── categories/        # 分类模块
│   ├── ingredients/       # 食材模块
│   ├── favorites/         # 收藏模块
│   ├── analytics/         # 数据分析模块
│   ├── admin_panel/       # 管理员模块
│   ├── behavior_logs/     # 行为日志模块
│   ├── .env               # 后端环境变量（需创建）
│   ├── .env.example       # 环境变量模板
│   └── requirements.txt
├── data-scripts/          # 数据脚本（爬虫、清洗、导入、模拟）
├── memory-bank/           # 项目文档（架构、进度、规范）
│   ├── architecture.md    # 架构设计
│   ├── PRD.md             # 产品需求文档
│   ├── progress.md        # 开发进度
│   ├── project-status.md  # 项目状态跟踪
│   ├── implementation-plan.md  # 实施计划
│   └── dev-standards/
│       └── backend-api-standards.md  # 后端开发规范
└── CLAUDE.md              # AI 开发指导文档
```

## 快速开始

### 前置要求

- Node.js 18+
- Python 3.12+
- MySQL 8.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd recipe-data-analysis-system
```

### 2. 后端配置

```bash
cd backend

# 创建虚拟环境
python -m venv backend_venv
source backend_venv/bin/activate  # Windows: backend_venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库密码等配置

# 创建数据库
mysql -u root -p -e "CREATE DATABASE recipe_analysis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 运行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动后端服务器
python manage.py runserver
```

后端服务：`http://localhost:8000/`

### 3. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env.local
# 根据需要修改 API 地址

# 启动开发服务器
npm run dev
```

前端服务：`http://localhost:5173/`

## 环境变量配置

### 后端 (backend/.env)

```bash
# 数据库配置
DB_NAME=recipe_analysis_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 前端 (frontend/.env.local)

```bash
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000
```

## 开发规范

- **后端开发**: 遵循 `memory-bank/dev-standards/backend-api-standards.md`
- **编码前必读**: `memory-bank/architecture.md` 和 `memory-bank/PRD.md`
- **进度跟踪**: 查看 `memory-bank/progress.md` 和 `memory-bank/project-status.md`

## 数据规模目标

| 数据类型 | 目标数量 |
|:---------|:--------:|
| 菜谱数据 | 10,000 - 20,000 条 |
| 模拟用户 | 100+ 个 |
| 用户行为记录 | 10,000+ 条 |
| 食材数据 | 500+ 种 |
| 分类数据 | 50+ 个 |

## 性能目标

| 指标 | 目标值 |
|:-----|:------:|
| 搜索响应时间 | < 500ms |
| 详情页加载时间 | < 1s |
| 大盘数据加载时间 | < 2s |
| 并发用户支持 | 100+ |

## 项目进度

当前阶段：**阶段二 - 数据库设计与模型创建** ✅ 已完成

详细进度请查看：[memory-bank/progress.md](memory-bank/progress.md)

## 文档说明

| 文档 | 说明 |
|:-----|:-----|
| [CLAUDE.md](CLAUDE.md) | AI 开发指导（必读） |
| [memory-bank/architecture.md](memory-bank/architecture.md) | 架构设计 |
| [memory-bank/PRD.md](memory-bank/PRD.md) | 产品需求 |
| [memory-bank/progress.md](memory-bank/progress.md) | 开发进度 |
| [memory-bank/implementation-plan.md](memory-bank/implementation-plan.md) | 实施计划 |

## 开发命令

### 后端

```bash
cd backend

# 运行开发服务器
python manage.py runserver

# 创建迁移
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 进入 Django Shell
python manage.py shell
```

### 前端

```bash
cd frontend

# 运行开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 常见问题

### 1. 数据库连接失败

检查 `.env` 文件中的数据库配置是否正确，确保 MySQL 服务已启动。

### 2. 前端无法访问后端 API

- 确保后端服务器已启动（`http://localhost:8000`）
- 检查前端 `.env.local` 中的 `VITE_API_BASE_URL` 配置
- 查看后端 CORS 配置是否允许前端地址

### 3. 迁移文件冲突

```bash
# 解决迁移冲突
python manage.py migrate --merge
```

## License

MIT
