<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <!-- Logo 区域 -->
      <div class="logo-section">
        <div class="logo-wrapper">
          <svg class="logo-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M24 4L4 14V34L24 44L44 34V14L24 4Z" fill="url(#logo-gradient)" />
            <path d="M24 12L12 18V30L24 36L36 30V18L24 12Z" fill="white" fill-opacity="0.3" />
            <circle cx="24" cy="24" r="6" fill="white" />
            <defs>
              <linearGradient id="logo-gradient" x1="4" y1="4" x2="44" y2="44" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#06b6d4" />
                <stop offset="100%" stop-color="#3b82f6" />
              </linearGradient>
            </defs>
          </svg>
          <transition name="logo-text">
            <span v-show="!isCollapsed" class="logo-text">改装件管理</span>
          </transition>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="nav-menu">
        <div
          v-for="item in menuItems"
          :key="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path), 'has-submenu': item.children }"
          @click="handleNavClick(item)"
        >
          <div class="nav-item-content">
            <component :is="item.icon" class="nav-icon" />
            <transition name="nav-text">
              <span v-show="!isCollapsed" class="nav-text">{{ item.title }}</span>
            </transition>
            <transition name="submenu-arrow">
              <el-icon v-if="!isCollapsed && item.children" class="submenu-arrow" :class="{ expanded: expandedMenus.includes(item.path) }">
                <ArrowRight />
              </el-icon>
            </transition>
          </div>

          <!-- 子菜单 -->
          <transition name="submenu">
            <div v-if="item.children && expandedMenus.includes(item.path)" class="submenu">
              <div
                v-for="subItem in item.children"
                :key="subItem.path"
                class="submenu-item"
                :class="{ active: isActive(subItem.path) }"
                @click.stop="handleNavClick(subItem)"
              >
                <span>{{ subItem.title }}</span>
              </div>
            </div>
          </transition>
        </div>
      </nav>

      <!-- 底部折叠按钮 -->
      <div class="sidebar-footer">
        <el-button
          :icon="isCollapsed ? DArrowRight : DArrowLeft"
          circle
          size="small"
          class="collapse-btn"
          @click="toggleCollapse"
        />
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-wrapper" :class="{ collapsed: isCollapsed }">
      <!-- 顶部导航栏 -->
      <header class="top-header">
        <!-- 左侧：面包屑 -->
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">
              <el-icon class="breadcrumb-icon"><HomeFilled /></el-icon>
              <span>首页</span>
            </el-breadcrumb-item>
            <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <!-- 右侧：工具栏 -->
        <div class="header-right">
          <!-- 全局搜索 -->
          <div class="search-wrapper">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索商品、订单、用户..."
              class="search-input"
              clearable
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>

          <!-- 快捷操作 -->
          <div class="quick-actions">
            <el-tooltip content="刷新" placement="bottom">
              <el-button :icon="Refresh" circle size="small" @click="handleRefresh" />
            </el-tooltip>

            <el-tooltip content="全屏" placement="bottom">
              <el-button :icon="FullScreen" circle size="small" @click="handleFullscreen" />
            </el-tooltip>
          </div>

          <!-- 消息通知 -->
          <el-badge :value="unreadCount" :hidden="unreadCount === 0" class="notification-badge">
            <el-button :icon="Bell" circle size="small" @click="handleMessageClick" />
          </el-badge>

          <!-- 分隔线 -->
          <div class="divider"></div>

          <!-- 用户信息 -->
          <el-dropdown @command="handleUserCommand" trigger="click">
            <div class="user-dropdown">
              <el-avatar :size="36" :src="userAvatar" class="user-avatar">
                <el-icon><UserFilled /></el-icon>
              </el-avatar>
              <div class="user-info">
                <div class="user-name">{{ authStore.user?.nickname || '管理员' }}</div>
                <div class="user-role">{{ authStore.user?.is_staff ? '超级管理员' : '管理员' }}</div>
              </div>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="frontend">
                  <el-icon><HomeFilled /></el-icon>
                  返回前台
                </el-dropdown-item>
                <el-dropdown-item divided command="profile">
                  <el-icon><User /></el-icon>
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="main-content">
        <router-view v-slot="{ Component, route }">
          <transition :name="route.meta.transition || 'fade'" mode="out-in">
            <component :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  HomeFilled, Search, Refresh, FullScreen, Bell, UserFilled, ArrowDown,
  User, Setting, SwitchButton, DArrowRight, DArrowLeft, ArrowRight,
  DataLine, Goods, ShoppingCart, User as UserIcon, Ticket, Document,
  Tools, Histogram, Star
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 侧边栏状态
const isCollapsed = ref(false)
const expandedMenus = ref([])

