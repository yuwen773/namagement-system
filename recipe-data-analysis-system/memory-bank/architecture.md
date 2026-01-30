# 菜谱数据分析系统 - 架构设计

> 更新日期: 2026-01-30
> 当前阶段: 阶段四进行中（1/7 步骤完成）

---

## 系统架构

```
前端层 (Vue 3)
    │ HTTP/JSON (REST API)
    ▼
API 网关层 (Django) - 认证/权限/统一响应
    │
    ▼
业务逻辑层 (Django Apps)
    │ ORM
    ▼
数据层 (MySQL 8.0+)
```

---

## 技术栈

| 层级 | 技术选型 |
|:-----|:---------|
| 前端 | Vue 3 + Vite + Element Plus + Tailwind CSS + ECharts + Pinia + Axios |
| 后端 | Django 5.2 + DRF + JWT + Pandas + NumPy |
| 数据库 | MySQL 8.0+ (utf8mb4) |

---

## 项目结构

```
recipe-data-analysis-system/
├── frontend/              # Vue 3 前端项目
├── backend/               # Django 后端项目
├── backend_venv/          # Python 虚拟环境
├── data-scripts/          # 数据脚本（爬虫、清洗、导入、模拟）
├── memory-bank/           # 项目文档（架构、进度、规范等）
├── sql/                   # 数据库初始化脚本
├── .gitignore             # Git 忽略配置
└── CLAUDE.md              # 项目指导文档
```

---

## 数据库设计

### 当前状态

| 表名 | 状态 | 说明 |
|:-----|:----:|:-----|
| users | ✅ 已创建 | 用户主表 |
| user_profiles | ✅ 已创建 | 用户资料表 |
| recipes | ✅ 已创建 | 菜谱主表 |
| categories | ✅ 已创建 | 分类表 |
| ingredients | ✅ 已创建 | 食材库 |
| recipe_ingredients | ✅ 已创建 | 菜谱-食材关联 |
| recipe_steps | ⏳ 待创建 | 制作步骤表 |
| user_favorites | ✅ 已创建 | 用户收藏 |
| user_behavior_logs | ✅ 已创建 | 行为日志 |

### 核心表结构（完整设计）

| 表名 | 说明 | 目标记录数 |
|:-----|:-----|:----------:|
| users / user_profiles | 用户账户与资料 | 100+ |
| categories | 分类（菜系/场景/难度/口味） | 50+ |
| ingredients | 食材库 | 500+ |
| recipes | 菜谱主表 | 10,000-20,000 |
| recipe_ingredients | 菜谱-食材关联 | 50,000+ |
| recipe_steps | 制作步骤 | 30,000+ |
| user_favorites | 用户收藏 | 5,000+ |
| user_behavior_logs | 行为日志 | 10,000+ |

### 已创建表详细设计

#### users 表（用户主表）✅

| 字段 | 类型 | 约束 | 说明 |
|:-----|:-----|:-----|:-----|
| id | bigint | PK, AUTO | 主键 |
| username | varchar(50) | UNIQUE, NOT NULL, INDEX | 用户名（登录用） |
| email | varchar(100) | UNIQUE, NULL, INDEX | 邮箱 |
| password | varchar(128) | NOT NULL | 加密密码 |
| role | varchar(10) | NOT NULL, INDEX | user/admin |
| is_active | tinyint(1) | NOT NULL, INDEX | 是否激活 |
| is_staff | tinyint(1) | NOT NULL | 是否管理员 |
| is_superuser | tinyint(1) | NOT NULL | 是否超级用户 |
| last_login | datetime(6) | NULL | 最后登录时间 |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |

**索引**：
- PRIMARY: `id`
- UNIQUE: `username`, `email`
- INDEX: `role`, `is_active`

**Django 模型**：`accounts.models.User`
- 继承: `AbstractBaseUser`, `PermissionsMixin`
- 认证字段: `USERNAME_FIELD = 'username'`
- 管理器: `UserManager`（提供 `create_user`, `create_superuser`）

#### user_profiles 表（用户资料）✅

| 字段 | 类型 | 约束 | 说明 |
|:-----|:-----|:-----|:-----|
| id | bigint | PK, AUTO | 主键 |
| user_id | bigint | UNIQUE, NOT NULL, FK | 关联 users.id |
| nickname | varchar(50) | NOT NULL | 昵称 |
| phone | varchar(20) | UNIQUE, NULL | 手机号 |
| bio | longtext | NOT NULL | 个人简介 |
| avatar_url | varchar(500) | NOT NULL | 头像 URL |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |

**关系**：
- `user_id` → `users.id`（ON DELETE CASCADE）
- 1:1 关系，通过 `user.profile` 访问

**Django 模型**：`accounts.models.UserProfile`

**使用示例**：
```python
# 创建用户
from accounts.models import User

user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='password123'
)

# 访问用户资料
profile = user.profile
profile.nickname = '测试用户'
profile.bio = '这是我的简介'
profile.save()

# 检查用户角色
if user.role == 'admin':
    # 管理员逻辑
    pass
```

#### recipes 表（菜谱主表）✅

