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

### `leaves` 应用 - 请假管理

请假管理模块，负责员工请假申请、审批流程管理。

#### 文件结构与职责

```
leaves/
├── __init__.py
├── admin.py              # Django Admin 配置
├── apps.py               # 应用配置
├── migrations/           # 数据库迁移文件
│   └── 0001_initial.py  # 创建 LeaveRequest 表
├── models.py             # 数据模型定义
├── serializers.py        # DRF 序列化器
├── urls.py               # 应用 URL 路由
└── views.py              # API 视图
```

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

**架构设计要点**：
- 使用 `TextChoices` 定义枚举类型，提供类型安全和中文标签
- `approver` 外键为可选，允许系统自动审批（如需要）
- 审批状态默认为 PENDING（待审批）
- 数据库索引优化查询性能：employee, status, created_at, start_time

#### 序列化器设计

| 序列化器 | 用途 | 特点 |
|---------|------|------|
| `LeaveRequestSerializer` | 请假申请详情 CRUD | 支持完整字段，包含员工名、岗位、审批人等显示 |
| `LeaveRequestListSerializer` | 请假申请列表展示 | 简化字段，提升列表查询性能 |
| `LeaveRequestCreateSerializer` | 请假申请创建 | 验证请假时间（结束时间必须大于开始时间） |
| `LeaveRequestApprovalSerializer` | 请假审批 | 验证审批参数 |
| `LeaveRequestMySerializer` | 我的请假申请 | 员工查看自己的请假记录 |

**设计理念**：
- 分离序列化器职责，避免单个序列化器过于复杂
- 创建序列化器包含业务逻辑验证（时间范围检查）
- 我的请假序列化器仅返回员工可见的信息

#### 视图设计：LeaveRequestViewSet

基于 DRF 的 `ModelViewSet`，提供标准的 CRUD 操作和特殊业务接口：

| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/leaves/` | 支持筛选、搜索、排序 |
| 创建 | POST | `/api/leaves/` | 标准操作，返回统一格式 |
| 详情 | GET | `/api/leaves/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/leaves/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/leaves/{id}/` | 标准操作 |
| 我的申请 | GET | `/api/leaves/my_requests/` | 查询当前员工的请假记录 |
| 待审批 | GET | `/api/leaves/pending/` | 管理员查看待审批列表 |
| 审批 | POST | `/api/leaves/{id}/approve/` | 批准或拒绝请假申请 |

**高级筛选功能**：
- **字段筛选**：使用 `django_filters` 的 `DjangoFilterBackend`
  - 按员工筛选：`?employee=1`
  - 按请假类型筛选：`?leave_type=SICK`
  - 按状态筛选：`?status=PENDING`
  - 组合筛选：`?employee=1&status=APPROVED`
- **全文搜索**：使用 DRF 的 `SearchFilter`
  - 搜索字段：员工姓名、员工电话、请假原因、审批意见
  - 示例：`?search=张三` 或 `?search=身体不适`
- **排序**：使用 DRF 的 `OrderingFilter`
  - 支持字段：创建时间、开始时间、结束时间
  - 示例：`?ordering=-created_at`（倒序）

**我的请假申请接口**：
- 输入参数：`employee_id`（必填）、`status`（可选）
- 返回当前员工的所有请假记录
- 支持按状态筛选（如只查询已通过的请假）

**待审批列表接口**：
- 返回所有状态为 PENDING 的请假申请
- 管理员专用接口（权限待后续实现）

**请假审批接口**：
- 输入参数：`approve`（是否批准）、`approval_remark`（审批意见）、`approver_id`（审批人ID）
- 检查申请状态，只有 PENDING 状态的申请可以被审批
- 批准时状态变为 APPROVED，拒绝时状态变为 REJECTED
- 记录审批人和审批意见，便于审计追溯

#### 路由配置

```python
router = DefaultRouter()
router.register(r'', LeaveRequestViewSet, basename='leave-request')
```

**路由映射**：
- 空字符串 `''` → 主路由为 `/api/leaves/`
- `basename='leave-request'` → 用于生成 URL 名称（如 `leave-request-detail`）

#### Django Admin 配置

`LeaveRequestAdmin` 类提供后台管理界面：
- 列表展示：id, 员工姓名, 请假类型, 开始时间, 结束时间, 请假天数, 审批状态, 审批人, 创建时间
- 过滤器：按请假类型、审批状态、创建时间、开始时间筛选
- 搜索：支持员工姓名、员工电话、原因、审批意见搜索
- 日期分层导航：按开始时间浏览
- 字段分组：基本信息、审批信息、时间信息（可折叠）
- 只读字段：创建时间、更新时间、请假天数

#### 业务流程

**请假申请流程**：
1. 员工提交请假申请（选择类型、时间、填写原因）
2. 系统创建请假申请，状态为 PENDING（待审批）
3. 管理员在待审批列表中查看申请
4. 管理员审批（批准/拒绝，填写意见）
5. 系统更新申请状态，记录审批人和审批意见
6. 员工查看审批结果

**请假天数计算逻辑**：
```
请假天数 = 结束日期 - 开始日期 + 1
（包含开始和结束日期，最少 1 天）
```

#### 与其他模块的关系

| 模块 | 关系 | 说明 |
|------|------|------|
| `employees` | 依赖 | `LeaveRequest.employee` 外键关联 `EmployeeProfile` |
| `attendance` | 联动 | 请假期间的考勤记录需要特殊处理 |
| `salaries` | 被依赖 | 薪资计算需要考虑请假天数（影响工资） |

---

### `salaries` 应用 - 薪资管理

薪资管理模块，负责薪资计算、薪资记录生成、异常申诉处理。

#### 文件结构与职责

```
salaries/
├── __init__.py
├── admin.py              # Django Admin 配置
├── apps.py               # 应用配置
├── migrations/           # 数据库迁移文件
│   └── 0001_initial.py  # 创建 SalaryRecord 和 Appeal 表
├── models.py             # 数据模型定义
├── serializers.py        # DRF 序列化器
├── urls.py               # 应用 URL 路由
└── views.py              # API 视图
```

#### 核心模型

**SalaryRecord 模型** - 薪资记录
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

**Appeal 模型** - 异常申诉
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

**架构设计要点**：
- 使用 `TextChoices` 定义枚举类型，提供类型安全和中文标签
- `total_salary` 字段在保存时自动计算（基础工资 + 岗位津贴 + 加班费 - 扣款）
- 使用 `unique_together = [['employee', 'year_month']]` 防止重复生成薪资
- 薪资申诉创建时，自动将关联的薪资记录状态更新为申诉中（APPEALED）
- 数据库索引优化查询性能：employee + year_month, year_month, status

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

**岗位津贴配置**（位于 `views.py`）：
```python
POSITION_ALLOWANCE_MAP = {
    'CHEF': 800,       # 厨师
    'PASTRY': 700,     # 面点
    'PREP': 500,       # 切配
    'CLEANER': 300,    # 保洁
    'SERVER': 400,     # 服务员
    'MANAGER': 1000,   # 经理
}
DEFAULT_BASE_SALARY = 3000  # 默认基本工资
```

#### 序列化器设计

| 序列化器 | 用途 | 特点 |
|---------|------|------|
| `SalaryRecordSerializer` | 薪资记录详情 CRUD | 支持完整字段，包含员工名、岗位、状态显示 |
| `SalaryRecordListSerializer` | 薪资记录列表展示 | 简化字段，提升列表查询性能 |
| `SalaryRecordCreateSerializer` | 薪资记录创建 | 验证唯一性（员工+年月）、金额非负 |
| `SalaryGenerateSerializer` | 薪资生成请求 | 验证年月格式、员工ID列表 |
| `SalaryAdjustSerializer` | 薪资调整请求 | 验证调整金额、调整原因（必填） |
| `AppealSerializer` | 异常申诉详情 CRUD | 支持完整字段，包含审批人、审批意见 |
| `AppealListSerializer` | 异常申诉列表展示 | 简化字段，提升列表查询性能 |
| `AppealCreateSerializer` | 异常申诉创建 | 验证目标记录ID是否存在 |
| `AppealApprovalSerializer` | 异常申诉审批 | 验证审批参数 |
| `MyAppealSerializer` | 我的申诉序列化器 | 员工查看自己的申诉记录 |

**设计理念**：
- 分离序列化器职责，避免单个序列化器过于复杂
- 列表使用简化版序列化器，减少不必要的数据传输
- 创建序列化器包含唯一性验证（同一员工同一月份只能有一条薪资记录）
- 调整序列化器要求必填调整原因，便于审计追溯

#### 视图设计

**SalaryRecordViewSet** - 薪资记录管理

| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/salaries/` | 支持筛选、搜索、排序 |
| 创建 | POST | `/api/salaries/` | 标准操作，返回统一格式 |
| 详情 | GET | `/api/salaries/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/salaries/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/salaries/{id}/` | 标准操作 |
| 薪资生成 | POST | `/api/salaries/generate/` | 根据考勤数据自动计算月薪 |
| 薪资调整 | POST | `/api/salaries/{id}/adjust/` | 管理员手动调整金额（必填原因） |
| 发布薪资 | POST | `/api/salaries/{id}/publish/` | 将状态从草稿改为已发布 |
| 我的薪资 | GET | `/api/salaries/my-salaries/` | 员工查询自己的薪资记录 |

**薪资生成接口逻辑**：
1. 验证年月格式（YYYY-MM）
2. 计算该月的起止日期
3. 获取需要生成薪资的员工（可指定员工ID列表，或所有在职员工）
4. 对每个员工：
   - 检查是否已存在薪资记录（如存在则跳过）
   - 统计考勤数据：迟到次数、缺卡次数、总加班时长、出勤天数
   - 统计请假天数
   - 计算各项薪资组成：基本工资、岗位津贴、加班费、扣款
   - 创建薪资记录，状态为 DRAFT（草稿）
5. 返回生成统计：创建数量、跳过数量、错误列表

**薪资调整接口逻辑**：
- 接收调整参数：基础工资、岗位津贴、加班费、扣款、调整原因（必填）
- 更新薪资字段
- 在备注中添加调整记录（原因 + 时间戳）
- 更新状态为 ADJUSTED（已调整）

