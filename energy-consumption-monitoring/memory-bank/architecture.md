# 架构说明（Architecture）

## 文档目的
仅记录稳定边界、分层职责、关键文件职责。

## 架构边界（2026-02-24）
- 开发策略：后端优先，前端后置。
- 技术基线：Django + DRF + MySQL（`utf8mb4`）。
- 存储策略：MySQL 单库；`em_energy_data`（原始）、`em_energy_statistics`（统计）、`em_energy_forecasts`（预测）分层。
- 业务域：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`。
- 统一规范：API 返回 `code/data/message/total`；需求追踪在 `docs/rtm.md`。

## 分层职责
1. 接入层：文件导入与 Modbus/BACnet 协议采集，统一写入原始能耗表。
2. 业务层：Django apps 承载模型、规则、任务命令与 API。
3. 持久层：MySQL 承载实体数据、统计数据、预测数据及索引约束。
4. 展示层：Vue 3 + ECharts（阶段七后实现）。

## 关键文件职责
- `memory-bank/implementation-plan.md`：阶段任务与验收口径。
- `memory-bank/progress.md`：当前状态与下一步。
- `memory-bank/architecture.md`：稳定边界与职责。
- `backend/energy_monitoring/settings.py`：全局配置（数据库、DRF、JWT、CORS）。
- `backend/apps/energy/models.py`：原始与统计能耗模型。
- `backend/apps/analysis/models.py`：预测模型（`em_energy_forecasts`）。
- `backend/apps/analysis/views.py`：分析与预测 API（`/api/analysis/forecast/` 读预测表）。
- `backend/apps/energy/management/commands/import_energy_data.py`：导入命令。
- `backend/apps/energy/management/commands/generate_statistics.py`：统计任务命令。
- `backend/apps/energy/management/commands/check_alarms.py`：告警任务命令。
- `backend/apps/energy/management/commands/generate_forecast.py`：预测任务命令。
- `backend/apps/energy/management/commands/run_scheduled_tasks.py`：定时任务入口（hourly/daily/weekly）。
- `scripts/data_importer.py`：多格式数据导入与分批写入。
- `scripts/generate_statistics.py`：统计聚合实现。
- `scripts/check_alarms.py`：告警检测实现。
- `scripts/generate_forecast.py`：7/30 天预测生成实现。
- `scripts/scheduled_tasks.py`：定时任务组合逻辑。
- `scripts/spark_offline_analysis.py`：Spark 可选离线分析与 Python 回退。
- `docs/scheduler.md`：cron 调度说明。
- `docs/rtm.md`：需求追踪矩阵。

## 维护规则
- 里程碑变化更新 `memory-bank/progress.md`。
- 架构边界变化更新 `memory-bank/architecture.md`。
