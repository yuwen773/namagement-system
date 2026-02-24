# 需求追踪矩阵（RTM）

## 文档说明
- 维护范围：`memory-bank/pre-prd.md` 与 `memory-bank/PRD.md` 的需求到实现、测试、证据的全链路追踪。
- 状态枚举：`未开始` / `进行中` / `已完成` / `已验收`。
- 更新时间要求：需求变更后 24 小时内更新本文件。
- 最近更新：2026-02-24（阶段四 `4.4` 建立初版 RTM）。

## pre-prd 需求追踪
| 需求ID | 来源文档 | 需求描述 | 实施步骤 | 代码位置 | 测试用例 | 证据链接 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRE-T1 | `memory-bank/pre-prd.md` | 选用合适操作系统和开发环境 | `1.2`、`1.4` | `backend/requirements.txt`<br>`backend/energy_monitoring/settings.py` | `python manage.py check` 成功 | `memory-bank/progress.md` | 已验收 |
| PRE-T2 | `memory-bank/pre-prd.md` | 使用 Modbus/BACnet 协议自动采集能耗数据 | `1.5` | `scripts/protocol_collection/collector.py`<br>`scripts/protocol_collection/adapters.py` | `python -m scripts.protocol_collection.validate_phase_1_5`（5项 PASS） | `scripts/protocol_collection/README.md`<br>`scripts/protocol_collection/output/phase_1_5_validation.jsonl` | 已验收 |
| PRE-T3 | `memory-bank/pre-prd.md` | 构建 MySQL 存储架构管理实时与历史数据 | `1.3`、`2.1`~`2.9` | `sql/init_db.sql`<br>`backend/apps/energy/models.py` | `python manage.py migrate` 成功 | `memory-bank/progress.md`<br>`sql/init_db.sql` | 已验收 |
| PRE-T4 | `memory-bank/pre-prd.md` | 基于 Spark 实现清洗、整合、多维分析 | `6.1`~`6.4`（规划） | `scripts/`（规划） | `实施计划 6.x` 验证项 | `memory-bank/implementation-plan.md` | 未开始 |
| PRE-T5 | `memory-bank/pre-prd.md` | 使用 Vue + ECharts 构建可视化界面 | `7.1`~`9.7`（规划） | `frontend/src/`（规划） | `实施计划 8.x/9.x` 页面验证 | `memory-bank/implementation-plan.md` | 未开始 |
| PRE-T6 | `memory-bank/pre-prd.md` | 开展功能验证与性能测试并优化 | `10.1`~`10.6`（规划） | `backend/apps/*/tests.py`<br>`frontend/tests/`（规划） | `pytest`、`vitest`、E2E 与性能验证 | `memory-bank/implementation-plan.md` | 未开始 |
| PRE-R1 | `memory-bank/pre-prd.md` | 研究工业协议采集与多源异构自动化接入 | `1.5`、`3.5` | `scripts/protocol_collection/*.py`<br>`backend/apps/energy/views.py` | 协议采集验收 + 批量导入接口测试 | `scripts/protocol_collection/README.md`<br>`docs/api-reference.md` | 已验收 |
| PRE-R2 | `memory-bank/pre-prd.md` | 研究 Spark 分析流程（趋势、异常、评估） | `3.6`（非 Spark 版本）+ `6.x`（Spark 规划） | `backend/apps/analysis/views.py` | `GET /api/analysis/*` 接口联调 | `docs/api-reference.md`<br>`memory-bank/implementation-plan.md` | 进行中 |
| PRE-R3 | `memory-bank/pre-prd.md` | 构建采集-存储-分析-可视化全流程系统架构 | `1.x`~`4.x` + `7.x`~`9.x`（后续） | `backend/energy_monitoring/urls.py`<br>`frontend/src/`（规划） | 分阶段验收：后端接口 + 前端页面 | `memory-bank/architecture.md`<br>`memory-bank/progress.md` | 进行中 |
| PRE-B1 | `memory-bank/pre-prd.md` | 了解校园能耗管理现状与需求 | `文档阶段`、`1.1` | `memory-bank/PRD.md`<br>`memory-bank/pre-prd.md` | 需求评审与 RTM 覆盖检查 | `docs/rtm.md` | 已验收 |
| PRE-B2 | `memory-bank/pre-prd.md` | 掌握工业协议应用与数据采集技术 | `1.5` | `scripts/protocol_collection/*.py` | 阶段 `1.5` 五项协议验收 | `scripts/protocol_collection/README.md` | 已验收 |
| PRE-B3 | `memory-bank/pre-prd.md` | 掌握 MySQL 架构设计与管理 | `1.3`、`2.1`~`2.9` | `sql/init_db.sql`<br>`backend/apps/*/migrations/*.py` | 建库、迁移、初始化数据检查 | `memory-bank/progress.md` | 已验收 |
| PRE-B4 | `memory-bank/pre-prd.md` | 熟悉 Spark 大数据处理与分析 | `6.x`（规划） | `scripts/`（规划） | `实施计划 6.x` 验证项 | `memory-bank/implementation-plan.md` | 未开始 |
| PRE-B5 | `memory-bank/pre-prd.md` | 掌握 Vue 与 ECharts 开发 | `7.x`~`9.x`（规划） | `frontend/src/`（规划） | `npm run dev` + 页面图表渲染验证 | `memory-bank/implementation-plan.md` | 未开始 |
| PRE-B6 | `memory-bank/pre-prd.md` | 具备系统测试与性能优化能力 | `10.x`（规划） | `backend/apps/*/tests.py`<br>`.github/workflows/`（规划） | 自动化测试 + 性能测试基线对比 | `memory-bank/implementation-plan.md` | 未开始 |
| PRE-B7 | `memory-bank/pre-prd.md` | 具备数据处理与问题解决能力 | `3.5`、`3.6`、`4.1`~`4.3` | `backend/apps/energy/views.py`<br>`backend/apps/analysis/views.py` | 导入、分析、导出、文档联调 | `docs/api-reference.md`<br>`docs/api-spec.json` | 已验收 |

