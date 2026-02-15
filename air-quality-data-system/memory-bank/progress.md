# 开发进度记录

## 2026-02-15 - 阶段一 `1.1` 项目初始化（已完成）

### 本次完成范围（严格限定在 `1.1`）
- 完成 `1.1.1` Django 项目结构初始化
- 完成 `1.1.2` MySQL 连接配置与数据库初始化
- 完成 `1.1.3` DRF/CORS/过滤/OpenAPI 基础配置
- 明确未开始 `1.2` 的任何子步骤

### 具体变更
- 新建后端工程与目录
- 注册业务 app（`apps.accounts`/`apps.airquality`/`apps.rules`/`apps.articles`/`apps.logs`）
- 配置 MySQL（默认 `air_quality_db@127.0.0.1:3307`，字符集 `utf8mb4`，时区 `Asia/Shanghai`，支持 `DB_*` 环境变量覆盖）
- 配置 DRF 及周边组件（`djangorestframework`/`django-cors-headers`/`django-filter`/`drf-spectacular`）
- URL：根路径 `/` 临时重定向到 `/api/`，预留 `DefaultRouter` 入口

### 验证记录（当时）
- `python backend/manage.py check` 通过
- `python backend/manage.py migrate` 完成内置表迁移
- `GET /` 返回 `302`，`GET /api/` 返回 `200`

### 给后续开发者的注意事项
- `1.2` 完成前，数据库仅包含 Django 内置表，不包含任何业务表
- `AUTH_USER_MODEL` 计划在 `1.2.3` 切换

## 2026-02-15 - 阶段一 `1.2` 数据库模型设计（已完成，测试通过）

### 本次完成范围（`1.2.*`）
- `1.2.1` 创建基础数据模型（省/市/站点）并添加行政区划码格式校验
- `1.2.2` 创建空气质量监测数据模型（含 AQI 分级自动计算、索引与唯一约束）
- `1.2.3` 创建自定义用户模型并切换 `AUTH_USER_MODEL`
- `1.2.4` 创建防护规则模型（含区间重叠校验）
- `1.2.5` 创建文章/公告模型
- `1.2.6` 创建系统日志与导入任务模型

### 具体变更（关键文件）
- `backend/air_quality_system/settings.py`：新增 `AUTH_USER_MODEL = "accounts.User"`。
- `backend/apps/accounts/models.py`：新增 `User(AbstractUser)`（`phone/role/status/is_deleted`）；按实施计划要求覆写 `set_password/check_password` 实现“明文存储与明文校验”（仅为满足课题要求，禁止用于生产）。
- `backend/apps/airquality/models.py`：新增 `Province/City/MonitoringStation/AirQualityData`；`AirQualityData.monitor_time` 索引；`(station, monitor_time)` 唯一约束；按 `HJ 633-2012` 计算 `quality_level`。
- `backend/apps/rules/models.py`：新增 `ProtectionRule`；`min_aqi <= max_aqi`（DB 约束）；同一 `population_type` 内区间不重叠（应用层校验）。
- `backend/apps/articles/models.py`：新增 `ArticleCategory/Article`。
- `backend/apps/logs/models.py`：新增 `OperationLog/ErrorLog/ImportTask/ImportTaskLog`。
- `backend/apps/*/admin.py`：为所有新模型补齐最小 Admin 注册，便于手工验证。
- `backend/apps/*/migrations/0001_initial.py`：生成各 app 初始迁移文件。
- `backend/air_quality_system/settings_migrations.py`：新增“迁移生成辅助 settings”，用于迁移历史不一致时对着 SQLite 生成迁移文件。

### 验证记录（本次）
- 用户反馈：测试通过

### 已知注意事项（非常重要）
- 如果本地 MySQL 数据库是在 `1.1` 阶段先跑了迁移（默认用户表为 `auth_user`），在 `1.2` 切换 `AUTH_USER_MODEL` 后可能出现 `InconsistentMigrationHistory`。
- 建议做法：对 `1.2` 使用全新数据库（删库重建或更换库名）后再执行 `python backend/manage.py migrate`，保证 schema 与迁移历史一致。

## 2026-02-15 - 阶段一 `1.3` 数据导入功能（已完成，测试通过）

### 本次完成范围（`1.3.*`）
- `1.3.1` 创建数据导入工具模块（CSV/Excel 解析、字段校验、分批入库、逐行错误收集）
- `1.3.2` 创建数据导入 API（上传返回 `task_id`，任务列表/详情/日志查询）

