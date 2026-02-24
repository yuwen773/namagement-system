# 架构说明（Architecture）

## 文档目的
只记录稳定边界、分层职责、关键文件职责。

## 架构边界（2026-02-24）
- 开发策略：后端优先，前端后置。
- 技术基线：Django + DRF + MySQL（`utf8mb4`）。
- 存储策略：MySQL 单库，`em_energy_data`（原始）与 `em_energy_statistics`（统计）分层。
- 业务域：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`。
- 统一规范：API 返回 `code/data/message/total`；需求追踪在 `docs/rtm.md`。

## 分层职责
1. 接入层：文件导入与 Modbus/BACnet 协议采集。
2. 业务层：Django apps 承载模型、规则、API。
3. 持久层：MySQL 承载约束、索引、迁移。
4. 展示层：Vue 3 + ECharts（后续阶段实现）。

## 架构见解
- 导入与采集统一落表 `em_energy_data`，保证监测中心与分析查询口径一致。
- 导入链路按“读取 -> 清洗 -> 分批写入”拆分，便于扩展与大数据量稳定处理。
- 协议采集按“单协议采集器 + 统一调度器”组织，降低重试与恢复逻辑重复。

## 关键文件职责
- `memory-bank/implementation-plan.md`：阶段任务与验收口径。
- `memory-bank/progress.md`：当前状态与下一步。
- `memory-bank/architecture.md`：稳定边界与职责。
- `backend/energy_monitoring/settings.py`：全局配置中心（数据库、DRF、JWT、CORS）。
- `backend/energy_monitoring/api.py`：统一响应、分页、异常处理。
- `backend/apps/energy/models.py`：`em_energy_data`、`em_energy_statistics` 数据模型。
- `backend/apps/energy/management/commands/import_energy_data.py`：导入命令入口。
- `backend/apps/energy/management/commands/generate_statistics.py`：统计命令入口（阶段六实现逻辑）。
- `backend/apps/energy/management/commands/check_alarms.py`：告警命令入口（阶段六实现逻辑）。
- `scripts/config.py`：导入与脚本配置加载、Django 启动。
- `scripts/data_cleaner.py`：数据校验、异常标记、标准化与清洗报告。
- `scripts/data_importer.py`：CSV/Excel/JSON 读取、分批导入、进度、断点续传。
- `scripts/protocol_collectors/modbus_collector.py`：Modbus 周期采集。
- `scripts/protocol_collectors/bacnet_collector.py`：BACnet 周期采集。
- `scripts/protocol_collectors/collector_runner.py`：统一调度、重试恢复、批量写入。
- `sql/init_db.sql`：数据库初始化脚本。
- `docs/rtm.md`：需求-实现-测试-证据追踪矩阵。

## 维护规则
- 里程碑变化先更新 `memory-bank/progress.md`。
- 架构边界变化先更新 `memory-bank/architecture.md`。
