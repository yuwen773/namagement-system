# 食堂管理系统 - 开发进度记录

> 记录开发过程中的已完成工作

---

## 2026-01-27

### ✅ 第一阶段：后端项目搭建

**步骤 1.1：Django 项目**
- 创建 Django 项目（`config/`）和 7 个应用：accounts、employees、schedules、attendance、leaves、salaries、analytics
- 配置 MySQL（端口 3307）、CORS、静态/媒体文件
- 依赖：django>=5.2、djangorestframework、mysqlclient、django-cors-headers

**步骤 1.2：Vue 项目**
- 使用 Vite 创建 Vue 3 项目（端口 5173）
- 依赖：element-plus、echarts、axios、vue-router、pinia
- 配置 API 代理（`/api` → `http://127.0.0.1:8000`）
- 目录结构：views/admin/employee/auth/、components/、api/、router/、stores/

---

### ✅ 第二阶段：后端模型与 API

**步骤 2.1：用户账号** (`accounts/`)
- User 模型：username、password（明文）、employee_id、role、status
- API：register/、login/、CRUD

**步骤 2.2：员工档案** (`employees/`)
- EmployeeProfile 模型：基础信息、岗位（CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER）、资质证书
- API：列表（支持筛选、搜索）、CRUD

**步骤 2.3：排班管理** (`schedules/`)
- Shift、Schedule、ShiftSwapRequest 模型
- API：batch_create/、calendar_view/、approve/、my_requests/、pending/

**步骤 2.4：考勤管理** (`attendance/`)
- AttendanceRecord 模型（自动计算状态和加班）
- 考勤规则：±5分钟宽限，迟到/早退/缺卡判定
- API：clock_in/、clock_out/、statistics/、correct/、my_attendance/

**步骤 2.5：请假管理** (`leaves/`)
- LeaveRequest 模型（自动计算请假天数）
- API：my_requests/、pending/、approve/

**步骤 2.6：薪资管理** (`salaries/`)
- SalaryRecord、Appeal 模型
- 薪资计算：日工资=月薪÷21.75，时薪=日工资÷8，加班费=时薪×1.5×小时
- 岗位津贴：CHEF(800)、PASTRY(700)、PREP(500)、CLEANER(300)、SERVER(400)、MANAGER(1000)
- API：generate/、adjust/、publish/、my-salaries/

**步骤 2.7：统计分析** (`analytics/`)
- API：employees/、attendance/、salaries/、overview/
- 数据格式：{code, message, data}，适配 ECharts

---

### ✅ 第三阶段：前端认证页面

**步骤 3.1：登录页面及基础架构**
- API 封装：axios 拦截器、401 自动跳转
- 用户状态：Pinia store（token、userInfo）
- 路由守卫：检查认证、验证角色、自动跳转
- 登录页：左右分屏、表单验证、记住账号

**步骤 3.2：注册页面**
- 注册页：用户名、密码（≥4字符）、确认密码、手机号、邮箱（选填）

---

### ✅ 第四阶段：管理员端页面

**步骤 4.1：Dashboard 首页**
- 快捷入口、今日概览、待办事项、本月统计
- API：`GET /api/analytics/overview/`

**步骤 4.2：人员档案管理**
- 员工列表、新增/编辑对话框（基础信息、岗位信息、资质证书）
- 岗位颜色：厨师-橙色、面点-红色、切配-蓝色、保洁-绿色、服务员-灰色、经理-深蓝

**步骤 4.3：排班管理**
- 日历视图/列表视图切换、批量排班、调班审批
- 班次颜色：早班-绿色、中班-橙色、晚班-红色、全天-蓝色

**步骤 4.4：考勤管理**
- 统计卡片、考勤记录表格、异常处理
- 状态颜色：正常-绿色、迟到-橙色、早退-红色、缺卡-灰色

**步骤 4.5：请假审批**
- 状态 Tab（全部/待审批/已通过/已驳回）、请假列表、审批对话框
- 请假类型颜色：病假-红色、事假-橙色、调休-绿色

**步骤 4.6：薪资管理**
- 薪资列表、调整对话框、申诉处理、分页
- 状态标签：草稿(灰)、已发布(绿)、已调整(橙)、申诉中(红)

**步骤 4.7：统计分析**
- 6 个 ECharts 图表：饼图×3、折线图×2、柱状图×2
- 统计：员工总数、出勤率、薪资支出、岗位分布、考勤趋势、薪资构成

**步骤 4.8：系统管理页面**
- 左侧导航：用户账号、角色权限、系统设置
- 用户账号管理：列表（ID/用户名/角色/关联员工/状态/时间）、新增/编辑对话框、筛选搜索、分页
- 角色权限展示：管理员/员工两种角色的权限说明卡片
- 系统设置：考勤规则（宽限时间、扣款金额）、薪资计算（月天数、日工时、加班倍率）
- API 封装：`frontend/src/api/accounts.js`

---

### ✅ 第五阶段：员工端页面

**步骤 5.1：员工端首页** (`HomeView.vue`)
- 欢迎区域：动态问候语（根据时间段）、员工姓名、当前日期、岗位标签
- 排班卡片：今日排班（班次名/时间 或 "今日休息"）、明日排班（班次名/时间 或 "明日休息"）
- 快捷入口：4 个彩色渐变按钮（签到签退-绿色、请假申请-橙色、调班申请-黄色、工资条-蓝色）
- 通知公告：审批结果、申诉反馈列表（带未读标记）
- API 增强：`getEmployeeSchedules()` 查询指定日期范围的排班
- 路由配置：添加员工端路由（schedule/attendance/leave/swap/salary/profile）
- 占位页面：创建 6 个员工端占位页面，待后续实现

---

## 待完成

- [ ] 第五阶段：员工端页面（步骤 5.2-5.7）
- [ ] 第六阶段：系统优化与部署（详见 IMPLEMENTATION_PLAN.md）

---

## 通用说明

**技术栈**：Django 5.2+、DRF、MySQL 8.0+、Vue 3、Element Plus、ECharts、Axios、Pinia、Vite

**UI 主题**：橙色 #FF6B35、黄色 #F7C52D、绿色 #4CAF50、浅米色 #FFF8F0

**注意事项**：
- 密码开发阶段明文存储/传输
- API 统一格式：{code, message, data}
- 删除操作有二次确认
- 管理页面路由需要 ADMIN 角色权限
