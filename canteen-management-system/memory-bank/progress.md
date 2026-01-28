# 食堂管理系统 - 开发进度记录

> 记录开发过程中的已完成工作

---

## 2026-01-27

### ✅ 步骤 1.1：创建后端 Django 项目

- 创建 Django 项目（`config/`）和 7 个应用：accounts、employees、schedules、attendance、leaves、salaries、analytics（原 statistics）
- 配置 MySQL 数据库（端口 3307）、CORS、静态/媒体文件
- 依赖：django>=5.2、djangorestframework、mysqlclient、django-cors-headers

**验证**：服务器启动成功，所有迁移正常应用

---

### ✅ 步骤 1.2：创建前端 Vue 项目

- 使用 Vite 创建 Vue 3 项目（端口 5173）
- 安装依赖：element-plus、echarts、axios、vue-router、pinia
- 配置 API 代理（`/api` → `http://127.0.0.1:8000`）
- 创建目录结构：views/admin/employee/auth/、components/、api/、router/、stores/

**验证**：开发服务器启动成功，热更新正常

---

### ✅ 步骤 2.1：用户账号模型与 API

**模型** (`accounts/models.py`)：User（username、password明文、employee_id、role、status）

**API 端点**：
```
POST   /api/accounts/register/   # 注册
POST   /api/accounts/login/      # 登录
GET    /api/accounts/            # 用户列表
```

---

### ✅ 步骤 2.2：员工档案模型与 API

**模型** (`employees/models.py`)：EmployeeProfile（基础信息、岗位信息、资质证书）

**API 端点**：
```
GET    /api/employees/           # 列表（?position=&status=&search=）
POST   /api/employees/           # 创建
```

---

### ✅ 步骤 2.3：排班相关模型与 API

**模型** (`schedules/models.py`)：Shift、Schedule、ShiftSwapRequest

**API 端点**：
```
POST   /api/schedules/schedules/batch_create/
POST   /api/schedules/schedules/calendar_view/
POST   /api/schedules/shift-requests/{id}/approve/
```

---

### ✅ 步骤 2.4：考勤模型与 API

**模型** (`attendance/models.py`)：AttendanceRecord（自动计算状态和加班时长）

**考勤规则**：±5分钟宽限，签到>开始+5分钟=迟到，签退<结束-5分钟=早退，无签到或签退=缺卡

**API 端点**：
```
POST   /api/attendance/clock_in/     # 签到
POST   /api/attendance/clock_out/    # 签退
POST   /api/attendance/statistics/   # 统计
```

---

### ✅ 步骤 2.5：请假模型与 API

**模型** (`leaves/models.py`)：LeaveRequest（leave_type、自动计算请假天数）

**API 端点**：
```
GET    /api/leaves/my-requests/     # 我的请假
GET    /api/leaves/pending/         # 待审批列表
POST   /api/leaves/{id}/approve/    # 审批
```

---

### ✅ 步骤 2.6：薪资模型与 API

**模型** (`salaries/models.py`)：SalaryRecord、Appeal

**薪资计算规则**：
```
日工资 = 月基本工资 ÷ 21.75
时薪 = 日工资 ÷ 8
加班费 = 时薪 × 1.5 × 加班小时数
实发工资 = 基本工资 + 岗位津贴 + 加班费 - 迟到扣款(20×次数) - 缺卡扣款(50×次数)
```

**API 端点**：
```
POST   /api/salaries/generate/         # 薪资生成
POST   /api/salaries/{id}/adjust/      # 薪资调整
POST   /api/salaries/{id}/publish/     # 发布薪资
POST   /api/appeals/{id}/approve/      # 申诉审批
```

---

### ✅ 步骤 2.7：统计分析接口

**视图** (`analytics/views.py`)：employee_statistics、attendance_statistics、salary_statistics、overview_statistics

**API 端点**：
```
GET    /api/analytics/employees/    # 人员统计
GET    /api/analytics/attendance/   # 考勤统计（?days=7）
GET    /api/analytics/salaries/     # 薪资统计（?months=12）
GET    /api/analytics/overview/     # 总览统计
```

**数据格式**：{code, message, data}，适配 ECharts（labels + data 结构）

---

### ✅ 步骤 3.1：登录页面及前端基础架构

**API 请求封装** (`src/api/request.js`)：axios 实例（baseURL: /api）、请求/响应拦截器、401 自动跳转登录

**用户状态管理** (`src/stores/user.js`)：token、userInfo、login()、logout()

**路由配置** (`src/router/index.js`)：导航守卫（检查认证、验证角色、自动跳转）

**登录页面** (`src/views/auth/LoginView.vue`)：左右分屏设计（品牌区 52% + 登录区 48%）、表单验证、记住账号

---