// 搜索
const searchKeyword = ref('')
const unreadCount = ref(3) // 模拟未读消息

// 用户头像
const userAvatar = computed(() => authStore.user?.avatar || '')

// 导航菜单配置
const menuItems = [
  {
    path: '/admin/dashboard',
    title: '数据统计',
    icon: Histogram
  },
  {
    path: '/admin/products',
    title: '商品管理',
    icon: Goods,
    children: [
      { path: '/admin/products', title: '商品列表' },
      { path: '/admin/categories', title: '分类管理' }
    ]
  },
  {
    path: '/admin/orders',
    title: '订单管理',
    icon: ShoppingCart
  },
  {
    path: '/admin/users',
    title: '用户管理',
    icon: UserIcon
  },
  {
    path: '/admin/marketing',
    title: '营销管理',
    icon: Ticket
  },
  {
    path: '/admin/recommendations',
    title: '推荐管理',
    icon: Star
  },
  {
    path: '/admin/content',
    title: '内容管理',
    icon: Document
  },
  {
    path: '/admin/system',
    title: '系统管理',
    icon: Tools,
    children: [
      { path: '/admin/system', title: '系统配置' },
      { path: '/admin/system/messages', title: '消息管理' },
      { path: '/admin/system/logs', title: '操作日志' }
    ]
  }
]

// 面包屑
const breadcrumbs = computed(() => {
  const path = route.path
  const segments = path.split('/').filter(Boolean)

  if (segments.length <= 2) return []

  const routeMap = {
    products: { title: '商品管理' },
    categories: { title: '分类管理' },
    orders: { title: '订单管理' },
    users: { title: '用户管理' },
    marketing: { title: '营销管理' },
    recommendations: { title: '推荐管理' },
    content: { title: '内容管理' },
    system: { title: '系统管理' }
  }

  const result = []
  segments.slice(2).forEach(segment => {
    const info = routeMap[segment]
    if (info) {
      result.push({ title: info.title, path })
    }
  })

  return result
})

// 判断是否激活
const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}

// 处理导航点击
const handleNavClick = (item) => {
  if (item.children) {
    // 切换子菜单展开状态
    const index = expandedMenus.value.indexOf(item.path)
    if (index > -1) {
      expandedMenus.value.splice(index, 1)
    } else {
      expandedMenus.value.push(item.path)
    }
  } else {
    // 跳转到目标页面
    router.push(item.path)
  }
}

// 切换侧边栏折叠
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
  localStorage.setItem('sidebar-collapsed', isCollapsed.value.toString())
}

// 搜索
const handleSearch = () => {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  ElMessage.info('搜索功能开发中...')
}

// 刷新
const handleRefresh = () => {
  location.reload()
}

// 全屏
const handleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

// 消息中心
const handleMessageClick = () => {
  router.push('/admin/system/messages')
}

// 用户操作
const handleUserCommand = async (command) => {
  switch (command) {
    case 'frontend':
      // 返回前台首页
      router.push('/')
      break
    case 'profile':
      router.push('/admin/profile')
      break
    case 'settings':
      router.push('/admin/system/config')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          customClass: 'logout-confirm-dialog'
        })
        authStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } catch {
        // 取消
      }
      break
  }
}

