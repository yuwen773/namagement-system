# 食堂管理系统 - 开发进度记录

> 记录开发过程中的已完成工作

---

## 2026-01-27

### ✅ 2026-01-29 完成

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

**步骤 5.2：个人信息中心页面** (`ProfileView.vue`)
- 四个信息卡片：基本信息、资质证书、修改密码、账号信息
- 基本信息展示：姓名、性别、岗位（彩色标签）、在职状态、手机、身份证（脱敏）、地址、入职日期
- 证书管理：健康证（有效期倒计时警告）、厨师等级证，即将到期（30天内）显示橙色警告
- 密码修改：旧密码验证、新密码强度指示器（弱/中等/较强/强）、确认密码一致性验证、修改成功后自动退出登录
- 账号信息：登录账号、角色、状态、创建时间
- 布局导航：修复 EmployeeLayout 中"个人信息"菜单跳转逻辑
- 后端 API：新增 `change_password` 接口（`POST /api/accounts/{id}/change_password/`）

**步骤 5.3：签到服务页面** (`CheckInView.vue`)
- 页面布局：左右分栏（左侧操作区 + 右侧日历区）
- 时间卡片：实时显示当前时间（每秒更新）和日期，渐变橙色背景
- 签到/签退按钮：根据今日记录状态自动切换（绿色签到 / 橙色签退），大尺寸便于点击
- 位置获取：使用浏览器 Geolocation API 获取经纬度
- 今日记录：签到时间、签退时间、考勤状态（彩色标签）、加班时长
- 打卡日历：Element Plus 日历组件，用彩色圆点标记打卡状态（正常-绿、迟到-橙、早退-红、缺卡-灰、异常-红）
- 月份切换：支持前后切换月份查看历史打卡记录
- 本月统计：出勤天数、迟到次数、缺卡次数、加班时长
- API 调用：`clockIn()`、`clockOut()`、`getMyAttendance()`、`getAttendanceStatistics()`
- 路由配置：`/employee/checkin`，添加到 EmployeeLayout 顶部导航菜单

**步骤 5.4：考勤信息查询页面** (`AttendanceView.vue`)
- 页面布局：顶部月份选择器 + 4个统计卡片 + 考勤记录表格
- 月份选择器：Element Plus 月份选择器，支持按月筛选考勤数据
- 统计卡片：出勤天数（绿色）、迟到次数（橙色）、缺卡次数（灰色）、加班时长（橙红渐变）
- 考勤记录表格：日期（大号日+小号月）、签到/签退时间（带图标）、状态标签、地点、加班时长
- 异常行高亮：迟到/早退/缺卡/异常记录行使用浅橙色背景
- 异常上报对话框：显示异常详情、状态标签、签到签退时间、异常说明输入框（5-200字符）
- API 调用：`getMyAttendance()`（按员工ID和日期范围）、`getAttendanceStatistics()`（获取统计数据）
- 路由配置：`/employee/attendance`，已在 EmployeeLayout 顶部导航菜单中配置
- 响应式设计：大屏4列统计卡片、中屏2列、小屏1列；表格横向滚动

**步骤 5.5：请假申请服务页面** (`LeaveView.vue`)
- 页面布局：页面标题 + 操作卡片 + Tab 导航 + 请假记录列表
- 操作卡片：橙色图标 + "提交新的请假申请"文字 + "新增请假"按钮
- Tab 导航：申请记录、审批中（带徽章计数）、已通过、已驳回
- 请假记录卡片：显示请假类型标签、状态标签、时间范围、请假天数、请假原因
- 审批意见：已驳回的请假显示橙色审批意见框（带图标和强调样式）
- 审批信息：已审批的记录显示审批人和相对时间（今天/昨天/N天前）
- 操作按钮：待审批状态显示"撤销申请"按钮（红色），所有记录显示"查看详情"按钮
- 新增请假对话框：
  - 请假类型选择：年假/病假/事假/产假/陪产假/其他
  - 开始/结束时间：日期时间选择器，禁用过去日期，结束时间自动限制不能早于开始时间
  - 请假原因：文本域，必填，5-200字，带字数统计
  - 预计天数：自动计算显示，大号橙色字体，渐变背景
