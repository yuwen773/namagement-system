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

## 重要文件说明

### `backend/config/settings.py`

Django 项目的核心配置文件，包含：

- **INSTALLED_APPS**：注册所有应用和第三方库
- **DATABASES**：数据库连接配置（MySQL）
- **MIDDLEWARE**：中间件配置（包含 CORS）
- **CORS_ALLOWED_ORIGINS**：允许跨域访问的前端地址
- **STATIC_URL/MEDIA_URL**：静态文件和媒体文件路径配置

### `backend/config/urls.py`

URL 路由配置（待实现），将各应用的 URL 路由包含进来。

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

## API 设计原则（待实现）

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
