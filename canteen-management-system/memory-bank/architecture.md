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

### `employees` 应用 - 员工档案管理

员工档案管理模块，负责员工业务信息的创建、维护和查询。

#### 文件结构与职责

```
employees/
├── __init__.py
├── admin.py              # Django Admin 配置
├── apps.py               # 应用配置
├── migrations/           # 数据库迁移文件
│   └── 0001_initial.py  # 创建 EmployeeProfile 表
├── models.py             # 数据模型定义
├── serializers.py        # DRF 序列化器
├── urls.py               # 应用 URL 路由
└── views.py              # API 视图
```

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

**架构设计要点**：
- 使用 `TextChoices` 定义枚举类型，提供类型安全和中文标签
- `id_card` 字段设置为唯一但允许为空，适应不同场景需求
- 岗位类型覆盖食堂行业所有典型岗位，从厨师到保洁员
- 资质证书字段均为可选，根据岗位需求灵活配置
- `__str__` 方法返回 `姓名 (岗位)` 格式，便于后台管理显示

#### 序列化器设计

| 序列化器 | 用途 | 特点 |
|---------|------|------|
| `EmployeeProfileSerializer` | 员工档案详情 CRUD | 支持完整字段，包含所有显示字段 |
| `EmployeeProfileListSerializer` | 员工列表展示 | 简化字段，提升列表查询性能 |

**设计理念**：
- 列表和详情使用不同序列化器，避免传输不必要的数据
- 详情序列化器包含所有 `*_display` 字段，方便前端直接显示中文标签
- 自定义 `validate_id_card()` 方法，在更新时排除当前记录进行唯一性验证

#### 视图设计：EmployeeProfileViewSet

基于 DRF 的 `ModelViewSet`，提供标准的 CRUD 操作和高级筛选功能：

| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/employees/` | 支持筛选、搜索、排序 |
| 创建 | POST | `/api/employees/` | 标准操作 |
| 详情 | GET | `/api/employees/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/employees/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/employees/{id}/` | 标准操作 |

**高级筛选功能**：
- **字段筛选**：使用 `django_filters` 的 `DjangoFilterBackend`
  - 按岗位筛选：`?position=CHEF`
  - 按状态筛选：`?status=ACTIVE`
  - 组合筛选：`?position=CHEF&status=ACTIVE`
- **全文搜索**：使用 DRF 的 `SearchFilter`
  - 搜索字段：姓名、电话、身份证号
  - 示例：`?search=张三`
- **排序**：使用 DRF 的 `OrderingFilter`
  - 支持字段：创建时间、入职日期、姓名
  - 示例：`?ordering=-created_at`（倒序）

#### 路由配置

使用 DRF 的 `DefaultRouter` 自动生成标准 RESTful 路由：

```python
router = DefaultRouter()
router.register(r'', EmployeeProfileViewSet, basename='employee')
```

**路由映射**：
- 空字符串 `''` → 主路由为 `/api/employees/`
- `basename='employee'` → 用于生成 URL 名称（如 `employee-detail`）

#### Django Admin 配置

`EmployeeProfileAdmin` 类提供后台管理界面：
- 列表展示：id, name, gender, phone, position, entry_date, status, created_at
- 过滤器：按岗位、状态、性别、创建时间筛选
- 搜索：支持姓名、电话、身份证号搜索
- 字段分组：基础信息、岗位信息、资质证书、时间信息（可折叠）
- 只读字段：创建时间、更新时间

#### 与 User 模型的关系

| 方面 | EmployeeProfile | User |
|------|-----------------|------|
| **用途** | 业务层面的员工信息 | 系统登录账号 |
| **存在形式** | 可独立存在 | 可独立存在 |
| **关联方式** | 通过 `employee_id` 外键可选关联 | 通过 `employee_id` 外键可选关联 |
| **典型场景** | 所有员工都需要档案 | 只有需要登录系统的员工需要账号 |
| **包含信息** | 姓名、岗位、健康证等业务数据 | 用户名、密码、角色等认证数据 |

**架构意义**：
- 这种分离设计允许"无账号员工"（如大龄保洁人员）的存在
- 员工离职时，只需禁用 User 账号，EmployeeProfile 档案可保留用于历史记录
- 灵活支持未来的业务扩展（如临时工、外包人员等）

---

### `schedules` 应用 - 排班管理

排班管理模块，负责班次定义、排班计划和调班申请管理。

#### 文件结构与职责

```
schedules/
├── __init__.py
├── admin.py              # Django Admin 配置
├── apps.py               # 应用配置
├── migrations/           # 数据库迁移文件
│   └── 0001_initial.py  # 创建 Shift, Schedule, ShiftSwapRequest 表
├── models.py             # 数据模型定义
├── serializers.py        # DRF 序列化器
├── urls.py               # 应用 URL 路由
└── views.py              # API 视图
```

#### 核心模型

**Shift 模型** - 班次定义
```python
class Shift(models.Model):
    name                    # 班次名称（如：早班/中班/晚班）
    start_time              # 上班开始时间
    end_time                # 下班结束时间
    created_at              # 创建时间
