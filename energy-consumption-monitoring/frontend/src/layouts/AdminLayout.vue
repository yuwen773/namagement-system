<template>
  <div class="admin-layout">
    <!-- Mobile Sidebar Overlay -->
    <div
      v-if="isMobile && isSidebarOpen"
      class="sidebar-overlay"
      @click="closeSidebar"
    ></div>

    <!-- Sidebar -->
    <aside
      class="sidebar"
      :class="{
        'sidebar-collapsed': isCollapsed && !isMobile,
        'sidebar-mobile': isMobile,
        'sidebar-open': isMobile && isSidebarOpen
      }"
    >
      <!-- Logo Section -->
      <div class="sidebar-header">
        <div class="logo-wrapper">
          <div class="logo-icon">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M24 4L6 14V30C6 35.5225 10.4772 40 16 40H32C37.5228 40 42 35.5225 42 30V14L24 4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M18 24L22 28L30 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="24" cy="18" r="4" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <transition name="logo-text">
            <div v-show="(!isCollapsed && !isMobile) || (isMobile && isSidebarOpen)" class="logo-text">
              <span class="logo-title">能耗监测</span>
              <span class="logo-subtitle">Energy Monitor</span>
            </div>
          </transition>
        </div>
        <!-- Collapse Button -->
        <button class="collapse-btn" @click="toggleSidebar">
          <el-icon :size="18">
            <icon-ep-fold v-if="!isCollapsed" />
            <icon-ep-expand v-else />
          </el-icon>
        </button>
      </div>

      <!-- Navigation Menu -->
      <nav class="sidebar-nav">
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapsed"
          :collapse-transition="true"
          router
          class="sidebar-menu"
        >
          <el-menu-item index="/admin/dashboard">
            <el-icon><icon-ep-monitor /></el-icon>
            <template #title>综合监控</template>
          </el-menu-item>

          <el-menu-item index="/admin/monitoring">
            <el-icon><icon-ep-data-analysis /></el-icon>
            <template #title>监测中心</template>
          </el-menu-item>

          <el-menu-item index="/admin/analysis">
            <el-icon><icon-ep-trend-charts /></el-icon>
            <template #title>统计分析</template>
          </el-menu-item>

          <el-menu-item index="/admin/alarms">
            <el-icon>
              <icon-ep-warning />
              <el-badge v-if="alarmCount > 0" :value="alarmCount" class="alarm-badge" />
            </el-icon>
            <template #title>异常告警</template>
          </el-menu-item>

          <el-menu-item index="/admin/devices">
            <el-icon><icon-ep-cpu /></el-icon>
            <template #title>设备管理</template>
          </el-menu-item>

          <el-menu-item index="/admin/configuration">
            <el-icon><icon-ep-setting /></el-icon>
            <template #title>基础配置</template>
          </el-menu-item>

          <el-menu-item index="/admin/system">
            <el-icon><icon-ep-tools /></el-icon>
            <template #title>系统管理</template>
          </el-menu-item>
        </el-menu>
      </nav>

      <!-- Sidebar Footer -->
      <div v-show="(!isCollapsed && !isMobile) || (isMobile && isSidebarOpen)" class="sidebar-footer">
        <div class="system-status">
          <div class="status-dot status-online"></div>
          <span class="status-text">系统运行正常</span>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="main-wrapper">
      <!-- Top Header -->
      <header class="top-header">
        <!-- Left: Mobile Menu Toggle + Breadcrumb -->
        <div class="header-left">
          <!-- Mobile Menu Toggle Button -->
          <button class="mobile-menu-btn" @click="toggleMobileSidebar">
            <el-icon :size="20">
              <icon-ep-fold v-if="isSidebarOpen" />
              <icon-ep-expand v-else />
            </el-icon>
          </button>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin' }">
              <el-icon><icon-ep-house /></el-icon>
              <span>首页</span>
            </el-breadcrumb-item>
            <el-breadcrumb-item v-for="item in breadcrumbItems" :key="item.path" :to="{ path: item.path }">
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <!-- Right: Actions & User Menu -->
        <div class="header-right">
          <!-- Notifications -->
          <el-badge :value="notificationCount" :hidden="notificationCount === 0" class="notification-badge">
            <el-button class="header-btn" @click="showNotifications = true">
              <el-icon :size="20"><icon-ep-bell /></el-icon>
            </el-button>
          </el-badge>

          <!-- Quick Actions -->
          <el-dropdown trigger="click" class="action-dropdown">
            <el-button class="header-btn">
              <el-icon :size="20"><icon-ep-plus /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleQuickAction('device')">
                  <el-icon><icon-ep-cpu /></el-icon>
                  <span>添加设备</span>
                </el-dropdown-item>
                <el-dropdown-item @click="handleQuickAction('alarm')">
                  <el-icon><icon-ep-warning /></el-icon>
                  <span>告警规则</span>
                </el-dropdown-item>
                <el-dropdown-item @click="handleQuickAction('report')">
                  <el-icon><icon-ep-document /></el-icon>
                  <span>生成报告</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <!-- User Dropdown -->
          <el-dropdown trigger="click" class="user-dropdown" @command="handleUserCommand">
            <div class="user-trigger">
              <div class="user-avatar">
                <el-icon :size="24"><icon-ep-user /></el-icon>
              </div>
              <div class="user-info">
                <span class="user-name">{{ displayName }}</span>
                <span class="user-role">{{ roleLabel }}</span>
              </div>
              <el-icon class="dropdown-arrow"><icon-ep-arrow-down /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><icon-ep-user /></el-icon>
                  <span>个人中心</span>
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><icon-ep-setting /></el-icon>
                  <span>系统设置</span>
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><icon-ep-switch-button /></el-icon>
                  <span>退出登录</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- Page Content -->
      <main class="page-content">
        <!-- Page Title Bar -->
        <div v-if="currentPageTitle" class="page-title-bar">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
          <div class="page-actions">
            <slot name="page-actions"></slot>
          </div>
        </div>

        <!-- Router View -->
        <div class="content-wrapper">
          <router-view v-slot="{ Component }">
            <transition name="page-fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>

    <!-- Notifications Drawer -->
    <el-drawer v-model="showNotifications" title="通知中心" size="380px">
      <div class="notifications-list">
        <div v-for="notification in notifications" :key="notification.id" class="notification-item" :class="{ 'is-unread': !notification.read }">
          <div class="notification-icon" :class="`type-${notification.type}`">
            <el-icon>
              <icon-ep-warning v-if="notification.type === 'warning'" />
              <icon-ep-success-filled v-else-if="notification.type === 'success'" />
              <icon-ep-info-filled v-else />
            </el-icon>
          </div>
          <div class="notification-content">
            <h4>{{ notification.title }}</h4>
            <p>{{ notification.message }}</p>
            <span class="notification-time">{{ notification.time }}</span>
          </div>
        </div>
        <el-empty v-if="notifications.length === 0" description="暂无通知" />
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// Sidebar state
const isCollapsed = ref(false)
const isMobile = ref(false)
const isSidebarOpen = ref(false)

