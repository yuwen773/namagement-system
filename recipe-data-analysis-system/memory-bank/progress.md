# 菜谱数据分析系统 - 实施进度

> 更新日期: 2026-01-30

---

## 进度概览

| 阶段 | 名称 | 进度 |
|:----:|:------|:----:|
| 阶段一 | 项目初始化与基础架构 | 4/4 ✅ |
| 阶段二 | 数据库设计与模型创建 | 6/6 ✅ |
| 阶段三 | 数据准备与导入 | 4/6 ⏳ |
| 阶段四 | 用户认证与权限系统 | 3/7 ⏳ |

---

## 阶段一：项目初始化与基础架构 ✅

| 步骤 | 任务 | 日期 |
|:----:|:------|:----:|
| 1.1 | 创建前端项目结构 | 2026-01-29 |
| 1.2 | 创建后端项目结构 | 2026-01-29 |
| 1.3 | 创建数据脚本目录 | 2026-01-29 |
| 1.4 | 配置开发环境 | 2026-01-29 |

---

## 阶段二：数据库设计与模型创建 ✅

| 步骤 | 任务 | 状态 | 日期 |
|:----:|:------|:----:|:----:|
| 2.1 | 设计用户表结构 | ✅ | 2026-01-29 |
| 2.2 | 设计菜谱表结构 | ✅ | 2026-01-29 |
| 2.3 | 设计食材表与关联表 | ✅ | 2026-01-29 |
| 2.4 | 设计收藏表结构 | ✅ | 2026-01-29 |
| 2.5 | 设计用户行为表 | ✅ | 2026-01-29 |
| 2.6 | 创建分类/标签表 | ✅ | 2026-01-30 |

---

## 阶段三：数据准备与导入 ⏳

| 步骤 | 任务 | 状态 | 日期 |
|:----:|:------|:----:|:----:|
| 3.1 | 分析目标网站 | ✅ | 2026-01-30 |
| 3.2 | 编写菜谱爬取脚本 | ✅ 已验证 | 2026-01-30 |
| 3.3 | 编写数据清洗脚本 | ✅ 已验证 | 2026-01-30 |
| 3.4 | 编写数据导入脚本 | ✅ 已验证 | 2026-01-30 |
| 3.5 | 执行完整爬取并导入 | ⏳ | - |
| 3.6 | 模拟用户行为数据 | ⏳ | - |

### 阶段三步骤2完成总结

#### 创建的文件

| 文件 | 作用 |
|:-----|:-----|
| `data-scripts/spiders/request_utils.py` | HTTP请求工具（UA轮换、重试机制、Session管理）|
| `data-scripts/spiders/parser_utils.py` | HTML解析工具（菜谱名称、食材、步骤、难度分析）|
| `data-scripts/spiders/xiachufang_spider.py` | 下厨房爬虫主脚本 |
| `data-scripts/spiders/test_spider.py` | 简单测试脚本 |
| `data-scripts/simulation/recipe_data_simulator.py` | 数据模拟器（备选方案）|

#### 爬虫功能

**HTTP请求工具 (`request_utils.py`)**：
- 真实浏览器 User-Agent 轮换（10个UA）
- 自动重试机制（可配置重试次数和延迟）
- 请求间隔控制（5-10秒，避免触发反爬）
- Session 管理
- 图片下载功能
- Windows 控制台编码修复

**HTML解析工具 (`parser_utils.py`)**：
- 解析菜谱名称、图片URL、食材列表、制作步骤
- 智能分析难度等级（基于步骤和食材数量）
- 菜系识别（基于菜谱名称关键词）
- 口味标签提取
- 烹饪时间估算
- 多CSS选择器备选方案

**主爬虫脚本 (`xiachufang_spider.py`)**：
- 按ID范围批量爬取
- 进度显示和统计
- 定期保存数据
- 图片下载和本地存储
- 测试模式支持

#### 反爬策略

| 策略 | 状态 | 应对措施 |
|:-----|:----:|:---------|
| User-Agent 检测 | ✅ 需要 | UA 轮换（10个真实浏览器UA）|
| IP 限制 | ✅ 严格 | 5-10秒请求间隔，禁用429重试 |
| 登录要求 | ❌ 不需要 | 基础数据可公开访问 |
| 请求频率限制 | ✅ 严格 | 单线程，5-10秒间隔 |

#### 备选方案

由于下厨房网站有严格的反爬限制（429错误），创建了**数据模拟器**作为备选方案：