```

**Schedule 模型** - 排班计划
```python
class Schedule(models.Model):
    employee                # 员工（外键 -> EmployeeProfile）
    shift                   # 班次（外键 -> Shift）
    work_date               # 排班日期（唯一约束：员工 + 日期）
    is_swapped              # 是否已调班
    created_at              # 创建时间
```

**架构设计要点**：
- 使用 `unique_together = [['employee', 'work_date']]` 防止同一员工在同一日期重复排班
- `is_swapped` 标记用于跟踪调班历史
- `work_date` 添加索引以优化日期范围查询性能

**ShiftSwapRequest 模型** - 调班申请
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

**架构设计要点**：
- 使用 `TextChoices` 定义状态枚举，提供类型安全
- 调班审核通过后，系统自动更新排班记录（删除原排班，创建新排班）
- 保留审批人和审批意见，便于审计和追溯

#### 序列化器设计

| 序列化器 | 用途 | 特点 |
|---------|------|------|
| `ShiftSerializer` | 班次详情 CRUD | 支持完整字段 |
| `ShiftListSerializer` | 班次列表展示 | 简化字段 |
| `ScheduleSerializer` | 排班创建 | 包含员工和班次 ID |
| `ScheduleListSerializer` | 排班列表展示 | 简化字段，提升性能 |
| `ScheduleDetailSerializer` | 排班详情 | 包含完整信息（员工姓名、岗位等） |
| `BatchScheduleSerializer` | 批量排班 | 验证员工 ID 列表和日期范围 |
| `ShiftSwapRequestSerializer` | 调班申请详情 | 包含完整审批信息 |
| `ShiftSwapRequestListSerializer` | 调班申请列表 | 简化字段 |
| `ShiftSwapApprovalSerializer` | 调班审批 | 验证审批参数 |
| `CalendarViewSerializer` | 日历视图 | 验证日期范围参数 |

#### 视图设计

**ShiftViewSet** - 班次定义管理
| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/schedules/shifts/` | 标准操作 |
| 创建 | POST | `/api/schedules/shifts/` | 标准操作，返回统一格式 |
| 详情 | GET | `/api/schedules/shifts/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/schedules/shifts/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/schedules/shifts/{id}/` | 标准操作 |

**ScheduleViewSet** - 排班计划管理
| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/schedules/schedules/` | 支持筛选、搜索、排序 |
| 创建 | POST | `/api/schedules/schedules/` | 标准操作，返回统一格式 |
| 批量创建 | POST | `/api/schedules/schedules/batch_create/` | 批量为多个员工创建排班 |
| 日历视图 | POST | `/api/schedules/schedules/calendar_view/` | 按日期分组返回排班数据 |
| 详情 | GET | `/api/schedules/schedules/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/schedules/schedules/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/schedules/schedules/{id}/` | 标准操作 |

**批量排班接口**：
- 输入参数：`employee_ids`（员工 ID 列表）、`shift_id`（班次 ID）、`start_date`、`end_date`
- 使用 `get_or_create` 避免重复创建
- 返回创建数量和跳过数量

**日历视图接口**：
- 输入参数：`start_date`、`end_date`、`employee_id`（可选）
- 返回按日期分组的排班数据
- 数据格式适合前端日历组件直接使用

**ShiftSwapRequestViewSet** - 调班申请管理
| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/schedules/shift-requests/` | 支持筛选、搜索、排序 |
| 创建 | POST | `/api/schedules/shift-requests/` | 标准操作，返回统一格式 |
| 审批 | POST | `/api/schedules/shift-requests/{id}/approve/` | 批准或拒绝调班申请 |
| 我的申请 | GET | `/api/schedules/shift-requests/my_requests/` | 查询当前员工的调班申请 |
| 待审批 | GET | `/api/schedules/shift-requests/pending/` | 管理员查看待审批列表 |
| 详情 | GET | `/api/schedules/shift-requests/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/schedules/shift-requests/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/schedules/shift-requests/{id}/` | 标准操作 |

