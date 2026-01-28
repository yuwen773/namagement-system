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
│   ├── static/           # 静态文件目录
│   ├── media/            # 用户上传的媒体文件
│   ├── manage.py         # Django 命令行工具
│   └── requirements.txt  # Python 依赖列表
├── frontend/             # Vue 3 前端项目
├── sql/                  # 数据库初始化 SQL 文件（参考用）
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

### `accounts` - 用户账号与认证

用户账号与认证模块，负责系统登录、注册和用户管理。

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

#### 架构设计要点

- `employee_id` 是可选字段，允许用户账号独立于员工档案存在
- 使用 Django 的 `TextChoices` 定义枚举类型，提供更好的类型安全
- `verify_password()` 类方法封装认证逻辑，便于后续扩展（如添加密码哈希）

---

### `employees` - 员工档案管理

员工档案管理模块，负责员工业务信息的创建、维护和查询。

#### 核心模型：EmployeeProfile

```python
class EmployeeProfile(models.Model):
    # 基础信息
    name                      # 姓名
    gender                    # 性别：MALE/FEMALE
    phone                     # 联系方式
    id_card                   # 身份证号（唯一，可为空）
    address                   # 家庭住址

    # 岗位信息
    position                  # 岗位：CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER
    entry_date                # 入职时间
    status                    # 在职状态：ACTIVE/INACTIVE/LEAVE_WITHOUT_PAY

    # 资质证书
    health_certificate_no         # 健康证号
    health_certificate_expiry     # 健康证有效期
    health_certificate_url        # 健康证图片地址
    chef_certificate_level        # 厨师等级证

    # 时间戳
    created_at                # 创建时间
    updated_at                # 更新时间
```

#### 架构设计要点

- 使用 `TextChoices` 定义枚举类型，提供类型安全和中文标签
- 岗位类型覆盖食堂行业所有典型岗位，从厨师到保洁员
- 资质证书字段均为可选，根据岗位需求灵活配置

#### 与 User 模型的关系

| 方面 | EmployeeProfile | User |
|------|-----------------|------|
| **用途** | 业务层面的员工信息 | 系统登录账号 |
| **存在形式** | 可独立存在 | 可独立存在 |
| **关联方式** | 通过 `employee_id` 外键可选关联 | 通过 `employee_id` 外键可选关联 |
| **典型场景** | 所有员工都需要档案 | 只有需要登录系统的员工需要账号 |
| **包含信息** | 姓名、岗位、健康证等业务数据 | 用户名、密码、角色等认证数据 |

---

### `schedules` - 排班管理

排班管理模块，负责班次定义、排班计划和调班申请管理。

#### 核心模型

**Shift** - 班次定义
```python
class Shift(models.Model):
    name                    # 班次名称（如：早班/中班/晚班）
    start_time              # 上班开始时间
    end_time                # 下班结束时间
    created_at              # 创建时间
```

**Schedule** - 排班计划
```python
class Schedule(models.Model):
    employee                # 员工（外键 -> EmployeeProfile）
    shift                   # 班次（外键 -> Shift）
    work_date               # 排班日期（唯一约束：员工 + 日期）
    is_swapped              # 是否已调班
    created_at              # 创建时间
```

**ShiftSwapRequest** - 调班申请
```python
class ShiftSwapRequest(models.Model):
    requester               # 发起员工（外键 -> EmployeeProfile）
    original_schedule       # 原定排班（外键 -> Schedule）
    target_date             # 期望调整日期
    target_shift            # 期望调整班次（外键 -> Shift）
    reason                  # 申请原因
    status                  # 审批状态：PENDING/APPROVED/REJECTED
    approver                # 审批管理员（外键 -> EmployeeProfile，可选）
    approval_remark         # 审批意见
    created_at              # 创建时间
```

#### 架构设计要点

- 使用 `unique_together = [['employee', 'work_date']]` 防止同一员工在同一日期重复排班
- `is_swapped` 标记用于跟踪调班历史
- 调班审核通过后，系统自动更新排班记录（删除原排班，创建新排班）

---

### `attendance` - 考勤管理

考勤管理模块，负责员工签到/签退、考勤记录和异常处理。

