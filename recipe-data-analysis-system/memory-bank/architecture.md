# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-30（阶段七第4步完成，食材使用频率统计接口测试通过 6/6）

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
│   ├── admin_panel/    # 管理后台
│   └── verify_script/  # API 测试脚本
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

### recipes - 菜谱模块

| 文件 | 作用 |
|:-----|:-----|
| `models.py` | Recipe 模型（菜谱主表）、RecipeIngredient 模型（菜谱-食材关联） |
| `serializers.py` | RecipeListSerializer（列表）、RecipeDetailSerializer（详情+食材）、RecipeIngredientSerializer（食材关联） |
| `views.py` | recipe_list（列表，支持分页/排序/筛选）、recipe_detail（详情+行为日志）、recipe_search（搜索）、hot_recipes（热门菜谱，按点击量/收藏量排序）、upload_image（图片上传） |
| `urls.py` | `/api/recipes/`、`/api/recipes/<id>/`、`/api/recipes/search/`、`/api/recipes/hot/`、`/api/recipes/upload-image/`、`/api/recipes/<id>/upload-image/` |

**已实现接口**（5/6）：
- `GET /api/recipes/` - 菜谱列表（支持分页、排序、筛选）
- `GET /api/recipes/search/` - 菜谱搜索（支持关键词名称搜索、食材搜索、分页）
- `GET /api/recipes/<id>/` - 菜谱详情（完整信息+食材列表+行为日志记录）
- `GET /api/recipes/hot/` - 热门菜谱（按点击量或收藏量排序，支持自定义返回数量）
- `POST /api/recipes/upload-image/` - 通用图片上传（需认证）
- `POST /api/recipes/<id>/upload-image/` - 菜谱图片上传（需认证）

**详情接口功能**：
- 返回菜谱完整信息（基本信息、食材列表、详细步骤、口味标签）
- 自动增加点击量计数
- 记录用户浏览行为到 `user_behavior_logs` 表
- 支持登录用户和未登录用户的行为记录

**列表接口参数**：
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认20，最大100）
- `ordering` - 排序字段（可选：view_count, -view_count, favorite_count, -favorite_count, created_at, -created_at）
- `cuisine_type` - 菜系筛选
- `difficulty` - 难度筛选
- `scene_type` - 场景筛选
- `target_audience` - 人群筛选

**搜索接口参数** (`/api/recipes/search/`)：
- `keyword` - 搜索关键词（必填）
- `search_type` - 搜索类型（可选：name-按名称搜索，ingredient-按食材搜索，默认name）
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认20，最大100）

**热门菜谱接口参数** (`/api/recipes/hot/`)：
- `sort_by` - 排序方式（可选：view_count-按点击量，favorite_count-按收藏量，默认view_count）
- `limit` - 返回数量（可选，1-50，默认20）

---

### categories - 分类模块

| 文件 | 作用 |
|:-----|:-----|
| `models.py` | Category 模型（分类主表，支持菜系/场景/人群/口味类型） |
| `serializers.py` | CategorySerializer（完整信息）、CategoryListSerializer（列表） |
| `views.py` | category_list（分类列表，支持按类型筛选）、category_by_type（按类型路径获取） |
| `urls.py` | `/api/categories/`、`/api/categories/<type>/` |

**已实现接口**（2/2）：
- `GET /api/categories/` - 分类列表（支持按 type 参数筛选：cuisine/scene/crowd/taste/difficulty）
- `GET /api/categories/<type>/` - 按类型路径获取分类

**分类数据**：
- 菜系（8个）：川菜、粤菜、鲁菜、苏菜、浙菜、湘菜、徽菜、闽菜
- 场景（7个）：早餐、午餐、晚餐、下午茶、夜宵、快手菜、宴客菜
- 人群（5个）：儿童、老人、孕妇、健身人群、素食者
- 口味（7个）：辣、甜、酸、咸、鲜、清淡、麻

**接口参数**：
- `type` - 分类类型筛选（可选）

---

### ingredients - 食材模块

| 文件 | 作用 |
|:-----|:-----|
| `models.py` | Ingredient 模型（食材库，包含名称、分类等字段） |
| `serializers.py` | IngredientSerializer（完整信息）、IngredientListSerializer（列表） |
| `views.py` | ingredient_list（食材列表，支持按分类筛选、关键词搜索） |
| `urls.py` | `/api/ingredients/` |

**已实现接口**（1/1）：
- `GET /api/ingredients/` - 食材列表（支持按 category 分类筛选、search 关键词搜索、分页）