**调班审核接口**：
- 输入参数：`approve`（是否批准）、`approval_remark`（审批意见）
- 批准时自动更新排班记录（删除原排班，创建新排班）
- 拒绝时仅更新申请状态和审批意见

#### 路由配置

```python
router = DefaultRouter()
router.register(r'shifts', ShiftViewSet, basename='shift')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'shift-requests', ShiftSwapRequestViewSet, basename='shift-request')
```

**路由映射**：
- `/api/schedules/shifts/` → 班次定义管理
- `/api/schedules/schedules/` → 排班计划管理
- `/api/schedules/shift-requests/` → 调班申请管理

#### Django Admin 配置

**ShiftAdmin** - 班次定义管理
- 列表展示：id, name, start_time, end_time, created_at
- 过滤器：按班次名称、创建时间筛选
- 字段分组：基本信息、时间信息

**ScheduleAdmin** - 排班计划管理
- 列表展示：id, 员工名, 班次名, 排班日期, 是否调班, 创建时间
- 自定义列：`employee_name`、`shift_name`
- 过滤器：按班次、日期、是否调班、创建时间筛选
- 搜索：支持员工姓名、手机号搜索
- 日期分层导航：按排班日期浏览

**ShiftSwapRequestAdmin** - 调班申请管理
- 列表展示：id, 发起人, 原定排班, 目标排班, 状态, 审批人, 创建时间
- 自定义列：`requester_name`、`original_info`、`target_info`、`approver_name`
- 过滤器：按状态、目标日期、创建时间筛选
- 搜索：支持发起人姓名、申请原因、审批意见搜索
- 字段分组：申请信息、审批信息、时间信息

#### 业务流程

**排班流程**：
1. 管理员创建班次定义（早班、中班、晚班等）
2. 管理员为员工创建排班（单个或批量）
3. 员工通过日历视图查看排班
4. 员工发起调班申请
5. 管理员审核调班申请（批准/拒绝）
6. 批准后系统自动更新排班记录

**批量排班逻辑**：
- 计算日期范围内的所有日期
- 为每个员工在每个日期创建排班
- 使用 `get_or_create` 避免重复
- 返回创建数量和跳过数量

---

### `attendance` 应用 - 考勤管理

考勤管理模块，负责员工签到/签退、考勤记录和异常处理。

#### 文件结构与职责

```
attendance/
├── __init__.py
├── admin.py              # Django Admin 配置
├── apps.py               # 应用配置
├── migrations/           # 数据库迁移文件
│   └── 0001_initial.py  # 创建 AttendanceRecord 表
├── models.py             # 数据模型定义
├── serializers.py        # DRF 序列化器
├── urls.py               # 应用 URL 路由
└── views.py              # API 视图
```

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

**架构设计要点**：
- 使用 `TextChoices` 定义状态枚举，提供类型安全和中文标签
- `schedule` 外键为可选，允许在没有排班的情况下手动创建考勤记录
- 保存时自动判断考勤状态（`_calculate_status` 方法）
- 自动计算加班时长（`calculate_overtime_hours` 方法）
- 使用 `UniqueConstraint` 确保同一员工在同一排班只有一条考勤记录

#### 考勤状态判断规则

```python
def _calculate_status(self):
    """
    自动判断考勤状态

    判断规则：
    - 无签到或无签退记录 → MISSING（缺卡）
    - 签到时间 > 班次开始时间 + 5分钟 → LATE（迟到）
    - 签退时间 < 班次结束时间 - 5分钟 → EARLY_LEAVE（早退）
    - 其他 → NORMAL（正常）
    """
```

**弹性时间**：5分钟内签到/签退不算迟到/早退

#### 序列化器设计

| 序列化器 | 用途 | 特点 |
|---------|------|------|
| `AttendanceRecordSerializer` | 考勤记录详情 CRUD | 支持完整字段，包含员工名、班次信息、状态显示 |
| `AttendanceRecordListSerializer` | 考勤记录列表展示 | 简化字段，提升列表查询性能 |
| `ClockInSerializer` | 签到请求验证 | 验证排班ID和签到地点 |
| `ClockOutSerializer` | 签退请求验证 | 验证签退地点 |
| `AttendanceStatisticsSerializer` | 考勤统计请求 | 验证日期范围和员工ID |
| `AttendanceStatisticsResponseSerializer` | 考勤统计响应 | 返回统计数据 |
| `AttendanceCorrectionSerializer` | 异常处理 | 验证状态修改和备注（备注必填） |

