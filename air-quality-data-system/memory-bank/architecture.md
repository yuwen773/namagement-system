# 架构文档（阶段一 `1.5` 完成后，文档本质版）

更新时间：2026-02-15  
当前里程碑：阶段一 `1.5`（管理端 API）已完成并通过测试。  
边界状态：阶段一 `1.6` 尚未开始；阶段二 `2.1` 尚未开始。

## 1. 当前架构状态

- 架构形态：B/S 前后端分离（Django + DRF 后端，Vue 3 前端待开发）。
- 已落地范围：
  - 核心业务模型（accounts / airquality / rules / articles / logs）
  - 数据导入能力（上传、任务跟踪、导入日志）
  - 用户端 API（概览、详情、历史、分析、防护、文章）
  - 管理端 API（仪表盘、空气质量数据管理、规则管理、用户管理、文章/分类管理、日志查询）
- 未落地范围：
  - 阶段一 `1.6` 认证与权限（简单 Token）
  - 阶段一 `1.7` API 文档导出
  - 阶段二前端与阶段三集成优化
- 全局约束：
  - 统一响应结构：`code` / `data` / `message`（分页附带 `total` / `page` / `page_size`）
  - 全局异常处理：`utils.exception_handler.custom_exception_handler`
  - 密码策略遵循课题要求：明文存储与明文校验（仅演示用途）

## 2. 分层与主数据流

1. 路由层：`air_quality_system/urls.py` 聚合各 app URL。  
2. 接口层：`views.py` 负责参数校验、权限控制、响应包装。  
3. 领域层：`services.py` 负责聚合、规则匹配、日志写入等复用逻辑。  
4. 数据层：`models.py` + Django ORM（过滤、聚合、分页、子查询）。  
5. 横切层：统一响应、异常处理、中间件日志。

## 3. 关键文件职责（按文件）

### 3.1 工程与全局配置

| 文件 | 作用 |
|---|---|
| `backend/manage.py` | Django 管理入口（`runserver` / `migrate` / `test` / `check`）。 |
| `backend/requirements.txt` | 后端依赖清单（Django/DRF/pandas/openpyxl/xlrd 等）。 |
| `backend/air_quality_system/__init__.py` | 注入 `PyMySQL` 兼容层。 |
| `backend/air_quality_system/settings.py` | 全局配置：数据库、DRF、CORS、异常处理、中间件、上传限制。 |
| `backend/air_quality_system/settings_migrations.py` | 迁移辅助配置（SQLite）。 |
| `backend/air_quality_system/urls.py` | 根路由：挂载 accounts/airquality/rules/articles/logs API。 |
| `backend/air_quality_system/asgi.py` | ASGI 入口。 |
| `backend/air_quality_system/wsgi.py` | WSGI 入口。 |

### 3.2 公共工具

| 文件 | 作用 |
|---|---|
| `backend/utils/response.py` | 统一响应包装类 `APIResponse`。 |
| `backend/utils/exception_handler.py` | 全局异常处理与统一错误输出。 |
| `backend/utils/data_importer.py` | CSV/XLS/XLSX 导入、字段映射、分批入库、导入错误收集。 |

### 3.3 accounts（用户域）

| 文件 | 作用 |
|---|---|
| `backend/apps/accounts/models.py` | 自定义用户模型 `User`（`phone/role/status/is_deleted`，明文密码逻辑）。 |
| `backend/apps/accounts/serializers.py` | 管理端用户序列化器 `UserManageSerializer`。 |
| `backend/apps/accounts/views.py` | 管理端用户管理 API（列表/更新/逻辑删除）。 |
| `backend/apps/accounts/urls.py` | `/api/admin/users/` 路由。 |
| `backend/apps/accounts/admin.py` | Django Admin 用户管理配置。 |
| `backend/apps/accounts/tests.py` | 用户管理 API 回归测试。 |
| `backend/apps/accounts/migrations/0001_initial.py` | accounts 初始迁移。 |

### 3.4 airquality（空气质量核心域）

| 文件 | 作用 |
|---|---|
| `backend/apps/airquality/models.py` | `Province/City/MonitoringStation/AirQualityData` 及约束。 |
| `backend/apps/airquality/serializers.py` | 用户端与管理端空气质量数据序列化。 |
| `backend/apps/airquality/filters.py` | 历史数据筛选条件。 |
| `backend/apps/airquality/services.py` | 快照、趋势、子查询聚合等复用逻辑。 |
| `backend/apps/airquality/views.py` | 导入 API、用户端 API、管理端仪表盘与数据管理 API。 |
| `backend/apps/airquality/urls.py` | `/api/overview/*`、`/api/historical-data/*`、`/api/admin/*` 路由。 |
| `backend/apps/airquality/admin.py` | Django Admin 空气质量模型管理。 |
| `backend/apps/airquality/tests.py` | 导入、用户端、管理端 API 回归测试。 |
| `backend/apps/airquality/management/commands/import_data_file.py` | 命令行导入触发。 |
| `backend/apps/airquality/migrations/0001_initial.py` | airquality 初始迁移。 |

