<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  House, Grid, User as UserIcon, SwitchButton, Menu,
  TrendCharts, Star, Bell
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
    path: '/user/announcements',
    icon: Bell,
    title: '公告中心'
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
    <div class="layout-background">
      <svg class="paw-grid" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="pawGrid" x="0" y="0" width="80" height="80" patternUnits="userSpaceOnUse">
            <g fill="none" stroke="rgba(255, 107, 53, 0.02)" stroke-width="1">
              <circle cx="40" cy="40" r="6"/>
              <circle cx="28" cy="32" r="3"/>
              <circle cx="52" cy="32" r="3"/>
              <circle cx="30" cy="48" r="3"/>
              <circle cx="50" cy="48" r="3"/>
            </g>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#pawGrid)"/>
      </svg>

      <div class="ambient-glow glow-1"></div>
      <div class="ambient-glow glow-2"></div>
    </div>

    <!-- Top Navigation -->
    <header :class="['top-nav', { 'is-scrolled': isScrolled }]">
      <div class="nav-container">
        <!-- Logo -->
        <router-link to="/user/market" class="nav-logo">
          <div class="logo-mark">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="12" fill="url(#navLogoGrad)"/>
              <g transform="translate(12, 9)">
                <path d="M12 3 L20 11 L12 19 L4 11 Z" fill="white"/>
                <path d="M8 19 L12 23 L16 19" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="11" r="3" fill="#FF6B35"/>
              </g>
              <defs>
                <linearGradient id="navLogoGrad" x1="0" y1="0" x2="48" y2="48">
                  <stop offset="0%" stop-color="#FF6B35"/>
                  <stop offset="100%" stop-color="#7B2CBF"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="logo-type">
            <span class="logo-title">宠物用品数据</span>
            <span class="logo-tag">PET DATA</span>
          </div>
        </router-link>

        <!-- Desktop Navigation -->
        <nav class="desktop-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: activeMenu.startsWith(item.path) }"
          >
            <component :is="item.icon" class="nav-icon" />
            <span class="nav-label">{{ item.title }}</span>
            <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
            <span class="nav-dot"></span>
          </router-link>
        </nav>

        <!-- User Actions -->
        <div class="nav-actions">
          <div class="user-chip">
            <div class="user-chip-avatar">
              <UserIcon class="avatar-icon" />
            </div>
            <span class="user-chip-name">{{ userStore.userInfo?.username || '用户' }}</span>
          </div>

          <el-dropdown @command="handleLogout" trigger="click">
            <button class="nav-icon-btn">
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

          <button class="mobile-toggle" @click="toggleMobileMenu">
            <Menu class="icon" />
          </button>
        </div>
      </div>
    </header>

    <!-- Mobile Menu Overlay -->
    <transition name="mobile-fade">
      <div v-if="isMobileMenuOpen" class="mobile-overlay" @click="toggleMobileMenu">
        <div class="mobile-menu" @click.stop>
          <div class="mobile-header">
            <div class="mobile-logo">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="48" height="48" rx="12" fill="url(#mobileLogoGrad)"/>
                <g transform="translate(12, 9)">
                  <path d="M12 3 L20 11 L12 19 L4 11 Z" fill="white"/>
                  <path d="M8 19 L12 23 L16 19" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="12" cy="11" r="3" fill="#FF6B35"/>
                </g>
                <defs>
                  <linearGradient id="mobileLogoGrad" x1="0" y1="0" x2="48" y2="48">
                    <stop offset="0%" stop-color="#FF6B35"/>
                    <stop offset="100%" stop-color="#7B2CBF"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <span class="mobile-title">菜单</span>
            <button class="mobile-close" @click="toggleMobileMenu">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <nav class="mobile-nav">
            <router-link
              v-for="item in menuItems"
              :key="item.path"
              :to="item.path"
              class="mobile-item"
              :class="{ active: activeMenu.startsWith(item.path) }"
              @click="toggleMobileMenu"
            >
              <component :is="item.icon" class="mobile-icon" />
              <span class="mobile-label">{{ item.title }}</span>
              <span v-if="item.badge" class="mobile-badge">{{ item.badge }}</span>
            </router-link>
          </nav>
        </div>
      </div>
    </transition>

    <!-- Main Content -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page-enter" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="layout-footer">
      <div class="footer-content">
        <p class="footer-text">© 2025 天猫宠物用品数据采集系统</p>
        <p class="footer-sub">Data-Driven Pet Market Insights</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens
   ============================================ */
.user-layout {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --bg-primary: #0D0D14;
  --bg-elevated: rgba(20, 20, 32, 0.8);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-hover: rgba(255, 107, 53, 0.3);

  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
  position: relative;
}

/* ============================================
   Background
   ============================================ */
.layout-background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.paw-grid {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.5;
}

.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.4;
  animation: ambientPulse 20s ease-in-out infinite;
}

.glow-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(255, 107, 53, 0.3) 0%, transparent 70%);
  top: -150px;
  right: -150px;
  animation-delay: 0s;
}

.glow-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(123, 44, 191, 0.25) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation-delay: -10s;
}

