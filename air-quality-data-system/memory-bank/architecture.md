# 架构文档（阶段二 `2.2` 完成版）

更新时间：2026-02-15

## 1. 当前架构状态
- 当前里程碑：阶段一 `1.1` ~ `1.7` 已完成并通过测试，阶段二 `2.1`、`2.2` 已完成并通过测试。
- 当前边界：阶段二 `2.3` 未开始（待用户确认）。
- 架构形态：B/S 前后端分离。
  - 后端：Django + DRF + MySQL（端口 8000）
  - 前端：Vue 3 + Vite + Element Plus（端口 5173）

## 2. 分层与主数据流
1. 路由层：`air_quality_system/urls.py` 聚合所有 app 路由，并暴露文档路由。
2. 接口层：`apps/*/views.py` 负责参数校验、权限校验、响应封装。
3. 业务层：`apps/*/services.py` 负责可复用业务逻辑（趋势、规则匹配、日志写入等）。
4. 数据层：`apps/*/models.py` + Django ORM。
5. 横切层：
   - 统一响应：`utils/response.py`
   - 统一异常：`utils/exception_handler.py`
   - 日志中间件：`apps/logs/middleware.py`
   - API 文档：`drf-spectacular` + 导出命令

## 3. 文件职责（回归文档本质：按可维护视角列清职责）

### 3.1 根目录与产物
- `API_DOCS.md`：面向前后端联调的 Markdown 接口文档（由命令自动生成）。
- `backend/openapi-schema.json`：OpenAPI JSON 原始产物（由命令自动生成）。

### 3.2 工程入口与全局配置
- `backend/manage.py`：Django 管理入口（runserver/migrate/test/check/自定义命令）。
- `backend/requirements.txt`：后端依赖清单。
- `backend/conf/README.md`：配置目录说明。
- `backend/conf/__init__.py`：配置包标记。
- `backend/air_quality_system/__init__.py`：工程初始化。
- `backend/air_quality_system/settings.py`：全局配置（数据库、DRF、CORS、Token、Spectacular、上传限制）。
- `backend/air_quality_system/settings_migrations.py`：迁移辅助配置（SQLite）。
- `backend/air_quality_system/urls.py`：根路由（业务 API + `/api/schema/` + `/api/docs/`）。
- `backend/air_quality_system/asgi.py`：ASGI 入口。
- `backend/air_quality_system/wsgi.py`：WSGI 入口。

### 3.3 公共工具
- `backend/utils/response.py`：统一响应结构（`code/data/message` + 分页字段）。
- `backend/utils/exception_handler.py`：统一异常处理与错误输出。
- `backend/utils/data_importer.py`：CSV/XLS/XLSX 解析、校验、批量入库、导入错误收集。
- `backend/utils/__init__.py`：工具包标记。

### 3.4 accounts（认证与用户域）
- `backend/apps/accounts/models.py`：自定义用户模型 `User` 与明文密码管理器。
- `backend/apps/accounts/serializers.py`：登录/注册/用户管理序列化。
- `backend/apps/accounts/permissions.py`：`IsAuthenticated`、`IsAdminUser`。
- `backend/apps/accounts/views.py`：登录、注册、用户管理 API（含文档注解）。
- `backend/apps/accounts/urls.py`：`/api/auth/*`、`/api/admin/users/`。
- `backend/apps/accounts/admin.py`：Django Admin 注册。
- `backend/apps/accounts/tests.py`：认证与用户管理回归测试。
- `backend/apps/accounts/apps.py`：App 配置。
- `backend/apps/accounts/migrations/0001_initial.py`：初始迁移。
- `backend/apps/accounts/migrations/__init__.py`：迁移包标记。
- `backend/apps/accounts/__init__.py`：包标记。

