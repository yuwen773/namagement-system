# 架构说明（Architecture）

## 文档目的
沉淀稳定的架构边界与文件职责；不记录过程性内容。

## 当前架构基线（2026-02-24）
- 开发策略：后端优先，前端后置
- 技术基线：Django + DRF + MySQL（`utf8mb4`），Spark 为可选增强
- 数据策略：MySQL 单库；原始数据与统计数据分层
- 领域边界：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`
- 进度基线：阶段三 `3.1`、`3.2`、`3.3` 已完成

## 分层职责
1. 数据接入层：数据集导入、协议采集接入（Modbus/BACnet）
2. 业务服务层：Django apps（模型、业务规则、API）
3. 持久化层：MySQL 表结构、约束、索引、迁移
4. 展示层：Vue 3 + ECharts（后续阶段实现）

## 关键文件职责
- `memory-bank/pre-prd.md`：原始课题背景与约束来源
- `memory-bank/PRD.md`：产品需求边界
- `memory-bank/implementation-plan.md`：实施步骤与验收标准
- `memory-bank/tech-stack.md`：技术选型与版本基线
- `memory-bank/progress.md`：里程碑结果与下一步
- `memory-bank/architecture.md`：稳定架构边界与职责
- `backend/manage.py`：Django 管理入口（检查/迁移/命令）
- `backend/energy_monitoring/settings.py`：全局配置（应用、数据库、DRF、JWT）
- `backend/energy_monitoring/urls.py`：全局 API 路由入口
- `backend/energy_monitoring/api.py`：统一响应格式、分页、异常处理
- `backend/energy_monitoring/permissions.py`：通用权限类（管理员/只读/资源所有者）
- `backend/apps/accounts/serializers.py`：注册/登录/用户信息/改密序列化
- `backend/apps/accounts/views.py`：认证接口实现
- `backend/apps/accounts/urls.py`：`/api/auth/*` 路由
- `backend/apps/buildings/serializers.py`：校区-建筑-楼层-房间及树结构序列化
- `backend/apps/buildings/views.py`：建筑域查询与管理接口（含 `tree`）
- `backend/apps/buildings/urls.py`：`/api/campuses|buildings|floors|rooms` 路由
- `backend/apps/*/models.py`：领域模型与约束
- `backend/apps/*/migrations/`：数据库结构演进记录
- `sql/init_db.sql`：数据库初始化与种子数据脚本

## 架构见解
- 统一响应与统一异常处理已下沉到框架层，业务视图保持薄控制器。
- API 权限模型已形成通用基元（`IsAdmin`、`IsAdminOrReadOnly`、`IsOwnerOrAdmin`），后续应用可复用。
- 建筑域采用“列表/详情 + 树结构”双输出口径，兼容管理页和监测树场景。

## 演进规则
- 实施步骤完成后，先更新 `memory-bank/progress.md`。
- 架构边界变化时，先更新 `memory-bank/architecture.md`，再调整代码实现。
