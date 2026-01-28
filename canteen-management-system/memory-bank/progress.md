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

### ✅ 步骤 2.6：创建薪资模型与 API

**实施内容**：

1. **创建模型** (`salaries/models.py`)
   - `SalaryRecord` 模型：薪资记录
     - 基本信息字段：`employee`（外键）、`year_month`
     - 薪资组成字段：`base_salary`、`position_allowance`、`overtime_pay`、`deductions`、`total_salary`
     - 统计字段：`work_days`、`late_count`、`missing_count`、`overtime_hours`
     - 状态和备注：`status`（枚举：DRAFT/PUBLISHED/APPEALED/ADJUSTED）、`remark`
     - 时间戳：`created_at`、`updated_at`
   - `Appeal` 模型：异常申诉
     - 申诉信息：`appeal_type`（枚举：ATTENDANCE/SALARY）、`employee`（外键）、`target_id`、`reason`
     - 审批信息：`status`（枚举：PENDING/APPROVED/REJECTED）、`approver`（外键）、`approval_remark`
     - 时间戳：`created_at`、`updated_at`
   - 使用 `unique_together` 防止同一员工在同一月份重复生成薪资
   - 自动计算实发工资（在 `save` 方法中完成）

2. **薪资计算规则**：
   - 日工资 = 月基本工资 ÷ 21.75
   - 时薪 = 日工资 ÷ 8
   - 加班费 = 时薪 × 1.5 × 加班小时数
   - 迟到扣款 = 20 元 × 迟到次数
   - 缺卡扣款 = 50 元 × 缺卡次数
   - 岗位津贴：CHEF(800)、PASTRY(700)、PREP(500)、CLEANER(300)、SERVER(400)、MANAGER(1000)
   - 实发工资 = 基本工资 + 岗位津贴 + 加班费 - 迟到扣款 - 缺卡扣款

3. **创建序列化器** (`salaries/serializers.py`)
   - `SalaryRecordSerializer` - 薪资记录详情序列化器
   - `SalaryRecordListSerializer` - 薪资记录列表序列化器
   - `SalaryRecordCreateSerializer` - 薪资记录创建序列化器
   - `SalaryGenerateSerializer` - 薪资生成请求序列化器
   - `SalaryAdjustSerializer` - 薪资调整序列化器
   - `AppealSerializer` - 异常申诉详情序列化器
   - `AppealListSerializer` - 异常申诉列表序列化器
   - `AppealCreateSerializer` - 异常申诉创建序列化器
   - `AppealApprovalSerializer` - 异常申诉审批序列化器
   - `MyAppealSerializer` - 我的申诉序列化器

4. **创建视图集** (`salaries/views.py`)
   - `SalaryRecordViewSet` - 薪资记录管理
     - `generate_salary/` - 薪资生成接口（根据考勤数据自动计算月薪）
     - `adjust/` - 薪资调整接口（管理员手动调整金额，必填调整原因）
     - `publish/` - 发布薪资接口（将状态从草稿改为已发布）
     - `my-salaries/` - 我的薪资记录接口（员工查询自己的薪资）
   - `AppealViewSet` - 异常申诉管理
     - `approve/` - 申诉审批接口（批准/拒绝，自动更新薪资状态）
     - `pending/` - 待审批申诉列表（管理员）
     - `my-appeals/` - 我的申诉接口（员工查询自己的申诉记录）
   - 统一的响应格式：`{code, message, data}`

5. **配置 URL 路由**
   - 创建 `salaries/urls.py` - 使用 DRF 的 `DefaultRouter`
   - 更新 `config/urls.py` - 包含 salaries 路由：`/api/`

6. **注册 Django Admin** (`salaries/admin.py`)
   - `SalaryRecordAdmin` - 薪资记录管理界面
     - 列表显示：员工姓名、岗位、年月、薪资组成、统计数据、状态、创建时间
     - 过滤器：状态、年月、岗位、创建时间
     - 搜索：员工姓名、电话、备注
     - 日期分层导航：按创建时间浏览
     - 字段分组：基本信息、薪资组成、统计数据、备注、时间信息
   - `AppealAdmin` - 异常申诉管理界面
     - 列表显示：申诉类型、申诉员工、目标记录、状态、审批人、创建时间
     - 过滤器：申诉类型、状态、创建时间
     - 搜索：员工姓名、申诉原因、审批意见
     - 日期分层导航：按创建时间浏览
     - 字段分组：申诉信息、审批信息、时间信息

