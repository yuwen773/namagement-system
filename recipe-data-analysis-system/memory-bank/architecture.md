# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-31（阶段十五完成）
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
│   ├── verify_script/  # 测试脚本
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
- `GET /api/accounts/admin/users/` - 用户列表（仅管理员，支持搜索、角色筛选、分页）
- `PUT /api/accounts/admin/users/<id>/ban/` - 封禁用户（仅管理员，禁止封禁自己）
- `PUT /api/accounts/admin/users/<id>/unban/` - 解封用户（仅管理员）

---

### recipes - 菜谱模块

**接口**：
- `GET /api/recipes/` - 菜谱列表（分页、排序、筛选）
- `GET /api/recipes/search/` - 菜谱搜索
- `GET /api/recipes/<id>/` - 菜谱详情
- `GET /api/recipes/hot/` - 热门菜谱
- `POST /api/recipes/upload-image/` - 图片上传
- `GET /api/admin/recipes/` - 管理员菜谱列表（仅管理员）
- `POST /api/admin/recipes/create/` - 创建菜谱（仅管理员）
- `POST /api/admin/recipes/import/` - 批量导入菜谱（仅管理员，支持 CSV/JSON）
- `PUT/PATCH /api/admin/recipes/<id>/update/` - 更新菜谱（仅管理员）
- `DELETE /api/admin/recipes/<id>/delete/` - 删除菜谱（仅管理员，级联删除）

**参数**：
- 列表：`page`, `page_size`, `ordering`, `cuisine_type`, `difficulty`, `scene_type`, `target_audience`
- 搜索：`keyword`, `search_type` (name/ingredient), `page`, `page_size`
- 热门：`sort_by` (view_count/favorite_count), `limit`
- 管理员列表：`page`, `page_size`, `search`, `cuisine_type`, `difficulty`, `scene_type`, `target_audience`, `ordering`
- 创建/更新：所有菜谱字段均为可选（创建时 name 必填），支持食材关联 `ingredients: [{"ingredient_id": 1, "amount": "200g", "sort_order": 1}]`
- 批量导入：`file` (文件)、`file_type` (csv/json，可选，自动检测)
- 删除：无参数，通过路径中的 `<id>` 指定菜谱

**文件说明**：
- `models.py` - 菜谱模型（Recipe）、菜谱-食材关联模型（RecipeIngredient）
- `serializers.py` - 序列化器（RecipeListSerializer、RecipeDetailSerializer、RecipeCreateSerializer、RecipeUpdateSerializer、RecipeImageUploadSerializer）
- `views.py` - 菜谱相关视图函数（包含管理员专用视图：admin_recipe_list、admin_create_recipe、admin_update_recipe、admin_delete_recipe、admin_import_recipes）
- `urls.py` - 普通用户路由配置
- `admin_urls.py` - 管理员专用路由配置（管理员菜谱管理接口）
- `frontend/src/views/RecipeManagement.vue` - 管理员菜谱管理页面（列表、新增、编辑、删除、批量导入）

**批量导入架构设计**：
- 支持格式：JSON 数组、CSV 文件
- 编码支持：UTF-8（默认）、GBK（中文 Excel）
- 数据验证：复用 RecipeCreateSerializer 进行字段验证
- 事务处理：每条记录独立事务，失败不影响其他记录
- 错误处理：收集所有失败记录，返回详细错误信息（行号、菜谱名称、错误原因）
- 食材关联：支持 JSON 格式的食材数组，CSV 中需为 JSON 字符串格式

---

### categories - 分类模块

**接口**：
- `GET /api/categories/` - 分类列表（支持 type 参数筛选）
- `GET /api/categories/<type>/` - 按类型获取分类
- `GET /api/admin/categories/` - 管理员分类列表（支持类型筛选、搜索、分页）
- `POST /api/admin/categories/create/` - 创建分类（仅管理员）
- `PUT/PATCH /api/admin/categories/<id>/update/` - 更新分类（仅管理员）
- `DELETE /api/admin/categories/<id>/delete/` - 删除分类（仅管理员，包含使用检查）

**分类类型**：cuisine（菜系）、scene（场景）、crowd（人群）、taste（口味）、difficulty（难度）

**文件说明**：
- `models.py` - 分类模型（Category）
- `serializers.py` - 序列化器（CategorySerializer、CategoryListSerializer、CategoryCreateSerializer、CategoryUpdateSerializer）
- `views.py` - 分类视图（包含管理员专用视图：admin_category_list、admin_create_category、admin_update_category、admin_delete_category）
- `urls.py` - 普通用户路由配置
- `admin_urls.py` - 管理员专用路由配置
- `frontend/src/api/categories.js` - 分类管理 API 模块
- `frontend/src/views/CategoryManagement.vue` - 分类管理页面（管理员专用，分类CRUD、类型筛选、搜索、分页）

---

### ingredients - 食材模块

