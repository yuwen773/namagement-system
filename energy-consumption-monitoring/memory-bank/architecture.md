# 架构说明（Architecture）

## 文档目的
只记录稳定边界、分层职责、关键文件作用。

## 架构边界（2026-02-24）
- 开发策略：后端优先，前端后置。
- 技术基线：Django + DRF + MySQL（`utf8mb4`）。
- 数据策略：MySQL 单库，原始数据与统计数据分层存储。
- 业务域：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`。

## 分层职责
1. 接入层：数据导入与协议采集输入。
2. 业务层：Django apps（模型、规则、API）。
3. 持久层：MySQL（约束、索引、迁移）。
4. 展示层：Vue 3 + ECharts（后续阶段）。

## 核心架构见解
- 共性能力统一在框架层：统一响应、异常处理、权限控制、OpenAPI 文档。
- 业务按领域 app 解耦，便于分阶段交付和独立演进。
- 分析接口直接输出聚合结果，减少前端二次计算复杂度。

## 文件职责
- `memory-bank/pre-prd.md`：课题背景与初始约束来源。
- `memory-bank/PRD.md`：产品功能与非功能需求边界。
- `memory-bank/implementation-plan.md`：阶段步骤与验收口径。
- `memory-bank/tech-stack.md`：技术栈基线。
- `memory-bank/progress.md`：当前进度与下一步。
- `memory-bank/architecture.md`：稳定架构边界与职责说明。
- `backend/manage.py`：后端管理入口（check/migrate/命令）。
- `backend/energy_monitoring/settings.py`：全局配置中心。
- `backend/energy_monitoring/urls.py`：全局路由与文档入口聚合。
- `backend/energy_monitoring/api.py`：统一响应、分页、异常处理实现。
- `backend/energy_monitoring/permissions.py`：权限基类与权限策略。
- `backend/apps/*/`：按业务域组织的模型、序列化器、视图和路由。
- `backend/apps/*/migrations/`：数据库结构演进记录。
- `sql/init_db.sql`：数据库初始化脚本。
- `docs/api-spec.json`：OpenAPI 机器可读规范文件。
- `docs/api-reference.md`：人工阅读版接口说明。

## 维护规则
- 里程碑变化：先更新 `memory-bank/progress.md`。
- 架构边界变化：先更新 `memory-bank/architecture.md`。
