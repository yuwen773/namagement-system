# 架构说明（Architecture）

## 文档目的
定义长期稳定的架构边界、分层职责与文件职责。
不记录一次性操作、命令输出和临时排障过程。

## 当前架构基线（2026-02-16）
- 开发策略：后端优先，前端后置
- 技术基线：Django + DRF + MySQL（`utf8mb4`）；Spark 为可选增强
- 数据策略：单库 MySQL；原始数据与统计数据分层（`em_energy_data` / `em_energy_statistics`）
- 领域划分：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`
- 当前进度基线：阶段 `2.5` 已完成并通过测试，`2.6` 未开始

## 分层职责
1. 数据接入层：CSV/Excel 导入与 Modbus/BACnet 协议采集入口
2. 业务服务层：Django Apps（模型、服务、API）
3. 数据持久层：MySQL 表结构、约束、索引与迁移
4. 展示层：Vue 3 + ECharts（后续阶段实现）

## 关键文件职责

### `memory-bank/`（项目记忆）
- `memory-bank/pre-prd.md`：课题原始背景与约束来源
- `memory-bank/PRD.md`：产品需求与功能边界
- `memory-bank/implementation-plan.md`：阶段划分、执行步骤与验收标准
- `memory-bank/tech-stack.md`：技术选型与版本约束
- `memory-bank/progress.md`：事实进度、验收状态与下一步
- `memory-bank/architecture.md`：稳定架构边界与文件职责

### `backend/`（后端锚点）
- `backend/manage.py`：Django 管理入口（运行、迁移、检查、管理命令）
- `backend/requirements.txt`：后端依赖基线
- `backend/energy_monitoring/settings.py`：全局配置中心（应用注册、数据库、中间件等）
- `backend/energy_monitoring/urls.py`：全局路由聚合入口
- `backend/energy_monitoring/asgi.py`：ASGI 入口
- `backend/energy_monitoring/wsgi.py`：WSGI 入口
- `backend/energy_monitoring/__init__.py`：项目包初始化入口

### `backend/apps/accounts/`（账户域）
- `backend/apps/accounts/models.py`：账户域模型定义（`UserProfile`、角色字段）
- `backend/apps/accounts/admin.py`：账户域后台管理注册
- `backend/apps/accounts/migrations/0001_initial.py`：账户域迁移基线
- `backend/apps/accounts/serializers.py`：账户域序列化层位点
- `backend/apps/accounts/views.py`：账户域 API 位点
- `backend/apps/accounts/urls.py`：账户域路由位点
- `backend/apps/accounts/tests.py`：账户域测试位点

### `backend/apps/buildings/`（空间域）
- `backend/apps/buildings/models.py`：空间层级模型（Campus/Building/Floor/Room）
- `backend/apps/buildings/admin.py`：空间域后台管理注册
- `backend/apps/buildings/migrations/0001_initial.py`：空间域迁移基线
- `backend/apps/buildings/serializers.py`：空间域序列化层位点
- `backend/apps/buildings/views.py`：空间域 API 位点
- `backend/apps/buildings/urls.py`：空间域路由位点
- `backend/apps/buildings/tests.py`：空间域测试位点

### `backend/apps/devices/`（设备域）
- `backend/apps/devices/models.py`：设备域模型（`EnergyType`、`Device`）与状态枚举
- `backend/apps/devices/admin.py`：设备域后台管理注册
- `backend/apps/devices/migrations/0001_initial.py`：设备域迁移基线
- `backend/apps/devices/serializers.py`：设备域序列化层位点
- `backend/apps/devices/views.py`：设备域 API 位点
- `backend/apps/devices/urls.py`：设备域路由位点
- `backend/apps/devices/tests.py`：设备域测试位点

### `backend/apps/`（其余领域模块）
- `backend/apps/energy/`：能耗原始数据与统计
- `backend/apps/analysis/`：统计分析、对比、预测
- `backend/apps/alarms/`：告警规则与处置
- `backend/apps/system/`：账单、充值、通知、操作日志

## 架构见解（阶段 2.5 后）
- 领域主干清晰：`buildings` 提供空间层级，`devices` 承载设备主数据，后续 `energy` 直接复用两者关联。
- 设备模型采用“房间可空”设计，支持室外设备与网关侧设备，避免强制绑定导致的数据落地阻塞。
- `device_id` 作为外部采集标识保持唯一，可稳定映射数据集与协议采集侧标识。
- 迁移策略统一：在已有业务表环境中继续通过 `--fake-initial` 对齐历史，后续只追加增量迁移。

## 演进规则
- 每完成一个实施步骤，同步更新 `memory-bank/progress.md`
- 架构边界变化时，先更新 `memory-bank/architecture.md`，再改代码