7. **数据库迁移**
   - 创建迁移：`salaries/migrations/0001_initial.py`
   - 应用迁移到数据库

**API 端点清单**：
```
# 薪资记录管理
GET    /api/salaries/              # 薪资记录列表（支持筛选、搜索、排序）
POST   /api/salaries/              # 创建薪资记录
GET    /api/salaries/{id}/         # 薪资记录详情
PUT    /api/salaries/{id}/         # 更新薪资记录
DELETE /api/salaries/{id}/         # 删除薪资记录
POST   /api/salaries/generate/     # 薪资生成
POST   /api/salaries/{id}/adjust/  # 薪资调整
POST   /api/salaries/{id}/publish/ # 发布薪资
GET    /api/salaries/my-salaries/  # 我的薪资记录（员工查询）

# 异常申诉管理
GET    /api/appeals/               # 申诉列表（支持筛选、搜索、排序）
POST   /api/appeals/               # 创建申诉
GET    /api/appeals/{id}/          # 申诉详情
PUT    /api/appeals/{id}/          # 更新申诉
DELETE /api/appeals/{id}/          # 删除申诉
POST   /api/appeals/{id}/approve/  # 申诉审批（批准/拒绝）
GET    /api/appeals/pending/       # 待审批申诉列表（管理员）
GET    /api/appeals/my-appeals/    # 我的申诉（员工查询）
```

**筛选和搜索参数**：
- 薪资记录筛选：`?employee=1&year_month=2026-01&status=PUBLISHED`
- 薪资记录搜索：`?search=张三`
- 薪资记录排序：`?ordering=-year_month`
- 我的薪资查询：`/api/salaries/my-salaries/?employee_id=1&year_month=2026-01`
- 申诉列表筛选：`?appeal_type=SALARY&status=PENDING`
- 申诉列表搜索：`?search=张三` 或 `?search=工资计算错误`

**测试验证**：
- ✅ 创建薪资记录，返回 201，薪资记录创建成功，实发工资自动计算
- ✅ 薪资生成接口，返回 200，根据考勤数据自动生成薪资
- ✅ 薪资调整接口，返回 200，手动调整薪资成功，记录调整原因和时间
- ✅ 发布薪资接口，返回 200，状态从 DRAFT 变为 PUBLISHED
- ✅ 我的薪资记录查询，返回 200，显示指定员工的薪资记录
- ✅ 创建异常申诉，返回 201，申诉创建成功，薪资状态变为 APPEALED
- ✅ 申诉审批接口（批准），返回 200，状态变为 APPROVED
- ✅ 申诉审批接口（拒绝），返回 200，薪资状态恢复为 PUBLISHED
- ✅ 待审批申诉列表，返回 200，仅显示待审批的申诉
- ✅ 我的申诉查询，返回 200，显示指定员工的申诉记录
- ✅ Django Admin 界面正常显示和管理薪资记录和申诉

**注意事项**：
- 薪资计算基于考勤数据统计（迟到次数、缺卡次数、加班时长）
- 岗位津贴使用固定配置，后续可改为系统设置中可配置
- 基本工资目前使用默认值（3000元），后续可扩展为从员工档案中读取
- 薪资调整会记录调整原因和时间，便于审计追溯
- 薪资申诉被拒绝时，自动恢复薪资记录状态为已发布
- 同一员工在同一月份只能有一条薪资记录（通过 unique_together 约束）
- 权限验证待后续实现（目前所有用户都可访问管理接口）

---

### ✅ 步骤 2.7：创建统计分析接口

**实施内容**：