| 功能 | 说明 |
|:-----|:-----|
| 随机菜谱生成 | 支持自定义菜系、难度、场景、口味 |
| 食材生成 | 3-6种主料 + 2-4种调料 |
| 步骤生成 | 基于难度生成3-8步制作步骤 |
| 统计数据 | 模拟点击量（100-50000）和收藏量 |

**使用模拟器**：
```bash
cd data-scripts
python simulation/recipe_data_simulator.py
```

**使用爬虫**（需要等待IP解封或使用代理）：
```bash
cd data-scripts/spiders
python xiachufang_spider.py
```

#### 测试结果

**模拟器测试**：✅ 成功生成100条测试数据
**爬虫测试**：⚠️ 受限（429错误），需要：
- 等待IP解封（建议等待30分钟以上）
- 或使用代理IP池
- 或直接使用模拟数据继续开发

#### 验证结果（2026-01-30）

**用户验证**：✅ **测试通过**

- 数据模拟器运行正常
- 生成的数据格式正确
- 可以继续进行下一步（数据清洗脚本）

### 阶段三步骤3完成总结

#### 创建的文件

| 文件 | 作用 |
|:-----|:-----|
| `data-scripts/cleaning/clean_recipes.py` | 数据清洗主脚本 |
| `data-scripts/cleaning/test_clean.py` | 测试脚本 |

#### 清洗脚本功能

**`clean_recipes.py`** 包含以下清洗功能：

1. **去重处理**
   - 基于 `recipe_id` 去重
   - 基于菜谱名称 MD5 哈希去重

2. **缺失字段补全**
   - 菜系缺失 → 默认"家常菜"
   - 场景缺失 → 默认"晚餐"
   - 难度缺失 → 默认"medium"
   - 烹饪时间缺失 → 默认30分钟
   - 统计数据缺失 → 默认0

3. **格式标准化**
   - 难度：中文 → `easy/medium/hard`
   - 烹饪时间：提取数字 → 分钟整数
   - 口味标签：字符串 → 列表，过滤无效值
   - 食材：字符串/列表 → 统一字典格式
   - 步骤：自动添加编号

4. **数据验证**
   - 必填字段检查（名称、食材、步骤）
   - 无效记录过滤

#### 测试结果

```
原始数据: 8 条
清洗后数据: 4 条
去除重复: 2 条
无效记录: 2 条

验证项：
✅ 去重检测
✅ 必填字段
✅ 难度标准化
✅ 时间格式
✅ 食材格式
```

#### 使用方式

```bash
# 清洗模拟数据
cd data-scripts/cleaning
python clean_recipes.py ../output/test_recipes_simulated.json ../output/cleaned_recipes.json

# 清洗爬虫数据
python clean_recipes.py ../output/test_recipes.json ../output/cleaned_recipes.json

# 运行测试
python test_clean.py
```

#### 验证结果（2026-01-30）

**用户验证**：✅ **测试通过**

- 所有验证项通过
- 可以继续进行下一步（数据导入脚本）

#### 数据格式

生成的 JSON 数据包含以下字段：
```json
{
  "recipe_id": 1,
  "name": "菜谱名称",
  "cuisine_type": "菜系",
  "scene_type": "场景",
  "difficulty": "easy/medium/hard",
  "cooking_time": 30,
  "flavor_tags": ["辣", "甜"],
  "image_url": "图片URL",
  "ingredients": [{"name": "食材名", "amount": "用量"}],
  "steps": ["步骤1", "步骤2"],
  "tips": "小贴士",
  "view_count": 1000,
  "favorite_count": 100
}
```

### 阶段三步骤4完成总结

#### 创建的文件

| 文件 | 作用 |
|:-----|:-----|
| `data-scripts/importing/import_recipes.py` | 数据导入主脚本 |
| `data-scripts/importing/test_import.py` | MySQL 版本测试脚本 |
| `data-scripts/importing/test_import_sqlite.py` | SQLite 版本测试脚本（快速测试）|

#### 导入脚本功能

**`import_recipes.py`** 包含以下功能：

1. **批量插入优化**
   - 使用 Django `bulk_create()` 批量插入数据
   - 默认批次大小 100，可配置
   - 使用事务确保数据一致性

2. **食材自动分类**
   - 内置 100+ 种常见食材的分类规则
   - 根据食材名称自动识别分类（蔬菜/肉类/海鲜/调料等）
   - 新食材自动创建并分类

