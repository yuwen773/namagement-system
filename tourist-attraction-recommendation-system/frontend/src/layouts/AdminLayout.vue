<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- Logo -->
      <div class="sidebar-header">
        <div class="logo-wrapper">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            <path d="M12 2C12 2 16 8 16 12C16 15.3137 13.3137 18 10 18C6.68629 18 4 15.3137 4 12C4 8 8 2 8 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M12 22V18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="logo-text">管理后台</span>
        </div>
        <button class="collapse-btn" @click="toggleSidebar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 19l-7-7 7-7M18 19l-7-7 7-7"/>
          </svg>
        </button>
      </div>

      <!-- Navigation -->
      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item) }"
        >
          <div class="nav-icon">
            <component :is="item.icon" />
          </div>
          <span class="nav-text">{{ item.title }}</span>
          <div class="nav-indicator" v-show="isActive(item)"></div>
        </router-link>
      </nav>

      <!-- User Section -->
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">
            {{ userStore.user?.real_name?.charAt(0) || userStore.user?.realName?.charAt(0) || 'A' }}
          </div>
          <div class="user-details">
            <p class="user-name">{{ userStore.user?.real_name || userStore.user?.realName || '管理员' }}</p>
            <p class="user-role">管理员</p>
          </div>
        </div>
        <el-dropdown trigger="click" @command="handleCommand" placement="right">
          <button class="user-menu-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"/>
              <circle cx="12" cy="5" r="1"/>
              <circle cx="12" cy="19" r="1"/>
            </svg>
          </button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="settings">
                <svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                个人设置
              </el-dropdown-item>
              <el-dropdown-item command="home">
                <svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                  <polyline points="9 22 9 12 15 12 15 22"/>
                </svg>
                返回前台
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="main-content" :class="{ expanded: sidebarCollapsed }">
      <!-- Top Bar -->
      <header class="topbar">
        <h1 class="page-title">{{ currentPageTitle }}</h1>
        <div class="topbar-actions">
          <router-link to="/" class="front-link" title="返回前台">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </router-link>
        </div>
      </header>

      <!-- Page Content -->
      <main class="page-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'
import {
  MapLocation, DataBoard, User, Ticket, ChatDotSquare, Bell, Setting
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const sidebarCollapsed = ref(false)

const menuItems = [
  { path: '/admin', title: '数据看板', icon: DataBoard },
  { path: '/admin/users', title: '用户管理', icon: User },
  { path: '/admin/attractions', title: '景点管理', icon: Ticket },
  { path: '/admin/comments', title: '评论审核', icon: ChatDotSquare },
  { path: '/admin/announcements', title: '公告管理', icon: Bell },
  { path: '/admin/settings', title: '个人设置', icon: Setting }
]

const currentPageTitle = computed(() => {
  const item = menuItems.find(m => m.path === route.path)
  return item?.title || route.meta?.title || '管理后台'
})

function isActive(item) {
  if (item.path === '/admin') {
    return route.path === '/admin'
  }
  return route.path === item.path || route.path.startsWith(item.path + '/')
}

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

function handleCommand(command) {
  switch (command) {
    case 'settings':
      router.push('/admin/settings')
      break
    case 'home':
      router.push('/')
      break
    case 'logout':
      ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        userStore.logout()
        router.push('/admin/login')
      })
      break
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.admin-layout {
  height: 100vh;
  display: flex;
  background: #f8fafc;
  font-family: 'DM Sans', sans-serif;
  overflow: hidden;
  width: 100%;
}

/* Sidebar */
.sidebar {
  width: 260px;
  min-width: 260px;
  background: linear-gradient(180deg, #1e3a5f 0%, #0f172a 100%);
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 50;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar.collapsed {
  width: 80px;
  min-width: 80px;
}

.sidebar-header {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar.collapsed .sidebar-header {
  padding: 0 12px;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: #fbbf24;
  flex-shrink: 0;
}

.logo-text {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  font-weight: 700;
  color: white;
  white-space: nowrap;
  letter-spacing: 0.5px;
  transition: opacity 0.3s ease;
}

.sidebar.collapsed .logo-text {
  display: none;
}

.collapse-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.collapse-btn svg {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.sidebar.collapsed .collapse-btn svg {
  transform: rotate(180deg);
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 20px 12px;
  overflow-y: auto;
  scrollbar-width: none; /* Firefox */
}

.sidebar-nav::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 6px;
  color: rgba(255, 255, 255, 0.65);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(249, 115, 22, 0.15) 100%);
  color: #fbbf24;
  font-weight: 600;
}

.nav-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon svg {
  width: 100%;
  height: 100%;
}

.nav-text {
  font-size: 14.5px;
  font-weight: 500;
  transition: opacity 0.3s ease;
}

.sidebar.collapsed .nav-text {
  display: none;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding-left: 0;
  padding-right: 0;
}

.nav-indicator {
  position: absolute;
  right: 14px;
  width: 6px;
  height: 6px;
  background: #fbbf24;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(251, 191, 36, 0.6);
}

.sidebar.collapsed .nav-indicator {
  right: 8px;
  width: 5px;
  height: 5px;
}

/* Sidebar Footer */
.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px;
  height: 80px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.1);
  overflow: hidden;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
  transition: opacity 0.3s ease;
}

.sidebar.collapsed .user-info {
  display: none;
}

.sidebar.collapsed .sidebar-footer {
  justify-content: center;
  padding: 0;
}

.user-avatar {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
  font-weight: 600;
  font-size: 15px;
  border-radius: 10px;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.user-details {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 2px;
}

.user-menu-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.user-menu-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.user-menu-btn svg {
  width: 16px;
  height: 16px;
}

/* Main Content */
.main-content {
  margin-left: 260px;
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 0;
  height: 100vh;
  overflow: hidden;
}

.main-content.expanded {
  margin-left: 80px;
}

/* Top Bar */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 72px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 700;
  color: #1f2937;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.front-link {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 10px;
  color: #64748b;
  transition: all 0.2s ease;
}

.front-link:hover {
  background: #1e3a5f;
  color: white;
  transform: translateY(-1px);
}

.front-link svg {
  width: 20px;
  height: 20px;
}

/* Page Content */
.page-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
  background: #f8fafc;
}

/* Dropdown Menu Styles */
:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
}

.menu-icon {
  width: 18px;
  height: 18px;
  color: #6b7280;
}

:deep(.el-dropdown-menu__item:hover .menu-icon) {
  color: #1e3a5f;
}

/* Responsive */
@media (max-width: 1024px) {
  .sidebar {
    width: 80px;
  }

  .sidebar.collapsed {
    width: 0;
    overflow: hidden;
  }

  .main-content {
    margin-left: 80px;
  }

  .main-content.expanded {
    margin-left: 0;
  }

  .logo-text,
  .nav-text,
  .user-info {
    display: none;
  }

  .sidebar-footer {
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .topbar {
    padding: 16px 20px;
  }

  .page-title {
    font-size: 20px;
  }

  .page-content {
    padding: 20px 16px;
  }
}
</style>