1. **创建视图函数** (`analytics/views.py`)
   - `employee_statistics` - 人员统计接口
     - 总人数统计
     - 岗位分布（用于 ECharts 饼图）
     - 持证率统计（健康证、厨师等级证）
     - 入职状态分布
   - `attendance_statistics` - 考勤统计接口
     - 出勤率统计（基于排班和考勤记录）
     - 迟到/早退/缺卡次数统计
     - 加班时长统计
     - 日期维度考勤趋势（用于 ECharts 折线图）
     - 岗位维度考勤统计
   - `salary_statistics` - 薪资统计接口
     - 月度薪资支出趋势（用于 ECharts 折线图）
     - 岗位薪资对比（用于 ECharts 柱状图）
     - 薪资构成统计（用于 ECharts 饼图）
   - `overview_statistics` - 总览统计接口（Dashboard 首页）
     - 今日概览数据（应到/实到、请假、异常）
     - 待办事项统计（待审批请假、薪资草稿数量）
     - 本月考勤统计

2. **数据格式设计**
   - 所有接口返回统一格式：`{code, message, data}`
   - 数据结构适配 ECharts 渲染需求
   - 使用 `labels` + `data` 结构传递图表数据
   - 中文标签映射（枚举值 → 中文显示）

3. **查询参数支持**
   - 考勤统计：支持日期范围筛选（`start_date`、`end_date`）或相对时间（`days`）
   - 薪资统计：支持月份范围筛选（`months`）

4. **配置 URL 路由** (`analytics/urls.py`)
   - `/api/analytics/employees/` - 人员统计
   - `/api/analytics/attendance/` - 考勤统计
   - `/api/analytics/salaries/` - 薪资统计
   - `/api/analytics/overview/` - 总览统计

5. **更新主路由** (`config/urls.py`)
   - 添加 `path("api/analytics/", include("analytics.urls"))`

**API 端点清单**：
```
GET    /api/analytics/employees/    # 人员统计（岗位分布、持证率）
GET    /api/analytics/attendance/   # 考勤统计（出勤率、趋势）
GET    /api/analytics/salaries/     # 薪资统计（月度趋势、岗位对比）
GET    /api/analytics/overview/     # 总览统计（Dashboard 首页）
```

**查询参数示例**：
- 考勤统计（最近 7 天）：`/api/analytics/attendance/?days=7`
- 考勤统计（日期范围）：`/api/analytics/attendance/?start_date=2026-01-01&end_date=2026-01-31`
- 薪资统计（最近 12 个月）：`/api/analytics/salaries/?months=12`

**测试验证**：
- ✅ 人员统计接口返回 200，包含岗位分布和持证率数据
- ✅ 考勤统计接口返回 200，包含出勤率和日期趋势数据
- ✅ 薪资统计接口返回 200，无数据时返回空列表而非错误
- ✅ 总览统计接口返回 200，包含今日概览和待办事项数据
- ✅ 所有接口数据格式适配 ECharts 渲染需求
- ✅ 中文标签正确显示

**数据格式示例**：
```json
// 岗位分布（饼图数据）
{
  "labels": ["厨师", "面点", "切配", "保洁", "服务员", "经理"],
  "data": [5, 3, 8, 4, 6, 2]
}

// 日期趋势（折线图数据）
[
  {"date": "2026-01-21", "normal": 8, "late": 1, "early_leave": 0, "missing": 0},
  {"date": "2026-01-22", "normal": 9, "late": 0, "early_leave": 0, "missing": 1}
]
```

**注意事项**：
- `analytics` 应用没有自己的数据模型，使用其他应用的模型进行统计
- 使用 Django ORM 的聚合函数（`Count`、`Sum`、`Avg`）提高查询效率
- 空数据情况处理：返回空列表而非 404 错误
- 出勤率计算基于排班记录（应出勤）和考勤记录（实出勤）
- 薪资统计仅统计已发布（`PUBLISHED`）和已调整（`ADJUSTED`）的记录
- 权限验证待后续实现（目前所有用户都可访问统计接口）

---

### ✅ 步骤 3.1：实现登录页面及前端基础架构

**实施内容**：