### 3.5 airquality（空气质量核心域）
- `backend/apps/airquality/models.py`：省/市/站点/监测数据模型与约束。
- `backend/apps/airquality/serializers.py`：用户端与管理端相关序列化。
- `backend/apps/airquality/filters.py`：历史数据过滤器。
- `backend/apps/airquality/services.py`：快照、趋势、统计与数值转换逻辑。
- `backend/apps/airquality/views.py`：导入 API、用户端 API、管理端 API（含文档注解）。
- `backend/apps/airquality/urls.py`：`overview/cities/stations/historical/analysis/admin` 路由。
- `backend/apps/airquality/admin.py`：Django Admin 注册。
- `backend/apps/airquality/tests.py`：导入/用户端/管理端回归测试。
- `backend/apps/airquality/tests_api_docs.py`：`1.7` 文档路由与导出命令测试。
- `backend/apps/airquality/apps.py`：App 配置。
- `backend/apps/airquality/migrations/0001_initial.py`：初始迁移。
- `backend/apps/airquality/migrations/__init__.py`：迁移包标记。
- `backend/apps/airquality/management/__init__.py`：管理命令包标记。
- `backend/apps/airquality/management/commands/import_data_file.py`：文件导入命令。
- `backend/apps/airquality/management/commands/export_api_docs.py`：`1.7` 新增，导出 OpenAPI JSON 与 `API_DOCS.md`。
- `backend/apps/airquality/management/commands/__init__.py`：命令包标记。
- `backend/apps/airquality/__init__.py`：包标记。

### 3.6 rules（防护规则域）
- `backend/apps/rules/models.py`：`ProtectionRule` 模型与区间约束。
- `backend/apps/rules/serializers.py`：规则管理序列化。
- `backend/apps/rules/services.py`：规则匹配服务。
- `backend/apps/rules/views.py`：防护指南与规则管理 API（含文档注解）。
- `backend/apps/rules/urls.py`：`/api/protection-guide/`、`/api/admin/rules/`。
- `backend/apps/rules/admin.py`：Django Admin 注册。
- `backend/apps/rules/tests.py`：规则与防护指南测试。
- `backend/apps/rules/apps.py`：App 配置。
- `backend/apps/rules/migrations/0001_initial.py`：初始迁移。
- `backend/apps/rules/migrations/__init__.py`：迁移包标记。
- `backend/apps/rules/__init__.py`：包标记。

### 3.7 articles（文章与公告域）
- `backend/apps/articles/models.py`：文章与分类模型。
- `backend/apps/articles/serializers.py`：用户端与管理端序列化。
- `backend/apps/articles/views.py`：文章/分类/公告 API（含文档注解）。
- `backend/apps/articles/urls.py`：用户端与管理端文章路由。
- `backend/apps/articles/admin.py`：Django Admin 注册。
- `backend/apps/articles/tests.py`：文章与分类回归测试。
- `backend/apps/articles/apps.py`：App 配置。
- `backend/apps/articles/migrations/0001_initial.py`：初始迁移。
- `backend/apps/articles/migrations/__init__.py`：迁移包标记。
- `backend/apps/articles/__init__.py`：包标记。

### 3.8 logs（系统日志与导入任务域）
- `backend/apps/logs/models.py`：操作日志、异常日志、导入任务、导入任务日志。
- `backend/apps/logs/serializers.py`：日志与导入任务序列化。
- `backend/apps/logs/services.py`：日志写入辅助。
- `backend/apps/logs/middleware.py`：管理端写操作日志与异常捕获落库。
- `backend/apps/logs/views.py`：日志查询 API（含文档注解）。
- `backend/apps/logs/urls.py`：`/api/admin/logs/*`。
- `backend/apps/logs/admin.py`：Django Admin 注册。
- `backend/apps/logs/tests.py`：日志查询与中间件行为测试。
- `backend/apps/logs/apps.py`：App 配置。
- `backend/apps/logs/migrations/0001_initial.py`：初始迁移。
- `backend/apps/logs/migrations/__init__.py`：迁移包标记。
- `backend/apps/logs/__init__.py`：包标记。

### 3.9 app 聚合
- `backend/apps/__init__.py`：apps 包标记。

