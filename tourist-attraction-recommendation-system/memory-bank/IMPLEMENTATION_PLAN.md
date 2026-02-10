# 旅游景点推荐系统 - 详细实施计划

> 本文档为 AI 开发者提供逐步实施说明，采用**后端优先**策略：完成后端开发 -> 提供接口文档 -> 开发前端。

---

## 开发原则

1. **不重复造轮子**：优先使用 Django、DRF、Element Plus、ECharts 等成熟框架
2. **小步快跑**：每个步骤都包含测试验证
3. **中文优先**：模型字段、API 响应使用中文命名
4. **先完成再完美**：确保基础功能可用后再优化

---

## 项目结构规划

```
tourist-attraction-recommendation-system/
├── backend/                    # Django 后端
│   ├── manage.py
│   ├── requirements.txt
│   ├── tourist/                # Django 项目配置
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/                   # 应用模块
│   │   ├── accounts/           # 账号管理
│   │   ├── attractions/        # 景点管理
│   │   ├── comments/           # 评论评分
│   │   ├── recommendations/    # 推荐算法
│   │   ├── notifications/      # 消息通知
│   │   └── statistics/         # 数据统计
│   ├── media/                  # 媒体文件
│   └── sql/                    # 数据库脚本
└── frontend/                   # Vue 3 前端
    ├── src/
    │   ├── api/                # API 接口
    │   ├── components/         # 组件
    │   ├── views/              # 页面
    │   ├── router/             # 路由
    │   └── stores/             # Pinia 状态管理
    └── package.json
```

---

## 阶段一：后端开发（Django + DRF）

### 模块 1.1 - 项目初始化

#### 步骤 1.1.1：创建 Django 项目
- 在项目根目录创建 `backend` 文件夹
- 在 `backend` 文件夹内执行 `django-admin startproject tourist .`
- 验证：运行 `python manage.py runserver`，访问 http://127.0.0.1:8000 看到 Django 欢迎页面

#### 步骤 1.1.2：配置数据库
- 修改 `tourist/settings.py`，配置 MySQL 数据库连接：
  - 数据库名：`tourist_attraction_db`
  - 字符集：`utf8mb4`
  - 引擎：`InnoDB`
