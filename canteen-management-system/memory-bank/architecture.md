# 食堂管理系统 - 架构文档

> 本文档说明项目架构和各文件作用，供开发者理解系统结构

---

## 项目总体结构

```
canteen-management-system/
├── backend/               # Django 后端项目
│   ├── config/           # Django 项目配置
│   ├── accounts/         # 用户账号与认证
│   ├── employees/        # 员工档案管理
│   ├── schedules/        # 排班管理
│   ├── attendance/       # 考勤管理
│   ├── leaves/           # 请假管理
│   ├── salaries/         # 薪资管理
│   ├── analytics/        # 统计分析
│   ├── static/           # 静态文件
│   ├── media/            # 媒体文件
│   └── manage.py         # 命令行工具
├── frontend/             # Vue 3 前端项目
├── sql/                  # 数据库参考脚本
├── memory-bank/          # 文档仓库
├── .gitignore
└── CLAUDE.md             # AI 开发指南
```

---

## 后端架构

### 核心设计原则

1. **模块化设计**：每个应用对应一个业务领域
2. **API 优先**：Django REST Framework 构建 RESTful API
3. **前后端分离**：通过 CORS 通信
4. **业务分离**：User（登录账号）与 EmployeeProfile（员工档案）独立

### 应用职责划分

| 应用 | 职责 | 主要模型 |
|------|------|---------|
| `accounts` | 用户登录、注册、认证 | User |
| `employees` | 员工档案管理 | EmployeeProfile |
| `schedules` | 排班计划、调班申请 | Shift, Schedule, ShiftSwapRequest |
| `attendance` | 签到/签退、考勤记录 | AttendanceRecord |
| `leaves` | 请假申请、审批 | LeaveRequest |
| `salaries` | 薪资计算、申诉 | SalaryRecord, Appeal |
| `analytics` | 数据统计（无模型） | - |

---

## 核心业务模型

### User（登录账号）
```python
username       # 登录账号（唯一）
password       # 密码（开发阶段明文）
employee_id    # 关联员工档案（可选）
role           # ADMIN/EMPLOYEE
status         # ENABLED/DISABLED
```

### EmployeeProfile（员工档案）
```python
# 基础信息
name, gender, phone, id_card, address
# 岗位信息
position (CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER)
entry_date, status (ACTIVE/INACTIVE/LEAVE_WITHOUT_PAY)
# 资质证书
health_certificate_no, health_certificate_expiry
chef_certificate_level
```

### 考勤状态判断规则
- **缺卡**：无签到或无签退记录
- **迟到**：签到时间 > 班次开始 + 5分钟
- **早退**：签退时间 < 班次结束 - 5分钟
- **正常**：其他情况

### 薪资计算公式
```
日工资 = 月基本工资 ÷ 21.75
时薪 = 日工资 ÷ 8
加班费 = 时薪 × 1.5 × 加班小时数
岗位津贴 = CHEF(800)/PASTRY(700)/PREP(500)/CLEANER(300)/SERVER(400)/MANAGER(1000)
迟到扣款 = 20 × 迟到次数
缺卡扣款 = 50 × 缺卡次数
实发工资 = 基本工资 + 岗位津贴 + 加班费 - 迟到扣款 - 缺卡扣款
```

### 数据流
```
排班 → 考勤 → 薪资
```

---

## 前端架构

### 项目结构
```
frontend/src/
├── views/
│   ├── admin/       # 管理员端（Dashboard/员工/排班/考勤/请假/薪资/统计）
│   ├── employee/    # 员工端（首页/个人/签到/考勤/请假/调班/薪资）
│   └── auth/        # 登录/注册
├── api/             # API 请求封装
├── router/          # 路由配置
├── stores/          # Pinia 状态管理
└── components/      # 公共组件
```

### 核心技术栈
- **Vue 3** + **Vite** + **Element Plus** + **ECharts**
- **Axios** + **Vue Router** + **Pinia**

### UI 主题配色
| 用途 | 色值 |
|------|------|
| 主色 | #FF6B35（橙色） |
| 辅助色 | #F7C52D（黄）、#4CAF50（绿） |
| 背景色 | #FFF8F0（浅米色） |

