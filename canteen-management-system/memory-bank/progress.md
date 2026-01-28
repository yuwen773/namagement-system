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

### ✅ 步骤 2.2：创建员工档案模型与 API

**实施内容**：

1. **创建 EmployeeProfile 模型** (`employees/models.py`)
   - 字段定义：
     - 基础信息：`name`, `gender`, `phone`, `id_card`（唯一）, `address`
     - 岗位信息：`position`, `entry_date`, `status`
     - 资质证书：`health_certificate_no`, `health_certificate_expiry`, `health_certificate_url`, `chef_certificate_level`
     - 时间戳：`created_at`, `updated_at`
   - 枚举类定义：`Gender`, `Position`, `Status` 使用 Django 的 `TextChoices`
   - 岗位类型：厨师(CHEF)、面点(PASTRY)、切配(PREP)、保洁(CLEANER)、服务员(SERVER)、经理(MANAGER)

2. **创建序列化器** (`employees/serializers.py`)
   - `EmployeeProfileSerializer` - 员工档案详情序列化器（支持 CRUD 操作）
   - `EmployeeProfileListSerializer` - 员工列表序列化器（简化版）
   - 身份证号唯一性验证（更新时排除当前记录）

3. **创建视图集** (`employees/views.py`)
   - `EmployeeProfileViewSet` - 基于 DRF 的 `ModelViewSet`
   - 支持筛选：按岗位(`position`)、状态(`status`)筛选
   - 支持搜索：按姓名(`name`)、电话(`phone`)、身份证号(`id_card`)搜索
   - 支持排序：按创建时间、入职日期、姓名排序
   - 统一的响应格式：`{code, message, data}`

4. **配置 URL 路由**
   - 创建 `employees/urls.py` - 使用 DRF 的 `DefaultRouter`
   - 更新 `config/urls.py` - 包含 employees 路由：`/api/employees/`

5. **注册 Django Admin** (`employees/admin.py`)
   - 配置 `EmployeeProfileAdmin` 类
   - 列表显示字段：id, name, gender, phone, position, entry_date, status, created_at
   - 过滤器：position, status, gender, created_at
   - 搜索字段：name, phone, id_card
   - 字段分组展示：基础信息、岗位信息、资质证书、时间信息

6. **数据库迁移**
   - 创建迁移：`employees/migrations/0001_initial.py`
   - 应用迁移到数据库

7. **新增依赖**
   - 添加 `django-filter` 到 `requirements.txt`
   - 添加 `django_filters` 到 `INSTALLED_APPS`

**API 端点清单**：
```
GET    /api/employees/           # 员工列表（支持筛选和搜索）
POST   /api/employees/           # 创建员工档案
GET    /api/employees/{id}/      # 员工详情
PUT    /api/employees/{id}/      # 更新员工档案
DELETE /api/employees/{id}/      # 删除员工档案
```

**筛选和搜索参数**：
- 筛选：`?position=CHEF&status=ACTIVE`
- 搜索：`?search=张三`
- 排序：`?ordering=-created_at`

**测试验证**：
- ✅ 创建新员工档案，返回 201，所有字段保存成功
- ✅ 获取员工列表，返回 200，支持筛选和搜索
- ✅ 获取员工详情，返回 200，显示完整信息
- ✅ 更新员工信息，返回 200，信息更新成功
- ✅ 删除员工档案，返回 200，删除成功
- ✅ 身份证号唯一性验证生效
- ✅ Django Admin 界面正常显示和管理员工档案

**注意事项**：
- 员工档案（EmployeeProfile）与用户账号（User）是独立概念，需要分别创建
- `id_card` 字段设置为唯一，但可为空，允许部分员工不录入身份证号
- `position` 枚举类型覆盖了食堂行业的所有典型岗位
- 健康证和厨师等级证字段为可选，适应不同岗位需求

---

### ✅ 步骤 2.3：创建排班相关模型与 API

**实施内容**：

1. **创建模型** (`schedules/models.py`)
   - `Shift` 模型：班次定义（name, start_time, end_time, created_at）
   - `Schedule` 模型：排班计划（employee, shift, work_date, is_swapped, created_at）
   - `ShiftSwapRequest` 模型：调班申请（requester, original_schedule, target_date, target_shift, reason, status, approver, approval_remark, created_at）
   - 使用 `unique_together` 防止同一员工在同一日期重复排班

2. **创建序列化器** (`schedules/serializers.py`)
   - `ShiftSerializer` / `ShiftListSerializer` - 班次详情/列表序列化器
   - `ScheduleSerializer` / `ScheduleListSerializer` / `ScheduleDetailSerializer` - 排班详情/列表/完整信息序列化器
   - `ShiftSwapRequestSerializer` / `ShiftSwapRequestListSerializer` - 调班申请详情/列表序列化器
   - `BatchScheduleSerializer` - 批量排班序列化器（支持多员工、日期范围）
   - `ShiftSwapApprovalSerializer` - 调班审批序列化器
   - `CalendarViewSerializer` - 日历视图序列化器

