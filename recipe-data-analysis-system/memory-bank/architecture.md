# 菜谱数据分析系统 - 架构设计文档

> 本文档描述系统的整体架构、数据库设计和技术选型
> 更新日期: 2026-01-29

---

## 目录

1. [系统架构概览](#系统架构概览)
2. [技术栈](#技术栈)
3. [数据库设计](#数据库设计)
4. [后端架构](#后端架构)
5. [前端架构](#前端架构)
6. [部署架构](#部署架构)

---

## 系统架构概览

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                          前端层 (Vue 3)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  普通用户界面  │  │  管理员界面   │  │   数据可视化 (ECharts) │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTP/JSON (REST API)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API 网关层 (Django)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  认证中间件    │  │  权限中间件    │  │   统一响应/异常处理    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      业务逻辑层 (Django Apps)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │ accounts │ │ recipes  │ │analytics │ │   admin_panel    │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                       │
│  │categories│ │ingredients│ │favorites │  behavior_logs      │   │
│  └──────────┘ └──────────┘ └──────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ ORM
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       数据层 (MySQL 8.0+)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           recipe_analysis_db (数据库)                     │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐    │  │
│  │  │ users   │ │ recipes │ │categories│ │ ingredients │    │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────┘    │  │
│  │  ┌─────────┐ ┌─────────────────────────────────────┐    │  │
│  │  │favorites│ │     user_behavior_logs              │    │  │
│  │  └─────────┘ └─────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据处理层 (Python)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Pandas     │  │    NumPy     │  │   数据分析脚本         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 数据流

```
用户 → 前端界面 → API 调用 → Django 视图 → 业务逻辑 → 数据库
                ↑                                         ↓
                └──────────── JSON 响应 ←─────────────────┘
```

---

## 技术栈

### 前端技术栈

| 类别 | 技术选型 | 版本 | 说明 |
|:---|:---------|:-----|:-----|
| 框架 | Vue 3 | 3.x | 使用 Composition API |
| 构建工具 | Vite | 5.x | 快速的开发服务器 |
| UI 组件库 | Element Plus | latest | 桌面端组件库 |
| CSS 框架 | Tailwind CSS | 3.x | 原子化 CSS |
| 图表库 | ECharts | 5.x | 数据可视化 |
| 状态管理 | Pinia | 2.x | 官方状态管理 |
| 路由 | Vue Router | 4.x | 官方路由 |
| HTTP 客户端 | Axios | 1.x | HTTP 请求 |

### 后端技术栈

| 类别 | 技术选型 | 版本 | 说明 |
|:---|:---------|:-----|:-----|
| 框架 | Django | 5.2 | Python Web 框架 |
| API 框架 | Django REST Framework | 3.x | RESTful API |
| 数据库 | MySQL | 8.0+ | 关系型数据库 |
| 认证 | JWT | - | JSON Web Token |
| 数据处理 | Pandas | 2.x | 数据分析 |
| 数据处理 | NumPy | 1.x | 科学计算 |
| CORS | django-cors-headers | - | 跨域支持 |

### 开发工具

| 类别 | 工具 | 说明 |
|:---|:-----|:-----|
| 前端脚手架 | create-vite | Vue 3 项目脚手架 |
| 后端脚手架 | django-admin | Django 项目脚手架 |
| 包管理 | npm/pnpm | 前端包管理 |
| 包管理 | pip | Python 包管理 |
| 虚拟环境 | venv | Python 虚拟环境 |

---

## 数据库设计

### 数据库概览

**数据库名称**: `recipe_analysis_db`
**字符集**: `utf8mb4`
**排序规则**: `utf8mb4_unicode_ci`

### 数据表清单

| 表名 | 说明 | 记录数预估 |
|:-----|:-----|:----------:|
| users | 用户表 | 100+ |
| user_profiles | 用户资料表 | 100+ |
| categories | 分类表（菜系、场景、人群） | 50+ |
| ingredients | 食材表 | 500+ |
| recipes | 菜谱主表 | 10,000 - 20,000 |
| recipe_ingredients | 菜谱-食材关联表 | 50,000+ |
| recipe_steps | 菜谱步骤表 | 30,000+ |
| user_favorites | 用户收藏表 | 5,000+ |
| user_behavior_logs | 用户行为日志表 | 10,000+ |

---

### 表结构详解

#### 1. users - 用户表

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名（唯一）',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密）',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    role ENUM('user', 'admin') DEFAULT 'user' COMMENT '角色',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_banned BOOLEAN DEFAULT FALSE COMMENT '是否被封禁',
    last_login DATETIME COMMENT '最后登录时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

#### 2. user_profiles - 用户资料表

```sql
CREATE TABLE user_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '资料ID',
    user_id INT UNIQUE NOT NULL COMMENT '用户ID（外键）',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar VARCHAR(255) COMMENT '头像URL',
    bio TEXT COMMENT '个人简介',
    gender ENUM('male', 'female', 'other') COMMENT '性别',
    birth_date DATE COMMENT '出生日期',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户资料表';
```

#### 3. categories - 分类表

```sql
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '分类ID',
    name VARCHAR(50) NOT NULL COMMENT '分类名称',
    type ENUM('cuisine', 'scene', 'crowd', 'difficulty', 'taste') NOT NULL COMMENT '分类类型',
    parent_id INT DEFAULT NULL COMMENT '父分类ID（支持层级）',
    level INT DEFAULT 1 COMMENT '层级（1=一级）',
    sort_order INT DEFAULT 0 COMMENT '排序序号',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_type (type),
    INDEX idx_parent_id (parent_id),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分类表';

-- 初始数据：八大菜系
INSERT INTO categories (name, type, sort_order) VALUES
('川菜', 'cuisine', 1),
('粤菜', 'cuisine', 2),
('鲁菜', 'cuisine', 3),
('苏菜', 'cuisine', 4),
('浙菜', 'cuisine', 5),
('闽菜', 'cuisine', 6),
('湘菜', 'cuisine', 7),
('徽菜', 'cuisine', 8);

-- 初始数据：场景分类
INSERT INTO categories (name, type, sort_order) VALUES
('早餐', 'scene', 1),
('午餐', 'scene', 2),
('晚餐', 'scene', 3),
('夜宵', 'scene', 4),
('下午茶', 'scene', 5);

-- 初始数据：难度等级
INSERT INTO categories (name, type, sort_order) VALUES
('简单', 'difficulty', 1),
('中等', 'difficulty', 2),
('困难', 'difficulty', 3);

-- 初始数据：口味标签
INSERT INTO categories (name, type, sort_order) VALUES
('酸甜', 'taste', 1),
('咸鲜', 'taste', 2),
('麻辣', 'taste', 3),
('清淡', 'taste', 4),
('香辣', 'taste', 5);
```

#### 4. ingredients - 食材表

```sql
CREATE TABLE ingredients (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '食材ID',
    name VARCHAR(100) UNIQUE NOT NULL COMMENT '食材名称',
    category ENUM('vegetable', 'meat', 'seafood', 'seasoning', 'fruit', 'grain', 'dairy', 'other') DEFAULT 'other' COMMENT '食材分类',
    unit VARCHAR(20) COMMENT '常用单位（克、毫升、个等）',
    description TEXT COMMENT '描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    INDEX idx_name (name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='食材表';
```

#### 5. recipes - 菜谱主表

```sql
CREATE TABLE recipes (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '菜谱ID',
    name VARCHAR(200) NOT NULL COMMENT '菜谱名称',
    cover_image VARCHAR(500) NOT NULL COMMENT '封面图片URL',
    description TEXT COMMENT '简介',
    cuisine_id INT COMMENT '菜系分类ID',
    difficulty_id INT COMMENT '难度分类ID',
    taste_ids JSON COMMENT '口味标签ID列表（JSON数组）',
    scene_id INT COMMENT '场景分类ID',
    cooking_time INT COMMENT '烹饪时长（分钟）',
    servings INT DEFAULT 2 COMMENT '份量（人份）',
    steps TEXT COMMENT '制作步骤（JSON格式）',
    tips TEXT COMMENT '小贴士',
    view_count INT DEFAULT 0 COMMENT '浏览量',
    collect_count INT DEFAULT 0 COMMENT '收藏量',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    FOREIGN KEY (cuisine_id) REFERENCES categories(id),
    FOREIGN KEY (difficulty_id) REFERENCES categories(id),
    FOREIGN KEY (scene_id) REFERENCES categories(id),

    INDEX idx_name (name),
    INDEX idx_cuisine (cuisine_id),
    INDEX idx_difficulty (difficulty_id),
    INDEX idx_scene (scene_id),
    INDEX idx_view_count (view_count),
    INDEX idx_collect_count (collect_count),
    INDEX idx_created_at (created_at),
    FULLTEXT INDEX ft_search (name, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='菜谱主表';
```

#### 6. recipe_ingredients - 菜谱食材关联表

```sql
CREATE TABLE recipe_ingredients (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '关联ID',
    recipe_id INT NOT NULL COMMENT '菜谱ID',
    ingredient_id INT NOT NULL COMMENT '食材ID',
    amount VARCHAR(100) COMMENT '用量描述（如：100克、2个）',
    sort_order INT DEFAULT 0 COMMENT '排序序号',

    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
    UNIQUE KEY uk_recipe_ingredient (recipe_id, ingredient_id),
    INDEX idx_recipe_id (recipe_id),
    INDEX idx_ingredient_id (ingredient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='菜谱食材关联表';
```

#### 7. recipe_steps - 菜谱步骤表

```sql
CREATE TABLE recipe_steps (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '步骤ID',
    recipe_id INT NOT NULL COMMENT '菜谱ID',
    step_number INT NOT NULL COMMENT '步骤序号',
    description TEXT NOT NULL COMMENT '步骤描述',
    image_url VARCHAR(500) COMMENT '步骤图片URL',

    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY uk_recipe_step (recipe_id, step_number),
    INDEX idx_recipe_id (recipe_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='菜谱步骤表';
```

#### 8. user_favorites - 用户收藏表

```sql
CREATE TABLE user_favorites (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '收藏ID',
    user_id INT NOT NULL COMMENT '用户ID',
    recipe_id INT NOT NULL COMMENT '菜谱ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_recipe (user_id, recipe_id),
    INDEX idx_user_id (user_id),
    INDEX idx_recipe_id (recipe_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收藏表';
```

#### 9. user_behavior_logs - 用户行为日志表

```sql
CREATE TABLE user_behavior_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    user_id INT COMMENT '用户ID（可为空，支持未登录用户）',
    behavior_type ENUM('login', 'search', 'view', 'collect', 'uncollect', 'share') NOT NULL COMMENT '行为类型',
    target_type VARCHAR(50) COMMENT '目标类型（recipe、category等）',
    target_id INT COMMENT '目标ID',
    extra_data JSON COMMENT '额外数据（搜索关键词、停留时长等）',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '行为时间',

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_behavior_type (behavior_type),
    INDEX idx_target (target_type, target_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户行为日志表';
```

---

### 数据库关系图 (ER图)

```
┌─────────────┐         ┌─────────────────┐
│   users     │────1:1─▶│ user_profiles   │
└─────────────┘         └─────────────────┘
      │
      │ 1:N
      ▼
┌─────────────────┐         ┌─────────────┐
│ user_favorites  │────────▶│   recipes   │
└─────────────────┘         └─────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
            │ recipe_...  │ │ recipe_...  │ │  categories  │
            │ ingredients │ │   steps     │ └──────────────┘
            └─────────────┘ └─────────────┘
                    │
                    ▼
            ┌─────────────┐
            │ ingredients │
            └─────────────┘

┌─────────────┐
│user_...logs │
└─────────────┘
```

---

## 后端架构

### 项目结构

```
backend/
├── config/                    # Django 项目配置
│   ├── __init__.py
│   ├── settings.py           # 项目设置
│   ├── urls.py               # 主路由
│   └── wsgi.py
│
├── utils/                     # 公共工具模块
│   ├── __init__.py
│   ├── response.py           # 统一响应封装
│   ├── exceptions.py         # 自定义异常
│   ├── pagination.py         # 分页配置
│   └── constants.py          # 常量定义
│
├── accounts/                  # 用户认证模块
│   ├── models.py             # User, UserProfile
│   ├── serializers.py        # 注册、登录、用户信息序列化器
│   ├── views.py              # 认证视图集
│   ├── urls.py               # 认证路由
│   └── permissions.py        # 权限类
│
├── recipes/                   # 菜谱模块
│   ├── models.py             # Recipe, RecipeStep
│   ├── serializers.py        # 菜谱序列化器
│   ├── views.py              # 菜谱视图集
│   └── urls.py
│
├── categories/                # 分类模块
│   ├── models.py             # Category
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── ingredients/               # 食材模块
│   ├── models.py             # Ingredient
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── favorites/                 # 收藏模块
│   ├── models.py             # UserFavorite
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── analytics/                 # 数据分析模块（普通用户）
│   ├── views.py              # 菜系、难度、口味、食材统计
│   ├── urls.py
│   └── services.py           # 数据分析服务
│
├── admin_panel/               # 管理员模块
│   ├── users/                # 用户管理
│   ├── recipes/              # 菜谱管理
│   ├── analytics/            # 深度数据分析
│   └── dashboard/            # 数据大盘
│
├── behavior_logs/             # 行为日志模块
│   ├── models.py             # UserBehaviorLog
│   └── services.py           # 行为记录服务
│
├── manage.py
└── requirements.txt
```

### API 路由设计

```
/api/
├── accounts/                  # 认证相关
│   ├── POST /register        # 注册
│   ├── POST /login           # 登录
│   ├── GET  /me              # 当前用户信息
│   ├── PUT  /me              # 更新用户信息
│   └── PUT  /password        # 修改密码
│
├── recipes/                   # 菜谱相关
│   ├── GET    /              # 菜谱列表（分页、筛选）
│   ├── GET    /search        # 搜索
│   ├── GET    /hot           # 热门菜谱
│   ├── GET    /{id}/         # 菜谱详情
│   ├── POST   /{id}/favorite/ # 收藏
│   └── DELETE /{id}/favorite/ # 取消收藏
│
├── favorites/                 # 收藏相关
│   ├── GET  /                # 我的收藏列表
│   └── GET  /check/{recipeId}/ # 检查收藏状态
│
├── categories/                # 分类相关
│   └── GET  /                # 分类列表
│
├── ingredients/               # 食材相关
│   └── GET  /                # 食材列表
│
├── analytics/                 # 数据分析（普通用户）
│   ├── GET  /cuisines        # 菜系分布
│   ├── GET  /difficulty      # 难度统计
│   ├── GET  /flavors         # 口味偏好
│   └── GET  /ingredients     # 食材频率
│
└── admin/                     # 管理员接口（需要管理员权限）
    ├── users/                # 用户管理
    │   ├── GET    /          # 用户列表
    │   ├── PUT    /{id}/ban/ # 封禁
    │   └── PUT    /{id}/unban/ # 解封
    │
    ├── recipes/              # 菜谱管理
    │   ├── GET    /          # 菜谱列表
    │   ├── POST   /          # 创建菜谱
    │   ├── PUT    /{id}/     # 更新菜谱
    │   ├── DELETE /{id}/     # 删除菜谱
    │   └── POST   /import/   # 批量导入
    │
    ├── categories/           # 分类管理
    │   ├── GET    /          # 分类列表
    │   ├── POST   /          # 创建分类
    │   ├── PUT    /{id}/     # 更新分类
    │   └── DELETE /{id}/     # 删除分类
    │
    ├── ingredients/          # 食材管理
    │   ├── GET    /          # 食材列表
    │   ├── POST   /          # 创建食材
    │   ├── PUT    /{id}/     # 更新食材
    │   └── DELETE /{id}/     # 删除食材
    │
    ├── analytics/            # 深度数据分析
    │   ├── GET  /cuisines    # 菜系深度分析
    │   ├── GET  /difficulty  # 难度深度分析
    │   ├── GET  /hot         # 热门菜谱分析
    │   └── GET  /ingredient-pairs/ # 食材关联分析
    │
    └── dashboard/            # 数据大盘
        ├── GET  /overview    # 数据总览
        ├── GET  /trends      # 数据趋势
        └── GET  /behaviors   # 用户行为统计
```

---

## 前端架构

### 项目结构

```
frontend/
├── src/
│   ├── assets/               # 静态资源
│   │   ├── images/
│   │   └── styles/
│   │
│   ├── components/           # 公共组件
│   │   ├── layout/           # 布局组件
│   │   │   ├── Header.vue    # 顶部导航
│   │   │   ├── Footer.vue    # 底部
│   │   │   └── Sidebar.vue   # 侧边栏
│   │   ├── common/           # 通用组件
│   │   │   ├── RecipeCard.vue # 菜谱卡片
│   │   │   ├── ImageLoader.vue # 图片加载
│   │   │   └── ChartContainer.vue # 图表容器
│   │   └── admin/            # 管理员组件
│   │
│   ├── views/                # 页面组件
│   │   ├── auth/             # 认证页面
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   └── Profile.vue
│   │   │
│   │   ├── recipes/          # 菜谱页面
│   │   │   ├── RecipeList.vue
│   │   │   ├── RecipeDetail.vue
│   │   │   ├── RecipeCategory.vue
│   │   │   └── HotRecipes.vue
│   │   │
│   │   ├── favorites/        # 收藏页面
│   │   │   └── MyFavorites.vue
│   │   │
│   │   ├── analytics/        # 数据展示页面（普通用户）
│   │   │   ├── DataOverview.vue
│   │   │   └── IngredientFreq.vue
│   │   │
│   │   └── admin/            # 管理员页面
│   │       ├── users/        # 用户管理
│   │       ├── recipes/      # 菜谱管理
│   │       ├── analytics/    # 数据分析
│   │       └── dashboard/    # 数据大盘
│   │
│   ├── api/                  # API 服务层
│   │   ├── request.js        # Axios 封装
│   │   ├── auth.js           # 认证 API
│   │   ├── recipes.js        # 菜谱 API
│   │   ├── analytics.js      # 分析 API
│   │   └── admin.js          # 管理员 API
│   │
│   ├── stores/               # Pinia 状态管理
│   │   ├── user.js           # 用户状态
│   │   ├── recipe.js         # 菜谱状态
│   │   └── admin.js          # 管理员状态
│   │
│   ├── router/               # 路由配置
│   │   └── index.js
│   │
│   ├── utils/                # 工具函数
│   │   ├── format.js         # 格式化工具
│   │   └── constants.js      # 常量
│   │
│   ├── App.vue
│   └── main.js
│
├── public/
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

### 路由设计

```
/                           # 首页
├── /login                  # 登录
├── /register               # 注册
│
├── /recipes                # 菜谱列表
│   ├── /recipes/:id        # 菜谱详情
│   ├── /recipes/category/:id # 分类菜谱
│   └── /recipes/hot        # 热门菜谱
│
├── /favorites              # 我的收藏
│
├── /analytics              # 数据概览（普通用户）
│
├── /profile                # 个人中心
│
└── /admin                  # 管理后台
    ├── /admin/users        # 用户管理
    ├── /admin/recipes      # 菜谱管理
    ├── /admin/categories   # 分类管理
    ├── /admin/ingredients  # 食材管理
    ├── /admin/analytics    # 数据分析
    └── /admin/dashboard    # 数据大盘
```

### 前端初始化状态（2026-01-29）

**阶段一第1步已完成**：前端项目基础结构已创建

#### 已创建的文件及其作用：

| 文件 | 作用 | 说明 |
|------|------|------|
| `frontend/package.json` | 项目依赖配置 | 定义项目元数据和所有 npm 依赖 |
| `frontend/vite.config.js` | Vite 配置 | Vite 构建工具的配置文件（由脚手架自动生成） |
| `frontend/tailwind.config.js` | Tailwind 配置 | 定义 Tailwind 的 content 路径和主题配置 |
| `frontend/postcss.config.js` | PostCSS 配置 | 配置 PostCSS 插件（tailwindcss, autoprefixer） |
| `frontend/src/main.js` | 应用入口 | 导入并初始化 Vue、Pinia、Router、Element Plus |
| `frontend/src/App.vue` | 根组件 | 应用的最顶层组件，包含 `<router-view>` |
| `frontend/src/style.css` | 全局样式 | 包含 Tailwind 指令（@tailwind base/components/utilities） |
| `frontend/src/router/index.js` | 路由配置 | Vue Router 实例，定义应用路由规则 |
| `frontend/src/stores/user.js` | 用户状态管理 | Pinia store，管理用户登录状态和信息 |
| `frontend/src/views/Home.vue` | 首页组件 | 应用的首页，使用 Tailwind 和 Element Plus |

#### 已安装的核心依赖：

| 依赖包 | 版本 | 作用 |
|--------|------|------|
| `vue` | latest | Vue 3 核心框架 |
| `element-plus` | latest | UI 组件库 |
| `pinia` | latest | 状态管理 |
| `vue-router` | latest | 路由管理 |
| `axios` | latest | HTTP 客户端 |
| `echarts` | latest | 数据可视化图表库 |
| `tailwindcss` | v3.4.19 | 原子化 CSS 框架（降级自 v4 以兼容 PostCSS） |
| `postcss` | v8.5.6 | CSS 处理器 |
| `autoprefixer` | v10.4.23 | CSS 自动前缀插件 |

#### 开发服务器：

- 命令：`cd frontend && npm run dev`
- 默认端口：5173（当前运行在 5174，因为 5173 被占用）
- 访问地址：`http://localhost:5174/`

---

### 后端初始化状态（2026-01-29）

**阶段一第2步已完成**：后端项目基础结构已创建

#### 已创建的文件及其作用：

| 文件 | 作用 | 说明 |
|------|------|------|
| `backend_venv/` | Python 虚拟环境 | Python 3.12 虚拟环境目录 |
| `config/backend/settings.py` | Django 配置 | 项目主配置文件（已配置数据库、DRF、JWT、CORS） |
| `config/backend/urls.py` | 主路由 | Django 主路由配置 |
| `config/utils/__init__.py` | 工具模块 | 公共工具模块 |
| `config/utils/response.py` | 统一响应封装 | ApiResponse 类，提供 success/error/paginate 方法 |
| `config/utils/exceptions.py` | 自定义异常 | BusinessError、ValidationError、NotFoundError 等 |
| `config/utils/pagination.py` | 分页配置 | StandardPagination 类，默认每页 20 条 |
| `config/utils/constants.py` | 常量定义 | 用户角色、分类类型、食材分类、行为类型等常量 |
| `config/accounts/` | 用户认证模块 | Django 应用，处理用户注册、登录、认证 |
| `config/recipes/` | 菜谱模块 | Django 应用，处理菜谱数据 |
| `config/categories/` | 分类模块 | Django 应用，处理菜系、场景、人群等分类 |
| `config/ingredients/` | 食材模块 | Django 应用，处理食材数据 |
| `config/favorites/` | 收藏模块 | Django 应用，处理用户收藏功能 |
| `config/analytics/` | 数据分析模块 | Django 应用，处理数据统计分析 |
| `config/admin_panel/` | 管理员模块 | Django 应用，处理管理员功能 |
| `config/behavior_logs/` | 行为日志模块 | Django 应用，处理用户行为记录 |
| `config/README.md` | 后端说明文档 | 后端项目配置和使用说明 |

#### 已安装的核心依赖：

| 依赖包 | 版本 | 作用 |
|--------|------|------|
| `Django` | 5.2.10 | Python Web 框架（降级自 6.0.1） |
| `djangorestframework` | latest | RESTful API 框架 |
| `django-cors-headers` | latest | 跨域支持 |
| `PyMySQL` | 1.1.2 | MySQL 数据库驱动 |
| `djangorestframework-simplejwt` | latest | JWT 认证 |
| `pandas` | latest | 数据分析 |
| `numpy` | latest | 科学计算 |
| `openpyxl` | latest | Excel 文件处理 |

#### 已配置的功能：

| 配置项 | 说明 |
|--------|------|
| 数据库 | MySQL 8.0+，字符集 utf8mb4 |
| 认证 | JWT Token，24 小时有效期 |
| CORS | 允许 localhost:5173-5175 访问 |
| 分页 | 默认每页 20 条，最大 100 条 |
| 时区 | Asia/Shanghai |
| 语言 | zh-hans（简体中文） |

#### 开发服务器：

- 命令：`cd config && ../backend_venv/Scripts/python manage.py runserver`
- 默认端口：8000
- 访问地址：`http://localhost:8000/`
- Django Admin: `http://localhost:8000/admin/`
- API 前缀：`/api/`

#### 注意事项：

1. ✅ 数据库已配置完成（用户名: root, 密码: yuwen123., 端口: 3306）
2. ✅ 数据库 `recipe_analysis_db` 已创建并完成迁移
3. ✅ 超级用户已创建，可以登录 Django Admin
4. 项目结构已调整为标准 Django 格式

#### 开发服务器启动命令：

```bash
cd backend
../backend_venv/Scripts/python manage.py runserver
```

#### 数据库信息：

- 数据库名：`recipe_analysis_db`
- 字符集：`utf8mb4`
- 排序规则：`utf8mb4_unicode_ci`
- 用户：`root`
- 密码：`yuwen123.`
- 主机：`localhost`
- 端口：`3306`

---

## 部署架构

### 开发环境

```
┌─────────────────┐
│  前端开发服务器   │ Vite Dev Server (localhost:5173)
│   (Vue 3)       │
└────────┬────────┘
         │ Proxy
         ▼
┌─────────────────┐
│  后端开发服务器   │ Django Dev Server (localhost:8000)
│   (Django)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MySQL 数据库   │ (localhost:3306)
└─────────────────┘
```

### 生产环境

```
┌─────────────────┐
│   Nginx 反向代理  │ (端口 80/443)
│  ├── /          │ → 前端静态文件
│  └── /api/      │ → 后端服务
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Gunicorn      │ (Django 应用服务器)
│   (Django)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MySQL 数据库   │
└─────────────────┘
```

---

## 安全设计

### 认证与授权

| 组件 | 实现方式 |
|:-----|:---------|
| 认证方式 | JWT (JSON Web Token) |
| Token 存储 | LocalStorage |
| Token 过期 | 24 小时 |
| 密码加密 | bcrypt |
| 权限控制 | 基于角色的访问控制 (RBAC) |

### 数据安全

| 措施 | 说明 |
|:-----|:-----|
| SQL 注入防护 | 使用 ORM 参数化查询 |
| XSS 防护 | 前端输入转义 + 后端验证 |
| CSRF 防护 | CSRF Token |
| 敏感数据 | 密码、身份证等字段 write_only |
| HTTPS | 生产环境强制 HTTPS |

---

## 性能优化

### 数据库优化

- 为常用查询字段添加索引
- 使用 `select_related` 和 `prefetch_related` 优化关联查询
- 分页查询避免大数据量加载
- **当前阶段不使用 Redis 缓存**

### 前端优化

- 图片懒加载
- 路由级别代码分割
- 组件按需加载
- 使用 CDN 加速静态资源

---

## 文档维护

本文档应随着项目发展持续更新：
- 新增表时更新数据库设计
- 架构变更时更新架构图
- 技术选型变更时更新技术栈

**更新日期**: 2026-01-29