### 具体变更（关键文件）
- `backend/utils/data_importer.py`：导入模板与字段别名映射（`provinces/cities/stations/air_quality_data`）；CSV 分块读取；分批 `bulk_create`；逐行错误写入 `logs_importtasklog`；导入时显式计算 `quality_level`。
- `backend/apps/airquality/views.py`：新增导入相关 API（上传、任务列表、任务详情、任务日志）。
- `backend/apps/airquality/urls.py`：导入 API 路由挂载。
- `backend/apps/logs/serializers.py`：导入任务与任务日志序列化（供 API 返回）。
- `backend/air_quality_system/settings.py`：增加 `MEDIA_ROOT/MEDIA_URL` 与上传大小限制；启用 `utils.exception_handler.custom_exception_handler`；增加 `DATA_IMPORT_ASYNC`。
- `backend/air_quality_system/urls.py`：include `apps.airquality.urls`（导入 API 挂载到 `/api/` 下）。
- `backend/apps/airquality/management/commands/import_data_file.py`：新增管理命令（脚本化导入/压测）。
- `backend/requirements.txt`：增加 `pandas/openpyxl/xlrd` 支持 CSV/Excel 解析。

### 验证记录（本次）
- 用户反馈：测试通过

## 2026-02-15 - 阶段一 `1.4` 用户端 API 开发（已完成，测试通过）

### 本次完成范围（`1.4.*`）
- `1.4.1` 首页数据 API：全国概览、地图数据、Top 城市（最佳/最差）
- `1.4.2` 城市/站点详情与 24 小时趋势 API
- `1.4.3` 历史数据查询 API：过滤、分页、排序、CSV/XLSX 导出
- `1.4.4` 数据分析 API：城市对比、污染物相关性、AQI 分布
- `1.4.5` 防护指南 API：规则匹配、一般/敏感人群建议、未来 6/12 小时简易预警
- `1.4.6` 科普文章与公告 API：文章列表/详情、分类列表、公告列表

### 具体变更（关键文件）
- `backend/apps/airquality/views.py`：在保留 `1.3` 导入接口的同时，新增并实现用户端 `1.4.1~1.4.4` 全部 API。
- `backend/apps/airquality/urls.py`：补齐用户端 API 路由（overview、cities、stations、historical-data、analysis）。
- `backend/apps/airquality/services.py`：新增空气质量服务层（最新快照、小时聚合趋势、最新站点数据子查询）。
- `backend/apps/airquality/serializers.py`：新增地图数据与历史数据序列化器。
- `backend/apps/airquality/filters.py`：新增历史数据过滤器（城市、站点、日期范围）。
- `backend/apps/rules/views.py`：新增 `ProtectionGuideView`（防护建议 + 趋势预警）。
- `backend/apps/rules/services.py`：新增规则匹配服务 `RuleMatcherService`。
- `backend/apps/rules/urls.py`：新增 `/api/protection-guide/` 路由。
- `backend/apps/articles/views.py`：新增用户端文章、分类、公告查询 API。
- `backend/apps/articles/serializers.py`：新增文章/分类序列化器。
- `backend/apps/articles/urls.py`：新增 `/api/articles/`、`/api/categories/`、`/api/announcements/` 路由。
- `backend/air_quality_system/urls.py`：新增挂载 `apps.rules.urls`、`apps.articles.urls`。
- `backend/air_quality_system/settings.py`：新增 `REST_FRAMEWORK.URL_FORMAT_OVERRIDE = None`，避免 `format` 查询参数与 DRF 格式后缀冲突（历史导出接口已验证）。

### 验证记录（本次）
- 本地静态检查通过：`python manage.py check --settings=air_quality_system.settings_migrations`
- 新增接口测试通过：`python manage.py test apps.airquality.tests apps.rules.tests apps.articles.tests --settings=air_quality_system.settings_migrations`
- 用户验收反馈：测试通过

### 边界确认
- 未开始阶段二 `2.1`。

## 2026-02-15 - 阶段一 `1.5` 管理端 API 开发（已完成，测试通过）

### 本次完成范围（`1.5.*`）
- `1.5.1` 管理后台仪表盘 API：系统运行时间、最近导入时间、数据统计、用户统计、最近导入任务状态
- `1.5.2` 空气质量数据管理 API：分页查询、单条更新、单条删除、批量删除
- `1.5.3` 防护规则管理 API：CRUD、AQI 区间校验、批量启用/禁用
- `1.5.4` 用户管理 API：默认过滤软删除用户、状态/角色修改、逻辑删除（`is_deleted=True`）
- `1.5.5` 文章与分类管理 API：文章 CRUD、分类 CRUD、发布状态管理
- `1.5.6` 系统日志 API：操作日志查询、异常日志查询、按时间/用户过滤；新增管理端操作/异常日志中间件

