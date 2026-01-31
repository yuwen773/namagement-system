# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-31（阶段九第3步完成，菜谱分类页面实现）

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
│   │   ├── views/      # 页面组件
│   │   ├── App.vue     # 根组件
│   │   └── main.js     # 入口文件
│   ├── index.html      # HTML 模板
│   ├── package.json    # 依赖配置
│   └── vite.config.js  # Vite 配置
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

## 前端模块说明

### api - API 请求模块

| 文件 | 作用 |
|:-----|:-----|
| `auth.js` | 封装用户认证相关 API（登录、注册、获取用户信息、更新资料、修改密码、角色检查） |
| `recipes.js` | 封装菜谱相关 API（列表、搜索、详情、热门菜谱、分类、食材） |

**auth.js 已实现接口**（6/6）：
- `login(username, password)` - 用户登录
- `register(data)` - 用户注册
- `getCurrentUser()` - 获取当前用户信息
- `updateProfile(data)` - 更新用户资料
- `changePassword(data)` - 修改密码
- `checkRole()` - 角色检查

**recipes.js 已实现接口**（11/11）：
- `getRecipeList(params)` - 获取菜谱列表（支持分页、排序、筛选）
- `searchRecipes(params)` - 搜索菜谱（支持按名称/食材搜索）
- `getRecipeDetail(id)` - 获取菜谱详情
- `getHotRecipes(params)` - 获取热门菜谱
- `getCategories(params)` - 获取分类列表（支持按类型筛选）
- `getCategoriesByType(type)` - 按类型路径获取分类
- `getIngredients(params)` - 获取食材列表（支持分类筛选、关键词搜索）
- `addFavorite(recipeId)` - 收藏菜谱
- `removeFavorite(recipeId)` - 取消收藏
- `checkFavoriteStatus(recipeId)` - 检查收藏状态
- `getFavoriteList(params)` - 获取收藏列表

**axios 配置**：
- 基础 URL：`http://localhost:8000`
- 请求超时：10 秒
- 请求拦截器：自动添加 Authorization 头
- 响应拦截器：统一处理响应格式和错误

---

### router - 路由模块

| 文件 | 作用 |
|:-----|:-----|
| `index.js` | 路由配置、路由守卫 |

**已配置路由**（9/18）：
- `/` - 首页 (Home.vue)
- `/recipes` - 菜谱列表页 (RecipeList.vue)
- `/recipes/:id` - 菜谱详情页 (RecipeDetail.vue)
- `/category/:type?/:value?` - 菜谱分类页 (RecipeCategory.vue，type/value 可选)
- `/hot` - 热门菜谱页 (RecipeHot.vue)
- `/login` - 登录页 (Login.vue)
- `/register` - 注册页 (Register.vue)
- `/profile` - 个人信息页 (Profile.vue，需认证)
- `/change-password` - 修改密码页 (ChangePassword.vue，需认证)

**路由守卫**：
- 检查 `meta.requiresAuth` 是否需要认证
- 未认证用户跳转到登录页，携带 redirect 参数

---

### stores - Pinia 状态管理

| 文件 | 作用 |
|:-----|:-----|
| `user.js` | 用户状态管理 |

**user store 状态**：
- `token` - JWT Token
- `userInfo` - 用户信息对象

**user store getters**：
- `isLoggedIn` - 是否已登录
- `isAdmin` - 是否是管理员

**user store actions**：
- `setToken(token)` - 设置 Token
- `setUserInfo(userInfo)` - 设置用户信息
- `logout()` - 退出登录

**数据持久化**：
- Token 和 userInfo 同步存储到 localStorage

---

### views - 页面组件

| 文件 | 作用 |
|:-----|:-----|
| `Home.vue` | 首页 |
| `RecipeList.vue` | 菜谱列表页（菜谱展示、搜索、筛选、分类入口） |
| `RecipeDetail.vue` | 菜谱详情页（详细信息、食材、步骤、收藏） |
| `RecipeCategory.vue` | 菜谱分类页（分类浏览、筛选、排序） |
| `RecipeHot.vue` | 热门菜谱页（排行榜样式、Top 50展示） |
| `Login.vue` | 登录页（美食主题设计） |
| `Register.vue` | 注册页（美食主题设计） |
| `Profile.vue` | 个人信息页（用户信息展示与编辑） |
| `ChangePassword.vue` | 修改密码页（密码修改与强度指示） |

