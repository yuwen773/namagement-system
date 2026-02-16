# 架构说明（Architecture）

## 文档目的
定义长期有效的架构边界、分层职责与文件分工；不记录一次性执行过程。

## 当前架构基线（截至阶段 1.3）
- 开发顺序：后端优先（Django + DRF 先落地，前端后置）
- 数据库策略：`MySQL` 单体架构（不引入 InfluxDB）
- 分析策略：`Spark` 为可选增强，不作为当前阶段硬门槛
- 运行环境：`backend/.venv`（Python 3.11，Django 5.2.x）
- 数据库基线：已落地 `energy_monitoring` 库，默认字符集 `utf8mb4`
- 前端策略：`frontend/` 由第七阶段 Vite 自动初始化，不在当前阶段手动创建

## 分层与职责
1. 数据接入层：负责 CSV/Excel 等数据导入与清洗入口。
2. 业务服务层：Django Apps 承载领域模型、业务逻辑与 API。
3. 数据持久层：MySQL 表结构、索引、初始化脚本。
4. 展示层：Vue 3 + ECharts（后续阶段实现）。

## 文档分工（回归文档本质）
- `memory-bank/pre-prd.md`：课题背景与原始需求来源。
- `memory-bank/PRD.md`：产品需求定义（做什么、给谁做、做到什么程度）。
- `memory-bank/implementation-plan.md`：实施顺序与验收标准（怎么分步做）。
- `memory-bank/tech-stack.md`：技术选型约束（用什么做）。
- `memory-bank/progress.md`：执行事实与验收结论（做到哪一步）。
- `memory-bank/architecture.md`：架构边界与职责约束（系统如何组织）。

## 工程文件职责

### 根目录
- `AGENTS.md`：仓库协作约束与执行规范（代理行为边界）。
- `CLAUDE.md`：实现约定与目标架构补充说明。
- `dataSource/`：原始数据集输入目录（导入与分析的上游数据）。
- `docs/`：交付文档目录（RTM、部署文档、接口说明等）。
- `scripts/`：数据导入、清洗、统计生成等脚本目录。
- `sql/init_db.sql`：数据库初始化与基线数据脚本入口。

### 后端入口与配置
- `backend/manage.py`：Django 管理入口，执行迁移、运行服务、管理命令。
- `backend/requirements.txt`：Python 依赖清单文件（用于环境复现）。
- `backend/energy_monitoring/settings.py`：全局配置中心（应用注册、中间件、数据库、时区等）。
- `backend/energy_monitoring/urls.py`：全局路由入口，聚合各 app API。
- `backend/energy_monitoring/wsgi.py`：WSGI 部署入口。
- `backend/energy_monitoring/asgi.py`：ASGI 部署入口（异步能力扩展预留）。
- `backend/energy_monitoring/__init__.py`：项目包标记文件。

### 领域应用边界（`backend/apps/`）
- `backend/apps/accounts/`：认证、用户、角色权限域。
- `backend/apps/buildings/`：校区/建筑/楼层/房间域。
- `backend/apps/devices/`：设备与能源类型域。
- `backend/apps/energy/`：能耗原始数据与统计域。
- `backend/apps/analysis/`：分析、对比、预测域。
- `backend/apps/alarms/`：告警规则与告警处理域。
- `backend/apps/system/`：账单、充值、通知、操作日志域。
- 各目录中的 `__init__.py`：包边界标记，确保可导入与模块化组织。

## 当前阶段架构见解
- 在阶段 1.3 明确 `MySQL + utf8mb4` 基线后，后续模型、索引与导入脚本可按统一字符语义设计，降低编码与排序不一致风险。
- `apps/` 按业务域划分是可维护性前提，跨域调用应经服务层或明确 API 边界，避免耦合扩散。
- 文档职责保持分离：`progress.md` 记录“事实与验收”，`architecture.md` 维护“长期约束与组织方式”。

## 架构演进规则
- 每完成一个实施计划步骤，必须同步更新 `memory-bank/progress.md`。
- 若架构决策变化（分层、基础设施、中间件、服务边界），先更新本文件，再改代码。
