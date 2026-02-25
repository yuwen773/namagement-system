# 系统架构文档

## 1. 项目概述

非物质文化遗产数据可视化系统是一个前后端分离的 Web 应用，支持管理员和普通用户两类角色，提供数据管理、可视化展示和数据导入功能。

## 2. 技术架构

### 2.1 整体架构
```
┌─────────────────────────────────────────────────────────┐
│                    前端层 (Frontend)                      │
│         Vue 3 + TypeScript + Element Plus               │
│              ECharts + Tailwind CSS                     │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────┐
│                    后端层 (Backend)                       │
│           Django 5.2 + Django REST Framework            │
└─────────────────────────────────────────────────────────┘
                          ↓ ORM
┌─────────────────────────────────────────────────────────┐
│                   数据层 (Database)                       │
│                    MySQL 8.0+                           │
└─────────────────────────────────────────────────────────┘
```

### 2.2 后端模块架构

```
backend/
├── heritage_system/          # Django 项目核心配置
│   ├── settings.py          # 全局配置（数据库、应用、中间件）
│   ├── urls.py              # 根路由配置
│   ├── wsgi.py              # WSGI 服务器入口
│   └── asgi.py              # ASGI 服务器入口（异步支持）
│
├── apps/                     # 业务应用模块
│   ├── users/               # 用户认证与权限模块
│   ├── heritage/            # 非遗项目管理模块
│   ├── inheritors/          # 传承人管理模块
│   ├── categories/          # 分类字典管理模块
│   ├── regions/             # 地理区域管理模块
│   ├── importer/            # 数据导入处理模块
│   └── dashboard/           # 驾驶舱统计模块
│
├── utils/                    # 通用工具模块
│   ├── response.py          # 统一响应格式（待实现）
│   ├── permissions.py       # 权限类（待实现）
│   └── jwt_utils.py         # JWT 工具（待实现）
│
├── media/                    # 用户上传文件存储
├── logs/                     # 应用日志存储
└── manage.py                # Django 命令行工具
```

## 3. 模块职责说明

### 3.1 heritage_system（项目配置）
**作用**：Django 项目的核心配置中心

**关键文件**：
- `settings.py`：
  - 数据库配置（MySQL 连接信息）
  - 应用注册（INSTALLED_APPS）
  - 中间件配置
  - 静态文件和媒体文件路径
  - 时区和语言设置（Asia/Shanghai, zh-hans）
  - REST Framework 配置（待添加）
  - JWT 配置（待添加）
  - CORS 配置（待添加）

- `urls.py`：根路由配置，将请求分发到各个应用

### 3.2 apps/users（用户管理）
**作用**：处理用户认证、授权和权限控制

**核心功能**：
- 用户登录/登出（JWT Token）
- Token 刷新机制
- 角色管理（admin/user）
- 权限验证（IsAdmin, IsAdminOrReadOnly）

**数据模型**（待实现）：
- User 扩展模型（添加 role 字段）

### 3.3 apps/heritage（非遗项目管理）
**作用**：管理非物质文化遗产项目数据

**核心功能**：
- 项目 CRUD 操作
- 项目查询和筛选（按类别、级别、国家）
- 项目详情展示
- 关联传承人查询

**数据模型**（待实现）：
- HeritageItem：项目名称、类别、级别、国家、地区、保护单位、简介等

### 3.4 apps/inheritors（传承人管理）
**作用**：管理非遗项目传承人信息

**核心功能**：
- 传承人 CRUD 操作
- 传承人查询和筛选
- 关联项目查询

**数据模型**（待实现）：
- Inheritor：姓名、性别、级别、所属项目、国家、地区等

### 3.5 apps/categories（分类字典管理）
**作用**：管理非遗项目的分类体系

**核心功能**：
- 分类 CRUD 操作
- 树形结构管理（支持多级分类）
- 分类查询和搜索

**数据模型**（待实现）：
- Category：名称、代码、级别、父分类

### 3.6 apps/regions（地理区域管理）
**作用**：管理国家和地区信息，提供地理数据标准化服务

**核心功能**：
- 国家/地区 CRUD 操作
- ISO-3166 国家代码映射
- 经纬度数据管理
- 国家名称标准化

**数据模型**（待实现）：
- Region：国家代码、国家名称、经度、纬度、所属洲

### 3.7 apps/importer（数据导入）
**作用**：处理 Excel/CSV 文件的批量导入

**核心功能**：
- 文件上传和解析
- 数据清洗和标准化
- 数据增强（地理信息补全、分类映射）
- 批量入库（事务处理）
- 导入日志和错误报告

**数据模型**（待实现）：
- ImportJob：导入任务记录
- ImportError：导入错误明细

**处理流程**：
1. 文件上传 → 2. 格式解析 → 3. 数据清洗 → 4. 标准化 → 5. 增强 → 6. 校验 → 7. 入库

