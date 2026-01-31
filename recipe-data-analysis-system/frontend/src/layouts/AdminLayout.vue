<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="admin-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- Logo 区域 -->
      <div class="sidebar-header">
        <router-link to="/admin" class="sidebar-logo">
          <div class="logo-icon">
            <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 8h24v24H8z" stroke="currentColor" stroke-width="2" fill="none"/>
              <path d="M8 14h24" stroke="currentColor" stroke-width="2"/>
              <circle cx="14" cy="11" r="1.5" fill="currentColor"/>
              <circle cx="19" cy="11" r="1.5" fill="currentColor"/>
              <path d="M14 24c0-3 6-3 6 0s-6 3-6 0" stroke="currentColor" stroke-width="1.5" fill="none"/>
              <path d="M12 28c2-4 8-4 10 0" stroke="currentColor" stroke-width="1.5" fill="none"/>
            </svg>
          </div>
          <span v-if="!sidebarCollapsed" class="logo-text">管理后台</span>
        </router-link>
        <button class="collapse-btn" @click="toggleSidebar">
          <svg viewBox="0 0 20 20" fill="none">
            <path v-if="sidebarCollapsed" d="M7 4l6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path v-else d="M13 4l-6 6 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <div class="nav-section">
          <span v-if="!sidebarCollapsed" class="nav-section-title">数据概览</span>
          <router-link
            v-for="item in overviewMenu"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span v-if="!sidebarCollapsed" class="nav-section-title">内容管理</span>
          <router-link
            v-for="item in contentMenu"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          </router-link>
        </div>

        <div class="nav-section">
          <span v-if="!sidebarCollapsed" class="nav-section-title">数据分析</span>
          <router-link
            v-for="item in analyticsMenu"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          </router-link>
        </div>
      </nav>

      <!-- 用户信息 -->
      <div class="sidebar-footer">
        <div class="admin-user">
          <div class="user-avatar">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M10 10a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" stroke-width="1.5"/>
              <path d="M4 18c0-4 3-6 6-6s6 2 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </div>
          <div v-if="!sidebarCollapsed" class="user-info">
            <span class="user-name">{{ userStore.userInfo?.username || '管理员' }}</span>
            <span class="user-role">系统管理员</span>
          </div>
        </div>
        <button v-if="!sidebarCollapsed" class="logout-btn" @click="handleLogout" title="退出登录">
          <svg viewBox="0 0 20 20" fill="none">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="admin-main-wrapper">
      <!-- 顶部栏 -->
      <header class="admin-header">
        <div class="header-left">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
        </div>
        <div class="header-right">
          <router-link to="/" class="header-link">
            <svg viewBox="0 0 20 20" fill="none">
              <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>返回前台</span>
          </router-link>
          <div class="header-user">
            <span class="header-username">{{ userStore.userInfo?.username || '管理员' }}</span>
            <div class="user-avatar-small">
              <svg viewBox="0 0 20 20" fill="none">
                <path d="M10 10a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M4 18c0-4 3-6 6-6s6 2 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="admin-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const sidebarCollapsed = ref(false)

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const isActive = (path) => {
  if (path === '/admin') {
    return route.path === '/admin'
  }
  return route.path.startsWith(path)
}

const currentPageTitle = computed(() => {
  const titles = {
    '/admin': '用户管理',
    '/admin/dashboard': '数据仪表盘',
    '/admin/recipes': '菜谱管理',
    '/admin/ingredients': '食材管理',
    '/admin/categories': '分类管理',
    '/admin/analytics': '深度分析',
    '/admin/behavior': '行为分析'
  }
  return titles[route.path] || '管理后台'
})

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}

// 菜单配置
const overviewMenu = [
  {
    path: '/admin/dashboard',
    label: '数据仪表盘',
    icon: '<svg viewBox="0 0 20 20" fill="none"><path d="M3 4a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1v-4zm8-8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V4zm0 8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
  }
]

const contentMenu = [
  {
    path: '/admin',
    label: '用户管理',
    icon: '<svg viewBox="0 0 20 20" fill="none"><path d="M10 10a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" stroke-width="1.5"/><path d="M4 18c0-4 3-6 6-6s6 2 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
  },
  {
    path: '/admin/recipes',
    label: '菜谱管理',
    icon: '<svg viewBox="0 0 20 20" fill="none"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
  },
  {
    path: '/admin/categories',
    label: '分类管理',
    icon: '<svg viewBox="0 0 20 20" fill="none"><path d="M5 8h10M5 12h8M5 16h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M16 6H8a4 4 0 00-4 4v0a4 4 0 004 4h2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
  },
  {
    path: '/admin/ingredients',
    label: '食材管理',
    icon: '<svg viewBox="0 0 20 20" fill="none"><path d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 8l2.55 3.4A1 1 0 0116 13H6a1 1 0 00-1 1v3a2 2 0 01-2-2V6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
  }
]