3. **统计数据生成**
   - 点击量：100-50000 随机数
   - 收藏量：点击量的 5%-20%
   - 难度分布：简单 40%、中等 40%、困难 20%
   - 保留数据中已有的统计数据

4. **数据验证**
   - 检查必填字段（菜谱名称、食材信息）
   - 跳过无效记录并记录错误
   - 完整的错误统计报告

5. **进度显示**
   - 使用 tqdm 显示实时进度条
   - 数据加载、处理、导入各阶段进度

#### 食材分类规则

| 分类 | 示例食材 |
|:-----|:--------|
| 蔬菜 (vegetable) | 白菜、菠菜、土豆、番茄、黄瓜、茄子、辣椒、豆腐 |
| 肉类 (meat) | 猪肉、牛肉、羊肉、鸡肉、鸭肉、火腿、鸡蛋 |
| 海鲜 (seafood) | 鱼、虾、蟹、海参、鱿鱼、海带 |
| 调料 (seasoning) | 盐、糖、酱油、醋、料酒、姜、蒜、葱 |
| 谷物 (grain) | 米、面、面条、粉丝 |
| 水果 (fruit) | 苹果、香蕉、梨、橙、葡萄 |
| 乳制品 (dairy) | 牛奶、酸奶、奶酪、黄油 |

#### 测试结果

**测试环境**：SQLite 内存数据库

```
============================================================
数据导入测试 (SQLite 版本)
============================================================
创建数据库表...
✓ 数据库表创建完成

加载测试数据...
✓ 加载 4 条菜谱数据

导入菜谱数据...
✓ 成功插入 4 条菜谱

处理食材关联...
✓ 成功创建 8 条食材关联

数据统计:
  菜谱总数:   4
  食材总数:   8
  食材关联数: 8

随机菜谱验证:
  名称:       宫保鸡丁
  菜系:       川菜
  难度:       中等
  点击量:     1000
  收藏量:     100
  食材数量:   2
  食材列表:
    - 鸡肉 (300g)
    - 花生 (50g)
```

#### 验证结果（2026-01-30）

**SQLite 版本测试**：✅ **测试通过**

**MySQL 版本测试**：✅ **用户验证通过**

用户验证结果：
```
============================================================
[OK] 所有验证通过！导入功能正常
============================================================

数据统计:
  菜谱总数:   4
  食材总数:   8
  食材关联数: 8

验证项:
  [OK] 菜谱数据存在 (4 条)
  [OK] 食材关联正确 (4/4 条菜谱有食材)
  [OK] 统计数据已生成 (4 条)
  [OK] 难度字段正确
  [OK] 食材分类已设置
  [OK] 外键约束已设置
  [OK] 收藏量比例合理 (10.0%)
```

- 数据加载功能正常
- 菜谱批量插入功能正常
- 食材自动分类功能正常
- 食材关联创建功能正常
- 统计数据生成功能正常
- 外键约束正确
- 可以继续进行下一步（执行完整数据导入）

#### 使用方式

```bash
cd data-scripts/importing

# 快速测试（推荐）
python test_import_sqlite.py

# 导入清洗后的数据
python import_recipes.py ../output/cleaned_recipes.json

# 导入测试数据
python import_recipes.py ../output/test_cleaned_output.json
```

### 阶段三步骤1完成总结

#### 目标网站选择

| 网站 | URL | 状态 | 结论 |
|:-----|:----|:----:|:-----|
| 下厨房 | https://www.xiachufang.com | ✅ 可访问 | 主要爬取目标 |
| 美食杰 | https://www.meishij.net | ❌ 404 | 不可用 |

#### 网站结构分析成果

**URL 格式**：
- 菜谱详情页：`https://www.xiachufang.com/recipe/{recipe_id}/`
- 分类页：`https://www.xiachufang.com/category/`

**关键数据字段与选择器映射**：

| 字段 | CSS选择器 | 数据库映射 |
|:-----|:----------|:-----------|
| 菜谱名称 | `h1.page-title` | `recipes.name` |
| 成品图片 | `.recipe-cover img` | `recipes.image_url` |
| 用料列表 | `.recipe-ingredients` | `recipe_ingredients` |
| 制作步骤 | `.recipe-steps` | `recipes.steps` |
| 小贴士 | `.recipe-tip` | 额外提示 |

#### 反爬策略分析

| 策略 | 状态 | 应对措施 |
|:-----|:----:|:---------|
| User-Agent 检测 | ✅ 需要 | UA 轮换 |
| IP 限制 | ⚠️ 可能存在 | 2-5秒请求间隔 |
| 登录要求 | ❌ 不需要 | 基础数据可公开访问 |

