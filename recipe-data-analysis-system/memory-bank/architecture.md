# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-31
---

## ⚠️ 文档定位

**本文档用途**：记录系统架构设计（技术栈、模块结构、数据模型、API规范）

**请勿在此添加**：
- ❌ 实施细节、测试结果、代码示例
- ❌ 详细的字段说明（代码本身即文档）
- ❌ 工作日志、变更记录

**如需记录实施细节**，请使用：
- `progress.md` - 进度追踪
- `implementation-plan.md` - 实施计划
- 独立的工作日志文件

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
│   ├── src/
│   │   ├── api/        # API 请求模块
│   │   ├── assets/     # 静态资源
│   │   ├── components/ # 公共组件
│   │   ├── router/     # 路由配置
│   │   ├── stores/     # Pinia 状态管理
│   │   └── views/      # 页面组件
├── backend/            # Django 后端
│   ├── config/         # 项目配置
│   ├── utils/          # 公共工具
│   ├── accounts/       # 用户认证
│   ├── recipes/        # 菜谱模块
│   ├── categories/     # 分类模块
│   ├── ingredients/    # 食材模块
│   ├── favorites/      # 收藏模块
│   ├── analytics/      # 数据分析
│   └── admin_panel/    # 管理后台
├── data-scripts/       # 数据脚本
└── memory-bank/        # 项目文档
```

---

## 后端模块

### accounts - 用户认证模块

**接口**：
- `POST /api/accounts/register/` - 用户注册
- `POST /api/accounts/login/` - 用户登录（返回 JWT）
- `GET /api/accounts/me/` - 获取当前用户信息
- `PUT /api/accounts/me/` - 更新用户资料
- `PUT /api/accounts/password/` - 修改密码
- `GET /api/accounts/role-check/` - 角色检查
- `GET /api/accounts/admin/stats/` - 管理员统计

---

### recipes - 菜谱模块

**接口**：
- `GET /api/recipes/` - 菜谱列表（分页、排序、筛选）
- `GET /api/recipes/search/` - 菜谱搜索
- `GET /api/recipes/<id>/` - 菜谱详情
- `GET /api/recipes/hot/` - 热门菜谱
- `POST /api/recipes/upload-image/` - 图片上传

**参数**：
- 列表：`page`, `page_size`, `ordering`, `cuisine_type`, `difficulty`, `scene_type`, `target_audience`
- 搜索：`keyword`, `search_type` (name/ingredient), `page`, `page_size`
- 热门：`sort_by` (view_count/favorite_count), `limit`

---

### categories - 分类模块

**接口**：
- `GET /api/categories/` - 分类列表（支持 type 参数筛选）
- `GET /api/categories/<type>/` - 按类型获取分类

**分类类型**：cuisine（菜系）、scene（场景）、crowd（人群）、taste（口味）、difficulty（难度）

---

### ingredients - 食材模块

**接口**：
- `GET /api/ingredients/` - 食材列表（支持分类筛选、关键词搜索）

**参数**：`category`, `search`, `page`, `page_size`

---

### favorites - 收藏模块

**接口**：
- `POST /api/favorites/` - 收藏菜谱
- `GET /api/favorites/` - 获取收藏列表
- `DELETE /api/favorites/<recipe_id>/` - 取消收藏
- `GET /api/favorites/check/<recipe_id>/` - 检查收藏状态

---

### analytics - 数据分析模块

**接口**：
- `GET /api/analytics/cuisines/` - 菜系分布分析
- `GET /api/analytics/difficulty/` - 难度等级统计
- `GET /api/analytics/flavors/` - 口味偏好分析
- `GET /api/analytics/ingredients/` - 食材使用频率

---

### utils - 公共工具模块

| 文件 | 作用 |
|:-----|:-----|
| `response.py` | 统一响应格式（ApiResponse） |
| `exceptions.py` | 自定义异常类 |
| `exception_handler.py` | 全局异常处理器 |
| `pagination.py` | 分页工具类 |
| `permissions.py` | 权限检查类 |
| `constants.py` | 常量定义 |

---

## 数据库设计

### 核心表结构

| 表名 | 说明 | 关键关系 |
|:-----|:-----|:---------|
| users | 用户主表 | 1:1 user_profiles, 1:N favorites, 1:N behavior_logs |
| user_profiles | 用户资料 | N:1 users |
| recipes | 菜谱主表 | 1:N recipe_ingredients, 1:N favorites |
| categories | 分类标签 | - |
| ingredients | 食材库 | 1:N recipe_ingredients |
| recipe_ingredients | 菜谱-食材关联 | N:1 recipes, N:1 ingredients |
| user_favorites | 用户收藏 | N:1 users, N:1 recipes |
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

**响应格式**：
```json
{"code": 200, "message": "操作成功", "data": {}}
```

**路由规范**：`/api/{module}/{resource}/`

**认证方式**：JWT Token (`Authorization: Bearer <token>`)

**分页参数**：`page`, `page_size` (默认20, 最大100)

---

## 前端模块

### router - 路由配置

**已配置路由**：
- `/` - 首页
- `/recipes` - 菜谱列表
- `/recipes/:id` - 菜谱详情
- `/category/:type?/:value?` - 分类页
- `/hot` - 热门菜谱
- `/login` - 登录
- `/register` - 注册
- `/profile` - 个人信息（需认证）
- `/change-password` - 修改密码（需认证）

### stores - Pinia 状态管理

**user store**：`token`, `userInfo`, `isLoggedIn`, `isAdmin`, `setToken()`, `setUserInfo()`, `logout()`

### views - 页面组件

| 文件 | 作用 |
|:-----|:-----|
| `Home.vue` | 首页 |
| `RecipeList.vue` | 菜谱列表页（搜索、筛选、分页） |
| `RecipeDetail.vue` | 菜谱详情页（收藏、分享） |
| `RecipeCategory.vue` | 分类浏览页 |
| `RecipeHot.vue` | 热门菜谱页 |
| `Login.vue` | 登录页 |
| `Register.vue` | 注册页 |
| `Profile.vue` | 个人信息页 |
| `ChangePassword.vue` | 修改密码页 |

---

## 权限模型

| 角色 | 权限 |
|:-----|:-----|
| user | 浏览/搜索/收藏菜谱，查看只读统计 |
| admin | 全部功能 |

---

## 性能指标

| 指标 | 目标值 |
|:-----|:------:|
| 搜索响应 | < 500ms |
| 详情页加载 | < 1s |
| 大盘加载 | < 2s |
