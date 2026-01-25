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

// 菜单图标渲染函数 - 每个菜单都有独特的图标
const renderIcon = (iconName) => {
  const icons = {
    // 仪表盘 - 房子
    dashboard: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }),
      h('polyline', { points: '9 22 9 12 15 12 15 22' })
    ]),
    // 员工管理 - 人员卡片
    employees: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('rect', { x: '2', y: '5', width: '20', height: '14', rx: '2' }),
      h('path', { d: 'M2 10h20' }),
      h('circle', { cx: '7', cy: '19', r: '2' }),
      h('circle', { cx: '17', cy: '19', r: '2' })
    ]),
    // 部门管理 - 树形结构
    departments: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M12 22V8' }),
      h('path', { d: 'M5 12H2a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h3' }),
      h('path', { d: 'M22 12h-3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h3' }),
      h('circle', { cx: '12', cy: '8', r: '3' })
    ]),
    // 岗位管理 - 标签
    posts: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z' }),
      h('line', { x1: '7', y1: '7', x2: '7.01', y2: '7' })
    ]),
    // 考勤管理 - 日历
    attendance: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('rect', { x: '3', y: '4', width: '18', height: '18', rx: '2', ry: '2' }),
      h('line', { x1: '16', y1: '2', x2: '16', y2: '6' }),
      h('line', { x1: '8', y1: '2', x2: '8', y2: '6' }),
      h('line', { x1: '3', y1: '10', x2: '21', y2: '10' })
    ]),
    // 薪资管理 - 信用卡
    salary: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('rect', { x: '1', y: '4', width: '22', height: '16', rx: '2', ry: '2' }),
      h('line', { x1: '1', y1: '10', x2: '23', y2: '10' }),
      h('path', { d: 'M12 12m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0' })
    ]),
    // 审批中心 - 印章
    approval: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z' }),
      h('path', { d: 'M9 12l2 2 4-4' })
    ]),
    // 入职管理 - 欢迎手势
    onboarding: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: '9', cy: '7', r: '4' }),
      h('line', { x1: '19', y1: '8', x2: '19', y2: '14' }),
      h('line', { x1: '22', y1: '11', x2: '16', y2: '11' }),
      h('path', { d: 'M16 3a5 5 0 0 1 0 10' })
    ]),
    // 用户管理 - 多人轮廓
    users: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: '9', cy: '7', r: '4' }),
      h('path', { d: 'M22 21v-2a4 4 0 0 0-3-3.87' }),
      h('path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' })
    ]),
    // 公告管理 - 广播
    notices: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M22 2L11 13' }),
      h('path', { d: 'M22 2l-7 20-4-9-9-4 20-7z' })
    ]),
    // 绩效管理 - 靶心
    performance: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('circle', { cx: '12', cy: '12', r: '10' }),
      h('circle', { cx: '12', cy: '12', r: '6' }),
      h('circle', { cx: '12', cy: '12', r: '2' })
    ]),
    // 个人中心 - 用户徽章
    profile: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: '12', cy: '7', r: '4' }),
      h('path', { d: 'M12 3v1' }),
      h('path', { d: 'M12 20v1' })
    ]),
    // 系统设置 - 滑块
    setting: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('line', { x1: '4', y1: '21', x2: '4', y2: '14' }),
      h('line', { x1: '4', y1: '10', x2: '4', y2: '3' }),
      h('line', { x1: '12', y1: '21', x2: '12', y2: '12' }),
      h('line', { x1: '12', y1: '8', x2: '12', y2: '3' }),
      h('line', { x1: '20', y1: '21', x2: '20', y2: '16' }),
      h('line', { x1: '20', y1: '12', x2: '20', y2: '3' }),
      h('line', { x1: '1', y1: '14', x2: '7', y2: '14' }),
      h('line', { x1: '9', y1: '8', x2: '15', y2: '8' }),
      h('line', { x1: '17', y1: '16', x2: '23', y2: '16' })
    ]),
    // 数据中心 - 服务器
    data: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('rect', { x: '2', y: '2', width: '20', height: '8', rx: '2', ry: '2' }),
      h('rect', { x: '2', y: '14', width: '20', height: '8', rx: '2', ry: '2' }),
      h('line', { x1: '6', y1: '6', x2: '6.01', y2: '6' }),
      h('line', { x1: '6', y1: '18', x2: '6.01', y2: '18' })
    ]),
    // 权限管理 - 钥匙
    permission: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4' })
    ]),
    // 离职管理 - 出口
    resignation: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6' }),
      h('polyline', { points: '15 3 21 3 21 9' }),
      h('line', { x1: '10', y1: '14', x2: '21', y2: '3' })
    ]),
    // 安全配置 - 盾牌
    security: () => h('svg', { class: 'nav-icon', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z' }),
      h('path', { d: 'M9 12l2 2 4-4' })
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

.el-menu-item.is-active::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 60px;
  height: 30px;
  background: radial-gradient(ellipse at right, rgba(79, 70, 229, 0.15) 0%, transparent 70%);
  pointer-events: none;
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  filter: drop-shadow(0 0 0 rgba(99, 102, 241, 0));
}

.el-menu-item:hover .nav-icon {
  transform: scale(1.12);
  filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.5));
}

.el-menu-item.is-active .nav-icon {
  color: var(--color-primary-light);
  filter: drop-shadow(0 0 4px rgba(99, 102, 241, 0.4));
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