- 创建 MySQL 数据库：`CREATE DATABASE tourist_attraction_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
- 验证：运行 `python manage.py migrate`，数据库中生成 Django 默认表

#### 步骤 1.1.3：安装核心依赖
- 创建 `requirements.txt`，包含：
  - `Django==5.2`
  - `djangorestframework`
  - `djangorestframework-simplejwt`
  - `mysqlclient`
  - `Pillow`（图片处理）
  - `django-cors-headers`（跨域）
  - `django-filter`（过滤）
- 执行 `pip install -r requirements.txt`
- 验证：`pip list` 显示所有包已安装

#### 步骤 1.1.4：配置 DRF 和 CORS
- 在 `settings.py` 的 `INSTALLED_APPS` 中添加：
  - `'rest_framework'`
  - `'rest_framework_simplejwt'`
  - `'corsheaders'`
  - `'django_filters'`
- 配置 CORS 允许的前端域名
- 验证：重启服务，无报错

---

### 模块 1.2 - 账号管理应用（accounts）

#### 步骤 1.2.1：创建应用
- 执行 `python manage.py startapp accounts`
- 在 `apps` 文件夹下创建 `accounts` 应用
- 在 `settings.py` 的 `INSTALLED_APPS` 中添加 `'accounts'`
- 验证：应用成功创建，`apps/accounts/` 目录存在

#### 步骤 1.2.2：设计用户模型
- 在 `accounts/models.py` 创建 `UserProfile` 模型，包含字段：
  - `username`（用户名，唯一）
  - `password`（密码，明文存储）
  - `real_name`（真实姓名）
  - `phone`（手机号）
  - `email`（邮箱）
  - `role`（角色：ADMIN/USER）
  - `is_active`（是否启用）
  - `is_deleted`（是否删除，逻辑删除）
  - `created_at`（创建时间）
  - `updated_at`（更新时间）
- 验证：执行 `python manage.py makemigrations` 和 `python manage.py migrate`，数据库生成表

#### 步骤 1.2.3：创建序列化器
- 在 `accounts/serializers.py` 创建：
  - `UserRegisterSerializer`：注册序列化器
  - `UserLoginSerializer`：登录序列化器
  - `UserProfileSerializer`：用户信息序列化器
  - `UserUpdateSerializer`：用户更新序列化器
  - `ChangePasswordSerializer`：修改密码序列化器
- 验证：导入序列化器无语法错误

#### 步骤 1.2.4：实现注册接口
- 在 `accounts/views.py` 创建 `RegisterView`：
  - POST 方法，接收用户名、密码、真实姓名、手机号、邮箱
  - 验证用户名唯一性
  - 创建用户，默认角色为 USER
  - 返回用户信息
- 配置 URL：`/api/accounts/register/`
- 验证：
  - 使用 Postman 发送 POST 请求，成功创建用户
  - 重复用户名注册，返回错误提示

#### 步骤 1.2.5：实现登录接口
- 在 `accounts/views.py` 创建 `LoginView`：
  - POST 方法，接收用户名、密码
  - 验证用户名密码是否正确
  - 验证用户是否被禁用或删除
  - 生成 JWT Token（Access: 2小时，Refresh: 7天）
  - 返回 Token 和用户信息
- 配置 URL：`/api/accounts/login/`
- 验证：
  - 正确用户名密码登录，返回 Token
  - 错误密码返回错误提示
  - 被禁用用户无法登录

#### 步骤 1.2.6：实现个人信息接口
- 在 `accounts/views.py` 创建 `UserProfileView`：
  - GET 方法：获取当前登录用户信息
  - PUT 方法：更新当前用户信息
- 配置 URL：`/api/accounts/profile/`
- 添加 JWT 认证
- 验证：
  - 携带 Token 访问，返回用户信息
  - 未携带 Token 返回 401

#### 步骤 1.2.7：实现修改密码接口
- 在 `accounts/views.py` 创建 `ChangePasswordView`：
  - POST 方法，接收旧密码、新密码
  - 验证旧密码正确性
  - 更新密码
- 配置 URL：`/api/accounts/change-password/`
- 验证：旧密码正确可修改，错误返回提示

#### 步骤 1.2.8：实现账号注销接口
- 在 `accounts/views.py` 创建 `DeleteAccountView`：
  - DELETE 方法，逻辑删除当前用户
  - 设置 `is_deleted=True`
- 配置 URL：`/api/accounts/delete-account/`
- 验证：注销后用户无法登录

---

### 模块 1.3 - 景点管理应用（attractions）

#### 步骤 1.3.1：创建应用
- 执行 `python manage.py startapp attractions`
- 在 `settings.py` 的 `INSTALLED_APPS` 中添加 `'attractions'`
- 验证：应用成功创建

#### 步骤 1.3.2：设计景点模型
- 在 `attractions/models.py` 创建 `Attraction` 模型，包含字段：
  - `name`（景点名称）
  - `description`（景点简介）
  - `address`（地址）
  - `category`（类别：自然风光/人文古迹/主题乐园/其他）
  - `region`（地区）
  - `opening_hours`（开放时间）
  - `cover_image`（封面图）
  - `images`（轮播图，JSON 数组）
  - `view_count`（浏览量）
  - `is_deleted`（是否删除）
  - `created_at`（创建时间）
  - `updated_at`（更新时间）
- 验证：执行迁移，数据库生成表

#### 步骤 1.3.3：创建景点序列化器
- 在 `attractions/serializers.py` 创建：
  - `AttractionListSerializer`：列表序列化器（简化字段）
  - `AttractionDetailSerializer`：详情序列化器（完整字段）
  - `AttractionCreateUpdateSerializer`：创建/更新序列化器
- 验证：导入序列化器无语法错误

#### 步骤 1.3.4：实现景点列表接口
- 在 `attractions/views.py` 创建 `AttractionListView`：
  - GET 方法：返回景点分页列表
  - 支持按名称搜索、按类别筛选、按地区筛选
  - 按创建时间倒序排列
- 配置 URL：`/api/attractions/`
- 验证：
  - 访问接口返回景点列表
  - 搜索功能正常
  - 筛选功能正常

#### 步骤 1.3.5：实现景点详情接口
- 在 `attractions/views.py` 创建 `AttractionDetailView`：
  - GET 方法：返回景点详细信息
  - 每次访问增加 `view_count`
- 配置 URL：`/api/attractions/{id}/`
- 验证：访问详情页，浏览量增加

#### 步骤 1.3.6：实现景点创建接口
- 在 `attractions/views.py` 创建 `AttractionCreateView`：
  - POST 方法：创建新景点
  - 仅管理员可访问
  - 支持图片上传
- 配置 URL：`/api/attractions/create/`
- 添加管理员权限验证
- 验证：
  - 管理员可创建景点
  - 普通用户访问返回 403

#### 步骤 1.3.7：实现景点更新接口
- 在 `attractions/views.py` 创建 `AttractionUpdateView`：
  - PUT/PATCH 方法：更新景点信息
  - 仅管理员可访问
- 配置 URL：`/api/attractions/{id}/update/`
- 验证：管理员可更新景点

#### 步骤 1.3.8：实现景点删除接口
- 在 `attractions/views.py` 创建 `AttractionDeleteView`：
  - DELETE 方法：删除景点（逻辑删除）
  - 仅管理员可访问
- 配置 URL：`/api/attractions/{id}/delete/`
- 验证：管理员可删除景点

#### 步骤 1.3.9：实现景点搜索接口
- 在 `attractions/views.py` 创建 `AttractionSearchView`：
  - GET 方法：关键词搜索
  - 支持景点名称、简介模糊搜索
- 配置 URL：`/api/attractions/search/`
- 验证：搜索功能正常

---

### 模块 1.4 - 评论评分应用（comments）

#### 步骤 1.4.1：创建应用
- 执行 `python manage.py startapp comments`
- 在 `settings.py` 的 `INSTALLED_APPS` 中添加 `'comments'`
- 验证：应用成功创建

#### 步骤 1.4.2：设计评论模型
- 在 `comments/models.py` 创建 `Comment` 模型，包含字段：
  - `user`（用户，外键）
  - `attraction`（景点，外键）
  - `content`（评论内容）
  - `rating`（评分，1-5 分）
  - `status`（状态：PENDING/APPROVED/REJECTED）
  - `is_deleted`（是否删除）
  - `created_at`（创建时间）
- 验证：执行迁移，数据库生成表

#### 步骤 1.4.3：设计收藏模型
- 在 `comments/models.py` 创建 `Favorite` 模型，包含字段：
  - `user`（用户，外键）
  - `attraction`（景点，外键）
  - `created_at`（创建时间）
  - 联合唯一约束：user + attraction
- 验证：执行迁移，数据库生成表

#### 步骤 1.4.4：创建评论序列化器
- 在 `comments/serializers.py` 创建：
  - `CommentSerializer`：评论序列化器
  - `CommentCreateSerializer`：评论创建序列化器
  - `FavoriteSerializer`：收藏序列化器
- 验证：导入序列化器无语法错误

#### 步骤 1.4.5：实现发表评论接口
- 在 `comments/views.py` 创建 `CommentCreateView`：
  - POST 方法：发表评论和评分
  - 需要登录
  - 默认状态为 PENDING（待审核）
- 配置 URL：`/api/comments/create/`
- 验证：
  - 登录用户可发表评论
  - 未登录返回 401

#### 步骤 1.4.6：实现景点评论列表接口
- 在 `comments/views.py` 创建 `CommentListView`：
  - GET 方法：获取指定景点的评论列表
  - 只返回状态为 APPROVED 的评论
  - 按创建时间倒序
- 配置 URL：`/api/comments/attraction/{attraction_id}/`
- 验证：只显示已审核通过的评论

#### 步骤 1.4.7：实现我的评论接口
- 在 `comments/views.py` 创建 `MyCommentsView`：
  - GET 方法：获取当前用户的所有评论
  - 需要登录
- 配置 URL：`/api/comments/my/`
- 验证：返回当前用户的评论

#### 步骤 1.4.8：实现删除评论接口
- 在 `comments/views.py` 创建 `CommentDeleteView`：
  - DELETE 方法：删除评论
  - 用户只能删除自己的评论
- 配置 URL：`/api/comments/{id}/delete/`
- 验证：用户可删除自己的评论

#### 步骤 1.4.9：实现管理员评论审核接口
- 在 `comments/views.py` 创建 `CommentReviewView`：
  - PUT 方法：审核评论（通过/驳回）
  - 仅管理员可访问
- 配置 URL：`/api/comments/{id}/review/`
- 验证：
  - 管理员可审核评论
  - 审核后评论状态更新

#### 步骤 1.4.10：实现收藏接口
- 在 `comments/views.py` 创建 `FavoriteView`：
  - POST 方法：添加收藏
  - DELETE 方法：取消收藏
  - GET 方法：获取收藏列表
- 配置 URL：`/api/favorites/`
- 验证：
  - 可添加/取消收藏
  - 重复添加返回错误

#### 步骤 1.4.11：实现我的收藏接口
- 在 `comments/views.py` 创建 `MyFavoritesView`：
  - GET 方法：获取当前用户的收藏列表
  - 需要登录
- 配置 URL：`/api/favorites/my/`
- 验证：返回当前用户的收藏

#### 步骤 1.4.12：实现取消收藏接口
- 在 `comments/views.py` 创建 `FavoriteDeleteView`：
  - DELETE 方法：取消指定收藏
  - 需要登录
- 配置 URL：`/api/favorites/{id}/delete/`
- 验证：可取消收藏

---

### 模块 1.5 - 消息通知应用（notifications）

#### 步骤 1.5.1：创建应用
- 执行 `python manage.py startapp notifications`
- 在 `settings.py` 的 `INSTALLED_APPS` 中添加 `'notifications'`
- 验证：应用成功创建

#### 步骤 1.5.2：设计通知模型
- 在 `notifications/models.py` 创建 `Notification` 模型，包含字段：
  - `title`（标题）
  - `content`（内容）
  - `type`（类型：SYSTEM/ANNOUNCEMENT/COMMENT）
  - `user`（用户，外键，为空表示全员通知）
  - `is_read`（是否已读）
  - `is_deleted`（是否删除）
  - `created_at`（创建时间）
- 验证：执行迁移，数据库生成表

#### 步骤 1.5.3：创建通知序列化器
- 在 `notifications/serializers.py` 创建：
  - `NotificationSerializer`：通知序列化器
  - `NotificationCreateSerializer`：通知创建序列化器
- 验证：导入序列化器无语法错误

#### 步骤 1.5.4：实现我的通知接口
- 在 `notifications/views.py` 创建 `MyNotificationsView`：
  - GET 方法：获取当前用户的通知列表
  - 包括全员通知和用户专属通知
  - 按创建时间倒序
- 配置 URL：`/api/notifications/my/`
- 验证：返回当前用户的通知

#### 步骤 1.5.5：实现标记已读接口
- 在 `notifications/views.py` 创建 `MarkReadView`：
  - PUT 方法：标记通知为已读
  - 支持单个标记和全部标记
- 配置 URL：`/api/notifications/{id}/read/`
- 验证：通知标记为已读

#### 步骤 1.5.6：实现管理员发布公告接口
- 在 `notifications/views.py` 创建 `AnnouncementCreateView`：
  - POST 方法：创建全员公告
  - 仅管理员可访问
  - `user` 字段为空
- 配置 URL：`/api/notifications/announcement/create/`
- 验证：
  - 管理员可发布公告
  - 所有用户都能看到

#### 步骤 1.5.7：实现管理员通知管理接口
- 在 `notifications/views.py` 创建 `NotificationManageView`：
  - GET 方法：获取所有通知（管理员）
  - PUT 方法：更新通知
  - DELETE 方法：删除通知
- 配置 URL：`/api/notifications/manage/`
- 验证：管理员可管理所有通知

---

### 模块 1.6 - 数据统计应用（statistics）

#### 步骤 1.6.1：创建应用
- 执行 `python manage.py startapp statistics`
- 在 `settings.py` 的 `INSTALLED_APPS` 中添加 `'statistics'`
- 验证：应用成功创建

#### 步骤 1.6.2：实现景点热度统计
- 在 `statistics/views.py` 创建 `AttractionHotView`：
  - GET 方法：返回景点热度排行
  - 热度公式：`热度值 = (浏览量 * 0.2) + (评论数 * 0.3) + (平均评分 * 浏览量 * 0.5)`
  - 返回 TOP 10
- 配置 URL：`/api/statistics/hot/`
- 验证：返回按热度排序的景点列表

#### 步骤 1.6.3：实现月度数据统计
- 在 `statistics/views.py` 创建 `MonthlyReportView`：
  - GET 方法：返回月度数据报告
  - 统计：新增用户数、景点浏览总量、新增评论数
  - 按月份分组
- 配置 URL：`/api/statistics/monthly/`
- 验证：返回月度统计数据

#### 步骤 1.6.4：实现数据看板接口
- 在 `statistics/views.py` 创建 `DashboardView`：
  - GET 方法：返回看板数据汇总
  - 包括：总用户数、总景点数、总评论数、本月新增用户
- 配置 URL：`/api/statistics/dashboard/`
- 验证：返回看板数据

#### 步骤 1.6.5：实现用户管理列表接口
- 在 `statistics/views.py` 创建 `UserManageView`：
  - GET 方法：返回所有用户列表
  - 支持分页
  - 仅管理员可访问
- 配置 URL：`/api/statistics/users/`
- 验证：管理员可查看用户列表

#### 步骤 1.6.6：实现用户禁用/启用接口
- 在 `statistics/views.py` 创建 `UserStatusView`：
  - PUT 方法：启用/禁用用户
  - 仅管理员可访问
- 配置 URL：`/api/statistics/users/{id}/status/`
- 验证：管理员可修改用户状态

---

### 模块 1.7 - 推荐算法应用（recommendations）

#### 步骤 1.7.1：创建应用
- 执行 `python manage.py startapp recommendations`
- 在 `settings.py` 的 `INSTALLED_APPS` 中添加 `'recommendations'`
- 验证：应用成功创建

#### 步骤 1.7.2：实现热门景点推荐
- 在 `recommendations/views.py` 创建 `PopularRecommendationsView`：
  - GET 方法：返回热门景点
  - 用于冷启动（新用户）
  - 基于热度值排序
- 配置 URL：`/api/recommendations/popular/`
- 验证：返回热门景点列表

#### 步骤 1.7.3：实现个性化推荐
- 在 `recommendations/views.py` 创建 `PersonalizedRecommendationsView`：
  - GET 方法：返回个性化推荐
  - 基于用户历史浏览、收藏、评分数据
  - 简单实现：推荐用户收藏过景点的同类景点
- 配置 URL：`/api/recommendations/personalized/`
- 验证：
  - 登录用户返回个性化推荐
  - 未登录用户返回热门推荐

#### 步骤 1.7.4：实现相似景点推荐
- 在 `recommendations/views.py` 创建 `SimilarRecommendationsView`：
  - GET 方法：返回与指定景点相似的景点
  - 基于类别和地区推荐
- 配置 URL：`/api/recommendations/similar/{attraction_id}/`
- 验证：返回相似景点列表

---

### 模块 1.8 - 初始化数据

#### 步骤 1.8.1：创建初始化 SQL 脚本
- 在 `backend/sql/` 创建 `init_db.sql`
- 包含：
  - 管理员账号（用户名：admin，密码：admin123）
  - 测试用户账号（用户名：user，密码：user123）
  - 示例景点数据（至少 10 条）
  - 示例分类和地区数据
- 验证：执行 SQL 脚本，数据成功导入

#### 步骤 1.8.2：创建媒体文件目录
- 在 `backend/` 创建 `media/attractions/` 目录
- 放入示例景点图片
- 配置 `settings.py` 的 `MEDIA_URL` 和 `MEDIA_ROOT`
- 验证：图片可通过 URL 访问

---

### 模块 1.9 - 接口文档生成

#### 步骤 1.9.1：安装 drf-spectacular
- 在 `requirements.txt` 添加 `drf-spectacular`
- 在 `settings.py` 配置：
  - `INSTALLED_APPS` 添加 `'drf_spectacular'`
  - `REST_FRAMEWORK` 配置默认 schema
- 验证：安装成功

#### 步骤 1.9.2：配置 Schema
- 在 `settings.py` 添加：
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
  }
  ```