### 3.10 前端工程入口与配置
- `frontend/package.json`：前端依赖清单（Vue 3.5、Vue Router 4.5、Pinia 2.3、Element Plus 2.9、ECharts 5.6、Tailwind CSS 3.4）。
- `frontend/vite.config.js`：Vite 构建配置（路径别名、Element Plus 按需引入、API 代理到后端 8000 端口）。
- `frontend/tailwind.config.js`：Tailwind CSS 配置（内容扫描路径）。
- `frontend/postcss.config.js`：PostCSS 配置（Tailwind 与 Autoprefixer 插件）。
- `frontend/index.html`：HTML 入口模板。
- `frontend/.gitignore`：Git 忽略规则（node_modules、dist、本地配置）。

### 3.11 前端核心层
- `frontend/src/main.js`：应用入口，注册 Vue Router、Pinia、Element Plus、全局图标。
- `frontend/src/App.vue`：根组件，渲染 router-view。
- `frontend/src/style.css`：全局样式（Tailwind 引入、基础 CSS 变量）。

### 3.12 前端工具层
- `frontend/src/utils/request.js`：Axios 实例封装。
  - 请求拦截器：自动添加 `Authorization: Token {token}` 头。
  - 响应拦截器：处理 `{ code, data, message }` 格式，401 自动跳转登录，统一错误提示。

### 3.13 前端路由层
- `frontend/src/router/index.js`：Vue Router 配置。
  - 用户端路由：`/` 前缀，8 个子路由（overview、city、station、historical、analysis、protection、knowledge、article）。
  - 管理端路由：`/admin` 前缀，7 个子路由（dashboard、data-import、air-quality、rules、users、articles、logs）。
  - 认证路由：`/login`、`/register`。
  - 导航守卫：校验 `requiresAuth`、`requiresAdmin`，自动处理登录态跳转。

### 3.14 前端状态层（Pinia）
- `frontend/src/stores/user.js`：用户状态管理。
  - 状态：token、userInfo、isLoggedIn、isAdmin、userId、username。
  - 操作：setUser（登录后保存）、clearUser（登出清除）、updateUser（更新用户信息）。
  - 持久化：localStorage 读写 token 与 user。
- `frontend/src/stores/city.js`：城市选择状态。
  - 状态：selectedCity、selectedCityCode、selectedStation、selectedStationCode。
  - 操作：setCity、setStation、clearSelection。
- `frontend/src/stores/admin.js`：管理端 UI 状态。
  - 状态：activeMenu（当前激活菜单）、isCollapsed（侧边栏收起状态）、importTaskStatus（导入任务状态）。
  - 操作：setActiveMenu、toggleSidebar、setImportTaskStatus。

### 3.15 前端 API 层
- `frontend/src/api/auth.js`：认证接口封装。
  - `login(username, password)`：登录，返回 token 与用户信息。
  - `register(data)`：注册，创建用户。
  - `logout()`：登出，清除本地存储。
- `frontend/src/api/airquality.js`：用户端空气质量接口（15 个）。
  - 概览：getOverview、getTopCities。
  - 详情：getCityDetail、getCityTrend、getStationDetail、getStationTrend。
  - 历史：getHistoricalData、exportHistoricalData。
  - 分析：compareCities、getCorrelationAnalysis、getAQIDistribution。
  - 防护：getProtectionGuide。
  - 文章：getArticles、getArticleDetail、getCategories、getAnnouncements。
- `frontend/src/api/admin.js`：管理端接口（20 个）。
  - 仪表盘：getDashboardData。
  - 导入：uploadDataFile、getImportTasks、getImportTaskDetail、getImportTaskLogs。
  - 数据：getAirQualityDataList、updateAirQualityData、deleteAirQualityData。
  - 规则：getRulesList、createRule、updateRule、deleteRule、batchUpdateRules。
  - 用户：getUsersList、updateUser、deleteUser。
  - 文章：getAdminArticles、createArticle、updateArticle、deleteArticle、getAdminCategories、createCategory、updateCategory、deleteCategory。
  - 日志：getOperationLogs、getErrorLogs。

### 3.16 前端布局层
- `frontend/src/layouts/UserLayout.vue`：用户端布局。
  - 顶部导航栏：Logo、菜单（首页/历史/分析/防护/科普）、用户下拉菜单（登录后显示管理员入口与退出）。
  - 内容区域：router-view 渲染子路由。
  - 页脚：版权信息。
