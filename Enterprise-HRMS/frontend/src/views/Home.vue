<script setup>
import { computed, h, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const userDisplayName = computed(() => {
  return authStore.user?.real_name || authStore.user?.username || '用户'
})

const userRoleText = computed(() => {
  const roleMap = {
    admin: '管理员',
    hr: '人事专员',
    employee: '普通员工'
  }
  return roleMap[authStore.user?.role] || '用户'
})

// 动态获取当前用户可访问的菜单列表
const accessibleMenus = computed(() => {
  return authStore.getAccessibleMenus()
})

// 页面加载时获取权限配置
onMounted(async () => {
  if (authStore.token && !authStore.rolePermissions) {
    await authStore.fetchRolePermissions()
  }
})

// 菜单图标渲染函数（使用 h 函数创建带 class 的 SVG，确保 scoped CSS 生效）
const renderIcon = (iconName) => {
  const icons = {
    dashboard: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('rect', { x: '3', y: '3', width: '7', height: '7', rx: '1' }),
      h('rect', { x: '14', y: '3', width: '7', height: '7', rx: '1' }),
      h('rect', { x: '3', y: '14', width: '7', height: '7', rx: '1' }),
      h('rect', { x: '14', y: '14', width: '7', height: '7', rx: '1' })
    ]),
    employees: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: '12', cy: '7', r: '4' })
    ]),
    departments: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M3 21h18' }),
      h('path', { d: 'M9 8h1' }),
      h('path', { d: 'M9 12h1' }),
      h('path', { d: 'M9 16h1' }),
      h('path', { d: 'M14 8h1' }),
      h('path', { d: 'M14 12h1' }),
      h('path', { d: 'M14 16h1' }),
      h('path', { d: 'M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16' })
    ]),
    posts: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('rect', { x: '2', y: '7', width: '20', height: '14', rx: '2', ry: '2' }),
      h('path', { d: 'M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16' })
    ]),
    attendance: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('circle', { cx: '12', cy: '12', r: '10' }),
      h('polyline', { points: '12 6 12 12 16 14' })
    ]),
    salary: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('rect', { x: '2', y: '4', width: '20', height: '16', rx: '2' }),
      h('path', { d: 'M12 12h.01' }),
      h('path', { d: 'M6 12h.01' }),
      h('path', { d: 'M18 12h.01' })
    ]),
    approval: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M9 11l3 3L22 4' }),
      h('path', { d: 'M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11' })
    ]),
    onboarding: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: '8.5', cy: '7', r: '4' }),
      h('line', { x1: '20', y1: '8', x2: '20', y2: '14' }),
      h('line', { x1: '23', y1: '11', x2: '17', y2: '11' })
    ]),
    users: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: '9', cy: '7', r: '4' }),
      h('path', { d: 'M23 21v-2a4 4 0 0 0-3-3.87' }),
      h('path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' })
    ]),
    notices: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
      h('polyline', { points: '14 2 14 8 20 8' }),
      h('line', { x1: '16', y1: '13', x2: '8', y2: '13' }),
      h('line', { x1: '16', y1: '17', x2: '8', y2: '17' }),
      h('polyline', { points: '10 9 9 9 8 9' })
    ]),
    performance: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M22 12h-4l-3 9L9 3l-3 9H2' })
    ]),
    profile: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: '12', cy: '7', r: '4' }),
      h('path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' })
    ]),
    setting: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
      h('circle', { cx: '12', cy: '12', r: '3' }),
      h('path', { d: 'M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z' })
    ])
  }
  return icons[iconName]?.() || null
}
</script>

<template>
  <div class="app-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon-wrapper">
            <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="logo-glow"></div>
          </div>
          <span class="logo-text">HRMS</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <el-menu
          :default-active="$route.path"
          router
          class="nav-menu"
        >
          <el-menu-item
            v-for="menu in accessibleMenus"
            :key="menu.path"
            :index="menu.path"
          >
            <div class="menu-item-wrapper">
              <component :is="renderIcon(menu.icon)" />
            </div>
            <span>{{ menu.label }}</span>
          </el-menu-item>
        </el-menu>
      </nav>

      <div class="sidebar-footer">
        <div class="footer-line"></div>
        <span class="version">v1.0</span>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-wrapper">
      <!-- 顶部栏 -->
      <header class="header">
        <div class="header-left">
          <div class="header-decoration"></div>
          <h2 class="header-title">企业人力资源管理系统</h2>
        </div>
        <div class="header-right">
          <el-dropdown trigger="click" placement="bottom-end">
            <div class="user-profile">
              <div class="user-avatar-wrapper">
                <div class="user-avatar">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </div>
                <div class="avatar-ring"></div>
              </div>
              <div class="user-info">
                <span class="user-name">{{ userDisplayName }}</span>
                <span class="user-role">{{ userRoleText }}</span>
              </div>
              <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
            <template #dropdown>
              <el-dropdown-menu class="user-dropdown-menu">
                <el-dropdown-item divided @click="$router.push('/profile')">
                  <svg class="dropdown-item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  <span>个人信息</span>
                </el-dropdown-item>
                <el-dropdown-item divided @click="authStore.logout()">
                  <svg class="dropdown-item-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                    <polyline points="16 17 21 12 16 7"/>
                    <line x1="21" y1="12" x2="9" y2="12"/>
                  </svg>
                  <span>退出登录</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   App Layout - Modern Corporate Design
   ======================================== */
