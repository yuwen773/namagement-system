# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-31（阶段十八全部完成）

---

## 系统架构

```
前端层 (Vue 3)
    │ REST API
    ▼
API 层 (Django + DRF)
    │ ORM
    ▼
数据层 (MySQL 8.0+)
```

---

## 技术栈

| 层级 | 技术选型 |
|:-----|:---------|
| 前端 | Vue 3 + Element Plus + Tailwind + ECharts + Pinia |
| 后端 | Django 5.2 + DRF + JWT + Pandas |
| 数据库 | MySQL 8.0+ |

---

## 项目结构

```
recipe-data-analysis-system/
├── frontend/           # Vue 3 前端
│   └── src/
│       ├── api/        # API 请求模块
│       ├── components/ # 公共组件
│       ├── router/     # 路由配置
│       ├── stores/     # Pinia 状态管理
│       └── views/      # 页面组件
├── backend/            # Django 后端
│   ├── config/         # 项目配置
│   ├── utils/          # 公共工具
│   ├── verify_script/  # 测试脚本
│   ├── accounts/       # 用户认证
│   ├── recipes/        # 菜谱模块
│   ├── categories/     # 分类模块
│   ├── ingredients/    # 食材模块
│   ├── favorites/      # 收藏模块
│   ├── analytics/      # 数据分析
│   ├── admin_panel/    # 管理仪表盘
│   └── behavior_logs/  # 用户行为日志
├── data-scripts/       # 数据脚本
└── memory-bank/        # 项目文档
```

---

## 后端模块

### admin_panel - 管理仪表盘

| 接口 | 功能 |
|:-----|:-----|
| GET /api/admin/dashboard/overview/ | 数据总览 |
| GET /api/admin/dashboard/trends/ | 数据趋势 |
| GET /api/admin/dashboard/behaviors/ | 用户行为统计 |

### accounts - 用户认证

| 接口 | 功能 |
|:-----|:-----|
| POST /api/accounts/register/ | 用户注册 |
| POST /api/accounts/login/ | 用户登录 |
| GET /api/accounts/me/ | 当前用户信息 |
| PUT /api/accounts/me/ | 更新用户资料 |
| GET /api/accounts/admin/users/ | 用户列表（管理） |
| PUT /api/accounts/admin/users/<id>/ban/ | 封禁用户 |

### recipes - 菜谱模块

| 接口 | 功能 |
|:-----|:-----|
| GET /api/recipes/ | 菜谱列表 |
| GET /api/recipes/search/ | 菜谱搜索 |
| GET /api/recipes/<id>/ | 菜谱详情 |
| GET /api/recipes/hot/ | 热门菜谱 |
| GET /api/admin/recipes/ | 菜谱管理列表 |
| POST /api/admin/recipes/create/ | 创建菜谱 |
| DELETE /api/admin/recipes/<id>/delete/ | 删除菜谱 |

### categories - 分类模块

| 接口 | 功能 |
|:-----|:-----|
| GET /api/categories/ | 分类列表 |
| GET /api/admin/categories/ | 分类管理 |
| POST /api/admin/categories/create/ | 创建分类 |
| DELETE /api/admin/categories/<id>/delete/ | 删除分类 |

### ingredients - 食材模块

| 接口 | 功能 |
|:-----|:-----|
| GET /api/ingredients/ | 食材列表 |
| GET /api/admin/ingredients/ | 食材管理 |
| POST /api/admin/ingredients/create/ | 创建食材 |

### favorites - 收藏模块

| 接口 | 功能 |
|:-----|:-----|
| POST /api/favorites/ | 收藏菜谱 |
| GET /api/favorites/ | 收藏列表 |
| DELETE /api/favorites/<recipe_id>/ | 取消收藏 |

### analytics - 数据分析

| 接口 | 功能 |
|:-----|:-----|
| GET /api/analytics/cuisines/ | 菜系分布 |
| GET /api/analytics/difficulty/ | 难度统计 |
| GET /api/analytics/flavors/ | 口味偏好 |
| GET /api/analytics/ingredients/ | 食材频率 |
| GET /api/admin/analytics/cuisines/ | 菜系深度分析 |
| GET /api/admin/analytics/hot/ | 热门菜谱分析 |
| GET /api/admin/analytics/ingredient-pairs/ | 食材关联分析 |
| GET /api/admin/analytics/clickstream/ | 点击流分析 |
| GET /api/admin/analytics/active-users/ | 活跃用户分析 |
| GET /api/admin/analytics/login-frequency/ | 登录频次分析 |
| GET /api/admin/analytics/page-duration/ | 页面停留分析 |