- 验证：配置生效

#### 步骤 1.9.3：生成接口文档
- 配置 URL：`/api/schema/` 和 `/api/docs/`
- 访问 http://127.0.0.1:8000/api/docs/ 查看 Swagger 文档
- 验证：所有接口文档显示正常

#### 步骤 1.9.4：导出接口文档
- 执行 `python manage.py spectacular --color --file schema.yml`
- 将文档导出到项目 `docs/` 目录
- 验证：文档文件生成

---

## 阶段二：前端开发（Vue 3 + Element Plus）

### 模块 2.1 - 项目初始化

#### 步骤 2.1.1：创建 Vue 项目
- 在项目根目录执行 `npm create vue@latest frontend`
- 选择：Vue 3、TypeScript、Pinia、Vue Router
- 验证：`npm run dev` 启动成功

#### 步骤 2.1.2：安装依赖
- 安装核心依赖：
  - `element-plus`（UI 组件库）
  - `echarts`（图表库）
  - `axios`（HTTP 客户端）
  - `@element-plus/icons-vue`（图标库）
  - `tailwindcss`（样式库，可选）
- 执行 `npm install`
- 验证：所有包安装成功

#### 步骤 2.1.3：配置 Element Plus
- 在 `main.js` 全局引入 Element Plus
- 引入样式文件
- 注册图标组件
- 验证：Element Plus 组件可用