#### 核心模型：AttendanceRecord

```python
class AttendanceRecord(models.Model):
    # 关联信息
    employee                # 员工（外键 -> EmployeeProfile）
    schedule                # 排班（外键 -> Schedule，可选）

    # 签到信息
    clock_in_time           # 签到时间（可为空）
    clock_in_location       # 签到地点

    # 签退信息
    clock_out_time          # 签退时间（可为空）
    clock_out_location      # 签退地点

    # 考勤状态
    status                  # 考勤状态：NORMAL/LATE/EARLY_LEAVE/MISSING/ABNORMAL

    # 异常处理
    correction_remark       # 更正备注

    # 时间戳
    created_at              # 创建时间
    updated_at              # 更新时间
```

#### 考勤状态判断规则

- **无签到或无签退记录** → MISSING（缺卡）
- **签到时间 > 班次开始时间 + 5分钟** → LATE（迟到）
- **签退时间 < 班次结束时间 - 5分钟** → EARLY_LEAVE（早退）
- **其他** → NORMAL（正常）

**弹性时间**：5分钟内签到/签退不算迟到/早退

---

### `leaves` - 请假管理

请假管理模块，负责员工请假申请、审批流程管理。

#### 核心模型：LeaveRequest

```python
class LeaveRequest(models.Model):
    # 基本信息字段
    employee                # 员工（外键 -> EmployeeProfile）
    leave_type              # 请假类型：SICK/PERSONAL/COMPENSATORY
    start_time              # 开始时间
    end_time                # 结束时间
    reason                  # 请假原因

    # 审批信息字段
    status                  # 审批状态：PENDING/APPROVED/REJECTED
    approver                # 审批人（外键 -> EmployeeProfile，可选）
    approval_remark         # 审批意见

    # 时间戳
    created_at              # 创建时间
    updated_at              # 更新时间
```

#### 架构设计要点

- 使用 `TextChoices` 定义枚举类型，提供类型安全和中文标签
- `approver` 外键为可选，允许系统自动审批（如需要）
- 审批状态默认为 PENDING（待审批）

---

### `salaries` - 薪资管理

薪资管理模块，负责薪资计算、薪资记录生成、异常申诉处理。

#### 核心模型

**SalaryRecord** - 薪资记录
```python
class SalaryRecord(models.Model):
    # 基本信息字段
    employee                # 员工（外键 -> EmployeeProfile）
    year_month              # 年月（格式：YYYY-MM）

    # 薪资组成字段
    base_salary             # 基本工资
    position_allowance      # 岗位津贴
    overtime_pay            # 加班费
    deductions              # 扣款
    total_salary            # 实发工资（自动计算）

    # 统计字段
    work_days               # 出勤天数
    late_count              # 迟到次数
    missing_count           # 缺卡次数
    overtime_hours          # 加班时长（小时）

    # 状态和备注
    status                  # 状态：DRAFT/PUBLISHED/APPEALED/ADJUSTED
    remark                  # 备注

    # 时间戳
    created_at              # 创建时间
    updated_at              # 更新时间
```

**Appeal** - 异常申诉
```python
class Appeal(models.Model):
    # 基本信息字段
    appeal_type             # 申诉类型：ATTENDANCE/SALARY
    employee                # 申诉员工（外键 -> EmployeeProfile）
    target_id               # 目标记录ID（考勤记录ID或薪资记录ID）

    # 申诉信息
    reason                  # 申诉原因

    # 审批信息
    status                  # 审批状态：PENDING/APPROVED/REJECTED
    approver                # 审批人（外键 -> EmployeeProfile，可选）
    approval_remark         # 审批意见

    # 时间戳
    created_at              # 创建时间
    updated_at              # 更新时间
```

#### 薪资计算规则

