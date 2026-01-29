# 菜谱数据分析系统 - 开发进度记录

> 本文档记录项目开发过程中的进度和完成的工作

---

## 2026-01-29

### 阶段一 第1步：创建前端项目结构

**完成内容**：

1. **创建前端项目**
   - 使用 Vite 脚手架创建 Vue 3 项目
   - 项目位置：`frontend/`
   - 模板：`vue` (Vue 3 + Vite)

2. **安装核心依赖**
   - `element-plus`: UI 组件库
   - `pinia`: 状态管理
   - `vue-router`: 路由管理
   - `axios`: HTTP 客户端
   - `echarts`: 数据可视化图表库
   - `tailwindcss`: 原子化 CSS 框架
   - `postcss`: CSS 处理器
   - `autoprefixer`: CSS 自动前缀

3. **配置文件**
   - `tailwind.config.js`: Tailwind CSS 配置
   - `postcss.config.js`: PostCSS 配置
   - `src/main.js`: 主入口文件，整合 Pinia、Router、Element Plus
   - `src/style.css`: 全局样式，包含 Tailwind 指令

4. **项目结构**
   ```
   frontend/
   ├── src/
   │   ├── router/
   │   │   └── index.js         # Vue Router 配置
   │   ├── stores/
   │   │   └── user.js          # Pinia 用户状态管理
   │   ├── views/
   │   │   └── Home.vue         # 首页组件
   │   ├── App.vue              # 根组件
   │   ├── main.js              # 主入口
   │   └── style.css            # 全局样式
   ├── tailwind.config.js       # Tailwind 配置
   ├── postcss.config.js        # PostCSS 配置
   └── package.json             # 依赖配置
   ```

5. **测试验证**
   - ✅ 开发服务器启动成功 (`npm run dev`)
   - ✅ 服务运行在 `http://localhost:5175/`（端口 5173、5174 被占用）
   - ✅ 所有依赖正确安装

6. **问题修复**
   - ⚠️ Tailwind CSS v4 与 PostCSS 配置不兼容
   - ✅ 降级到 Tailwind CSS v3.4.0 解决问题
   - ✅ 开发服务器正常启动，无错误

**下一步**：等待用户验证后，执行阶段一第2步（创建后端项目）

---

### 阶段一 第2步：创建后端项目结构

**完成内容**：

1. **创建 Python 虚拟环境**
   - 虚拟环境位置：`backend_venv/`（项目根目录）
   - Python 版本：3.12

2. **安装 Django 和相关依赖**
   - `Django 5.2.10`: Python Web 框架（降级自 6.0.1 以兼容 PyMySQL）
   - `djangorestframework`: RESTful API 框架
   - `django-cors-headers`: 跨域支持
   - `PyMySQL`: MySQL 数据库驱动
   - `djangorestframework-simplejwt`: JWT 认证
   - `pandas`: 数据分析
   - `numpy`: 科学计算
   - `openpyxl`: Excel 文件处理

3. **创建 Django 项目**
   - 使用 Django 模板创建项目
   - 项目位置：`backend/`
   - 配置目录：`backend/config/`

4. **创建 8 个 Django 应用**
   - `accounts`: 用户认证模块
   - `recipes`: 菜谱模块
   - `categories`: 分类模块
   - `ingredients`: 食材模块
   - `favorites`: 收藏模块
   - `analytics`: 数据分析模块
   - `admin_panel`: 管理员模块
   - `behavior_logs`: 行为日志模块

5. **创建 utils 公共工具模块**
   - `response.py`: 统一响应封装（ApiResponse 类）
   - `exceptions.py`: 自定义异常（BusinessError、ValidationError、NotFoundError、PermissionDeniedError、StateNotAllowedError）
   - `pagination.py`: 分页配置（StandardPagination 类）
   - `constants.py`: 常量定义（用户角色、分类类型、食材分类、行为类型等）

6. **配置数据库连接**
   - 配置 MySQL 数据库连接（用户名: root, 密码: yuwen123., 端口: 3306）
   - 设置字符集为 utf8mb4
   - 配置 PyMySQL 作为 MySQL 驱动
   - 配置 DRF（分页、权限等）
   - 配置 JWT 认证（24小时有效期）
   - 配置 CORS（允许本地开发服务器）
   - 设置时区为 Asia/Shanghai
   - 设置语言为 zh-hans

