# 响应式设计优化实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 让前端在所有屏幕尺寸下完美适配，重点优化桌面端体验，统一使用全局CSS变量断点系统

**架构方案:** 在 App.vue 中定义全局 CSS 变量和响应式工具类，修改各布局组件和业务页面使用统一断点

**技术栈:** Vue 3 + Element Plus + CSS Variables

---

## Task 1: 添加全局 CSS 变量和响应式工具类

**Files:**
- Modify: `canteen-management-system/frontend/src/App.vue`

**Step 1: 添加全局 CSS 变量和响应式工具类**

```vue
<template>
  <router-view />
</template>

<style>
/* ==================== 全局变量 ==================== */
:root {
  /* 响应式断点 */
  --breakpoint-xl: 1440px;
  --breakpoint-lg: 1200px;
  --breakpoint-md: 992px;
  --breakpoint-sm: 768px;
  --breakpoint-xs: 480px;

  /* 主题色 */
  --primary-orange: #FF6B35;
  --primary-light: #FF8C42;
  --primary-dark: #E55A2B;
  --bg-cream: #FFF8F0;
  --bg-light: #FFFDF8;
  --text-primary: #333333;
  --text-secondary: #606266;
  --text-muted: #909399;
  --border-color: #E8DCC8;

  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Microsoft YaHei', 'PingFang SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#app {
  height: 100%;
}

/* ==================== 响应式工具类 ==================== */

/* 大桌面及以上显示 */
@media (min-width: 1440px) {
  .responsive-show-xl { display: block !important; }
  .responsive-hide-xl { display: none !important; }
}

/* 桌面及以上显示 */
@media (min-width: 1200px) {
  .responsive-show-lg { display: block !important; }
  .responsive-hide-lg { display: none !important; }
}

/* 小桌面及以上显示 */
@media (min-width: 992px) {
  .responsive-show-md { display: block !important; }
  .responsive-hide-md { display: none !important; }
}

/* 平板及以上显示 */
@media (min-width: 768px) {
  .responsive-show-sm { display: block !important; }
  .responsive-hide-sm { display: none !important; }
}

/* 默认隐藏，通过媒体查询显示 */
.responsive-show-xs { display: none !important; }
.responsive-show-xxs { display: none !important; }

@media (max-width: 767px) {
  .responsive-show-xs { display: block !important; }
}

@media (max-width: 479px) {
  .responsive-show-xxs { display: block !important; }
}

/* 响应式间距工具类 */
.responsive-p-sm { padding: var(--spacing-sm); }
.responsive-p-md { padding: var(--spacing-md); }
.responsive-p-lg { padding: var(--spacing-lg); }

@media (max-width: 767px) {
  .responsive-p-sm { padding: var(--spacing-xs); }
  .responsive-p-md { padding: var(--spacing-sm); }
  .responsive-p-lg { padding: var(--spacing-md); }
}

/* 响应式文字大小 */
.responsive-text-lg { font-size: 18px; }
.responsive-text-md { font-size: 16px; }
.responsive-text-sm { font-size: 14px; }
.responsive-text-xs { font-size: 12px; }

@media (max-width: 767px) {
  .responsive-text-lg { font-size: 16px; }
  .responsive-text-md { font-size: 14px; }
  .responsive-text-sm { font-size: 13px; }
  .responsive-text-xs { font-size: 11px; }
}

/* 响应式Grid布局 */
.responsive-grid {
  display: grid;
  gap: var(--spacing-md);
}

@media (min-width: 1440px) {
  .responsive-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1200px) and (max-width: 1439px) {
  .responsive-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 992px) and (max-width: 1199px) {
  .responsive-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) and (max-width: 991px) {
  .responsive-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .responsive-grid {
    grid-template-columns: 1fr;
  }
}

/* 响应式表格容器 */
.responsive-table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media (min-width: 768px) {
  .responsive-table-container {
    overflow-x: visible;
  }
}
</style>
```

**Step 2: 保存文件**

文件已修改完成。

**Step 3: Commit**