---

## API 端点

| 模块 | 端点 | 说明 |
|------|------|------|
| accounts | `/api/accounts/login/` | 登录 |
| employees | `/api/employees/` | 员工 CRUD |
| schedules | `/api/schedules/schedules/batch_create/` | 批量排班 |
| attendance | `/api/attendance/clock_in/` | 签到 |
| leaves | `/api/leaves/{id}/approve/` | 审批请假 |
| salaries | `/api/salaries/salaries/generate/` | 生成薪资 |
| analytics | `/api/analytics/overview/` | 总览统计 |

---

## 重要文件

### 后端
- `settings.py` - 数据库、CORS、静态文件配置
- `urls.py` - API 路由配置
- `requirements.txt` - Python 依赖
- `manage.py` - Django 命令行工具

### 前端
- `vite.config.js` - API 代理配置
- `package.json` - 项目依赖
- `src/api/request.js` - Axios 实例配置
- `src/api/accounts.js` - 用户账号管理 API
- `src/router/index.js` - 路由与导航守卫
- `src/stores/user.js` - 用户状态管理
- `src/views/admin/SystemManageView.vue` - 系统管理页面
- `src/layouts/AdminLayout.vue` - 管理员端布局（含菜单配置）

---

## 开发工作流

```bash
# 后端
python manage.py makemigrations    # 创建迁移
python manage.py migrate           # 应用迁移
python manage.py runserver         # 启动服务器

# 前端
npm run dev                        # 启动开发服务器
npm run build                      # 构建生产版本
```

---

## 注意事项

1. **analytics 应用**：避免与 Python 内置 `statistics` 模块冲突
2. **数据库迁移**：始终使用 Django migrations，不直接执行 SQL
3. **密码存储**：开发阶段明文，生产环境需加密
4. **CORS 配置**：前端开发需配置跨域
5. **User vs EmployeeProfile**：员工档案与登录账号是两个独立概念

---

## 系统管理页面架构见解

### 设计理念

系统管理页面（`SystemManageView.vue`）采用**左侧导航 + 右侧内容**的布局模式，将三类管理功能整合在同一页面中，通过 Tab 切换实现无刷新视图切换。

### 文件职责

| 文件 | 作用 |
|------|------|
| `frontend/src/api/accounts.js` | 封装用户账号相关的 API 请求（CRUD、角色列表、系统设置） |
| `frontend/src/views/admin/SystemManageView.vue` | 系统管理主页面，包含用户管理、角色展示、系统设置三个功能模块 |
| `frontend/src/router/index.js` | 添加 `/admin/system` 路由配置 |
| `frontend/src/layouts/AdminLayout.vue` | 添加"系统管理"菜单项，更新菜单标题映射，处理顶部"系统设置"下拉操作跳转 |

### 页面模块划分

```
SystemManageView.vue
├── 左侧导航
│   ├── 用户账号
│   ├── 角色权限
│   └── 系统设置
├── 用户账号管理
│   ├── 操作栏（新增、筛选、搜索）
│   ├── 用户列表表格
│   ├── 分页组件
│   └── 新增/编辑对话框
├── 角色权限展示
│   └── 角色卡片（管理员/员工）
└── 系统设置
    ├── 考勤规则设置
    ├── 薪资计算设置
    └── 保存/重置按钮
```

### 关键技术点

1. **Tab 切换实现**：使用 `v-show` 控制内容区显示/隐藏，保持各模块状态
2. **表单复用**：用户表单通过 `isEditUser` 标志区分新增/编辑模式
3. **密码处理**：编辑模式下密码为空则不修改，保持原密码
4. **员工关联**：通过下拉选择器关联员工档案，支持搜索过滤
5. **系统设置持久化**：设置项保存到数据库，页面加载时读取

### 菜单集成

系统管理页面通过两种方式访问：
1. **侧边栏菜单**：AdminLayout 添加固定的"系统管理"菜单项
2. **顶部下拉菜单**：用户头像下拉中的"系统设置"选项跳转到系统管理页面

这样设计既保证了功能的可发现性，又符合用户的使用习惯。

---