**食材分类**：
- 蔬菜 (vegetable)、肉类 (meat)、海鲜 (seafood)、调料 (seasoning)
- 水果 (fruit)、谷物 (grain)、乳制品 (dairy)、其他 (other)

**接口参数**：
- `category` - 食材分类筛选（可选：vegetable/meat/seafood/seasoning/fruit/grain/dairy/other）
- `search` - 搜索食材名称（可选，模糊匹配）
- `page` - 页码（默认1）
- `page_size` - 每页数量（默认20，最大100）

---

### favorites - 收藏模块

| 文件 | 作用 |
|:-----|:-----|
| `models.py` | UserFavorite 模型（用户收藏表，存储用户对菜谱的收藏关系） |
| `serializers.py` | FavoriteCreateSerializer（创建收藏）、FavoriteListSerializer（收藏列表）、FavoriteSerializer（收藏详情） |
| `views.py` | FavoriteViewSet（收藏创建/列表）、FavoriteDetailView（取消收藏）、check_favorite_status（检查状态） |
| `urls.py` | `/api/favorites/`、`/api/favorites/<recipe_id>/`、`/api/favorites/check/<recipe_id>/` |

**UserFavorite 模型字段**：
- `user` - 关联用户（外键）
- `recipe` - 关联菜谱（外键）
- `created_at` - 收藏时间

**约束**：
- 联合唯一约束（user + recipe），防止重复收藏

**已实现接口**（4/4）：
- `POST /api/favorites/` - 收藏菜谱（需认证）
- `GET /api/favorites/` - 获取收藏列表（需认证，支持分页）
- `DELETE /api/favorites/<recipe_id>/` - 取消收藏（需认证）
- `GET /api/favorites/check/<recipe_id>/` - 检查收藏状态（需认证）

**接口功能**：
- 收藏时自动增加菜谱的 `favorite_count`
- 取消收藏时自动减少菜谱的 `favorite_count`
- 自动记录收藏/取消收藏行为到 `user_behavior_logs` 表
- 防止重复收藏同一菜谱
- 取消收藏前检查是否已收藏

**架构设计说明**：

1. **数据一致性**：
   - 使用 `IntegrityError` 捕获和联合唯一约束确保数据一致性
   - 收藏/取消操作与 `favorite_count` 字段同步更新

2. **行为追踪**：
   - 收藏行为（`COLLECT`）和取消收藏行为（`UNCOLLECT`）均记录到行为日志
   - 日志包含 `recipe_id`、`recipe_name`、`cuisine_type` 等上下文信息

3. **API 设计**：
   - 使用 `ViewSet` + `APIView` 混合模式
   - `FavoriteViewSet` 处理集合操作（列表、创建）
   - `FavoriteDetailView` 处理单个资源操作（删除）
   - 路由使用 recipe_id 作为路径参数（而非主键ID），更符合业务语义

4. **测试覆盖**：
   - 12 项测试覆盖正常流程、异常流程、边界条件
   - 测试包括：重复收藏、取消未收藏菜谱、收藏量同步、行为日志记录

**测试结果**：12/12 通过（2026-01-30 验证）

**阶段六第4步测试详情**（检查收藏状态接口）：
- ✅ 检查已收藏的菜谱，`is_favorited` 返回 `true`
- ✅ 检查未收藏的菜谱，`is_favorited` 返回 `false`
- ✅ 未认证访问返回 401

---

### behavior_logs - 用户行为日志模块

| 文件 | 作用 |
|:-----|:-----|
| `models.py` | UserBehaviorLog 模型（用户行为日志，支持登录/搜索/浏览/收藏等行为记录） |

**UserBehaviorLog 模型字段**：
- `user` - 关联用户（可为空，支持未登录用户）
- `behavior_type` - 行为类型（login/search/view/collect）
- `target` - 行为目标（如 recipe:123）
- `timestamp` - 行为时间
- `extra_data` - 额外数据（JSON格式）
- `ip_address` - IP地址
- `user_agent` - 用户代理

**类方法**：
- `UserBehaviorLog.log_behavior()` - 便捷方法，记录用户行为

---

### analytics - 数据分析模块

| 文件 | 作用 |
|:-----|:-----|
| `views.py` | 菜系分布分析视图（CuisineDistributionView）、难度等级统计视图（DifficultyStatsView）、口味偏好分析视图（FlavorPreferenceView）、食材使用频率统计视图（IngredientFrequencyView） |
| `urls.py` | `/api/analytics/cuisines/`、`/api/analytics/difficulty/`、`/api/analytics/flavors/`、`/api/analytics/ingredients/` |