### 具体变更（关键文件）
- `backend/apps/airquality/views.py`：新增 `AdminDashboardView`、`AirQualityDataManageView`
- `backend/apps/airquality/serializers.py`：新增 `AirQualityDataManageSerializer`
- `backend/apps/airquality/urls.py`：新增 `/api/admin/dashboard/`、`/api/admin/air-quality/`
- `backend/apps/rules/serializers.py`：新增 `ProtectionRuleSerializer`
- `backend/apps/rules/views.py`：新增 `ProtectionRuleManageView`
- `backend/apps/rules/urls.py`：新增 `/api/admin/rules/`
- `backend/apps/accounts/serializers.py`：新增 `UserManageSerializer`
- `backend/apps/accounts/views.py`：新增 `UserManageView`
- `backend/apps/accounts/urls.py`：新增 `/api/admin/users/`
- `backend/apps/articles/serializers.py`：新增管理端序列化器
- `backend/apps/articles/views.py`：新增 `ArticleManageView`、`CategoryManageView`
- `backend/apps/articles/urls.py`：新增 `/api/admin/articles/`、`/api/admin/categories/`
- `backend/apps/logs/serializers.py`：新增操作日志/异常日志序列化器
- `backend/apps/logs/views.py`：新增 `OperationLogListView`、`ErrorLogListView`
- `backend/apps/logs/urls.py`：新增 `/api/admin/logs/operations/`、`/api/admin/logs/errors/`
- `backend/apps/logs/services.py`：新增操作日志写入工具
- `backend/apps/logs/middleware.py`：新增管理端写操作与异常自动记录中间件
- `backend/air_quality_system/settings.py`：挂载日志中间件
- `backend/air_quality_system/urls.py`：挂载 `apps.accounts.urls`、`apps.logs.urls`

### 验证记录（本次）
- 本地静态检查通过：`python manage.py check --settings=air_quality_system.settings_migrations`
- 回归测试通过：`python manage.py test apps.airquality.tests apps.rules.tests apps.articles.tests apps.accounts.tests apps.logs.tests --settings=air_quality_system.settings_migrations`
- 用户验收反馈：测试通过

### 边界确认
- 在用户确认测试结果前未进入 `1.6`。
- 当前仍未开始阶段二 `2.1`。

## 2026-02-15 - 阶段一 `1.6` 认证与权限（已完成，测试通过）

### 本次完成范围（`1.6.*`）
- `1.6.1` 实现登录 API（用户名+密码，返回 Token 与用户信息，拦截 `is_deleted=True`）
- `1.6.1b` 实现注册 API（用户名唯一校验、用户名/密码长度与邮箱格式校验）
- `1.6.2` 实现并应用权限类（登录态校验 + 管理员校验），管理端 API 全量切换到 Token 鉴权链路

### 具体变更（关键文件）
- `backend/air_quality_system/settings.py`
  - 启用 `rest_framework.authtoken`
  - 配置 `DEFAULT_AUTHENTICATION_CLASSES = TokenAuthentication`
- `backend/apps/accounts/models.py`
  - 新增 `PlaintextUserManager`，修复 `create_user/create_superuser` 仍哈希密码的问题，统一为明文存储（按课题要求）
- `backend/apps/accounts/permissions.py`
  - 新增 `IsAuthenticated`（登录、未软删、启用状态）
  - 新增 `IsAdminUser`（管理员角色/标记校验）
- `backend/apps/accounts/serializers.py`
  - 新增 `AuthUserSerializer`、`LoginSerializer`、`RegisterSerializer`
- `backend/apps/accounts/views.py`
  - 新增 `LoginView`、`RegisterView`
  - 管理端用户接口改用项目内权限类 `IsAdminUser`
- `backend/apps/accounts/urls.py`
  - 新增 `/api/auth/login/`
  - 新增 `/api/auth/register/`
- `backend/apps/airquality/views.py`
- `backend/apps/rules/views.py`
- `backend/apps/articles/views.py`
- `backend/apps/logs/views.py`
  - 管理端接口统一改用 `apps.accounts.permissions.IsAdminUser`
- `backend/apps/accounts/tests.py`
  - 新增认证与权限回归测试（登录、注册、软删用户拦截、管理端权限）
- `backend/apps/airquality/tests.py`
  - 未登录访问管理导入接口状态码由 `403` 更新为 `401`（Token 认证生效后的预期）

### 验证记录（本次）
- 本地静态检查通过：`python manage.py check --settings=air_quality_system.settings_migrations`
- 认证专项测试通过：`python manage.py test apps.accounts.tests --settings=air_quality_system.settings_migrations`
- 关键回归测试通过：`python manage.py test apps.airquality.tests apps.rules.tests apps.articles.tests apps.accounts.tests apps.logs.tests --settings=air_quality_system.settings_migrations`
- 用户验收反馈：测试通过

### 给后续开发者的注意事项
- 首次拉取 `1.6` 代码后需执行 `python manage.py migrate`，创建 `authtoken_token` 表。
- 管理端接口不再依赖 `force_authenticate` 思维，前后端联调需显式传 `Authorization: Token <token>`。

### 边界确认
- 阶段一 `1.6` 已收口。
- 按用户要求未开始阶段一 `1.7`。
- 当前仍未开始阶段二 `2.1`。