**AppealViewSet** - 异常申诉管理

| 操作 | HTTP 方法 | 端点 | 说明 |
|------|----------|------|------|
| 列表 | GET | `/api/appeals/` | 支持筛选、搜索、排序 |
| 创建 | POST | `/api/appeals/` | 标准操作，返回统一格式 |
| 详情 | GET | `/api/appeals/{id}/` | 标准操作 |
| 更新 | PUT/PATCH | `/api/appeals/{id}/` | 标准操作 |
| 删除 | DELETE | `/api/appeals/{id}/` | 标准操作 |
| 申诉审批 | POST | `/api/appeals/{id}/approve/` | 批准或拒绝申诉（自动更新薪资状态） |
| 待审批列表 | GET | `/api/appeals/pending/` | 管理员查看待审批列表 |
| 我的申诉 | GET | `/api/appeals/my-appeals/` | 员工查询自己的申诉记录 |

**申诉审批接口逻辑**：
- 检查申诉状态，只有 PENDING 状态的申诉可以被审批
- 批准时：状态变为 APPROVED
- 拒绝时：状态变为 REJECTED；如果是薪资申诉，恢复薪资记录状态为 PUBLISHED
- 记录审批人和审批意见，便于审计追溯

#### 路由配置

```python
router = DefaultRouter()
router.register(r'salaries', SalaryRecordViewSet, basename='salary-record')
router.register(r'appeals', AppealViewSet, basename='appeal')
```

**路由映射**：
- `/api/salaries/` → 薪资记录管理
- `/api/appeals/` → 异常申诉管理

#### Django Admin 配置

**SalaryRecordAdmin** - 薪资记录管理界面
- 列表展示：id, 员工姓名, 岗位, 年月, 薪资组成, 统计数据, 状态, 创建时间
- 过滤器：状态、年月、岗位、创建时间
- 搜索：员工姓名、电话、备注
- 日期分层导航：按创建时间浏览
- 字段分组：基本信息、薪资组成、统计数据、备注、时间信息（可折叠）
- 只读字段：创建时间、更新时间、实发工资

**AppealAdmin** - 异常申诉管理界面
- 列表展示：id, 申诉类型, 申诉员工, 目标记录, 状态, 审批人, 创建时间
- 过滤器：申诉类型、状态、创建时间
- 搜索：员工姓名、申诉原因、审批意见
- 日期分层导航：按创建时间浏览
- 字段分组：申诉信息、审批信息、时间信息（可折叠）
- 只读字段：创建时间、更新时间

#### 业务流程

**薪资生成流程**：
1. 管理员选择年月（可选：选择员工）
2. 调用薪资生成接口
3. 系统统计每个员工的考勤数据（迟到、缺卡、加班时长）
4. 系统根据薪资计算规则自动计算各项金额
5. 系统创建薪资记录，状态为 DRAFT（草稿）
6. 管理员审核并调整（如需要）
7. 管理员发布薪资，状态变为 PUBLISHED（已发布）

**薪资申诉流程**：
1. 员工查看薪资记录，发现异议
2. 员工提交薪资申诉（填写申诉原因）
3. 系统创建申诉，状态为 PENDING，薪资记录状态变为 APPEALED
4. 管理员在待审批列表中查看申诉
5. 管理员处理申诉：
   - 批准：调整薪资金额，申诉状态变为 APPROVED，薪资状态变为 ADJUSTED
   - 拒绝：填写审批意见，申诉状态变为 REJECTED，薪资状态恢复为 PUBLISHED
6. 员工查看处理结果

#### 与其他模块的关系

| 模块 | 关系 | 说明 |
|------|------|------|
| `employees` | 依赖 | `SalaryRecord.employee` 外键关联 `EmployeeProfile` |
| `attendance` | 依赖 | 薪资计算需要考勤数据（迟到次数、缺卡次数、加班时长） |
| `leaves` | 依赖 | 薪资计算需要考虑请假天数（影响工资） |
| `schedules` | 依赖 | 薪资计算需要排班数据（统计出勤天数） |

**数据依赖关系**：
- 薪资计算依赖于考勤模块的数据统计
- 考勤统计依赖于排班模块的班次定义
- 请假数据影响薪资计算（请假期间的工资处理）

---

### `analytics` 应用 - 统计分析

统计分析模块，负责跨模块的数据聚合和报表生成，为 Dashboard 和统计页面提供数据支持。

#### 文件结构与职责

```
analytics/
├── __init__.py
├── admin.py              # Django Admin 配置（空）
├── apps.py               # 应用配置
├── migrations/           # 数据库迁移文件（空，无模型）
├── models.py             # 数据模型定义（空，使用其他应用模型）
├── urls.py               # 应用 URL 路由
└── views.py              # 统计分析视图
```

#### 架构设计要点

**无模型设计**：
- `analytics` 应用没有自己的数据模型
- 直接使用其他应用的模型进行数据聚合
- 避免数据冗余和同步问题

**视图函数而非 ViewSet**：
- 使用 `@api_view` 装饰器定义视图函数
- 每个接口对应一个统计维度
- 返回数据格式专为 ECharts 优化