### ✅ 步骤 3.2：注册页面

**注册页面** (`src/views/auth/RegisterView.vue`)：用户名、密码（≥4字符，显示/隐藏）、确认密码、手机号（中国格式）、邮箱（选填）

---

### ✅ 步骤 4.1：管理员首页（Dashboard）

**管理员首页** (`src/views/admin/DashboardView.vue`)：
- 顶部导航栏：Logo、日期显示、用户信息、退出登录
- 快捷入口：人员新增、排班制定、考勤异常、薪资生成
- 今日概览：出勤情况、今日请假、今日异常
- 待办事项：待审批请假、调班申请、申诉、待发布薪资
- 本月统计：员工总数、本月迟到、本月薪资支出

**API**：`GET /api/analytics/overview/`

---

### ✅ 步骤 4.2：人员档案管理页面

**人员档案管理** (`src/views/admin/EmployeeManageView.vue`)：
- 员工列表：ID、姓名、性别、岗位（彩色标签）、手机号、身份证号、入职日期、状态（徽章）
- 新增/编辑对话框：基础信息、岗位信息、资质证书（3 个标签页）
- 岗位颜色：厨师-橙色、面点-红色、切配-蓝色、保洁-绿色、服务员-灰色、经理-深蓝

**API**：`GET/POST /api/employees/`（支持 ?position=&status=&search=）

---

### ✅ 步骤 4.3：排班安排管理页面

**排班管理** (`src/views/admin/ScheduleManageView.vue`)：
- 日历视图：每日排班（员工+班次）、班次颜色标签、已调班特殊标记
- 列表视图：ID、员工、班次、日期、时间、是否调班
- 批量排班对话框：多选员工、选择班次、日期范围
- 班次颜色：早班-绿色、中班-橙色、晚班-红色、全天-蓝色

**API**：
```
GET    /api/schedules/schedules/calendar_view/
POST   /api/schedules/schedules/batch_create/
POST   /api/schedules/shift-requests/{id}/approve/
```

---

### ✅ 步骤 4.4：考勤记录管理页面

**考勤管理** (`src/views/admin/AttendanceManageView.vue`)：
- 统计卡片：迟到次数、缺卡次数、加班时长、出勤天数
- 考勤记录表格：异常记录行高亮（黄色背景），加班>0 绿色高亮
- 异常处理对话框：状态修改、备注（必填，5-200字符）
- 状态颜色：正常-绿色、迟到-橙色、早退-红色、缺卡-灰色、异常-红色

**API**：
```
GET    /api/attendance/
POST   /api/attendance/statistics/
POST   /api/attendance/{id}/correct/
```

---

### ✅ 步骤 4.5：请假审批管理页面

**请假审批** (`src/views/admin/LeaveApproveView.vue`)：
- 状态 Tab：全部、待审批（高亮）、已通过、已驳回（带徽章）
- 请假列表：待审批记录行高亮（黄色背景）
- 审批对话框：申请摘要、审批意见（驳回必填，批准选填）
- 请假类型颜色：病假-红色、事假-橙色、调休-绿色

**API**：
```
GET    /api/leaves/（?status=&search=）
GET    /api/leaves/pending/
POST   /api/leaves/{id}/approve/
```

---

### ✅ 步骤 4.6：薪资信息管理页面

**薪资管理** (`src/views/admin/SalaryManageView.vue` + `src/api/salary.js`)：
- 顶部操作栏：月份选择器、生成薪资按钮、导出工资表按钮
- 统计卡片：本月薪资总额、平均薪资、待发布薪资、待处理申诉
- 薪资列表表格：员工姓名、岗位、月份、基本工资、岗位津贴、加班费、扣款、实发工资、状态、操作
  - 金额列右对齐，保留两位小数，使用 ¥ 前缀
  - 状态标签：草稿(灰色)、已发布(绿色)、已调整(橙色)、申诉中(红色)
  - 操作按钮：详情、调整、发布、删除
- 调整薪资对话框：显示当前薪资详情、可调整基本工资和加班费、调整原因必填
- 薪资详情对话框：完整薪资构成、考勤统计（出勤天数、迟到/缺卡次数、加班时长）
- 申诉处理对话框：批准/拒绝申诉、审批意见必填
- 分页组件

**API**：
```
GET    /api/salaries/salaries/           # 薪资列表（?year_month=&page=）
POST   /api/salaries/salaries/generate/  # 生成薪资
POST   /api/salaries/salaries/{id}/adjust/    # 调整薪资
POST   /api/salaries/salaries/{id}/publish/   # 发布薪资
DELETE /api/salaries/salaries/{id}/      # 删除薪资
POST   /api/salaries/appeals/{id}/approve/    # 审批申诉
```