## 员工端首页架构见解

### 设计理念

员工端首页（`HomeView.vue`）采用**卡片式布局**，以信息展示和快捷操作为核心，为员工提供一站式的个人信息和快速访问入口。

### 文件职责

| 文件 | 作用 |
|------|------|
| `frontend/src/api/schedule.js` | 新增 `getEmployeeSchedules()` 函数，支持按员工ID和日期范围查询排班数据 |
| `frontend/src/views/employee/HomeView.vue` | 员工端首页组件，包含欢迎区、排班卡片、快捷入口、通知列表 |
| `frontend/src/router/index.js` | 添加员工端路由配置（schedule/attendance/leave/swap/salary/profile） |
| `frontend/src/views/employee/[ScheduleView, AttendanceView, LeaveView, SwapView, SalaryView, ProfileView].vue` | 员工端各功能模块的占位页面，待后续步骤实现 |

### 页面模块划分

```
HomeView.vue
├── 欢迎区域
│   ├── 动态问候语（早/上/中/下午/晚上好）
│   ├── 员工姓名
│   ├── 当前日期
│   └── 岗位标签
├── 排班卡片区域
│   ├── 今日排班（班次名、时间 或 "今日休息"）
│   └── 明日排班（班次名、时间 或 "明日休息"）
├── 快捷入口区域
│   ├── 签到签退（绿色渐变）
│   ├── 请假申请（橙色渐变）
│   ├── 调班申请（黄色渐变）
│   └── 工资条（蓝色渐变）
└── 通知公告区域
    ├── 通知标题
    ├── 通知描述
    ├── 通知时间
    └── 未读标记
```

### 关键技术点

1. **动态问候语**：根据当前时间段（6-9/9-12/12-14/14-18/18-22/22-6）显示不同的问候语
2. **排班查询**：通过 `getEmployeeSchedules(employeeId, startDate, endDate)` 一次性获取今日和明日的排班数据
3. **岗位映射**：将后端返回的岗位枚举（CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER）映射为中文显示
4. **通知图标**：根据通知类型（leave_approved/leave_rejected/swap_approved等）动态显示对应图标
5. **响应式设计**：使用 CSS Grid 和媒体查询，适配不同屏幕尺寸

### UI/UX 设计

1. **配色方案**：
   - 欢迎卡片：橙色渐变（#FF6B35 → #FF8C42）
   - 快捷按钮：绿色、橙色、黄色、蓝色渐变
   - 休息日：灰色调（#f5f7fa）
2. **交互动效**：
   - 卡片悬停：向上平移 4px + 阴影加深
   - 按钮悬停：向上平移 4px + 橙色阴影
   - 通知点击：标记为已读 + 跳转对应页面
3. **图标使用**：Element Plus icons-vue（Calendar、Clock、Sunny、Moon、Grid、CircleCheck、DocumentAdd、Switch、Wallet、Bell等）

### 数据流

```
用户登录 → userStore.userInfo → employeeId
                ↓
        getEmployeeSchedules()
                ↓
        解析今日/明日排班 → 渲染排班卡片
                ↓
        快捷入口点击 → router.push() → 跳转对应页面
```

### 扩展性考虑

1. **通知数据**：当前使用模拟数据，后续可替换为真实 API 调用
2. **员工信息**：当前从 `userInfo` 中获取，如需更详细信息可调用员工档案 API
3. **占位页面**：已创建 6 个占位页面，便于后续步骤逐步实现各功能模块

---

## 员工端个人信息中心架构见解

### 设计理念

个人信息中心（`ProfileView.vue`）采用**多卡片垂直布局**，将个人信息、资质证书、密码管理和账号信息分为四个独立的功能模块，每个模块使用独立的卡片容器，便于信息组织和维护。

### 文件职责

| 文件 | 作用 |
|------|------|
| `frontend/src/api/auth.js` | 新增 `changePassword(id, data)` 函数，封装密码修改 API 请求 |
| `frontend/src/api/employee.js` | 提供 `getEmployeeDetail(id)` 函数，获取员工档案详细信息 |
| `frontend/src/views/employee/ProfileView.vue` | 个人信息中心主组件，包含四个信息卡片和密码修改功能 |
| `frontend/src/layouts/EmployeeLayout.vue` | 修复用户下拉菜单中"个人信息"的跳转逻辑（从显示提示改为路由跳转） |
| `backend/accounts/views.py` | 新增 `change_password()` action，提供密码修改后端接口 |