**路由配置**：
```python
# analytics/urls.py
urlpatterns = [
    path("employees/", views.employee_statistics, name="employee_statistics"),
    path("attendance/", views.attendance_statistics, name="attendance_statistics"),
    path("salaries/", views.salary_statistics, name="salary_statistics"),
    path("overview/", views.overview_statistics, name="overview_statistics"),
]
```

#### 统计接口设计

**人员统计接口** (`employee_statistics`)
- **数据源**：`EmployeeProfile` 模型
- **统计维度**：
  - 总人数：在职员工总数
  - 岗位分布：各岗位人数统计（饼图数据）
  - 持证率：健康证、厨师等级证持有率
  - 入职状态分布：在职/离职/停薪留职
- **聚合操作**：使用 `Count` 聚合函数

**考勤统计接口** (`attendance_statistics`)
- **数据源**：`AttendanceRecord`、`Schedule` 模型
- **统计维度**：
  - 出勤率：实到 / 应到 × 100%
  - 状态分布：正常/迟到/早退/缺卡/异常（饼图数据）
  - 日期趋势：每日考勤状态变化（折线图数据）
  - 岗位维度：各岗位考勤对比
- **查询参数**：支持日期范围筛选或相对时间（最近 N 天）

**薪资统计接口** (`salary_statistics`)
- **数据源**：`SalaryRecord`、`EmployeeProfile` 模型
- **统计维度**：
  - 月度趋势：每月薪资支出（折线图数据）
  - 岗位对比：各岗位平均薪资（柱状图数据）
  - 薪资构成：基本工资/岗位津贴/加班费/扣款（饼图数据）
- **过滤条件**：仅统计已发布（`PUBLISHED`）和已调整（`ADJUSTED`）的记录

**总览统计接口** (`overview_statistics`)
- **数据源**：所有核心模型
- **统计维度**：
  - 今日概览：应到/实到/请假/异常
  - 待办事项：待审批请假、薪资草稿数量
  - 总览统计：员工总数、岗位总数
  - 本月考勤：迟到/缺卡统计
- **用途**：Dashboard 首页数据展示

#### 数据格式设计（适配 ECharts）

**饼图数据格式**：
```python
{
  "labels": ["厨师", "面点", "切配", "保洁", "服务员", "经理"],
  "data": [5, 3, 8, 4, 6, 2]
}
```

**折线图数据格式**：
```python
[
  {"date": "2026-01-21", "normal": 8, "late": 1, "missing": 0},
  {"date": "2026-01-22", "normal": 9, "late": 0, "missing": 1}
]
```

**柱状图数据格式**：
```python
[
  {"position": "厨师", "avg_salary": 4500},
  {"position": "面点", "avg_salary": 3800}
]
```

#### 路由配置

```python
# config/urls.py
urlpatterns = [
    # ...
    path("api/analytics/", include("analytics.urls")),
]
```

**路由映射**：
- `/api/analytics/employees/` → 人员统计
- `/api/analytics/attendance/` → 考勤统计
- `/api/analytics/salaries/` → 薪资统计
- `/api/analytics/overview/` → 总览统计

#### 性能优化策略

1. **聚合查询**：使用 Django ORM 的 `Count`、`Sum`、`Avg` 减少数据库查询次数
2. **索引利用**：利用其他应用定义的数据库索引（如 `employee_id`、`created_at`）
3. **空数据处理**：无数据时返回空列表而非 404，避免前端错误处理
4. **中文标签映射**：在 Python 层完成枚举值到中文的转换，减轻前端负担

#### 与其他模块的关系

| 模块 | 关系 | 说明 |
|------|------|------|
| `employees` | 依赖 | 人员统计依赖 `EmployeeProfile` 模型 |
| `attendance` | 依赖 | 考勤统计依赖 `AttendanceRecord` 模型 |
| `salaries` | 依赖 | 薪资统计依赖 `SalaryRecord` 模型 |
| `schedules` | 依赖 | 考勤统计需要 `Schedule` 模型计算应出勤人数 |
| `leaves` | 依赖 | 总览统计需要 `LeaveRequest` 模型 |

#### 架构设计意义

**跨模块数据聚合**：
- 统计分析是典型的跨模块业务
- 将所有统计接口集中在一个应用中，便于维护
- 避免在各应用中分散实现统计逻辑

**前后端分离优化**：
- 数据格式专为 ECharts 优化
- 前端无需复杂的数据转换
- 减少网络传输和前端计算负担

**无状态设计**：
- 不存储统计数据，每次实时计算
- 确保数据的实时性和准确性
- 避免数据同步和一致性问题

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
  - `LoginView.vue` - 登录页面（已实现）
  - `RegisterView.vue` - 注册页面（占位）

#### `src/components/` - 公共组件

可复用的 Vue 组件，如：
- 数据表格组件
- 表单组件
- 图表组件
- 布局组件（侧边栏、顶部导航等）

#### `src/api/` - API 请求封装

封装与后端 API 的交互逻辑：