1. **API 请求封装** (`src/api/request.js`)
   - 创建 axios 实例，配置 baseURL 为 `/api`
   - 请求拦截器：自动添加 Authorization 头（从 localStorage 读取 token）
   - 响应拦截器：
     - 统一处理后端返回格式 `{code, message, data}`
     - 处理 HTTP 错误状态（401、403、404、500 等）
     - 401 时自动清除 token 并跳转登录页
   - 超时设置：10 秒

2. **认证 API 封装** (`src/api/auth.js`)
   - `login(username, password)` - 用户登录
   - `register(data)` - 用户注册
   - `getUserInfo(id)` - 获取用户信息

3. **用户状态管理** (`src/stores/user.js`)
   - 状态字段：token、userInfo
   - 计算属性：isLoggedIn、userRole、isAdmin、isEmployee
   - 操作方法：
     - `login()` - 用户登录并保存凭证
     - `logout()` - 退出登录并清除状态
     - `updateUserInfo()` - 更新用户信息
   - 数据持久化：使用 localStorage

4. **路由配置** (`src/router/index.js`)
   - 已配置路由：
     - `/login` - 登录页面（无需认证）
     - `/register` - 注册页面（占位，无需认证）
     - `/admin` - 管理员首页（需要 ADMIN 角色）
     - `/employee` - 员工首页（需要 EMPLOYEE 角色）
     - `/` - 默认重定向到登录页
     - 404 页面 - 重定向到登录页
   - 导航守卫功能：
     - 检查路由是否需要认证
     - 验证用户角色权限
     - 自动跳转到对应角色的首页
     - 已登录用户访问登录页时自动跳转

5. **登录页面** (`src/views/auth/LoginView.vue`)
   - **布局结构**：
     - 左右分屏设计，充满视口（100vw × 100vh）
     - 左侧品牌区域（52%）：橙色渐变背景、Logo、功能特性展示
     - 右侧登录区域（48%）：登录表单
   - **品牌区域特性**：
     - Logo 动画效果（浮动 + 光晕脉冲）
     - 功能特性网格（员工管理、智能排班、考勤打卡、薪资核算）
     - 浮动装饰元素（餐具 emoji）
     - 底部统计信息（500+ 企业用户、99.9% 稳定性）
   - **登录表单特性**：
     - 表单验证（用户名最少 2 字符、密码最少 4 字符）
     - 记住账号功能（持久化到 localStorage）
     - 忘记密码链接
     - 支持回车键提交
     - 登录按钮加载状态
   - **交互体验**：
     - 表单字段焦点效果（边框变色 + 阴影）
     - 按钮悬停效果（上移 + 箭头滑动）
     - 统一错误提示（Element Plus Message）
   - **响应式设计**：
     - 使用 `clamp()` 实现流畅响应式
     - 平板竖屏（≤768px）：上下布局
     - 手机（≤480px）：优化间距和字体
   - **技术实现**：
     - Vue 3 Composition API（`<script setup>`）
     - Element Plus 组件库
     - Pinia 状态管理
     - Vue Router 导航
     - CSS 变量和自定义动画

6. **占位页面**
   - `RegisterView.vue` - 注册页面（占位）
   - `DashboardView.vue` - 管理员首页（占位）
   - `HomeView.vue` - 员工首页（占位）

7. **全局样式优化**
   - 隐藏滚动条但保持滚动功能
   - CSS 变量定义主题色

**技术优化**：
- 使用 `clamp()` 实现流畅响应式，避免媒体查询断点
- 使用 CSS 变量统一管理主题色
- 封装统一的 API 请求处理逻辑
- 实现完整的用户认证流程
- 路由守卫确保权限控制

**测试验证**：
- ✅ 登录页面正常显示
- ✅ 表单验证生效（用户名、密码长度校验）
- ✅ 登录成功后根据角色正确跳转（ADMIN → /admin, EMPLOYEE → /employee）
- ✅ 记住账号功能正常工作
- ✅ 路由守卫正确拦截未登录用户
- ✅ 已登录用户访问登录页自动跳转
- ✅ 响应式布局在不同屏幕尺寸下正常显示