#### 步骤 2.1.4：配置 Axios
- 在 `src/api/` 创建 `request.js`
- 配置基础 URL：`http://127.0.0.1:8000/api`
- 配置请求拦截器：添加 JWT Token
- 配置响应拦截器：处理错误
- 验证：请求可正常发送

#### 步骤 2.1.5：配置路由
- 在 `src/router/` 配置路由：
  - 管理端路由：`/admin/*`
  - 用户端路由：`/*`
  - 登录路由：`/login`、`/register`
- 配置路由守卫：验证登录状态
- 验证：路由跳转正常

#### 步骤 2.1.6：配置 Pinia Store
- 在 `src/stores/` 创建：
  - `user.js`：用户信息 store
  - `token.js`：Token store
- 配置持久化存储
- 验证：Store 数据可正常读写

---

### 模块 2.2 - 公共组件开发

#### 步骤 2.2.1：创建布局组件
- 在 `src/components/` 创建：
  - `AdminLayout.vue`：管理端布局（顶部导航 + 侧边栏）
  - `UserLayout.vue`：用户端布局（顶部导航 + 底部）
- 验证：布局组件可正常显示

#### 步骤 2.2.2：创建景点卡片组件
- 创建 `AttractionCard.vue`：
  - 显示景点图片、名称、简介、评分
  - 点击跳转详情页