| 字段 | 类型 | 约束 | 说明 |
|:-----|:-----|:-----|:-----|
| id | bigint | PK, AUTO | 主键 |
| name | varchar(200) | NOT NULL, INDEX | 菜谱名称 |
| cuisine_type | varchar(50) | NULL, INDEX | 菜系分类（川菜、粤菜等） |
| scene_type | varchar(50) | NULL, INDEX | 场景分类（早餐、午餐、晚餐等） |
| target_audience | varchar(100) | NULL | 适用人群（儿童、老人、孕妇等） |
| difficulty | varchar(10) | NOT NULL, INDEX, DEFAULT 'medium' | 难度等级（easy/medium/hard） |
| cooking_time | int | NULL | 烹饪时长（分钟） |
| image_url | varchar(500) | NULL | 成品图片 URL |
| steps | longtext | NULL | 制作步骤（文本或JSON格式） |
| flavor_tags | varchar(200) | NULL | 口味标签（逗号分隔，如"辣,甜,酸"） |
| view_count | int | NOT NULL, INDEX, DEFAULT 0 | 点击量 |
| favorite_count | int | NOT NULL, INDEX, DEFAULT 0 | 收藏量 |
| created_at | datetime(6) | NOT NULL, INDEX | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |

**索引**：
- PRIMARY: `id`
- INDEX: `name` - 用于搜索
- INDEX: `cuisine_type` - 用于按菜系筛选
- INDEX: `difficulty` - 用于按难度筛选
- INDEX: `scene_type` - 用于按场景筛选
- INDEX: `view_count` - 用于按热度排序
- INDEX: `favorite_count` - 用于按收藏排序
- INDEX: `created_at` (DESC) - 用于按时间排序

**Django 模型**：`recipes.models.Recipe`
- 难度选择：`DIFFICULTY_CHOICES = [('easy', '简单'), ('medium', '中等'), ('hard', '困难')]`
- 默认排序：`ordering = ['-created_at']`
- 方法：
  - `get_flavor_list()` - 将逗号分隔的口味标签转换为列表
  - `set_flavor_list(flavor_list)` - 将列表转换为逗号分隔的口味标签

**使用示例**：
```python
# 创建菜谱
from recipes.models import Recipe

recipe = Recipe.objects.create(
    name='宫保鸡丁',
    cuisine_type='川菜',
    scene_type='晚餐',
    difficulty='medium',
    cooking_time=30,
    image_url='https://example.com/kungpao.jpg',
    steps='1. 鸡胸肉切丁\n2. 花生米炸香\n3. 爆炒鸡肉\n4. 调味收汁',
    flavor_tags='辣,甜,酸'
)

# 获取口味标签列表
flavors = recipe.get_flavor_list()  # ['辣', '甜', '酸']

# 按菜系筛选
sichuan_recipes = Recipe.objects.filter(cuisine_type='川菜')

# 按难度筛选
easy_recipes = Recipe.objects.filter(difficulty='easy')

# 按热度排序
hot_recipes = Recipe.objects.order_by('-view_count')
```

**设计说明**：

| 设计决策 | 理由 |
|:---------|:-----|
| 分类字段使用 CharField | 为后续关联分类表预留灵活性，当前直接存储简化实现 |
| 口味标签用逗号分隔 | 简化多对多关系，后续可扩展为独立标签表 |
| 难度等级使用 choices | 确保数据一致性，便于前端下拉选择 |
| 冗余统计字段 | 避免频繁 JOIN 统计，通过应用层或触发器维护 |
| 多维度索引 | 覆盖常用查询（筛选、搜索、排序）场景，优化性能 |

#### ingredients 表（食材库）✅

| 字段 | 类型 | 约束 | 说明 |
|:-----|:-----|:-----|:-----|
| id | bigint | PK, AUTO | 主键 |
| name | varchar(100) | UNIQUE, NOT NULL, INDEX | 食材名称 |
| category | varchar(20) | NOT NULL, INDEX | 食材分类 |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |

**索引**：
- PRIMARY: `id`
- UNIQUE: `name`
- INDEX: `category`

**Django 模型**：`ingredients.models.Ingredient`
- 分类选择：`IngredientCategory.CHOICES` (vegetable/meat/seafood/seasoning/fruit/grain/dairy/other)
- 默认排序：`ordering = ['category', 'name']`

#### recipe_ingredients 表（菜谱-食材关联）✅

| 字段 | 类型 | 约束 | 说明 |
|:-----|:-----|:-----|:-----|
| id | bigint | PK, AUTO | 主键 |
| recipe_id | bigint | NOT NULL, FK, INDEX | 关联 recipes.id |
| ingredient_id | bigint | NOT NULL, FK, INDEX | 关联 ingredients.id |
| amount | varchar(100) | NULL | 用量描述 |
| sort_order | int | NOT NULL, DEFAULT 0 | 排序序号 |
| created_at | datetime(6) | NOT NULL | 创建时间 |

**关系**：
- `recipe_id` → `recipes.id`（ON DELETE CASCADE）
- `ingredient_id` → `ingredients.id`（ON DELETE CASCADE）
- 联合唯一约束：`UNIQUE(recipe_id, ingredient_id)`

**Django 模型**：`recipes.models.RecipeIngredient`

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

#### user_favorites 表（用户收藏）✅

| 字段 | 类型 | 约束 | 说明 |
|:-----|:-----|:-----|:-----|
| id | bigint | PK, AUTO | 主键 |
| user_id | bigint | NOT NULL, FK, INDEX | 关联 users.id |
| recipe_id | bigint | NOT NULL, FK, INDEX | 关联 recipes.id |
| created_at | datetime(6) | NOT NULL, INDEX | 收藏时间 |

**关系**：
- `user_id` → `users.id`（ON DELETE CASCADE）
- `recipe_id` → `recipes.id`（ON DELETE CASCADE）
- 联合唯一约束：`UNIQUE(user_id, recipe_id)`