3. **创建视图集** (`schedules/views.py`)
   - `ShiftViewSet` - 班次定义的增删改查操作
   - `ScheduleViewSet` - 排班计划的增删改查
     - `batch_create/` - 批量排班接口
     - `calendar_view/` - 日历视图接口（按日期分组返回排班数据）
   - `ShiftSwapRequestViewSet` - 调班申请的增删改查
     - `approve/` - 调班审核接口（批准/拒绝，自动更新排班）
     - `my_requests/` - 我的调班申请接口
     - `pending/` - 待审批调班申请列表
   - 统一的响应格式：`{code, message, data}`

4. **配置 URL 路由**
   - 创建 `schedules/urls.py` - 使用 DRF 的 `DefaultRouter`
   - 更新 `config/urls.py` - 包含 schedules 路由：`/api/schedules/`

5. **注册 Django Admin** (`schedules/admin.py`)
   - `ShiftAdmin` - 班次定义管理界面
   - `ScheduleAdmin` - 排班计划管理界面（显示员工名、班次名、日期）
   - `ShiftSwapRequestAdmin` - 调班申请管理界面（显示发起人、原定排班、目标排班、审批状态）

6. **数据库迁移**
   - 创建迁移：`schedules/migrations/0001_initial.py`
   - 应用迁移到数据库

**API 端点清单**：
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
POST   /api/schedules/schedules/batch_create/  # 批量排班
POST   /api/schedules/schedules/calendar_view/ # 日历视图
GET    /api/schedules/schedules/{id}/   # 排班详情
PUT    /api/schedules/schedules/{id}/   # 更新排班
DELETE /api/schedules/schedules/{id}/   # 删除排班

