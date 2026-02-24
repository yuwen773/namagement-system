# 架构说明（Architecture）

## 文档目的
仅记录稳定边界、分层职责、关键文件职责。

## 架构边界（2026-02-24）
- 开发策略：后端优先，前端后置
- 技术基线：Django + DRF + MySQL（utf8mb4）+ Vue 3 + Element Plus + ECharts + Tailwind v3.3.3
- 存储策略：MySQL 单库；em_energy_data（原始）/em_energy_statistics（统计）/em_energy_forecasts（预测）分层
- 业务域：accounts、buildings、devices、energy、analysis、alarms、system
- 统一规范：API 返回 code/data/message/total

## 分层职责
1. **接入层**：文件导入（Pandas）与 Modbus/BACnet 采集
2. **业务层**：Django apps 承载模型、规则、任务命令与 REST API
3. **持久层**：MySQL 承载实体数据、统计数据、预测数据
4. **展示层**：Vue 3 + Pinia + Element Plus + ECharts

## 关键文件职责

### 后端
- `backend/energy_monitoring/settings.py`：全局配置
- `backend/energy_monitoring/permissions.py`：权限类（IsAdmin、IsAdminOrReadOnly、IsOwnerOrAdmin）

**Models**：accounts/`UserProfile`、buildings/`Campus Building Floor Room`、devices/`EnergyType Device`、energy/`EnergyData EnergyStatistics`、alarms/`AlarmRule Alarm`、system/`Bill RechargeRecord Notice OperationLog`、analysis/`EnergyForecast`

**Views**：accounts/登录注册刷新Token用户信息修改密码、analysis/Dashboard趋势分布排名对比预测

**管理命令**：import_energy_data、generate_statistics、check_alarms、generate_forecast、run_scheduled_tasks

**脚本**：data_importer.py、generate_statistics.py、check_alarms.py、generate_forecast.py、scheduled_tasks.py、spark_offline_analysis.py

### 前端
- `frontend/vite.config.js`：Vite 配置（自动导入、代理、别名）
- `frontend/tailwind.config.js`：温暖色系主题（primary橙/success绿/warning黄/danger红）
- `frontend/postcss.config.cjs`：PostCSS 配置（.cjs 扩展名兼容 ES module）
- `frontend/src/main.js`：入口（Element Plus、Router、Pinia、图标注册 icon-ep-xxx）

**Stores**：user（token userInfo role 持久化）、building（树形结构 当前选中）、energy（设备 日期范围 能源类型）

**Router**：`setupRouterGuards(pinia)` 在 Pinia 安装后设置认证守卫和角色权限

**Utils**：request.js（Axios 拦截器 token 401处理）

**API**：auth、building、device、energy、analysis、alarm、system、recharge、profile

**Views**：
- Login.vue（完整）
- AdminLayout.vue（完整）
- admin/Dashboard.vue（8.3）- 综合监控大屏：指标卡片（总能耗/功率/覆盖率/告警）、ECharts 图表（趋势/分布/功率/2D 地图热力）、告警列表、设备状态概览
- admin/Monitoring.vue（8.4）- 监测中心：左侧树形导航（校区-楼宇-楼层-房间）、右侧数据看板（实时数据卡片、趋势折线图、时间选择器、设备列表）
- admin/Analysis.vue（8.5）- 统计分析：筛选区（时间/建筑/能源类型）、图表区（趋势/对比/排名/预测）、导出功能（Excel/PDF）、数据表格
- admin/Alarms.vue（8.6 待实现）、admin/Devices.vue、admin/Configuration.vue、admin/System.vue
- UserLayout.vue（待实现）
- user/Dashboard、UsageHistory、CostPayment、Comparison、Notices、Profile

**Layouts**：AdminLayout.vue（完整）、UserLayout.vue（待实现）

**设计系统（Design System）**：
- **色彩主题**：温暖色系（Primary #f97316 橙、Success #22c55e 绿、Warning #eab308 黄、Danger #ef4444 红、Water #3b82f6 蓝）
- **字体**：Orbitron（数字显示）、Noto Sans SC（中文）、Poppins（英文）
- **组件风格**：卡片式设计（16px 圆角、1px #e5e7eb 边框）、网格背景图案、发光效果、脉冲动画
- **交互反馈**：hover 上移（translateY -4px）、阴影加深、边框高亮 #f97316

**ECharts 图表规范**：
- 使用 `shallowRef` 存储图表实例（避免深度响应）
- `onUnmounted` 时调用 `chart.dispose()` 释放内存
- 图表主题色与系统一致
- 自定义 tooltip（半透明深色背景、橙色边框）
- 自动刷新机制（30秒定时器）
- 响应式处理（window resize 监听）

### 文档
- `memory-bank/implementation-plan.md`：阶段任务与验收口径
- `docs/scheduler.md`：cron 调度说明
- `docs/rtm.md`：需求追踪矩阵

## 维护规则
- 里程碑变化更新 progress.md
- 架构边界变化更新 architecture.md