// 初始化
onMounted(() => {
  const collapsed = localStorage.getItem('sidebar-collapsed')
  if (collapsed) {
    isCollapsed.value = collapsed === 'true'
  }

  // 添加窗口大小变化监听
  const handleResize = () => {
    const width = window.innerWidth
    // 在小屏幕上自动折叠侧边栏
    if (width <= 768) {
      isCollapsed.value = true
    }
  }

  // 初始检查
  handleResize()

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)

  // 组件卸载时移除监听
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })
})
</script>

<style scoped>
/* ========================================
   全局样式变量
   ======================================== */
.admin-layout {
  --sidebar-width: 260px;
  --sidebar-collapsed-width: 70px;
  --header-height: 64px;
  --sidebar-bg: #0f172a;
  --sidebar-active-bg: linear-gradient(90deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
  --sidebar-text: #94a3b8;
  --sidebar-text-hover: #e2e8f0;
  --sidebar-border: rgba(148, 163, 184, 0.1);
  --accent-cyan: #06b6d4;
  --accent-blue: #3b82f6;
  --bg-color: #f8fafc;
  --card-bg: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;

  display: flex;
  min-height: 100vh;
  width: 100%;
  background: var(--bg-color);
  overflow-x: hidden;
}

/* ========================================
   侧边栏样式
   ======================================== */
.sidebar {
  position: sticky;
  top: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--sidebar-bg);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  overflow: hidden;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

/* Logo 区域 */
.logo-section {
  padding: 20px;
  border-bottom: 1px solid var(--sidebar-border);
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  filter: drop-shadow(0 0 12px rgba(6, 182, 212, 0.4));
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

/* 导航菜单 */
.nav-menu {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-menu::-webkit-scrollbar {
  width: 4px;
}

.nav-menu::-webkit-scrollbar-track {
  background: transparent;
}

.nav-menu::-webkit-scrollbar-thumb {
  background: var(--sidebar-border);
  border-radius: 2px;
}

.nav-item {
  margin-bottom: 4px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-item-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  color: var(--sidebar-text);
  border-radius: 10px;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.nav-item-content::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, var(--accent-cyan), var(--accent-blue));
  transform: scaleY(0);
  transition: transform 0.2s ease;
}

.nav-item:hover .nav-item-content {
  color: var(--sidebar-text-hover);
  background: rgba(255, 255, 255, 0.05);
}

.nav-item.active .nav-item-content {
  color: #fff;
  background: var(--sidebar-active-bg);
}

.nav-item.active .nav-item-content::before {
  transform: scaleY(1);
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.submenu-arrow {
  margin-left: auto;
  font-size: 14px;
  transition: transform 0.3s ease;
}

.submenu-arrow.expanded {
  transform: rotate(90deg);
}

/* 子菜单 */
.submenu {
  padding-left: 44px;
  margin-top: 4px;
}

.submenu-item {
  padding: 8px 12px;
  font-size: 13px;
  color: var(--sidebar-text);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submenu-item:hover {
  color: var(--sidebar-text-hover);
  background: rgba(255, 255, 255, 0.05);
}

.submenu-item.active {
  color: var(--accent-cyan);
  background: rgba(6, 182, 212, 0.1);
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--sidebar-border);
  display: flex;
  justify-content: center;
}

.collapse-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--sidebar-border);
  color: var(--sidebar-text);
  transition: all 0.2s ease;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-color: var(--accent-cyan);
}

/* ========================================
   主内容区域
   ======================================== */
.main-wrapper {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  width: calc(100% - var(--sidebar-width));
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-wrapper.collapsed {
  width: calc(100% - var(--sidebar-collapsed-width));
}

/* ========================================
   顶部导航栏
   ======================================== */
.top-header {
  height: var(--header-height);
  background: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: relative;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.9);
  flex-shrink: 0;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 面包屑 */
:deep(.el-breadcrumb) {
  font-size: 14px;
}

:deep(.el-breadcrumb__item) {
  font-size: 14px;
}

:deep(.el-breadcrumb__inner) {
  color: var(--text-secondary);
  font-weight: 500;
}

:deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: var(--text-primary);
}

.breadcrumb-icon {
  margin-right: 4px;
  font-size: 16px;
}

/* 搜索框 */
.search-wrapper {
  width: 280px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  background: var(--bg-color);
  border: 1px solid var(--border-color);
  box-shadow: none;
  transition: all 0.2s ease;
}

.search-input :deep(.el-input__wrapper:hover) {
  border-color: var(--accent-cyan);
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
}

.search-input :deep(.el-input__inner) {
  font-size: 13px;
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  gap: 8px;
}

.quick-actions .el-button {
  background: var(--bg-color);
  border-color: var(--border-color);
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.quick-actions .el-button:hover {
  color: var(--accent-cyan);
  border-color: var(--accent-cyan);
  background: rgba(6, 182, 212, 0.05);
}

/* 消息通知 */
.notification-badge {
  display: inline-flex;
}

.notification-badge .el-button {
  background: var(--bg-color);
  border-color: var(--border-color);
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.notification-badge .el-button:hover {
  color: var(--accent-cyan);
  border-color: var(--accent-cyan);
  background: rgba(6, 182, 212, 0.05);
}

/* 分隔线 */
.divider {
  width: 1px;
  height: 24px;
  background: var(--border-color);
  margin: 0 4px;
}

/* 用户下拉菜单 */
.user-dropdown {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px 6px 6px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-dropdown:hover {
  background: var(--bg-color);
}

.user-avatar {
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.3);
}

.user-info {
  text-align: left;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.user-role {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.dropdown-icon {
  font-size: 14px;
  color: var(--text-secondary);
  transition: transform 0.2s ease;
}

.user-dropdown:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* ========================================
   主内容区
   ======================================== */
.main-content {
  flex: 1;
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
}

/* ========================================
   过渡动画
   ======================================== */
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

.logo-text-enter-active,
.logo-text-leave-active {
  transition: all 0.2s ease;
}

.logo-text-enter-from,
.logo-text-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

.nav-text-enter-active,
.nav-text-leave-active {
  transition: all 0.2s ease;
}

.nav-text-enter-from,
.nav-text-leave-to {
  opacity: 0;
  width: 0;
}

.submenu-arrow-enter-active,
.submenu-arrow-leave-active {
  transition: all 0.2s ease;
}

.submenu-enter-active,
.submenu-leave-active {
  transition: all 0.3s ease;
  transform-origin: top;
}

.submenu-enter-from,
.submenu-leave-to {
  opacity: 0;
  transform: scaleY(0.8);
}

/* ========================================
   响应式设计
   ======================================== */
@media (max-width: 1200px) {
  .search-wrapper {
    width: 220px;
  }

  .header-left {
    flex: 0 1 auto;
  }
}

@media (max-width: 1024px) {
  .search-wrapper {
    width: 180px;
  }

  .user-info {
    display: none;
  }

  .main-content {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .admin-layout {
    flex-direction: column;
  }

  .sidebar {
    position: fixed;
    width: var(--sidebar-width);
    height: 100vh;
    z-index: 1001;
  }

  .sidebar.collapsed {
    width: 0;
    transform: translateX(-100%);
  }

  .main-wrapper {
    width: 100%;
  }

  .main-wrapper.collapsed {
    width: 100%;
  }

  .top-header {
    padding: 0 16px;
  }

  .search-wrapper {
    display: none;
  }

  .quick-actions {
    display: none;
  }

  .main-content {
    padding: 16px;
  }

  /* Add mobile overlay when sidebar is open */
  .sidebar:not(.collapsed)::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: -1;
  }
}
</style>