**索引**：
- PRIMARY: `id`
- INDEX: `user_id` - 用于查询用户的收藏
- INDEX: `recipe_id` - 用于查询收藏该菜谱的用户
- INDEX: `created_at` - 用于按时间排序

**Django 模型**：`favorites.models.UserFavorite`
- 反向关系：`user.favorites`（用户的收藏）、`recipe.favorited_by`（菜谱的收藏者）
- 默认排序：`ordering = ['-created_at']`

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

# 检查用户是否已收藏某菜谱
is_favorited = UserFavorite.objects.filter(user=user, recipe=recipe).exists()
```

**设计说明**：
- 联合唯一约束防止同一用户重复收藏同一菜谱
- 双向外键级联删除，确保数据一致性
- 反向关系命名清晰：`favorites`（用户的收藏）、`favorited_by`（菜谱的收藏者）
- 收藏时间索引支持按时间排序查询

#### categories 表（分类标签）✅

| 字段 | 类型 | 约束 | 说明 |
|:-----|:-----|:-----|:-----|
| id | bigint | PK, AUTO | 主键 |
| name | varchar(50) | NOT NULL | 分类名称 |
| type | varchar(20) | NOT NULL, INDEX | 分类类型（cuisine/scene/crowd/taste） |
| sort_order | int | NOT NULL, DEFAULT 0 | 排序序号 |
| created_at | datetime(6) | NOT NULL | 创建时间 |
| updated_at | datetime(6) | NOT NULL | 更新时间 |

**索引**：
- PRIMARY: `id`
- INDEX: `type`, `sort_order`
- 联合唯一约束：`UNIQUE(type, name)`

**Django 模型**：`categories.models.Category`
- 分类选择：`CategoryType.CHOICES` (cuisine/scene/crowd/taste)
- 默认排序：`ordering = ['type', 'sort_order', 'id']`
- 类方法：
  - `get_by_type(category_type)` - 获取指定类型的所有分类
  - `get_cuisines()` - 获取所有菜系
  - `get_scenes()` - 获取所有场景
  - `get_crowds()` - 获取所有人群
  - `get_tastes()` - 获取所有口味

**初始数据**：
- 八大菜系：川菜、粤菜、鲁菜、苏菜、浙菜、湘菜、徽菜、闽菜
- 场景：早餐、午餐、晚餐、下午茶、夜宵、快手菜、宴客菜
- 人群：儿童、老人、孕妇、健身人群、素食者
- 口味：辣、甜、酸、咸、鲜、清淡、麻

**使用示例**：
```python
from categories.models import Category
from utils.constants import CategoryType

# 获取所有菜系
cuisines = Category.get_cuisines()
for cuisine in cuisines:
    print(f"{cuisine.name}")

# 获取指定类型的分类
scenes = Category.get_by_type(CategoryType.SCENE)

# 创建新分类
new_category = Category.objects.create(
    name='春季时令',
    type=CategoryType.SCENE,
    sort_order=99
)
```

**设计说明**：
- 联合唯一约束确保同一类型下分类名称不重复
- 支持多种分类类型，灵活扩展
- 排序字段支持自定义显示顺序
- 提供便捷的类方法快速获取各类型分类

### 核心关系（完整设计）

```
users (1:1) user_profiles
  │
  ├─ (1:N) user_favorites (N:1) recipes
  │                                    │
  └─ (1:N) user_behavior_logs ────────┘
                                        │
                    ┌───────────────────┼───────────────┐
                    ▼                   ▼               ▼
            recipe_ingredients    recipe_steps    categories
                    │
                    ▼
              ingredients
```

---

## 后端架构

### 项目结构

```
backend/
├── config/                 # Django 主配置
│   ├── __init__.py
│   ├── settings.py        # 项目设置（从 .env 读取环境变量）
│   ├── urls.py            # 主路由配置
│   ├── asgi.py            # ASGI 配置
│   └── wsgi.py            # WSGI 配置
├── utils/                  # 公共工具模块 ✅
│   ├── __init__.py
│   ├── response.py        # 统一响应封装
│   ├── exceptions.py      # 自定义异常
│   ├── pagination.py      # 分页配置
│   └── constants.py       # 常量定义
├── accounts/               # 认证模块 ✅
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── models.py          # User, UserProfile, UserManager
│   ├── serializers.py     # 序列化器（注册验证）
│   ├── views.py           # 视图（注册、登录等）
│   └── urls.py            # 路由配置
├── recipes/                # 菜谱模块 ✅
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_recipeingredient.py
│   ├── models.py          # Recipe, RecipeIngredient 模型
│   └── ...
├── categories/             # 分类模块 ✅
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_seed_initial_categories.py
│   └── models.py          # Category 模型
├── ingredients/            # 食材模块 ✅
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── models.py          # Ingredient 模型
├── mysql_backend/          # PyMySQL 兼容层 ✅
│   ├── __init__.py         # 包初始化
│   └── base.py             # Django 6.0 兼容修复
├── favorites/              # 收藏模块 ✅
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── models.py          # UserFavorite 模型
│   └── admin.py           # Django Admin 配置
├── analytics/              # 数据分析（用户）⏳
├── admin_panel/            # 管理员模块 ⏳
├── behavior_logs/          # 行为日志 ⏳
├── static/                 # 静态文件目录 ✅
├── mediafiles/             # 媒体文件目录 ✅
├── verify_script/          # 验证脚本目录 ✅
│   ├── test_db_connection.py       # 数据库连接测试 ✅
│   ├── verify_user_model.py        # 用户模型验证脚本 ✅
│   ├── verify_recipe_model.py      # 菜谱模型验证脚本 ✅
│   ├── verify_category_model.py    # 分类模型验证脚本 ✅
│   ├── verify_ingredient_models.py # 食材模型验证脚本 ✅
│   ├── verify_favorite_model.py    # 收藏模型验证脚本 ✅
│   └── test_login.py               # 登录接口测试脚本 ✅
├── manage.py               # Django 管理脚本
├── .env                    # 环境变量（本地，不提交）✅
├── .env.example            # 环境变量模板（提交）✅
├── requirements.txt        # Python 依赖列表 ✅
└── README.md               # 后端说明文档 ✅
```

### 环境配置说明

- `.env`：包含敏感配置（SECRET_KEY、数据库密码），通过 python-dotenv 加载
- `.env.example`：不含敏感值的模板，供其他开发者参考
- `settings.py`：使用 `os.getenv()` 读取环境变量，设置合理的默认值

**Django 6.0 + PyMySQL 兼容性处理**：

```python
# settings.py 中的 PyMySQL 配置
import pymysql

