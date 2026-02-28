<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  DataBoard, DataAnalysis, Setting, User, SwitchButton,
  Expand, Fold, Histogram, TrendCharts, ShoppingCart, Bell
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const isCollapsed = ref(false)

const menuItems = computed(() => [
  {
    path: '/admin/dashboard',
    icon: DataBoard,
    title: '数据概览',
    color: '#FF6B35'
  },
  {
    path: '/admin/statistics',
    icon: Histogram,
    title: '数据分析',
    color: '#7B2CBF'
  },
  {
    path: '/admin/crawler',
    icon: TrendCharts,
    title: '数据采集',
    color: '#FFD700'
  },
  {
    path: '/admin/crawler/config',
    icon: Setting,
    title: '爬虫配置',
    color: '#06FFA5'
  },
  {
    path: '/admin/products',
    icon: ShoppingCart,
    title: '商品管理',
    color: '#FF6B35'
  },
  {
    path: '/admin/users',
    icon: User,
    title: '用户管理',
    color: '#7B2CBF'
  },
  {
    path: '/admin/announcements',
    icon: Bell,
    title: '公告管理',
    color: '#FFD700'
  }
])

const activeMenu = computed(() => route.path)

const isActive = (path) => {
  if (activeMenu.value === path) return true
  if (activeMenu.value.startsWith(path + '/')) {
    const hasMoreSpecificMatch = menuItems.value.some(item => {
      if (item.path === path) return false
      return item.path.length > path.length && activeMenu.value.startsWith(item.path + '/') || activeMenu.value === item.path
    })
    return !hasMoreSpecificMatch
  }
  return false
}

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside :class="['sidebar', { 'is-collapsed': isCollapsed }]">
      <!-- Sidebar Header -->
      <div class="sidebar-header">
        <transition name="logo-expand">
          <div v-if="!isCollapsed" class="logo-full">
            <div class="logo-icon">
              <svg viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="56" height="56" rx="16" fill="url(#adminLogoGrad)"/>
                <g transform="translate(14, 11)">
                  <path d="M14 4 L24 14 L14 24 L4 14 Z" fill="white"/>
                  <path d="M10 24 L14 28 L18 24" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="14" cy="14" r="4" fill="#FF6B35"/>
                </g>
                <defs>
                  <linearGradient id="adminLogoGrad" x1="0" y1="0" x2="56" y2="56">
                    <stop offset="0%" stop-color="#FF6B35"/>
                    <stop offset="100%" stop-color="#7B2CBF"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div class="logo-text">
              <span class="logo-title">宠物用品数据</span>
              <span class="logo-badge">ADMIN</span>
            </div>
          </div>
        </transition>
        <transition name="logo-shrink">
          <div v-if="isCollapsed" class="logo-mini">
            <svg viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="56" height="56" rx="16" fill="url(#adminLogoGradMini)"/>
              <g transform="translate(14, 11)">
                <path d="M14 4 L24 14 L14 24 L4 14 Z" fill="white"/>
                <path d="M10 24 L14 28 L18 24" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="14" cy="14" r="4" fill="#FF6B35"/>
              </g>
              <defs>
                <linearGradient id="adminLogoGradMini" x1="0" y1="0" x2="56" y2="56">
                  <stop offset="0%" stop-color="#FF6B35"/>
                  <stop offset="100%" stop-color="#7B2CBF"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
        </transition>
      </div>

      <!-- Navigation -->
      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
          :style="{ '--nav-color': item.color }"
        >
          <component :is="item.icon" class="nav-icon" />
          <transition name="nav-text">
            <span v-if="!isCollapsed" class="nav-label">{{ item.title }}</span>
          </transition>
          <span class="nav-glow" :style="{ background: item.color }"></span>
        </router-link>
      </nav>

      <!-- Sidebar Footer -->
      <div class="sidebar-footer">
        <button class="collapse-btn" @click="toggleCollapse">
          <component :is="isCollapsed ? Expand : Fold" class="icon" />
          <transition name="collapse-text">
            <span v-if="!isCollapsed" class="collapse-label">收起侧边栏</span>
          </transition>
        </button>
      </div>
    </aside>

    <!-- Main Wrapper -->
    <div class="main-wrapper">
      <!-- Top Header -->
      <header class="top-header">
        <div class="header-left">
          <h1 class="page-title">{{ route.meta.title || '管理控制台' }}</h1>
          <span class="page-breadcrumb">控制台 / {{ route.meta.title || '首页' }}</span>
        </div>

        <div class="header-right">
          <div class="user-profile">
            <div class="user-avatar">
              <User class="avatar-icon" />
            </div>
            <div class="user-info">
              <span class="user-name">{{ userStore.userInfo?.username || 'Admin' }}</span>
              <span class="user-role">系统管理员</span>
            </div>
          </div>

          <el-dropdown @command="handleLogout" trigger="click">
            <button class="logout-btn">
              <SwitchButton class="icon" />
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">
                  <SwitchButton class="dropdown-icon" />
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- Content Area -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="content-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens
   ============================================ */