### 页面模块划分

```
ProfileView.vue
├── 页面标题
│   ├── 标题：个人信息中心
│   └── 副标题：查看您的个人档案、岗位信息及资质证书
├── 基本信息卡片（橙色图标）
│   ├── 姓名、性别
│   ├── 岗位（彩色标签）、在职状态
│   ├── 手机号码、身份证号（脱敏）
│   ├── 家庭住址、入职日期
├── 资质证书卡片（黄色图标）
│   ├── 健康证（证书号、有效期、到期警告）
│   └── 厨师等级证（如有）
├── 修改密码卡片（绿色图标）
│   ├── 旧密码输入
│   ├── 新密码输入（强度指示器）
│   ├── 确认密码输入
│   └── 修改/重置按钮
└── 账号信息卡片（绿色图标）
    ├── 登录账号、角色标签
    └── 账号状态、创建时间
```

### 关键技术点

1. **证书到期预警**：使用 `computed` 属性计算健康证有效期，距离到期30天内显示橙色警告样式和"即将到期"标签
2. **密码强度指示器**：根据密码长度动态计算强度（弱/中等/较强/强），使用不同颜色的类名展示
3. **表单验证**：
   - 旧密码必填
   - 新密码最少4位
   - 确认密码与新密码一致性验证（使用自定义 validator）
4. **身份证脱敏**：使用正则表达式 `replace(/(\d{6})\d{8}(\d{4})/, '$1********$2')` 隐藏中间8位
5. **岗位标签颜色**：通过 `getPositionTagType()` 函数为不同岗位返回对应的 Element Plus 标签类型
6. **自动退出登录**：密码修改成功后延迟1.5秒自动退出并跳转到登录页，让用户看到成功提示

### 数据流

```
组件挂载 → fetchEmployeeProfile()
                ↓
        getEmployeeDetail(employeeId)
                ↓
        解析员工数据 → 渲染四个信息卡片
                ↓
        用户点击修改密码 → 表单验证
                ↓
        changePassword(userId, passwordData)
                ↓
        后端验证旧密码 → 更新密码
                ↓
        前端显示成功 → 延迟退出登录
```

### UI/UX 设计

1. **卡片图标配色**：
   - 基本信息卡片：橙色图标 `#FF6B35`
   - 资质证书卡片：黄色图标 `#F7C52D`
   - 修改密码卡片：绿色图标 `#4CAF50`
   - 账号信息卡片：绿色图标 `#67C23A`

2. **证书卡片交互**：
   - 正常状态：绿色边框 + 灰色背景
   - 即将到期：橙色边框 + 浅橙色背景 + 警告图标
   - 悬停效果：背景变色 + 向右平移 4px

3. **密码强度颜色**：
   - 弱：红色 `#F56C6C`
   - 中等：橙色 `#E6A23C`
   - 较强：绿色 `#4CAF50`
   - 强：深绿色 `#67C23A`

4. **响应式设计**：
   - 小屏幕（≤768px）：证书卡片改为垂直布局，居中对齐
   - 页面内边距和字体大小自适应调整

### 安全性考虑

1. **密码修改验证**：后端验证旧密码正确性后才能修改
2. **敏感信息脱敏**：身份证号中间8位显示为星号
3. **自动退出登录**：密码修改成功后强制重新登录，防止旧会话被滥用
4. **表单确认机制**：新密码需要输入两次确认，防止误操作

### 后端 API 设计

```python
@action(detail=True, methods=['post'], url_path='change_password')
def change_password(self, request, pk=None):
    """
    修改密码接口
    POST /api/accounts/{id}/change_password/
    请求体：{"old_password": "old123", "new_password": "new123"}
    """
```

- 使用 `detail=True` 确保 URL 包含用户 ID
- 验证旧密码正确性
- 明文存储密码（开发阶段）
