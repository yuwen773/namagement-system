# 食堂管理系统 - 架构文档

> 本文档说明项目架构和各文件作用，供开发者理解系统结构

---

## 项目结构

```
canteen-management-system/
├── backend/               # Django 后端
│   ├── config/           # 项目配置
│   ├── accounts/         # 用户认证
│   ├── employees/        # 员工档案
│   ├── schedules/        # 排班管理
│   ├── attendance/       # 考勤管理
│   ├── leaves/           # 请假管理
│   ├── salaries/         # 薪资管理
│   └── analytics/        # 统计分析
├── frontend/             # Vue 3 前端
│   └── src/
│       ├── views/        # 页面组件
│       ├── components/   # 可复用组件
│       ├── api/          # API 封装
│       ├── utils/        # 工具函数
│       ├── router/       # 路由配置
│       ├── stores/       # 状态管理
│       ├── layouts/      # 布局组件
│       └── styles/       # 全局样式
├── memory-bank/          # 文档仓库
└── sql/                  # 数据库脚本
```

---

## 后端架构

### 核心设计原则
- **模块化设计**：每个应用对应一个业务领域
- **API 优先**：Django REST Framework 构建 RESTful API
- **前后端分离**：通过 CORS 通信
- **业务分离**：User（登录账号）与 EmployeeProfile（员工档案）独立

### 应用职责

| 应用 | 职责 | 主要模型 |
|------|------|---------|
| `accounts` | 用户登录、注册、认证 | User |
| `employees` | 员工档案管理 | EmployeeProfile |
| `schedules` | 排班计划、调班申请 | Shift, Schedule, ShiftSwapRequest |
| `attendance` | 签到/签退、考勤记录 | AttendanceRecord |
| `leaves` | 请假申请、审批 | LeaveRequest |
| `salaries` | 薪资计算、申诉 | SalaryRecord, Appeal |
| `analytics` | 数据统计 | - |

### 核心业务模型

**User（登录账号）**
```python
username, password, employee_id, role, status
```

**EmployeeProfile（员工档案）**
```python
name, gender, phone, id_card, address
position (CHEF/PASTRY/PREP/CLEANER/SERVER/MANAGER)
entry_date, status
health_certificate_no, health_certificate_expiry
chef_certificate_level
```

**考勤状态规则**
- 缺卡：无签到或无签退
- 迟到：签到时间 > 班次开始 + 5分钟
- 早退：签退时间 < 班次结束 - 5分钟

**薪资计算公式**
```
日工资 = 月基本工资 ÷ 21.75
时薪 = 日工资 ÷ 8
加班费 = 时薪 × 1.5 × 加班小时数
岗位津贴 = CHEF(800)/PASTRY(700)/PREP(500)/CLEANER(300)/SERVER(400)/MANAGER(1000)
实发工资 = 基本工资 + 岗位津贴 + 加班费 - 迟到扣款 - 缺卡扣款
```

---

## 前端架构

### 技术栈
- **Vue 3** + **Vite** + **Element Plus** + **ECharts**
- **Axios** + **Vue Router** + **Pinia**

### 样式架构
```
frontend/src/styles/
├── theme.css          # 食堂主题 CSS 变量和响应式断点
├── mixins.css         # 全局响应式混入样式
└── (未来) icons.css   # 食堂主题图标样式（待实现）
```

**文件作用**：
- `theme.css`：定义所有设计变量（颜色、间距、圆角、阴影、字体），统一主题管理
- `mixins.css`：定义全局响应式样式，自动应用于 Element Plus 组件

**设计变量使用**：
```css
/* 在组件中使用 CSS 变量 */
.my-component {
  color: var(--canteen-text-primary);
  background: var(--canteen-bg-primary);
  padding: var(--canteen-spacing-md);
  border-radius: var(--canteen-border-radius);
}
```

### UI 主题配色
- 主色：`#FF6B35`（橙色）
- 辅助色：`#F7C52D`（黄）、`#4CAF50`（绿）
- 背景色：`#FFF8F0`（浅米色）

### 响应式断点标准
| 断点 | 屏幕宽度 | 字体大小 | 说明 |
|------|---------|---------|------|
| 超小屏 | < 768px | 16px | 移动设备，放大字体方便老年员工 |
| 小屏幕 | < 1200px | 15px | 笔记本电脑 |
| 中等屏 | 1200px - 1439px | 14px | 常见显示器 |
| 大屏幕 | >= 1440px | 16px | 大显示器 |