# 修复 Django 6.0 版本检查问题
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()
```

**问题**：Django 6.0 要求 MySQLdb 2.2.1+，但 PyMySQL 1.1.2 声称是 1.4.6
**解决方案**：修改 `pymysql.version_info` 绕过版本检查

### 工具模块详细说明 ✅

#### `utils/response.py` - 统一响应封装

```python
class ApiResponse:
    @staticmethod
    def success(data=None, message="操作成功", code=200) -> Response
    @staticmethod
    def error(message, code=400, errors=None, data=None) -> Response
    @staticmethod
    def paginate(data, message="获取成功") -> Response
```

**作用**：
- 统一 API 响应格式：`{ code, message, data }`
- 处理成功和错误响应
- 支持分页响应

#### `utils/exceptions.py` - 自定义异常

```python
class BusinessError(APIException)        # 业务异常基类
class ValidationError(BusinessError)     # 参数验证异常
class NotFoundError(BusinessError)       # 资源不存在异常
class PermissionDeniedError(BusinessError)  # 权限不足异常
class StateNotAllowedError(BusinessError)   # 状态不允许异常
```

**作用**：
- 定义业务相关的异常类型
- 统一异常处理和错误信息

#### `utils/pagination.py` - 分页配置

```python
class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

**作用**：
- 配置标准分页行为
- 默认每页 20 条，最大 100 条

#### `utils/constants.py` - 常量定义

```python
# 用户角色
ROLE_USER = 'user'
ROLE_ADMIN = 'admin'

# 分类类型
CATEGORY_CUISINE = 'cuisine'
CATEGORY_SCENE = 'scene'
CATEGORY_AUDIENCE = 'audience'
CATEGORY_FLAVOR = 'flavor'

# 食材分类
INGREDIENT_CAT_VEGETABLE = 'vegetable'
INGREDIENT_CAT_MEAT = 'meat'
INGREDIENT_CAT_SEAFOOD = 'seafood'
INGREDIENT_CAT_SPICE = 'spice'
# ...

# 行为类型
BEHAVIOR_LOGIN = 'login'
BEHAVIOR_SEARCH = 'search'
BEHAVIOR_VIEW = 'view'
BEHAVIOR_FAVORITE = 'favorite'
```

**作用**：
- 定义系统常量
- 避免硬编码
- 提供类型安全

### 认证模块详细说明 ✅

#### `accounts/serializers.py` - 序列化器

```python
class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    username       # 用户名（3-50字符，必填）
    password        # 密码（至少8位，必填）
    password_confirm # 确认密码（必填）
    email          # 邮箱（可选，唯一）

class LoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username       # 用户名（必填）
    password        # 密码（必填，write_only）
    # 验证：用户名密码验证、账户激活状态检查
    # 返回：验证通过后附加 user 实例到 validated_data

class UserSerializer(serializers.ModelSerializer):
    """用户基础序列化器"""
    # 返回用户基本信息（不含敏感数据）

class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    # 序列化用户资料信息
```

**作用**：
- `RegisterSerializer` - 注册请求数据验证
  - 用户名唯一性检查
  - 邮箱唯一性检查（如提供）
  - 密码强度验证（使用 Django 内置验证器）
  - 两次密码一致性验证
  - 创建用户和用户资料（使用事务）
- `LoginSerializer` - 登录请求数据验证
  - 使用 Django 的 `authenticate()` 验证用户名密码
  - 检查账户是否激活（`is_active`）
  - 验证通过后将 `user` 实例附加到 `validated_data`
- `UserSerializer` - 返回用户基本信息（不含密码）
- `UserProfileSerializer` - 用户资料序列化

#### `accounts/views.py` - 视图

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册接口"""
    # POST /api/accounts/register/

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录接口"""
    # POST /api/accounts/login/
    # 验证用户名密码，生成 JWT Token
    # 更新最后登录时间

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """健康检查接口"""
    # GET /api/accounts/health/