```bash
git add frontend/src/App.vue
git commit -m "feat: 添加全局CSS变量和响应式工具类"
```

---

## Task 2: 优化 index.html viewport 配置

**Files:**
- Modify: `canteen-management-system/frontend/index.html`

**Step 1: 更新 viewport meta 标签**

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, minimum-scale=1.0, user-scalable=yes" />
    <meta name="theme-color" content="#FF6B35" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <title>食堂管理系统</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

**Step 2: 保存文件**

文件已修改完成。

**Step 3: Commit**

```bash
git add index.html
git commit -m "feat: 优化index.html viewport配置支持响应式"
```

---

## Task 3: 更新 AdminLayout.vue 响应式断点

**Files:**
- Modify: `canteen-management-system/frontend/src/layouts/AdminLayout.vue`

**Step 1: 更新响应式 CSS 断点**

将现有的断点从 `1199px` 调整为使用变量或统一标准：

```css
/* 响应式设计 */
/* 大桌面 1440px+ */
@media (min-width: 1440px) {
  .sidebar {
    width: 200px;
  }

  .main-content {
    padding: 24px;
  }
}

/* 桌面 1200px - 1439px */
@media (min-width: 1200px) and (max-width: 1439px) {
  .sidebar {
    width: 200px;
  }

  .top-header {
    padding: 0 20px;
  }

  .main-content {
    padding: 20px;
  }
}

/* 小桌面 992px - 1199px */
@media (min-width: 992px) and (max-width: 1199px) {
  .top-header {
    padding: 0 16px;
  }

  .header-left {
    gap: 12px;
  }

  .header-right {
    gap: 16px;
  }

  .user-name {
    max-width: 80px;
  }

  .main-content {
    padding: 16px;
  }

  .logo-text {
    font-size: 16px;
  }

  .sidebar-menu :deep(.el-menu-item) {
    height: 52px;
    line-height: 52px;
    margin: 4px 6px;
  }
}

/* 平板 768px - 991px */
@media (min-width: 768px) and (max-width: 991px) {
  .sidebar {
    width: 64px;
  }

  .logo-area {
    padding: 0;
  }

  .logo-text,
  .sidebar-menu :deep(.el-menu-item span) {
    display: none;
  }

  .top-header {
    padding: 0 12px;
  }

  .main-content {
    padding: 12px;
  }

  .date-info {
    display: none;
  }

  .user-name {
    display: none;
  }
}

/* 手机 < 768px */
@media (max-width: 767px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .main-container {
    margin-left: 0;
  }

  .user-name {
    display: none;
  }

  .date-info {
    display: none;
  }

  .logo-text {
    font-size: 14px;
  }

  .main-content {
    padding: 8px;
  }

  .collapse-btn {
    min-width: 40px;
    min-height: 40px;
  }

  .header-left :deep(.el-breadcrumb) {
    font-size: 13px;
  }
}
```

**Step 2: 添加移动端侧边栏遮罩层**

在 template 中添加遮罩层：

```vue
<!-- 移动端遮罩层 -->
<div
  v-if="isMobileMenuOpen"
  class="mobile-overlay"
  @click="closeMobileMenu"
></div>
```

添加相关状态和方法：

```javascript
// 移动端菜单状态
const isMobileMenuOpen = ref(false)

// 响应式检测
const isMobile = ref(window.innerWidth < 768)

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

const openMobileMenu = () => {
  if (isMobile.value) {
    isMobileMenuOpen.value = true
  }
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

onMounted(() => {
  updateDate()
  dateTimer = setInterval(updateDate, 1000)
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  if (dateTimer) {
    clearInterval(dateTimer)
  }
  window.removeEventListener('resize', checkMobile)
})
```

添加遮罩层样式：

```css
.mobile-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}
```

**Step 3: Commit**

```bash
git add frontend/src/layouts/AdminLayout.vue
git commit -feat: 更新AdminLayout响应式断点和移动端菜单
```

---

## Task 4: 更新 EmployeeLayout.vue 响应式断点

**Files:**
- Modify: `canteen-management-system/frontend/src/layouts/EmployeeLayout.vue`