- 验证：卡片组件正常显示

#### 步骤 2.2.3：创建评论组件
- 创建 `CommentItem.vue`：
  - 显示用户头像、昵称、评论内容、评分、时间
  - 支持删除（自己的评论）
- 验证：评论组件正常显示

#### 步骤 2.2.4：创建分页组件
- 使用 Element Plus 的 `el-pagination`
- 封装为 `Pagination.vue`
- 验证：分页功能正常

---

### 模块 2.3 - 用户端页面开发

#### 步骤 2.3.1：登录/注册页面
- 创建 `views/auth/Login.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 表单：用户名、密码
  - 登录成功后跳转
- 创建 `views/auth/Register.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 表单：用户名、密码、确认密码、真实姓名、手机号、邮箱
  - 表单验证：用户名唯一性、密码强度
- 验证：
  - 登录功能正常
  - 注册功能正常
  - 表单验证生效

#### 步骤 2.3.2：首页
- 创建 `views/user/Home.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 个性化推荐模块（调用 `/api/recommendations/personalized/`）
  - 热门景点展示（调用 `/api/statistics/hot/`）
  - 搜索入口
- 验证：
  - 推荐数据正常显示
  - 热门景点正常显示

#### 步骤 2.3.3：景点列表页
- 创建 `views/user/AttractionList.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 筛选：类别、地区
  - 搜索：关键词搜索
  - 列表展示：使用 `AttractionCard` 组件
  - 分页
