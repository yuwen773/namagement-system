# 天猫宠物用品数据采集系统

<div align="center">

**一个基于 Django + Vue 3 的宠物用品数据采集与可视化分析平台**

[![Django](https://img.shields.io/badge/Django-5.2-green)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[功能特性](#功能特性) • [快速开始](#快速开始) • [项目结构](#项目结构) • [技术栈](#技术栈) • [文档](#文档)

</div>

---

## 项目简介

随着宠物用品市场的蓬勃发展，商品更新迭代迅速，价格与销量波动频繁。本项目旨在构建一个**自动化数据采集与可视化分析系统**，帮助用户高效获取并分析天猫宠物用品商品数据。

### 核心功能

| 模块 | 功能描述 |
|------|----------|
| **数据采集** | 基于 TaobaoMtopAPI 的智能爬虫，支持演示模式与批量采集 |
| **数据管理** | 10,000+ 真实宠物用品商品数据，支持搜索、筛选、导出 |
| **数据可视化** | ECharts 图表展示价格分布、销量排行、品牌占比 |
| **用户权限** | 管理员与普通用户双角色，权限分级管理 |
| **统计分析** | 商品总量、价格区间、店铺排行等多维度统计 |

---

## 功能特性

### 管理端功能

- **系统仪表盘** - 全局数据概览、价格分布图、品牌占比
- **采集控制台** - 一键启动爬虫任务、实时日志监控
- **商品管理** - 数据表格维护、搜索筛选、批量导出
- **用户管理** - 账号管理、冻结解冻、权限控制
- **个人中心** - 资料维护、密码修改

### 用户端功能

- **市场行情** - 销量 Top10 榜单、降价推荐、热度趋势
- **商品资源库** - 高级搜索、商品浏览、详情查看
- **商品详情** - 深度分析、历史价格走势、直达天猫
- **个人中心** - 信息管理、偏好设置

---

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/tmall-collecting-platform.git
cd tmall-collecting-platform
```

### 2. 数据库配置

```bash
# 创建数据库
mysql -u root -p -P 3307
CREATE DATABASE tmall_collecting CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入初始数据（包含 10,000+ 条宠物用品商品数据）
mysql -u root -p -P 3307 tmall_collecting < sql/init_db.sql
```

### 3. 后端配置

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（编辑 .env 文件）
cp .env.example .env
# 修改数据库密码等配置

# 执行数据库迁移
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser

# 启动后端服务（默认端口 8000）
python manage.py runserver
```

### 4. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（默认端口 5173）
npm run dev
```

### 5. 访问系统

- **前端地址**: http://localhost:5173
- **后端 API**: http://localhost:8000/api
- **管理员后台**: http://localhost:8000/admin

默认测试账号：
- 管理员: `admin` / `admin123`
- 普通用户: `user` / `user123`

---

## 项目结构

```
tmall-collecting-platform/
├── backend/                    # Django 后端
│   ├── tmall_project/         # 项目配置
│   │   ├── settings.py        # 全局配置
│   │   ├── urls.py            # 路由配置
│   │   └── celery.py          # Celery 配置
│   ├── users/                 # 用户模块
│   │   ├── models.py          # User 模型
│   │   ├── views.py           # 认证视图
│   │   └── urls.py
│   ├── products/              # 商品模块
│   │   ├── models.py          # Product, PriceHistory 模型
│   │   ├── views.py           # CRUD 视图
│   │   └── urls.py
│   ├── crawler/               # 爬虫模块
│   │   ├── services.py        # 爬虫服务层
│   │   ├── views.py           # API 视图
│   │   ├── spiders/           # 爬虫实现
│   │   │   ├── taobao_mtop_api.py    # Mtop API 爬虫
│   │   │   └── tmall_real_api.py     # 真实 API 爬虫
│   │   ├── pipelines.py       # 数据处理管道
│   │   └── middlewares.py     # 中间件
│   ├── requirements.txt       # Python 依赖
│   └── manage.py
│
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── api/              # API 接口封装
│   │   ├── components/       # 公共组件
│   │   │   ├── Layout/      # 布局组件
│   │   │   └── common/      # 通用组件
│   │   ├── views/            # 页面组件
│   │   │   ├── admin/       # 管理端页面
│   │   │   └── user/        # 用户端页面
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # Pinia 状态管理
│   │   └── utils/            # 工具函数
│   ├── package.json
│   └── vite.config.js
│
├── scripts/                   # 工具脚本
│   ├── test_tmall_crawler.py    # 爬虫测试
│   ├── test_mtop_api.py         # Mtop API 测试
│   └── import_from_csv.py       # CSV 导入
│
├── sql/
│   └── init_db.sql            # 数据库初始化脚本
│
├── docs/                      # 项目文档
│   ├── API.md                  # API 接口文档
│   ├── crawler-usage-guide.md  # 爬虫使用指南
│   └── csv-import-guide.md     # CSV 导入指南
│
└── memory-bank/              # 项目知识库
    ├── architecture.md         # 系统架构
    ├── PRD.md                  # 产品需求文档
    ├── tech-stack.md           # 技术栈说明
    ├── IMPLEMENTATION_PLAN.md  # 实施计划
    └── progress.md             # 开发进度
```

---

## 技术栈

### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Django | 5.2 | Web 框架 |
| Django REST Framework | 3.15 | API 框架 |
| MySQL | 8.0+ | 数据库 |
| Celery | 5.4 | 异步任务队列 |
| Redis | 6.0+ | 消息代理 |
| Pandas | 2.0+ | 数据处理 |

### 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.5 | 前端框架 |
| Element Plus | Latest | UI 组件库 |
| ECharts | 5.x | 数据可视化 |
| Tailwind CSS | 3.4 | 样式框架 |
| Pinia | Latest | 状态管理 |
| Axios | Latest | HTTP 客户端 |

### 爬虫技术

| 技术 | 用途 |
|------|------|
| TaobaoMtopAPI | 天猫内部 API |
| Python Threading | 多线程采集 |
| Requests | HTTP 请求 |

---

## 数据采集

### 采集模式

系统支持多种采集模式，自动降级切换：

1. **Mtop API**（优先）- 使用天猫内部 API，效率最高
2. **真实 API** - 基于 g_page_config 解析
3. **演示数据** - 用于快速演示和测试

### 快速测试

```bash
# 设置 Cookie（参考 docs/crawler-cookie-guide.md）
export TAOBAO_COOKIE="你的Cookie字符串"

# 测试爬虫
cd backend
python scripts/test_mtop_api.py
```

### 批量导入

```bash
# 导入 CSV 数据
python manage.py import_csv --file data/products.csv
```

---

## API 文档

完整的 API 接口文档请参阅 [docs/API.md](docs/API.md)

### 主要接口

```
POST   /api/users/register/     # 用户注册
POST   /api/users/login/        # 用户登录
GET    /api/products/           # 商品列表
GET    /api/products/{id}/      # 商品详情
POST   /api/crawler/start/      # 启动采集
GET    /api/crawler/status/     # 采集状态
GET    /api/statistics/overview/# 数据统计
```

### 响应格式

```json
// 成功响应
{
  "code": 0,
  "data": {...},
  "total": 10000
}

// 错误响应
{
  "code": -1,
  "message": "错误描述"
}
```

---

## 开发进度

| 阶段 | 状态 | 说明 |
|------|------|------|
| 后端开发 | ✅ | Django + DRF + Celery 完成 |
| 接口文档 | ✅ | API 文档完整 |
| 爬虫实现 | ✅ | Mtop API + 多层降级 |
| 数据准备 | ✅ | 10,000+ 条宠物用品数据 |
| 前端开发 | ⏳ | 进行中 |

详见 [memory-bank/progress.md](memory-bank/progress.md)

---

## 环境配置

### 本地开发环境

| 配置项 | 值 |
|--------|-----|
| 后端端口 | 8000 |
| 前端端口 | 5173 |
| MySQL 端口 | 3307 |
| Redis 端口 | 6379 |
| JWT Access Token | 2 小时 |
| JWT Refresh Token | 7 天 |

### .env 配置示例

```bash
# 数据库配置
DB_NAME=tmall_collecting
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3307

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT 配置
SECRET_KEY=your_secret_key
ACCESS_TOKEN_LIFETIME=120  # 分钟
REFRESH_TOKEN_LIFETIME=10080  # 分钟 (7天)

# 爬虫配置
TAOBAO_COOKIE=your_cookie_string
```

---

## 常见问题

### 1. 数据库连接失败

检查 MySQL 服务是否启动，端口是否为 3307

### 2. 爬虫无法获取数据

请确保已正确设置 TAOBAO_COOKIE，参考 [Cookie 获取指南](docs/crawler-cookie-guide.md)

### 3. 前端跨域问题

后端已配置 CORS，确保前端代理配置正确

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 Issue
- 发送邮件

---

<div align="center">

**本项目仅供学习研究使用，请遵守相关法律法规**

Made with ❤️ by Tmall Pet Supplies Platform Team

</div>