**注意事项**：
- Token 目前使用用户 ID 或用户名，后续需要改用 JWT
- 密码开发阶段采用明文传输和存储，生产环境需加密
- 注册页面为占位页面，需要后续完善
- 管理员首页和员工首页需要后续实现具体功能

---

### ✅ 步骤 3.2：完善注册页面

**实施内容**：

1. **注册页面布局** (`src/views/auth/RegisterView.vue`)
   - **布局结构**：
     - 左右分屏设计，充满视口（100vw × 100vh）
     - 左侧品牌区域（52%）：橙色渐变背景、Logo、注册优势展示
     - 右侧注册区域（48%）：注册表单
   - **品牌区域特性**：
     - Logo 动画效果（浮动 + 光晕脉冲）
     - 注册优势网格（快速入职、安全可靠、移动办公、智能提醒）
     - 浮动装饰元素（餐具 emoji）
     - 底部统计信息（500+ 企业用户、99.9% 稳定性）
   - **注册表单特性**：
     - 用户名输入框（必填，最少 2 字符）
     - 密码输入框（必填，最少 4 字符，显示/隐藏切换）
     - 确认密码输入框（必填，需与密码一致）
     - 手机号输入框（必填，中国手机号格式验证）
     - 邮箱输入框（选填，邮箱格式验证）
     - 注册按钮（带加载状态）
     - 已有账号提示链接
   - **交互体验**：
     - 表单字段焦点效果（边框变色 + 阴影）
     - 按钮悬停效果（上移 + 阴影增强）
     - 统一错误提示（Element Plus Message）
     - 注册成功后延迟跳转到登录页
   - **响应式设计**：
     - 使用 `clamp()` 实现流畅响应式
     - 平板竖屏（≤768px）：上下布局
     - 手机（≤480px）：优化间距和字体
   - **技术实现**：
     - Vue 3 Composition API（`<script setup>`）
     - Element Plus 组件库
     - Vue Router 导航
     - CSS 变量和自定义动画

2. **表单验证逻辑**
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

3. **注册流程**
   - 调用后端 `/api/accounts/register/` 接口
   - 注册成功（code 201）：
     - 显示成功提示
     - 延迟 1.5 秒后跳转到登录页
   - 注册失败：
     - 显示后端返回的错误信息
     - 用户名已存在时提示"用户名已存在"
     - 网络错误时提示"注册失败，请检查网络连接"
   - 支持回车键提交表单

4. **UI/UX 设计**
   - 配色方案与登录页一致：
     - 主色：橙色 #FF6B35
     - 辅助色：黄色 #F7C52D
     - 背景色：浅米色 #FFF8F0
   - 使用食堂主题图标（餐具、食物 emoji）
   - 卡片式表单容器，圆角 24px
   - 渐变背景叠加层营造氛围感
   - 浮动动画增加视觉趣味性

**测试验证**：
- ✅ 访问 `/register` 页面，UI 正常显示
- ✅ 表单验证生效（所有字段验证规则正确）
- ✅ 密码与确认密码不一致时显示错误提示
- ✅ 手机号格式错误时显示错误提示
- ✅ 邮箱格式错误时显示错误提示（选填字段）
- ✅ 提交注册，成功后显示提示并跳转到登录页
- ✅ 用户名已存在时显示正确错误提示
- ✅ 响应式布局在不同屏幕尺寸下正常显示

**注意事项**：
- 注册成功后默认角色为 EMPLOYEE（由后端控制）
- 注册完成后跳转到登录页，用户需手动登录
- 邮箱字段为选填，适应不同用户需求
- 密码在开发阶段采用明文传输和存储
- UI 设计与登录页保持一致，使用相同的配色和设计语言

---

## 待完成

- [ ] 第三阶段：前端公共模块
  - [x] 步骤 3.1：创建登录页面
  - [x] 步骤 3.2：完善注册页面
  - [x] 步骤 3.3：配置路由与导航守卫
- [ ] ...（详见 IMPLEMENTATION_PLAN.md）