**已实现接口**（4/4）：
- `GET /api/analytics/cuisines/` - 菜系分布分析
- `GET /api/analytics/difficulty/` - 难度等级统计
- `GET /api/analytics/flavors/` - 口味偏好分析
- `GET /api/analytics/ingredients/` - 食材使用频率统计

**菜系分布接口功能**：
- 统计各菜系的菜谱数量
- 计算占比百分比（保留两位小数）
- 按数量降序排列
- 排除空菜系
- 返回格式：`[{name, count, percentage}, ...]`

**难度等级接口功能**：
- 统计各难度等级（简单/中等/困难）的菜谱数量和占比
- 计算各难度等级的平均烹饪时长
- 按数量降序排列
- 返回格式：`[{name, value, count, percentage, avg_cooking_time}, ...]`

**口味偏好分析接口功能**：
- 统计各口味标签的菜谱数量
- 计算占比百分比
- 按数量降序排列
- 返回格式：`[{name, count, percentage}, ...]`

**食材使用频率统计接口功能**：
- 统计各食材被使用的菜谱数量
- 返回 Top 20 或指定数量食材
- 支持自定义返回数量（limit 参数，1-100，默认20）
- 按使用次数降序排列
- 返回格式：`[{id, name, count, category}, ...]`

**接口参数** (`/api/analytics/ingredients/`)：
- `limit` - 返回数量（可选，1-100，默认20）

**测试结果**：菜系分布 6/6 通过，难度统计 6/6 通过，口味偏好 6/6 通过，食材频率 6/6 通过

---

### utils - 公共工具模块

| 文件 | 作用 |
|:-----|:-----|
| `response.py` | 统一响应格式（ApiResponse） |
| `exceptions.py` | 自定义异常类（BusinessError, ValidationError, NotFoundError, PermissionDeniedError） |
| `exception_handler.py` | 全局异常处理器（统一 DRF 异常响应格式） |
| `pagination.py` | 分页工具类（StandardPagination） |
| `permissions.py` | 权限检查类（IsAdminUser, IsAdminUserOrReadOnly） |
| `constants.py` | 常量定义（UserRole, CategoryType, IngredientCategory, BehaviorType） |

**权限类说明**：
- `IsAdminUser` - 仅允许管理员访问，普通用户返回 403
- `IsAdminUserOrReadOnly` - 管理员可全部操作，普通用户仅读操作

**异常处理器**：
- `custom_exception_handler` - 将所有 DRF 异常转换为统一格式 `{"code": xxx, "message": "xxx", "data": null}`

---

## 测试脚本

### verify_script - API 测试脚本目录

| 文件 | 作用 |
|:-----|:-----|
| `test_hot_recipes.py` | 热门菜谱接口测试（默认排序、收藏量排序、自定义数量、边界值、无效参数） |
| `test_recipe_detail.py` | 菜谱详情接口测试 |
| `test_recipe_list.py` | 菜谱列表接口测试 |
| `test_recipe_search.py` | 菜谱搜索接口测试 |
| `test_simple_recipe_list.py` | 简单菜谱列表接口测试 |
| `test_category_list.py` | 分类列表接口测试 |
| `test_ingredient_list.py` | 食材列表接口测试（全量获取、分类筛选、关键词搜索、分页、无效参数、空结果、组合筛选） |
| `test_favorite.py` | 收藏功能接口测试（收藏/取消收藏/收藏列表/检查状态/重复收藏/未认证访问，12项测试全部通过） |
| `test_cuisine_distribution.py` | 菜系分布分析接口测试（数据获取、结构验证、数量总和、占比计算、排序验证、空值处理，6项测试全部通过） |
| `test_difficulty_stats.py` | 难度等级统计接口测试（数据获取、结构验证、数量总和、占比计算、排序验证、空值处理，6项测试全部通过） |
| `test_flavor_preference.py` | 口味偏好分析接口测试（数据获取、结构验证、数量验证、占比计算、排序验证、数据类型，6项测试全部通过） |
| `test_ingredient_frequency.py` | 食材使用频率分析接口测试（数据获取、结构验证、数量验证、排序验证、数据类型、limit参数，6项测试全部通过） |

**测试脚本运行方式**：
```bash
cd backend
python verify_script/test_hot_recipes.py
```

**辅助测试脚本**：
| 文件 | 作用 |
|:-----|:-----|
| `add_flavor_test_data.py` | 为菜谱添加口味标签测试数据 |

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