7. **项目结构调整**
   - 调整为标准 Django 项目结构
   - `backend/config/` - Django 配置目录
   - `backend/manage.py` - Django 管理脚本
   - `backend/utils/` - 公共工具模块
   - `backend/[apps]/` - Django 应用模块
   - 更新 `manage.py` 的 DJANGO_SETTINGS_MODULE 为 `'config.settings'`
   - 更新 `settings.py` 的 ROOT_URLCONF 为 `'config.urls'`
   - 更新 `settings.py` 的 WSGI_APPLICATION 为 `'config.wsgi.application'`

8. **项目结构**
   ```
   backend/
   ├── config/                 # Django 项目配置
   │   ├── settings.py        # 项目设置（已配置）
   │   ├── urls.py            # 主路由
   │   └── wsgi.py
   ├── utils/                  # 公共工具模块
   │   ├── __init__.py
   │   ├── response.py        # ✅ 统一响应封装
   │   ├── exceptions.py      # ✅ 自定义异常
   │   ├── pagination.py      # ✅ 分页配置
   │   └── constants.py       # ✅ 常量定义
   ├── accounts/              # ✅ 用户认证模块
   ├── recipes/               # ✅ 菜谱模块
   ├── categories/            # ✅ 分类模块
   ├── ingredients/           # ✅ 食材模块
   ├── favorites/             # ✅ 收藏模块
   ├── analytics/             # ✅ 数据分析模块
   ├── admin_panel/           # ✅ 管理员模块
   ├── behavior_logs/         # ✅ 行为日志模块
   ├── manage.py              # Django 管理脚本
   ├── README.md              # ✅ 后端说明文档
   ├── static/                # 静态文件目录
   └── mediafiles/            # 媒体文件目录
   ```

9. **数据库初始化**
   - ✅ 创建数据库 `recipe_analysis_db`（字符集: utf8mb4）
   - ✅ 运行数据库迁移（应用所有 Django 内置迁移）
   - ✅ Django 开发服务器启动成功
   - ✅ 超级用户创建完成

10. **测试验证**
    - ✅ Django 项目配置检查通过（`manage.py check`）
    - ✅ 虚拟环境创建成功
    - ✅ 所有依赖正确安装
    - ✅ 数据库连接成功
    - ✅ 数据库迁移完成
    - ✅ 服务器启动成功

11. **问题修复**
    - ⚠️ Django 6.0.1 与 PyMySQL 版本检查不兼容
    - ✅ 降级到 Django 5.2.10 解决问题
    - ⚠️ 缺少 static 和 mediafiles 目录
    - ✅ 创建所需目录
    - ⚠️ 项目结构需要调整
    - ✅ 调整为标准 Django 项目结构
    - ⚠️ 数据库不存在
    - ✅ 创建数据库并完成迁移

12. **创建后端 README**
    - 位置：`backend/README.md`
    - 包含项目结构说明
    - 包含数据库配置步骤（密码: yuwen123.）
    - 包含服务器启动说明
    - 包含快速开始指南

**最终状态**：✅ 后端项目完全配置完成并测试通过

**下一步**：等待用户指示后，执行阶段一第3步（创建数据脚本目录）

---

### 阶段一 第3步：创建数据脚本目录

**完成内容**：

1. **创建数据脚本目录结构**
   - 主目录：`data-scripts/`
   - 四个子目录：`spiders/`、`cleaning/`、`importing/`、`simulation/`

2. **创建说明文档**
   - `data-scripts/README.md`：数据脚本总体说明，包含执行顺序和注意事项
   - `data-scripts/spiders/README.md`：爬虫脚本说明（目标：下厨房、美食杰）
   - `data-scripts/cleaning/README.md`：数据清洗规则说明
   - `data-scripts/importing/README.md`：数据导入流程和性能优化方案
   - `data-scripts/simulation/README.md`：用户行为模拟规则说明

3. **创建测试脚本**
   - `data-scripts/test_structure.py`：验证目录结构和测试基本功能
   - 测试项包括：目录检查、Python模块导入、文件读写、JSON处理、后端配置检测

4. **项目结构**
   ```
   data-scripts/
   ├── README.md              # 总体说明文档
   ├── test_structure.py      # 目录结构测试脚本
   ├── spiders/               # 爬虫脚本
   │   └── README.md
   ├── cleaning/              # 数据清洗脚本
   │   └── README.md
   ├── importing/             # 数据导入脚本
   │   └── README.md
   └── simulation/            # 用户行为模拟脚本
       └── README.md
   ```

