<template>
  <div class="user-layout">
    <!-- Top Navigation -->
    <header class="top-nav">
      <div class="nav-container">
        <div class="nav-brand">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <span class="brand-text">问答采集</span>
        </div>

        <nav class="nav-menu">
          <router-link
            v-for="item in userNavItems"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ active: isActive(item.path) }"
          >
            <span class="nav-icon" v-html="item.icon"></span>
            <span>{{ item.name }}</span>
          </router-link>
        </nav>

        <div class="nav-actions">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-menu">
              <div class="user-avatar">
                <span>{{ userInitials }}</span>
              </div>
              <span class="user-name">{{ authStore.userInfo?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人中心
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade-scale" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <span class="footer-text">问答信息采集系统</span>
        <span class="footer-divider">|</span>
        <span class="footer-copyright">© 2024</span>
      </div>
    </footer>

    <!-- Decorative Elements -->
    <div class="deco-circle deco-1"></div>
    <div class="deco-circle deco-2"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { User, SwitchButton, ArrowDown } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const currentRoute = computed(() => route)

const userInitials = computed(() => {
  const name = authStore.userInfo?.username || ''
  return name.charAt(0).toUpperCase()
})

const isActive = (path) => {
  return route.path === path
}

const handleCommand = (command) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    authStore.logout()
  }
}

const userNavItems = [
  {
    path: '/overview',
    name: '数据概览',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>'
  },
  {
    path: '/my-data',
    name: '我的数据',
    icon: '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 110-12 6 6 0 010 12z"/><path d="M10 4a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 4zm0 10a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 0110 14z"/></svg>'
  },
  {
    path: '/notices',
    name: '通知公告',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 13a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2Z"/><path d="m9 9 2 2 4-4"/></svg>'
  },
  {
    path: '/profile',
    name: '个人中心',
    icon: '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"/></svg>'
  }
]
</script>

<style scoped>
/* CSS Variables - Soft Minimal Theme */
.user-layout {
  --color-bg: #fafbfc;
  --color-bg-card: #ffffff;
  --color-bg-hover: #f5f7fa;
  --color-border: #e5e9f0;
  --color-border-light: #eef1f5;
  --color-primary: #5c7cfa;
  --color-primary-light: rgba(92, 124, 250, 0.1);
  --color-primary-hover: #748ffc;
  --color-text-primary: #2d3748;
  --color-text-secondary: #718096;
  --color-text-muted: #a0aec0;
  --color-success: #38a169;
  --nav-height: 64px;
}

/* Layout */
.user-layout {
  min-height: 100vh;
  background: var(--color-bg);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-x: hidden;
}

/* Decorative Circles */
.deco-circle {
  position: fixed;
  border-radius: 50%;
  pointer-events: none;
  z-index: 0;
}

.deco-1 {
  width: 400px;
  height: 400px;
  top: -150px;
  right: -100px;
  background: radial-gradient(circle, rgba(92, 124, 250, 0.08) 0%, transparent 70%);
}

.deco-2 {
  width: 300px;
  height: 300px;
  bottom: -100px;
  left: -80px;
  background: radial-gradient(circle, rgba(56, 161, 105, 0.06) 0%, transparent 70%);
}

/* Top Navigation */
.top-nav {
  height: var(--nav-height);
  background: var(--color-bg-card);
  border-bottom: 1px solid var(--color-border-light);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.brand-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, var(--color-primary) 0%, #4263eb 100%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(92, 124, 250, 0.25);
}

.brand-icon svg {
  width: 22px;
  height: 22px;
  color: white;
}

.brand-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -0.02em;
}

/* Navigation Menu */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border-radius: 10px;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.nav-link.active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.nav-icon {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

/* User Actions */
.nav-actions {
  flex-shrink: 0;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.5rem 1rem;
  background: var(--color-bg);
  border: 1px solid var(--color-border-light);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-menu:hover {
  border-color: var(--color-primary);
  box-shadow: 0 2px 8px rgba(92, 124, 250, 0.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, var(--color-primary) 0%, #4263eb 100%);
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: white;
}

.user-name {
  font-size: 0.875rem;
  color: var(--color-text-primary);
  font-weight: 500;
}

.user-menu .el-icon {
  color: var(--color-text-muted);
  font-size: 0.75rem;
  transition: transform 0.2s ease;
}

.user-menu:hover .el-icon {
  transform: rotate(180deg);
}

/* Main Content */
.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem;
  position: relative;
  z-index: 1;
}

/* Transitions */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-scale-enter-from {
  opacity: 0;
  transform: scale(0.98) translateY(10px);
}

.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.98) translateY(-10px);
}

/* Footer */
.footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg-card);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.footer-text {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.footer-divider {
  color: var(--color-border);
}

.footer-copyright {
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
  }

  .nav-menu {
    display: none;
  }

  .brand-text {
    font-size: 1.125rem;
  }

  .user-name {
    display: none;
  }

  .main-content {
    padding: 1rem;
  }
}
</style>