### 响应式设计策略
1. **布局组件**：AdminLayout 和 EmployeeLayout 自身包含响应式样式
2. **全局混入**：mixins.css 中的样式自动应用于所有页面
3. **组件级样式**：页面组件可使用媒体查询自定义特定样式
4. **Element Plus**：通过深度选择器覆盖第三方组件样式

### 页面结构
```
views/
├── admin/          # 管理员端（Dashboard/员工/排班/考勤/请假/薪资/统计/系统）
├── employee/       # 员工端（首页/个人/签到/考勤/请假/调班/薪资）
└── auth/           # 登录/注册
```

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
2. **数据库迁移**：始终使用 Django migrations
3. **密码存储**：开发阶段明文，生产环境需加密
4. **CORS 配置**：前端开发需配置跨域
5. **User vs EmployeeProfile**：员工档案与登录账号是两个独立概念

---

## 页面架构总览

### 管理员端页面

| 页面 | 文件 | 核心功能 |
|------|------|---------|
| Dashboard | `DashboardView.vue` | 快捷入口、今日概览、待办事项、本月统计 |
| 人员管理 | `EmployeeManageView.vue` | 员工列表、新增/编辑对话框 |
| 排班管理 | `ScheduleManageView.vue` | 日历/列表视图、批量排班、调班审批 |
| 考勤管理 | `AttendanceManageView.vue` | 统计卡片、记录表格、异常处理 |
| 请假审批 | `LeaveApproveView.vue` | 状态 Tab、请假列表、审批对话框 |
| 薪资管理 | `SalaryManageView.vue` | 薪资列表、调整对话框、申诉处理 |
| 统计分析 | `StatisticsView.vue` | 6 个 ECharts 图表 |
| 系统管理 | `SystemManageView.vue` | 用户账号、角色权限、系统设置 |

### 员工端页面

| 页面 | 文件 | 核心功能 |
|------|------|---------|
| 首页 | `HomeView.vue` | 欢迎区、排班卡片、快捷入口、通知列表 |
| 个人信息 | `ProfileView.vue` | 基本信息、资质证书、密码修改、账号信息 |
| 签到签退 | `CheckInView.vue` | 时间显示、签到/签退按钮、打卡日历、月度统计 |
| 考勤记录 | `AttendanceView.vue` | 月份选择、统计卡片、记录表格、异常上报 |
| 请假申请 | `LeaveView.vue` | Tab 分类、请假列表、新增对话框、详情对话框 |
| 调班申请 | `SwapView.vue` | 调班记录列表、原班次/目标班次对比、新增对话框 |
| 薪资查询 | `SalaryView.vue` | 月份选择、薪资脱敏、工资明细、历史记录、申诉功能 |

### 员工端页面详细说明

#### 薪资查询页面 (`SalaryView.vue`)

**文件作用**：员工查看个人工资条和薪资明细的专用页面，支持薪资申诉功能。

**核心功能**：
1. **月份选择器**：使用 Element Plus 月份选择器，支持查看历史薪资
2. **薪资脱敏显示**：默认隐藏所有金额（显示 `****`），点击"查看详情"按钮后显示具体金额
3. **工资总览卡片**：橙色渐变背景，大字显示实发工资，状态标签（草稿/已发布/已调整/申诉中）
4. **工资明细卡片**（4个）：
   - 基本工资（蓝色图标）
   - 岗位津贴（绿色图标）
   - 加班费（橙色图标）+ 加班时长提示
   - 扣款（红色图标）+ 迟到/缺卡次数提示
5. **工资明细说明**：使用 `el-descriptions` 展示完整计算过程，包含公式提示
6. **历史薪资记录**：可点击切换月份，显示月份、金额、状态
7. **薪资申诉对话框**：提交申诉原因（5-200字），带提示信息

**API 调用**：
- `getMySalaries({ employee_id, year_month })` - 获取薪资记录
- `createAppeal({ appeal_type, employee, target_id, reason })` - 提交申诉

**安全设计**：
- 默认脱敏状态 `isShowDetail = false`
- 切换月份后自动重置为脱敏状态
- 所有金额字段使用 `v-if="isShowDetail"` 条件渲染

**数据流向**：
```
用户选择月份 → 调用 getMySalaries() → 返回薪资列表
                ↓
        找到当前月份薪资 → 设置 currentSalary
                ↓
        其他月份记录 → 设置 salaryHistory
                ↓
        用户点击"查看详情" → isShowDetail = true → 显示具体金额
```