#### 视图设计：AttendanceRecordViewSet

基于 DRF 的 `ModelViewSet`，提供标准的 CRUD 操作和特殊业务接口：

| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/attendance/` | 支持筛选、搜索、排序 |
| 创建 | POST | `/api/attendance/` | 标准操作（管理员手动创建） |
| 详情 | GET | `/api/attendance/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/attendance/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/attendance/{id}/` | 标准操作 |
| 签到 | POST | `/api/attendance/clock_in/` | 员工签到接口 |
| 签退 | POST | `/api/attendance/clock_out/` | 员工签退接口 |
| 统计 | POST | `/api/attendance/statistics/` | 考勤统计接口 |
| 异常处理 | POST | `/api/attendance/{id}/correct/` | 管理员修改考勤状态 |
| 我的考勤 | GET | `/api/attendance/my_attendance/` | 员工查看自己的考勤记录 |

**签到接口逻辑**：
- 接收员工ID、排班ID（可选）、签到地点
- 如果没有提供排班，自动查找今日排班
- 检查是否已签到，避免重复签到
- 创建或更新考勤记录
- 自动判断考勤状态

**签退接口逻辑**：
- 接收员工ID、签退地点
- 查找今日考勤记录
- 检查是否已签到，未签到则提示错误
- 检查是否已签退，避免重复签退
- 更新签退信息
- 自动重新判断考勤状态

**考勤统计接口**：
- 接收日期范围（开始日期、结束日期）
- 可选员工ID（不提供则统计所有员工）
- 返回统计数据：
  - `total_days` - 总天数
  - `present_days` - 出勤天数
  - `late_count` - 迟到次数
  - `early_leave_count` - 早退次数
  - `missing_count` - 缺卡次数
  - `overtime_hours` - 加班时长（小时）

**异常处理接口**：
- 管理员可修改考勤状态
- 必须填写更正备注（`correction_remark`）
- 修改后的状态会覆盖自动判断的状态
- 保留修改历史（通过 `correction_remark` 字段）

#### 路由配置

```python
router = DefaultRouter()
router.register(r'', AttendanceRecordViewSet, basename='attendance')
```

**路由映射**：
- 空字符串 `''` → 主路由为 `/api/attendance/`
- `basename='attendance'` → 用于生成 URL 名称（如 `attendance-detail`）

#### Django Admin 配置

`AttendanceRecordAdmin` 类提供后台管理界面：
- 列表展示：id, 员工名, 工作日期, 班次, 签到时间, 签退时间, 状态, 迟到, 早退, 缺卡, 加班时长, 创建时间
- 过滤器：按状态、创建时间、工作日期筛选
- 搜索：支持员工姓名、电话、地点搜索
- 日期分层导航：按工作日期浏览
- 字段分组：基本信息、签到信息、签退信息、考勤状态、异常处理、时间信息（可折叠）
- 只读字段：创建时间、更新时间、状态、加班时长

#### 业务流程

**签到流程**：
1. 员工在班次开始时间前后进行签到
2. 系统记录签到时间和地点
3. 系统自动判断考勤状态（正常/迟到）
4. 返回签到结果给员工

**签退流程**：
1. 员工在班次结束时间前后进行签退
2. 系统记录签退时间和地点
3. 系统自动判断考勤状态（正常/早退/缺卡）
4. 系统计算加班时长（如有）
5. 返回签退结果给员工

**异常处理流程**：
1. 管理员发现异常考勤记录
2. 管理员修改考勤状态（如将"缺卡"改为"正常"）
3. 管理员填写更正备注（必填）
4. 系统保存修改，记录修改历史

**加班计算逻辑**：
```
加班时长 = 签退时间 - 班次结束时间
（仅计算超出部分，以小时为单位，保留2位小数）
```

#### 与其他模块的关系

| 模块 | 关系 | 说明 |
|------|------|------|
| `employees` | 依赖 | `AttendanceRecord.employee` 外键关联 `EmployeeProfile` |
| `schedules` | 依赖 | `AttendanceRecord.schedule` 外键关联 `Schedule` |
| `salaries` | 被依赖 | 薪资计算需要考勤数据（迟到次数、缺卡次数、加班时长） |

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
- `django-filter` - 查询过滤功能（支持高级筛选）

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

**用户认证 API (`/api/accounts/`)**
```
POST   /api/accounts/register/   # 用户注册
POST   /api/accounts/login/      # 用户登录
GET    /api/accounts/            # 用户列表
GET    /api/accounts/{id}/       # 用户详情
POST   /api/accounts/            # 创建用户（管理员）
PUT    /api/accounts/{id}/       # 更新用户
DELETE /api/accounts/{id}/       # 删除用户
```

**员工档案 API (`/api/employees/`)**
```
GET    /api/employees/           # 员工列表（支持筛选和搜索）
POST   /api/employees/           # 创建员工档案
GET    /api/employees/{id}/      # 员工详情
PUT    /api/employees/{id}/      # 更新员工档案
DELETE /api/employees/{id}/      # 删除员工档案
```

**筛选参数示例**：
- 按岗位筛选：`/api/employees/?position=CHEF`
- 按状态筛选：`/api/employees/?status=ACTIVE`
- 组合筛选：`/api/employees/?position=CHEF&status=ACTIVE`
- 搜索：`/api/employees/?search=张三`
- 排序：`/api/employees/?ordering=-created_at`

**排班管理 API (`/api/schedules/`)**
```
# 班次定义
GET    /api/schedules/shifts/           # 班次列表
POST   /api/schedules/shifts/           # 创建班次
GET    /api/schedules/shifts/{id}/      # 班次详情
PUT    /api/schedules/shifts/{id}/      # 更新班次
DELETE /api/schedules/shifts/{id}/      # 删除班次

