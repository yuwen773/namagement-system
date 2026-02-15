# 架构文档（阶段一 `1.4` 完成后）

更新时间：2026-02-15  
当前里程碑：阶段一 `1.4`（用户端 API）已完成并通过测试。  
边界状态：阶段二 `2.1` 尚未开始。

## 1. 当前架构状态（文档本质版）

- 架构形态：B/S 前后端分离。
- 已落地范围：后端 Django + DRF、核心业务模型、数据导入能力、用户端 API（概览/详情/历史/分析/防护/文章公告）。
- 未落地范围：前端开发（阶段二）、部署优化（阶段三）。
- 统一约束：
  - 统一响应结构：`code` / `data` / `message`（分页附带 `total` / `page` / `page_size`）。
  - 全局异常处理：DRF 统一错误出口。
  - 项目要求保留明文密码逻辑（仅课题演示，禁止生产使用）。

## 2. 分层与主数据流

1. 请求入口：`urls.py` 分发到各 app 视图。
2. 业务编排：`views.py` 做参数校验、权限控制、响应包装。
3. 领域逻辑：`services.py` 处理聚合、趋势、规则匹配等可复用逻辑。
4. 数据访问：`models.py` + ORM 查询（含聚合、子查询、过滤、分页）。
5. 输出标准化：`utils/response.py` 与 `utils/exception_handler.py`。

## 3. 关键文件职责（按文件说明）

### 3.1 工程与全局配置

| 文件 | 作用 |
|---|---|
| `backend/manage.py` | Django 管理入口（`runserver` / `migrate` / `test` / `check`）。 |
| `backend/requirements.txt` | 后端依赖清单（Django/DRF/pandas/openpyxl/xlrd 等）。 |
| `backend/air_quality_system/__init__.py` | 注入 `PyMySQL` 兼容层。 |
| `backend/air_quality_system/settings.py` | 全局设置：数据库、DRF、异常处理、CORS、上传、`AUTH_USER_MODEL`。 |
| `backend/air_quality_system/settings_migrations.py` | 迁移辅助 settings（SQLite 用于迁移生成/测试）。 |
| `backend/air_quality_system/urls.py` | 根路由：挂载 airquality/rules/articles API。 |
| `backend/air_quality_system/asgi.py` | ASGI 入口。 |
| `backend/air_quality_system/wsgi.py` | WSGI 入口。 |

### 3.2 公共工具层

| 文件 | 作用 |
|---|---|
| `backend/utils/response.py` | 统一响应包装器 `APIResponse`。 |
| `backend/utils/exception_handler.py` | 全局异常处理，统一错误输出。 |
| `backend/utils/data_importer.py` | CSV/XLS/XLSX 导入、字段映射、分批入库、导入日志记录。 |

### 3.3 accounts（用户）

| 文件 | 作用 |
|---|---|
| `backend/apps/accounts/models.py` | `User` 自定义用户模型（`phone/role/status/is_deleted` + 明文密码逻辑）。 |
| `backend/apps/accounts/admin.py` | 用户后台管理配置。 |
| `backend/apps/accounts/migrations/0001_initial.py` | 用户与权限关联表初始迁移。 |

### 3.4 airquality（空气质量核心域）

| 文件 | 作用 |
|---|---|
| `backend/apps/airquality/models.py` | `Province/City/MonitoringStation/AirQualityData` 数据模型与约束。 |
| `backend/apps/airquality/serializers.py` | 地图数据、历史数据输出序列化。 |
| `backend/apps/airquality/filters.py` | 历史数据筛选条件（城市/站点/日期范围）。 |
| `backend/apps/airquality/services.py` | 快照、24h 趋势、最新站点记录等可复用查询逻辑。 |
| `backend/apps/airquality/views.py` | 阶段 `1.3` 导入 API + 阶段 `1.4.1~1.4.4` 用户端 API。 |
| `backend/apps/airquality/urls.py` | 导入 API、概览 API、详情 API、历史 API、分析 API 路由。 |
| `backend/apps/airquality/admin.py` | 空气质量相关模型后台管理。 |
| `backend/apps/airquality/management/commands/import_data_file.py` | 命令行触发导入任务。 |
| `backend/apps/airquality/migrations/0001_initial.py` | airquality 初始迁移。 |

### 3.5 rules（防护规则域）

| 文件 | 作用 |
|---|---|
| `backend/apps/rules/models.py` | `ProtectionRule` 模型，含 AQI 区间约束与重叠校验。 |
| `backend/apps/rules/services.py` | 规则匹配服务 `RuleMatcherService`。 |
| `backend/apps/rules/views.py` | `ProtectionGuideView`（防护建议 + 6/12h 趋势预警）。 |
| `backend/apps/rules/urls.py` | `/api/protection-guide/` 路由。 |
| `backend/apps/rules/admin.py` | 规则后台管理。 |
| `backend/apps/rules/migrations/0001_initial.py` | rules 初始迁移。 |