# 调班申请
GET    /api/schedules/shift-requests/   # 调班申请列表
POST   /api/schedules/shift-requests/   # 创建调班申请
POST   /api/schedules/shift-requests/{id}/approve/  # 调班审核
GET    /api/schedules/shift-requests/my_requests/   # 我的调班申请
GET    /api/schedules/shift-requests/pending/       # 待审批列表
GET    /api/schedules/shift-requests/{id}/  # 调班申请详情
PUT    /api/schedules/shift-requests/{id}/  # 更新调班申请
DELETE /api/schedules/shift-requests/{id}/  # 删除调班申请
```

**筛选和搜索参数**：
- 排班筛选：`?employee=1&shift=2&work_date=2026-01-28`
- 排班搜索：`?search=张三`
- 排班排序：`?ordering=-work_date`
- 调班申请筛选：`?requester=1&status=PENDING&target_date=2026-01-28`

**测试验证**：
- ✅ 创建班次，返回 200，班次创建成功
- ✅ 查询班次列表，返回 200，显示所有班次
- ✅ 创建排班，返回 200，排班创建成功
- ✅ 批量排班，返回 200，创建 9 条记录（3 个员工 × 3 天）
- ✅ 查询排班列表，返回 200，显示 10 条排班记录
- ✅ 日历视图接口，返回 200，按日期分组显示排班数据
- ✅ Django Admin 界面正常显示和管理排班数据

**注意事项**：
- 批量排班使用 `get_or_create` 避免重复创建
- 调班审核通过后，自动更新排班记录（删除原排班，创建新排班）
- 日历视图返回的数据格式适合前端日历组件使用
- 权限验证待后续实现（目前所有用户都可访问管理接口）

---

### ✅ 步骤 2.4：创建考勤模型与 API

**实施内容**：

1. **创建 AttendanceRecord 模型** (`attendance/models.py`)
   - 字段定义：
     - 关联信息：`employee`（外键）、`schedule`（外键，可为空）
     - 签到信息：`clock_in_time`、`clock_in_location`
     - 签退信息：`clock_out_time`、`clock_out_location`
     - 考勤状态：`status`（枚举：NORMAL, LATE, EARLY_LEAVE, MISSING, ABNORMAL）
     - 异常处理：`correction_remark`
     - 时间戳：`created_at`、`updated_at`
   - 枚举类定义：`Status` 使用 Django 的 `TextChoices`
   - 自动考勤状态判断逻辑（`_calculate_status` 方法）
   - 加班时长计算（`calculate_overtime_hours` 方法）
   - 约束：同一员工在同一排班只能有一条考勤记录

2. **考勤状态判断规则**：
   - 无签到或无签退记录 → `MISSING`（缺卡）
   - 签到时间 > 班次开始时间 + 5分钟 → `LATE`（迟到）
   - 签退时间 < 班次结束时间 - 5分钟 → `EARLY_LEAVE`（早退）
   - 其他情况 → `NORMAL`（正常）
   - 加班计算：签退时间 > 班次结束时间，计算超出的小时数

3. **创建序列化器** (`attendance/serializers.py`)
   - `AttendanceRecordSerializer` - 考勤记录详情序列化器（支持完整字段）
   - `AttendanceRecordListSerializer` - 考勤记录列表序列化器（简化版）
   - `ClockInSerializer` - 签到请求验证序列化器
   - `ClockOutSerializer` - 签退请求验证序列化器
   - `AttendanceStatisticsSerializer` - 考勤统计请求序列化器
   - `AttendanceStatisticsResponseSerializer` - 考勤统计响应序列化器
   - `AttendanceCorrectionSerializer` - 异常处理序列化器

4. **创建视图集** (`attendance/views.py`)
   - `AttendanceRecordViewSet` - 基于 DRF 的 `ModelViewSet`
   - 支持筛选：按员工、状态筛选
   - 支持搜索：按姓名、电话、地点搜索
   - 支持排序：按创建时间、签到时间、签退时间排序
   - 自定义 action：
     - `clock_in/` - 签到接口（记录签到时间和地点，自动判断考勤状态）
     - `clock_out/` - 签退接口（记录签退时间和地点，自动判断考勤状态）
     - `statistics/` - 考勤统计接口（汇总迟到次数、缺卡次数、加班时长）
     - `correct/` - 异常处理接口（管理员可修改考勤状态并填写备注）
     - `my_attendance/` - 我的考勤记录接口（员工查看自己的考勤记录）
   - 统一的响应格式：`{code, message, data}`

5. **配置 URL 路由**
   - 创建 `attendance/urls.py` - 使用 DRF 的 `DefaultRouter`
   - 更新 `config/urls.py` - 包含 attendance 路由：`/api/attendance/`

6. **注册 Django Admin** (`attendance/admin.py`)
   - 配置 `AttendanceRecordAdmin` 类
   - 列表显示字段：id, 员工姓名, 工作日期, 班次, 签到时间, 签退时间, 状态, 迟到, 早退, 缺卡, 加班时长, 创建时间
   - 过滤器：状态、创建时间、工作日期
   - 搜索字段：姓名、电话、地点
   - 日期分层导航：按工作日期浏览
   - 字段分组展示：基本信息、签到信息、签退信息、考勤状态、异常处理、时间信息
   - 只读字段：创建时间、更新时间、状态、加班时长

7. **数据库迁移**
   - 创建迁移：`attendance/migrations/0001_initial.py`
   - 迁移文件已创建，等待应用（需要 MySQL 服务器运行）

**API 端点清单**：
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

**筛选和搜索参数**：
- 考勤记录筛选：`?employee=1&status=LATE`
- 考勤记录搜索：`?search=张三`
- 考勤记录排序：`?ordering=-clock_in_time`
- 我的考勤查询：`?employee_id=1&start_date=2026-01-01&end_date=2026-01-31`

**测试验证**：
- ⏳ 等待 MySQL 服务器启动后应用数据库迁移
- ⏳ 员工签到测试（在班次开始时间前 5 分钟内签到，确认状态为 NORMAL）
- ⏳ 员工签到测试（在班次开始时间后 6 分钟签到，确认状态为 LATE）
- ⏳ 员工签退测试（提前签退超过 5 分钟，确认状态为 EARLY_LEAVE）
- ⏳ 员工签退测试（只有签到没有签退，确认状态为 MISSING）
- ⏳ 员工签退测试（签退时间超过班次结束时间，确认计算了加班时长）
- ⏳ 管理员修改异常考勤（确认状态更新且有备注）

**注意事项**：
- 考勤状态在保存时自动判断，管理员也可以手动修改（需要填写更正备注）
- 加班时长仅计算超出班次结束时间的部分，以小时为单位（保留2位小数）
- 签到和签退接口需要员工ID，后续需要实现登录认证后从token中获取
- 缺卡状态会在只有签到或只有签退时自动触发
- 权限验证待后续实现（目前所有用户都可访问管理接口）

---

### ✅ 步骤 2.5：创建请假模型与 API

**实施内容**：

1. **创建 LeaveRequest 模型** (`leaves/models.py`)
   - 字段定义：
     - 基本信息字段：`employee`（外键）、`leave_type`（枚举：SICK/PERSONAL/COMPENSATORY）、`start_time`、`end_time`、`reason`
     - 审批信息字段：`status`（枚举：PENDING/APPROVED/REJECTED）、`approver`（外键，可选）、`approval_remark`
     - 时间戳：`created_at`、`updated_at`
   - 枚举类定义：`LeaveType` 和 `Status` 使用 Django 的 `TextChoices`
   - 自定义属性：`leave_duration_days` 计算请假天数
   - 数据库索引：employee, status, created_at, start_time

2. **创建序列化器** (`leaves/serializers.py`)
   - `LeaveRequestSerializer` - 请假申请详情序列化器（支持完整字段）
   - `LeaveRequestListSerializer` - 请假申请列表序列化器（简化版）
   - `LeaveRequestCreateSerializer` - 请假申请创建序列化器（验证请假时间）
   - `LeaveRequestApprovalSerializer` - 请假审批序列化器
   - `LeaveRequestMySerializer` - 我的请假申请序列化器（员工查看自己的请假记录）

3. **创建视图集** (`leaves/views.py`)
   - `LeaveRequestViewSet` - 基于 DRF 的 `ModelViewSet`
   - 支持筛选：按员工、请假类型、状态筛选
   - 支持搜索：按姓名、电话、原因、审批意见搜索
   - 支持排序：按创建时间、开始时间、结束时间排序
   - 自定义 action：
     - `my_requests/` - 我的请假申请接口（查询当前员工的请假记录）
     - `pending/` - 待审批列表接口（管理员）
     - `approve/` - 请假审批接口（批准/拒绝，填写意见）
   - 统一的响应格式：`{code, message, data}`
   - 请假时间验证：结束时间必须大于开始时间

4. **配置 URL 路由**
   - 创建 `leaves/urls.py` - 使用 DRF 的 `DefaultRouter`
   - 更新 `config/urls.py` - 包含 leaves 路由：`/api/leaves/`

5. **注册 Django Admin** (`leaves/admin.py`)
   - 配置 `LeaveRequestAdmin` 类
   - 列表显示字段：id, 员工姓名, 请假类型, 开始时间, 结束时间, 请假天数, 审批状态, 审批人, 创建时间
   - 过滤器：请假类型、审批状态、创建时间、开始时间
   - 搜索字段：员工姓名、员工电话、原因、审批意见
   - 日期分层导航：按开始时间浏览
   - 字段分组展示：基本信息、审批信息、时间信息
   - 只读字段：创建时间、更新时间、请假天数

6. **数据库迁移**
   - 创建迁移：`leaves/migrations/0001_initial.py`
   - 应用迁移到数据库

**API 端点清单**：
```
# 请假申请管理
GET    /api/leaves/                    # 请假申请列表（支持筛选、搜索、排序）
POST   /api/leaves/                    # 创建请假申请
GET    /api/leaves/{id}/               # 请假申请详情
PUT    /api/leaves/{id}/               # 更新请假申请
DELETE /api/leaves/{id}/               # 删除请假申请

