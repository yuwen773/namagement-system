# 食堂管理系统 - 架构文档

> 本文档说明项目架构和各文件作用，供开发者理解系统结构

---

## 项目总体结构

```
canteen-management-system/
├── backend/               # Django 后端项目
│   ├── config/           # Django 项目配置（settings、urls、wsgi 等）
│   ├── accounts/         # 用户账号与认证模块
│   ├── employees/        # 员工档案管理模块
│   ├── schedules/        # 排班管理模块
│   ├── attendance/       # 考勤管理模块
│   ├── leaves/           # 请假管理模块
│   ├── salaries/         # 薪资管理模块
│   ├── analytics/        # 统计分析模块
│   ├── static/           # 静态文件目录（CSS、JS、图片等）
│   ├── media/            # 用户上传的媒体文件（健康证图片等）
│   ├── manage.py         # Django 命令行工具
│   └── requirements.txt  # Python 依赖列表
├── frontend/             # Vue 3 前端项目（已创建）
├── sql/                  # 数据库初始化 SQL 文件（参考用，不直接执行）
├── memory-bank/          # 文档仓库
│   ├── PRD.md            # 产品需求文档
│   ├── tech-stack.md     # 技术栈说明
│   ├── IMPLEMENTATION_PLAN.md  # 详细实施计划
│   ├── progress.md       # 开发进度记录
│   └── architecture.md   # 本文档 - 架构说明
├── .gitignore
└── CLAUDE.md             # AI 开发者指南
```

---

## 后端 Django 项目架构

### 核心设计原则

1. **模块化设计**：每个应用（app）对应一个业务领域
2. **API 优先**：使用 Django REST Framework 构建 RESTful API
3. **前后端分离**：前端独立部署，通过 CORS 与后端通信
4. **业务层分离**：用户账号（User）与员工档案（EmployeeProfile）是两个独立概念

### Django 应用职责划分

| 应用 | 职责 | 主要模型 |
|------|------|---------|
| `config` | Django 项目配置、URL 路由、WSGI 配置 | - |
| `accounts` | 用户登录、注册、认证 | User（登录账号） |
| `employees` | 员工档案管理（业务信息，非登录账号） | EmployeeProfile |
| `schedules` | 排班计划、班次定义、调班申请 | Shift, Schedule, ShiftSwapRequest |
| `attendance` | 签到/签退、考勤记录、异常处理 | AttendanceRecord |
| `leaves` | 请假申请、审批流程 | LeaveRequest |
| `salaries` | 薪资计算、薪资记录、申诉处理 | SalaryRecord, Appeal |
| `analytics` | 数据统计、报表生成 | -（使用其他应用的模型） |

---

## 应用模块详解

### `accounts` 应用 - 用户账号与认证

用户账号与认证模块，负责系统登录、注册和用户管理。

#### 文件结构与职责

```
accounts/
├── __init__.py
├── admin.py              # Django Admin 配置
├── apps.py               # 应用配置
├── migrations/           # 数据库迁移文件
│   └── 0001_initial.py  # 创建 User 表
├── models.py             # 数据模型定义
├── serializers.py        # DRF 序列化器
├── urls.py               # 应用 URL 路由
└── views.py              # API 视图
```

#### 核心模型：User

```python
class User(models.Model):
    username       # 登录账号（唯一）
    password       # 登录密码（开发阶段明文）
    employee_id    # 关联员工档案ID（可选外键）
    role           # 角色类型：ADMIN/EMPLOYEE
    status         # 账号状态：ENABLED/DISABLED
    created_at     # 创建时间
    updated_at     # 更新时间
```

**架构设计要点**：
- `employee_id` 是可选字段，允许用户账号独立于员工档案存在
- 使用 Django 的 `TextChoices` 定义枚举类型，提供更好的类型安全
- `verify_password()` 类方法封装认证逻辑，便于后续扩展（如添加密码哈希）

#### 序列化器设计