### 3.6 articles（文章/公告域）

| 文件 | 作用 |
|---|---|
| `backend/apps/articles/models.py` | `ArticleCategory`、`Article` 模型。 |
| `backend/apps/articles/serializers.py` | 文章列表、详情、分类输出序列化。 |
| `backend/apps/articles/views.py` | 文章列表/详情、分类列表、公告列表 API。 |
| `backend/apps/articles/urls.py` | `/api/articles/`、`/api/categories/`、`/api/announcements/` 路由。 |
| `backend/apps/articles/admin.py` | 文章后台管理。 |
| `backend/apps/articles/migrations/0001_initial.py` | articles 初始迁移。 |

### 3.7 logs（日志与导入任务域）

| 文件 | 作用 |
|---|---|
| `backend/apps/logs/models.py` | `OperationLog/ErrorLog/ImportTask/ImportTaskLog` 模型。 |
| `backend/apps/logs/serializers.py` | 导入任务与导入错误日志序列化。 |
| `backend/apps/logs/admin.py` | 日志后台管理。 |
| `backend/apps/logs/migrations/0001_initial.py` | logs 初始迁移。 |

### 3.8 测试文件（阶段一 `1.4` 回归）

| 文件 | 作用 |
|---|---|
| `backend/apps/airquality/tests.py` | 覆盖概览、详情、趋势、历史导出、分析接口。 |
| `backend/apps/rules/tests.py` | 覆盖防护指南接口与异常城市场景。 |
| `backend/apps/articles/tests.py` | 覆盖文章/分类/公告接口与发布状态约束。 |

## 4. 已交付 API（阶段一）

### 4.1 阶段 `1.3` 管理端导入 API

- `POST /api/admin/data-import/`
- `GET /api/admin/data-import/tasks/`
- `GET /api/admin/data-import/tasks/{task_id}/`
- `GET /api/admin/data-import/tasks/{task_id}/logs/`

### 4.2 阶段 `1.4` 用户端 API

- `GET /api/overview/`
- `GET /api/overview/top-cities/`
- `GET /api/cities/{code}/`
- `GET /api/cities/{code}/trend/`
- `GET /api/stations/{code}/`
- `GET /api/stations/{code}/trend/`
- `GET /api/historical-data/`
- `GET /api/historical-data/export/`
- `POST /api/analysis/compare/`
- `GET /api/analysis/correlation/`
- `GET /api/analysis/distribution/`
- `GET /api/protection-guide/`
- `GET /api/articles/`
- `GET /api/articles/{id}/`
- `GET /api/categories/`
- `GET /api/announcements/`

## 5. 架构洞见（阶段一 `1.4` 的关键决策）

1. `airquality/services.py` 把快照和趋势聚合从视图中剥离，降低视图耦合，便于后续前端联调和复用。
2. 概览接口采用“每站点最新记录”子查询策略，避免混入历史旧数据导致全国均值失真。
3. 历史导出接口使用 `pandas` 输出 CSV/XLSX；同时把 `REST_FRAMEWORK.URL_FORMAT_OVERRIDE` 设为 `None`，避免 `format` 查询参数冲突。
4. 防护建议采用“规则匹配服务 + 趋势预测”结构，后续可在不改接口契约的前提下替换预测算法。
5. 缓存策略先应用在首页概览和 Top 城市接口（60 秒），在数据实时性与响应速度之间取平衡。

## 6. 数据库 Schema（完整）

说明：以下为当前代码从零迁移后的完整 schema（逻辑完整，不省略任何表）。

### 6.1 Django 基础表

#### `django_migrations`
- `id` bigint PK
- `app` varchar(255)
- `name` varchar(255)
- `applied` datetime(6)

#### `django_content_type`
- `id` int PK
- `app_label` varchar(100)
- `model` varchar(100)
- 约束：`(app_label, model)` 唯一

#### `auth_permission`
- `id` int PK
- `name` varchar(255)
- `content_type_id` int FK -> `django_content_type.id`
- `codename` varchar(100)
- 约束：`(content_type_id, codename)` 唯一

#### `auth_group`
- `id` int PK
- `name` varchar(150) UNIQUE

#### `auth_group_permissions`
- `id` bigint PK
- `group_id` int FK -> `auth_group.id`
- `permission_id` int FK -> `auth_permission.id`
- 约束：`(group_id, permission_id)` 唯一

#### `django_admin_log`
- `id` int PK
- `action_time` datetime(6)
- `object_id` longtext NULL
- `object_repr` varchar(200)
- `action_flag` smallint unsigned
- `change_message` longtext
- `content_type_id` int NULL FK -> `django_content_type.id`
- `user_id` bigint FK -> `accounts_user.id`

#### `django_session`
- `session_key` varchar(40) PK
- `session_data` longtext
- `expire_date` datetime(6) INDEX

### 6.2 accounts