**相关文件**：
- `frontend/src/api/salary.js` - 新增 `getMySalaries()` 方法
- `frontend/src/views/employee/SalaryView.vue` - 页面组件

---

## 通用设计模式

### 员工端页面通用结构
```
页面标题 + 副标题
├── 操作卡片（图标 + 说明 + 按钮）
├── 数据列表/卡片展示
└── 对话框（新增/详情）
```

### 常用组件模式
- **Tab 导航**：按状态分类数据（全部/待审批/已通过/已驳回）
- **操作卡片**：橙色/黄色图标 + 说明文字 + 主按钮
- **记录卡片**：左边框强调色 + 悬停平移效果
- **表单验证**：必填字段 + 字数限制 + 实时提示

### 状态标签颜色映射
- 审批中：`warning`（橙色）
- 已通过：`success`（绿色）
- 已驳回：`danger`（红色）
- 正常：`success`（绿色）
- 异常：`warning`/`danger`（橙色/红色）

---

## 关键技术点

### 数据加载策略
- **并行请求**：使用 `Promise.all()` 同时加载相关数据
- **按需加载**：打开对话框时才加载选择列表数据
- **数据缓存**：使用 computed 属性缓存计算结果

### 表单处理
- **表单复用**：通过 `isEdit` 标志区分新增/编辑模式
- **密码处理**：编辑模式下密码为空则不修改
- **日期限制**：禁用过去日期，结束时间不早于开始时间

### 响应式设计
- 大屏（> 768px）：水平布局，多列显示
- 小屏（≤ 768px）：垂直布局，单列显示，全宽按钮

### 安全性
- **权限隔离**：员工只能查看自己的数据
- **二次确认**：删除操作需确认对话框
- **表单验证**：前端验证 + 后端验证
- **薪资脱敏**：
  - 默认隐藏所有金额显示 `****`
  - 用户主动点击"查看详情"后才显示具体金额
  - 切换月份后自动重置为脱敏状态
  - 防止他人窥屏看到敏感薪资信息

---

## 常用 API 模式

### 员工端数据获取
```javascript
// 通过 userStore 获取员工 ID
const employeeId = userStore.userInfo?.employee

// 调用 API 获取数据
const res = await getXXX({ employee_id: employeeId })
```

### 列表数据结构
```javascript
{
  code: 200,
  data: {
    results: [],      // 分页数据
    count: 100        // 总数
  }
}
```

### 统一响应格式
```javascript
{
  code: 200,          // 200成功/400错误
  message: "操作成功",
  data: {}
}
```

---

## 扩展方向

### 功能扩展
- 请假余额显示
- 附件上传（证明文件）
- 调班协商功能
- 考勤异常申诉
- 薪资报表导出

### 技术优化
- 虚拟滚动（大列表）
- 离线打卡支持
- WiFi 定位验证
- 人脸识别集成
- 消息推送通知

---

## 重要文件索引

### 后端核心文件
- `backend/config/settings.py` - 项目配置
- `backend/config/urls.py` - 路由配置
- `backend/accounts/views.py` - 认证视图
- `backend/schedules/serializers.py` - 排班序列化器

### 前端核心文件
- `frontend/src/api/request.js` - Axios 配置、拦截器、Loading 集成、错误处理
- `frontend/src/utils/loading.js` - 全局 Loading 服务（计数器管理并发请求）
- `frontend/src/components/EmptyState.vue` - 空状态组件（用于无数据场景）
- `frontend/src/router/index.js` - 路由配置
- `frontend/src/stores/user.js` - 用户状态
- `frontend/src/layouts/AdminLayout.vue` - 管理员布局
- `frontend/src/layouts/EmployeeLayout.vue` - 员工布局
- `frontend/src/styles/theme.css` - 主题变量和响应式断点
- `frontend/src/styles/mixins.css` - 全局响应式混入样式

### 样式文件说明

#### `theme.css` - 主题变量文件
定义所有食堂主题的 CSS 变量，包括：
- 颜色系统（主色、辅助色、背景色、文字色）
- 间距系统（xs/sm/md/lg/xl）
- 圆角、阴影系统
- 响应式字体大小基准

使用方式：
```css
.component {
  color: var(--canteen-primary);
  padding: var(--canteen-spacing-md);
  border-radius: var(--canteen-border-radius);
}
```

#### `mixins.css` - 响应式混入文件
定义全局响应式样式，自动应用于 Element Plus 组件：
- 表单对话框响应式（小屏幕宽度 95%、垂直布局）
- 表格响应式（小屏幕字体缩小）
- 卡片、分页、输入框、菜单等组件的响应式样式
- 统计卡片网格布局（4列 → 2列 → 1列）

