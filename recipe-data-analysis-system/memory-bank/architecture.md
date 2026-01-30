# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-30（阶段四完成）

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
├── backend/            # Django 后端
│   ├── config/         # 项目配置
│   ├── utils/          # 公共工具（response/exceptions/pagination/permissions）
│   ├── accounts/       # 用户认证
│   ├── recipes/        # 菜谱模块
│   ├── categories/     # 分类模块
│   ├── ingredients/    # 食材模块
│   ├── favorites/      # 收藏模块
│   ├── analytics/      # 数据分析
│   └── admin_panel/    # 管理后台
├── data-scripts/       # 数据脚本
├── memory-bank/        # 项目文档
└── CLAUDE.md           # 开发指导
```

---

## 后端模块说明

### accounts - 用户认证模块

| 文件 | 作用 |
|:-----|:-----|
| `models.py` | User 模型（用户名/密码/角色/状态）、UserProfile 模型（昵称/头像/简介） |
| `serializers.py` | RegisterSerializer（注册）、LoginSerializer（登录）、UserSerializer（用户信息）、UpdateProfileSerializer（更新资料）、ChangePasswordSerializer（修改密码） |
| `views.py` | register（注册）、login（登录+JWT生成）、me（获取/更新当前用户）、change_password（修改密码）、role_check（角色检查）、admin_stats（管理员统计） |
| `urls.py` | `/api/accounts/register/`、`/api/accounts/login/`、`/api/accounts/me/`、`/api/accounts/password/`、`/api/accounts/role-check/`、`/api/accounts/admin/stats/` |

**已实现接口**（7/7）：
- `POST /api/accounts/register/` - 用户注册
- `POST /api/accounts/login/` - 用户登录（返回 JWT Token）
- `GET /api/accounts/me/` - 获取当前用户信息（需认证）
- `PUT /api/accounts/me/` - 更新当前用户资料（需认证）
- `PUT /api/accounts/password/` - 修改密码（需认证）
- `GET /api/accounts/role-check/` - 角色检查（需认证）
- `GET /api/accounts/admin/stats/` - 管理员统计（需管理员权限）

---

### utils - 公共工具模块

| 文件 | 作用 |
|:-----|:-----|
| `response.py` | 统一响应格式（ApiResponse） |
| `exceptions.py` | 自定义异常类（BusinessError, ValidationError, NotFoundError, PermissionDeniedError） |
| `pagination.py` | 分页工具类 |
| `permissions.py` | 权限检查类（IsAdminUser, IsAdminUserOrReadOnly） |
| `constants.py` | 常量定义（UserRole, CategoryType, IngredientCategory, BehaviorType） |

**权限类说明**：
- `IsAdminUser` - 仅允许管理员访问，普通用户返回 403
- `IsAdminUserOrReadOnly` - 管理员可全部操作，普通用户仅读操作

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

## 权限模型

| 角色 | 权限 |
|:-----|:-----|
| user | 浏览/搜索/收藏菜谱，查看统计 |
| admin | 全部功能 |

---

## 性能指标

| 指标 | 目标值 |
|:-----|:------:|
| 搜索响应 | < 500ms |
| 详情页加载 | < 1s |
| 大盘加载 | < 2s |
