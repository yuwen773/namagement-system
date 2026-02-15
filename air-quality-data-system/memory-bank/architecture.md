# 架构文档（阶段一 `1.3` 完成后）

更新时间：2026-02-15  
当前里程碑：阶段一 `1.3`（数据导入功能）已完成；在确认后未继续实施 `1.4`。

## 1. 架构现状概览

- 架构形态：B/S 前后端分离；当前仓库已落地后端 Django 项目骨架与数据库模型，前端尚未开始。
- 后端技术：Django 5.2 + Django REST Framework；MySQL 作为主库。
- 关键约束（来自实施计划）：鉴权使用简单 Token（后续实现）；密码按课题要求“明文存储与明文校验”（已在自定义用户模型中落地，禁止用于生产）。

## 2. 目录与文件职责（以关键文件为主）

### 2.1 工程入口层

| 路径 | 作用 |
|---|---|
| `backend/manage.py` | Django 命令入口（`runserver`/`migrate`/`check`/`createsuperuser` 等）。 |
| `backend/requirements.txt` | 后端依赖版本锁定（Django/DRF/CORS/filter/spectacular/PyMySQL/pandas/openpyxl/xlrd）。 |

### 2.2 项目配置层（`backend/air_quality_system/`）

| 路径 | 作用 |
|---|---|
| `backend/air_quality_system/__init__.py` | 安装 `PyMySQL` 兼容层（将 `pymysql` 注入为 `MySQLdb`）。 |
| `backend/air_quality_system/settings.py` | 全局配置中心：MySQL 连接、DRF/CORS/OpenAPI、`AUTH_USER_MODEL`、上传文件（`MEDIA_*`）、统一异常响应等。 |
| `backend/air_quality_system/settings_migrations.py` | 迁移生成辅助 settings：当 MySQL 迁移历史不一致时，允许用 SQLite 生成迁移文件（不改变生产目标库为 MySQL 的事实）。 |
| `backend/air_quality_system/urls.py` | 根路由汇总：`/admin/`、`/api/`；`/` 临时重定向到 `/api/`；`apps.airquality.urls` 挂载导入相关 API。 |
| `backend/air_quality_system/asgi.py` | ASGI 入口。 |
| `backend/air_quality_system/wsgi.py` | WSGI 入口。 |

### 2.3 通用工具层（`backend/utils/`）

| 路径 | 作用 |
|---|---|
| `backend/utils/response.py` | 统一 API 响应结构（`code/data/message`，列表可带 `total/page/page_size`）。 |
| `backend/utils/exception_handler.py` | DRF 全局异常处理器：把常见 4xx/5xx 转换为统一响应。 |
| `backend/utils/data_importer.py` | 数据导入核心实现：CSV/Excel 解析、模板字段映射、分批入库、逐行错误收集；写入 `ImportTask/ImportTaskLog`。 |

### 2.4 业务应用层（`backend/apps/`）

| app | 路径 | 作用 |
|---|---|---|
| accounts | `backend/apps/accounts/models.py` | 自定义用户模型 `User(AbstractUser)`，包含 `phone/role/status/is_deleted`，并按课题要求覆写密码为明文。 |
| accounts | `backend/apps/accounts/admin.py` | 用户模型 Admin 注册与最小检索能力。 |
| airquality | `backend/apps/airquality/models.py` | 省/市/监测站点/空气质量数据模型与约束（行政区划码校验、AQI 分级、唯一约束等）。 |
| airquality | `backend/apps/airquality/admin.py` | 省/市/站点/空气质量数据 Admin 注册，便于手工验证。 |
| airquality | `backend/apps/airquality/views.py` | 数据导入 API：上传返回 `task_id`；任务列表/详情；失败日志查询。 |
| airquality | `backend/apps/airquality/urls.py` | 导入相关 API 路由（挂载到 `/api/`）。 |
| airquality | `backend/apps/airquality/management/commands/import_data_file.py` | 管理命令：从本地文件触发导入（便于脚本化/压测）。 |
| rules | `backend/apps/rules/models.py` | 防护规则 `ProtectionRule`，含区间合法性与区间重叠校验。 |
| rules | `backend/apps/rules/admin.py` | 防护规则 Admin 注册。 |
| articles | `backend/apps/articles/models.py` | 内容模型：分类 `ArticleCategory`、文章/公告 `Article`。 |
| articles | `backend/apps/articles/admin.py` | 内容模型 Admin 注册。 |
| logs | `backend/apps/logs/models.py` | 系统日志与导入任务：操作日志/异常日志/导入任务/导入明细日志。 |
| logs | `backend/apps/logs/admin.py` | 日志与导入任务 Admin 注册。 |
| logs | `backend/apps/logs/serializers.py` | 导入任务与日志的序列化（供导入 API 返回）。 |

