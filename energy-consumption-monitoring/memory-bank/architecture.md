# 架构说明（Architecture）

## 文档目的
只记录稳定边界、分层职责、核心文件职责。

## 架构边界（2026-02-24）
- 开发策略：后端优先，前端后置。
- 技术基线：Django + DRF + MySQL（`utf8mb4`）。
- 数据策略：MySQL 单库，原始数据与统计数据分层存储。
- 业务域：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`。
- 统一规范：API 统一响应 `code/data/message/total`；需求追踪统一维护于 `docs/rtm.md`。

## 分层职责
1. 接入层：数据导入与协议采集输入。
2. 业务层：Django apps（模型、规则、API）。
3. 持久层：MySQL（约束、索引、迁移）。
4. 展示层：Vue 3 + ECharts（阶段七后实现）。

## 架构见解
- 共性能力收敛到框架层（响应包装、异常处理、权限、OpenAPI），降低业务重复实现。
- 业务按领域解耦，支持分阶段交付与独立演进。
- 分析接口直接输出聚合结果，前端只做展示与交互。

## 核心文件职责
- `memory-bank/pre-prd.md`：课题来源与初始技术诉求。
- `memory-bank/PRD.md`：产品需求边界（功能/非功能）。
- `memory-bank/implementation-plan.md`：阶段任务与验收口径。
- `memory-bank/progress.md`：当前阶段结论与下一步。
- `memory-bank/architecture.md`：稳定架构边界与职责分工。
- `memory-bank/tech-stack.md`：技术栈基线。
- `backend/energy_monitoring/settings.py`：全局配置中心（数据库、DRF、JWT、CORS）。
- `backend/energy_monitoring/urls.py`：全局路由聚合与文档入口。
- `backend/energy_monitoring/api.py`：统一响应、分页、异常处理。
- `backend/energy_monitoring/permissions.py`：RBAC 权限策略。
- `backend/apps/*/models.py`：领域数据模型定义。
- `backend/apps/*/views.py`：领域 API 入口与业务编排。
- `backend/apps/*/serializers.py`：请求校验与响应序列化。
- `backend/apps/*/urls.py`：领域路由注册。
- `sql/init_db.sql`：数据库初始化脚本。
- `docs/api-spec.json`：OpenAPI 规范导出文件。
- `docs/api-reference.md`：接口阅读文档。
- `docs/rtm.md`：需求-实现-测试-证据追踪矩阵。

## 维护规则
- 里程碑变化：先更新 `memory-bank/progress.md`。
- 架构边界变化：先更新 `memory-bank/architecture.md`。