- `frontend/src/layouts/AdminLayout.vue`：管理端布局。
  - 侧边栏：可折叠，7 个菜单项，使用 Element Plus Menu 组件。
  - 顶部栏：折叠按钮、面包屑、用户端入口按钮、用户下拉菜单。
  - 内容区域：router-view 渲染子路由。

### 3.17 前端视图层
#### 认证视图（`frontend/src/views/auth/`）
- `Login.vue`：登录页。
  - 表单：用户名、密码。
  - 验证：用户名 3-20 字符，密码 6-20 字符。
  - 逻辑：调用 `login` API，成功后保存用户信息与 token，根据角色跳转（管理员→/admin，普通用户→/）。
- `Register.vue`：注册页。
  - 表单：用户名、邮箱（必填）、手机号（选填）、密码、确认密码。
  - 验证：邮箱格式、手机号格式、密码一致性。
  - 逻辑：调用 `register` API，成功后跳转登录页。

#### 用户端视图（`frontend/src/views/user/`）
- `Overview.vue`：全国概览页占位。
- `CityDetail.vue`：城市详情页占位。
- `StationDetail.vue`：站点详情页占位。
- `HistoricalData.vue`：历史数据查询页占位。
- `Analysis.vue`：数据分析页占位。
- `ProtectionGuide.vue`：防护指南页占位。
- `KnowledgeBase.vue`：科普知识库页占位。
- `ArticleDetail.vue`：文章详情页占位。

#### 管理端视图（`frontend/src/views/admin/`）
- `Dashboard.vue`：仪表盘页占位。
- `DataImport.vue`：数据导入管理页占位。
- `AirQualityManage.vue`：空气质量数据管理页占位。
- `RulesManage.vue`：防护规则管理页占位。
- `UsersManage.vue`：用户管理页占位。
- `ArticlesManage.vue`：文章管理页占位。
- `SystemLogs.vue`：系统日志页占位。

### 3.18 前端静态资源
- `frontend/src/assets/`：静态资源目录（待开发，图片、字体等）。

### 3.19 前端公共组件
- `frontend/src/components/`：公共组件目录（待开发，ECharts 封装、数据表格等）。

## 4. 已交付 API（阶段一）
### 4.1 文档与契约（`1.7`）
- `GET /api/schema/`：OpenAPI JSON
- `GET /api/docs/`：Swagger UI
- `python manage.py export_api_docs ...`：导出 `API_DOCS.md` 与 `backend/openapi-schema.json`

### 4.2 认证与权限（`1.6`）
- `POST /api/auth/login/`
- `POST /api/auth/register/`

### 4.3 用户端 API（`1.4`）
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

### 4.4 管理端 API（`1.3` + `1.5`）
- `GET /api/admin/dashboard/`
- `POST /api/admin/data-import/`
- `GET /api/admin/data-import/tasks/`
- `GET /api/admin/data-import/tasks/{task_id}/`
- `GET /api/admin/data-import/tasks/{task_id}/logs/`
- `GET|PUT|DELETE /api/admin/air-quality/`
- `GET|POST|PUT|DELETE /api/admin/rules/`
- `GET|PUT|DELETE /api/admin/users/`
- `GET|POST|PUT|DELETE /api/admin/articles/`
- `GET|POST|PUT|DELETE /api/admin/categories/`
- `GET /api/admin/logs/operations/`
- `GET /api/admin/logs/errors/`

## 5. 架构见解（`2.2` 后）

### 5.1 前端路由设计原则
1. **路由按端分层**：用户端（`/`）与管理端（`/admin`）使用不同布局组件，通过路由嵌套实现。
2. **路由守卫前置**：`beforeEach` 钩子统一处理权限校验与登录态跳转，组件内无需重复判断。
3. **懒加载路由**：所有页面组件使用动态 `import()`，减少初始加载体积。
4. **meta 扩展性**：路由 `meta` 字段预留 `title`、`requiresAuth`、`requiresAdmin` 等配置，便于统一处理。