5. **测试验证**
   - ✅ 所有子目录创建成功
   - ✅ 所有 README 文件创建成功
   - ✅ Python 模块导入测试通过（json、random）
   - ✅ 文件读写测试通过
   - ✅ JSON 处理测试通过
   - ✅ 后端项目配置检测通过
   - ✅ Django 配置文件存在
   - ✅ 数据库配置正确

6. **各目录用途说明**
   - **spiders/**：从下厨房、美食杰等网站爬取菜谱数据（10,000-20,000条）
   - **cleaning/**：清洗和标准化爬取的数据（去重、补全缺失值、统一格式）
   - **importing/**：将清洗后的数据批量导入 MySQL 数据库
   - **simulation/**：生成模拟用户行为数据（100+用户，10,000+行为记录）

**最终状态**：✅ 数据脚本目录结构完全创建并测试通过

**下一步**：等待用户指示后，执行阶段一第4步（配置开发环境）

---

### 阶段二 第1步：设计用户表结构

**完成内容**：

1. **创建用户模型** (`backend/accounts/models.py`)
   - `User` 模型 - 继承 AbstractBaseUser, PermissionsMixin
   - `UserProfile` 模型 - 1:1 关联的用户资料表
   - `UserManager` - 自定义用户管理器

2. **User 模型字段**
   - `id` - 主键
   - `username` - 用户名（唯一，已索引）
   - `email` - 邮箱（唯一，已索引）
   - `password` - 加密密码
   - `role` - 用户角色（user/admin，已索引）
   - `is_active` - 是否激活（已索引）
   - `is_staff` - 是否管理员
   - `last_login` - 最后登录时间
   - `created_at` - 创建时间
   - `updated_at` - 更新时间

3. **UserProfile 模型字段**
   - `id` - 主键
   - `user` - 关联用户（一对一）
   - `nickname` - 昵称
   - `phone` - 手机号（唯一，已索引）
   - `bio` - 个人简介
   - `avatar_url` - 头像 URL
   - `created_at` - 创建时间
   - `updated_at` - 更新时间

4. **更新 Django settings.py**
   - 添加 `AUTH_USER_MODEL = 'accounts.User'`

5. **创建数据库迁移文件**
   - `accounts/migrations/0001_initial.py`

6. **配置环境变量** (`.env`)
   - 更新 DB_PORT 为 3307
   - 更新 DB_PASSWORD 为 yuwen123

7. **创建数据库**
   - 数据库名: `recipe_analysis_db`
   - 字符集: `utf8mb4`

8. **执行迁移**
   - 成功创建 users 和 user_profiles 表
   - 所有索引正确创建

9. **测试验证**
   - ✅ 模型结构验证通过
   - ✅ 数据库表创建成功
   - ✅ 用户创建测试通过
   - ✅ 1:1 关联测试通过

10. **创建的验证脚本**
    - `backend/verify_user_model.py` - 模型验证脚本
    - `backend/test_db_connection.py` - 数据库连接测试脚本

**文件结构**：
```
backend/
├── accounts/
│   ├── models.py           # ✅ User, UserProfile, UserManager
│   └── migrations/
│       └── 0001_initial.py # ✅ 用户表迁移文件
├── config/
│   └── settings.py         # ✅ AUTH_USER_MODEL 已配置
├── .env                    # ✅ 数据库配置已更新
├── verify_user_model.py    # ✅ 模型验证脚本
└── test_db_connection.py   # ✅ 数据库连接测试脚本
```

**数据库结构**：
```
recipe_analysis_db (MySQL 3307)
├── users              # 用户主表
│   ├── id (PK)
│   ├── username (UNIQUE, INDEX)
│   ├── email (UNIQUE, INDEX)
│   ├── password
│   ├── role (INDEX) - user/admin
│   ├── is_active (INDEX)
│   ├── is_staff
│   ├── last_login
│   ├── created_at
│   └── updated_at
└── user_profiles      # 用户资料表
    ├── id (PK)
    ├── user_id (UNIQUE) → users.id
    ├── nickname
    ├── phone (UNIQUE, INDEX)
    ├── bio
    ├── avatar_url
    ├── created_at
    └── updated_at
```

**最终状态**：✅ 用户表结构完全创建并测试通过

**下一步**：等待用户指示后，执行阶段二第2步（设计菜谱表结构）

---

### 阶段一 第4步：配置开发环境

**完成内容**：

1. **创建前端环境变量文件**
   - `frontend/.env.local`：本地开发环境变量（不提交到版本控制）
   - `frontend/.env.example`：环境变量模板（提交到版本控制）
   - 配置项：
     - `VITE_API_BASE_URL`: 后端 API 地址
     - `VITE_API_TIMEOUT`: 请求超时时间
     - `VITE_APP_TITLE`: 应用标题
     - `VITE_PAGE_SIZE`: 分页大小

2. **创建后端环境变量文件**
   - `backend/.env`：本地开发环境变量（不提交到版本控制）
   - `backend/.env.example`：环境变量模板（提交到版本控制）
   - 配置项：
     - `SECRET_KEY`: Django 密钥
     - `DEBUG`: 调试模式
     - `ALLOWED_HOSTS`: 允许的主机
     - `DB_NAME`: 数据库名称
     - `DB_USER`: 数据库用户
     - `DB_PASSWORD`: 数据库密码
     - `DB_HOST`: 数据库主机
     - `DB_PORT`: 数据库端口
     - `LANGUAGE_CODE`: 语言代码
     - `TIME_ZONE`: 时区

3. **更新 Django settings.py**
   - 添加 `python-dotenv` 导入
   - 使用 `os.getenv()` 从环境变量读取配置
   - 设置默认值以防环境变量未定义
   - 更新 SECRET_KEY、DEBUG、ALLOWED_HOSTS 配置
   - 更新数据库配置
   - 更新国际化和时区配置

4. **创建后端 requirements.txt**
   - Django 5.2.10
   - djangorestframework 3.15.2
   - django-cors-headers 4.6.0
   - djangorestframework-simplejwt 5.5.0
   - PyMySQL 1.1.1
   - pandas 2.2.3
   - numpy 2.2.2
   - openpyxl 3.1.5
   - python-dotenv 1.1.0

5. **创建开发环境验证脚本**
   - `test_dev_env.py`：完整的开发环境验证工具
   - 测试项：
     - .gitignore 配置正确性
     - 环境变量文件存在性
     - 环境变量内容完整性
     - Django settings.py 配置正确性
     - 前端环境变量配置

6. **更新 .gitignore**
   - 添加 `*.pyc` 条目（已有 `*.py[cod]` 覆盖）

7. **项目结构**
   ```
   .
   ├── .gitignore              # ✅ 更新，包含所有排除项
   ├── frontend/
   │   ├── .env.local          # ✅ 前端环境变量（本地）
   │   └── .env.example        # ✅ 前端环境变量模板
   ├── backend/
   │   ├── .env                # ✅ 后端环境变量（本地）
   │   ├── .env.example        # ✅ 后端环境变量模板
   │   ├── requirements.txt    # ✅ 依赖列表
   │   ├── config/
   │   │   └── settings.py     # ✅ 更新，从环境变量读取
   │   └── test_env.py         # ✅ 环境变量测试脚本
   └── test_dev_env.py         # ✅ 开发环境验证脚本
   ```

8. **测试验证**
   - ✅ 环境变量文件创建成功（4个文件）
   - ✅ 环境变量可正确读取（8个后端变量 + 2个前端变量）
   - ✅ Django settings.py 配置正确
   - ✅ .gitignore 配置完整
   - ✅ 所有 5/5 验证测试通过

9. **文件作用说明**
   - `.env.local` (前端)：Vite 在开发时自动加载，包含 API 配置
   - `.env` (后端)：通过 python-dotenv 手动加载，包含 Django 配置
   - `.env.example`：模板文件，供其他开发者参考复制
   - `requirements.txt`：后端 Python 依赖列表，用于虚拟环境安装
   - `test_dev_env.py`：验证开发环境配置完整性的工具

**最终状态**：✅ 开发环境配置完全完成并验证通过

**下一步**：等待用户验证测试结果后，执行阶段二第2步（设计菜谱表结构）

---

### 阶段二 第2步：设计菜谱表结构

**完成内容**：

1. **创建 Recipe 模型** (`backend/recipes/models.py`)
   - `Recipe` 模型 - 菜谱主表，存储菜谱的基本信息

2. **Recipe 模型字段**
   - `id` - 主键（BigAutoField）
   - `name` - 菜谱名称（最大200字符，已索引）
   - `cuisine_type` - 菜系分类（如"川菜"、"粤菜"，已索引）
   - `scene_type` - 场景分类（如"早餐"、"午餐"、"晚餐"，已索引）
   - `target_audience` - 适用人群（如"儿童"、"老人"、"孕妇"）
   - `difficulty` - 难度等级（easy/medium/hard，默认medium，已索引）
   - `cooking_time` - 烹饪时长（分钟，可为空）
   - `image_url` - 成品图片URL（最大500字符）
   - `steps` - 制作步骤（文本或JSON格式）
   - `flavor_tags` - 口味标签（逗号分隔，如"辣,甜,酸"）
   - `view_count` - 点击量（默认0，已索引）
   - `favorite_count` - 收藏量（默认0，已索引）
   - `created_at` - 创建时间（自动添加，已索引）
   - `updated_at` - 更新时间（自动更新）

3. **模型方法**
   - `get_flavor_list()` - 将逗号分隔的口味标签转换为列表
   - `set_flavor_list()` - 将列表转换为逗号分隔的口味标签
   - `__str__()` - 返回菜谱名称

4. **数据库索引**
   - `recipes_name_66b98f_idx` - 菜谱名称索引（用于搜索）
   - `recipes_cuisine_3862f6_idx` - 菜系分类索引（用于筛选）
   - `recipes_difficu_9b84bb_idx` - 难度等级索引（用于筛选）
   - `recipes_scene_t_695d9f_idx` - 场景分类索引（用于筛选）
   - `recipes_view_co_7980ec_idx` - 点击量索引（用于排序）
   - `recipes_favorit_456657_idx` - 收藏量索引（用于排序）
   - `recipes_created_00c815_idx` - 创建时间索引（用于排序）

5. **创建数据库迁移文件**
   - `recipes/migrations/0001_initial.py`

6. **执行迁移**
   - 成功创建 recipes 表
   - 所有索引正确创建

7. **创建验证脚本**
   - `backend/verify_recipe_model.py` - 模型验证脚本

8. **测试验证**
   - ✅ 模型结构验证通过
   - ✅ 数据库表创建成功
   - ✅ 菜谱创建测试通过
   - ✅ 菜谱读取测试通过
   - ✅ 菜谱更新测试通过
   - ✅ 口味标签方法测试通过
   - ✅ 筛选功能测试通过（按菜系、难度）
   - ✅ 排序功能测试通过（按点击量）
   - ✅ 数据库索引验证通过（8个索引）

**文件结构**：
```
backend/
├── recipes/
│   ├── models.py           # ✅ Recipe 模型
│   └── migrations/
│       └── 0001_initial.py # ✅ 菜谱表迁移文件
└── verify_recipe_model.py  # ✅ 模型验证脚本
```

**数据库结构**：
```
recipe_analysis_db (MySQL 3307)
├── users              # 用户主表
├── user_profiles      # 用户资料表
└── recipes            # ✅ 菜谱主表
    ├── id (PK)
    ├── name (INDEX)
    ├── cuisine_type (INDEX)
    ├── scene_type (INDEX)
    ├── target_audience
    ├── difficulty (INDEX) - easy/medium/hard
    ├── cooking_time
    ├── image_url
    ├── steps
    ├── flavor_tags
    ├── view_count (INDEX)
    ├── favorite_count (INDEX)
    ├── created_at (INDEX)
    └── updated_at
```

**设计说明**：
- 使用 `CharField` 存储分类字段（cuisine_type, scene_type），为后续关联分类表预留灵活性
- 口味标签使用逗号分隔的字符串存储，简化实现，后续可扩展为独立表
- 难度等级使用 `choices` 参数，确保数据一致性
- 统计字段（view_count, favorite_count）为冗余设计，通过触发器或应用层维护
- 索引覆盖所有常用查询和排序场景，优化查询性能

**最终状态**：✅ 菜谱表结构完全创建并测试通过

**下一步**：等待用户验证测试结果后，执行阶段二第3步（设计食材表与关联表）

---

### 阶段二 第3步：设计食材表与关联表

**完成内容**：

1. **创建 Ingredient 模型** (`backend/ingredients/models.py`)
   - `Ingredient` 模型 - 食材库，存储各种食材的基本信息

2. **Ingredient 模型字段**
   - `id` - 主键
   - `name` - 食材名称（最大100字符，唯一，已索引）
   - `category` - 食材分类（choices: vegetable/meat/seafood/seasoning/fruit/grain/dairy/other，已索引）
   - `created_at` - 创建时间
   - `updated_at` - 更新时间

3. **创建 RecipeIngredient 模型** (`backend/recipes/models.py`)
   - `RecipeIngredient` 模型 - 菜谱-食材关联表，实现多对多关系

4. **RecipeIngredient 模型字段**
   - `id` - 主键
   - `recipe` - 关联菜谱（外键 → Recipe，级联删除，已索引）
   - `ingredient` - 关联食材（外键 → Ingredient，级联删除，已索引）
   - `amount` - 用量描述（最大100字符，如"200g"、"2个"、"适量"）
   - `sort_order` - 排序序号（默认0）
   - `created_at` - 创建时间

5. **联合唯一约束**
   - `unique_recipe_ingredient` - 同一菜谱不能重复添加同一食材

6. **数据库索引**
   - ingredients 表：
     - `ingredients_name_9f76a2_idx` - 食材名称索引（用于搜索）
     - `ingredients_categor_ed8c56_idx` - 食材分类索引（用于筛选）
   - recipe_ingredients 表：
     - `recipe_ingr_recipe__c09862_idx` - 菜谱ID索引（用于查询菜谱的食材）
     - `recipe_ingr_ingredi_1f18f7_idx` - 食材ID索引（用于查询使用该食材的菜谱）

7. **创建数据库迁移文件**
   - `ingredients/migrations/0001_initial.py`
   - `recipes/migrations/0002_recipeingredient.py`

8. **执行迁移**
   - 成功创建 ingredients 表
   - 成功创建 recipe_ingredients 表
   - 所有索引和约束正确创建

9. **创建验证脚本**
   - `backend/verify_ingredient_models.py` - 模型验证脚本

10. **测试验证**
    - ✅ 食材创建和查询测试通过
    - ✅ 菜谱-食材关联创建测试通过
    - ✅ 反向查询测试通过（菜谱→食材、食材→菜谱）
    - ✅ 联合唯一约束测试通过（IntegrityError 正确抛出）
    - ✅ 食材反向查询测试通过
    - ✅ 数据库索引验证通过（6个索引）
    - ✅ 外键约束验证通过（2个外键）

**文件结构**：
```
backend/
├── ingredients/
│   ├── models.py              # ✅ Ingredient 模型
│   └── migrations/
│       └── 0001_initial.py    # ✅ 食材表迁移文件
├── recipes/
│   ├── models.py              # ✅ Recipe + RecipeIngredient 模型
│   └── migrations/
│       └── 0002_recipeingredient.py  # ✅ 关联表迁移文件
└── verify_ingredient_models.py # ✅ 模型验证脚本
```

**数据库结构**：
```
recipe_analysis_db (MySQL 3307)
├── users              # 用户主表
├── user_profiles      # 用户资料表
├── recipes            # 菜谱主表
├── ingredients        # ✅ 食材库
│   ├── id (PK)
│   ├── name (UNIQUE, INDEX)
│   ├── category (INDEX) - meat/vegetable/seafood/seasoning等
│   ├── created_at
│   └── updated_at
└── recipe_ingredients # ✅ 菜谱-食材关联表
    ├── id (PK)
    ├── recipe_id (INDEX, FK) → recipes.id (CASCADE)
    ├── ingredient_id (INDEX, FK) → ingredients.id (CASCADE)
    ├── amount
    ├── sort_order
    ├── created_at
    └── UNIQUE(recipe_id, ingredient_id)
```

**使用示例**：
```python
# 创建食材
from ingredients.models import Ingredient

chicken = Ingredient.objects.create(name='鸡肉', category='meat')
potato = Ingredient.objects.create(name='土豆', category='vegetable')

# 为菜谱添加食材
from recipes.models import Recipe, RecipeIngredient

recipe = Recipe.objects.get(name='宫保鸡丁')
RecipeIngredient.objects.create(
    recipe=recipe,
    ingredient=chicken,
    amount='300g',
    sort_order=1
)

# 查询菜谱的所有食材
for ri in recipe.recipe_ingredients.all():
    print(f"{ri.ingredient.name}: {ri.amount}")

# 查询使用某食材的所有菜谱
for ri in chicken.recipe_ingredients.all():
    print(ri.recipe.name)
```

**设计说明**：
- 食材名称使用唯一约束，避免重复创建
- 食材分类使用 choices 参数，确保数据一致性
- 关联表包含用量字段，支持灵活的用量描述
- 排序序号支持食材按特定顺序显示
- 联合唯一约束防止同一菜谱重复添加同一食材
- 双向外键级联删除，确保数据一致性

**最终状态**：✅ 食材表与关联表完全创建并测试通过

**下一步**：等待用户指示后，执行阶段二第4步（设计收藏表结构）

---

### 阶段二 第4步：设计收藏表结构

**完成内容**：

1. **创建 UserFavorite 模型** (`backend/favorites/models.py`)
   - `UserFavorite` 模型 - 用户收藏表，存储用户对菜谱的收藏关系

2. **UserFavorite 模型字段**
   - `id` - 主键
   - `user` - 关联用户（外键 → User，级联删除，已索引）
   - `recipe` - 关联菜谱（外键 → Recipe，级联删除，已索引）
   - `created_at` - 收藏时间（自动添加，已索引）

3. **联合唯一约束**
   - `unique_user_recipe_favorite` - 同一用户不能重复收藏同一菜谱

4. **数据库索引**
   - `user_favori_user_id_216ac3_idx` - 用户ID索引（用于查询用户的收藏）
   - `user_favori_recipe__6f6610_idx` - 菜谱ID索引（用于查询收藏该菜谱的用户）
   - `user_favori_created_d0b934_idx` - 收藏时间索引（用于按时间排序）

5. **创建数据库迁移文件**
   - `favorites/migrations/0001_initial.py`

6. **执行迁移**
   - 成功创建 user_favorites 表
   - 所有索引和约束正确创建

7. **创建验证脚本**
   - `backend/verify_favorite_model.py` - 模型验证脚本

8. **测试验证**
   - ✅ 模型结构验证通过
   - ✅ 收藏创建测试通过
   - ✅ 联合唯一约束测试通过（重复收藏被正确拒绝）
   - ✅ 反向查询测试通过（user.favorites、recipe.favorited_by）
   - ✅ 数据库索引验证通过（4个索引）

**文件结构**：
```
backend/
├── favorites/
│   ├── models.py              # ✅ UserFavorite 模型
│   ├── admin.py               # ✅ Django Admin 配置
│   └── migrations/
│       └── 0001_initial.py    # ✅ 收藏表迁移文件
└── verify_favorite_model.py   # ✅ 模型验证脚本
```

**数据库结构**：
```
recipe_analysis_db (MySQL 3307)
├── users              # 用户主表
├── user_profiles      # 用户资料表
├── recipes            # 菜谱主表
├── ingredients        # 食材库
├── recipe_ingredients # 菜谱-食材关联表
└── user_favorites     # ✅ 用户收藏表
    ├── id (PK)
    ├── user_id (INDEX, FK) → users.id (CASCADE)
    ├── recipe_id (INDEX, FK) → recipes.id (CASCADE)
    ├── created_at (INDEX)
    └── UNIQUE(user_id, recipe_id)
```

**使用示例**：
```python
# 创建收藏
from accounts.models import User
from recipes.models import Recipe
from favorites.models import UserFavorite

user = User.objects.get(username='testuser')
recipe = Recipe.objects.get(name='宫保鸡丁')

favorite = UserFavorite.objects.create(user=user, recipe=recipe)

# 查询用户的收藏
user_favorites = user.favorites.all()

# 查询菜谱的收藏者
recipe_favorited = recipe.favorited_by.all()
```

**设计说明**：
- 联合唯一约束防止同一用户重复收藏同一菜谱
- 双向外键级联删除，确保数据一致性
- 反向关系命名：`favorites`（用户的收藏）、`favorited_by`（菜谱的收藏者）
- 收藏时间索引支持按时间排序查询

**最终状态**：✅ 收藏表结构完全创建并测试通过

**下一步**：等待用户验证测试结果后，执行阶段二第5步（设计用户行为表）

---

## 待完成任务

- [x] 阶段一 第1步：创建前端项目结构
- [x] 阶段一 第2步：创建后端项目结构（Django）
- [x] 阶段一 第3步：创建数据脚本目录
- [x] 阶段一 第4步：配置开发环境
- [x] 阶段二 第1步：设计用户表结构
- [x] 阶段二 第2步：设计菜谱表结构
- [x] 阶段二 第3步：设计食材表与关联表
- [x] 阶段二 第4步：设计收藏表结构