### 3.8 apps/dashboard（驾驶舱统计）
**作用**：提供数据聚合和统计分析接口

**核心功能**：
- 总览统计（项目数、传承人数、类别数、国家数）
- 地图分布数据（国家级热力图数据）
- 类别占比统计
- 国家排行统计
- 趋势分析（按年度）

**特点**：
- 无独立数据模型，通过聚合查询其他模块数据
- 优化查询性能（使用 Django ORM 聚合函数）

### 3.9 utils（通用工具）
**作用**：提供跨模块的通用功能

**待实现组件**：
- `response.py`：统一 API 响应格式 `{ code: 0, data: {...}, total: n }`
- `permissions.py`：自定义权限类（IsAdmin, IsAdminOrReadOnly）
- `jwt_utils.py`：JWT Token 生成和验证工具
- `validators.py`：通用数据验证器
- `exceptions.py`：自定义异常处理

### 3.10 media/（媒体文件）
**作用**：存储用户上传的文件

**目录结构**（规划）：
```
media/
├── uploads/              # 导入文件临时存储
│   ├── 2026/
│   │   └── 02/
│   │       └── heritage_data.xlsx
└── exports/              # 导出文件存储
```

### 3.11 logs/（日志文件）
**作用**：存储应用运行日志

**日志类型**（规划）：
- `django.log`：Django 框架日志
- `api.log`：API 请求日志
- `import.log`：数据导入日志
- `error.log`：错误日志

## 4. 数据库设计

### 4.1 数据库信息
- **名称**：heritage_db
- **字符集**：utf8mb4
- **排序规则**：utf8mb4_unicode_ci
- **引擎**：InnoDB（默认）

### 4.2 核心数据表（待创建）

#### 用户相关
- `auth_user`（Django 内置，已创建）
- `users_profile`（扩展用户信息，待创建）

#### 业务数据
- `heritage_items`：非遗项目
- `inheritors`：传承人
- `categories`：分类字典
- `regions`：地理区域

#### 导入管理
- `import_jobs`：导入任务
- `import_errors`：导入错误

## 5. API 设计规范

### 5.1 路由规范
- 统一前缀：`/api/v1/`
- 命名风格：kebab-case（如 `/heritage-items`）
- RESTful 风格：使用标准 HTTP 方法（GET/POST/PUT/DELETE）

### 5.2 响应格式
```json
{
  "code": 0,           // 0 表示成功，非 0 表示失败
  "message": "成功",   // 提示信息
  "data": {...},       // 响应数据
  "total": 100         // 列表总数（分页时使用）
}
```

### 5.3 认证方式
- JWT Bearer Token
- Header: `Authorization: Bearer <token>`

## 6. 开发环境配置

### 6.1 已完成配置
- Python 3.12.7
- Django 5.2
- MySQL 8.0+（数据库 heritage_db 已创建）
- mysqlclient（MySQL 驱动）

### 6.2 待安装依赖
- djangorestframework
- djangorestframework-simplejwt
- pandas
- openpyxl
- Pillow
- django-cors-headers

## 7. 安全考虑

### 7.1 已实施
- 数据库密码不提交到版本控制（.gitignore 已配置）
- SECRET_KEY 使用 Django 默认生成（生产环境需更换）

### 7.2 待实施
- 环境变量管理（.env 文件）
- CORS 白名单配置
- API 限流
- SQL 注入防护（Django ORM 自带）
- XSS 防护
- CSRF 防护

## 8. 部署架构（规划）

```
┌─────────────┐
│   Nginx     │  反向代理 + 静态文件服务
└─────────────┘
       ↓
┌─────────────┐
│   Gunicorn  │  WSGI 服务器
└─────────────┘
       ↓
┌─────────────┐
│   Django    │  应用服务器
└─────────────┘
       ↓
┌─────────────┐
│   MySQL     │  数据库
└─────────────┘
```

## 9. 性能优化策略（规划）

### 9.1 数据库层
- 添加索引（name, category, region 等常用查询字段）
- 使用 select_related 和 prefetch_related 优化关联查询
- 数据库连接池配置

### 9.2 应用层
- API 响应缓存（Redis）
- 分页查询（默认 20 条/页）
- 批量操作优化（bulk_create, bulk_update）

### 9.3 前端层
- ECharts 图表按需加载
- 组件懒加载
- 静态资源 CDN

## 10. 测试策略

### 10.1 单元测试
- 模型测试：字段约束、关联关系
- 序列化器测试：数据验证、转换
- 权限测试：角色权限验证

### 10.2 集成测试
- API 接口测试：请求/响应格式
- 认证测试：登录、Token 刷新
- 导入流程测试：完整导入链路

### 10.3 性能测试
- 1 万条数据导入测试
- 驾驶舱接口响应时间测试（< 3 秒）
- 并发请求测试

---

**文档版本**：v1.0  
**最后更新**：2026-02-25  
**维护者**：开发团队