**接口**：
- `GET /api/ingredients/` - 食材列表（支持分类筛选、关键词搜索）
- `GET /api/admin/ingredients/` - 管理员食材列表（支持分类筛选、搜索、分页，仅管理员）
- `POST /api/admin/ingredients/create/` - 创建食材（仅管理员）
- `PUT/PATCH /api/admin/ingredients/<id>/update/` - 更新食材（仅管理员）
- `DELETE /api/admin/ingredients/<id>/delete/` - 删除食材（仅管理员，包含使用检查）

**参数**：
- 列表：`category`, `search`, `page`, `page_size`
- 创建/更新：`name` (食材名称), `category` (食材分类)

**食材分类**：vegetable（蔬菜）、meat（肉类）、seafood（海鲜）、seasoning（调料）、fruit（水果）、grain（谷物）、dairy（乳制品）、other（其他）

**文件说明**：
- `models.py` - 食材模型（Ingredient）
- `serializers.py` - 序列化器（IngredientSerializer、IngredientListSerializer、IngredientCreateSerializer、IngredientUpdateSerializer）
- `views.py` - 食材视图（包含管理员专用视图：admin_ingredient_list、admin_create_ingredient、admin_update_ingredient、admin_delete_ingredient）
- `urls.py` - 普通用户路由配置
- `admin_urls.py` - 管理员专用路由配置
- `frontend/src/api/ingredients.js` - 食材管理 API 模块
- `frontend/src/views/IngredientManagement.vue` - 管理员食材管理页面（列表、新增、编辑、删除）

---

### favorites - 收藏模块

**接口**：
- `POST /api/favorites/` - 收藏菜谱
- `GET /api/favorites/` - 获取收藏列表
- `DELETE /api/favorites/<recipe_id>/` - 取消收藏
- `GET /api/favorites/check/<recipe_id>/` - 检查收藏状态

---

### analytics - 数据分析模块

**普通用户接口**：
- `GET /api/analytics/cuisines/` - 菜系分布分析
- `GET /api/analytics/difficulty/` - 难度等级统计
- `GET /api/analytics/flavors/` - 口味偏好分析
- `GET /api/analytics/ingredients/` - 食材使用频率

**管理员专用接口**：
- `GET /api/admin/analytics/cuisines/` - 菜系深度分析（仅管理员）
- `GET /api/admin/analytics/difficulty/` - 难度深度分析（仅管理员）
- `GET /api/admin/analytics/hot/` - 热门菜谱分析（仅管理员）
- `GET /api/admin/analytics/ingredient-pairs/` - 食材关联分析（仅管理员）

**文件说明**：
- `models.py` - 数据分析模型（当前无独立模型，使用 Recipe 模型）
- `views.py` - 数据分析视图（包含普通用户视图和管理员专用视图：AdminCuisineAnalysisView、AdminDifficultyAnalysisView、AdminHotRecipeAnalysisView）
- `urls.py` - 普通用户路由配置
- `admin_urls.py` - 管理员专用路由配置
- `verify_script/test_admin_analytics.py` - 菜系深度分析测试脚本
- `verify_script/test_admin_difficulty_analysis.py` - 难度深度分析测试脚本
- `verify_script/test_admin_hot_recipe_analysis.py` - 热门菜谱分析测试脚本
- `verify_script/test_admin_ingredient_pairs_analysis.py` - 食材关联分析测试脚本

**管理员菜系深度分析数据结构**：
```json
{
    "summary": {
        "total_recipes": 20004,      // 总菜谱数
        "total_cuisines": 13          // 菜系类型数量
    },
    "cuisines": [
        {
            "name": "川菜",              // 菜系名称
            "count": 1754,              // 菜谱数量
            "percentage": 8.77,         // 占比百分比
            "avg_view_count": 25005.67, // 平均点击量
            "avg_favorite_count": 3101.5,// 平均收藏量
            "avg_cooking_time": 30.0,   // 平均烹饪时长（分钟）
            "difficulty_distribution": { // 难度分布
                "easy": 584,
                "medium": 849,
                "hard": 321
            }
        }
    ]
}
```

**管理员难度深度分析数据结构**：
```json
{
    "summary": {
        "total_recipes": 20004,           // 总菜谱数
        "total_difficulty_levels": 3       // 难度等级数量
    },
    "difficulties": [
        {
            "name": "简单",                  // 难度中文名
            "value": "easy",                // 难度值
            "count": 6783,                  // 菜谱数量
            "percentage": 33.91,            // 占比百分比
            "avg_cooking_time": 30.0,       // 平均烹饪时长（分钟）
            "avg_view_count": 24909.29,     // 平均点击量
            "avg_favorite_count": 3078.51   // 平均收藏量
        }
    ]
}
```