```

**作用**：
- `register` - 处理用户注册请求
  - 验证请求数据
  - 创建用户和用户资料（使用事务确保原子性）
  - 返回用户基本信息
- `login` - 处理用户登录请求
  - 验证用户名和密码（使用 Django 的 `authenticate()`）
  - 更新用户最后登录时间（`last_login`）
  - 生成 JWT Token（access_token 和 refresh_token）
  - 返回 Token 和用户基本信息
- `health_check` - 健康检查，用于测试模块是否正常工作

#### `accounts/urls.py` - 路由

```python
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('health/', views.health_check, name='health_check'),
]
```

**作用**：
- 定义 accounts 模块的 URL 路由
- 通过主路由 `/api/accounts/` 前缀访问

**注册接口请求示例**：
```bash
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "testuser",
  "password": "Test1234",
  "password_confirm": "Test1234",
  "email": "test@example.com"
}
```

**成功响应（201）**：
```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2026-01-30T14:01:48.812786+08:00"
  }
}
```

**错误响应（400）**：
```json
{
  "code": 400,
  "message": "参数验证失败",
  "data": null,
  "errors": {
    "username": ["该用户名已被注册"]
  }
}
```

**登录接口请求示例**：
```bash
POST /api/accounts/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "Test1234"
}
```

**登录成功响应（200）**：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4MjQyMjM4LCJpYXQiOjE3MzgyNDA2MzgsImp0aSI6IjRkZmE5YmJlLWY1NzQtNDNmYS1hMzYxLWU5M2RiM2YzNTdjZCIsInVzZXJfaWQiOjF9.rK6h...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczODMyNjYzOCwiaWF0IjoxNzM4MjQwNjM4LCJqdGkiOiJlYTNhOGJlOS0wZjQyLTRjNDItOWI4ZC1iZjE3NjUzYjYwZTciLCJ1c2VyX2lkIjoxfQ.xyz...",
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "role": "user",
      "is_active": true
    }
  }
}
```

**登录失败响应（400）**：
```json
{
  "code": 400,
  "message": "参数验证失败",
  "data": null,
  "errors": {
    "non_field_errors": ["用户名或密码错误"]
  }
}
```

### API 规范

- **前缀**: `/api/`
- **响应格式**: `{ code, message, data }`
- **分页参数**: `page`, `page_size` (max 100)
- **认证方式**: JWT (24h)
- **路由命名**: `/api/{module}/{resource}/`，自定义动作用 kebab-case

---

## 前端架构