- 请假详情对话框：显示完整的请假申请信息（类型、时间、天数、原因、状态、审批意见、审批人、审批时间、申请时间）
- 请假类型标签颜色：年假-success、病假-danger、事假-warning、其他-info
- 状态标签颜色：审批中-warning、已通过-success、已驳回-danger
- API 调用：`getMyLeaves()`、`createLeave()`、`deleteLeave()`
- 数据加载：页面加载时自动获取请假列表，同时统计审批中数量
- Tab 切换：切换 Tab 时重新加载对应状态的请假数据
- 撤销确认：点击撤销时弹出确认对话框，确认后调用 API 删除
- 响应式设计：小屏幕下操作按钮垂直布局，全宽显示

**步骤 5.6：调班申请服务页面** (`SwapView.vue`)
- 页面布局：页面标题 + 操作卡片 + 调班记录列表
- 操作卡片：黄色 Switch 图标 + "需要调整班次？"说明 + "新增调班申请"按钮
- 调班记录卡片：
  - 左边框：4px 橙色边框，悬停时向右平移 4px
  - 状态标签（审批中-warning、已通过-success、已驳回-danger）
  - 原班次区域：橙色标签，显示日期、班次名、时间
  - 调整箭头：橙色箭头图标指向右侧
  - 目标班次区域：绿色标签，显示日期、班次名、时间
  - 申请原因：灰色背景，带文档图标
  - 驳回原因：仅已驳回时显示，橙色边框背景
  - 审批信息：已通过时显示绿色提示
- 操作按钮：待审批状态显示"撤销申请"（红色），所有记录显示"查看详情"
- 新增调班对话框：
  - 原班次选择：下拉框显示未来30天排班，包含日期、班次标签、时间
  - 目标日期：日期选择器，禁用今天之前的日期
  - 目标班次：下拉框显示所有班次
  - 申请原因：文本域，必填，5-200字，带字数统计
- 调班详情对话框：显示完整调班申请信息（状态、原班次、目标班次、原因、审批信息、时间）
- 状态颜色：审批中-橙色、已通过-绿色、已驳回-红色
- API 调用：`getMyShiftRequests()`、`createShiftRequest()`、`deleteShiftRequest()`、`getShiftList()`、`getEmployeeSchedules()`
- 数据加载：打开对话框时自动加载排班和班次列表
- 表单验证：所有字段必填，原因5-200字
- 撤销确认：点击撤销时弹出确认对话框，确认后调用 API 删除
- 响应式设计：小屏幕下调班内容垂直布局，箭头旋转90度
- 导航菜单：在 EmployeeLayout 顶部添加"调班申请"菜单项
- 后端更新：`ShiftSwapRequestSerializer` 和 `ShiftSwapRequestListSerializer` 添加 `original_schedule_date`、`original_shift_time`、`target_shift_time`、`approval_time` 字段