| 序列化器 | 用途 | 特点 |
|---------|------|------|
| `LoginSerializer` | 登录请求验证 | 仅验证字段，不涉及模型 |
| `RegisterSerializer` | 注册请求验证 | 包含用户名唯一性检查 |
| `UserSerializer` | 用户详情 CRUD | 支持完整字段，用于增删改查 |
| `UserListSerializer` | 用户列表展示 | 简化字段，提升列表性能 |

**设计理念**：
- 分离序列化器职责，避免单个序列化器过于复杂
- 列表使用简化版序列化器，减少不必要的数据传输

#### 视图设计：UserViewSet

基于 DRF 的 `ModelViewSet`，提供标准的 CRUD 操作：

| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 登录 | POST | `/api/accounts/login/` | 自定义 action |
| 注册 | POST | `/api/accounts/register/` | 自定义 action，默认角色 EMPLOYEE |
| 列表 | GET | `/api/accounts/` | 标准操作 |
| 详情 | GET | `/api/accounts/{id}/` | 标准操作 |
| 创建 | POST | `/api/accounts/` | 标准操作（管理员） |
| 更新 | PUT/PATCH | `/api/accounts/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/accounts/{id}/` | 标准操作 |

**响应格式规范**：
```json
{
  "code": 200,           // 状态码
  "message": "成功",      // 消息提示
  "data": { ... }        // 响应数据
}
```

#### 路由配置

使用 DRF 的 `DefaultRouter` 自动生成标准 RESTful 路由：

```python
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
```

**路由映射**：
- 空字符串 `''` → 主路由为 `/api/accounts/`
- `basename='user'` → 用于生成 URL 名称（如 `user-detail`）

#### Django Admin 配置

`UserAdmin` 类提供后台管理界面：
- 列表展示：id, username, role, status, employee_id, created_at
- 过滤器：按角色、状态、创建时间筛选
- 搜索：支持用户名和 ID 搜索
- 字段分组：基本信息、角色与状态、时间信息（可折叠）

---

## 重要文件说明

### `backend/config/settings.py`

Django 项目的核心配置文件，包含：

- **INSTALLED_APPS**：注册所有应用和第三方库
- **DATABASES**：数据库连接配置（MySQL）
- **MIDDLEWARE**：中间件配置（包含 CORS）
- **CORS_ALLOWED_ORIGINS**：允许跨域访问的前端地址
- **STATIC_URL/MEDIA_URL**：静态文件和媒体文件路径配置

### `backend/config/urls.py`

URL 路由配置，将各应用的 URL 路由包含进来：
- `/admin/` - Django 管理后台
- `/api/accounts/` - 用户账号与认证 API

### `backend/requirements.txt`

Python 依赖列表，包含：
- `django>=5.2` - Django 框架
- `djangorestframework` - REST API 框架
- `mysqlclient` - MySQL 数据库驱动
- `django-cors-headers` - 跨域请求处理

### `backend/manage.py`

Django 命令行工具，用于：
- `python manage.py runserver` - 启动开发服务器
- `python manage.py makemigrations` - 创建数据库迁移文件
- `python manage.py migrate` - 应用数据库迁移
- `python manage.py createsuperuser` - 创建超级管理员
- `python manage.py startapp <appname>` - 创建新应用

---

## 数据库设计原则

### 表结构参考

- `sql/init_db.sql` 包含完整的数据库表结构定义
- **重要**：不要直接执行 SQL 文件，使用 Django migrations 管理数据库
- 每个 Django 应用的 `models.py` 文件定义对应的数据模型

### 核心业务概念

1. **User vs EmployeeProfile**
   - `User`：系统登录账号（存在于 `accounts` 应用）
   - `EmployeeProfile`：员工业务档案（存在于 `employees` 应用）
   - 两者通过 `employee_id` 外键关联（可选）
   - 并非所有员工都需要登录账号

2. **排班 → 考勤 → 薪资** 数据流
   - 排班（`schedules`）定义员工的工作班次
   - 考勤（`attendance`）记录员工的实际签到/签退
   - 薪资（`salaries`）根据考勤数据计算工资

