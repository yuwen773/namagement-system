# 食堂管理系统 - 开发进度记录

> 本文档记录开发过程中的已完成工作，供未来开发者参考

---

## 2026-01-27

### ✅ 步骤 1.1：创建后端 Django 项目

**实施内容**：

1. **项目初始化**
   - 创建了 `backend/` 目录作为后端项目根目录
   - 使用 `django-admin startproject config .` 创建 Django 项目
   - 项目名称为 `config`（Django 项目配置目录）

2. **创建 Django 应用**
   - `accounts` - 用户账号与认证
   - `employees` - 员工档案管理
   - `schedules` - 排班管理
   - `attendance` - 考勤管理
   - `leaves` - 请假管理
   - `salaries` - 薪资管理
   - `analytics` - 统计分析（注意：原计划使用 `statistics`，但与 Python 内置模块冲突，故改为 `analytics`）

3. **依赖配置** (`requirements.txt`)
   - django>=5.2
   - djangorestframework
   - mysqlclient
   - django-cors-headers

4. **数据库配置** (`config/settings.py`)
   - 数据库类型：MySQL
   - 主机：127.0.0.1
   - 端口：3307
   - 数据库名：canteen_management
   - 用户：root
   - 密码：yuwen123

5. **应用注册**
   - 将所有本地应用添加到 `INSTALLED_APPS`
   - 添加 `rest_framework` 和 `corsheaders` 第三方应用

6. **CORS 配置**
   - 添加 `corsheaders.middleware.CorsMiddleware` 到 `MIDDLEWARE`
   - 配置 `CORS_ALLOWED_ORIGINS` 允许前端跨域访问（http://127.0.0.1:5173, http://localhost:5173）

7. **静态文件和媒体文件配置**
   - 创建 `static/` 和 `media/` 目录
   - 配置 `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS`
   - 配置 `MEDIA_URL`, `MEDIA_ROOT`

**测试验证**：
- ✅ `python manage.py runserver` - 服务器启动成功
- ✅ `python manage.py makemigrations` - 无错误
- ✅ `python manage.py migrate` - 所有迁移成功应用
- ✅ `python manage.py showmigrations` - 所有应用迁移状态正常
- ✅ 访问 http://127.0.0.1:8000/ - 服务器响应正常

**注意事项**：
- 数据库 `canteen_management` 需要预先在 MySQL 中创建
- 开发阶段密码采用明文存储（根据需求文档）
- `analytics` 应用对应实施计划中的 `statistics` 模块

### ✅ 步骤 1.2：创建前端 Vue 项目

**实施内容**：

1. **项目初始化**
   - 使用 Vite 创建了 Vue 3 项目，项目目录为 `frontend/`
   - 使用 `npm create vite@latest frontend -- --template vue` 命令

2. **安装依赖**
   - 默认依赖：Vue 3 (^3.5.24)、Vite (^7.2.4)
   - 额外依赖已安装：
     - `element-plus` ^2.13.1 - UI 组件库
     - `echarts` ^6.0.0 - 数据可视化图表库
     - `axios` ^1.13.3 - HTTP 客户端
     - `vue-router` ^4.6.4 - 路由管理
     - `pinia` ^3.0.4 - 状态管理

3. **配置 Vite** (`vite.config.js`)
   - 添加服务器代理配置
   - 将 `/api` 请求代理到后端 `http://127.0.0.1:8000`
   - 设置 `changeOrigin: true` 以正确处理跨域

4. **创建目录结构**
   ```
   src/
   ├── views/
   │   ├── admin/      # 管理员端页面
   │   ├── employee/   # 员工端页面
   │   └── auth/       # 认证相关页面（登录/注册）
   ├── components/     # 公共组件
   ├── api/            # API 请求封装
   ├── router/         # Vue Router 配置
   └── stores/         # Pinia 状态管理
   ```

5. **测试热更新**
   - 修改 `App.vue` 添加测试文字，验证 Vite 热更新功能正常

**测试验证**：
- ✅ `npm run dev` - 开发服务器启动成功（运行在 http://localhost:5173/）
- ✅ 访问开发服务器地址 - 看到 Vue 欢迎页面
- ✅ 修改 `App.vue` 添加测试文字 - 热更新正常工作