@keyframes ambientPulse {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.4; }
  50% { transform: translate(30px, -20px) scale(1.1); opacity: 0.5; }
}

/* ============================================
   Top Navigation
   ============================================ */
.top-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: transparent;
  border-bottom: 1px solid transparent;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.top-nav.is-scrolled {
  background: rgba(13, 13, 20, 0.85);
  backdrop-filter: blur(24px);
  border-bottom-color: var(--border-subtle);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
}

/* Logo */
.nav-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.nav-logo:hover {
  transform: scale(1.02);
}

.nav-logo:hover .logo-mark {
  transform: rotate(-5deg);
}

.logo-mark {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  transition: transform 0.3s ease;
  filter: drop-shadow(0 4px 16px rgba(255, 107, 53, 0.3));
}

.logo-mark svg {
  width: 100%;
  height: 100%;
}

.logo-type {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logo-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 16px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-orange), #FFD700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
  line-height: 1;
}

.logo-tag {
  font-family: 'Outfit', sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.15em;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

/* Desktop Navigation */
.desktop-nav {
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

.nav-item.active {
  color: var(--primary-orange);
  background: rgba(255, 107, 53, 0.1);
}

.nav-item.active .nav-dot {
  opacity: 1;
  transform: scale(1);
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav-label {
  position: relative;
  z-index: 1;
}

.nav-badge {
  padding: 3px 8px;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  color: white;
  font-family: 'Outfit', sans-serif;
  font-size: 10px;
  font-weight: 700;
  border-radius: 6px;
  letter-spacing: 0.05em;
}

.nav-dot {
  position: absolute;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%) scale(0);
  width: 4px;
  height: 4px;
  background: var(--primary-orange);
  border-radius: 50%;
  opacity: 0;
  transition: all 0.3s ease;
}

/* Nav Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px 8px 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-default);
  border-radius: 24px;
  transition: all 0.3s ease;
}

.user-chip:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: var(--border-hover);
}

.user-chip-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  border-radius: 50%;
}

.avatar-icon {
  width: 16px;
  height: 16px;
  color: white;
}

.user-chip-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.nav-icon-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-icon-btn:hover {
  color: #ff6b6b;
  border-color: rgba(255, 107, 107, 0.3);
  background: rgba(255, 107, 107, 0.1);
}

.nav-icon-btn .icon {
  width: 18px;
  height: 18px;
}

.mobile-toggle {
  display: none;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-toggle:hover {
  background: rgba(255, 107, 53, 0.1);
  border-color: var(--border-hover);
  color: var(--primary-orange);
}

.mobile-toggle .icon {
  width: 20px;
  height: 20px;
}

/* ============================================
   Mobile Menu
   ============================================ */
.mobile-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(12px);
}

.mobile-menu {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 300px;
  max-width: 90vw;
  background: var(--bg-elevated);
  border-left: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(40px);
}

.mobile-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.mobile-logo {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.mobile-logo svg {
  width: 100%;
  height: 100%;
}

.mobile-title {
  flex: 1;
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.mobile-close {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-default);
  border-radius: 10px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-close:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
}

.mobile-nav {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
}

.mobile-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.mobile-item:hover,
.mobile-item.active {
  background: rgba(255, 107, 53, 0.1);
  color: var(--primary-orange);
}

.mobile-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.mobile-label {
  flex: 1;
}

.mobile-badge {
  padding: 4px 10px;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  color: white;
  font-family: 'Outfit', sans-serif;
  font-size: 10px;
  font-weight: 700;
  border-radius: 6px;
}

/* ============================================
   Main Content
   ============================================ */
.main-content {
  flex: 1;
  position: relative;
  z-index: 1;
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* ============================================
   Footer
   ============================================ */
.layout-footer {
  position: relative;
  z-index: 1;
  padding: 24px;
  border-top: 1px solid var(--border-subtle);
  text-align: center;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
}

.footer-text {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0 0 4px 0;
}

.footer-sub {
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
  opacity: 0.6;
  margin: 0;
  letter-spacing: 0.05em;
}

/* ============================================
   Animations
   ============================================ */
.mobile-fade-enter-active,
.mobile-fade-leave-active {
  transition: all 0.4s ease;
}

.mobile-fade-enter-from,
.mobile-fade-leave-to {
  opacity: 0;
}

.mobile-fade-enter-from .mobile-menu,
.mobile-fade-leave-to .mobile-menu {
  transform: translateX(100%);
}

.page-enter-enter-active,
.page-enter-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-enter-from {
  opacity: 0;
  transform: translateY(16px);
}

.page-enter-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .mobile-toggle {
    display: flex;
  }

  .user-chip {
    display: none;
  }

  .nav-container {
    padding: 16px 20px;
  }
}

@media (max-width: 640px) {
  .main-content {
    padding: 20px 16px;
  }

  .nav-container {
    padding: 12px 16px;
    gap: 12px;
  }

  .logo-type {
    display: none;
  }

  .nav-actions {
    gap: 8px;
  }

  .nav-icon-btn {
    width: 36px;
    height: 36px;
  }

  .mobile-toggle {
    width: 36px;
    height: 36px;
  }
}
</style>