---

## 前端 Vue 3 项目架构

### 项目结构

```
frontend/
├── src/
│   ├── views/
│   │   ├── admin/       # 管理员端页面
│   │   ├── employee/    # 员工端页面
│   │   └── auth/        # 登录/注册页面
│   ├── components/      # 公共组件
│   ├── api/             # API 请求封装
│   ├── router/          # Vue Router 配置
│   ├── stores/          # Pinia 状态管理
│   ├── assets/          # 静态资源（图片、样式等）
│   ├── App.vue          # 根组件
│   └── main.js          # 应用入口
├── public/              # 公共静态文件
├── index.html           # HTML 模板
├── package.json         # 项目依赖和脚本
├── vite.config.js       # Vite 配置
└── README.md            # 项目说明
```

### 核心技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue** | ^3.5.24 | 核心框架，使用 Composition API |
| **Vite** | ^7.2.4 | 构建工具，提供快速的开发体验 |
| **Element Plus** | ^2.13.1 | UI 组件库，提供丰富的界面组件 |
| **ECharts** | ^6.0.0 | 数据可视化，用于统计图表 |
| **Axios** | ^1.13.3 | HTTP 客户端，用于 API 请求 |
| **Vue Router** | ^4.6.4 | 路由管理，控制页面导航 |
| **Pinia** | ^3.0.4 | 状态管理，替代 Vuex |

### 目录职责说明

#### `src/views/` - 页面视图组件

- **admin/** - 管理员端页面
  - `DashboardView.vue` - 管理员首页/仪表板
  - `EmployeeManageView.vue` - 人员档案管理
  - `ScheduleManageView.vue` - 排班安排管理
  - `AttendanceManageView.vue` - 考勤记录管理
  - `LeaveApproveView.vue` - 请假审批管理
  - `SalaryManageView.vue` - 薪资信息管理
  - `StatisticsView.vue` - 综合统计分析
  - `SystemManageView.vue` - 系统管理

- **employee/** - 员工端页面
  - `HomeView.vue` - 员工端首页
  - `ProfileView.vue` - 个人信息中心
  - `CheckInView.vue` - 签到服务页面
  - `AttendanceView.vue` - 考勤信息查询
  - `LeaveView.vue` - 请假申请服务
  - `ShiftSwapView.vue` - 调班申请服务
  - `SalaryView.vue` - 薪资信息查询

- **auth/** - 认证相关页面
  - `LoginView.vue` - 登录页面
  - `RegisterView.vue` - 注册页面

#### `src/components/` - 公共组件

可复用的 Vue 组件，如：
- 数据表格组件
- 表单组件
- 图表组件
- 布局组件（侧边栏、顶部导航等）

#### `src/api/` - API 请求封装

封装与后端 API 的交互逻辑：
- `request.js` - Axios 实例配置（拦截器、基础 URL 等）
- `auth.js` - 认证相关 API
- `employee.js` - 员工档案 API
- `schedule.js` - 排班管理 API
- `attendance.js` - 考勤管理 API
- `leave.js` - 请假管理 API
- `salary.js` - 薪资管理 API
- `analytics.js` - 统计分析 API

#### `src/router/` - 路由配置

- `index.js` - 路由配置文件
  - 定义页面路径
  - 配置导航守卫（权限控制、登录状态检查）
  - 根据用户角色动态加载路由

#### `src/stores/` - Pinia 状态管理

- `user.js` - 用户状态（登录信息、权限等）
- `app.js` - 应用全局状态（主题、语言等）

### 重要文件说明

#### `frontend/vite.config.js`

Vite 构建工具的配置文件：

```javascript
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**配置说明**：
- **proxy**：开发服务器代理配置
  - 将前端 `/api` 请求代理到后端 `http://127.0.0.1:8000`
  - `changeOrigin: true` 确保跨域请求正确处理
- **plugins**：注册 Vue 3 插件

#### `frontend/package.json`

项目依赖和脚本配置：

```json
{
  "scripts": {
    "dev": "vite",           // 启动开发服务器
    "build": "vite build",   // 构建生产版本
    "preview": "vite preview" // 预览生产构建
  },
  "dependencies": { /* 生产依赖 */ },
  "devDependencies": { /* 开发依赖 */ }
}
```

#### `frontend/src/main.js`

应用入口文件，负责：
- 创建 Vue 应用实例
- 注册全局插件（Element Plus、Vue Router、Pinia）
- 挂载根组件

#### `frontend/src/App.vue`

根组件，包含：
- 路由视图容器（`<router-view>`）
- 全局布局组件（侧边栏、顶部导航等）
- 全局样式

### UI 主题设计

#### 配色方案

| 用途 | 色值 | 说明 |
|------|------|------|
| **主色** | `#FF6B35` | 橙色，体现食堂温暖氛围 |
| **辅助色1** | `#F7C52D` | 黄色，用于高亮和提示 |
| **辅助色2** | `#4CAF50` | 绿色，用于成功状态 |
| **背景色** | `#FFF8F0` | 浅米色，营造温馨感 |
| **文字色** | `#333333` | 深灰，保证可读性 |