**`request.js`** - Axios 实例配置
- 创建 axios 实例，配置 baseURL 为 `/api`
- 请求拦截器：自动添加 Authorization 头（从 localStorage 读取 token）
- 响应拦截器：
  - 统一处理后端返回格式 `{code, message, data}`
  - 处理 HTTP 错误状态（401、403、404、500 等）
  - 401 时自动清除 token 并跳转登录页
- 超时设置：10 秒

**`auth.js`** - 认证相关 API
- `login(username, password)` - 用户登录
- `register(data)` - 用户注册
- `getUserInfo(id)` - 获取用户信息

- `analytics.js` - 统计分析 API（已实现）
- `employee.js` - 员工档案 API（计划中）
- `schedule.js` - 排班管理 API（计划中）
- `attendance.js` - 考勤管理 API（计划中）
- `leave.js` - 请假管理 API（计划中）
- `salary.js` - 薪资管理 API（计划中）

**`analytics.js`** - 统计分析 API
- `getEmployeeStatistics()` - 获取人员统计数据（岗位分布、持证率等）
- `getAttendanceStatistics(params)` - 获取考勤统计数据（支持日期范围筛选）
- `getSalaryStatistics(params)` - 获取薪资统计数据（支持月份范围筛选）
- `getOverviewStatistics()` - 获取总览统计数据（Dashboard 首页专用）

**`employee.js`** - 员工档案 API
- `getEmployeeList(params)` - 获取员工列表（支持分页、筛选、搜索）
- `getEmployeeDetail(id)` - 获取员工详情
- `createEmployee(data)` - 创建员工档案
- `updateEmployee(id, data)` - 更新员工档案（完整更新）
- `patchEmployee(id, data)` - 部分更新员工档案
- `deleteEmployee(id)` - 删除员工档案

- `schedule.js` - 排班管理 API（计划中）
- `attendance.js` - 考勤管理 API（计划中）
- `leave.js` - 请假管理 API（计划中）
- `salary.js` - 薪资管理 API（计划中）

#### `src/router/` - 路由配置

**`index.js`** - 路由配置文件

**已配置路由**：
- `/login` - 登录页面（无需认证）
- `/register` - 注册页面（无需认证）
- `/admin` - 管理员首页（需要 ADMIN 角色）
- `/admin/employees` - 人员档案管理页面（需要 ADMIN 角色）
- `/employee` - 员工首页（需要 EMPLOYEE 角色）
- `/` - 默认重定向到登录页
- `/:pathMatch(.*)*` - 404 页面（重定向到登录页）

**导航守卫功能**：
- 检查路由是否需要认证（`meta.requiresAuth`）
- 未登录用户访问受保护路由时，重定向到登录页
- 检查用户角色权限（`meta.role`）
- 角色不匹配时，自动跳转到对应角色的首页
- 已登录用户访问登录页时，自动跳转到对应角色的首页

**路由元信息**：
- `requiresAuth` - 是否需要登录
- `role` - 所需角色（ADMIN/EMPLOYEE）

#### `src/stores/` - Pinia 状态管理

**`user.js`** - 用户状态管理

**状态字段**：
- `token` - 登录凭证（存储在 localStorage）
- `userInfo` - 用户信息对象（包含 id、username、role 等）

**计算属性**：
- `isLoggedIn` - 是否已登录
- `userRole` - 获取用户角色
- `isAdmin` - 是否是管理员
- `isEmployee` - 是否是员工

**操作方法**：
- `login(username, password)` - 用户登录
  - 调用登录 API
  - 保存 token 和用户信息到 store
  - 持久化到 localStorage
- `logout()` - 退出登录
  - 清空 store 中的 token 和用户信息
  - 清除 localStorage
- `updateUserInfo(userInfo)` - 更新用户信息

**计划中**（待实现）：
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

### 已实现组件

#### 登录页面 (`LoginView.vue`)

**布局结构**：
- 左右分屏设计，充满视口（100vw × 100vh）
- 左侧品牌区域（52%）：展示系统品牌形象
- 右侧登录区域（48%）：登录表单和操作区

**左侧品牌区域特性**：
- 橙色渐变背景（#FF6B35 → #FF8C42 → #F7C52D）
- Logo 动画效果（浮动 + 光晕脉冲）
- 功能特性网格（员工管理、智能排班、考勤打卡、薪资核算）
- 浮动装饰元素（餐具 emoji）
- 底部统计信息（500+ 企业用户、99.9% 稳定性）
- 背景图案叠加层和渐变叠加层

**右侧登录表单特性**：
- 表单验证：
  - 用户名：必填，最少 2 个字符
  - 密码：必填，最少 4 个字符
- 记住账号功能（持久化到 localStorage）
- 忘记密码链接（提示联系管理员）
- 登录按钮加载状态
- 支持回车键提交

**交互体验**：
- 表单字段焦点效果（边框变色 + 阴影）
- 按钮悬停效果（上移 + 箭头滑动）
- 输入框前缀图标（用户、锁图标）
- 统一的错误提示（Element Plus Message）

**响应式设计**：
- 使用 `clamp()` 实现流畅响应式
- 平板竖屏（≤768px）：上下布局
- 手机（≤480px）：优化间距和字体大小