### 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/                    # 源代码
│   ├── router/             # 路由配置 ✅
│   │   └── index.js
│   ├── stores/             # Pinia 状态管理 ✅
│   │   └── user.js
│   ├── views/              # 页面组件 ✅
│   │   └── Home.vue
│   ├── App.vue             # 根组件 ✅
│   ├── main.js             # 主入口 ✅
│   └── style.css           # 全局样式 ✅
├── .env.local              # 环境变量（本地，不提交）✅
├── .env.example            # 环境变量模板（提交）✅
├── index.html              # HTML 入口 ✅
├── vite.config.js          # Vite 配置 ✅
├── tailwind.config.js      # Tailwind 配置 ✅
├── postcss.config.js       # PostCSS 配置 ✅
├── package.json            # 依赖配置 ✅
└── README.md               # 前端说明文档 ✅
```

### 环境配置说明

- `.env.local`：Vite 开发服务器自动加载，变量必须以 `VITE_` 前缀开头
- `.env.example`：不含敏感值的模板
- 环境变量访问：`import.meta.env.VITE_API_BASE_URL`

### 路由设计

```
/                           # 首页
/login, /register           # 认证
/recipes, /recipes/:id      # 菜谱
/favorites                  # 收藏
/analytics                  # 数据概览
/admin/*                    # 管理后台
```

### 核心依赖

| 包名 | 版本 | 用途 |
|:-----|:----:|:-----|
| vue | ^3.5.13 | 前端框架 |
| element-plus | ^2.9.3 | UI 组件库 |
| pinia | ^2.3.0 | 状态管理 |
| vue-router | ^4.5.0 | 路由管理 |
| axios | ^1.7.9 | HTTP 客户端 |
| echarts | ^5.6.0 | 数据可视化 |
| tailwindcss | ^3.4.0 | 原子化 CSS |

---

## 数据脚本架构

```
data-scripts/
├── README.md               # 总体说明文档 ✅
├── test_structure.py       # 目录结构测试脚本 ✅
├── spiders/                # 爬虫脚本
│   ├── README.md           # 爬虫模块说明 ✅
│   ├── website_analysis.md # 目标网站分析报告 ✅
│   ├── request_utils.py    # HTTP请求封装（UA轮换、重试）✅
│   ├── parser_utils.py     # HTML解析工具 ✅
│   ├── xiachufang_spider.py # 下厨房爬虫主脚本 ✅
│   └── test_spider.py      # 测试脚本 ✅
├── cleaning/               # 数据清洗脚本
│   ├── README.md           # 清洗模块说明 ✅
│   ├── clean_recipes.py    # 数据清洗主脚本 ✅
│   └── test_clean.py       # 测试脚本 ✅
├── importing/              # 数据导入脚本
│   └── README.md
├── simulation/             # 用户行为模拟脚本
│   └── README.md
└── output/                 # 数据输出目录 ✅
    ├── test_recipes_simulated.json
    ├── test_cleaned_output.json
    └── cleaning_report.json
```

### 执行流程

爬取数据 → 清洗数据 → 导入数据库 → 模拟行为

### 模块详细说明

#### spiders/ - 爬虫模块

**目标网站**：
- **下厨房** (https://www.xiachufang.com) - 主要目标
- 备选：豆果美食、香哈菜谱、心食谱

**已完成的文件**：

| 文件 | 作用 | 状态 |
|:-----|:-----|:----:|
| `website_analysis.md` | 目标网站结构分析报告 | ✅ |
| `request_utils.py` | HTTP请求工具 | ✅ |
| `parser_utils.py` | HTML解析工具 | ✅ |
| `xiachufang_spider.py` | 主爬虫脚本 | ✅ |
| `test_spider.py` | 测试脚本 | ✅ |

**模块架构**：

```
request_utils.py (HTTP请求层)
    ├─ User-Agent 轮换（10个真实浏览器UA）
    ├─ 自动重试机制（排除429错误）
    ├─ 请求间隔控制（5-10秒）
    └─ 图片下载功能

parser_utils.py (解析层)
    ├─ RecipeParser 类
    ├─ 多CSS选择器备选
    ├─ 智能分析（难度、菜系、口味）
    └─ 数据格式化

xiachufang_spider.py (业务层)
    ├─ XiachufangSpider 类
    ├─ 批量爬取逻辑
    ├─ 进度跟踪
    └─ 数据持久化
```

**request_utils.py - HTTP请求工具**：

```python
class RequestUtils:
    # 10个真实浏览器 User-Agent
    USER_AGENTS = [...]

    # 功能：
    - get() - GET请求（UA轮换、重试、延迟）
    - download_image() - 图片下载
    - _respect_delay() - 请求间隔控制
```

**parser_utils.py - HTML解析工具**：

```python
class RecipeParser:
    # 解析功能：
    - parse_recipe_detail() - 解析菜谱详情
    - parse_recipe_list() - 解析菜谱列表

    # 数据提取：
    - _parse_name() - 菜谱名称
    - _parse_image_url() - 成品图片
    - _parse_ingredients() - 食材列表
    - _parse_steps() - 制作步骤
    - _parse_tips() - 小贴士

    # 智能分析：
    - _analyze_difficulty() - 难度分析
    - _analyze_cuisine() - 菜系识别
    - _analyze_flavors() - 口味提取
    - _estimate_cooking_time() - 时间估算
```

**xiachufang_spider.py - 主爬虫**：

```python
class XiachufangSpider:
    # 主要方法：
    - crawl_by_ids() - 按ID列表爬取
    - crawl_by_range() - 按ID范围爬取
    - crawl_test() - 测试爬取
    - save_data() - 保存JSON
    - download_image() - 图片下载
```

**反爬策略**：

| 策略 | 状态 | 应对措施 |
|:-----|:----:|:---------|
| User-Agent 检测 | ✅ 需要 | UA 轮换（10个真实浏览器UA）|
| IP 限制 | ✅ 严格 | 5-10秒请求间隔，禁用429重试 |
| 登录要求 | ❌ 不需要 | 基础数据可公开访问 |
| 请求频率限制 | ✅ 严格 | 单线程，5-10秒间隔 |

**使用示例**：

```bash
# 测试爬取（10条）
cd data-scripts/spiders
python xiachufang_spider.py

# 或使用测试脚本
python test_spider.py
```

**注意事项**：
- 下厨房网站有严格的反爬限制（429 Too Many Requests）
- 如遇429错误，建议等待30分钟以上或使用代理IP
- 备选方案：使用 `simulation/recipe_data_simulator.py` 生成模拟数据

#### simulation/ - 数据模拟模块

**目的**: 作为爬虫的备选方案，快速生成测试数据

| 文件 | 作用 | 状态 |
|:-----|:-----|:----:|
| `recipe_data_simulator.py` | 菜谱数据模拟器 | ✅ |

**recipe_data_simulator.py 功能**:

```python
class RecipeDataSimulator:
    # 数据配置：
    CUISINE_TYPES = ['川菜', '粤菜', '鲁菜', ...]
    SCENE_TYPES = ['早餐', '午餐', '晚餐', ...]
    DIFFICULTIES = ['easy', 'medium', 'hard']
    FLAVORS = ['辣', '甜', '酸', ...]

    # 主要方法：
    - generate_recipe() - 生成单条菜谱
    - generate_recipes(count) - 批量生成
    - save_data() - 保存JSON
```

**生成逻辑**:
- 随机选择菜系、难度、场景、口味组合
- 3-6种主料 + 2-4种调料
- 根据难度生成3-8步制作步骤
- 模拟点击量（100-50000）和收藏量

**使用方式**:
```bash
cd data-scripts
python simulation/recipe_data_simulator.py
```

**验证状态**: ✅ 已测试通过（2026-01-30）

**数据字段映射**：

| 数据字段 | CSS选择器 | 目标数据库表 |
|:---------|:----------|:-------------|
| 菜谱名称 | `h1.page-title` | `recipes.name` |
| 成品图片 | `.recipe-cover img` | `recipes.image_url` |
| 用料列表 | `.recipe-ingredients` | `recipe_ingredients` |
| 制作步骤 | `.recipe-steps` | `recipes.steps` |
| 小贴士 | `.recipe-tip` | 扩展字段 |

**反爬策略配置**：
- 请求间隔：2-5秒
- User-Agent：真实浏览器UA轮换
- 并发数：1个（单线程）
- 每日请求上限：1000-2000次

**输出格式**：
- 原始数据：JSON文件（按日期/批次命名）
- 图片：下载至 `data-scripts/spiders/images/`
- 元数据：爬取时间、来源网站、成功/失败数量

#### cleaning/ - 数据清洗脚本

**目的**: 清洗和标准化爬取或模拟的菜谱数据

| 文件 | 作用 | 状态 |
|:-----|:-----|:----:|
| `clean_recipes.py` | 数据清洗主脚本 | ✅ |
| `test_clean.py` | 测试脚本 | ✅ |
| `README.md` | 模块说明 | ✅ |

**clean_recipes.py 功能**:

```python
class RecipeCleaner:
    # 清洗功能：
    - clean_recipe() - 清洗单条记录
    - clean_recipes() - 批量清洗
    - _normalize_difficulty() - 难度标准化
    - _normalize_cooking_time() - 时间标准化
    - _normalize_flavor_tags() - 口味标签标准化
    - _normalize_ingredients() - 食材标准化
    - _normalize_steps() - 步骤标准化
    - _is_duplicate() - 重复检测
    - _validate_recipe() - 数据验证
    - _fill_missing_fields() - 缺失字段补全
```

**清洗规则**:

| 数据项 | 清洗规则 |
|:------|:---------|
| 去重 | 基于 `recipe_id` 和菜谱名称 MD5 哈希 |
| 难度 | 中文 → `easy/medium/hard`，默认 `medium` |
| 烹饪时间 | 提取数字 → 分钟整数，默认 30 |
| 菜系 | 不在标准列表 → 默认"家常菜" |
| 场景 | 缺失 → 默认"晚餐" |
| 口味标签 | 逗号分隔字符串 → 列表，过滤无效值 |
| 食材 | 字符串/列表 → 统一字典格式 `[{'name': '...', 'amount': '...'}]` |
| 步骤 | 字符串/列表 → 统一列表格式，自动编号 |
| 图片URL | 验证 HTTP/HTTPS 格式 |

**必填字段验证**:
- 菜谱名称 (name)
- 食材列表 (ingredients) - 至少 1 条
- 制作步骤 (steps) - 至少 1 步

**使用方式**:
```bash
cd data-scripts/cleaning

# 清洗数据（默认使用模拟数据）
python clean_recipes.py

# 指定输入输出文件
python clean_recipes.py input.json output.json

# 运行测试
python test_clean.py
```

**验证状态**: ✅ 已测试通过（2026-01-30）

#### importing/ - 数据导入脚本

**目的**: 将清洗后的菜谱数据导入到数据库中

| 文件 | 作用 | 状态 |
|:-----|:-----|:----:|
| `import_recipes.py` | 数据导入主脚本 | ✅ |
| `test_import.py` | MySQL 版本测试脚本 | ✅ |
| `test_import_sqlite.py` | SQLite 版本测试脚本（快速测试）| ✅ |
| `README.md` | 模块说明文档 | ✅ |

**import_recipes.py 功能**:

```python
class RecipeImporter:
    # 数据导入流程：
    - load_data() - 加载 JSON 数据
    - import_recipes() - 批量导入菜谱
    - get_or_create_ingredient() - 获取或创建食材
    - generate_random_stats() - 生成统计数据
    - print_summary() - 打印导入摘要
    - verify_import() - 验证导入结果
```

**主要功能**:

| 功能 | 说明 |
|:-----|:-----|
| 批量插入 | 使用 Django `bulk_create()` 批量插入数据 |
| 食材自动分类 | 内置 100+ 种食材的分类规则 |
| 统计数据生成 | 点击量 100-50000，收藏量 5%-20% |
| 数据验证 | 检查必填字段，跳过无效记录 |
| 进度显示 | 使用 tqdm 显示实时进度 |
| 错误处理 | 完整的错误统计报告 |

**食材分类规则**:

```python
INGREDIENT_CATEGORY_MAP = {
    # 蔬菜类
    '白菜': 'vegetable', '菠菜': 'vegetable', '土豆': 'vegetable',
    '番茄': 'vegetable', '黄瓜': 'vegetable', '茄子': 'vegetable',
    # 肉类
    '猪肉': 'meat', '牛肉': 'meat', '羊肉': 'meat',
    '鸡肉': 'meat', '鸭肉': 'meat',
    # 海鲜类
    '鱼': 'seafood', '虾': 'seafood', '蟹': 'seafood',
    # 调料类
    '盐': 'seasoning', '糖': 'seasoning', '酱油': 'seasoning',
    '姜': 'seasoning', '蒜': 'seasoning', '葱': 'seasoning',
    # ... 共 100+ 种食材
}
```

**使用方式**:
```bash
cd data-scripts/importing

# 快速测试（推荐）
python test_import_sqlite.py

# 导入清洗后的数据
python import_recipes.py ../output/cleaned_recipes.json

# 导入测试数据
python import_recipes.py ../output/test_cleaned_output.json
```

**验证状态**: ✅ 已测试通过（2026-01-30）

**测试结果**:
```
成功导入 4 条菜谱
创建 8 种食材
建立 8 条食材关联
统计数据生成正确
外键约束正确
```

**架构见解 - Django 6.0 bulk_create 兼容性处理**:

在 Django 6.0 中，`bulk_create()` 方法的行为有所变化。批量插入后返回的对象默认不包含数据库生成的主键 ID，这导致无法直接使用这些对象创建外键关联。

**解决方案**：
```python
# 1. 批量插入菜谱
created_recipes = Recipe.objects.bulk_create(recipes_to_create, batch_size=100)

# 2. 从数据库重新获取带主键的对象
recipe_names = [r.name for r in created_recipes]
recipes_from_db = Recipe.objects.filter(name__in=recipe_names)

# 3. 使用从数据库获取的对象创建外键关联
for recipe in recipes_from_db:
    # recipe.id 现在有值，可以创建外键关联
    RecipeIngredient.objects.create(recipe=recipe, ...)
```

**设计说明**：

| 设计决策 | 理由 |
|:---------|:-----|
| 分批查询重新获取 | 避免 `name__in` 查询过大，保持性能 |
| 使用名称映射 | 菜谱名称唯一，可以作为临时关联键 |
| 食材缓存 | 避免重复查询食材表，提升性能 |
| 统计数据可选保留 | 如果数据中已有统计数据，使用原值 |

**各文件作用**：

| 文件 | 作用 | 关键类/函数 |
|:-----|:-----|:-----------|
| `import_recipes.py` | 主导入脚本 | `RecipeImporter.run()`, `RecipeImporter.import_recipes()` |
| `test_import.py` | MySQL 测试脚本 | `clear_test_data()`, `verify_import_results()` |
| `test_import_sqlite.py` | SQLite 快速测试 | 使用内存数据库快速验证逻辑 |
| `README.md` | 模块文档 | 使用说明、测试结果、注意事项 |

#### simulation/ - 用户行为模拟脚本

生成100+用户、20-100条行为/用户、时间分布过去30天

---

## 部署架构

### 开发环境

- **前端**: Vite (5173) → Django (8000) → MySQL (3307)
- **服务器**: `npm run dev` (5175) + `python manage.py runserver` (8000)

### 生产环境

- **前端**: Nginx → 静态资源
- **后端**: Gunicorn → Django → MySQL

### 环境变量配置

**前端环境变量** (`frontend/.env.local`):
```bash
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000
VITE_APP_TITLE=菜谱数据分析系统
VITE_PAGE_SIZE=20
```

**后端环境变量** (`backend/.env`):
```bash
SECRET_KEY=django-insecure-...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=recipe_analysis_db
DB_USER=root
DB_PASSWORD=yuwen123
DB_HOST=localhost
DB_PORT=3307
LANGUAGE_CODE=zh-hans
TIME_ZONE=Asia/Shanghai
```

**重要说明**：
- `.env` 文件包含敏感信息，已被 `.gitignore` 排除
- 新环境部署时，复制 `.env.example` 并填入实际值
- 生产环境必须修改 `SECRET_KEY` 和 `DEBUG=False`

---

## 权限模型

| 角色 | 权限 |
|:-----|:-----|
| user | 浏览/搜索/收藏菜谱，查看只读统计 |
| admin | 用户管理，菜谱/分类/食材 CRUD，深度分析 |

---

## 数据可视化

### 用户端
- 菜系分布（饼图）
- 难度统计（柱状图）
- 口味偏好（雷达图）
- 食材频率（词云）

### 管理端
- 概览指标
- 趋势图表
- 用户行为分析（DAU/WAU/MAU、转化漏斗）

---

## 性能要求

| 指标 | 目标值 |
|:-----|:------:|
| 搜索响应时间 | < 500ms |
| 详情页加载时间 | < 1s |
| 大盘数据加载时间 | < 2s |
| 并发用户支持 | 100+ |

---

## 开发进度

### 已完成

| 阶段 | 步骤 | 状态 | 完成日期 |
|:----:|:-----|:----:|:--------:|
| 一 | 创建前端项目结构 | ✅ | 2026-01-29 |
| 一 | 创建后端项目结构 | ✅ | 2026-01-29 |
| 一 | 创建数据脚本目录 | ✅ | 2026-01-29 |
| 一 | 配置开发环境 | ✅ | 2026-01-29 |
| 二 | 设计用户表结构 | ✅ | 2026-01-29 |
| 二 | 设计菜谱表结构 | ✅ | 2026-01-29 |
| 二 | 设计食材表与关联表 | ✅ | 2026-01-29 |
| 二 | 设计收藏表结构 | ✅ | 2026-01-29 |
| 二 | 设计用户行为表 | ✅ | 2026-01-29 |
| 二 | 创建分类/标签表 | ✅ | 2026-01-30 |
| 三 | 分析目标网站 | ✅ | 2026-01-30 |
| 三 | 编写数据清洗脚本 | ✅ | 2026-01-30 |

### 阶段三步骤1成果

**网站分析**：
- 下厨房 (xiachufang.com) - 可访问，确定为主要目标
- 美食杰 (meishij.net) - 404不可用

**爬虫环境准备**：
- 依赖已安装：requests, beautifulsoup4, lxml, pandas
- 分析文档已创建：`data-scripts/spiders/website_analysis.md`

**数据字段映射已明确**：
- 菜谱名称 → `recipes.name`
- 成品图片 → `recipes.image_url`
- 用料列表 → `recipe_ingredients`
- 制作步骤 → `recipes.steps`

### 待完成

详见 `memory-bank/implementation-plan.md` 和 `memory-bank/progress.md`

---

## 重要文档

| 文档 | 路径 | 用途 |
|:-----|:-----|:-----|
| 架构设计 | `memory-bank/architecture.md` | 本文档 |
| 产品需求 | `memory-bank/PRD.md` | PRD 文档 |
| 实施计划 | `memory-bank/implementation-plan.md` | 22阶段实施计划 |
| 开发进度 | `memory-bank/progress.md` | 详细进度记录 |
| 后端规范 | `memory-bank/dev-standards/backend-api-standards.md` | 后端开发标准 |
| 项目指导 | `CLAUDE.md` | AI 开发指导 |