#### `accounts_user`
- `id` bigint PK
- `password` varchar(128)（按课题要求明文存储）
- `last_login` datetime(6) NULL
- `is_superuser` tinyint(1)
- `username` varchar(150) UNIQUE
- `first_name` varchar(150)
- `last_name` varchar(150)
- `email` varchar(254)
- `is_staff` tinyint(1)
- `is_active` tinyint(1)
- `date_joined` datetime(6)
- `phone` varchar(20) NULL
- `role` varchar(20)（`USER` / `ADMIN`）
- `status` tinyint(1)
- `is_deleted` tinyint(1) DEFAULT 0

#### `accounts_user_groups`
- `id` bigint PK
- `user_id` bigint FK -> `accounts_user.id`
- `group_id` int FK -> `auth_group.id`
- 约束：`(user_id, group_id)` 唯一

#### `accounts_user_user_permissions`
- `id` bigint PK
- `user_id` bigint FK -> `accounts_user.id`
- `permission_id` int FK -> `auth_permission.id`
- 约束：`(user_id, permission_id)` 唯一

### 6.3 airquality

#### `airquality_province`
- `id` bigint PK
- `name` varchar(100)
- `code` varchar(12) UNIQUE（6 位行政区划码）
- `level` varchar(20)

#### `airquality_city`
- `id` bigint PK
- `province_id` bigint FK -> `airquality_province.id`
- `name` varchar(100)
- `code` varchar(12) UNIQUE（6 位行政区划码）
- `longitude` decimal(10,6)
- `latitude` decimal(10,6)

#### `airquality_monitoringstation`
- `id` bigint PK
- `city_id` bigint FK -> `airquality_city.id`
- `name` varchar(200)
- `code` varchar(50) UNIQUE
- `address` varchar(255)
- `station_type` varchar(50)

#### `airquality_airqualitydata`
- `id` bigint PK
- `station_id` bigint FK -> `airquality_monitoringstation.id`
- `monitor_time` datetime(6) INDEX
- `aqi` int unsigned（0-500）
- `pm25` decimal(10,2) NULL
- `pm10` decimal(10,2) NULL
- `so2` decimal(10,2) NULL
- `no2` decimal(10,2) NULL
- `co` decimal(10,2) NULL
- `o3` decimal(10,2) NULL
- `quality_level` varchar(20)（按 `HJ 633-2012` 计算）
- 约束：`(station_id, monitor_time)` 唯一（`uq_airq_station_monitor_time`）

### 6.4 rules

#### `rules_protectionrule`
- `id` bigint PK
- `rule_name` varchar(100)
- `min_aqi` int unsigned
- `max_aqi` int unsigned
- `population_type` varchar(20)（`GENERAL` / `CHILDREN` / `ELDERLY` / `PATIENTS` / `SENSITIVE`）
- `advice` longtext
- `is_enabled` tinyint(1) DEFAULT 1
- 约束：`min_aqi <= max_aqi`（`ck_rule_min_le_max`）
- 业务约束：同一 `population_type` 的 AQI 区间闭区间不可重叠

### 6.5 articles

#### `articles_articlecategory`
- `id` bigint PK
- `name` varchar(100) UNIQUE
- `sort` int DEFAULT 0

#### `articles_article`
- `id` bigint PK
- `title` varchar(255)
- `category_id` bigint FK -> `articles_articlecategory.id`
- `content` longtext
- `status` varchar(20)（`DRAFT` / `PUBLISHED` / `OFFLINE`）
- `is_announcement` tinyint(1) DEFAULT 0
- `sort_order` int DEFAULT 0
- `created_at` datetime(6)
- `updated_at` datetime(6)
- 索引：`(status, is_announcement)`

### 6.6 logs

#### `logs_operationlog`
- `id` bigint PK
- `user_id` bigint FK -> `accounts_user.id`
- `operation_type` varchar(50)
- `operation_content` longtext
- `ip_address` varchar(45)
- `operation_time` datetime(6)

#### `logs_errorlog`
- `id` bigint PK
- `error_type` varchar(100)
- `error_message` longtext
- `stack_trace` longtext
- `occurred_at` datetime(6)

#### `logs_importtask`
- `id` bigint PK
- `task_id` varchar(64) UNIQUE
- `file_name` varchar(255)
- `file_type` varchar(20)
- `status` varchar(20)（`PENDING` / `RUNNING` / `SUCCESS` / `FAILED`）
- `total_count` int DEFAULT 0
- `success_count` int DEFAULT 0
- `failed_count` int DEFAULT 0
- `initiator_id` bigint FK -> `accounts_user.id`
- `start_time` datetime(6)
- `end_time` datetime(6) NULL

#### `logs_importtasklog`
- `id` bigint PK
- `task_id` bigint FK -> `logs_importtask.id`
- `row_number` int
- `error_reason` longtext
- `raw_data_snippet` longtext NULL
- `created_at` datetime(6)

## 7. 下一步边界

- 阶段一 `1.4` 已收口。
- 在收到明确指令前，不进入阶段二 `2.1`。