const analyticsMenu = [
  {
    path: '/admin/analytics',
    label: '深度分析',
    icon: '<svg viewBox="0 0 20 20" fill="none"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
  },
  {
    path: '/admin/behavior',
    label: '行为分析',
    icon: '<svg viewBox="0 0 20 20" fill="none"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="1.5"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke="currentColor" stroke-width="1.5"/></svg>'
  }
]
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ========== 布局容器 ========== */
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f8f6f3;
}

/* ========== 侧边栏 ========== */
.admin-sidebar {
  width: 260px;
  background: linear-gradient(180deg, #2d3a3f 0%, #1f2a2e 100%);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
}

.admin-sidebar.collapsed {
  width: 72px;
}

/* ========== 侧边栏头部 ========== */
.sidebar-header {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.logo-icon {
  width: 36px;
  height: 36px;
  color: #e8955c;
  flex-shrink: 0;
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #f0ebe6;
  white-space: nowrap;
}

.collapse-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 6px;
  color: #8b9a9e;
  cursor: pointer;
  transition: all 0.2s ease;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e8955c;
}

.collapse-btn svg {
  width: 16px;
  height: 16px;
}

.collapsed .collapse-btn {
  position: absolute;
  right: -14px;
  top: 50%;
  transform: translateY(-50%);
  background: #2d3a3f;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

/* ========== 导航菜单 ========== */
.sidebar-nav {
  flex: 1;
  padding: 1.25rem 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 1.5rem;
}

.nav-section-title {
  display: block;
  padding: 0 1.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #5c6b70;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 1.5rem;
  color: #a3b0b4;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  position: relative;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.04);
  color: #f0ebe6;
}

.nav-item.active {
  background: linear-gradient(90deg, rgba(232, 149, 92, 0.15) 0%, rgba(232, 149, 92, 0.05) 100%);
  color: #e8955c;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #e8955c 0%, #c2622e 100%);
  border-radius: 0 2px 2px 0;
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.nav-label {
  white-space: nowrap;
}

.collapsed .nav-item {
  justify-content: center;
  padding: 0.85rem;
}

/* ========== 侧边栏底部 ========== */
.sidebar-footer {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.admin-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e8955c 0%, #c2622e 100%);
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.user-avatar svg {
  width: 18px;
  height: 18px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #f0ebe6;
}

.user-role {
  font-size: 0.75rem;
  color: #6b7a7e;
}

.logout-btn {
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(231, 76, 60, 0.1);
  border: none;
  border-radius: 8px;
  color: #e74c3c;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(231, 76, 60, 0.2);
}

.logout-btn svg {
  width: 18px;
  height: 18px;
}

.collapsed .sidebar-footer {
  flex-direction: column;
  gap: 0.75rem;
}

.collapsed .admin-user {
  flex-direction: column;
}

/* ========== 主内容区 ========== */
.admin-main-wrapper {
  flex: 1;
  margin-left: 260px;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease;
}

.admin-sidebar.collapsed + .admin-main-wrapper {
  margin-left: 72px;
}

/* ========== 顶部栏 ========== */
.admin-header {
  height: 64px;
  background: white;
  border-bottom: 1px solid #e8e3dd;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3a3f;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.header-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: #6b7a7e;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.header-link:hover {
  background: #f5f2ed;
  color: #c2622e;
}

.header-link svg {
  width: 18px;
  height: 18px;
}

.header-user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-username {
  font-size: 0.9rem;
  font-weight: 500;
  color: #3d2914;
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e8955c 0%, #c2622e 100%);
  border-radius: 50%;
  color: white;
}

.user-avatar-small svg {
  width: 16px;
  height: 16px;
}

/* ========== 页面内容 ========== */
.admin-content {
  flex: 1;
  padding: 2rem;
}

/* ========== 过渡动画 ========== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========== 响应式 ========== */
@media (max-width: 1024px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-sidebar:not(.collapsed) {
    transform: translateX(0);
  }

  .admin-main-wrapper {
    margin-left: 0;
  }

  .collapsed .admin-main-wrapper {
    margin-left: 0;
  }
}
</style>
