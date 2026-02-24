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

## 文件职责（最小清单）
- `memory-bank/pre-prd.md`：课题背景与初始技术约束
- `memory-bank/PRD.md`：产品需求边界
- `memory-bank/implementation-plan.md`：实施步骤与验收口径
- `memory-bank/tech-stack.md`：技术栈基线
- `memory-bank/progress.md`：里程碑状态与下一步
- `memory-bank/architecture.md`：稳定架构边界与职责
- `backend/manage.py`：Django 管理入口（迁移、检查、命令）
- `backend/energy_monitoring/settings.py`：全局配置（应用、数据库、DRF、JWT、CORS）
- `backend/energy_monitoring/urls.py`：API 总路由入口
- `backend/energy_monitoring/api.py`：统一响应、分页、异常处理
- `backend/energy_monitoring/permissions.py`：权限基元（管理员/只读/资源所有者）
- `backend/apps/accounts/`：认证、用户资料与角色来源
- `backend/apps/buildings/`：校区-建筑-楼层-房间主数据
- `backend/apps/devices/`：能源类型与设备台账
- `backend/apps/energy/`：能耗原始数据、导入导出、统计查询
- `backend/apps/analysis/`：聚合分析与预测接口
- `backend/apps/alarms/`：告警规则、告警记录、处理与统计
- `backend/apps/system/`：用户管理、账单、通知、日志、充值、个人中心
- `backend/apps/*/migrations/`：数据库结构演进记录
- `sql/init_db.sql`：初始化表结构与种子数据

## 当前架构结论
- 共性能力下沉到框架层（统一响应、异常处理、权限控制），业务域按 app 分治。
- API 按业务域组织，满足分阶段交付与验收。
- 分析层输出聚合结果，降低前端二次计算复杂度。

## 维护规则
- 里程碑变化先更新 `memory-bank/progress.md`。
- 架构边界变化先更新 `memory-bank/architecture.md`。