## PRD 需求追踪
| 需求ID | 来源文档 | 需求描述 | 实施步骤 | 代码位置 | 测试用例 | 证据链接 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRD-G1 | `memory-bank/PRD.md` 1.2 | 支持 CSV/Excel 等数据批量导入 | `3.5` + `5.2`（规划增强） | `backend/apps/energy/views.py` | `POST /api/energy-data/batch-import/`（CSV/Excel/JSON） | `docs/api-reference.md` | 进行中 |
| PRD-G2 | `memory-bank/PRD.md` 1.2 | 使用 MySQL 存储历史与业务数据 | `1.3`、`2.1`~`2.9` | `sql/init_db.sql`<br>`backend/apps/*/models.py` | 迁移与初始化 SQL 验证 | `memory-bank/progress.md` | 已验收 |
| PRD-G3 | `memory-bank/PRD.md` 1.2 | 多维分析、异常识别、趋势预测 | `3.6`、`3.7` | `backend/apps/analysis/views.py`<br>`backend/apps/alarms/views.py` | `GET /api/analysis/*`、`GET /api/alarms/statistics/` | `docs/api-reference.md` | 进行中 |
| PRD-G4 | `memory-bank/PRD.md` 1.2 | 提供大屏与多端可视化交互 | `8.x`、`9.x`（规划） | `frontend/src/views/`（规划） | 前端页面加载与图表交互测试 | `memory-bank/implementation-plan.md` | 未开始 |
| PRD-ROLE-1 | `memory-bank/PRD.md` 2 | 系统管理员具备全量管理权限 | `2.3`、`3.9` | `backend/energy_monitoring/permissions.py`<br>`backend/apps/system/views.py` | 管理员访问受限接口返回 200 | `memory-bank/progress.md` | 已验收 |
| PRD-ROLE-2 | `memory-bank/PRD.md` 2 | 普通用户仅查看权限 | `2.3`、`3.9` | `backend/apps/accounts/models.py`<br>`backend/energy_monitoring/permissions.py` | 普通用户访问管理写接口返回 403 | `memory-bank/progress.md` | 已验收 |
| PRD-A1 | `memory-bank/PRD.md` 3.1 | 管理端综合监控大屏 | `3.6` + `8.3`（规划） | `backend/apps/analysis/views.py`<br>`frontend/src/views/admin/Dashboard.vue`（规划） | `GET /api/analysis/dashboard/` + 前端联调 | `docs/api-reference.md` | 进行中 |
| PRD-A2 | `memory-bank/PRD.md` 3.2 | 管理端监测中心 | `3.3`、`3.4`、`3.5` + `8.4`（规划） | `backend/apps/buildings/views.py`<br>`backend/apps/energy/views.py` | `GET /api/buildings/tree/`、`GET /api/energy-data/latest/` | `docs/api-reference.md` | 进行中 |
| PRD-A3 | `memory-bank/PRD.md` 3.3 | 管理端统计分析报表 | `3.6` + `8.5`（规划） | `backend/apps/analysis/views.py` | 趋势/分布/排名/预测/导出接口验证 | `docs/api-reference.md` | 进行中 |
| PRD-A4 | `memory-bank/PRD.md` 3.4 | 管理端异常告警管理 | `3.7` + `8.6`（规划） | `backend/apps/alarms/views.py` | 告警列表、处理、统计接口验证 | `docs/api-reference.md` | 进行中 |
| PRD-A5 | `memory-bank/PRD.md` 3.5 | 管理端设备资产管理 | `3.4` + `8.7`（规划） | `backend/apps/devices/views.py` | 设备 CRUD + `bind-room` + `data-status` | `docs/api-reference.md` | 进行中 |
| PRD-A6 | `memory-bank/PRD.md` 3.6 | 管理端基础档案与费率配置 | `3.3`、`3.4` + `8.8`（规划） | `backend/apps/buildings/views.py`<br>`backend/apps/devices/views.py` | 建筑树与能源类型接口验证 | `docs/api-reference.md` | 进行中 |
| PRD-A7 | `memory-bank/PRD.md` 3.7 | 管理端系统管理（用户/角色/日志） | `3.8` + `8.9`（规划） | `backend/apps/system/views.py` | 用户/角色/日志 API 验证 | `docs/api-reference.md` | 进行中 |
| PRD-U1 | `memory-bank/PRD.md` 4.1 | 用户首页（个人/部门概览） | `3.6`、`3.8` + `9.2`（规划） | `backend/apps/analysis/views.py`<br>`backend/apps/system/views.py` | 用户态查询概览与通知 | `docs/api-reference.md` | 进行中 |
| PRD-U2 | `memory-bank/PRD.md` 4.2 | 用户用能查询明细 | `3.5` + `9.3`（规划） | `backend/apps/energy/views.py` | `GET /api/energy-data/` 时间范围筛选 | `docs/api-reference.md` | 进行中 |
| PRD-U3 | `memory-bank/PRD.md` 4.3 | 用户费用与充值 | `3.8` + `9.4`（规划） | `backend/apps/system/views.py` | `GET /api/bills/my/`、`POST /api/recharges/simulate/` | `docs/api-reference.md` | 进行中 |
| PRD-U4 | `memory-bank/PRD.md` 4.4 | 用户能耗对比与排名 | `3.6` + `9.5`（规划） | `backend/apps/analysis/views.py` | `GET /api/analysis/ranking/`、`comparison/` | `docs/api-reference.md` | 进行中 |
| PRD-U5 | `memory-bank/PRD.md` 4.5 | 节能公告与知识 | `3.8` + `9.6`（规划） | `backend/apps/system/views.py` | `GET /api/notices/`、详情接口 | `docs/api-reference.md` | 进行中 |
| PRD-U6 | `memory-bank/PRD.md` 4.6 | 个人中心与偏好配置 | `3.8` + `9.7`（规划） | `backend/apps/system/views.py` | `GET/PUT /api/profile/`、绑定房间、订阅开关 | `docs/api-reference.md` | 进行中 |
| PRD-NF-P1 | `memory-bank/PRD.md` 5.1 | 百万级导入效率 | `10.2`（规划） | `backend/apps/energy/views.py`<br>`scripts/`（规划） | 百万级导入压测记录 | `memory-bank/implementation-plan.md` | 未开始 |
| PRD-NF-P2 | `memory-bank/PRD.md` 5.1 | 复杂查询响应 < 3 秒 | `10.2`（规划） | `backend/apps/analysis/views.py` | 统计分析接口性能压测 | `memory-bank/implementation-plan.md` | 未开始 |
| PRD-NF-P3 | `memory-bank/PRD.md` 5.1 | Spark 分析分钟级延迟 | `6.x` + `10.2`（规划） | `scripts/`（规划） | Spark 离线任务时延验证 | `memory-bank/implementation-plan.md` | 未开始 |
| PRD-NF-S1 | `memory-bank/PRD.md` 5.2 | 演示场景敏感数据明文存储 | `3.2`（当前实现与 PRD 有偏差） | `backend/apps/accounts/serializers.py` | 校验用户密码存储策略 | `backend/apps/accounts/serializers.py` | 进行中 |
| PRD-NF-S2 | `memory-bank/PRD.md` 5.2 | 基于 RBAC 的权限管理 | `2.3`、`3.9` | `backend/energy_monitoring/permissions.py`<br>`backend/apps/accounts/models.py` | 管理员/普通用户越权测试 | `memory-bank/progress.md` | 已验收 |
| PRD-NF-E1 | `memory-bank/PRD.md` 5.3 | 支持 CSV/Excel/JSON 多格式导入 | `3.5` | `backend/apps/energy/views.py` | 批量导入三种格式验证 | `docs/api-reference.md` | 已验收 |
| PRD-NF-E2 | `memory-bank/PRD.md` 5.3 | 主流浏览器兼容 | `10.4`（规划） | `frontend/`（规划） | Chrome/Firefox/Edge/Safari 兼容测试 | `memory-bank/implementation-plan.md` | 未开始 |
| PRD-ARC-1 | `memory-bank/PRD.md` 6.1 | 前端技术栈 Vue3 + Element Plus + ECharts + Tailwind | `7.x`（规划） | `frontend/package.json`（规划） | `npm run dev` + 组件渲染 | `memory-bank/tech-stack.md` | 未开始 |
| PRD-ARC-2 | `memory-bank/PRD.md` 6.1 | 后端技术栈 Django + DRF | `1.2`、`1.4`、`3.x` | `backend/requirements.txt`<br>`backend/energy_monitoring/settings.py` | `python manage.py check` | `memory-bank/progress.md` | 已验收 |
| PRD-ARC-3 | `memory-bank/PRD.md` 6.1 | Spark 离线分析能力 | `6.x`（规划） | `scripts/`（规划） | Spark 分析任务运行验证 | `memory-bank/implementation-plan.md` | 未开始 |
| PRD-ARC-4 | `memory-bank/PRD.md` 6.1 | MySQL 数据库 | `1.3`、`2.x` | `sql/init_db.sql`<br>`backend/energy_monitoring/settings.py` | 建库与迁移验证 | `memory-bank/progress.md` | 已验收 |
| PRD-ARC-5 | `memory-bank/PRD.md` 6.1 | Pandas/Python 数据导入 | `3.5` + `5.x`（规划增强） | `backend/apps/energy/views.py` | 批量导入接口文件解析验证 | `docs/api-reference.md` | 进行中 |
| PRD-FLOW-1 | `memory-bank/PRD.md` 6.2 | 数据源：CSV/Excel 数据集 | `1.x`、`3.5` | `dataSource/`<br>`backend/apps/energy/views.py` | 上传样例数据集导入验证 | `docs/api-reference.md` | 进行中 |
| PRD-FLOW-2 | `memory-bank/PRD.md` 6.2 | 导入层：清洗后入库 | `3.5`、`5.x`（规划增强） | `backend/apps/energy/serializers.py`<br>`backend/apps/energy/views.py` | 批量导入 + 字段校验 + 入库检查 | `docs/api-reference.md` | 进行中 |
| PRD-FLOW-3 | `memory-bank/PRD.md` 6.2 | 处理层：Spark 聚合与异常检测回写 | `3.6`、`3.7` + `6.x`（Spark 规划） | `backend/apps/analysis/views.py`<br>`backend/apps/alarms/views.py` | 分析/告警 API 验证 + Spark 任务验证 | `docs/api-reference.md`<br>`memory-bank/implementation-plan.md` | 进行中 |
| PRD-FLOW-4 | `memory-bank/PRD.md` 6.2 | 应用层：前端 API 调用与图表渲染 | `7.x`~`9.x`（规划） | `frontend/src/api/`（规划）<br>`frontend/src/views/`（规划） | 管理端/用户端页面联调 | `memory-bank/implementation-plan.md` | 未开始 |

## 覆盖检查
- `pre-prd.md` 需求条目：16/16 已纳入 RTM。
- `PRD.md` 需求条目：35/35 已纳入 RTM。
- 每条需求均绑定至少 1 个测试用例（已验收项均给出可访问证据路径）。

## 维护规则
- 新需求：先分配 `需求ID`，再补齐矩阵 8 列。
- 状态流转：`未开始 -> 进行中 -> 已完成 -> 已验收`。
- 里程碑更新顺序：先更新 `memory-bank/progress.md`，再更新本 RTM 与相关架构文档。
