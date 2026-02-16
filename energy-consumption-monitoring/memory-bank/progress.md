# 项目进度记录（Progress）

## 文档目的
仅记录已完成事实、验收结果与下一步，不在此文档展开实现细节。

## 当前里程碑（截至 2026-02-16）
- 当前阶段：第一阶段（项目初始化与基础设施）
- 已完成步骤：`1.1`、`1.2`、`1.3`、`1.4`、`1.5`
- 当前状态：`1.5` 已由用户测试通过；按计划可进入第二阶段 `2.1`

## 已完成内容

### 步骤 1.1：创建项目目录结构（已完成）
- 已创建 `backend/`、`sql/`、`scripts/`、`docs/` 及后端应用骨架目录。
- 已创建各 Python 包 `__init__.py` 占位文件。

### 步骤 1.2：配置后端虚拟环境（已完成）
- 在 `backend/` 下创建虚拟环境：`backend/.venv`
- 在该虚拟环境中安装基础后端依赖：
  - `Django 5.2.x`
  - `djangorestframework`
  - `django-cors-headers`
  - `djangorestframework-simplejwt`
  - `PyMySQL`

### 步骤 1.3：配置 MySQL 数据库（已完成）
- 已确认本机 MySQL 服务运行正常。
- 已确认 MySQL 版本满足 `8.0+` 要求。
- 已创建数据库 `energy_monitoring`（不存在时自动创建）。
- 已通过 `SHOW CREATE DATABASE energy_monitoring;` 验证默认字符集为 `utf8mb4`（排序规则 `utf8mb4_0900_ai_ci`）。

### 步骤 1.4：配置 Django 项目（已完成）
- 已完成 Django 项目基础文件落地：
  - `backend/manage.py`
  - `backend/energy_monitoring/settings.py`
  - `backend/energy_monitoring/urls.py`
  - `backend/energy_monitoring/wsgi.py`
  - `backend/energy_monitoring/asgi.py`
  - `backend/energy_monitoring/__init__.py`
- 已完成 `settings.py` 关键配置：
  - `DATABASES` 连接 MySQL（默认 `energy_monitoring` / `127.0.0.1:3307`，支持环境变量覆盖）
  - `ALLOWED_HOSTS`（本地默认 `127.0.0.1,localhost`）
  - `INSTALLED_APPS` 包含 `rest_framework`、`corsheaders`
  - 时区 `TIME_ZONE = "Asia/Shanghai"`
- 已完成 `backend/requirements.txt` 依赖清单整理（Django、DRF、CORS、SimpleJWT、PyMySQL）。

### 步骤 1.5：工业协议采集环境准备（Modbus/BACnet）（已完成）
- 已新增阶段 1.5 协议采集脚手架目录：`scripts/protocol_collection/`。
- 已落地点位映射配置模板：`collection_config.example.json`，明确 `仪表ID -> 设备ID -> 房间`，并保留 `gateway_mode`（`gateway_forward`/`direct_meter`）字段。
- 已提供 Modbus/BACnet 协议模拟器：`simulators.py`，用于无实物设备场景验收。
- 已实现采集策略与适配器：`adapters.py`、`collector.py`，覆盖采集频率、请求超时、重试退避、断线重连。
- 已实现字段对齐校验：采集输出键严格对齐 `em_energy_data` 目标字段
  `device/energy_type/timestamp/value/voltage/current/power/flow_rate`。
- 已提供一键验收脚本：`validate_phase_1_5.py`，输出 5 项验收结果（PASS/FAIL）。

## 验收对照

### 1.1 验收
- 所有目标目录已创建：是
- Python 包目录 `__init__.py` 已补齐：是
- `tree` 结构检查已执行：是

### 1.2 验收
- 虚拟环境激活成功：是
- `django-admin --version`：`5.2.11`
- `python --version`：`Python 3.11.7`
- Python 解释器路径：`backend/.venv/Scripts/python.exe`
- 验收结论：通过（用户已确认测试通过）

### 1.3 验收
- MySQL 服务正在运行：是
- 数据库 `energy_monitoring` 已创建：是
- `SHOW CREATE DATABASE` 确认字符集为 `utf8mb4`：是
- 验收结论：通过（用户已确认测试通过）

### 1.4 验收
- `python manage.py check`：通过（System check identified no issues）
- `python manage.py migrate`：通过（`admin/auth/contenttypes/sessions` 初始迁移成功）
- 首页验证：通过（`GET /` 返回 200，Django 安装成功页面可访问）
- 验收结论：通过（用户已确认测试通过）

### 1.5 验收
- Modbus 模拟设备可被读取，返回稳定测点值：通过
- BACnet 模拟设备可被读取，返回稳定测点值：通过
- 断网后自动重连并恢复采集：通过
- 采集数据字段与 `em_energy_data` 字段一致：通过
- 无实物设备场景下可通过协议模拟器完成验收：通过
- 验证命令：`python -m scripts.protocol_collection.validate_phase_1_5`
- 验收结论：通过（用户已确认测试通过）

## 关键决策与约束
- 严格按实施计划顺序执行，`1.4` 验收通过后再进入 `1.5`，并在 `1.5` 验收完成后进入下一阶段。
- `frontend/` 继续按计划在第七阶段通过 Vite 自动初始化。
- 生产环境敏感配置（如 `SECRET_KEY`、数据库凭据）采用环境变量覆盖本地默认值。
- 阶段 1.5 验收以模拟器为默认基线，不依赖实物仪表。

## 下一步（待执行）
- 第二阶段 `2.1`：设计数据库表结构（`sql/init_db.sql`）。