### 3.5 rules（防护规则域）

| 文件 | 作用 |
|---|---|
| `backend/apps/rules/models.py` | `ProtectionRule` 模型（区间约束、重叠校验）。 |
| `backend/apps/rules/serializers.py` | 规则管理序列化器。 |
| `backend/apps/rules/services.py` | 规则匹配服务 `RuleMatcherService`。 |
| `backend/apps/rules/views.py` | 用户端防护指南 API + 管理端规则管理 API。 |
| `backend/apps/rules/urls.py` | `/api/protection-guide/`、`/api/admin/rules/` 路由。 |
| `backend/apps/rules/admin.py` | Django Admin 规则管理。 |
| `backend/apps/rules/tests.py` | 防护指南与规则管理回归测试。 |
| `backend/apps/rules/migrations/0001_initial.py` | rules 初始迁移。 |

### 3.6 articles（文章与公告域）

| 文件 | 作用 |
|---|---|
| `backend/apps/articles/models.py` | `ArticleCategory`、`Article` 模型。 |
| `backend/apps/articles/serializers.py` | 用户端与管理端文章/分类序列化。 |
| `backend/apps/articles/views.py` | 用户端文章 API + 管理端文章/分类管理 API。 |
| `backend/apps/articles/urls.py` | `/api/articles/*`、`/api/categories/`、`/api/announcements/`、`/api/admin/articles/`、`/api/admin/categories/`。 |
| `backend/apps/articles/admin.py` | Django Admin 文章与分类管理。 |
| `backend/apps/articles/tests.py` | 用户端与管理端文章接口回归测试。 |
| `backend/apps/articles/migrations/0001_initial.py` | articles 初始迁移。 |

### 3.7 logs（系统日志与导入任务域）

| 文件 | 作用 |
|---|---|
| `backend/apps/logs/models.py` | `OperationLog/ErrorLog/ImportTask/ImportTaskLog` 模型。 |
| `backend/apps/logs/serializers.py` | 导入任务、操作日志、异常日志序列化。 |
| `backend/apps/logs/services.py` | 日志写入辅助（IP 获取、操作日志记录）。 |
| `backend/apps/logs/middleware.py` | 管理端写操作自动记录 + 未处理异常捕获入库。 |
| `backend/apps/logs/views.py` | 管理端日志查询 API。 |
| `backend/apps/logs/urls.py` | `/api/admin/logs/operations/`、`/api/admin/logs/errors/` 路由。 |
| `backend/apps/logs/admin.py` | Django Admin 日志管理。 |
| `backend/apps/logs/tests.py` | 日志查询与中间件行为测试。 |
| `backend/apps/logs/migrations/0001_initial.py` | logs 初始迁移。 |

## 4. 已交付 API（阶段一）

### 4.1 `1.3` 管理端导入 API

- `POST /api/admin/data-import/`
- `GET /api/admin/data-import/tasks/`
- `GET /api/admin/data-import/tasks/{task_id}/`
- `GET /api/admin/data-import/tasks/{task_id}/logs/`

### 4.2 `1.4` 用户端 API

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

### 4.3 `1.5` 管理端 API

- `GET /api/admin/dashboard/`
- `GET|PUT|DELETE /api/admin/air-quality/`
- `GET|POST|PUT|DELETE /api/admin/rules/`
- `GET|PUT|DELETE /api/admin/users/`
- `GET|POST|PUT|DELETE /api/admin/articles/`
- `GET|POST|PUT|DELETE /api/admin/categories/`
- `GET /api/admin/logs/operations/`
- `GET /api/admin/logs/errors/`

## 5. 架构洞见（`1.5`）

1. 管理端与用户端 API 继续复用统一响应与统一异常，不在业务视图里分散拼装错误格式。  
2. 通过 `IsAdminUser` 快速收口管理端权限，后续 `1.6` 再替换为 Token 鉴权链路。  
3. 管理写操作日志与异常日志下沉到 `logs/middleware.py`，减少每个视图重复打点代码。  
4. 用户管理使用软删除（`is_deleted`）保留审计链路，默认查询排除软删用户。  
5. 数据管理与规则管理都支持批量操作，接口契约稳定，便于后续前端后台批处理。  

## 6. 数据库 Schema（完整）

说明：以下为当前代码从零迁移后的完整 schema（不省略任何表）。

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
- 业务约束：同一 `population_type` 的 AQI 闭区间不可重叠

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

- 阶段一 `1.5` 已收口并验证通过。
- 在收到明确指令前，不进入阶段一 `1.6`。