**Step 1: 更新响应式 CSS 断点**

```css
/* 响应式设计 */
/* 大桌面 1440px+ */
@media (min-width: 1440px) {
  .top-menu {
    max-width: 800px;
  }
}

/* 桌面 1200px - 1439px */
@media (min-width: 1200px) and (max-width: 1439px) {
  .top-header {
    padding: 0 20px;
  }

  .header-right {
    gap: 16px;
  }

  .user-name {
    max-width: 80px;
  }

  .main-content {
    padding: 18px;
  }

  .logo-text {
    font-size: 18px;
  }

  .top-menu {
    max-width: 600px;
  }

  .top-menu :deep(.el-menu-item) {
    font-size: 15px;
    padding: 0 16px;
  }
}

/* 小桌面 992px - 1199px */
@media (min-width: 992px) and (max-width: 1199px) {
  .top-header {
    padding: 0 16px;
  }

  .header-right {
    gap: 12px;
  }

  .user-name {
    max-width: 60px;
  }

  .main-content {
    padding: 16px;
  }

  .logo-text {
    font-size: 16px;
  }

  .top-menu {
    max-width: 500px;
  }

  .top-menu :deep(.el-menu-item) {
    font-size: 14px;
    padding: 0 12px;
    height: 56px;
    line-height: 56px;
  }
}

/* 平板 768px - 991px */
@media (min-width: 768px) and (max-width: 991px) {
  .top-header {
    padding: 0 12px;
    height: 56px;
  }

  .logo-text {
    font-size: 14px;
  }

  .header-center {
    display: none;
  }

  .header-right {
    gap: 12px;
  }

  .user-name {
    display: none;
  }

  .date-info {
    display: none;
  }

  .main-content {
    padding: 12px;
  }

  /* 平板显示简化的底部导航 */
  .mobile-nav {
    display: flex;
  }
}

/* 手机 < 768px */
@media (max-width: 767px) {
  .top-header {
    padding: 0 8px;
    height: 52px;
  }

  .logo-text {
    display: none;
  }

  .header-center {
    display: none;
  }

  .date-info {
    display: none;
  }

  .user-name {
    display: none;
  }

  .main-content {
    padding: 8px;
  }

  .top-menu :deep(.el-menu-item) {
    font-size: 14px;
    padding: 0 8px;
    height: 56px;
    line-height: 56px;
  }

  .user-dropdown {
    padding: 6px 8px;
  }

  .user-dropdown,
  .top-menu :deep(.el-menu-item) {
    min-height: 44px;
  }
}
```

**Step 2: 添加移动端底部导航（可选）**

如果需要平板/手机端有更好的导航体验，可以添加底部导航栏。

**Step 3: Commit**

```bash
git add frontend/src/layouts/EmployeeLayout.vue
git commit -m "feat: 更新EmployeeLayout响应式断点"
```

---

## Task 5: 优化 LoginView.vue 响应式细节

**Files:**
- Modify: `canteen-management-system/frontend/src/views/auth/LoginView.vue`

**Step 1: 微调响应式样式**

检查现有响应式样式是否完整，补充缺失的断点：

```css
/* 超大桌面 1920px+ */
@media (min-width: 1920px) {
  .brand-side {
    width: 58%;
  }

  .form-wrapper {
    max-width: 480px;
  }
}

/* 确保 1440px 断点 */
@media (min-width: 1440px) and (max-width: 1919px) {
  .brand-side {
    width: 54%;
  }
}

/* 小屏幕优化 */
@media (max-width: 360px) {
  .brand-title {
    font-size: 22px;
  }

  .form-header h2 {
    font-size: 20px;
  }

  .login-form {
    padding: 20px 14px;
  }
}
```

**Step 2: Commit**

```bash
git add frontend/src/views/auth/LoginView.vue
git commit -m "feat: 优化LoginView响应式细节"
```

---

## Task 6: 优化 DashboardView.vue 卡片 Grid 布局