### 5.2 状态管理设计原则
1. **按域拆分 store**：user/city/admin 三个 store 各司其职，避免单一臃肿 store。
2. **Composition API 风格**：使用 `defineStore` + `setup` 语法，类型推导更友好。
3. **计算属性派生**：`isLoggedIn`、`isAdmin` 等通过 `computed` 派生，减少冗余状态。
4. **localStorage 持久化**：用户状态自动同步到本地存储，刷新后保持登录态。

### 5.3 前后端协同架构
1. **文档生产链工程化**：接口文档由 OpenAPI 自动生成，降低前后端契约漂移风险。
2. **API 请求层统一封装**：`request.js` 集中处理 token、错误码、401 跳转。
3. **占位页面先行**：先建立完整路由与目录结构，后续并行开发业务页面时互不阻塞。
4. **代理配置解耦**：开发环境通过 Vite proxy 转发 `/api` 到后端，避免跨域配置。

## 6. 数据库 Schema（完整）

说明：以下为当前迁移状态下的完整表清单（含 Django 内置表、authtoken 表和业务表）。

### 6.1 Django/DRF 基础表

#### `django_migrations`
- `id` INTEGER PK
- `app` varchar(255) NOT NULL
- `name` varchar(255) NOT NULL
- `applied` datetime NOT NULL

#### `django_content_type`
- `id` INTEGER PK
- `app_label` varchar(100) NOT NULL
- `model` varchar(100) NOT NULL
- UNIQUE: `(app_label, model)`

#### `auth_permission`
- `id` INTEGER PK
- `content_type_id` INTEGER FK -> `django_content_type.id`
- `codename` varchar(100) NOT NULL
- `name` varchar(255) NOT NULL
- UNIQUE: `(content_type_id, codename)`

#### `auth_group`
- `id` INTEGER PK
- `name` varchar(150) UNIQUE

#### `auth_group_permissions`
- `id` INTEGER PK
- `group_id` INTEGER FK -> `auth_group.id`
- `permission_id` INTEGER FK -> `auth_permission.id`
- UNIQUE: `(group_id, permission_id)`

#### `django_admin_log`
- `id` INTEGER PK
- `object_id` TEXT NULL
- `object_repr` varchar(200) NOT NULL
- `action_flag` smallint unsigned NOT NULL
- `change_message` TEXT NOT NULL
- `content_type_id` INTEGER NULL FK -> `django_content_type.id`
- `user_id` bigint FK -> `accounts_user.id`
- `action_time` datetime NOT NULL

#### `django_session`
- `session_key` varchar(40) PK
- `session_data` TEXT NOT NULL
- `expire_date` datetime NOT NULL
- INDEX: `expire_date`

#### `authtoken_token`
- `key` varchar(40) PK
- `created` datetime NOT NULL
- `user_id` bigint UNIQUE FK -> `accounts_user.id`

### 6.2 accounts

#### `accounts_user`
- `id` INTEGER PK
- `password` varchar(128) NOT NULL
- `last_login` datetime NULL
- `is_superuser` bool NOT NULL
- `username` varchar(150) UNIQUE
- `first_name` varchar(150) NOT NULL
- `last_name` varchar(150) NOT NULL
- `email` varchar(254) NOT NULL
- `is_staff` bool NOT NULL
- `is_active` bool NOT NULL
- `date_joined` datetime NOT NULL
- `phone` varchar(20) NULL
- `role` varchar(20) NOT NULL
- `status` bool NOT NULL
- `is_deleted` bool NOT NULL

#### `accounts_user_groups`
- `id` INTEGER PK
- `user_id` bigint FK -> `accounts_user.id`
- `group_id` INTEGER FK -> `auth_group.id`
- UNIQUE: `(user_id, group_id)`

#### `accounts_user_user_permissions`
- `id` INTEGER PK
- `user_id` bigint FK -> `accounts_user.id`
- `permission_id` INTEGER FK -> `auth_permission.id`
- UNIQUE: `(user_id, permission_id)`

### 6.3 airquality

