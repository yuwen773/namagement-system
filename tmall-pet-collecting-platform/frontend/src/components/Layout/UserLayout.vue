<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  House, Grid, User as UserIcon, SwitchButton, Menu,
  TrendCharts, Star
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const isMobileMenuOpen = ref(false)
const isScrolled = ref(false)

const menuItems = computed(() => [
  {
    path: '/user/market',
    icon: Star,
    title: '市场行情',
    badge: 'HOT'
  },
  {
    path: '/user/products',
    icon: Grid,
    title: '商品资源库'
  },
  {
    path: '/user/profile',
    icon: UserIcon,
    title: '个人中心'
  }
])

const activeMenu = computed(() => route.path)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  document.body.style.overflow = isMobileMenuOpen.value ? 'hidden' : ''
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="user-layout">
    <!-- Background Effects -->
    <div class="user-layout__background">
      <div class="bg-gradient-orb orb-1"></div>
      <div class="bg-gradient-orb orb-2"></div>
      <div class="bg-gradient-orb orb-3"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- Top Navigation -->
    <header :class="['top-nav', { 'top-nav--scrolled': isScrolled }]">
      <div class="nav-container">
        <!-- Logo -->
        <router-link to="/user/market" class="nav-logo">
          <div class="logo-icon">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="12" fill="url(#logo-gradient)"/>
              <path d="M24 12L32 20L24 28L16 20L24 12Z" fill="white"/>
              <path d="M20 28L24 32L28 28" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="24" cy="20" r="3" fill="#FF6B35"/>
              <defs>
                <linearGradient id="logo-gradient" x1="0" y1="0" x2="48" y2="48">
                  <stop offset="0%" stop-color="#FF6B35"/>
                  <stop offset="100%" stop-color="#7B2CBF"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="logo-text">
            <span class="logo-title">宠物用品数据</span>
            <span class="logo-subtitle">COLLECT DATA</span>
          </div>
        </router-link>

        <!-- Desktop Navigation -->
        <nav class="desktop-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ active: activeMenu.startsWith(item.path) }"
          >
            <component :is="item.icon" class="nav-icon" />
            <span class="nav-text">{{ item.title }}</span>
            <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
            <span class="nav-indicator"></span>
          </router-link>
        </nav>

        <!-- User Actions -->
        <div class="nav-actions">
          <div class="user-mini-profile">
            <div class="user-avatar">
              <UserIcon class="avatar-icon" />
            </div>
            <span class="user-name">{{ userStore.userInfo?.username || 'Collector' }}</span>
          </div>

          <el-dropdown @command="handleLogout" trigger="click">
            <button class="icon-btn">
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

          <button class="mobile-menu-btn" @click="toggleMobileMenu">
            <Menu class="icon" />
          </button>
        </div>
      </div>
    </header>

    <!-- Mobile Menu Overlay -->
    <transition name="mobile-menu">
      <div v-if="isMobileMenuOpen" class="mobile-menu-overlay" @click="toggleMobileMenu">
        <div class="mobile-menu" @click.stop>
          <div class="mobile-menu-header">
            <div class="logo-icon-small"></div>
            <span class="mobile-menu-title">导航菜单</span>
            <button class="mobile-close-btn" @click="toggleMobileMenu">
              ×
            </button>
          </div>
          <nav class="mobile-nav">
            <router-link
              v-for="item in menuItems"
              :key="item.path"
              :to="item.path"
              class="mobile-nav-link"
              :class="{ active: activeMenu.startsWith(item.path) }"
              @click="toggleMobileMenu"
            >
              <component :is="item.icon" class="nav-icon" />
              <span class="nav-text">{{ item.title }}</span>
              <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
            </router-link>
          </nav>
        </div>
      </div>
    </transition>

    <!-- Main Content -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page-transition" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="layout-footer">
      <p class="footer-text">
        © 2025 天猫宠物用品数据采集系统 · Data Driven Decisions
      </p>
    </footer>
  </div>
</template>

<style scoped>
/* ========================================
   Layout Base
   ======================================== */
.user-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  font-family: var(--font-body);
  position: relative;
}

/* ========================================
   Background Effects
   ======================================== */
.user-layout__background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.bg-gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.15;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: var(--neon-orange);
  top: -200px;
  right: -200px;
  animation-delay: 0s;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: var(--neon-purple);
  bottom: -150px;
  left: -150px;
  animation-delay: -7s;
}

.orb-3 {
  width: 400px;
  height: 400px;
  background: var(--neon-cyan);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.05);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.95);
  }
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, black 0%, transparent 70%);
}