#### 环境准备

已安装依赖：
- `requests` - HTTP 请求
- `beautifulsoup4` - HTML 解析
- `lxml` - 高性能解析器
- `pandas` - 数据处理

#### 已创建文件

| 文件 | 作用 |
|:-----|:-----|
| `data-scripts/spiders/website_analysis.md` | 完整的网站分析报告（9章节） |

---

## 待完成任务

### 阶段三剩余步骤
- [ ] 编写菜谱爬取脚本
- [ ] 编写数据清洗脚本
- [ ] 编写数据导入脚本
- [ ] 执行完整爬取并导入
- [ ] 模拟用户行为数据

---

## 数据库表状态

| 表名 | 状态 |
|:-----|:----:|
| users | ✅ |
| user_profiles | ✅ |
| recipes | ✅ |
| ingredients | ✅ |
| recipe_ingredients | ✅ |
| user_favorites | ✅ |
| user_behavior_logs | ✅ |
| categories | ✅ |

---

## 阶段二完成总结

### 已创建的文件

| 文件 | 作用 |
|:-----|:-----|
| `backend/categories/models.py` | Category 模型定义 |
| `backend/categories/migrations/0001_initial.py` | 创建 categories 表的迁移 |
| `backend/categories/migrations/0002_seed_initial_categories.py` | 插入初始分类数据（27条） |
| `backend/verify_category_model_sqlite.py` | SQLite 验证脚本 |

### 初始分类数据

| 类型 | 数量 | 内容 |
|:-----|:----:|:-----|
| 菜系 | 8 | 川菜、粤菜、鲁菜、苏菜、浙菜、湘菜、徽菜、闽菜 |
| 场景 | 7 | 早餐、午餐、晚餐、下午茶、夜宵、快手菜、宴客菜 |
| 人群 | 5 | 儿童、老人、孕妇、健身人群、素食者 |
| 口味 | 7 | 辣、甜、酸、咸、鲜、清淡、麻 |

---

---

## 阶段四：用户认证与权限系统 ⏳

| 步骤 | 任务 | 状态 | 日期 |
|:----:|:------|:----:|:----:|
| 4.1 | 实现用户注册接口 | ✅ 已验证 | 2026-01-30 |
| 4.2 | 实现用户登录接口 | ✅ 已验证 | 2026-01-30 |
| 4.3 | 实现 Token 验证中间件 | ✅ 待测试 | 2026-01-30 |
| 4.4 | 实现获取当前用户信息接口 | ⏳ | - |
| 4.5 | 实现更新用户信息接口 | ⏳ | - |
| 4.6 | 实现修改密码接口 | ⏳ | - |
| 4.7 | 实现角色权限控制 | ⏳ | - |

### 阶段四步骤1完成总结

#### 创建的文件

| 文件 | 作用 |
|:-----|:-----|
| `backend/accounts/serializers.py` | 注册序列化器（验证规则）|
| `backend/accounts/views.py` | 注册视图（含健康检查）|
| `backend/accounts/urls.py` | 路由配置 |

#### 修改的文件

| 文件 | 变更 |
|:-----|:-----|
| `backend/config/urls.py` | 添加 accounts 路由 |

#### 注册接口功能

**接口信息**：
- 路由：`POST /api/accounts/register/`
- 功能：用户注册

**验证规则**：
| 字段 | 验证规则 |
|:-----|:---------|
| username | 必填，3-50字符，唯一 |
| password | 必填，至少8位，密码强度验证 |
| password_confirm | 必填，需与 password 一致 |
| email | 可选，需符合邮箱格式，唯一 |

**注册流程**：
1. 验证请求数据格式
2. 检查用户名唯一性
3. 检查邮箱唯一性（如提供）
4. 验证密码强度
5. 验证两次密码一致性
6. 使用事务创建用户和用户资料
7. 返回用户基本信息

#### 测试结果

| 测试场景 | 结果 |
|:--------|:----:|
| 有效数据注册 | ✅ 成功返回 201 |
| 重复用户名 | ✅ 正确拒绝（用户名已被注册）|
| 弱密码（<8位）| ✅ 正确拒绝（密码至少8个字符）|
| 两次密码不一致 | ✅ 正确拒绝（两次输入的密码不一致）|
| 邮箱格式错误 | ✅ 正确拒绝（邮箱格式不正确）|
| 用户名太短（<3位）| ✅ 正确拒绝（用户名至少需要3个字符）|
| 健康检查接口 | ✅ 正常返回 |