### 2.5 迁移层（`backend/apps/*/migrations/`）

| 路径 | 作用 |
|---|---|
| `backend/apps/accounts/migrations/0001_initial.py` | accounts 初始迁移（创建 `accounts_user` 及其与权限相关的多对多表）。 |
| `backend/apps/airquality/migrations/0001_initial.py` | airquality 初始迁移（省/市/站点/空气质量数据）。 |
| `backend/apps/rules/migrations/0001_initial.py` | rules 初始迁移（防护规则）。 |
| `backend/apps/articles/migrations/0001_initial.py` | articles 初始迁移（分类与文章）。 |
| `backend/apps/logs/migrations/0001_initial.py` | logs 初始迁移（操作日志/异常日志/导入任务/导入日志）。 |

## 3. 关键架构决策与实现要点

- 自定义用户模型：`AUTH_USER_MODEL = accounts.User`；按课题要求实现“明文密码存储与校验”（仅用于课题演示，禁止用于生产）。
- 约束分层：唯一约束/索引尽量下沉到 DB；业务约束在模型层 `full_clean()` 做校验。
- 数据导入：通过 `ImportTask/ImportTaskLog` 记录导入任务与逐行失败原因，便于后台定位问题。
- 批量写入注意事项：`bulk_create` 不会触发 `Model.save()`；导入 `AirQualityData` 时需显式计算 `quality_level`。
- 迁移历史风险：若 `1.1` 先在 MySQL 迁移（存在 `auth_user` 历史），再在 `1.2` 切换 `AUTH_USER_MODEL` 可能出现 `InconsistentMigrationHistory`；推荐使用全新库执行迁移。

## 4. 数据库 Schema（完整）

说明：以下为“按当前代码从零迁移到 MySQL 后”的规范 schema（即推荐的干净安装结果）。

### 4.1 Django 基础表

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

### 4.2 accounts（用户与权限关联）

#### `accounts_user`
- `id` bigint PK
- `password` varchar(128) 备注：实现为明文（课题要求）
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
- `role` varchar(20) 取值：`USER`/`ADMIN`
- `status` tinyint(1) 备注：业务启用/禁用
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

### 4.3 airquality（基础数据与监测数据）

#### `airquality_province`
- `id` bigint PK
- `name` varchar(100)
- `code` varchar(12) UNIQUE 备注：校验为 6 位数字（国标行政区划码）
- `level` varchar(20)

#### `airquality_city`
- `id` bigint PK
- `province_id` bigint FK -> `airquality_province.id`
- `name` varchar(100)
- `code` varchar(12) UNIQUE 备注：校验为 6 位数字（国标行政区划码）
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
- `aqi` int unsigned 备注：范围校验 0-500
- `pm25` decimal(10,2) NULL
- `pm10` decimal(10,2) NULL
- `so2` decimal(10,2) NULL
- `no2` decimal(10,2) NULL
- `co` decimal(10,2) NULL
- `o3` decimal(10,2) NULL
- `quality_level` varchar(20) 备注：按 `HJ 633-2012` 边界自动计算
- 约束：`(station_id, monitor_time)` 唯一（`uq_airq_station_monitor_time`）

### 4.4 rules（防护规则）

#### `rules_protectionrule`
- `id` bigint PK
- `rule_name` varchar(100)
- `min_aqi` int unsigned
- `max_aqi` int unsigned
- `population_type` varchar(20) 取值：`GENERAL`/`CHILDREN`/`ELDERLY`/`PATIENTS`/`SENSITIVE`
- `advice` longtext
- `is_enabled` tinyint(1) DEFAULT 1
- 约束：`min_aqi <= max_aqi`（`ck_rule_min_le_max`）
- 业务约束：同一 `population_type` 内 AQI 闭区间 `[min_aqi, max_aqi]` 不允许重叠（模型层校验）

### 4.5 articles（文章与公告）

#### `articles_articlecategory`
- `id` bigint PK
- `name` varchar(100) UNIQUE
- `sort` int DEFAULT 0

#### `articles_article`
- `id` bigint PK
- `title` varchar(255)
- `category_id` bigint FK -> `articles_articlecategory.id`
- `content` longtext
- `status` varchar(20) 取值：`DRAFT`/`PUBLISHED`/`OFFLINE`
- `is_announcement` tinyint(1) DEFAULT 0
- `sort_order` int DEFAULT 0
- `created_at` datetime(6)
- `updated_at` datetime(6)
- 索引：`(status, is_announcement)`

### 4.6 logs（操作/异常/导入任务）

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
- `status` varchar(20) 取值：`PENDING`/`RUNNING`/`SUCCESS`/`FAILED`
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

## 5. 下一步边界

- 阶段一 `1.4` 尚未开始；进入 `1.4` 前应先确认本地数据库是否为“干净安装”（避免迁移历史不一致）。