**Files:**
- Modify: `canteen-management-system/frontend/src/views/admin/DashboardView.vue`

**Step 1: 更新响应式 Grid 布局**

```css
/* 响应式设计 */
/* 大桌面 1440px+ */
@media (min-width: 1440px) {
  .quick-access-grid {
    grid-template-columns: repeat(5, 1fr);
  }

  .overview-cards {
    grid-template-columns: repeat(3, 1fr);
  }

  .monthly-cards {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* 桌面 1200px - 1439px */
@media (min-width: 1200px) and (max-width: 1439px) {
  .quick-access-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .overview-cards {
    grid-template-columns: repeat(3, 1fr);
  }

  .monthly-cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* 小桌面 992px - 1199px */
@media (min-width: 992px) and (max-width: 1199px) {
  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .overview-card:last-child {
    grid-column: span 2;
  }

  .monthly-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 平板 768px - 991px */
@media (min-width: 768px) and (max-width: 991px) {
  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .overview-cards {
    grid-template-columns: 1fr;
  }

  .monthly-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 手机 < 768px */
@media (max-width: 767px) {
  .welcome-title {
    font-size: 20px;
  }

  .welcome-subtitle {
    font-size: 13px;
  }

  .quick-access-grid {
    grid-template-columns: 1fr;
  }

  .overview-cards {
    grid-template-columns: 1fr;
  }

  .monthly-cards {
    grid-template-columns: 1fr;
  }

  .card-icon {
    width: 48px;
    height: 48px;
    font-size: 24px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-value-large {
    font-size: 28px;
  }

  .monthly-value {
    font-size: 20px;
  }
}
```

**Step 2: Commit**

```bash
git add frontend/src/views/admin/DashboardView.vue
git commit -m "feat: 优化DashboardView响应式Grid布局"
```

---

## Task 7: 优化业务页面表格响应式

**Files:**
- Modify: `canteen-management-system/frontend/src/views/admin/EmployeeManageView.vue`
- Modify: `canteen-management-system/frontend/src/views/admin/ScheduleManageView.vue`
- Modify: `canteen-management-system/frontend/src/views/admin/AttendanceManageView.vue`
- Modify: `canteen-management-system/frontend/src/views/admin/SalaryManageView.vue`

**Step 1: 为表格容器添加响应式类**

在每个管理页面的表格外层容器添加 `responsive-table-container` 类：

```vue
<div class="responsive-table-container">
  <el-table ...>
    ...
  </el-table>
</div>
```

**Step 2: 添加表格响应式样式**

```css
.responsive-table-container {
  width: 100%;
}

@media (max-width: 767px) {
  .responsive-table-container :deep(.el-table) {
    font-size: 13px;
  }

  .responsive-table-container :deep(.el-table__header th) {
    padding: 8px 0;
  }

  .responsive-table-container :deep(.el-table__body td) {
    padding: 10px 0;
  }
}
```

**Step 3: 逐个修改文件并提交**

```bash
git add frontend/src/views/admin/EmployeeManageView.vue
git commit -m "feat: 优化EmployeeManageView表格响应式"
```

---

## Task 8: 测试验证

**Step 1: 启动开发服务器**

```bash
cd canteen-management-system/frontend
npm run dev
```

**Step 2: 测试各断点**

在不同浏览器窗口尺寸下测试：
- 1920px (大桌面)
- 1440px (桌面)
- 1200px (小桌面)
- 992px (平板横屏)
- 768px (平板竖屏)
- 480px (手机)

**Step 3: 检查项目是否正常运行**

```bash
npm run build
```

确保构建无错误。

**Step 4: Commit**

```bash
git commit -m "test: 验证响应式设计在各断点正常工作"
```

---

## 执行方式选择

**计划完成并保存到 `docs/plans/2026-02-22-responsive-implementation.md`。两种执行方式：**

**1. Subagent-Driven (本会话)** - 每个任务分配一个子代理，任务间进行代码审查，快速迭代

**2. Parallel Session (单独会话)** - 在新会话中使用 executing-plans，批量执行并设置检查点

**选择哪种方式？**
