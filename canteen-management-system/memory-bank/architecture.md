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

每个文件封装一个业务模块的 API 请求方法，基于统一的 `request.js` Axios 实例。

- `request.js` - Axios 实例配置，请求/响应拦截器，401 自动跳转登录
- `auth.js` - 认证相关 API（登录、注册、用户列表）
- `employee.js` - 员工档案 API（CRUD、筛选、搜索）
- `schedule.js` - 排班管理 API（班次、排班、调班申请、日历视图、批量排班）
- `attendance.js` - 考勤管理 API（签到、签退、统计、更正、我的考勤）
- `leave.js` - 请假管理 API（请假申请、审批、我的请假、待审批列表）
- `salary.js` - 薪资管理 API（薪资列表/详情/生成/调整/发布/删除、申诉列表/审批）
- `analytics.js` - 统计分析 API（人员统计、考勤统计、薪资统计、总览统计）

**`salary.js` 薪资 API 文件说明**：
```
getSalaryList(params)        # 获取薪资列表，支持月份、员工、状态筛选和分页
getSalaryDetail(id)          # 获取薪资详情
createSalary(data)           # 创建薪资记录
updateSalary(id, data)       # 更新薪资记录
generateSalary(data)         # 生成薪资（根据考勤自动计算）
adjustSalary(id, data)       # 调整薪资（手动修改基本工资、加班费等）
publishSalary(id)            # 发布薪资（状态从草稿改为已发布）
deleteSalary(id)             # 删除薪资记录

# 申诉相关
getAppealList(params)        # 获取申诉列表
getAppealDetail(id)          # 获取申诉详情
createAppeal(data)           # 创建申诉
approveAppeal(id, data)      # 审批申诉
getPendingAppeals(params)    # 获取待审批申诉列表
exportSalarySheet(params)    # 导出工资表
```

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

---

## 前端页面组件详解

### `SalaryManageView.vue` - 薪资信息管理页面

薪资管理是管理员端的核心功能之一，负责员工薪资的生成、查看、调整和发布。

#### 页面结构

```
┌─────────────────────────────────────────────────────────┐
│ 页面标题: 💰 薪资管理                                     │
├─────────────────────────────────────────────────────────┤
│ 操作栏: [月份选择器] [生成薪资] [导出工资表]                 │
├─────────────────────────────────────────────────────────┤
│ 统计卡片: 💵本月薪资总额  📈平均薪资  📝待发布  ⚠️待处理申诉   │
├─────────────────────────────────────────────────────────┤
│ 薪资列表表格:                                             │
│ | 员工 | 岗位 | 月份 | 基本 | 津贴 | 加班 | 扣款 | 实发 | 状态 | 操作 | │
│ | 张三 | 厨师 | 2024-01 | ¥3000 | ¥800 | ¥500 | ¥20 | ¥4280 | 草稿 | 详情 调整 发布 删除 | │
├─────────────────────────────────────────────────────────┤
│ 分页: 总共 50 条, 每页 20 条 [1] 2 3                     │
└─────────────────────────────────────────────────────────┘
```

#### 核心功能模块

**1. 月份筛选与薪资生成**
- 默认显示当前月份的薪资数据
- 选择月份后自动刷新列表
- "生成薪资"按钮触发批量计算，基于考勤数据自动生成所有员工的薪资记录

**2. 统计卡片区域**
四个渐变卡片显示本月薪资概况：
- **本月薪资总额**（橙黄渐变）- 所有员工实发工资总和
- **平均薪资**（黄绿渐变）- 人均薪资水平
- **待发布薪资**（绿色渐变）- 草稿状态的薪资记录数量
- **待处理申诉**（红色渐变）- 待审批的申诉数量

**3. 薪资列表表格**
列设计强调数据可读性：
- **员工姓名**：带头像圆形渐变背景
- **岗位**：彩色标签（厨师-橙色、面点-红色等）
- **薪资项**：右对齐，等宽字体，带货币符号
  - 岗位津贴：绿色 `+¥800`
  - 加班费：橙色高亮 `+¥500`（>0时）
  - 扣款：红色 `-¥20`
  - 实发工资：橙色大字 `¥4280.00`
- **状态标签**：草稿(灰)、已发布(绿)、已调整(橙)、申诉中(红)
- **操作按钮**：详情、调整、发布、删除（已发布不可调整）

**4. 调整薪资对话框**
管理员可手动修正薪资数据：
- 顶部显示当前员工、月份、实发工资摘要
- 可调整项：基本工资、加班费（数字输入框，步进100/50）
- 调整原因：必填文本域（5-200字符）
- 确认提示：调整后状态自动变更为"已调整"

