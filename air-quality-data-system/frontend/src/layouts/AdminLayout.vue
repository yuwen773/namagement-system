<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: adminStore.isCollapsed }">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <svg viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="2" y="2" width="24" height="24" rx="4" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M8 14L12 18L20 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <transition name="fade">
            <span v-if="!adminStore.isCollapsed" class="sidebar-title">管理后台</span>
          </transition>
        </div>
      </div>

      <nav class="sidebar-nav">
        <div
          v-for="item in menuItems"
          :key="item.key"
          class="nav-item"
          :class="{ active: adminStore.activeMenu === item.key }"
          @click="handleMenuSelect(item.key)"
        >
          <svg class="nav-icon" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path v-if="item.key === 'dashboard'" d="M3 3V17H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path v-if="item.key === 'dashboard'" d="M7 11L11 7L15 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'data-import'" d="M17 15V17C17 17.5304 16.7893 18.0391 16.4142 18.4142C16.0391 18.7893 15.5304 19 15 19H5C4.46957 19 3.96086 18.7893 3.58579 18.4142C3.21071 18.0391 3 17.5304 3 17V15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path v-if="item.key === 'data-import'" d="M15 8L10 3L5 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'data-import'" d="M10 15V3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <rect v-if="item.key === 'air-quality'" x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
            <path v-if="item.key === 'air-quality'" d="M7 10H13M10 7V13" stroke="currentColor" stroke-width="1.5"/>
            <path v-if="item.key === 'rules'" d="M10 2L2 7L10 12L18 7L10 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'rules'" d="M2 17L10 22L18 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'rules'" d="M2 12L10 17L18 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'users'" d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <circle v-if="item.key === 'users'" cx="7" cy="7" r="4" stroke="currentColor" stroke-width="1.5"/>
            <path v-if="item.key === 'articles'" d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V16C4 16.5304 4.21071 17.0391 4.58579 17.4142C4.96086 17.7893 5.46957 18 6 18H14C14.5304 18 15.0391 17.7893 15.4142 17.4142C15.7893 17.0391 16 16.5304 16 16V8L14 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'articles'" d="M14 2V8H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'logs'" d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V16C4 16.5304 4.21071 17.0391 4.58579 17.4142C4.96086 17.7893 5.46957 18 6 18H14C14.5304 18 15.0391 17.7893 15.4142 17.4142C15.7893 17.0391 16 16.5304 16 16V8L14 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path v-if="item.key === 'logs'" d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <transition name="fade">
            <span v-if="!adminStore.isCollapsed" class="nav-label">{{ item.label }}</span>
          </transition>
        </div>
      </nav>

      <div class="sidebar-footer">
        <button class="collapse-btn" @click="adminStore.toggleSidebar">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" :class="{ rotated: adminStore.isCollapsed }">
            <path d="M13 15L8 10L13 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="main-wrapper">
      <!-- Top Bar -->
      <header class="top-bar">
        <div class="breadcrumb">
          <span class="breadcrumb-item">管理后台</span>
          <span class="breadcrumb-separator">/</span>
          <span v-if="currentTitle" class="breadcrumb-item current">{{ currentTitle }}</span>
        </div>

        <div class="top-right">
          <button class="user-site-btn" @click="goToUserSite">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 10H17M17 10L12 5M17 10L12 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>用户端</span>
          </button>

          <el-dropdown @command="handleCommand" trigger="click" class="user-dropdown">
            <div class="user-avatar">
              {{ userStore.username?.charAt(0).toUpperCase() || 'A' }}
            </div>
            <template #dropdown>
              <div class="dropdown-menu">
                <div class="dropdown-item" @click="handleLogout">退出登录</div>
              </div>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- Page Content -->
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useAdminStore } from '@/stores/admin'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const adminStore = useAdminStore()

const currentTitle = computed(() => route.meta.title || '')

const menuItems = [
  { key: 'dashboard', label: '仪表盘', path: '/admin' },
  { key: 'data-import', label: '数据导入', path: '/admin/data-import' },
  { key: 'air-quality', label: '数据管理', path: '/admin/air-quality' },
  { key: 'rules', label: '规则管理', path: '/admin/rules' },
  { key: 'users', label: '用户管理', path: '/admin/users' },
  { key: 'articles', label: '文章管理', path: '/admin/articles' },
  { key: 'logs', label: '系统日志', path: '/admin/logs' }
]

const handleMenuSelect = (key) => {
  adminStore.setActiveMenu(key)
  const item = menuItems.find(i => i.key === key)
  if (item) {
    router.push(item.path)
  }
}

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.clearUser()
      router.push('/login')
    })
  }
}

const handleLogout = () => {
  handleCommand('logout')
}

const goToUserSite = () => {
  router.push('/')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-main);
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: var(--bg-card);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-base);
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.sidebar-logo svg {
  width: 24px;
  height: 24px;
  color: var(--primary);
  flex-shrink: 0;
}

.sidebar-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
}

/* Sidebar Navigation */
.sidebar-nav {
  flex: 1;
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.nav-item.active {
  background: var(--bg-hover);
  color: var(--primary);
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav-label {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border);
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm);
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  color: var(--text-secondary);
}

.collapse-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.collapse-btn svg {
  width: 16px;
  height: 16px;
  transition: transform var(--transition-base);
}

.collapse-btn svg.rotated {
  transform: rotate(180deg);
}

/* Main Wrapper */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Top Bar */
.top-bar {
  height: 64px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-xl);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.breadcrumb-item {
  font-size: 14px;
  color: var(--text-secondary);
}

.breadcrumb-item.current {
  color: var(--text);
}

.breadcrumb-separator {
  color: var(--text-muted);
}

.top-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-site-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.user-site-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
  border-color: var(--border);
}

.user-site-btn svg {
  width: 16px;
  height: 16px;
}

.user-dropdown {
  cursor: pointer;
}

.user-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary);
  color: white;
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius-md);
}

/* Dropdown Menu */
.dropdown-menu {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  min-width: 140px;
  padding: var(--spacing-xs);
}

.dropdown-item {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--bg-hover);
  color: var(--text);
}

/* Main Content */
.main-content {
  flex: 1;
  padding: var(--spacing-xl);
  overflow-y: auto;
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity var(--transition-fast);
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 100;
  }

  .sidebar.collapsed {
    transform: translateX(-100%);
  }
}

/* Scrollbar */
.main-content::-webkit-scrollbar {
  width: 6px;
}

.main-content::-webkit-scrollbar-track {
  background: transparent;
}

.main-content::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: var(--radius-sm);
}

.main-content::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}

/* Override Element Plus */
:deep(.el-dropdown-menu) {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}
</style>