.admin-layout {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --bg-primary: #0D0D14;
  --bg-sidebar: rgba(15, 15, 24, 0.95);
  --bg-elevated: rgba(255, 255, 255, 0.03);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-hover: rgba(255, 107, 53, 0.3);

  display: flex;
  height: 100vh;
  overflow: hidden;
  background: var(--bg-primary);
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
}

/* ============================================
   Sidebar
   ============================================ */
.sidebar {
  width: 280px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 50;
  backdrop-filter: blur(20px);
}

.sidebar.is-collapsed {
  width: 80px;
}

/* Sidebar Header */
.sidebar-header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.logo-full {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  filter: drop-shadow(0 4px 16px rgba(255, 107, 53, 0.3));
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 15px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-orange), #FFD700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
  line-height: 1;
}

.logo-badge {
  font-family: 'Outfit', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--text-tertiary);
}

.logo-mini {
  width: 40px;
  height: 40px;
}

.logo-mini svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 12px rgba(255, 107, 53, 0.25));
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: var(--border-default);
  border-radius: 2px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 14px;
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--bg-elevated);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-item:hover {
  color: var(--text-secondary);
}

.nav-item:hover::before {
  opacity: 1;
}

.nav-item.active {
  color: white;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(123, 44, 191, 0.15));
}

.nav-item.active .nav-icon {
  color: var(--nav-color);
  filter: drop-shadow(0 0 12px var(--nav-color));
}

.nav-item.active .nav-glow {
  opacity: 1;
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.nav-label {
  position: relative;
  z-index: 1;
  white-space: nowrap;
}

.nav-glow {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  border-radius: 0 4px 4px 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-subtle);
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: 14px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.collapse-btn:hover {
  background: rgba(255, 107, 53, 0.08);
  border-color: var(--border-hover);
  color: var(--primary-orange);
}

.collapse-btn .icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.collapse-label {
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

/* ============================================
   Main Wrapper
   ============================================ */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* Background Decoration */
.main-wrapper::before {
  content: '';
  position: absolute;
  top: -200px;
  right: -200px;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255, 107, 53, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
}

/* Top Header */
.top-header {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 32px;
  background: rgba(13, 13, 20, 0.8);
  backdrop-filter: blur(24px);
  border-bottom: 1px solid var(--border-subtle);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.02em;
}

.page-breadcrumb {
  font-family: 'Outfit', sans-serif;
  font-size: 12px;
  color: var(--text-tertiary);
  letter-spacing: 0.05em;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px 8px 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: 24px;
  transition: all 0.3s ease;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-hover);
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  border-radius: 12px;
}

.avatar-icon {
  width: 18px;
  height: 18px;
  color: white;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

.user-role {
  font-size: 11px;
  color: var(--text-tertiary);
  font-weight: 500;
}

.logout-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: 14px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  color: #ff6b6b;
  border-color: rgba(255, 107, 107, 0.3);
  background: rgba(255, 107, 107, 0.08);
}

.logout-btn .icon {
  width: 18px;
  height: 18px;
}

/* Main Content */
.main-content {
  flex: 1;
  position: relative;
  z-index: 1;
  padding: 32px;
  overflow-y: auto;
  overflow-x: hidden;
}

.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: transparent;
}

.main-content::-webkit-scrollbar-thumb {
  background: var(--border-default);
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: var(--border-hover);
}

/* ============================================
   Animations
   ============================================ */
.logo-expand-enter-active,
.logo-expand-leave-active {
  transition: all 0.3s ease;
}

.logo-expand-enter-from,
.logo-expand-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.logo-shrink-enter-active,
.logo-shrink-leave-active {
  transition: all 0.3s ease;
}

.logo-shrink-enter-from,
.logo-shrink-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.nav-text-enter-active,
.nav-text-leave-active {
  transition: all 0.2s ease;
}

.nav-text-enter-from,
.nav-text-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.collapse-text-enter-active,
.collapse-text-leave-active {
  transition: all 0.2s ease;
}

.collapse-text-enter-from,
.collapse-text-leave-to {
  opacity: 0;
  width: 0;
}

.content-fade-enter-active,
.content-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-fade-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.content-fade-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1024px) {
  .sidebar {
    position: absolute;
    height: 100%;
  }

  .sidebar.is-collapsed {
    width: 280px;
    transform: translateX(-100%);
  }
}
</style>