| 项目 | 计算公式 | 说明 |
|------|---------|------|
| 日工资 | 月薪 ÷ 21.75 | 固定工作日21.75天 |
| 时薪 | 日工资 ÷ 8 | 每日工作8小时 |
| 加班费 | 时薪 × 1.5 × 加班小时数 | 加班按1.5倍计算 |
| 迟到扣款 | 20 元 × 迟到次数 | 每次迟到扣20元 |
| 缺卡扣款 | 50 元 × 缺卡次数 | 每次缺卡扣50元 |
| 岗位津贴 | 固定金额 | CHEF(800)、PASTRY(700)、PREP(500)、CLEANER(300)、SERVER(400)、MANAGER(1000) |
| 实发工资 | 基本工资 + 岗位津贴 + 加班费 - 扣款 | 自动计算 |

---

### `analytics` - 统计分析

统计分析模块，负责跨模块的数据聚合和报表生成。

#### 架构设计要点

- **无模型设计**：`analytics` 应用没有自己的数据模型，直接使用其他应用的模型进行数据聚合
- **视图函数而非 ViewSet**：使用 `@api_view` 装饰器定义视图函数，每个接口对应一个统计维度
- **数据格式专为 ECharts 优化**：前端无需复杂的数据转换

#### 统计维度

**人员统计** (`employee_statistics`)
- 总人数、岗位分布、持证率、入职状态分布

**考勤统计** (`attendance_statistics`)
- 出勤率、状态分布、日期趋势、岗位维度

**薪资统计** (`salary_statistics`)
- 月度趋势、岗位对比、薪资构成

**总览统计** (`overview_statistics`)
- 今日概览、待办事项、总览统计、本月考勤

---

## 数据库设计原则

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
| **Vite** | ^7.2.4 | 构建工具 |
| **Element Plus** | ^2.13.1 | UI 组件库 |
| **ECharts** | ^6.0.0 | 数据可视化 |
| **Axios** | ^1.13.3 | HTTP 客户端 |
| **Vue Router** | ^4.6.4 | 路由管理 |
| **Pinia** | ^3.0.4 | 状态管理 |

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

可复用的 Vue 组件，如数据表格、表单、图表、布局组件等。

#### `src/api/` - API 请求封装

- `request.js` - Axios 实例配置，请求/响应拦截器
- `auth.js` - 认证相关 API
- `employee.js` - 员工档案 API
- `schedule.js` - 排班管理 API
- `attendance.js` - 考勤管理 API
- `leave.js` - 请假管理 API
- `salary.js` - 薪资管理 API
- `analytics.js` - 统计分析 API

#### `src/router/` - 路由配置

**路由导航守卫功能**：
- 检查路由是否需要认证
- 检查用户角色权限
- 角色不匹配时，自动跳转到对应角色的首页

#### `src/stores/` - Pinia 状态管理

**`user.js`** - 用户状态管理
- 状态字段：`token`、`userInfo`
- 操作方法：`login()`、`logout()`、`updateUserInfo()`

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
- `/api/employees/` - 员工档案 API
- `/api/schedules/` - 排班管理 API
- `/api/attendance/` - 考勤管理 API
- `/api/leaves/` - 请假管理 API
- `/api/salaries/` - 薪资管理 API
- `/api/analytics/` - 统计分析 API

### `backend/requirements.txt`

Python 依赖列表，包含：
- `django>=5.2` - Django 框架
- `djangorestframework` - REST API 框架
- `mysqlclient` - MySQL 数据库驱动
- `django-cors-headers` - 跨域请求处理
- `django-filter` - 查询过滤功能

### `backend/manage.py`

Django 命令行工具，用于：
- `python manage.py runserver` - 启动开发服务器
- `python manage.py makemigrations` - 创建数据库迁移文件
- `python manage.py migrate` - 应用数据库迁移
- `python manage.py createsuperuser` - 创建超级管理员

### `frontend/vite.config.js`

Vite 构建工具的配置文件：
- **proxy**：将前端 `/api` 请求代理到后端 `http://127.0.0.1:8000`
- **plugins**：注册 Vue 3 插件

### `frontend/package.json`

项目依赖和脚本配置：
- `npm run dev` - 启动开发服务器
- `npm run build` - 构建生产版本
- `npm run preview` - 预览生产构建

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
5. **API 代理**：前端 `/api` 请求通过 Vite 代理转发到后端，生产环境需配置 Nginx 反向代理
6. **前端路由**：使用 Vue Router 的 Hash 模式或 History 模式（需服务器配置支持）