**注意事项**：
- Vite 默认端口为 5173，如果被占用会自动尝试其他端口
- 开发服务器运行时，修改代码会自动触发热更新
- API 代理配置确保前端 `/api` 请求正确转发到后端

- 注意事项：
- Vite 默认端口为 5173，如果被占用会自动尝试其他端口
- 开发服务器运行时，修改代码会自动触发热更新
- API 代理配置确保前端 `/api` 请求正确转发到后端

---

### ✅ 步骤 2.1：创建用户账号模型与 API

**实施内容**：

1. **创建 User 模型** (`accounts/models.py`)
   - 字段定义：
     - `username` - 登录账号（唯一）
     - `password` - 登录密码（开发阶段明文存储）
     - `employee_id` - 关联员工档案ID（可选，外键）
     - `role` - 角色类型（ADMIN/EMPLOYEE）
     - `status` - 账号状态（ENABLED/DISABLED）
     - `created_at`, `updated_at` - 时间戳
   - 枚举类定义：`Role` 和 `Status` 使用 Django 的 `TextChoices`
   - 自定义方法：`verify_password()` 用于验证用户名和密码

2. **创建序列化器** (`accounts/serializers.py`)
   - `LoginSerializer` - 登录请求验证（username, password 必填）
   - `RegisterSerializer` - 注册请求验证（包含用户名唯一性检查）
   - `UserSerializer` - 用户详情序列化（支持 CRUD 操作）
   - `UserListSerializer` - 用户列表序列化（简化版，用于列表展示）

3. **创建视图集** (`accounts/views.py`)
   - `UserViewSet` - 基于 DRF 的 `ModelViewSet`
   - 自定义 action：
     - `login/` - 用户登录接口
     - `register/` - 用户注册接口（默认角色为 EMPLOYEE）
   - 标准 CRUD 操作：list, retrieve, create, update, destroy
   - 统一的响应格式：`{code, message, data}`

4. **配置 URL 路由**
   - 创建 `accounts/urls.py` - 使用 DRF 的 `DefaultRouter`
   - 更新 `config/urls.py` - 包含 accounts 路由：`/api/accounts/`

5. **注册 Django Admin** (`accounts/admin.py`)
   - 配置 `UserAdmin` 类
   - 列表显示字段：id, username, role, status, employee_id, created_at
   - 过滤器：role, status, created_at
   - 搜索字段：username, id
   - 分组字段展示：基本信息、角色与状态、时间信息

6. **数据库迁移**
   - 创建迁移：`accounts/migrations/0001_initial.py`
   - 应用迁移到数据库

**API 端点清单**：
```
POST   /api/accounts/register/   # 用户注册
POST   /api/accounts/login/      # 用户登录
GET    /api/accounts/            # 用户列表
GET    /api/accounts/{id}/       # 用户详情
POST   /api/accounts/            # 创建用户（管理员）
PUT    /api/accounts/{id}/       # 更新用户
DELETE /api/accounts/{id}/       # 删除用户
```

**测试验证**：
- ✅ 注册新用户 - 返回 201，用户创建成功，默认角色为 EMPLOYEE
- ✅ 登录验证（正确凭证）- 返回 200，获取用户信息
- ✅ 登录验证（错误密码）- 返回 401，提示"用户名或密码错误"
- ✅ 重复用户名注册 - 返回 400，提示"用户名已存在"
- ✅ 获取用户列表 - 返回 200，显示所有用户
- ✅ 获取用户详情 - 返回 200，显示完整用户信息

**注意事项**：
- 密码开发阶段采用明文存储，生产环境需改用哈希加密
- `employee_id` 外键将在步骤 2.2 创建员工档案模型后建立关联
- 权限验证待后续实现（目前所有用户都可访问管理接口）

---

## 待完成

- [ ] 步骤 2.2：创建员工档案模型与 API
- [ ] 步骤 2.3：创建排班相关模型与 API
- [ ] 步骤 2.4：创建考勤模型与 API
- [ ] 步骤 2.5：创建请假模型与 API
- [ ] 步骤 2.6：创建薪资模型与 API
- [ ] 步骤 2.7：创建统计分析接口
- [ ] ...（详见 IMPLEMENTATION_PLAN.md）