**技术实现**：
- Vue 3 Composition API（`<script setup>`）
- Element Plus 组件库（el-form、el-input、el-button、el-checkbox）
- Pinia 状态管理（调用 userStore.login）
- Vue Router 导航（登录成功后根据角色跳转）
- CSS 变量定义全局主题色
- 自定义动画效果（浮动、渐入、脉冲）

**路由跳转逻辑**：
- 管理员（ADMIN）→ `/admin`
- 员工（EMPLOYEE）→ `/employee`
- 其他角色 → 保持登录页

#### 注册页面 (`RegisterView.vue`)

**布局结构**：
- 左右分屏设计，充满视口（100vw × 100vh）
- 左侧品牌区域（52%）：展示系统品牌形象和注册优势
- 右侧注册区域（48%）：注册表单和操作区

**左侧品牌区域特性**：
- 橙色渐变背景（#FF6B35 → #FF8C42 → #F7C52D）
- Logo 动画效果（浮动 + 光晕脉冲）
- 注册优势网格（快速入职、安全可靠、移动办公、智能提醒）
- 浮动装饰元素（餐具 emoji）
- 底部统计信息（500+ 企业用户、99.9% 稳定性）
- 背景图案叠加层和渐变叠加层

**右侧注册表单特性**：
- 表单字段：
  - 用户名：必填，最少 2 个字符
  - 密码：必填，最少 4 个字符，支持显示/隐藏切换
  - 确认密码：必填，需与密码一致
  - 手机号：必填，中国手机号格式验证
  - 邮箱：选填，邮箱格式验证
- 注册按钮加载状态
- 已有账号提示链接
- 支持回车键提交

**表单验证逻辑**：
- **用户名验证**：
  - 必填校验
  - 最小长度 2 字符
- **密码验证**：
  - 必填校验
  - 最小长度 4 字符
  - 密码修改时自动重新验证确认密码
- **确认密码验证**：
  - 必填校验
  - 与密码值一致性校验
- **手机号验证**：
  - 必填校验
  - 中国手机号格式（1[3-9]xxxxxxxxx）
- **邮箱验证**：
  - 选填字段
  - 有值时验证邮箱格式

**注册流程**：
1. 用户填写表单
2. 前端验证所有字段
3. 调用后端 `/api/accounts/register/` 接口
4. 注册成功（code 201）：
   - 显示成功提示消息
   - 延迟 1.5 秒后跳转到登录页
5. 注册失败：
   - 显示后端返回的错误信息
   - 用户名已存在时提示"用户名已存在"
   - 网络错误时提示"注册失败，请检查网络连接"

**交互体验**：
- 表单字段焦点效果（边框变色 + 阴影）
- 按钮悬停效果（上移 + 阴影增强）
- 输入框前缀图标（用户、锁、电话、邮件图标）
- 统一的错误提示（Element Plus Message）

**响应式设计**：
- 使用 `clamp()` 实现流畅响应式
- 平板竖屏（≤768px）：上下布局，简化装饰元素
- 手机（≤480px）：优化间距和字体大小

**技术实现**：
- Vue 3 Composition API（`<script setup>`）
- Element Plus 组件库（el-form、el-input、el-button）
- 自定义验证器函数（validatePassword、validateConfirmPassword、validatePhone、validateEmail）
- Vue Router 导航（注册成功后跳转到登录页）
- CSS 变量定义全局主题色
- 自定义动画效果（浮动、渐入、渐出）

**与后端 API 对接**：
- 接口地址：`/api/accounts/register/`
- 请求方法：POST
- 请求参数：`{ username, password, phone, email }`
- 响应格式：`{ code: 201, message: "成功", data: { ... } }`
- 错误处理：检查 `error.response.data.username` 或 `error.response.data.message`

**路由配置**：
- 路径：`/register`
- 无需认证即可访问
- meta 信息：`{ requiresAuth: false }`

---

#### 管理员首页 (`DashboardView.vue`)

**布局结构**：
- 充满视口（100vh）的单页布局
- 顶部导航栏（固定定位，sticky）
- 主内容区域（包含欢迎区、快捷入口、今日概览、待办事项、本月统计）

**顶部导航栏特性**：
- 橙色渐变背景（#FF6B35 → #FF8C42 → #F7C52D）
- Logo 区域（厨师帽图标 + 浮动动画）
- 系统标题："食堂管理系统"
- 日期显示（自动格式化为中文格式）
- 用户信息展示（用户名 + 管理员角色）
- 退出登录按钮（带门图标）

**欢迎区域特性**：
- 动态欢迎语："欢迎回来，{用户名}！"（带挥手动画）
- 当前日期和星期显示（格式：2026年1月28日 星期三）

**快捷入口区域特性**：
- 4 个快捷入口卡片（人员新增、排班制定、考勤异常、薪资生成）
- 每个卡片包含：
  - 食堂相关图标（64px 圆角容器）
  - 功能名称和描述
  - 悬停效果（上移 4px + 阴影增强 + 边框高亮）
  - 箭头指示（悬停时滑动显示）

**今日概览区域特性**：
- 3 个统计卡片（出勤情况、今日请假、今日异常）
- 出勤情况卡片：
  - 显示应到/实到人数对比
  - 绿色边框和数字高亮
- 今日请假卡片：
  - 显示请假人数
  - 橙色边框和数字