### analytics/views.py - 用户行为分析视图

| 类名 | 功能 |
|:-----|:-----|
| ClickStreamAnalysisView | 点击流分析，含路径模式和转化漏斗 |
| ActiveUsersAnalysisView | 活跃用户分析，含 DAU/WAU/MAU |
| LoginFrequencyAnalysisView | 登录频次分析，含时间段分布 |
| PageDurationAnalysisView | 页面停留分析，含各页面统计 |

### behavior_logs - 用户行为日志

**核心模型**：UserBehaviorLog

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| user | FK | 用户（可为空） |
| behavior_type | Char | 行为类型 |
| target | Char | 行为目标 |
| timestamp | DateTime | 行为时间 |
| extra_data | JSON | 额外数据 |

### utils - 公共工具

| 文件 | 作用 |
|:-----|:-----|
| response.py | 统一响应格式 |
| exceptions.py | 自定义异常 |
| permissions.py | 权限检查 |
| constants.py | 常量定义 |

---

## 数据库设计

### 核心表结构

| 表名 | 说明 | 关键关系 |
|:-----|:-----|:---------|
| users | 用户主表 | 1:1 user_profiles, 1:N favorites |
| user_profiles | 用户资料 | N:1 users |
| recipes | 菜谱主表 | 1:N recipe_ingredients |
| categories | 分类标签 | - |
| ingredients | 食材库 | 1:N recipe_ingredients |
| recipe_ingredients | 菜谱-食材关联 | N:1 recipes/ingredients |
| user_favorites | 用户收藏 | N:1 users/recipes |
| user_behavior_logs | 行为日志 | N:1 users |

### 数据规模目标

| 数据类型 | 目标数量 |
|:---------|:--------:|
| 菜谱数据 | 10,000-20,000 |
| 食材数据 | 500+ |
| 用户数据 | 100+ |
| 行为日志 | 10,000+ |

---

## API 规范

**响应格式**：`{"code": 200, "message": "操作成功", "data": {}}`

**路由规范**：`/api/{module}/{resource}/`

**认证**：JWT Token (`Authorization: Bearer <token>`)

**分页**：`page`, `page_size` (默认20, 最大100)

---

## 前端模块

### router - 路由配置

| 路径 | 功能 |
|:-----|:-----|
| / | 首页 |
| /recipes | 菜谱列表 |
| /recipes/:id | 菜谱详情 |
| /category/:type?/:value? | 分类页 |
| /hot | 热门菜谱 |
| /analytics | 数据概览 |
| /login, /register | 登录/注册 |
| /profile | 个人信息 |
| /favorites | 我的收藏 |
| /admin | 用户管理 |
| /admin/recipes | 菜谱管理 |
| /admin/ingredients | 食材管理 |
| /admin/categories | 分类管理 |
| /admin/dashboard | 数据仪表盘 |
| /admin/analytics | 深度数据分析 |
| /admin/behavior | 用户行为分析 |

### views - 前端页面组件

| 文件 | 功能 |
|:-----|:-----|
| MyFavorites.vue | 我的收藏页面（阶段十一第1步新增） |
| | - 收藏菜谱列表展示 |
| | - 取消收藏功能 |
| | - 排序（最新/最早收藏） |
| | - 分页加载 |
| AdminDashboard.vue | 管理后台数据仪表盘（阶段十六第4步新增） |
| | - 关键指标卡片（菜谱数、用户数、活跃度） |
| | - 数据趋势折线图 |
| | - 用户行为分布饼图 |
| UserBehaviorAnalytics.vue | 用户行为分析页面（阶段十八第5步新增） |
| | - 点击流分析（桑基图、转化漏斗） |
| | - 活跃用户趋势（DAU/WAU/MAU） |
| | - 登录频次分布（柱状图、时段分析） |
| | - 页面停留分析（热力图、统计表） |

### api - API 模块

| 文件 | 作用 |
|:-----|:-----|
| auth.js | 用户认证 |
| recipes.js | 菜谱/分类/食材 |
| analytics.js | 数据分析 |

### stores

**user store**：token, userInfo, isLoggedIn, isAdmin

---

## 权限模型

| 角色 | 权限 |
|:-----|:-----|
| user | 浏览、搜索、收藏、查看统计 |
| admin | 全部功能 |

---

## 性能指标

| 指标 | 目标值 |
|:-----|:------:|
| 搜索响应 | < 500ms |
| 详情页加载 | < 1s |
| 大盘加载 | < 2s |
