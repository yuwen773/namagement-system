<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  DataBoard, DataAnalysis, Setting, User, SwitchButton,
  Expand, Fold, Histogram, TrendCharts, ShoppingCart, Bell, Message
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
    color: '#2D6A4F'
  },
  {
    path: '/admin/statistics',
    icon: Histogram,
    title: '数据分析',
    color: '#40916C'
  },
  {
    path: '/admin/crawler',
    icon: TrendCharts,
    title: '数据采集',
    color: '#52B788'
  },
  {
    path: '/admin/crawler/config',
    icon: Setting,
    title: '爬虫配置',
    color: '#74C69D'
  },
  {
    path: '/admin/products',
    icon: ShoppingCart,
    title: '商品管理',
    color: '#00B4D8'
  },
  {
    path: '/admin/users',
    icon: User,
    title: '用户管理',
    color: '#90E0EF'
  },
  {
    path: '/admin/announcements',
    icon: Bell,
    title: '公告管理',
    color: '#2D6A4F'
  },
  {
    path: '/admin/feedback',
    icon: Message,
    title: '反馈管理',
    color: '#40916C'
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
    <!-- 自然背景装饰 -->
    <div class="layout-background">
      <div class="paper-texture"></div>
      <div class="ambient-glow glow-1"></div>
      <div class="ambient-glow glow-2"></div>

      <!-- 叶片装饰 -->
      <div class="leaf-decoration leaf-left">
        <svg viewBox="0 0 80 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M40 10C40 10 70 30 70 60C70 90 55 110 40 110C25 110 10 90 10 60C10 30 40 10 40 10Z" fill="url(#leafGradLeft)" opacity="0.08"/>
          <path d="M40 10L40 110" stroke="url(#leafGradLeft)" stroke-width="1" opacity="0.15"/>
          <defs>
            <linearGradient id="leafGradLeft" x1="40" y1="10" x2="40" y2="110">
              <stop offset="0%" stop-color="#52B788"/>
              <stop offset="100%" stop-color="#2D6A4F"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <div class="leaf-decoration leaf-right">
        <svg viewBox="0 0 60 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M30 8C30 8 52 24 52 50C52 76 40 92 30 92C20 92 8 76 8 50C8 24 30 8 30 8Z" fill="url(#leafGradRight)" opacity="0.06"/>
          <defs>
            <linearGradient id="leafGradRight" x1="30" y1="8" x2="30" y2="92">
              <stop offset="0%" stop-color="#90E0EF"/>
              <stop offset="100%" stop-color="#00B4D8"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>

    <!-- Sidebar -->
    <aside :class="['sidebar', { 'is-collapsed': isCollapsed }]">
      <!-- Sidebar Header -->
      <div class="sidebar-header">
        <transition name="logo-expand">
          <div v-if="!isCollapsed" class="logo-full">
            <div class="logo-icon">
              <svg viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="28" cy="28" r="26" fill="url(#sidebarLogoBg)" fill-opacity="0.15"/>
                <circle cx="28" cy="28" r="26" stroke="url(#sidebarLogoBorder)" stroke-width="1.5"/>
                <g transform="translate(28, 28)">
                  <path d="M0 -14C0 -14 12 -6 12 6C12 16 6 18 0 18C-6 18 -12 16 -12 6C-12 -6 0 -14 0 -14Z" fill="url(#sidebarLogoLeaf)"/>
                  <path d="M0 -14L0 18" stroke="white" stroke-width="1.2" stroke-linecap="round" opacity="0.5"/>
                  <circle cx="0" cy="-14" r="3" fill="#52B788"/>
                </g>
                <defs>
                  <linearGradient id="sidebarLogoBg" x1="2" y1="2" x2="54" y2="54">
                    <stop offset="0%" stop-color="#52B788"/>
                    <stop offset="100%" stop-color="#2D6A4F"/>
                  </linearGradient>
                  <linearGradient id="sidebarLogoBorder" x1="2" y1="2" x2="54" y2="54">
                    <stop offset="0%" stop-color="#74C69D"/>
                    <stop offset="100%" stop-color="#40916C"/>
                  </linearGradient>
                  <linearGradient id="sidebarLogoLeaf" x1="-12" y1="-14" x2="12" y2="18">
                    <stop offset="0%" stop-color="#74C69D"/>
                    <stop offset="100%" stop-color="#40916C"/>
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
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="24" cy="24" r="22" fill="url(#miniLogoBg)" fill-opacity="0.15"/>
              <circle cx="24" cy="24" r="22" stroke="url(#miniLogoBorder)" stroke-width="1.5"/>
              <g transform="translate(24, 24)">
                <path d="M0 -12C0 -12 10 -5 10 5C10 14 5 16 0 16C-5 16 -10 14 -10 5C-10 -5 0 -12 0 -12Z" fill="url(#miniLogoLeaf)"/>
                <circle cx="0" cy="-12" r="2.5" fill="#52B788"/>
              </g>
              <defs>
                <linearGradient id="miniLogoBg" x1="2" y1="2" x2="46" y2="46">
                  <stop offset="0%" stop-color="#52B788"/>
                  <stop offset="100%" stop-color="#2D6A4F"/>
                </linearGradient>
                <linearGradient id="miniLogoBorder" x1="2" y1="2" x2="46" y2="46">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="miniLogoLeaf" x1="-10" y1="-12" x2="10" y2="16">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
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
          <div class="nav-icon-wrapper">
            <component :is="item.icon" class="nav-icon" />
          </div>
          <transition name="nav-text">
            <span v-if="!isCollapsed" class="nav-label">{{ item.title }}</span>
          </transition>
          <span class="nav-indicator" :style="{ background: item.color }"></span>
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

        <!-- 装饰小植物 -->
        <div v-if="!isCollapsed" class="footer-plant">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
            <path d="M20 35V15" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M20 25C20 25 28 20 28 14C28 10 25 8 20 8C15 8 12 10 12 14C12 20 20 25 20 25Z" fill="#74C69D" fill-opacity="0.2"/>
            <path d="M20 18C20 18 26 15 26 10C26 7 23 5 20 5C17 5 14 7 14 10C14 15 20 18 20 18Z" fill="#52B788" fill-opacity="0.3"/>
          </svg>
        </div>
      </div>
    </aside>

    <!-- Main Wrapper -->
    <div class="main-wrapper">
      <!-- Top Header -->
      <header class="top-header">
        <div class="header-left">
          <div class="page-info">
            <h1 class="page-title">{{ route.meta.title || '管理控制台' }}</h1>
            <span class="page-breadcrumb">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M7 2L2 7L7 12M12 7H2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              控制台 / {{ route.meta.title || '首页' }}
            </span>
          </div>
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.admin-layout {
  --primary-green: #2D6A4F;
  --primary-green-light: #40916C;
  --primary-green-lighter: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-sidebar: rgba(255, 255, 255, 0.9);
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);

  display: flex;
  height: 100vh;
  overflow: hidden;
  background: var(--bg-cream);
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  position: relative;
}