**UI 特色**：
- 食堂主题配色渐变（对话框标题：橙黄、绿、红渐变）
- 统计卡片悬停效果（边框高亮对应主题色）
- 加班费高亮显示、扣款红色显示、实发工资橙色大字
- 员工头像圆形渐变背景
- 表格行 hover 浅米色背景
- 响应式布局适配

**路由更新**：
- 添加 `/admin/salaries` 路由
- AdminLayout 添加薪资管理菜单项（💰 图标）
- Dashboard 快捷入口添加薪资管理

---

### ✅ 步骤 4.7：综合统计分析页面

**统计分析页面** (`src/views/admin/StatisticsView.vue`)：

**顶部统计卡片**（4个渐变卡片）：
- 员工总数：在职人员数量
- 今日出勤率：实时出勤百分比，迟到/全员准时提示
- 本月薪资支出：含岗位津贴的薪资总额
- 待处理事项：待审批数量，需要处理/全部完成提示

**人员统计区域**：
- 岗位分布饼图：环形饼图展示各岗位人员占比
  - 厨师-橙色、面点-黄色、切配-绿色、保洁-蓝色、服务员-紫色、服务员-棕色
  - 悬停显示详情，底部自定义图例
- 持证率统计卡片：
  - 健康证持证率（绿色进度条）
  - 厨师证持证率（蓝色进度条）
  - 在职状态分布条形图

**考勤统计区域**：
- 出勤率折线图：最近7天出勤趋势
  - 正常出勤（绿色）+ 迟到（橙色）双折线
  - 渐变填充区域，平滑曲线
- 岗位考勤排行柱状图：迟到/缺卡统计
  - 双柱状图，渐变色填充
  - 圆角柱体
- 考勤状态分布卡片：状态图标+数量统计

**薪资统计区域**：
- 月度薪资支出趋势图：最近12个月
  - 折线+面积渐变，悬停显示总支出和平均薪资
  - Y轴单位：万元
- 薪资构成饼图：基本工资、岗位津贴、加班费、扣款
  - 环形饼图，右侧图例
- 岗位薪资对比柱状图：各岗位平均薪资
  - 渐变橙色柱状图，顶部显示标签（¥X.Xk）

**API**：
```
GET    /api/analytics/employees/    # 人员统计
GET    /api/analytics/attendance/   # 考勤统计（?days=7）
GET    /api/analytics/salaries/     # 薪资统计（?months=12）
GET    /api/analytics/overview/     # 总览统计
```

**UI 特色**：
- 食堂主题配色（橙#FF6B35、黄#F7C52D、绿#4CAF50、米色#FFF8F0）
- 页面标题渐变背景（橙色渐变）
- 浮动动画图标（title-icon 上下浮动）
- 卡片悬停效果（向上平移+阴影增强）
- 背景渐变（浅米色到浅橙色）
- 图表响应式设计
- 食堂元素图标（👥📈💰📋👤⏰🏥👨‍🍳）

**路由更新**：
- 添加 `/admin/statistics` 路由
- AdminLayout 添加统计分析菜单项（📊 TrendCharts 图标）

**技术实现**：
- 6个 ECharts 图表（饼图×3、折线图×2、柱状图×2）
- 响应式图表（resize 事件监听）
- 组件卸载时自动销毁图表实例
- 变量作用域问题修复（salaryAmounts 替代 salaryData）

**Bug 修复**：
- 修复 `initSalaryTrendChart` 中变量名冲突（局部变量 `salaryData` 与响应式变量重名）
- 修复 AdminLayout 中 FoodIcon 组件运行时编译警告（替换为 Element Plus Grid 图标）

---

## 待完成

- [ ] 第四阶段：管理员端页面
  - [x] 步骤 4.1：管理员首页（Dashboard）
  - [x] 步骤 4.2：人员档案管理页面
  - [x] 步骤 4.3：排班安排管理页面
  - [x] 步骤 4.4：考勤记录管理页面
  - [x] 步骤 4.5：请假审批管理页面
  - [x] 步骤 4.6：薪资信息管理页面
  - [x] 步骤 4.7：综合统计分析页面
  - [ ] 步骤 4.8：系统管理页面
- [ ] ...（详见 IMPLEMENTATION_PLAN.md）

---

## 通用说明

**技术栈**：Django 5.2+、DRF、MySQL 8.0+、Vue 3、Element Plus、ECharts、Axios、Pinia、Vite

**UI 主题**：橙色 #FF6B35、黄色 #F7C52D、绿色 #4CAF50、浅米色 #FFF8F0、食堂元素图标

**通用注意事项**：
- 密码开发阶段明文存储/传输
- 权限验证待后续实现
- 管理页面路由需要 ADMIN 角色权限
- 删除操作有二次确认
- API 统一格式：{code, message, data}