#### `airquality_province`
- `id` INTEGER PK
- `name` varchar(100) NOT NULL
- `code` varchar(12) UNIQUE
- `level` varchar(20) NOT NULL

#### `airquality_city`
- `id` INTEGER PK
- `name` varchar(100) NOT NULL
- `code` varchar(12) UNIQUE
- `longitude` decimal NOT NULL
- `latitude` decimal NOT NULL
- `province_id` bigint FK -> `airquality_province.id`

#### `airquality_monitoringstation`
- `id` INTEGER PK
- `name` varchar(200) NOT NULL
- `code` varchar(50) UNIQUE
- `address` varchar(255) NOT NULL
- `station_type` varchar(50) NOT NULL
- `city_id` bigint FK -> `airquality_city.id`

#### `airquality_airqualitydata`
- `id` INTEGER PK
- `monitor_time` datetime NOT NULL（INDEX）
- `aqi` integer unsigned NOT NULL
- `pm25` decimal NULL
- `pm10` decimal NULL
- `so2` decimal NULL
- `no2` decimal NULL
- `co` decimal NULL
- `o3` decimal NULL
- `quality_level` varchar(20) NOT NULL
- `station_id` bigint FK -> `airquality_monitoringstation.id`
- UNIQUE: `(station_id, monitor_time)`（`uq_airq_station_monitor_time`）

### 6.4 rules

#### `rules_protectionrule`
- `id` INTEGER PK
- `rule_name` varchar(100) NOT NULL
- `min_aqi` integer unsigned NOT NULL
- `max_aqi` integer unsigned NOT NULL
- `population_type` varchar(20) NOT NULL
- `advice` TEXT NOT NULL
- `is_enabled` bool NOT NULL
- CHECK: `min_aqi <= max_aqi`（`ck_rule_min_le_max`）
- 业务约束：同 `population_type` 下 AQI 区间不可重叠（模型 `clean` 校验）

### 6.5 articles

#### `articles_articlecategory`
- `id` INTEGER PK
- `name` varchar(100) UNIQUE
- `sort` INTEGER NOT NULL

#### `articles_article`
- `id` INTEGER PK
- `title` varchar(255) NOT NULL
- `content` TEXT NOT NULL
- `status` varchar(20) NOT NULL
- `is_announcement` bool NOT NULL
- `sort_order` INTEGER NOT NULL
- `created_at` datetime NOT NULL
- `updated_at` datetime NOT NULL
- `category_id` bigint FK -> `articles_articlecategory.id`
- INDEX: `(status, is_announcement)`

### 6.6 logs

#### `logs_operationlog`
- `id` INTEGER PK
- `operation_type` varchar(50) NOT NULL
- `operation_content` TEXT NOT NULL
- `ip_address` varchar(45) NOT NULL
- `operation_time` datetime NOT NULL
- `user_id` bigint FK -> `accounts_user.id`

#### `logs_errorlog`
- `id` INTEGER PK
- `error_type` varchar(100) NOT NULL
- `error_message` TEXT NOT NULL
- `stack_trace` TEXT NOT NULL
- `occurred_at` datetime NOT NULL

#### `logs_importtask`
- `id` INTEGER PK
- `task_id` varchar(64) UNIQUE
- `file_name` varchar(255) NOT NULL
- `file_type` varchar(20) NOT NULL
- `status` varchar(20) NOT NULL
- `total_count` INTEGER NOT NULL
- `success_count` INTEGER NOT NULL
- `failed_count` INTEGER NOT NULL
- `start_time` datetime NOT NULL
- `end_time` datetime NULL
- `initiator_id` bigint FK -> `accounts_user.id`

#### `logs_importtasklog`
- `id` INTEGER PK
- `row_number` INTEGER NOT NULL
- `error_reason` TEXT NOT NULL
- `raw_data_snippet` TEXT NULL
- `created_at` datetime NOT NULL
- `task_id` bigint FK -> `logs_importtask.id`

## 7. 下一步边界
- 当前已完成阶段一 `1.7` 与阶段二 `2.1`、`2.2`。
- 在新的用户确认前，不进入阶段二 `2.3`（公共组件开发）。