**Login.vue 组件**：
- **设计风格**：美食主题，温暖琥珀橙配色
- **布局**：双栏设计（左侧品牌展示 + 右侧登录表单）
- **字体**：Playfair Display（标题）+ DM Sans（正文）
- **功能**：用户名/密码登录、记住我、表单验证、错误提示
- **响应式**：移动端隐藏左侧装饰区

**Register.vue 组件**：
- **设计风格**：与登录页一致的美食主题
- **布局**：双栏设计（左侧功能展示 + 右侧注册表单）
- **功能**：用户名/邮箱/密码注册、密码强度指示器、表单验证
- **验证规则**：用户名3-20字符（字母数字下划线）、密码至少8位、两次密码匹配
- **密码强度**：基于长度、大小写、数字、特殊字符计算（弱/中/强）
- **交互**：注册成功后跳转到登录页并携带用户名

**Profile.vue 组件**：
- **设计风格**：与登录页一致的美食主题
- **布局**：顶部导航 + 主内容卡片
- **功能**：
  - 显示用户信息（用户名、邮箱、昵称、手机号、个人简介、注册时间、账号状态）
  - 头像区域带角色徽章（管理员/用户）
  - 编辑对话框（昵称、邮箱、手机号、个人简介）
  - 表单验证（邮箱格式、手机号格式、字符限制）
  - 保存后同步更新 Pinia store
  - "修改密码"按钮跳转到修改密码页面
- **响应式**：支持桌面端和移动端
- **路由守卫**：需认证才能访问

**ChangePassword.vue 组件**：
- **设计风格**：与个人信息页一致的美食主题
- **布局**：顶部导航 + 主内容卡片（居中单栏）
- **功能**：
  - 旧密码输入框（带图标）
  - 新密码输入框（带图标）
  - 确认新密码输入框（带图标）
  - 密码强度实时指示器（弱/中/强）
  - 表单验证：
    - 旧密码必填
    - 新密码至少 8 位
    - 新密码不能与旧密码相同
    - 确认密码必须与新密码一致
  - 修改成功后自动清除登录状态
  - 延迟跳转到登录页
- **密码强度计算**：基于长度（8/12位）、大小写字母、数字、特殊字符
- **响应式**：支持桌面端和移动端
- **路由守卫**：需认证才能访问

**RecipeList.vue 组件**：
- **设计风格**：与登录页一致的美食主题
- **布局**：顶部搜索栏 + 侧边栏筛选区 + 主内容区（菜谱卡片网格）
- **功能**：
  - 搜索框：支持按菜谱名称搜索（Enter 键触发）
  - 筛选条件：
    - 菜系筛选（从分类 API 动态加载）
    - 难度筛选（简单/中等/困难）
    - 排序选项（最新发布、点击量、收藏量）
  - 分页组件：支持 12/24/48 每页，带总数显示
  - 菜谱卡片：
    - 图片展示（带悬停放大效果）
    - 难度徽章（简单/中等/困难，不同颜色）
    - 菜谱名称（最多显示 2 行）
    - 菜系标签
    - 烹饪时长（带图标）
    - 统计信息（点击量、收藏量，带格式化）
  - 点击卡片跳转到详情页
  - 空状态处理（显示重置筛选按钮）
  - 侧边栏底部"浏览分类"入口链接（跳转到分类页面）
- **响应式**：
  - 桌面端（>1200px）：侧边栏 + 3 列网格
  - 平板端（768-1200px）：侧边栏 + 2 列网格
  - 移动端（<768px）：单列网格，侧边栏移至顶部
- **动画效果**：
  - 卡片悬停上浮 + 阴影加深
  - 图片悬停放大
  - 卡片淡入动画