#### 设计元素

- **图标**：餐具（刀叉、勺子）、厨师帽、食材等食堂相关元素
- **字体**：清晰易读，考虑部分员工年龄偏大，适度放大
- **圆角**：8px 圆角，营造亲和感
- **间距**：统一的 16px 间距规则

---

## API 设计原则与已实现端点

### RESTful 规范

- 资源使用名词复数：`/api/accounts/`
- HTTP 方法：GET（查询）、POST（创建）、PUT/PATCH（更新）、DELETE（删除）
- 使用 Django REST Framework 的 ViewSets 和 Serializers
- 统一响应格式：`{code, message, data}`

### API 端点结构

#### 已实现

```
POST   /api/accounts/register/   # 用户注册
POST   /api/accounts/login/      # 用户登录
GET    /api/accounts/            # 用户列表
GET    /api/accounts/{id}/       # 用户详情
POST   /api/accounts/            # 创建用户（管理员）
PUT    /api/accounts/{id}/       # 更新用户
DELETE /api/accounts/{id}/       # 删除用户
```

#### 计划中

### RESTful 规范

- 资源使用名词复数：`/api/employees/`
- HTTP 方法：GET（查询）、POST（创建）、PUT/PATCH（更新）、DELETE（删除）
- 使用 Django REST Framework 的 ViewSets 和 Serializers

### API 端点结构（计划）

```
/api/accounts/        # 用户认证
/api/employees/       # 员工档案
/api/schedules/       # 排班管理
/api/attendance/      # 考勤记录
/api/leaves/          # 请假申请
/api/salaries/        # 薪资记录
/api/analytics/       # 统计数据
```

---

## 开发工作流

1. **修改模型**：在对应应用的 `models.py` 中定义或修改数据模型
2. **创建迁移**：`python manage.py makemigrations`
3. **应用迁移**：`python manage.py migrate`
4. **创建序列化器**：在 `serializers.py` 中定义 API 序列化器
5. **创建视图**：在 `views.py` 中实现 API 端点
6. **配置路由**：在应用的 `urls.py` 中配置 URL 路由
7. **测试验证**：使用 Postman 或 curl 测试 API

---

## 注意事项

1. **statistics 应用名称冲突**：Python 内置了 `statistics` 模块，因此该应用命名为 `analytics`
2. **数据库迁移**：始终使用 Django migrations，不要直接执行 SQL
3. **密码存储**：开发阶段采用明文存储，生产环境需改为加密存储
4. **CORS 配置**：前端开发时需要配置 CORS 允许跨域请求
5. **Vite 端口**：Vite 默认使用 5173 端口，如被占用会自动尝试其他端口
6. **API 代理**：前端 `/api` 请求通过 Vite 代理转发到后端，生产环境需配置 Nginx 反向代理
7. **前端路由**：使用 Vue Router 的 Hash 模式或 History 模式（需服务器配置支持）