- 今日异常卡片：
  - 显示异常记录数
  - 黄色边框和警告色数字

**待办事项区域特性**：
- 列表显示所有待办事项
- 支持的待办类型：
  - 请假审批（🏖️ 图标）
  - 调班审批（🔄 图标）
  - 申诉处理（📝 图标）
  - 薪资发布（自动汇总）
- 每个待办项显示：
  - 类型图标（带渐变背景）
  - 待办标题
  - 类型标签和相对时间（刚刚、X分钟前等）
  - 悬停效果（背景变色 + 箭头显示）
- 空状态：显示庆祝图标和"暂无待办事项"提示

**本月统计区域特性**：
- 3 个统计卡片（员工总数、本月迟到、本月薪资）
- 每个卡片包含：
  - 食堂相关图标（64px 渐变背景）
  - 统计数值（大号字体，橙色）
  - 统计标签（灰色小字）
- 悬停效果（上移 + 阴影增强）

**交互体验**：
- 组件挂载时自动加载总览数据
- Loading 状态显示（区域级）
- 快捷入口点击：显示提示消息（路由功能待实现）
- 待办事项点击：显示提示消息（详情页面待实现）
- 退出登录：清空用户信息并跳转到登录页

**响应式设计**：
- 使用 CSS Grid 自适应布局
- 平板竖屏（≤768px）：
  - 顶部导航栏：垂直布局
  - 所有卡片区域：单列布局
- 手机（≤480px）：
  - 减小内边距和字体大小
  - 优化卡片间距

**技术实现**：
- Vue 3 Composition API（`<script setup>`）
- Element Plus 组件库（el-button、v-loading 指令）
- Pinia 状态管理（获取用户信息）
- Vue Router（页面导航）
- 自定义计算属性：
  - `userName` - 获取用户名
  - `currentDate` - 格式化当前日期
  - `currentDateDisplay` - 完整日期显示（含星期）
- 自定义方法：
  - `loadOverviewData()` - 加载总览数据
  - `formatDate()` - 智能时间格式化
  - `formatSalary()` - 薪资格式化（¥ + 千分位）
  - `getTodoIcon()` - 获取待办类型图标
- CSS 动画：
  - Logo 浮动（上下浮动 8px，3秒循环）
  - 挥手动画（左右摇摆 20 度，2秒循环）
  - 卡片悬停上移（translateY -4px）
  - 箭头滑动（translateX + opacity）

**数据对接**：
- 接口地址：`/api/analytics/overview/`
- 请求方法：GET
- 响应数据包含：
  - `expected_attendance` - 今日应到人数
  - `actual_attendance` - 今日实到人数
  - `today_leaves` - 今日请假人数
  - `today_abnormal` - 今日异常数量
  - `total_employees` - 员工总数
  - `monthly_late` - 本月迟到次数
  - `monthly_salary` - 本月薪资支出
  - `pending_leaves` - 待审批请假列表
  - `pending_shift_swaps` - 待审批调班列表
  - `pending_appeals` - 待审批申诉列表
  - `draft_salaries` - 待发布薪资数量

**设计亮点**：
1. **食堂主题贯穿**：使用暖色调（橙色、黄色）和食堂相关图标（厨师帽、餐具、食物）
2. **动画丰富但不干扰**：Logo 浮动、挥手、卡片悬停等微交互提升用户体验
3. **信息层次清晰**：从欢迎语 → 快捷入口 → 今日数据 → 待办事项 → 本月统计，符合阅读习惯
4. **空状态友好**：无待办事项时显示庆祝图标，避免空列表的枯燥感
5. **智能时间格式化**：自动计算相对时间（刚刚、X分钟前、X小时前、X天前），提升可读性

**路由配置**：
- 路径：`/admin`
- 需要认证：是
- 需要角色：ADMIN
- meta 信息：`{ requiresAuth: true, role: 'ADMIN' }`

---

#### 人员档案管理页面 (`EmployeeManageView.vue`)

**布局结构**：
- 充满视口（100vh）的单页布局
- 顶部操作栏：新增按钮 + 搜索框 + 筛选器
- 员工列表表格：显示员工信息和操作按钮
- 分页组件：底部居中显示
- 对话框：新增/编辑对话框、详情对话框

**顶部操作栏特性**：
- 新增员工按钮（橙色主色调）
- 搜索框：支持姓名、电话、身份证号搜索，带清空功能
- 岗位筛选器：厨师、面点、切配、保洁、服务员、经理
- 状态筛选器：在职、离职、停薪留职
- 响应式布局：小屏幕下垂直排列

**员工列表表格特性**：
- 显示字段：ID、姓名、性别、岗位、手机号、身份证号、入职日期、状态、操作
- 岗位列彩色标签：
  - 厨师 → warning (橙色)
  - 面点 → danger (红色)
  - 切配 → info (蓝色)
  - 保洁 → success (绿色)
  - 服务员 → 默认灰色
  - 经理 → primary (深蓝色)
- 状态列彩色徽章：
  - 在职 → success (绿色)
  - 离职 → info (灰色)
  - 停薪留职 → warning (橙色)
