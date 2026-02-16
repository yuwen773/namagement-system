# 架构说明（Architecture）

## 文档目的
定义当前阶段可执行的系统架构基线，明确目录与文件职责，避免后续开发偏离设计。

## 当前架构基线（截至阶段 1.1）
- 架构策略：后端优先（先 Django + DRF，再前端）。
- 数据存储：`MySQL` 单体架构（不引入 InfluxDB）。
- 数据分析：`Spark` 为可选增强能力，不作为当前硬门槛。
- 前端初始化：`frontend/` 在第七阶段通过 Vite 生成，不在阶段 1.1 手动创建。

## 分层设计（目标）
1. 数据接入层：CSV/Excel 数据导入脚本与管理命令。
2. 业务服务层：Django Apps（账户、建筑、设备、能耗、分析、告警、系统）。
3. 数据持久层：MySQL 表结构与索引（`sql/init_db.sql`）。
4. 展示层：Vue 3 + ECharts（后续阶段实现）。

## 目录与文件职责

### 文档层（memory-bank）
- `memory-bank/pre-prd.md`：课题原始需求与研究背景。
- `memory-bank/PRD.md`：产品需求定义（功能、角色、非功能需求）。
- `memory-bank/implementation-plan.md`：分阶段实施计划与验收标准。
- `memory-bank/tech-stack.md`：技术栈约束清单。
- `memory-bank/progress.md`：实施进度与落地记录（持续更新）。
- `memory-bank/architecture.md`：架构基线与职责划分（本文件，持续更新）。

### 后端骨架（backend）
- `backend/manage.py`：Django 管理入口（迁移、启动、管理命令）。
- `backend/requirements.txt`：后端 Python 依赖清单。
- `backend/energy_monitoring/__init__.py`：Django 项目包标记。
- `backend/energy_monitoring/settings.py`：全局配置（数据库、中间件、应用注册等）。
- `backend/energy_monitoring/urls.py`：全局路由入口。
- `backend/energy_monitoring/wsgi.py`：WSGI 部署入口。
- `backend/energy_monitoring/asgi.py`：ASGI 入口（异步/长连接扩展预留）。
- `backend/apps/__init__.py`：业务应用命名空间。
- `backend/apps/accounts/__init__.py`：用户认证与角色域（ADMIN/USER）预留。
- `backend/apps/buildings/__init__.py`：校区/建筑/楼层/房间域预留。
- `backend/apps/devices/__init__.py`：设备与能源类型域预留。
- `backend/apps/energy/__init__.py`：原始能耗与统计数据域预留。
- `backend/apps/analysis/__init__.py`：统计分析与预测域预留。
- `backend/apps/alarms/__init__.py`：告警规则与告警记录域预留。
- `backend/apps/system/__init__.py`：账单、充值、通知、日志域预留。

### 数据与脚本层
- `sql/init_db.sql`：数据库初始化脚本入口（表结构、索引、初始数据）。
- `scripts/`：数据导入与处理脚本目录（后续补充）。
- `docs/`：接口与交付文档目录（后续补充，如 `docs/rtm.md`、API 文档）。

## 当前状态说明
- 当前仅完成“工程骨架”落地，不包含可运行业务逻辑。
- 各业务域已完成目录级边界划分，可直接进入后续模型与 API 开发。
- 所有后续实现需保持 app 边界清晰，避免跨域耦合。

## 架构演进规则
- 每完成一个实施计划步骤，必须同步更新 `progress.md`。
- 若出现架构决策变化（如新增中间件、调整分层、引入新基础设施），必须先更新本文件再实施代码。