- 验证：
  - 筛选功能正常
  - 搜索功能正常
  - 分页功能正常

#### 步骤 2.3.4：景点详情页
- 创建 `views/user/AttractionDetail.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 显示：景点图片、名称、简介、地址、开放时间
  - 评论列表：显示所有评论
  - 发表评论：登录用户可评论
  - 收藏按钮：登录用户可收藏
  - 相似景点推荐
- 验证：
  - 详情信息正常显示
  - 评论功能正常
  - 收藏功能正常

#### 步骤 2.3.5：个人中心页
- 创建 `views/user/UserCenter.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 显示：用户信息
  - 编辑：真实姓名、手机号、邮箱
  - 修改密码：旧密码、新密码、确认密码
- 验证：
  - 信息显示正常
  - 编辑功能正常
  - 修改密码功能正常

#### 步骤 2.3.6：我的收藏页
- 创建 `views/user/MyFavorites.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 列表显示收藏的景点
  - 取消收藏按钮
- 验证：
  - 收藏列表正常显示
  - 取消收藏功能正常

#### 步骤 2.3.7：我的评论页
- 创建 `views/user/MyComments.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 列表显示我的评论
  - 删除评论按钮
- 验证：
  - 评论列表正常显示
  - 删除功能正常

#### 步骤 2.3.8：消息中心页
- 创建 `views/user/Notifications.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 列表显示通知
  - 标记已读功能
  - 删除通知功能
- 验证：
  - 通知列表正常显示
  - 标记已读功能正常

---

### 模块 2.4 - 管理端页面开发

#### 步骤 2.4.1：管理员登录页面
- 创建 `views/admin/AdminLogin.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 与用户登录类似，但跳转到管理端
- 验证：管理员登录后跳转到管理端首页