**管理员热门菜谱分析数据结构**：
```json
{
    "summary": {
        "total_recipes": 20004,      // 总菜谱数
        "sort_by": "view_count",     // 排序字段（view_count/favorite_count）
        "sort_by_label": "点击量",    // 排序方式中文名
        "limit": 50                  // 返回数量
    },
    "trends": {
        "avg_view_count": 24972.39,       // 全平台平均点击量
        "avg_favorite_count": 3108.69,    // 全平台平均收藏量
        "avg_conversion_rate": 12.45      // 全平台平均转化率（%）
    },
    "recipes": [
        {
            "id": 59198,                   // 菜谱ID
            "name": "米奇纸杯蛋糕mini可爱版", // 菜谱名称
            "cuisine_type": "面食",        // 菜系
            "difficulty": "easy",          // 难度
            "view_count": 50002,           // 点击量
            "favorite_count": 7457,        // 收藏量
            "conversion_rate": 14.91       // 转化率（%）
        }
    ]
}
```

**管理员食材关联分析数据结构**：
```json
{
    "summary": {
        "total_recipes": 20004,       // 总菜谱数
        "total_pairs": 49914,         // 食材配对总数
        "min_count": 10,              // 最小共现次数
        "limit": 50,                  // 返回数量
        "category_filter": "全部"     // 分类筛选
    },
    "pairs": [
        {
            "ingredient_1": {              // 食材1
                "id": 1,                   // 食材ID
                "name": "适量盐",          // 食材名称
                "category": "seasoning"    // 食材分类
            },
            "ingredient_2": {              // 食材2
                "id": 2,
                "name": "适量生抽",
                "category": "seasoning"
            },
            "count": 250,                  // 共现次数
            "percentage": 1.25            // 占比百分比
        }
    ]
}
```

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
- `/analytics` - 数据概览（数据分析）
- `/ingredients-frequency` - 食材频率分析
- `/login` - 登录
- `/register` - 注册
- `/profile` - 个人信息（需认证）
- `/change-password` - 修改密码（需认证）
- `/admin` - 用户管理（需管理员权限）
- `/admin/recipes` - 菜谱管理（需管理员权限）
- `/admin/categories` - 分类管理（需管理员权限）
- `/admin/ingredients` - 食材管理（需管理员权限）
- `/admin/analytics` - 数据分析（需管理员权限）

### stores - Pinia 状态管理

**user store**：`token`, `userInfo`, `isLoggedIn`, `isAdmin`, `setToken()`, `setUserInfo()`, `logout()`

### api - API 请求模块

| 文件 | 作用 |
|:-----|:-----|
| `auth.js` | 用户认证 API + 用户管理 API（管理员） + axios 实例配置 |
| `recipes.js` | 菜谱、分类、食材、收藏 API |
| `categories.js` | 分类管理 API（管理员） |
| `ingredients.js` | 食材管理 API（管理员） |
| `analytics.js` | 数据分析 API（菜系/难度/口味/食材统计 + 管理员深度分析） |

### views - 页面组件

| 文件 | 作用 |
|:-----|:-----|
| `Home.vue` | 首页 |
| `RecipeList.vue` | 菜谱列表页（搜索、筛选、分页） |
| `RecipeDetail.vue` | 菜谱详情页（收藏、分享） |
| `RecipeCategory.vue` | 分类浏览页 |
| `RecipeHot.vue` | 热门菜谱页 |
| `RecipeAnalytics.vue` | 数据概览页（4个 ECharts 图表：菜系饼图、难度柱状图、口味雷达图、高频食材条形图） |
| `IngredientFrequency.vue` | 食材频率页（9种分类筛选、Top20/50/100切换、搜索、统计卡片、排行榜、ECharts图表） |
| `Login.vue` | 登录页 |
| `Register.vue` | 注册页 |
| `Profile.vue` | 个人信息页 |
| `ChangePassword.vue` | 修改密码页 |
| `UserManagement.vue` | 用户管理页（管理员专用，用户列表、搜索、角色筛选、封禁/解封、分页） |
| `RecipeManagement.vue` | 菜谱管理页（管理员专用，菜谱CRUD、批量导入CSV/JSON、搜索筛选、分页） |
| `CategoryManagement.vue` | 分类管理页（管理员专用，分类CRUD、类型筛选、排序） |
| `IngredientManagement.vue` | 食材管理页（管理员专用，食材CRUD、分类筛选、搜索） |
| `AdminAnalytics.vue` | 管理员数据分析页（管理员专用，4个分析维度：菜系/难度/热门/食材关联，图表+表格，数据导出） |

### components - 公共组件

| 文件 | 作用 |
|:-----|:-----|
| `AppNavbar.vue` | 顶部导航栏（含搜索、用户菜单、移动端菜单） |
| `HelloWorld.vue` | 示例组件 |

### 数据可视化组件

**ECharts 图表配置**（RecipeAnalytics.vue）：
- **菜系分布饼图**：环形饼图，展示各菜系占比
- **难度统计柱状图**：垂直柱状图，展示 easy/medium/hard 分布
- **口味偏好雷达图**：雷达图，展示 Top 6 口味标签
- **高频食材条形图**：水平条形图，展示 Top 15 食材

**配色方案**：
- 主色：`#c2622e`（琥珀橙）
- 辅色：`#d4773a`（浅琥珀）、`#a35220`（深琥珀）
- 图表色板：温暖色调（amber, orange, gold, coral）

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
