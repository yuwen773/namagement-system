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
    title: '数据概览'
  },
  {
    path: '/admin/statistics',
    icon: Histogram,
    title: '数据分析'
  },
  {
    path: '/admin/crawler',
    icon: TrendCharts,
    title: '数据采集'
  },
  {
    path: '/admin/crawler/config',
    icon: Setting,
    title: '爬虫配置'
  },
  {
    path: '/admin/products',
    icon: ShoppingCart,
    title: '商品管理'
  },
  {
    path: '/admin/users',
    icon: User,
    title: '用户管理'
  },
  {
    path: '/admin/announcements',
    icon: Bell,
    title: '公告管理'
  }
])

const activeMenu = computed(() => route.path)

const isActive = (path) => {
  // 精确匹配当前路径
  if (activeMenu.value === path) return true

  // 检查当前路径是否以该菜单项路径开头（用于子路由高亮）
  // 只有当没有其他更具体的菜单项匹配时才高亮父菜单
  if (activeMenu.value.startsWith(path + '/')) {
    // 检查是否有更具体的菜单项匹配
    const hasMoreSpecificMatch = menuItems.value.some(item => {
      if (item.path === path) return false // 排除自己
      // 更具体的路径：比当前路径更长且能匹配活动路径
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
    <!-- 侧边栏 -->
    <aside :class="['sidebar', { collapsed: isCollapsed }]">
      <div class="sidebar-header">
        <transition name="logo-fade">
          <div v-if="!isCollapsed" class="logo-full">
            <div class="logo-icon-mini">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="48" height="48" rx="12" fill="url(#admin-logo-gradient)"/>
                <path d="M24 12L32 20L24 28L16 20L24 12Z" fill="white"/>
                <path d="M20 28L24 32L28 28" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="24" cy="20" r="3" fill="#FF6B35"/>
                <defs>
                  <linearGradient id="admin-logo-gradient" x1="0" y1="0" x2="48" y2="48">
                    <stop offset="0%" stop-color="#FF6B35"/>
                    <stop offset="100%" stop-color="#7B2CBF"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <span class="logo-text">宠物用品数据</span>
          </div>
        </transition>
        <transition name="logo-fade">
          <div v-if="isCollapsed" class="logo-mini">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="12" fill="url(#admin-logo-gradient-mini)"/>
              <path d="M24 12L32 20L24 28L16 20L24 12Z" fill="white"/>
              <path d="M20 28L24 32L28 28" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="24" cy="20" r="3" fill="#FF6B35"/>
              <defs>
                <linearGradient id="admin-logo-gradient-mini" x1="0" y1="0" x2="48" y2="48">
                  <stop offset="0%" stop-color="#FF6B35"/>
                  <stop offset="100%" stop-color="#7B2CBF"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
        </transition>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <component :is="item.icon" class="nav-icon" />
          <transition name="text-fade">
            <span v-if="!isCollapsed" class="nav-text">{{ item.title }}</span>
          </transition>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button class="collapse-btn" @click="toggleCollapse">
          <component :is="isCollapsed ? Expand : Fold" class="icon" />
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-wrapper">
      <!-- 顶部导航栏 -->
      <header class="top-header">
        <div class="header-left">
          <h1 class="page-title">{{ route.meta.title || '管理控制台' }}</h1>
        </div>

        <div class="header-right">
          <div class="user-info">
            <div class="user-avatar">
              <component :is="User" class="avatar-icon" />
            </div>
            <div class="user-details">
              <span class="user-name">{{ userStore.userInfo.username || 'Admin' }}</span>
              <span class="user-role">管理员</span>
            </div>
          </div>

          <el-dropdown @command="handleLogout">
            <button class="logout-btn">
              <SwitchButton class="logout-icon" />
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- 内容区 -->
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
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

.admin-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: #0f0f1a;
  font-family: 'Nunito', -apple-system, sans-serif;
}

/* 侧边栏 */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #1a1a2e 0%, #16162a 100%);
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 100;
}

.sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo-full {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon-mini {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.logo-icon-mini svg,
.logo-mini svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  font-size: 18px;
  font-weight: 800;
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-mini {
  width: 36px;
  height: 36px;
}

/* 导航 */
.sidebar-nav {
  flex: 1;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
  scrollbar-width: none; /* Firefox */
}

.sidebar-nav::-webkit-scrollbar {
  display: none; /* Chrome/Safari/Webkit */
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.1), rgba(123, 44, 191, 0.1));
  opacity: 0;
  transition: opacity 0.2s ease;
}

.nav-item:hover {
  color: rgba(255, 255, 255, 0.8);
  background: rgba(255, 255, 255, 0.03);
}

.nav-item.active {
  color: #FF6B35;
  background: rgba(255, 107, 53, 0.1);
}

.nav-item.active::before {
  opacity: 1;
}

.nav-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.nav-text {
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.collapse-btn {
  width: 100%;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.2s ease;
}

.collapse-btn:hover {
  background: rgba(255, 107, 53, 0.1);
  color: #FF6B35;
  border-color: rgba(255, 107, 53, 0.3);
}

.collapse-btn .icon {
  width: 20px;
  height: 20px;
}

/* 主内容区 */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-header {
  height: 72px;
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #FF6B35, #7B2CBF);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-icon {
  width: 22px;
  height: 22px;
  color: white;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-size: 14px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
}

.logout-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(255, 59, 48, 0.1);
  color: #ff6b6b;
  border-color: rgba(255, 59, 48, 0.3);
}

.logout-icon {
  width: 20px;
  height: 20px;
}

/* 主内容 */
.main-content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

/* 动画 */
.logo-fade-enter-active,
.logo-fade-leave-active {
  transition: all 0.2s ease;
}

.logo-fade-enter-from,
.logo-fade-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.text-fade-enter-active,
.text-fade-leave-active {
  transition: all 0.2s ease;
}

.text-fade-enter-from,
.text-fade-leave-to {
  opacity: 0;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.3s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