#### 使用方式

```bash
# 启动开发服务器
cd backend
python manage.py runserver 8000

# 注册新用户
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test1234",
    "password_confirm": "Test1234",
    "email": "test@example.com"
  }'
```

#### 响应格式

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

#### 验证结果（2026-01-30）

**用户验证**：✅ **测试通过**

- 所有验证场景测试通过
- 数据库正确创建用户和用户资料
- 返回格式符合后端 API 规范
- 可以继续进行下一步（用户登录接口）

### 阶段四步骤2完成总结

#### 创建的文件

| 文件 | 作用 |
|:-----|:-----|
| `backend/accounts/serializers.py` | 添加 `LoginSerializer`（验证用户名、密码）|
| `backend/accounts/views.py` | 添加 `login` 视图（JWT Token 生成、更新最后登录时间）|
| `backend/accounts/urls.py` | 添加 `/api/accounts/login/` 路由 |
| `backend/verify_script/test_login.py` | 登录测试脚本 |

#### 修改的文件

| 文件 | 变更 |
|:-----|:-----|
| `backend/accounts/serializers.py` | 添加 `LoginSerializer` 类 |
| `backend/accounts/views.py` | 添加 `login` 函数视图 |
| `backend/accounts/urls.py` | 添加 `login/` 路由 |

#### 登录接口功能

**接口信息**：
- 路由：`POST /api/accounts/login/`
- 功能：用户登录并获取 JWT Token

**请求参数**：
| 字段 | 类型 | 必填 | 说明 |
|:-----|:----:|:----:|:-----|
| username | string | ✅ | 用户名 |
| password | string | ✅ | 密码 |

**登录流程**：
1. 验证请求数据格式（用户名、密码必填）
2. 使用 Django 的 `authenticate()` 验证用户名和密码
3. 检查账户是否激活
4. 更新用户最后登录时间
5. 生成 JWT Token（access_token 和 refresh_token）
6. 返回 Token 和用户基本信息

**成功响应（200）**：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "...",
    "user": {
      "id": 1,
      "username": "testuser_login",
      "email": "testlogin@example.com",
      "role": "user",
      "is_active": true
    }
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
    "non_field_errors": ["用户名或密码错误"]
  }
}
```

#### 测试结果

| 测试场景 | 结果 |
|:--------|:----:|
| 正确密码登录 | ✅ 成功返回 200 和 Token |
| 错误密码登录 | ✅ 正确拒绝（用户名或密码错误）|
| 不存在用户登录 | ✅ 正确拒绝（用户名或密码错误）|
| 未激活用户登录 | ✅ 正确拒绝（该账户已被禁用）|
| 缺少必填字段 | ✅ 正确拒绝（参数验证失败）|

**测试输出**：
```
============================================================
用户登录接口测试
============================================================
创建测试用户...
  ✓ 创建 2 个测试用户

[测试] 正确的用户名密码登录...
  ✓ 登录成功
  ✓ Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ✓ 用户名: testuser_login
  ✓ 角色: user
  ✓ 邮箱: testlogin@example.com
  ✓ 最后登录时间已更新: 2026-01-30 06:37:18.428977+00:00

[测试] 错误的用户名密码登录...
  ✓ 正确拒绝登录
  ✓ 消息: 参数验证失败

[测试] 不存在的用户登录...
  ✓ 正确拒绝登录
  ✓ 消息: 参数验证失败

[测试] 未激活用户登录...
  ✓ 正确拒绝登录
  ✓ 消息: 参数验证失败

[测试] 缺少必填字段...
  ✓ 正确拒绝（缺少密码）
  ✓ 正确拒绝（缺少用户名）

============================================================
测试结果汇总
============================================================
  ✓ PASS  正确密码登录
  ✓ PASS  错误密码登录
  ✓ PASS  不存在用户登录
  ✓ PASS  未激活用户登录
  ✓ PASS  缺少必填字段

总计: 5 通过, 0 失败

============================================================
[OK] 所有测试通过！登录功能正常
============================================================
```

#### 使用方式

```bash
# 启动开发服务器
cd backend
python manage.py runserver 8000

# 用户登录
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test1234"
  }'