.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--color-bg-primary);
}

/* 侧边栏 */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #1a1d21 0%, #1f2226 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon-wrapper {
  position: relative;
  width: 36px;
  height: 36px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  color: var(--color-primary-light);
  position: relative;
  z-index: 1;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50px;
  height: 50px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.8; }
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.7) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-menu {
  border-right: none;
  background: transparent;
}

.nav-menu:not(.el-menu--collapse) {
  width: 100%;
}

.el-menu-item {
  display: flex;
  align-items: center;
  height: 48px;
  margin-bottom: 4px;
  padding: 0 16px !important;
  color: rgba(255, 255, 255, 0.6);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.el-menu-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background: var(--color-primary);
  border-radius: 0 2px 2px 0;
  transition: height var(--transition-base);
}

.el-menu-item:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

.el-menu-item:hover::before {
  height: 24px;
}

.el-menu-item.is-active {
  color: #ffffff;
  background: rgba(79, 70, 229, 0.15);
}

.el-menu-item.is-active::before {
  height: 24px;
}

.menu-item-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  transition: transform var(--transition-fast);
}

.el-menu-item:hover .nav-icon {
  transform: scale(1.1);
}

.el-menu-item.is-active .nav-icon {
  color: var(--color-primary-light);
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.footer-line {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  margin-bottom: 12px;
}

.version {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
  letter-spacing: 1px;
}

/* 主内容区 */
.main-wrapper {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--color-bg-primary);
}

/* 顶部栏 */
.header {
  height: 64px;
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: var(--shadow-xs);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-decoration {
  width: 4px;
  height: 24px;
  background: linear-gradient(180deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  border-radius: 2px;
}

.header-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  letter-spacing: 0.5px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--color-gray-50);
}

.user-profile:hover {
  background: var(--color-gray-100);
}

.user-avatar-wrapper {
  position: relative;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  z-index: 1;
}

.user-avatar svg {
  width: 18px;
  height: 18px;
}

.avatar-ring {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: var(--radius-lg);
  border: 2px solid transparent;
  background: linear-gradient(135deg, var(--color-primary), var(--color-success)) border-box;
  mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  -webkit-mask-composite: xor;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.user-profile:hover .avatar-ring {
  opacity: 1;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.3;
}

.user-role {
  font-size: 12px;
  color: var(--color-text-tertiary);
  line-height: 1.3;
}

.dropdown-icon {
  width: 16px;
  height: 16px;
  color: var(--color-text-tertiary);
  transition: transform var(--transition-fast);
}

.user-profile:hover .dropdown-icon {
  transform: rotate(180deg);
  color: var(--color-text-secondary);
}

/* 下拉菜单 */
.user-dropdown-menu {
  min-width: 180px;
  padding: 8px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border-light);
}

.user-dropdown-menu .el-dropdown-menu__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 14px;
  transition: all var(--transition-fast);
}

.user-dropdown-menu .el-dropdown-menu__item:hover {
  background: var(--color-gray-100);
  color: var(--color-text-primary);
}

.user-dropdown-menu .el-dropdown-menu__item--divided {
  margin-top: 4px;
  padding-top: 10px;
  border-top-color: var(--color-border-light);
}

.user-dropdown-menu .el-dropdown-menu__item--divided:hover {
  background: var(--color-danger-subtle);
  color: var(--color-danger);
}

.dropdown-item-icon {
  width: 18px;
  height: 18px;
  color: inherit;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 28px 32px;
  min-height: calc(100vh - 64px);
}

/* 页面切换动画 */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.2s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 响应式 */
@media (max-width: 1024px) {
  .sidebar {
    width: 72px;
  }

  .logo-text,
  .el-menu-item span,
  .sidebar-footer,
  .user-info {
    display: none;
  }

  .el-menu-item {
    justify-content: center;
    padding: 0 !important;
  }

  .menu-item-wrapper {
    justify-content: center;
  }

  .main-wrapper {
    margin-left: 72px;
  }

  .user-profile {
    padding: 8px;
  }

  .header {
    padding: 0 20px;
  }

  .main-content {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0 16px;
  }

  .main-content {
    padding: 16px;
  }
}
</style>

<style>
/* 全局 dropdown 样式覆盖 */
.user-dropdown-menu .el-dropdown-menu__item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.user-dropdown-menu .el-dropdown-menu__item--divided {
  margin-top: 4px;
  border-top-color: var(--color-border-light);
}
</style>