**RecipeDetail.vue 组件**：
- **设计风格**：与菜谱列表页一致的美食主题
- **布局**：返回导航 + 顶部大图区 + 主内容区（左主右副）
- **功能**：
  - 返回导航栏（返回菜谱列表按钮）
  - 顶部大图展示区（400px 高度，带难度徽章）
  - 标题区（菜谱名称、菜系标签、烹饪时长）
  - 统计栏（浏览量、收藏量，带图标）
  - 食材清单：
    - 网格布局（200px 最小宽度）
    - 显示食材名称和用量
    - 空状态处理
  - 制作步骤：
    - 支持文本格式（直接显示）
    - 支持数组格式（带序号的步骤列表）
    - 空状态处理
  - 口味标签区（如果有口味数据）
  - 侧边栏操作区：
    - 收藏按钮（大尺寸，状态切换）
    - 分享按钮（原生分享或复制链接）
    - 收藏提示（显示收藏人数）
  - 收藏功能：
    - 登录用户可收藏/取消收藏
    - 未登录用户点击收藏提示登录并跳转
    - 收藏后按钮状态同步更新
    - 收藏数量实时更新
  - 加载状态（骨架屏）
  - 404 错误处理（显示友好提示页）
- **响应式**：
  - 桌面端（>968px）：双栏布局（主内容 + 侧边栏）
  - 平板/移动端（≤968px）：单栏布局，侧边栏移至底部
  - 移动端（<640px）：大图高度减小至 220px
- **路由**：`/recipes/:id`（从路由参数获取菜谱 ID）
- **API 调用**：
  - `getRecipeDetail(id)` - 获取菜谱详情
  - `checkFavoriteStatus(id)` - 检查收藏状态（仅登录用户）
  - `addFavorite(id)` / `removeFavorite(id)` - 收藏操作

**RecipeCategory.vue 组件**：
- **设计风格**：与菜谱列表页一致的美食主题
- **布局**：顶部标题区 + 分类标签切换区 + 筛选区 + 菜谱网格
- **功能**：
  - 返回导航栏（返回菜谱列表按钮）
  - 动态标题栏（显示当前分类名称和菜谱数量）
  - 分类类型切换标签：
    - 菜系分类（cuisine）
    - 场景分类（scene）
    - 人群分类（crowd）
  - 分类标签列表：
    - 点击选择分类
    - 再次点击取消选择
    - 选中状态有高亮样式
  - 筛选条件区：
    - 难度筛选（全部/简单/中等/困难）
    - 排序方式（7种：最新、点击量、收藏量、烹饪时长）
  - 菜谱卡片网格（与列表页一致的样式）
  - 分页功能（支持12/24/48每页）
  - 空状态处理
- **动态路由**：
  - `/category` - 分类浏览首页
  - `/category/:type` - 指定分类类型
  - `/category/:type/:value` - 指定分类的具体值（如川菜）
- **路由参数映射**：
  - `cuisine` → `cuisine_type`（菜系）
  - `scene` → `scene_type`（场景）
  - `crowd` → `target_audience`（人群）
- **响应式**：
  - 桌面端：完整布局
  - 平板端：筛选区变为垂直布局
  - 移动端：单列网格
- **API 调用**：
  - `getCategories({ type })` - 获取分类列表
  - `getRecipeList(params)` - 获取菜谱列表（带分类筛选）

**RecipeHot.vue 组件功能**：
- 顶部标题区（带脉冲动画火焰图标装饰）
- 排序方式切换（按点击量/按收藏量）
- 返回按钮（返回上一页）
- 排行榜样式菜谱卡片（Top 50展示）：
  - 前三名金银铜牌徽章（带特殊边框和阴影）
  - 4-10名排名数字徽章
  - 点击量/收藏量高亮显示
- 排序说明提示（显示当前排序方式和展示数量）
- 菜谱卡片网格（与列表页一致的交互样式）
- 空状态处理
- 响应式设计（移动端布局优化）
- **路由**：`/hot`
- **API 调用**：
  - `getHotRecipes(params)` - 获取热门菜谱列表

**主题配色**：
| 颜色名 | 值 | 用途 |
|:-------|:-----|:-----|
| 琥珀橙主色 | #d4773a | 渐变背景、按钮 |
| 琥珀橙深色 | #c2622e | 按钮渐变、强调色 |
| 琥珀橙暗色 | #a35220 | 边框、阴影 |
| 巧克力棕 | #3d2914 | 标题、文字 |
| 奶油白 | #faf8f5 | 页面背景 |

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