**步骤 5.7：薪资信息查询页面** (`SalaryView.vue`)
- 页面布局：页面标题 + 月份选择器 + 薪资详情卡片
- 月份选择器：日期选择器（月份类型）+ "薪资申诉"按钮
- 当月工资总览卡片：
  - 橙色渐变背景（linear-gradient(135deg, #FF6B35, #FF8C42)）
  - 实发工资大字显示（48px），默认脱敏 `****`，点击"查看详情"后显示具体金额
  - 状态标签（草稿-info、已发布-success、已调整-warning、申诉中-danger）
  - "查看详情"/"隐藏详情"按钮切换脱敏状态
- 工资明细卡片（4个）：
  - 基本工资：蓝色渐变图标
  - 岗位津贴：绿色渐变图标
  - 加班费：橙色渐变图标，显示加班时长提示
  - 扣款：红色渐变图标，显示迟到/缺卡次数提示
  - 所有金额默认脱敏，点击查看详情后显示
- 工资明细说明：
  - 使用 `el-descriptions` 展示完整计算明细
  - 显示公式提示：时薪 × 1.5 × 加班小时数、迟到×20 + 缺卡×50
  - 字段：月份、出勤天数、迟到次数、缺卡次数、加班时长、各项金额
- 历史薪资记录：
  - 可点击切换查看其他月份
  - 显示月份、金额、状态标签
  - 当前选中项高亮显示
- 薪资申诉对话框：
  - 显示申诉月份和当前金额
  - 申诉原因文本域（5-200字，带字数统计）
  - 提示信息：提交后管理员将审核
- 安全特性：
  - 默认脱敏显示所有金额
  - 切换月份后自动重新隐藏
  - 查看详情后才能看到具体金额
- API 调用：`getMySalaries()`、`createAppeal()`
- API 更新：`salary.js` 新增 `getMySalaries()` 方法
- 响应式设计：大屏4列、中屏2列、小屏1列，移动端按钮全宽

---

## 待完成

- [x] 第五阶段步骤 5.5：请假申请服务页面
- [x] 第五阶段步骤 5.6：调班申请服务页面
- [x] 第五阶段步骤 5.7：薪资信息查询页面
- [ ] 第六步骤 6.3：添加加载状态与错误处理
- [ ] 第六步骤 6.1：应用食堂主题全局样式（图标库）

---

## 2026-01-29

### ✅ 第六阶段：UI/UX 优化 - 步骤 6.2 响应式设计优化

**实施内容**：

1. **创建主题文件** (`frontend/src/styles/theme.css`)
   - 定义食堂主题 CSS 变量（主色、辅助色、背景色、文字色、边框、间距、阴影）
   - 定义响应式断点：
     - 小屏幕 < 1200px：字体 15px
     - 中等屏幕 1200px-1439px：字体 14px
     - 大屏幕 >= 1440px：字体 16px
     - 超小屏幕 < 768px：字体 16px（放大字体方便老年员工）

2. **创建响应式混入文件** (`frontend/src/styles/mixins.css`)
   - 表单对话框响应式：小屏幕宽度 95%、表单项垂直布局、按钮全宽
   - 表格响应式：小屏幕字体缩小、单元格内边距调整
   - 卡片响应式：小屏幕边距调整
   - 操作栏响应式：小屏幕垂直布局
   - 分页响应式：小屏幕居中、按钮尺寸调整
   - 统计卡片响应式：4列 → 2列 → 1列
   - 输入框响应式：更大字体和点击区域（44px 高度）
   - 菜单响应式：更大高度和字体

3. **更新 main.js**
   - 引入 `theme.css` 和 `mixins.css`
   - 确保主题变量在所有页面生效

4. **优化 AdminLayout 响应式设计**
   - 小屏幕 < 1200px：调整间距、字体大小
   - 中等屏幕 1200px-1439px：边距优化
   - 超小屏幕 < 768px：侧边栏固定、隐藏用户名和日期、面包屑简化、按钮更大

5. **优化 EmployeeLayout 响应式设计**
   - 小屏幕 < 1200px：调整间距、字体大小、菜单项
   - 中等屏幕 1200px-1439px：边距优化
   - 超小屏幕 < 768px：隐藏 Logo 文字、日期、用户名；菜单项高度 56px；更大点击区域

6. **全局响应式样式应用**
   - mixins.css 中的样式自动应用于所有页面
   - Element Plus 组件（对话框、表格、表单、按钮等）自动适配小屏幕

**断点标准统一**：
- 从原来的 768px/1024px 调整为 1199px/1439px（符合实施计划要求）
- 小屏幕字体适度放大（考虑部分员工年龄偏大）
- 按钮和表单在小屏幕下更大、更易点击

**测试建议**：
- 在不同分辨率下测试：1366×768、1920×1080、2560×1440
- 测试不同浏览器：Chrome、Firefox、Edge
- 测试缩放级别：100%、125%、150%

---

### ✅ 第六阶段：UI/UX 优化 - 步骤 6.3 加载状态与错误处理

**实施内容**：

1. **创建全局 Loading 服务** (`frontend/src/utils/loading.js`)
   - 使用计数器管理多个并发请求，确保只有在所有请求完成后才关闭 Loading
   - 提供 `showLoading(message)` 函数显示 Loading
   - 提供 `hideLoading()` 函数隐藏 Loading
   - 提供 `resetLoading()` 函数用于异常情况下的重置
   - 使用 Element Plus 的 `ElLoading.service` 创建全屏 Loading
   - 自定义样式类 `canteen-loading`，支持主题定制

2. **增强 request.js 错误处理** (`frontend/src/api/request.js`)
   - 导入 `ElMessage` 和 `ElMessageBox` 用于统一错误提示
   - 集成全局 Loading 服务，自动在请求开始/结束时显示/隐藏 Loading
   - 请求拦截器：
     - 自动从 localStorage 获取 token 并添加到请求头
     - 每个请求开始前显示 Loading
     - 请求错误时隐藏 Loading
   - 响应拦截器 - 成功处理：
     - 自动隐藏 Loading
     - 检查业务状态码（200/201），其他状态视为业务错误
     - 业务错误使用 `ElMessage` 显示错误消息（5秒）
   - 响应拦截器 - 错误处理：
     - 自动隐藏 Loading
     - 网络错误：显示"网络连接失败，请检查网络设置"
     - HTTP 错误状态处理：
       - 400：请求参数错误
       - 401：使用 `ElMessageBox` 确认对话框提示重新登录（而非直接跳转）
       - 403：没有权限访问
       - 404：请求的资源不存在
       - 500：服务器错误，请稍后重试
       - 502/503/504：网关错误/服务不可用/网关超时
       - 其他：显示具体状态码

3. **创建空状态组件** (`frontend/src/components/EmptyState.vue`)
   - 基于 Element Plus 的 `el-empty` 组件封装
   - 支持多种图标类型：default（默认）、document（文档）、picture（图片）、user（用户）、calendar（日历）、box（盒子）、warning（警告）
   - 支持自定义描述文字、图标颜色、操作按钮
   - 支持按钮尺寸：large、default、small
   - 内置响应式样式：小屏幕下减少内边距和最小高度
   - 使用 `@emit('action')` 触发按钮点击事件
   - 使用食堂主题 CSS 变量（`var(--canteen-spacing-xl)` 等）

**使用方式**：

```vue
<!-- 在页面中使用空状态组件 -->
<template>
  <div class="employee-manage">
    <!-- 数据列表 -->
    <el-table v-if="tableData.length > 0" :data="tableData">
      <!-- ... -->
    </el-table>

    <!-- 空状态 -->
    <EmptyState
      v-else
      icon="user"
      description="暂无员工数据"
      :show-button="true"
      buttonText="新增员工"
      @action="handleAdd"
    />
  </div>
</template>

<script setup>
import EmptyState from '@/components/EmptyState.vue'
// ...
</script>
```

**架构改进**：

| 改进项 | 改进前 | 改进后 |
|-------|--------|--------|
| Loading 状态 | 每个页面单独定义 loading 变量 | 全局自动管理，无需手动处理 |
| 错误提示 | 部分使用 `ElMessage`，部分使用 `ElMessageBox` | 统一使用 `ElMessage` + `ElMessageBox` |
| 网络错误 | 仅在控制台打印 | 显示用户友好的错误提示 |
| 401 处理 | 直接跳转登录页 | 弹出确认对话框，用户确认后才跳转 |
| 空状态 | 显示空白或自行实现 | 统一的空状态组件，支持多种场景 |

**新增文件**：
- `frontend/src/utils/loading.js` - 全局 Loading 服务
- `frontend/src/components/EmptyState.vue` - 空状态组件

**修改文件**：
- `frontend/src/api/request.js` - 集成 Loading 服务，增强错误处理

**待测试项**（由用户验证）：
- [ ] 所有 API 请求自动显示 Loading
- [ ] 并发请求正确显示/隐藏 Loading（计数器逻辑）
- [ ] 网络错误场景：断网、超时、DNS 失败等
- [ ] 401 错误：弹出确认对话框，点击"重新登录"后清除 token 并跳转
- [ ] 其他 HTTP 错误：400、403、404、500 等，显示友好提示
- [ ] 业务错误：code !== 200，显示后端返回的 message
- [ ] 空状态组件在各种场景下正常显示

---

## 通用说明

**技术栈**：Django 5.2+、DRF、MySQL 8.0+、Vue 3、Element Plus、ECharts、Axios、Pinia、Vite

**UI 主题**：橙色 #FF6B35、黄色 #F7C52D、绿色 #4CAF50、浅米色 #FFF8F0

**注意事项**：
- 密码开发阶段明文存储/传输
- API 统一格式：{code, message, data}
- 删除操作有二次确认
- 管理页面路由需要 ADMIN 角色权限