// UI state
const showNotifications = ref(false)
const alarmCount = ref(0) // TODO: 从告警API获取待处理告警数量
const notificationCount = ref(0) // TODO: 从通知API获取未读通知数量

// Notifications - 从API获取通知列表 (待实现)
const notifications = ref([])

// Load notification counts (待实现API)
async function loadNotificationCounts() {
  try {
    // TODO: 调用API获取告警和通知数量
    // const alarmResponse = await getAlarmStatistics()
    // if (alarmResponse.code === 0) {
    //   alarmCount.value = alarmResponse.data.pending || 0
    // }
  } catch (error) {
    console.error('Failed to load notification counts:', error)
  }
}

// Computed properties
const activeMenu = computed(() => route.path)

const currentPageTitle = computed(() => {
  const titles = {
    'AdminDashboard': '综合监控大屏',
    'Monitoring': '监测中心',
    'Analysis': '统计分析报表',
    'Alarms': '异常告警管理',
    'Devices': '设备资产管理',
    'Configuration': '基础档案配置',
    'System': '系统管理',
  }
  return titles[route.name] || ''
})

const breadcrumbItems = computed(() => {
  const items = {
    'AdminDashboard': [{ title: '综合监控', path: '/admin/dashboard' }],
    'Monitoring': [{ title: '监测中心', path: '/admin/monitoring' }],
    'Analysis': [{ title: '统计分析', path: '/admin/analysis' }],
    'Alarms': [{ title: '异常告警', path: '/admin/alarms' }],
    'Devices': [{ title: '设备管理', path: '/admin/devices' }],
    'Configuration': [{ title: '基础配置', path: '/admin/configuration' }],
    'System': [{ title: '系统管理', path: '/admin/system' }],
  }
  return items[route.name] || []
})

