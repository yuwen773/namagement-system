<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAppStore } from '@/stores/app'
import {
  Expand,
  Fold,
  ArrowDown,
  User,
  SwitchButton,
  Odometer,
  VideoCamera,
  CollectionTag,
  Location,
  Grid,
  Money,
  DataAnalysis,
  Setting,
  Bell,
  Tickets,
  Histogram,
  PictureRounded,
  Operation,
  Moon,
  Sunny
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

// 当前时间
const currentTime = ref('')
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

let timer = null
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// 菜单数据 - 增强版
const menuGroups = [
  {
    title: '数据中心',
    items: [
      { path: '/admin/dashboard', name: '系统概览', icon: Odometer, color: 'from-blue-500 to-cyan-500' },
      { path: '/admin/prediction', name: '预测分析', icon: DataAnalysis, color: 'from-purple-500 to-pink-500' }
    ]
  },
  {
    title: '基础数据',
    items: [
      { path: '/admin/movies', name: '影片管理', icon: VideoCamera, color: 'from-rose-500 to-orange-500' },
      { path: '/admin/movie-types', name: '影片类型', icon: CollectionTag, color: 'from-amber-500 to-yellow-500' },
      { path: '/admin/cinemas', name: '影院管理', icon: Location, color: 'from-emerald-500 to-teal-500' },
      { path: '/admin/regions', name: '地域管理', icon: Grid, color: 'from-indigo-500 to-violet-500' }
    ]
  },
  {
    title: '业务数据',
    items: [
      { path: '/admin/boxoffice', name: '票房数据', icon: Money, color: 'from-green-500 to-emerald-500' }
    ]
  },
  {
    title: '系统管理',
    items: [
      { path: '/admin/users', name: '用户管理', icon: User, color: 'from-slate-500 to-gray-500' }
    ]
  }
]

// 当前激活菜单
const activeMenu = computed(() => route.path)

// 菜单项悬停状态
const hoveredMenu = ref(null)

// 用户下拉菜单状态
const userDropdownVisible = ref(false)

// 退出登录
const handleLogout = async () => {
  userDropdownVisible.value = false
  await userStore.doLogout()
  router.push('/login')
}

// 路由跳转
const navigateTo = (path) => {
  router.push(path)
}
</script>

<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside
      class="sidebar"
      :class="{ collapsed: appStore.sidebarCollapsed }"
    >
      <!-- 背景装饰 -->
      <div class="sidebar-bg">
        <div class="grid-pattern"></div>
        <div class="gradient-mesh">
          <div class="mesh-orb mesh-orb-1"></div>
          <div class="mesh-orb mesh-orb-2"></div>
          <div class="mesh-orb mesh-orb-3"></div>
        </div>
      </div>

      <!-- Logo 区域 -->
      <div class="sidebar-header">
        <div class="logo-container">
          <div class="logo-icon">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="4" y="8" width="40" height="32" rx="4" fill="currentColor" opacity="0.2"/>
              <rect x="4" y="8" width="40" height="32" rx="4" stroke="currentColor" stroke-width="2"/>
              <path d="M16 18L24 14L32 18V30L24 34L16 30V18Z" fill="currentColor"/>
              <circle cx="24" cy="24" r="4" fill="#10b981"/>
            </svg>
          </div>
          <transition name="logo-text">
            <div v-if="!appStore.sidebarCollapsed" class="logo-text">
              <h1 class="logo-title">票房预测</h1>
              <p class="logo-subtitle">Admin Console</p>
            </div>
          </transition>
        </div>
      </div>

      <!-- 菜单区域 -->
      <div class="sidebar-menu">
        <div
          v-for="group in menuGroups"
          :key="group.title"
          class="menu-group"
        >
          <transition name="group-title">
            <div v-if="!appStore.sidebarCollapsed" class="menu-group-title">
              {{ group.title }}
            </div>
          </transition>
          <nav class="menu-nav">
            <div
              v-for="item in group.items"
              :key="item.path"
              class="menu-item"
              :class="{ active: activeMenu === item.path }"
              @click="navigateTo(item.path)"
              @mouseenter="hoveredMenu = item.path"
              @mouseleave="hoveredMenu = null"
            >
              <div class="menu-item-bg" :class="`${item.color}`"></div>
              <div class="menu-item-content">
                <div class="menu-icon-wrapper" :class="`${item.color}`">
                  <component :is="item.icon" class="menu-icon" />
                </div>
                <transition name="menu-text">
                  <span v-if="!appStore.sidebarCollapsed" class="menu-text">{{ item.name }}</span>
                </transition>
              </div>
              <div v-if="activeMenu === item.path" class="active-indicator"></div>
            </div>
          </nav>
        </div>
      </div>

      <!-- 侧边栏底部 -->
      <div class="sidebar-footer">
        <transition name="footer-content">
          <div v-if="!appStore.sidebarCollapsed" class="footer-content">
            <div class="time-display">
              <div class="time-value">{{ currentTime }}</div>
              <div class="time-label">{{ new Date().toLocaleDateString('zh-CN', { weekday: 'long', month: 'short', day: 'numeric' }) }}</div>
            </div>
          </div>
        </transition>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 顶部栏 -->
      <header class="header">
        <!-- 左侧：折叠按钮 + 面包屑 -->
        <div class="header-left">
          <button
            class="collapse-btn"
            @click="appStore.toggleSidebar"
            :title="appStore.sidebarCollapsed ? '展开侧边栏' : '收起侧边栏'"
          >
            <component :is="appStore.sidebarCollapsed ? Expand : Fold" class="collapse-icon" />
            <div class="collapse-btn-bg"></div>
          </button>

          <div class="breadcrumb">
            <div class="breadcrumb-item">
              <svg class="breadcrumb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <polyline points="9 22 9 12 15 12 15 22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>管理控制台</span>
            </div>
            <svg class="breadcrumb-separator" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <polyline points="9 18 15 12 9 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="breadcrumb-item current">{{ route.meta.title || '未知页面' }}</div>
          </div>
        </div>

        <!-- 右侧：工具栏 + 用户信息 -->
        <div class="header-right">
          <!-- 系统状态指示器 -->
          <div class="status-indicators">
            <div class="status-dot status-online"></div>
            <span class="status-text">系统正常</span>
          </div>

          <!-- 分隔线 -->
          <div class="header-divider"></div>

          <!-- 用户下拉菜单 -->
          <div class="user-section" @click="userDropdownVisible = !userDropdownVisible">
            <div class="user-avatar">
              <div class="avatar-bg" :class="userDropdownVisible ? 'avatar-active' : ''">
                <span class="avatar-text">{{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'A' }}</span>
              </div>
              <div class="avatar-ring" :class="{ active: userDropdownVisible }"></div>
            </div>
            <div class="user-info">
              <span class="user-name">{{ userStore.user?.real_name || userStore.user?.username || '管理员' }}</span>
              <span class="user-role">系统管理员</span>
            </div>
            <component :is="ArrowDown" class="dropdown-arrow" :class="{ rotate: userDropdownVisible }" />

            <!-- 下拉菜单 -->
            <transition name="dropdown">
              <div v-if="userDropdownVisible" class="user-dropdown" @click.stop>
                <div class="dropdown-header">
                  <div class="dropdown-avatar">{{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'A' }}</div>
                  <div class="dropdown-user-info">
                    <div class="dropdown-user-name">{{ userStore.user?.real_name || userStore.user?.username || '管理员' }}</div>
                    <div class="dropdown-user-email">{{ userStore.user?.email || 'admin@example.com' }}</div>
                  </div>
                </div>
                <div class="dropdown-divider"></div>
                <button class="dropdown-item" @click="router.push('/user/profile')">
                  <User class="dropdown-item-icon" />
                  <span>个人中心</span>
                </button>
                <button class="dropdown-item danger" @click="handleLogout">
                  <SwitchButton class="dropdown-item-icon" />
                  <span>退出登录</span>
                </button>
              </div>
            </transition>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="page-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
/* ========== 全局布局 ========== */
.admin-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
  position: relative;
}