- 操作按钮：查看、编辑、删除（link 样式）
- 表头样式：浅米色背景 (#FFF8F0)

**分页组件特性**：
- 支持每页 10、20、50、100 条记录
- 显示总记录数
- 支持页码跳转
- 上一页/下一页导航

**新增/编辑对话框特性**：
- 3 个标签页：基础信息、岗位信息、资质证书
- 基础信息标签页：
  - 姓名（必填，2-20字符）
  - 性别（单选：男/女）
  - 手机号（必填，中国手机号格式）
  - 身份证号（选填）
  - 家庭住址（选填，多行文本框）
- 岗位信息标签页：
  - 岗位（下拉选择）
  - 入职日期（日期选择器）
  - 状态（下拉选择）
- 资质证书标签页：
  - 健康证号（选填）
  - 健康证有效期（选填，日期选择器）
  - 健康证图片 URL（选填）
  - 厨师等级证（选填，下拉选择）
- 表单验证：所有必填字段都有验证规则
- 对话框关闭时自动重置表单

**详情对话框特性**：
- 使用 `el-descriptions` 组件展示
- 2 列布局，带边框
- 显示所有字段信息
- 姓名显示格式化标签
- 岗位和状态使用彩色标签
- 空字段显示 "-"

**删除确认特性**：
- 二次确认对话框（警告类型）
- 显示员工姓名提示
- 确认后调用删除 API
- 删除成功后刷新列表

**交互体验**：
- 组件挂载时自动加载员工列表
- Loading 状态显示（表格级别）
- 操作成功/失败提示
- 搜索和筛选自动触发第一页
- 分页变化时自动加载数据
- 删除操作需要确认，防止误操作

**响应式设计**：
- 桌面端：操作栏水平布局
- 平板竖屏（≤768px）：操作栏垂直布局
- 手机（≤480px）：优化间距和字体大小

**技术实现**：
- Vue 3 Composition API（`<script setup>`）
- Element Plus 组件库：
  - `el-table` - 数据表格
  - `el-dialog` - 对话框
  - `el-form` - 表单
  - `el-tabs` - 标签页
  - `el-pagination` - 分页
  - `el-select` - 下拉选择
  - `el-input` - 输入框
  - `el-date-picker` - 日期选择
  - `el-message-box` - 确认对话框
- 响应式数据管理：
  - `ref()` - 单个值响应式（loading、dialogVisible 等）
  - `reactive()` - 对象响应式（pagination、filters、formData）
  - `computed()` - 计算属性（dialogTitle）
- 自定义样式覆盖（`:deep()` 选择器）
- 表单验证（el-form 的 rules 属性）

**数据对接**：
- 接口地址：`/api/employees/`
- 请求方法：
  - GET - 获取列表、获取详情
  - POST - 创建员工
  - PUT - 更新员工
  - DELETE - 删除员工
- 查询参数：
  - `page` - 页码
  - `page_size` - 每页数量
  - `position` - 岗位筛选
  - `status` - 状态筛选
  - `search` - 搜索关键字
  - `ordering` - 排序字段
- 响应格式：
  ```json
  {
    "code": 200,
    "message": "成功",
    "data": {
      "count": 100,
      "results": [...],
      "next": null,
      "previous": null
    }
  }
  ```

**颜色映射函数**：
- `getPositionTagType(position)` - 岗位标签颜色映射
- `getStatusTagType(status)` - 状态徽章颜色映射

**设计亮点**：
1. **食堂主题配色**：橙色主题贯穿整个页面
2. **标签页设计**：新增/编辑表单使用标签页分组，清晰易用
3. **彩色标签系统**：岗位和状态使用不同颜色，直观识别
4. **表单验证完善**：所有必填字段都有验证，防止无效数据提交
5. **删除二次确认**：防止误操作删除重要数据
6. **响应式设计**：适配不同屏幕尺寸
7. **Loading 状态**：提升用户体验，明确数据加载状态

**路由配置**：
- 路径：`/admin/employees`
- 需要认证：是
- 需要角色：ADMIN
- meta 信息：`{ requiresAuth: true, role: 'ADMIN' }`

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

**请假管理 API (`/api/leaves/`)**
```
# 请假申请管理
GET    /api/leaves/                    # 请假申请列表（支持筛选、搜索、排序）
POST   /api/leaves/                    # 创建请假申请
GET    /api/leaves/{id}/               # 请假申请详情
PUT    /api/leaves/{id}/               # 更新请假申请
DELETE /api/leaves/{id}/               # 删除请假申请

# 自定义接口
GET    /api/leaves/my_requests/        # 我的请假申请（员工查询）
GET    /api/leaves/pending/            # 待审批列表（管理员）
POST   /api/leaves/{id}/approve/       # 请假审批（批准/拒绝）
```

**筛选参数示例**：
- 请假申请筛选：`/api/leaves/?employee=1&leave_type=SICK&status=PENDING`
- 请假申请搜索：`/api/leaves/?search=张三` 或 `?search=身体不适`
- 请假申请排序：`/api/leaves/?ordering=-created_at`
- 我的请假查询：`/api/leaves/my_requests/?employee_id=1&status=APPROVED`

#### 计划中

```
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
