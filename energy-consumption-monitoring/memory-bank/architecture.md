# 架构说明（Architecture）

## 文档目的
定义长期稳定的架构边界、分层职责、文件职责。
不记录一次性操作、命令输出和临时排障过程。

## 当前架构基线（2026-02-16）
- 开发策略：后端优先，前端后置
- 技术基线：Django + DRF + MySQL（`utf8mb4`）；Spark 为可选增强
- 数据策略：单库 MySQL；原始数据与统计数据分层（`em_energy_data` / `em_energy_statistics`）
- 领域划分：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`
- 当前进度基线：阶段 `2.2` 已完成应用骨架与注册，`2.3` 未开始

## 分层职责
1. 数据接入层：CSV/Excel 导入与 Modbus/BACnet 协议采集入口
2. 业务服务层：Django Apps（模型、服务、API）
3. 数据持久层：MySQL 表结构、约束、索引与迁移
4. 展示层：Vue 3 + ECharts（后续阶段实现）

## 关键文件职责

### `memory-bank/`（项目记忆）
- `memory-bank/pre-prd.md`：课题原始背景与约束来源
- `memory-bank/PRD.md`：产品功能与非功能需求边界
- `memory-bank/implementation-plan.md`：分阶段实施步骤与验收标准
- `memory-bank/tech-stack.md`：技术选型与版本约束
- `memory-bank/progress.md`：事实性进度与验收结果
- `memory-bank/architecture.md`：长期架构边界与职责定义

### `backend/`（后端锚点）
- `backend/manage.py`：Django 管理入口（`runserver`、`migrate`、`check`、管理命令）
- `backend/requirements.txt`：后端依赖基线
- `backend/energy_monitoring/settings.py`：全局配置中心（应用注册、数据库、中间件等）
- `backend/energy_monitoring/urls.py`：全局路由聚合入口
- `backend/energy_monitoring/asgi.py`：ASGI 入口
- `backend/energy_monitoring/wsgi.py`：WSGI 入口
- `backend/energy_monitoring/__init__.py`：项目包初始化入口

### `backend/apps/`（领域模块）
- `backend/apps/accounts/`：认证、用户、角色权限
- `backend/apps/buildings/`：校区、建筑、楼层、房间
- `backend/apps/devices/`：设备与能源类型
- `backend/apps/energy/`：能耗原始数据与统计
- `backend/apps/analysis/`：统计分析、对比、预测
- `backend/apps/alarms/`：告警规则与处置
- `backend/apps/system/`：账单、充值、通知、操作日志

## 架构见解（阶段 2.2 后）
- 先完成 7 个应用骨架并注册，确保“领域边界先行”，避免后续把模型与 API 混杂在单一应用。
- 在 2.2 阶段即统一 `urls.py` 与 `serializers.py` 文件位点，后续接口开发可按固定路径推进，降低重构成本。
- 应用统一在 `settings.py` 注册后，迁移、路由、权限的演进入口集中，便于按阶段做验收与回归。

## 演进规则
- 每完成一个实施步骤，同步更新 `memory-bank/progress.md`
- 架构边界发生变化时，先更新 `memory-bank/architecture.md`，再改代码