/* ========== 侧边栏样式 ========== */
.sidebar {
  width: 280px;
  height: 100%;
  flex-shrink: 0;
  position: relative;
  display: flex;
  flex-direction: column;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.sidebar.collapsed {
  width: 72px;
}

/* 侧边栏背景 */
.sidebar-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(ellipse at left, black 30%, transparent 80%);
}

.gradient-mesh {
  position: absolute;
  inset: 0;
}

.mesh-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.15;
  animation: meshFloat 15s ease-in-out infinite;
}

.mesh-orb-1 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  top: 20%;
  left: -50px;
  animation-delay: 0s;
}

.mesh-orb-2 {
  width: 180px;
  height: 180px;
  background: linear-gradient(135deg, #059669, #0d9488);
  bottom: 30%;
  right: -40px;
  animation-delay: -5s;
}

.mesh-orb-3 {
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, #14b8a6, #0ea5e9);
  top: 60%;
  left: 50%;
  animation-delay: -10s;
}

@keyframes meshFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(10px, -15px) scale(1.1); }
  50% { transform: translate(-5px, 10px) scale(0.95); }
  75% { transform: translate(-10px, -5px) scale(1.05); }
}

/* Logo 区域 */
.sidebar-header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  position: relative;
  z-index: 1;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  color: #10b981;
  flex-shrink: 0;
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-title {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
}

/* Logo 文本过渡动画 */
.logo-text-enter-active,
.logo-text-leave-active {
  transition: all 0.3s ease;
}

.logo-text-enter-from,
.logo-text-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* 菜单区域 */
.sidebar-menu {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px 12px;
  position: relative;
  z-index: 1;
}

.sidebar-menu::-webkit-scrollbar {
  width: 4px;
}

.sidebar-menu::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-menu::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.menu-group {
  margin-bottom: 24px;
}

.menu-group:last-child {
  margin-bottom: 0;
}

.menu-group-title {
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.35);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  padding: 0 12px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.group-title-enter-active,
.group-title-leave-active {
  transition: all 0.3s ease;
}