/* ========================================
   Top Navigation
   ======================================== */
.top-nav {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: transparent;
  border-bottom: 1px solid transparent;
  transition: all var(--transition-base);
}

.top-nav--scrolled {
  background: rgba(10, 10, 18, 0.85);
  backdrop-filter: blur(20px);
  border-bottom-color: var(--border-subtle);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-lg) var(--space-xl);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-xl);
}

/* Logo */
.nav-logo {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  text-decoration: none;
  transition: all var(--transition-base);
}

.nav-logo:hover .logo-icon {
  transform: rotate(5deg) scale(1.05);
}

.logo-icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  transition: transform var(--transition-base);
  filter: drop-shadow(0 0 20px rgba(255, 107, 53, 0.4));
}

.logo-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-title {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 800;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 0.02em;
  line-height: 1;
}

.logo-subtitle {
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

/* Desktop Navigation */
.desktop-nav {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.nav-link {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all var(--transition-base);
  overflow: hidden;
}

.nav-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.active {
  color: var(--neon-orange);
}

.nav-link.active .nav-indicator {
  opacity: 1;
  transform: scaleX(1);
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.nav-badge {
  padding: 2px 6px;
  background: var(--gradient-primary);
  color: white;
  font-family: var(--font-display);
  font-size: 0.625rem;
  font-weight: 700;
  border-radius: var(--radius-sm);
  letter-spacing: 0.05em;
}

.nav-indicator {
  position: absolute;
  bottom: 0;
  left: var(--space-sm);
  right: var(--space-sm);
  height: 2px;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  opacity: 0;
  transform: scaleX(0);
  transition: all var(--transition-base);
}

/* User Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.user-mini-profile {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-sm);
  background: var(--surface-glass);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-full);
}

.user-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: 50%;
}

.avatar-icon {
  width: 16px;
  height: 16px;
  color: white;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

.icon-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-glass);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.icon-btn:hover {
  color: var(--status-error);
  border-color: rgba(255, 59, 48, 0.3);
  background: rgba(255, 59, 48, 0.1);
}

.icon-btn .icon {
  width: 18px;
  height: 18px;
}

.mobile-menu-btn {
  display: none;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  background: var(--surface-glass);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-tertiary);
  cursor: pointer;
}

.mobile-menu-btn .icon {
  width: 20px;
  height: 20px;
}

/* ========================================
   Mobile Menu
   ======================================== */
.mobile-menu-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
}

.mobile-menu {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 280px;
  max-width: 85vw;
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
}

.mobile-menu-header {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border-subtle);
}

.logo-icon-small {
  width: 32px;
  height: 32px;
  background: var(--gradient-primary);
  border-radius: var(--radius-md);
}

.mobile-menu-title {
  flex: 1;
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.mobile-close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: var(--radius-sm);
}

.mobile-close-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.mobile-nav {
  flex: 1;
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  transition: all var(--transition-base);
}

.mobile-nav-link:hover,
.mobile-nav-link.active {
  background: rgba(255, 107, 53, 0.1);
  color: var(--neon-orange);
}

.mobile-nav-link .nav-icon {
  width: 20px;
  height: 20px;
}

.mobile-nav-link .nav-badge {
  margin-left: auto;
  padding: 4px 8px;
  background: var(--gradient-primary);
  color: white;
  font-family: var(--font-display);
  font-size: 0.625rem;
  font-weight: 700;
  border-radius: var(--radius-sm);
}

/* ========================================
   Main Content
   ======================================== */
.main-content {
  flex: 1;
  position: relative;
  z-index: 1;
  padding: var(--space-2xl) var(--space-xl);
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* ========================================
   Footer
   ======================================== */
.layout-footer {
  position: relative;
  z-index: 1;
  padding: var(--space-lg);
  text-align: center;
  border-top: 1px solid var(--border-subtle);
}

.footer-text {
  font-size: 0.8125rem;
  color: var(--text-tertiary);
  margin: 0;
}

/* ========================================
   Animations
   ======================================== */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all var(--transition-base);
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
}

.mobile-menu-enter-from .mobile-menu,
.mobile-menu-leave-to .mobile-menu {
  transform: translateX(100%);
}

.page-transition-enter-active,
.page-transition-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-transition-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ========================================
   Responsive
   ======================================== */
@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .user-mini-profile {
    display: none;
  }
}

@media (max-width: 640px) {
  .main-content {
    padding: var(--space-lg) var(--space-md);
  }

  .nav-container {
    padding: var(--space-md) var(--space-lg);
  }
}
</style>
