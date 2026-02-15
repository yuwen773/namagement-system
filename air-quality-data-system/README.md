# 全国空气质量数据监测与居民个人防护指南平台

<div align="center">

**基于 Python 与 Django 的空气质量可视化与智能防护系统**

[![Django](https://img.shields.io/badge/Django-5.2.10-green)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen)](https://vuejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 项目简介

本项目是一个基于 **B/S 架构**的国家级空气质量监测与居民防护指导平台，通过 Python 技术处理全国空气质量数据，利用可视化技术直观展示空气质量状况，并结合决策树模型为居民提供科学的健康防护建议。

### 核心功能

- **全景可视化** - 实现全国空气质量的时空分布可视化
- **数据分析** - 提供多维度的数据查询、对比与趋势分析
- **智能防护** - 基于数据分析结果，自动生成个性化防护指南

### 用户角色

| 角色 | 描述 |
|------|------|
| **普通用户** | 查看空气质量数据、浏览可视化图表、获取防护建议 |
| **系统管理员** | 管理数据采集任务、维护基础数据、配置防护规则 |

---

## 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Django | 5.2.10 | Web 框架 |
| Django REST Framework | 3.16.1 | API 开发框架 |
| MySQL | 8.0+ | 关系型数据库 |
| drf-spectacular | 0.28.0 | OpenAPI 文档生成 |
| pandas | 2.2.3 | 数据处理 |

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue.js | 3.5 | 前端框架 |
| Element Plus | - | UI 组件库 |
| ECharts | - | 数据可视化 |

---

## 项目结构

```
air-quality-data-system/
├── backend/                    # Django 后端项目
│   ├── air_quality_system/    # 项目配置目录
│   │   ├── settings.py        # 核心配置文件
│   │   ├── urls.py            # 路由配置
│   │   └── wsgi.py            # WSGI 配置
│   ├── apps/                  # 业务应用目录
│   │   ├── accounts/          # 用户认证模块
│   │   ├── airquality/        # 空气质量数据模块
│   │   ├── rules/             # 防护规则模块
│   │   ├── articles/          # 文章公告模块
│   │   └── logs/              # 日志管理模块
│   ├── utils/                 # 工具函数目录
│   ├── manage.py              # Django 管理脚本
│   └── requirements.txt       # Python 依赖
├── dataSource/                # 数据源文件
├── memory-bank/               # 项目文档库
│   ├── PRD.md                 # 产品需求文档
│   ├── architecture.md        # 架构设计文档
│   └── progress.md            # 开发进度记录
├── API_DOCS.md                # API 接口文档
├── AGENTS.md                  # Agent 使用指南
└── README.md                  # 项目说明文档
```

---

## 功能模块

### 用户端功能

| 模块 | 功能描述 |
|------|----------|
| **首页概览** | 全国空气质量地图、实时排行榜、核心指标概览 |
| **城市详情** | 城市/站点实时数据、污染物浓度、24小时趋势图 |
| **历史查询** | 历史数据检索、分页展示、数据导出 |
| **数据分析** | 城市对比、相关性分析、统计图表 |
| **防护指南** | 基于 AQI 的智能防护建议、人群分类提示 |
| **科普知识** | 空气质量指标说明、健康小贴士 |

### 管理端功能

| 模块 | 功能描述 |
|------|----------|
| **控制台** | 系统状态监控、数据统计、用户概况 |
| **数据导入** | CSV/Excel 文件上传、导入任务监控、日志记录 |
| **数据管理** | 空气质量数据的查询、编辑、删除 |
| **规则管理** | 防护规则的配置与维护 |
| **用户管理** | 用户列表、状态管理、权限分配 |
| **内容管理** | 文章发布、分类管理 |
| **系统日志** | 操作日志、异常日志查看 |

---

## 快速开始

### 环境要求

- Python 3.10+
- MySQL 8.0+
- Node.js 16+ (前端开发)

### 后端安装

```bash
# 1. 克隆项目
git clone <repository-url>
cd air-quality-data-system/backend

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置数据库
# 编辑 air_quality_system/settings.py，配置数据库连接
# 或使用环境变量：
# export DB_NAME=air_quality_db
# export DB_USER=root
# export DB_PASSWORD=your_password
# export DB_HOST=127.0.0.1
# export DB_PORT=3307

# 5. 执行数据库迁移
python manage.py migrate

# 6. 创建超级用户
python manage.py createsuperuser

# 7. 启动开发服务器
python manage.py runserver
```

后端服务默认运行在 `http://127.0.0.1:8000/`

### 前端安装

```bash
# 1. 进入前端目录（如果存在）
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
```

前端服务默认运行在 `http://127.0.0.1:5173/`

---

## API 文档

项目提供完整的 OpenAPI 3.0 规范文档：

| 文档类型 | 地址 |
|----------|------|
| Swagger UI | `http://127.0.0.1:8000/api/docs/` |
| OpenAPI Schema | `http://127.0.0.1:8000/api/schema/` |
| Markdown 文档 | 查看 [API_DOCS.md](./API_DOCS.md) |

### API 认证

本项目使用 **Token Authentication**：

```http
Authorization: Token <your_token_here>
```

登录成功后返回的 token 需要在后续请求中携带。

---

## 数据库配置

### 默认配置

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "air_quality_db",
        "USER": "root",
        "PASSWORD": "your_password",
        "HOST": "127.0.0.1",
        "PORT": "3307",
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}
```

### 环境变量

支持通过环境变量覆盖配置：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DB_NAME` | 数据库名称 | `air_quality_db` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | - |
| `DB_HOST` | 数据库主机 | `127.0.0.1` |
| `DB_PORT` | 数据库端口 | `3307` |

---

## 数据模型

### 核心数据表

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| `accounts_user` | 用户表 | username, email, phone, role, status |
| `airquality_province` | 省份表 | code, name |
| `airquality_city` | 城市表 | code, name, province |
| `airquality_monitoringstation` | 监测站点 | code, name, city, address |
| `airquality_airqualitydata` | 空气质量数据 | aqi, pm25, pm10, so2, no2, co, o3 |
| `rules_protectionrule` | 防护规则 | min_aqi, max_aqi, population_type, advice |
| `articles_article` | 文章公告 | title, content, category, status |
| `logs_operationlog` | 操作日志 | user, operation_type, ip_address |
| `logs_errorlog` | 异常日志 | error_type, error_message, stack_trace |

### 空气质量等级

| 等级 | AQI 范围 | 说明 |
|------|----------|------|
| EXCELLENT | 0-50 | 优 |
| GOOD | 51-100 | 良 |
| LIGHT_POLLUTION | 101-150 | 轻度污染 |
| MODERATE_POLLUTION | 151-200 | 中度污染 |
| HEAVY_POLLUTION | 201-300 | 重度污染 |
| SEVERE_POLLUTION | 301-500 | 严重污染 |

---

## 开发指南

### 代码规范

- 后端遵循 [PEP 8](https://pep8.org/) 规范
- 前端遵循 [ESLint](https://eslint.org/) 规范
- 提交信息遵循 [约定式提交](https://www.conventionalcommits.org/zh-hans/) 规范

### 分支策略

```
main          # 主分支，稳定版本
develop       # 开发分支
feature/*     # 功能分支
fix/*         # 修复分支
```

### 测试

```bash
# 运行所有测试
python manage.py test

# 运行特定应用的测试
python manage.py test apps.accounts

# 生成测试覆盖率报告
coverage run --source='.' manage.py test
coverage report
```

---

## 部署

### 生产环境配置

```bash
# 1. 设置环境变量
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY=<your-secret-key>
export DJANGO_ALLOWED_HOSTS=yourdomain.com

# 2. 收集静态文件
python manage.py collectstatic

# 3. 使用 Gunicorn 启动
gunicorn air_quality_system.wsgi:application --bind 0.0.0.0:8000
```

### Docker 部署

```dockerfile
# 示例 Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "air_quality_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 常见问题

### 1. 数据库连接失败

检查 MySQL 服务是否启动，端口和密码配置是否正确。

### 2. CORS 跨域问题

在 `settings.py` 中配置 `CORS_ALLOWED_ORIGINS`：

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

### 3. 数据导入失败

检查文件格式是否正确（CSV/XLSX），字段映射是否匹配。

---

## 项目文档

| 文档 | 说明 |
|------|------|
| [API_DOCS.md](./API_DOCS.md) | 完整的 API 接口文档 |
| [memory-bank/PRD.md](./memory-bank/PRD.md) | 产品需求文档 |
| [memory-bank/architecture.md](./memory-bank/architecture.md) | 架构设计文档 |
| [memory-bank/progress.md](./memory-bank/progress.md) | 开发进度记录 |
| [AGENTS.md](./AGENTS.md) | Claude Agent 使用指南 |

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'feat: 添加某个功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 许可证

本项目采用 [MIT](LICENSE) 许可证。

---

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 Issue
- 发送邮件至项目维护者

---

<div align="center">

**感谢使用全国空气质量数据监测与居民个人防护指南平台！**

Made with ❤️ by the Air Quality Team

</div>