.group-title-enter-from,
.group-title-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

.menu-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  position: relative;
  height: 48px;
  display: flex;
  align-items: center;
  cursor: pointer;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-item-bg {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.menu-item:hover .menu-item-bg {
  opacity: 0.15;
}

.menu-item.active .menu-item-bg {
  opacity: 0.2;
}

.menu-item-content {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 12px;
  width: 100%;
  z-index: 1;
}

.menu-icon-wrapper {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}

.menu-icon-wrapper::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, currentColor 0%, transparent 100%);
  opacity: 0.3;
}

.menu-icon {
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.7);
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.menu-item:hover .menu-icon {
  color: #fff;
  transform: scale(1.1);
}

.menu-item.active .menu-icon-wrapper {
  background: linear-gradient(135deg, #10b981, #14b8a6);
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.menu-item.active .menu-icon {
  color: #fff;
}

.menu-text {
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  white-space: nowrap;
  transition: all 0.3s ease;
}

.menu-item:hover .menu-text {
  color: #fff;
}

.menu-item.active .menu-text {
  color: #fff;
  font-weight: 600;
}

.menu-text-enter-active,
.menu-text-leave-active {
  transition: all 0.3s ease;
}

.menu-text-enter-from,
.menu-text-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.active-indicator {
  position: absolute;
  right: 12px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 16px 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  position: relative;
  z-index: 1;
}

.footer-content-enter-active,
.footer-content-leave-active {
  transition: all 0.3s ease;
}

.footer-content-enter-from,
.footer-content-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.time-display {
  text-align: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.time-value {
  font-size: 18px;
  font-weight: 700;
  color: #10b981;
  font-family: 'SF Mono', 'Consolas', monospace;
  letter-spacing: 2px;
}

.time-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 4px;
}

/* ========== 主内容区 ========== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* 主内容背景 */
.main-content::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at top right, rgba(16, 185, 129, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse at bottom left, rgba(20, 184, 166, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

/* ========== 顶部栏样式 ========== */
.header {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  z-index: 10;
}

/* 左侧区域 */
.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 折叠按钮 */
.collapse-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.collapse-btn:hover {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.3);
}

.collapse-btn:hover .collapse-icon {
  color: #10b981;
  transform: scale(1.1);
}

.collapse-btn-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.collapse-btn:hover .collapse-btn-bg {
  opacity: 1;
}

.collapse-icon {
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

/* 面包屑 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}

.breadcrumb-icon {
  width: 16px;
  height: 16px;
  opacity: 0.5;
}

.breadcrumb-separator {
  width: 14px;
  height: 14px;
  color: rgba(255, 255, 255, 0.2);
}

.breadcrumb-item.current {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

/* 右侧区域 */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 状态指示器 */
.status-indicators {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 20px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: statusPulse 2s ease-in-out infinite;
}

.status-online {
  background: #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

@keyframes statusPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-size: 12px;
  color: #10b981;
  font-weight: 500;
}

/* 分隔线 */
.header-divider {
  width: 1px;
  height: 32px;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.1), transparent);
}

/* 用户区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.user-section:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.15);
}

.user-avatar {
  position: relative;
}

.avatar-bg {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.avatar-bg.avatar-active {
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.avatar-text {
  font-size: 14px;
  font-weight: 700;
  color: #fff;
}

.avatar-ring {
  position: absolute;
  inset: -3px;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.avatar-ring.active {
  border-color: #10b981;
  animation: ringPulse 2s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.3); }
  50% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.user-role {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.4);
}

.dropdown-arrow {
  width: 16px;
  height: 16px;
  color: rgba(255, 255, 255, 0.4);
  transition: transform 0.3s ease;
}

.dropdown-arrow.rotate {
  transform: rotate(180deg);
}

/* 用户下拉菜单 */
.user-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 240px;
  background: rgba(30, 41, 59, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  z-index: 100;
}

.dropdown-enter-active {
  animation: dropdownSlide 0.3s ease-out;
}

.dropdown-leave-active {
  animation: dropdownSlide 0.2s ease-in reverse;
}

@keyframes dropdownSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.dropdown-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #10b981, #14b8a6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
}

.dropdown-user-info {
  flex: 1;
}

.dropdown-user-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.dropdown-user-email {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 2px;
}

.dropdown-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.dropdown-item.danger:hover {
  background: rgba(239, 68, 68, 0.1);
}

.dropdown-item-icon {
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.5);
}

.dropdown-item span {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.dropdown-item.danger:hover .dropdown-item-icon,
.dropdown-item.danger:hover span {
  color: #ef4444;
}

/* ========== 页面内容 ========== */
.page-content {
  flex: 1;
  overflow: auto;
  position: relative;
}

.page-content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.page-content::-webkit-scrollbar-track {
  background: transparent;
}

.page-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.page-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1000;
    transform: translateX(-100%);
  }

  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }

  .sidebar.collapsed {
    width: 280px;
    transform: translateX(-100%);
  }

  .header {
    padding: 0 16px;
  }

  .breadcrumb {
    display: none;
  }
}
</style>