```

#### 运行测试

```bash
cd backend
python verify_script/test_login.py
```

#### 验证结果（2026-01-30）

**用户验证**：✅ **测试通过**

- 所有验证场景测试通过（5/5）
- JWT Token 正确生成
- 最后登录时间正确更新
- 返回格式符合后端 API 规范
- 可以继续进行下一步（Token 验证中间件）

### 阶段四步骤3完成总结

#### 创建的文件

| 文件 | 作用 |
|:-----|:-----|
| `backend/accounts/authentication.py` | JWT 认证类 |
| `backend/verify_script/test_auth_middleware.py` | 认证中间件测试脚本 |

#### 修改的文件

| 文件 | 变更 |
|:-----|:-----|
| `backend/config/settings.py` | 添加 `DEFAULT_AUTHENTICATION_CLASSES` 配置 |
| `backend/accounts/views.py` | 添加 `me` 视图（获取当前用户信息）|
| `backend/accounts/urls.py` | 添加 `/api/accounts/me/` 路由 |

#### JWT 认证类功能

**`authentication.py` - JWTAuthentication 类**：

**认证流程**：
1. 从 `Authorization` 请求头中提取 Token
2. 验证 Token 格式（需以 `Bearer ` 开头）
3. 使用 `rest_framework_simplejwt` 解析并验证 Token
4. 返回认证用户

**错误处理**：
| 场景 | HTTP 状态码 | 错误消息 |
|:-----|:----------:|:---------|
| 未提供 Token | - | 返回 `None`（允许匿名访问）|
| Token 格式错误 | 401 | 无效的 Token 请求头 |
| Token 无效/过期 | 401 | Token 无效或已过期 |
| 用户不存在 | 401 | 用户不存在 |
| 用户已禁用 | 401 | 该用户已被禁用 |

**使用方式**：

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    # request.user 包含当前认证用户
    user = request.user
    ...
```

**请求头格式**：
```
Authorization: Bearer <access_token>
```

#### 获取当前用户信息接口

**接口信息**：
- 路由：`GET /api/accounts/me/`
- 权限：需要认证（`IsAuthenticated`）

**成功响应（200）**：
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2026-01-30T12:00:00Z"
  }
}
```

**错误响应（401）**：
```json
{
  "code": 401,
  "message": "未提供有效的认证凭据"
}
```

#### 运行测试

```bash
# 启动开发服务器
cd backend
python manage.py runserver 8000

# 在另一个终端运行测试
python verify_script/test_auth_middleware.py
```

#### 测试场景

| 测试场景 | 预期结果 |
|:--------|:---------|
| 有效 Token 访问受保护接口 | ✅ 返回 200 和用户信息 |
| 无 Token 访问受保护接口 | ✅ 返回 401 |
| 无效 Token 访问受保护接口 | ✅ 返回 401 |
| 错误的 Token 格式（缺少 Bearer） | ✅ 返回 401 |
| 已禁用用户访问 | ✅ 返回 401 |

#### 验证结果（2026-01-30）

**状态**：⏳ **待用户测试验证**

**测试前准备**：
1. 确保开发服务器正在运行（`python manage.py runserver 8000`）
2. 运行测试脚本：`python verify_script/test_auth_middleware.py`

**预期测试结果**：
```
============================================================
JWT 认证中间件测试
============================================================
测试服务器: http://localhost:8000

创建测试用户...
  ✓ 创建测试用户: auth_test_user
  ✓ 用户已激活

获取 JWT Token...
  → Access Token: eyJ0eXAiOiJKV1QiLCJhbGc...
  → Refresh Token: eyJ0eXAiOiJKV1QiLCJhbGc...

开始测试...

[测试] 有效 Token 访问受保护接口
  ✓ 请求成功
  → 用户名: auth_test_user
  → 邮箱: authtest@example.com
  → 角色: user

[测试] 无 Token 访问受保护接口
  ✓ 正确拒绝访问 (401)

[测试] 无效 Token 访问受保护接口
  ✓ 正确拒绝访问 (401)

[测试] 错误的 Token 格式
  ✓ 正确拒绝访问 (401) - 缺少 Bearer 前缀

[测试] 已禁用用户访问
  ✓ 正确拒绝访问 (401) - 用户已禁用

测试结果汇总
  ✓ PASS  有效 Token
  ✓ PASS  无 Token
  ✓ PASS  无效 Token
  ✓ PASS  错误 Token 格式
  ✓ PASS  已禁用用户

总计: 5 通过, 0 失败

============================================================
[OK] 所有测试通过！认证中间件功能正常
============================================================
```

---

## 备注

- 详细工作记录请查看 `project-status.md`
- 实施计划请查看 `implementation-plan.md`
