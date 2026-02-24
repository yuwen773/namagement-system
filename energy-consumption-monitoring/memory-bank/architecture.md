# 架构说明

## 技术栈

**后端**：Django 5.2 + DRF + MySQL 8.0
**前端**：Vue 3 + Element Plus + ECharts + Pinia
**开发策略**：后端优先，前端后置

---

## 分层架构

```
┌─────────────────────────────────────┐
│  展示层 (Vue 3)                      │
│  layouts/ + views/ + stores/        │
└─────────────────────────────────────┘
              ↕ HTTP/REST
┌─────────────────────────────────────┐
│  业务层 (Django Apps)                │
│  accounts │ buildings │ devices     │
│  energy │ analysis │ alarms │ system │
└─────────────────────────────────────┘
              ↕ ORM
┌─────────────────────────────────────┐
│  持久层 (MySQL 8.0 utf8mb4)          │
│  em_* 表：用户/建筑/设备/能耗/告警/系统 │
└─────────────────────────────────────┘
```

---

## 关键文件

| 类型 | 文件 | 职责 |
|:---|:---|:---|
| 后端 | `settings.py` | 全局配置 |
| 后端 | `permissions.py` | 权限类 |
| 后端 | `apps/*/models.py` | 数据模型 |
| 后端 | `apps/*/views.py` | API 视图 |
| 前端 | `router/index.js` | 路由 + 守卫 |
| 前端 | `stores/*.js` | 状态管理 |
| 前端 | `api/*.js` | API 封装 |
| 前端 | `layouts/*.vue` | 布局组件 |
| 前端 | `views/**/*.vue` | 页面组件 |

---

## 页面清单

### 管理端 `/admin` (7个)
- Dashboard - 综合监控
- Monitoring - 监测中心
- Analysis - 统计分析
- Alarms - 异常告警
- Devices - 设备管理
- Configuration - 基础配置
- System - 系统管理

### 用户端 `/user` (6个)
- Dashboard - 个人首页 ✅
- UsageHistory - 用能查询 ✅
- CostPayment - 费用充值 ✅
- Comparison - 能耗对比 ✅
- Notices - 节能公告 ✅
- Profile - 个人中心 ✅

---

## 数据模型

| 模块 | 表 |
|:---|:---|
| accounts | em_users, em_roles |
| buildings | em_campuses, em_buildings, em_floors, em_rooms |
| devices | em_energy_types, em_devices |
| energy | em_energy_data, em_energy_statistics |
| alarms | em_alarm_rules, em_alarms |
| system | em_bills, em_recharge_records, em_notices, em_operation_logs |
| analysis | em_energy_forecasts |

---

## 设计规范

| 类别 | 规范 |
|:---|:---|
| 色彩 | #f97316 橙 / #eab308 黄 / #22c55e 绿 / #ef4444 红 / #3b82f6 蓝 |
| 字体 | Orbitron（数字）、Noto Sans SC（中文） |
| 组件 | 16px 圆角、1px 边框、hover 上移 |
| 图表 | shallowRef + dispose、响应式 |

---

## API 响应格式

```json
{
  "code": 0,
  "data": {},
  "message": "",
  "total": 0
}
```

---

## 用户端页面架构详解

### Notices.vue - 节能公告页面

**文件路径**：`frontend/src/views/user/Notices.vue`

**职责**：
- 展示通知公告列表（支持按优先级、已读状态筛选）
- 提供节能知识卡片展示
- 支持通知详情查看和已读标记

**架构特点**：
1. **Tab 切换模式**：使用 `v-if` + `transition` 实现 Tab 切换动画
2. **筛选逻辑**：使用 `computed` 实现响应式数据过滤
3. **状态管理**：本地状态管理，通过 `getNotices()` API 获取数据
4. **时间格式化**：`formatTime()` 函数实现相对时间显示

**API 对接**：
- `getNotices(params)` - 获取通知列表
- `getNotice(id)` - 获取通知详情（预留）

**样式规范**：
- 使用渐变背景 `.page-header` 增强视觉冲击
- 未读通知使用黄色渐变背景 `.notice-card.unread`
- 节能知识卡片使用 5 种颜色主题轮换

---

### Profile.vue - 个人中心页面

**文件路径**：`frontend/src/views/user/Profile.vue`

**职责**：
- 基本资料编辑（头像上传、表单验证）
- 房间绑定管理（添加/解绑）
- 告警订阅设置（开关控制）

**架构特点**：
1. **三 Tab 布局**：基本资料 | 账号绑定 | 告警订阅
2. **表单验证**：使用 Element Plus `el-form` + `rules` 实现
3. **级联选择**：建筑 → 楼层 → 房间三级联动
4. **头像上传**：使用 `FormData` + `multipart/form-data`

**API 对接**：
- `getMyProfile()` - 获取个人资料
- `updateMyProfile(data)` - 更新个人资料
- `getMyBindRooms()` - 获取已绑定房间
- `bindRoom(data)` - 绑定房间
- `unbindRoom(roomId)` - 解绑房间
- `getMyAlarmSubscriptions()` - 获取告警订阅
- `updateAlarmSubscriptions(data)` - 更新告警订阅
- `uploadAvatar(data)` - 上传头像

**数据流**：
```
API 响应 → 更新本地状态 → 同步 Pinia Store → UI 自动更新
```

**样式规范**：
- 头像区域使用渐变背景和阴影突出显示
- 表单区域使用浅灰背景区分
- 房间卡片 hover 效果增强交互反馈

---

## 前端组件复用模式

| 组件 | 位置 | 用途 |
|:---|:---|:---|
| UserLayout | `layouts/UserLayout.vue` | 用户端统一布局（顶部导航） |
| Dashboard | `views/user/Dashboard.vue` | 个人首页（指标卡片 + 趋势图） |
| Notices | `views/user/Notices.vue` | 通知公告（Tab 切换） |
| Profile | `views/user/Profile.vue` | 个人中心（表单验证） |

**共享模式**：
- 所有页面使用相同的 `.page-header` 渐变样式
- 统一使用 16px 圆角和 1px 边框
- Tab 导航使用相同的基础样式

