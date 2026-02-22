# 架构文档

更新时间：2026-02-16

## 1. 系统架构

**架构形态**：B/S 前后端分离
- **后端**：Django 5.2 + DRF + MySQL（端口 8000）
- **前端**：Vue 3 + Vite + Element Plus（端口 5173）

## 2. 技术栈

### 后端
| 组件 | 技术 |
|------|------|
| 框架 | Django 5.2 + DRF |
| 数据库 | MySQL 8.0 (utf8mb4) |
| 认证 | Token (djangorestframework-authtoken) |
| 文档 | drf-spectacular (OpenAPI 3.0) |
| 数据处理 | pandas, openpyxl |

### 前端
| 组件 | 技术 |
|------|------|
| 框架 | Vue 3 + Vite |
| UI库 | Element Plus |
| 图表 | ECharts |
| 状态 | Pinia |
| 路由 | Vue Router |
| 样式 | Tailwind CSS |

## 3. 项目结构

```
air-quality-data-system/
├── backend/                    # Django 后端
│   ├── air_quality_system/     # 项目配置
│   ├── apps/                   # 应用模块
│   │   ├── accounts/           # 用户认证
│   │   ├── airquality/         # 空气质量核心
│   │   ├── rules/              # 防护规则
│   │   ├── articles/           # 文章公告
│   │   └── logs/               # 系统日志
│   └── utils/                  # 公共工具
├── frontend/                   # Vue 3 前端
│   └── src/
│       ├── api/                # API 接口层
│       ├── components/         # 公共组件
│       ├── layouts/            # 布局组件
│       ├── router/             # 路由配置
│       ├── stores/             # Pinia 状态
│       └── views/              # 页面视图
├── dataSource/                 # 源数据集
└── memory-bank/                # 文档记录
```

## 4. 数据库 Schema

### 核心表
| 表名 | 说明 |
|------|------|
| accounts_user | 用户表（软删除 is_deleted） |
| airquality_province | 省份表 |
| airquality_city | 城市表 |
| airquality_monitoringstation | 监测站点表 |
| airquality_airqualitydata | 空气质量监测数据 |
| rules_protectionrule | 防护规则表（AQI区间 × 人群类型） |
| articles_article | 文章表（含公告标识） |
| articles_articlecategory | 文章分类表 |
| logs_importtask | 导入任务表 |
| logs_importtasklog | 导入失败日志表 |

## 5. API 端点

### 认证（2个）
- POST /api/auth/login/
- POST /api/auth/register/

### 用户端（15个）
- GET /api/overview/ - 全国概览
- GET /api/overview/top-cities/ - 城市排行榜
- GET /api/cities/{code}/ - 城市详情
- GET /api/stations/{code}/ - 站点详情
- GET /api/historical-data/ - 历史数据
- GET /api/analysis/compare/ - 城市对比
- GET /api/protection-guide/ - 防护指南
- GET /api/articles/ - 文章列表
- GET /api/announcements/ - 系统公告

### 管理端（13个）
- GET /api/admin/dashboard/ - 仪表盘
- POST /api/admin/data-import/ - 数据导入
- GET|PUT|DELETE /api/admin/air-quality/ - 数据管理
- GET|POST|PUT|DELETE /api/admin/rules/ - 规则管理
- GET|PUT|DELETE /api/admin/users/ - 用户管理
- GET|POST|PUT|DELETE /api/admin/articles/ - 文章管理
- GET /api/admin/logs/operations/ - 操作日志

## 6. 前端路由

### 用户端（8个）
| 路由 | 页面 | 功能 |
|------|------|------|
| /overview | Overview.vue | 全国概览（地图、排行榜） |
| /city/:code | CityDetail.vue | 城市详情 |
| /station/:code | StationDetail.vue | 站点详情 |
| /historical | HistoricalData.vue | 历史数据查询 |
| /analysis | Analysis.vue | 数据分析 |
| /protection | ProtectionGuide.vue | 防护指南 |
| /knowledge | KnowledgeBase.vue | 科普知识库 |
| /article/:id | ArticleDetail.vue | 文章详情 |

### 管理端（7个）
| 路由 | 页面 | 功能 |
|------|------|------|
| /admin/dashboard | Dashboard.vue | 仪表盘 |
| /admin/data-import | DataImport.vue | 数据导入 |
| /admin/air-quality | AirQualityManage.vue | 数据管理 |
| /admin/rules | RulesManage.vue | 规则管理 |
| /admin/users | UsersManage.vue | 用户管理 |
| /admin/articles | ArticlesManage.vue | 文章管理 |
| /admin/logs | SystemLogs.vue | 系统日志 |

## 7. 关键设计决策

### 认证与权限
- Token 认证（非 JWT）
- 管理员统一权限校验（IsAdminUser）
- 用户软删除（is_deleted 字段）

### AQI 标准
- 采用中国 HJ 633-2012 标准
- 6 个等级：0-50（优）、51-100（良）、101-150（轻度）、151-200（中度）、201-300（重度）、301-500（严重）

### 防护规则矩阵
- 6 个 AQI 区间 × 5 种人群类型 = 30 条规则
- 人群类型：一般人群、儿童、老年人、病患者、敏感人群

### 响应格式
- 统一格式：`{ code: 0, data: {...}, total: n }`
- 列表分页：page、page_size 参数

### 前端设计风格
- **用户端**：Atmospheric Data Professional（深色模式、AQI 色谱、玻璃态卡片）
- **管理端**：科学仪器美学（深色主题 #0a0e1a、青色强调 #22d3ee、JetBrains Mono 字体）

## 8. 性能要求

| 指标 | 要求 |
|------|------|
| 首页加载 | < 3 秒 |
| 列表接口 | < 500ms |
| 详情接口 | < 200ms |
| 图表渲染 | 支持 5000+ 数据点 |
| 数据导入 | 支持 10 万+ 记录 |

## 9. 待优化项

**非阻塞优化**：
- Article 模型添加 `get_announcements()` 管理器方法
- Province/City 的 code 字段统一长度为 6

**阶段三任务**：
- 前后端联调测试
- 性能压测
- 浏览器兼容性测试
- 生产环境部署配置