**5. 薪资详情对话框**
展示完整薪资构成和考勤统计：
- 头部：员工头像、姓名、月份、状态标签
- 明细网格：基本工资、岗位津贴、加班费、迟到扣款、缺卡扣款、实发工资
  - 实发工资行：橙色渐变背景，大号字体
- 考勤统计标签：出勤天数、迟到次数、缺卡次数、加班时长

**6. 申诉处理对话框**
处理员工的考勤/薪资申诉：
- 顶部警告框显示申诉原因
- 单选按钮：批准申诉（绿色✅）/ 拒绝申诉（红色❌）
- 审批意见：必填文本域，根据批准/拒绝显示不同提示

#### 状态管理

```javascript
// 页面状态
selectedMonth        // 当前选择的月份（YYYY-MM 格式）
salaryList          // 薪资记录列表
statsData           // 统计数据（总额、平均、待发布、待申诉）
pagination          // 分页信息（page, pageSize, total）

// 对话框状态
adjustDialogVisible     // 调整薪资对话框
detailDialogVisible     // 薪资详情对话框
appealDialogVisible     // 申诉处理对话框

// 当前操作对象
currentSalary       // 当前查看/调整的薪资记录
currentAppeal       // 当前处理的申诉

// 表单数据
adjustForm          // 调整表单 { base_salary, overtime_pay, reason }
appealForm          // 申诉审批表单 { approve, approval_remark }
```

#### API 调用流程

```
页面加载
  │
  ├─> loadSalaryList() ──────────────────────────────────────┐
  │     GET /api/salaries/salaries/?year_month=2024-01&page=1 │
  │     │                                                    │
  │     └─> salaryList = response.data.results              │
  │     └─> updateStats() 计算统计数据                        │
  │                                                          │
  ├─> 生成薪资                                               │
  │     generateSalary({ year_month })                      │
  │     POST /api/salaries/salaries/generate/               │
  │     └─> 重新加载列表                                     │
  │                                                          │
  ├─> 调整薪资                                               │
  │     adjustSalary(id, { base_salary, overtime_pay, reason })│
  │     POST /api/salaries/salaries/{id}/adjust/            │
  │     └─> 重新加载列表                                     │
  │                                                          │
  ├─> 发布薪资                                               │
  │     publishSalary(id)                                   │
  │     POST /api/salaries/salaries/{id}/publish/           │
  │     └─> 更新状态为"已发布"                               │
  │                                                          │
  └─> 审批申诉                                               │
        approveAppeal(id, { approve, approval_remark })      │
        POST /api/salaries/appeals/{id}/approve/            │
        └─> 重新加载列表                                     │
```

#### UI 设计亮点

**渐变配色系统**
- 对话框标题使用不同渐变：
  - 调整薪资：橙黄渐变 `#FF6B35 → #F7C52D`
  - 薪资详情：绿色渐变 `#4CAF50 → #8BC34A`
  - 申诉处理：红色渐变 `#F44336 → #FF9800`

**交互动效**
- 统计卡片悬停：向上平移4px + 阴影增强 + 边框高亮
- 表格行悬停：浅米色背景 `#FFF8F0`
- 快捷入口箭头：悬停时从左滑入

**可访问性设计**
- 金额使用等宽字体（SF Mono / Consolas）
- 数字右对齐便于对比
- 状态用颜色+文字双重标识
- 表单验证实时反馈

**响应式布局**
- 桌面端：统计卡片4列，详情网格2列
- 平板端：统计卡片2列，详情网格1列
- 移动端：全部单列堆叠

#### 与后端的契约

**薪资状态流转**
```
DRAFT（草稿）
  │
  ├─> publishSalary() ──> PUBLISHED（已发布）
  │
  └─> adjustSalary() ──> ADJUSTED（已调整）
                            │
                            └─> publishSalary() ──> PUBLISHED

APPEALED（申诉中）
  │
  └─> approveAppeal(approve=true) ──> ADJUSTED（批准后调整薪资）
      │
      └─> approveAppeal(approve=false) ──> 保持原状态
```

**薪资计算公式（后端执行）**
```
日工资 = 月基本工资 ÷ 21.75
时薪 = 日工资 ÷ 8
加班费 = 时薪 × 1.5 × 加班小时数
岗位津贴 = 根据岗位固定金额
迟到扣款 = 20 × 迟到次数
缺卡扣款 = 50 × 缺卡次数
实发工资 = 基本工资 + 岗位津贴 + 加班费 - 迟到扣款 - 缺卡扣款
```

前端只负责展示和手动调整，计算逻辑全部在后端完成，确保数据一致性。