# 自定义接口
GET    /api/leaves/my-requests/        # 我的请假申请（员工查询）
GET    /api/leaves/pending/            # 待审批列表（管理员）
POST   /api/leaves/{id}/approve/       # 请假审批（批准/拒绝）
```

**筛选和搜索参数**：
- 请假申请筛选：`?employee=1&leave_type=SICK&status=PENDING`
- 请假申请搜索：`?search=张三` 或 `?search=身体不适`
- 请假申请排序：`?ordering=-created_at`
- 我的请假查询：`/api/leaves/my-requests/?employee_id=1&status=APPROVED`

**测试验证**：
- ✅ 创建请假申请，返回 201，请假申请创建成功，默认状态为 PENDING
- ✅ 获取请假列表，返回 200，显示所有请假申请
- ✅ 获取待审批列表，返回 200，仅显示待审批的申请
- ✅ 查询我的请假记录，返回 200，显示指定员工的请假记录
- ✅ 批准请假申请，返回 200，状态变为 APPROVED，记录审批人和审批意见
- ✅ 拒绝请假申请，返回 200，状态变为 REJECTED，记录审批人和审批意见
- ✅ 按状态筛选请假申请（APPROVED/REJECTED/PENDING），返回正确结果
- ✅ 按请假类型筛选（SICK/PERSONAL/COMPENSATORY），返回正确结果
- ✅ 请假天数自动计算（包含开始和结束日期）
- ✅ Django Admin 界面正常显示和管理请假申请

**注意事项**：
- 请假时间验证确保结束时间大于开始时间
- 审批时检查申请状态，只有 PENDING 状态的申请可以被审批
- 审批通过或拒绝后，记录审批人和审批意见，便于追溯
- 请假天数计算包含开始和结束日期（最少 1 天）
- 权限验证待后续实现（目前所有用户都可访问管理接口）

---

## 待完成

- [ ] 步骤 2.6：创建薪资模型与 API
- [ ] 步骤 2.7：创建统计分析接口
- [ ] ...（详见 IMPLEMENTATION_PLAN.md）
