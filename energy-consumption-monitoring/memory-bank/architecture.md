# 架构说明（Architecture）

## 文档目的
仅记录稳定边界、分层职责、关键文件职责。

## 架构边界（2026-02-24）
- 开发策略：后端优先，前端后置。
- 技术基线：Django + DRF + MySQL（`utf8mb4`）+ Vue 3 + Element Plus + ECharts。
- 存储策略：MySQL 单库；`em_energy_data`（原始）、`em_energy_statistics`（统计）、`em_energy_forecasts`（预测）分层。
- 业务域：`accounts`、`buildings`、`devices`、`energy`、`analysis`、`alarms`、`system`。
- 统一规范：API 返回 `code/data/message/total`；需求追踪在 `docs/rtm.md`。

## 分层职责
1. **接入层**：文件导入（Pandas）与 Modbus/BACnet 协议采集，统一写入原始能耗表。
2. **业务层**：Django apps 承载模型、规则、任务命令与 REST API。
3. **持久层**：MySQL 承载实体数据、统计数据、预测数据及索引约束。
4. **展示层**：Vue 3 + Pinia + Element Plus + ECharts + Tailwind CSS v3.3.3。

## 关键文件职责

### 文档与配置
- `memory-bank/implementation-plan.md`：阶段任务与验收口径。
- `memory-bank/progress.md`：当前状态与下一步。
- `memory-bank/architecture.md`：稳定边界与职责。

### 后端（Backend）
- `backend/energy_monitoring/settings.py`：全局配置（数据库、DRF、JWT、CORS）。
- `backend/energy_monitoring/permissions.py`：自定义权限类（`IsAdmin`、`IsAdminOrReadOnly`、`IsOwnerOrAdmin`）。

**Models**：
- `backend/apps/accounts/models.py`：`UserProfile`（role、bind_rooms）。
- `backend/apps/buildings/models.py`：`Campus`、`Building`、`Floor`、`Room` 层级结构。
- `backend/apps/devices/models.py`：`EnergyType`、`Device`。
- `backend/apps/energy/models.py`：`EnergyData`（原始）、`EnergyStatistics`（统计）。
- `backend/apps/alarms/models.py`：`AlarmRule`、`Alarm`。
- `backend/apps/system/models.py`：`Bill`、`RechargeRecord`、`Notice`、`OperationLog`。
- `backend/apps/analysis/models.py`：`EnergyForecast`（预测）。

**Views & APIs**：
- `backend/apps/accounts/views.py`：登录/注册/刷新 Token/用户信息/修改密码。
- `backend/apps/analysis/views.py`：Dashboard/趋势/分布/排名/对比/预测 API。

**管理命令**：
- `backend/apps/energy/management/commands/import_energy_data.py`：数据导入。
- `backend/apps/energy/management/commands/generate_statistics.py`：统计聚合。
- `backend/apps/energy/management/commands/check_alarms.py`：告警检测。
- `backend/apps/energy/management/commands/generate_forecast.py`：预测生成。
- `backend/apps/energy/management/commands/run_scheduled_tasks.py`：定时任务入口。

**脚本**：
- `scripts/data_importer.py`：多格式数据导入与分批写入。
- `scripts/generate_statistics.py`：统计聚合实现。
- `scripts/check_alarms.py`：告警检测实现。
- `scripts/generate_forecast.py`：7/30 天预测生成实现。
- `scripts/scheduled_tasks.py`：定时任务组合逻辑。
- `scripts/spark_offline_analysis.py`：Spark 可选离线分析与 Python 回退。

### 前端（Frontend）
- `frontend/vite.config.js`：Vite 配置（Element Plus 自动导入、代理、路径别名）。
- `frontend/tailwind.config.js`：Tailwind v3.3.3 主题（温暖色系：primary 橙色、success 绿色、warning 黄色、danger 红色）。
- `frontend/postcss.config.cjs`：PostCSS 配置（Tailwind、Autoprefixer），使用 .cjs 扩展名以兼容 ES module 项目。
- `frontend/src/main.js`：应用入口（Element Plus、Router、Pinia setup、图标注册）。

**Stores（Pinia）**：
- `frontend/src/stores/user.js`：用户状态（token、userInfo、role、持久化）。
- `frontend/src/stores/building.js`：建筑选择状态（树形结构、当前选中）。
- `frontend/src/stores/energy.js`：能耗查询状态（设备、日期范围、能源类型）。

**Router**：
- `frontend/src/router/index.js`：路由配置、`setupRouterGuards(pinia)` 函数用于在 Pinia 安装后设置认证守卫和角色权限控制。

**Utils**：
- `frontend/src/utils/request.js`：Axios 实例、请求/响应拦截器、token 注入、401 处理。

**API Modules**：
- `frontend/src/api/auth.js`：登录/注册/刷新/用户信息/修改密码。
- `frontend/src/api/building.js`：校区/建筑/楼层/房间 CRUD + 树形结构。
- `frontend/src/api/device.js`：设备/能源类型 CRUD + 绑定房间。
- `frontend/src/api/energy.js`：能耗数据录入/批量导入/统计/导出。
- `frontend/src/api/analysis.js`：Dashboard/趋势/分布/排名/对比/预测。
- `frontend/src/api/alarm.js`：告警规则/告警记录/处理/统计。
- `frontend/src/api/system.js`：用户/角色/账单/通知/日志。
- `frontend/src/api/recharge.js`：充值记录/模拟充值。
- `frontend/src/api/profile.js`：个人中心/绑定房间/告警订阅。

**Views**：
- `frontend/src/views/Login.vue`：登录页（完整实现，带动画、表单验证、API 集成）。

**Layouts**：
- `frontend/src/layouts/AdminLayout.vue`：管理端布局（侧边栏/顶栏/内容区、通知抽屉、完整交互）。
- `frontend/src/layouts/UserLayout.vue`：用户端布局（顶栏/内容区，待实现）。

**Views（占位，待实现）**：
- `frontend/src/views/admin/`：Dashboard（8.3）、Monitoring、Analysis、Alarms、Devices、Configuration、System。
- `frontend/src/views/user/`：Dashboard、UsageHistory、CostPayment、Comparison、Notices、Profile。

### 图标注册
- 在 `main.js` 中，为所有 Element Plus 图标注册两个版本：
  - 原始 PascalCase 名称（如 `User`、`Lock`）
  - `icon-ep-` 前缀 + kebab-case 名称（如 `icon-ep-user`、`icon-ep-lock`）
- 模板中统一使用 `icon-ep-xxx` 格式以保持命名一致性

### 文档
- `docs/scheduler.md`：cron 调度说明。
- `docs/rtm.md`：需求追踪矩阵。

## 维护规则
- 里程碑变化更新 `memory-bank/progress.md`。
- 架构边界变化更新 `memory-bank/architecture.md`。
