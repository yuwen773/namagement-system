<template>
  <div class="user-layout">
    <!-- Header -->
    <header class="header">
      <div class="header-container">
        <!-- Logo -->
        <div class="logo" @click="router.push('/')">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="18" cy="18" r="14" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M18 8V28" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="18" cy="18" r="4" fill="currentColor"/>
          </svg>
          <span class="logo-text">空气质量监测</span>
        </div>

        <!-- Navigation -->
        <nav class="nav">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            {{ item.label }}
          </router-link>
        </nav>

        <!-- User Section -->
        <div class="user-section">
          <template v-if="!userStore.isLoggedIn">
            <router-link to="/login" class="btn btn-primary">登录</router-link>
          </template>
          <el-dropdown v-else @command="handleCommand" trigger="click" class="user-dropdown">
            <div class="user-trigger">
              <svg class="user-icon" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 10C12.7614 10 15 7.76142 15 5C15 2.23858 12.7614 0 10 0C7.23858 0 5 2.23858 5 5C5 7.76142 7.23858 10 10 10Z" stroke="currentColor" stroke-width="1.5" fill="none"/>
                <path d="M17 17C17 14.7909 15.7558 13 13 13H7C4.24419 13 3 14.7909 3 17" stroke="currentColor" stroke-width="1.5" fill="none" stroke-linecap="round"/>
              </svg>
              <span class="user-name">{{ userStore.username }}</span>
              <svg class="dropdown-icon" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 8L10 13L15 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <template #dropdown>
              <div class="dropdown-menu">
                <div v-if="userStore.isAdmin" class="dropdown-item" @click="router.push('/admin')">
                  <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 3H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M3 7H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M3 11H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  管理后台
                </div>
                <div class="dropdown-divider" v-if="userStore.isAdmin"></div>
                <div class="dropdown-item" @click="handleLogout">
                  <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7 17L10.5 20.5L17 14M17 14H11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M14 6H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M10 2V10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  退出登录
                </div>
              </div>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-content">
          <p class="copyright">&copy; 2026 全国空气质量数据监测与居民个人防护指南平台</p>
          <p class="footer-links">
            <a href="#">关于我们</a>
            <span class="separator">·</span>
            <a href="#">隐私政策</a>
            <span class="separator">·</span>
            <a href="#">使用条款</a>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const navItems = [
  { path: '/', label: '首页' },
  { path: '/historical', label: '历史数据' },
  { path: '/analysis', label: '数据分析' },
  { path: '/protection', label: '防护指南' },
  { path: '/knowledge', label: '科普知识' }
]

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.clearUser()
      router.push('/')
    })
  }
}

const handleLogout = () => {
  handleCommand('logout')
}
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-main);
}

/* Header */
.header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  cursor: pointer;
  user-select: none;
}

.logo svg {
  width: 28px;
  height: 28px;
  color: var(--primary);
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

/* Navigation */
.nav {
  display: flex;
  gap: var(--spacing-xs);
}

.nav-item {
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.nav-item:hover {
  color: var(--primary);
  background: var(--bg-hover);
}

.nav-item.active {
  color: var(--primary);
  background: var(--bg-hover);
}

/* User Section */
.user-section {
  display: flex;
  align-items: center;
}

.btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: all var(--transition-fast);
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
}

/* User Dropdown */
.user-dropdown {
  cursor: pointer;
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  cursor: pointer;
}

.user-trigger:hover {
  background: var(--bg-hover);
}

.user-icon {
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text);
}

.dropdown-icon {
  width: 16px;
  height: 16px;
  color: var(--text-muted);
}

/* Dropdown Menu */
.dropdown-menu {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  min-width: 180px;
  padding: var(--spacing-xs);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-secondary);
  font-size: 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.dropdown-item svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.dropdown-divider {
  height: 1px;
  background: var(--border);
  margin: var(--spacing-xs) 0;
}

/* Main Content */
.main-content {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: var(--spacing-2xl) var(--spacing-xl);
}

/* Footer */
.footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  padding: var(--spacing-xl) 0;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.copyright {
  font-size: 13px;
  color: var(--text-muted);
}

.footer-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  font-size: 13px;
}

.footer-links a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer-links a:hover {
  color: var(--primary);
}

.separator {
  color: var(--border);
}

/* Responsive */
@media (max-width: 768px) {
  .nav {
    display: none;
  }

  .footer-content {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
}

/* Override Element Plus */
:deep(.el-dropdown-menu) {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}
</style>
