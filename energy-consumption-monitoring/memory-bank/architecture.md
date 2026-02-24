# 架构说明（Architecture）

## 文档目的
只描述稳定边界、职责分工、关键文件作用。

## 架构基线（2026-02-24）
- 开发策略：后端优先，前端后置
- 技术栈：Django + DRF + MySQL（`utf8mb4`）
- 数据策略：MySQL 单库，`em_energy_data`（原始）与 `em_energy_statistics`（统计）分层
- 领域边界：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`

## 分层职责
1. 接入层：数据导入与协议采集（Modbus/BACnet）
2. 业务层：Django apps（模型、规则、接口）
3. 持久层：MySQL（约束、索引、迁移）
4. 展示层：Vue 3 + ECharts（后续阶段）

## 文件职责（核心）
- `memory-bank/pre-prd.md`：课题原始背景与初始约束
- `memory-bank/PRD.md`：产品需求边界
- `memory-bank/implementation-plan.md`：实施步骤与验收口径
- `memory-bank/tech-stack.md`：技术选型基线
- `memory-bank/progress.md`：里程碑与下一步
- `memory-bank/architecture.md`：稳定架构边界与职责
- `backend/manage.py`：Django 管理入口（检查、迁移、命令）
- `backend/energy_monitoring/settings.py`：全局配置（应用、数据库、DRF、JWT）
- `backend/energy_monitoring/urls.py`：后端总路由入口
- `backend/energy_monitoring/api.py`：统一响应、分页、异常处理
- `backend/energy_monitoring/permissions.py`：权限基元（管理员、只读、资源所有者）
- `backend/apps/accounts/*`：认证与用户信息接口（`/api/auth/*`）
- `backend/apps/buildings/*`：校区-建筑-楼层-房间模型与树接口
- `backend/apps/devices/*`：能源类型与设备台账接口
- `backend/apps/energy/*`：能耗数据录入、批量导入、查询、导出、统计接口
- `backend/apps/analysis/*`：统计分析接口（dashboard/trend/distribution/ranking/comparison/forecast）
- `backend/apps/alarms/*`：告警规则与告警记录
- `backend/apps/system/*`：账单、充值、通知、日志与系统管理
- `backend/apps/*/migrations/`：数据库结构演进记录
- `sql/init_db.sql`：数据库初始化与种子数据

## 架构见解（当前）
- 通用能力已下沉到框架层：统一响应、异常处理、权限控制，业务视图保持薄控制器。
- API 组织按业务域分包，便于前后端按域协作和分阶段验收。
- 分析接口（`analysis`）直接面向展示层输出聚合结果，减少前端二次计算负担。

## 维护规则
- 功能步骤完成后，先更新 `memory-bank/progress.md`。
- 结构边界变化时，先更新 `memory-bank/architecture.md`，再改代码。