#### 步骤 2.4.2：数据看板页
- 创建 `views/admin/Dashboard.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 统计卡片：总用户数、总景点数、总评论数、本月新增
  - 图表：月度数据报告（ECharts）
  - 热门景点排行
- 验证：
  - 统计数据正常显示
  - 图表正常显示

#### 步骤 2.4.3：用户管理页
- 创建 `views/admin/UserManage.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 用户列表：分页显示
  - 操作：启用/禁用按钮
  - 搜索：用户名搜索
- 验证：
  - 用户列表正常显示
  - 启用/禁用功能正常

#### 步骤 2.4.4：景点列表管理页
- 创建 `views/admin/AttractionManage.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 景点列表：分页显示
  - 筛选：类别、地区
  - 搜索：景点名称
  - 操作：编辑、删除
  - 新增按钮
- 验证：
  - 列表正常显示
  - 筛选搜索功能正常
  - 编辑删除功能正常

#### 步骤 2.4.5：景点编辑/新增页
- 创建 `views/admin/AttractionEdit.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 表单：名称、类别、地区、地址、开放时间、简介
  - 图片上传：封面图、轮播图
  - 表单验证
- 验证：
  - 新增景点成功
  - 编辑景点成功
  - 图片上传成功

#### 步骤 2.4.6：评论审核管理页
- 创建 `views/admin/CommentReview.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 评论列表：分页显示
  - 筛选：审核状态
  - 操作：通过、驳回
- 验证：
  - 评论列表正常显示
  - 审核功能正常

#### 步骤 2.4.7：公告管理页
- 创建 `views/admin/AnnouncementManage.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 公告列表：分页显示
  - 操作：编辑、删除
  - 新增按钮
- 验证：
  - 公告列表正常显示
  - 新增编辑删除功能正常

#### 步骤 2.4.8：个人设置页
- 创建 `views/admin/AdminSettings.vue`：
  - 使用 `frontend-design` skill 设计美观界面
  - 显示：管理员信息
  - 编辑：真实姓名、手机号、邮箱
  - 修改密码
- 验证：
  - 信息显示正常
  - 编辑功能正常
  - 修改密码功能正常

---

### 模块 2.5 - API 集成层

#### 步骤 2.5.1：创建账号相关 API
- 在 `src/api/` 创建 `auth.js`：
  - `login(data)`：登录
  - `register(data)`：注册
  - `getUserInfo()`：获取用户信息
  - `updateUserInfo(data)`：更新用户信息
  - `changePassword(data)`：修改密码
  - `deleteAccount()`：删除账号
- 验证：所有 API 可正常调用

#### 步骤 2.5.2：创建景点相关 API
- 在 `src/api/` 创建 `attractions.js`：
  - `getAttractionList(params)`：获取景点列表
  - `getAttractionDetail(id)`：获取景点详情
  - `createAttraction(data)`：创建景点
  - `updateAttraction(id, data)`：更新景点
  - `deleteAttraction(id)`：删除景点
  - `searchAttractions(keyword)`：搜索景点