const displayName = computed(() => {
  return userStore.userInfo?.real_name || userStore.userInfo?.username || 'Admin'
})

const roleLabel = computed(() => {
  const roleMap = {
    'ADMIN': '系统管理员',
    'USER': '普通用户',
  }
  return roleMap[userStore.role] || '未知'
})

// Methods
function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
  // Save preference
  localStorage.setItem('sidebarCollapsed', String(isCollapsed.value))
}

function toggleMobileSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value
}

function closeSidebar() {
  isSidebarOpen.value = false
}

function checkMobile() {
  isMobile.value = window.innerWidth < 1024
  // Close mobile sidebar when switching to desktop
  if (!isMobile.value) {
    isSidebarOpen.value = false
  }
}

function handleUserCommand(command) {
  switch (command) {
    case 'profile':
      router.push('/user/profile')
      break
    case 'settings':
      ElMessage.info('系统设置功能开发中')
      break
    case 'logout':
      handleLogout()
      break
  }
}

function handleQuickAction(type) {
  const actions = {
    device: () => router.push('/admin/devices'),
    alarm: () => router.push('/admin/alarms'),
    report: () => ElMessage.info('报告生成功能开发中'),
  }
  actions[type]?.()
}

async function handleLogout() {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '退出确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // User cancelled
  }
}

// Lifecycle
onMounted(() => {
  // Load notification counts
  loadNotificationCounts()

  // Restore sidebar state
  const savedState = localStorage.getItem('sidebarCollapsed')
  if (savedState !== null) {
    isCollapsed.value = savedState === 'true'
  }

  // Check mobile status
  checkMobile()

  // Handle responsive sidebar
  const handleResize = () => {
    checkMobile()
    // Auto collapse on desktop if window gets smaller
    if (window.innerWidth < 1024 && !isMobile.value) {
      isCollapsed.value = true
    }
  }

  window.addEventListener('resize', handleResize)

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

.admin-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  font-family: 'Poppins', 'Noto Sans SC', sans-serif;
}

/* ========================================
   SIDEBAR STYLES
   ======================================== */
.sidebar {
  position: relative;
  z-index: 100;
  display: flex;
  flex-direction: column;
  width: 260px;
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);
}

.sidebar-collapsed {
  width: 64px;
}

/* Sidebar Header */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  overflow: hidden;
}

.logo-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 10px;
  color: white;
}

.logo-icon svg {
  width: 24px;
  height: 24px;
}

.logo-text {
  display: flex;
  flex-direction: column;
  white-space: nowrap;
}

.logo-title {
  font-size: 16px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
  color: #fff;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 10px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
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

.collapse-btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
}

.collapse-btn:hover {
  background: rgba(249, 115, 22, 0.2);
  color: #f97316;
}

/* Sidebar Navigation */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
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
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

.sidebar-menu {
  border: none;
  background: transparent;
}

.sidebar-menu :deep(.el-menu-item) {
  display: flex;
  align-items: center;
  height: 48px;
  margin-bottom: 4px;
  padding: 0 16px;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
}