# 排班计划
GET    /api/schedules/schedules/        # 排班列表（支持筛选、搜索、排序）
POST   /api/schedules/schedules/        # 创建排班
POST   /api/schedules/schedules/batch_create/    # 批量排班
POST   /api/schedules/schedules/calendar_view/   # 日历视图
GET    /api/schedules/schedules/{id}/   # 排班详情
PUT    /api/schedules/schedules/{id}/   # 更新排班
DELETE /api/schedules/schedules/{id}/   # 删除排班

# 调班申请
GET    /api/schedules/shift-requests/   # 调班申请列表
POST   /api/schedules/shift-requests/   # 创建调班申请
POST   /api/schedules/shift-requests/{id}/approve/ # 调班审核
GET    /api/schedules/shift-requests/my_requests/  # 我的调班申请
GET    /api/schedules/shift-requests/pending/      # 待审批列表
GET    /api/schedules/shift-requests/{id}/ # 调班申请详情
PUT    /api/schedules/shift-requests/{id}/ # 更新调班申请
DELETE /api/schedules/shift-requests/{id}/ # 删除调班申请
```

**筛选参数示例**：
- 排班筛选：`/api/schedules/schedules/?employee=1&shift=2&work_date=2026-01-28`
- 排班搜索：`/api/schedules/schedules/?search=张三`
- 排班排序：`/api/schedules/schedules/?ordering=-work_date`
- 调班申请筛选：`/api/schedules/shift-requests/?requester=1&status=PENDING`

**考勤管理 API (`/api/attendance/`)**
```
# 考勤记录管理
GET    /api/attendance/              # 考勤记录列表（支持筛选、搜索、排序）
POST   /api/attendance/              # 创建考勤记录（管理员手动创建）
GET    /api/attendance/{id}/         # 考勤记录详情
PUT    /api/attendance/{id}/         # 更新考勤记录
DELETE /api/attendance/{id}/         # 删除考勤记录

# 签到签退
POST   /api/attendance/clock_in/     # 员工签到
POST   /api/attendance/clock_out/    # 员工签退

# 统计与异常处理
POST   /api/attendance/statistics/   # 考勤统计
POST   /api/attendance/{id}/correct/ # 异常处理（修改考勤状态）

# 员工查询
GET    /api/attendance/my_attendance/ # 我的考勤记录（员工查询）
```

**筛选参数示例**：
- 考勤记录筛选：`/api/attendance/?employee=1&status=LATE`
- 考勤记录搜索：`/api/attendance/?search=张三`
- 考勤记录排序：`/api/attendance/?ordering=-clock_in_time`
- 我的考勤查询：`/api/attendance/my_attendance/?employee_id=1&start_date=2026-01-01&end_date=2026-01-31`

#### 计划中

```
/api/leaves/          # 请假申请
/api/salaries/        # 薪资记录
/api/analytics/       # 统计数据
```

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
