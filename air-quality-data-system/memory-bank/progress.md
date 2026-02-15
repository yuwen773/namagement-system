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
- `backend/air_quality_system/settings.py`
  - 新增 `AUTH_USER_MODEL = "accounts.User"`
- `backend/apps/accounts/models.py`
  - 新增 `User(AbstractUser)`：`phone/role/status/is_deleted`
  - 按实施计划要求覆写 `set_password/check_password` 实现“明文存储与明文校验”（仅为满足课题要求，禁止用于生产）
- `backend/apps/airquality/models.py`
  - `Province`/`City`/`MonitoringStation`/`AirQualityData`
  - `AirQualityData.monitor_time` 索引
  - `(station, monitor_time)` 唯一约束
  - 基于 `HJ 633-2012` 边界的 AQI 分级写入 `quality_level`
- `backend/apps/rules/models.py`
  - `ProtectionRule`：`min_aqi <= max_aqi`（DB 约束）
  - 同一 `population_type` 内区间 `[min_aqi, max_aqi]` 不允许重叠（应用层校验）
- `backend/apps/articles/models.py`
  - `ArticleCategory`/`Article`
- `backend/apps/logs/models.py`
  - `OperationLog`/`ErrorLog`/`ImportTask`/`ImportTaskLog`
- `backend/apps/*/admin.py`
  - 为所有新模型补齐最小 Admin 注册，便于按计划在 Django Admin 手工验证
- `backend/apps/*/migrations/0001_initial.py`
  - 生成各 app 的初始迁移文件
- `backend/air_quality_system/settings_migrations.py`
  - 新增“迁移生成辅助 settings”：用于在已有 MySQL 迁移历史不一致时，仍可对着 SQLite 生成迁移文件

### 验证记录（本次）
- 用户反馈：测试通过

### 已知注意事项（非常重要）
- 如果本地 MySQL 数据库是在 `1.1` 阶段先跑了迁移（默认用户表为 `auth_user`），在 `1.2` 切换 `AUTH_USER_MODEL` 后可能出现 `InconsistentMigrationHistory`。
- 建议做法：对 `1.2` 使用全新数据库（删库重建或更换库名）后再执行 `python backend/manage.py migrate`，保证 schema 与迁移历史一致。