/* ============================================
   Layout Background
   ============================================ */
.layout-background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.paper-texture {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.02'/%3E%3C/svg%3E");
  opacity: 0.5;
}

.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  animation: ambientDrift 40s ease-in-out infinite;
}

.glow-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(82, 183, 136, 0.15) 0%, transparent 70%);
  top: -150px;
  right: -150px;
  animation-delay: 0s;
}

.glow-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(144, 224, 239, 0.12) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation-delay: -20s;
}

@keyframes ambientDrift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-20px, 30px) scale(0.95); }
  75% { transform: translate(20px, 20px) scale(1.02); }
}

.leaf-decoration {
  position: absolute;
  opacity: 0.5;
}

.leaf-left {
  top: 20%;
  left: 280px;
  width: 100px;
  height: 150px;
}

.leaf-right {
  bottom: 15%;
  right: 60px;
  width: 80px;
  height: 133px;
}

/* ============================================
   Sidebar
   ============================================ */
.sidebar {
  width: 280px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-light);
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
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, rgba(116, 198, 157, 0.03) 0%, transparent 100%);
}

.logo-full {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  animation: logoBreath 6s ease-in-out infinite;
}

@keyframes logoBreath {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.logo-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 15px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-green), var(--primary-green-lighter));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.01em;
  line-height: 1;
}

.logo-badge {
  font-family: 'Nunito', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--text-tertiary);
}

.logo-mini {
  width: 44px;
  height: 44px;
}

.logo-mini svg {
  width: 100%;
  height: 100%;
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
  background: var(--border-light);
  border-radius: 2px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border-radius: 12px;
  color: var(--text-secondary);
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
  background: var(--bg-sand);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.nav-item:hover {
  color: var(--primary-green);
}

.nav-item:hover::before {
  opacity: 1;
}

.nav-item.active {
  color: white;
  background: linear-gradient(135deg, var(--nav-color), color-mix(in srgb, var(--nav-color) 85%, black));
  box-shadow: 0 4px 12px rgba(45, 106, 79, 0.15);
}

.nav-item.active .nav-icon-wrapper {
  background: rgba(255, 255, 255, 0.2);
}

.nav-item.active .nav-indicator {
  opacity: 1;
}

.nav-icon-wrapper {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-sand);
  border-radius: 10px;
  flex-shrink: 0;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav-label {
  flex: 1;
  position: relative;
  z-index: 1;
  white-space: nowrap;
  font-family: 'Noto Serif SC', serif;
}

.nav-indicator {
  position: absolute;
  right: 10px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-light);
  position: relative;
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Nunito', sans-serif;
}

.collapse-btn:hover {
  background: rgba(116, 198, 157, 0.1);
  border-color: var(--accent-green);
  color: var(--primary-green);
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

.footer-plant {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0.6;
  animation: plantSway 4s ease-in-out infinite;
}

@keyframes plantSway {
  0%, 100% { transform: translateX(-50%) rotate(-2deg); }
  50% { transform: translateX(-50%) rotate(2deg); }
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
  z-index: 1;
}

/* Top Header */
.top-header {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  background: rgba(250, 250, 249, 0.9);
  backdrop-filter: blur(24px);
  border-bottom: 1px solid var(--border-light);
}

.header-left {
  display: flex;
  align-items: center;
}

.page-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.page-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.01em;
}

.page-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Nunito', sans-serif;
  font-size: 12px;
  color: var(--text-tertiary);
  letter-spacing: 0.02em;
}

.page-breadcrumb svg {
  flex-shrink: 0;
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
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(45, 106, 79, 0.04);
}

.user-profile:hover {
  box-shadow: var(--shadow-soft);
  border-color: var(--accent-green);
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-green-light), var(--primary-green-lighter));
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
  font-family: 'Noto Serif SC', serif;
}

.user-role {
  font-size: 11px;
  color: var(--text-tertiary);
  font-weight: 500;
  font-family: 'Nunito', sans-serif;
}

.logout-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
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
  padding: 28px 32px;
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
  background: var(--border-light);
  border-radius: 4px;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: var(--accent-green);
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
    box-shadow: var(--shadow-hover);
  }

  .sidebar.is-collapsed {
    width: 280px;
    transform: translateX(-100%);
  }

  .leaf-left {
    display: none;
  }

  .main-content {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .top-header {
    padding: 12px 16px;
  }

  .page-title {
    font-size: 18px;
  }

  .user-info {
    display: none;
  }

  .main-content {
    padding: 16px;
  }
}
</style>