页面组件通过类名（如 `operation-bar`、`stats-cards`）自动应用响应式样式。

---

## 工具函数与可复用组件

### utils 目录
存放前端工具函数和公共服务。

#### `loading.js` - 全局 Loading 服务
**文件作用**：管理全局 Loading 状态，处理并发请求场景。

**核心设计**：
- **计数器模式**：使用 `loadingCount` 跟踪并发请求数量
  - 请求开始：`loadingCount++`
  - 请求结束：`loadingCount--`
  - 只有 `loadingCount === 0` 时才真正关闭 Loading
- **全屏遮罩**：使用 Element Plus 的 `ElLoading.service`
- **异常恢复**：提供 `resetLoading()` 用于异常情况下的强制重置

**使用场景**：
```javascript
import { showLoading, hideLoading } from '@/utils/loading'

// 手动控制（不推荐，request.js 已自动集成）
showLoading('加载中...')
try {
  await someOperation()
} finally {
  hideLoading()
}

// 异常恢复
resetLoading()
```

**集成方式**：在 `request.js` 的拦截器中自动调用，页面组件无需手动处理。

### components 目录
存放可复用的 Vue 组件。

#### `EmptyState.vue` - 空状态组件
**文件作用**：在列表或页面无数据时显示友好的空状态提示。

**组件特性**：
- **多种图标**：支持 default、document、picture、user、calendar、box、warning
- **可定制**：描述文字、图标颜色、操作按钮、按钮尺寸
- **响应式**：小屏幕下自动调整内边距和最小高度
- **主题变量**：使用 `var(--canteen-spacing-xl)` 等主题变量

**使用示例**：
```vue
<template>
  <!-- 列表有数据时显示表格 -->
  <el-table v-if="tableData.length > 0" :data="tableData">
    <!-- ... -->
  </el-table>

  <!-- 无数据时显示空状态 -->
  <EmptyState
    v-else
    icon="user"
    description="暂无员工数据"
    :show-button="true"
    buttonText="新增员工"
    @action="handleAdd"
  />
</template>

<script setup>
import EmptyState from '@/components/EmptyState.vue'
// ...
</script>
```

**Props 说明**：
| Prop | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| description | String | '暂无数据' | 描述文字 |
| icon | String | 'default' | 图标类型 |
| showButton | Boolean | false | 是否显示操作按钮 |
| buttonText | String | '立即创建' | 按钮文字 |
| buttonSize | String | 'default' | 按钮尺寸（large/default/small） |
| iconColor | String | '#CCCCCC' | 图标颜色 |

---

## API 请求处理架构

### 请求拦截器链
```
页面组件发起请求
    ↓
request.js 请求拦截器
    ├─ 从 localStorage 获取 token
    ├─ 添加 Authorization 头
    └─ 调用 showLoading()
    ↓
发送 HTTP 请求
    ↓
request.js 响应拦截器
    ├─ 调用 hideLoading()
    ├─ 检查业务状态码（200/201）
    ├─ 业务错误：显示 ElMessage
    └─ HTTP 错误：分类处理（400/401/403/404/500/502/503/504）
    ↓
返回数据或抛出错误
    ↓
页面组件处理结果
```

### 错误处理策略
| 错误类型 | 处理方式 | 用户体验 |
|---------|---------|---------|
| 网络错误 | ElMessage 提示"网络连接失败" | 5秒自动关闭 |
| 400 参数错误 | ElMessage 提示"请求参数错误" | 3秒自动关闭 |
| 401 未授权 | ElMessageBox 确认对话框 | 用户确认后才跳转登录 |
| 403 无权限 | ElMessage 提示"没有权限访问" | 3秒自动关闭 |
| 404 资源不存在 | ElMessage 提示"请求的资源不存在" | 3秒自动关闭 |
| 500 服务器错误 | ElMessage 提示"服务器错误，请稍后重试" | 3秒自动关闭 |
| 业务错误（code !== 200） | ElMessage 显示后端返回的 message | 5秒自动关闭 |

### Loading 并发处理
```
请求 A 开始 → loadingCount = 1 → 显示 Loading
请求 B 开始 → loadingCount = 2 → 保持 Loading
请求 A 结束 → loadingCount = 1 → 保持 Loading
请求 B 结束 → loadingCount = 0 → 关闭 Loading
```

这种设计确保了在并发请求场景下，Loading 不会闪烁或提前关闭。

---