.sidebar-menu :deep(.el-menu-item):hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #fff;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
  font-size: 20px;
  margin-right: 12px;
}

.alarm-badge {
  position: absolute;
  top: -5px;
  right: -5px;
}

.sidebar-menu :deep(.el-menu-item .el-badge) {
  position: relative;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.system-status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.status-online {
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

/* ========================================
   MAIN WRAPPER
   ======================================== */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f8fafc;
}

/* ========================================
   TOP HEADER
   ======================================== */
.top-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-left :deep(.el-breadcrumb) {
  font-size: 14px;
}

.header-left :deep(.el-breadcrumb__item) {
  display: flex;
  align-items: center;
}

.header-left :deep(.el-breadcrumb__inner) {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #6b7280;
  transition: color 0.3s ease;
}

.header-left :deep(.el-breadcrumb__inner:hover) {
  color: #f97316;
}

.header-left :deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: #1f2937;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
}

.header-btn:hover {
  background: #fef3c7;
  color: #f97316;
}

.notification-badge :deep(.el-badge__content) {
  background: #ef4444;
  border: 2px solid #fff;
}

.action-dropdown :deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* User Dropdown */
.user-dropdown {
  margin-left: 8px;
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px 6px 6px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-trigger:hover {
  background: #fef3c7;
  border-color: #fcd34d;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 10px;
  color: #fff;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.2;
}

.user-role {
  font-size: 12px;
  color: #6b7280;
  line-height: 1.2;
}

.dropdown-arrow {
  font-size: 14px;
  color: #9ca3af;
  transition: transform 0.3s ease;
}

/* ========================================
   PAGE CONTENT
   ======================================== */
.page-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.page-content::-webkit-scrollbar {
  width: 8px;
}

.page-content::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.page-content::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.page-content::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.page-title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.content-wrapper {
  min-height: 400px;
}

/* ========================================
   PAGE TRANSITIONS
   ======================================== */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========================================
   NOTIFICATIONS DRAWER
   ======================================== */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-item:hover {
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.notification-item.is-unread {
  background: #fffbeb;
  border-color: #fcd34d;
}

.notification-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.notification-icon.type-warning {
  background: #fef3c7;
  color: #f59e0b;
}

.notification-icon.type-success {
  background: #dcfce7;
  color: #22c55e;
}

.notification-icon.type-info {
  background: #dbeafe;
  color: #3b82f6;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-content h4 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.notification-content p {
  margin: 0 0 8px;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.4;
}

.notification-time {
  font-size: 12px;
  color: #9ca3af;
}

/* ========================================
   RESPONSIVE DESIGN
   ======================================== */

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 12px;
}

.mobile-menu-btn:hover {
  background: #fef3c7;
  color: #f97316;
}

/* Sidebar Overlay */
.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 1024px) {
  .mobile-menu-btn {
    display: flex;
  }

  /* Sidebar Overlay - only show on mobile when sidebar is open */
  .sidebar-overlay {
    display: block;
  }

  .sidebar {
    position: fixed !important;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 100;
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .sidebar-open {
    transform: translateX(0) !important;
    width: 260px !important;
  }

  .sidebar-collapsed {
    /* Don't collapse on mobile, sidebar is hidden by default */
  }

  /* Hide collapse button on mobile */
  .collapse-btn {
    display: none;
  }

  .page-content {
    padding: 16px;
  }

  .page-title {
    font-size: 20px;
  }

  /* Hide breadcrumb on mobile */
  .header-left :deep(.el-breadcrumb) {
    display: none;
  }
}

@media (max-width: 640px) {
  .top-header {
    padding: 0 16px;
  }

  .header-left {
    display: none;
  }

  .user-info {
    display: none;
  }

  .page-content {
    padding: 12px;
  }

  .page-title-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
}

:deep(.el-dropdown-menu__item .el-icon) {
  font-size: 18px;
}
</style>