- 验证：所有 API 可正常调用

#### 步骤 2.5.3：创建评论相关 API
- 在 `src/api/` 创建 `comments.js`：
  - `createComment(data)`：发表评论
  - `getCommentList(attractionId)`：获取评论列表
  - `getMyComments()`：获取我的评论
  - `deleteComment(id)`：删除评论
  - `reviewComment(id, data)`：审核评论
- 验证：所有 API 可正常调用

#### 步骤 2.5.4：创建收藏相关 API
- 在 `src/api/` 创建 `favorites.js`：
  - `addFavorite(attractionId)`：添加收藏
  - `removeFavorite(id)`：取消收藏
  - `getMyFavorites()`：获取我的收藏
- 验证：所有 API 可正常调用

#### 步骤 2.5.5：创建通知相关 API
- 在 `src/api/` 创建 `notifications.js`：
  - `getMyNotifications()`：获取我的通知
  - `markAsRead(id)`：标记已读
  - `deleteNotification(id)`：删除通知
  - `createAnnouncement(data)`：发布公告
  - `getAnnouncementList()`：获取公告列表
- 验证：所有 API 可正常调用

#### 步骤 2.5.6：创建统计相关 API
- 在 `src/api/` 创建 `statistics.js`：
  - `getDashboard()`：获取看板数据
  - `getHotAttractions()`：获取热门景点
  - `getMonthlyReport()`：获取月度报告
  - `getUserList(params)`：获取用户列表
  - `updateUserStatus(id, data)`：更新用户状态
- 验证：所有 API 可正常调用

#### 步骤 2.5.7：创建推荐相关 API
- 在 `src/api/` 创建 `recommendations.js`：
  - `getPopularRecommendations()`：获取热门推荐
  - `getPersonalizedRecommendations()`：获取个性化推荐
  - `getSimilarRecommendations(attractionId)`：获取相似推荐
- 验证：所有 API 可正常调用

---

## 阶段三：测试与部署

### 模块 3.1 - 后端测试

#### 步骤 3.1.1：接口测试
- 使用 Postman 测试所有接口
- 验证：
  - 请求参数正确
  - 响应格式正确
  - 错误处理正确
- 验证：所有接口测试通过

#### 步骤 3.1.2：权限测试
- 测试不同角色的权限
- 验证：
  - 未登录无法访问需要登录的接口
  - 普通用户无法访问管理员接口
- 验证：权限控制正确

---

### 模块 3.2 - 前端测试

#### 步骤 3.2.1：功能测试
- 手动测试所有页面功能
- 验证：
  - 所有按钮可点击
  - 所有表单可提交
  - 所有数据正确显示
- 验证：所有功能正常

#### 步骤 3.2.2：兼容性测试
- 在不同浏览器测试
- 验证：
  - Chrome 正常
  - Edge 正常
  - Firefox 正常
- 验证：浏览器兼容性良好

---

### 模块 3.3 - 性能优化

#### 步骤 3.3.1：前端优化
- 使用 Vue DevTools 检查性能
- 优化：图片懒加载、列表虚拟滚动
- 验证：页面加载速度 < 2 秒

#### 步骤 3.3.2：后端优化
- 添加数据库索引
- 优化查询语句
- 验证：接口响应时间 < 500ms

---

### 模块 3.4 - 部署准备

#### 步骤 3.4.1：后端打包
- 修改 `settings.py` 的 `DEBUG=False`
- 配置 `ALLOWED_HOSTS`
- 收集静态文件：`python manage.py collectstatic`
- 验证：生产环境配置正确

#### 步骤 3.4.2：前端打包
- 执行 `npm run build`
- 检查 `dist/` 目录
- 验证：打包成功

#### 步骤 3.4.3：部署文档
- 创建部署文档 `docs/DEPLOYMENT.md`
- 包含：
  - 环境要求
  - 安装步骤
  - 配置说明
  - 启动命令
- 验证：文档完整

---

## 附录

### A. 开发环境要求
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Git

### B. 推荐使用 VS Code 插件
- Python
- Vue Language Features (Volar)
- ESLint
- Prettier

### C. 代码规范
- 后端：遵循 PEP 8
- 前端：遵循 ESLint 配置
- 提交信息：遵循约定式提交规范

---

**最后更新时间：2026-02-10**
