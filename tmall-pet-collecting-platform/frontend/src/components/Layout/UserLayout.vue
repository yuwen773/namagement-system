<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  House, Grid, User as UserIcon, SwitchButton, Menu,
  TrendCharts, Star, Bell, Message
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
    path: '/user/feedback',
    icon: Message,
    title: '意见反馈'
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
    <!-- 自然背景装饰 -->
    <div class="layout-background">
      <div class="paper-texture"></div>

      <!-- 漂浮叶片 -->
      <div class="floating-leaves">
        <div class="leaf leaf-1">
          <svg viewBox="0 0 60 80" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M30 5C30 5 50 20 50 40C50 60 40 70 30 70C20 70 10 60 10 40C10 20 30 5 30 5Z" fill="url(#leafGrad1)" opacity="0.08"/>
            <defs>
              <linearGradient id="leafGrad1" x1="30" y1="5" x2="30" y2="70">
                <stop offset="0%" stop-color="#52B788"/>
                <stop offset="100%" stop-color="#2D6A4F"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div class="leaf leaf-2">
          <svg viewBox="0 0 50 70" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M25 5C25 5 42 18 42 35C42 52 34 60 25 60C16 60 8 52 8 35C8 18 25 5 25 5Z" fill="url(#leafGrad2)" opacity="0.06"/>
            <defs>
              <linearGradient id="leafGrad2" x1="25" y1="5" x2="25" y2="60">
                <stop offset="0%" stop-color="#90E0EF"/>
                <stop offset="100%" stop-color="#00B4D8"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <div class="leaf leaf-3">
          <svg viewBox="0 0 40 60" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 5C20 5 34 15 34 30C34 45 28 52 20 52C12 52 6 45 6 30C6 15 20 5 20 5Z" fill="url(#leafGrad3)" opacity="0.05"/>
            <defs>
              <linearGradient id="leafGrad3" x1="20" y1="5" x2="20" y2="52">
                <stop offset="0%" stop-color="#74C69D"/>
                <stop offset="100%" stop-color="#40916C"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>

      <!-- 环境光晕 -->
      <div class="ambient-glow glow-green"></div>
      <div class="ambient-glow glow-blue"></div>
    </div>

    <!-- Top Navigation -->
    <header :class="['top-nav', { 'is-scrolled': isScrolled }]">
      <div class="nav-container">
        <!-- Logo -->
        <router-link to="/user/market" class="nav-logo">
          <div class="logo-mark">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="24" cy="24" r="22" fill="url(#navLogoBg)" fill-opacity="0.15"/>
              <circle cx="24" cy="24" r="22" stroke="url(#navLogoBorder)" stroke-width="1.5"/>
              <g transform="translate(24, 24)">
                <path d="M0 -13C0 -13 11 -6 11 5C11 14 5 17 0 17C-5 17 -11 14 -11 5C-11 -6 0 -13 0 -13Z" fill="url(#navLogoLeaf)"/>
                <path d="M0 -13L0 17" stroke="white" stroke-width="1" stroke-linecap="round" opacity="0.5"/>
                <circle cx="0" cy="-13" r="2.5" fill="#52B788"/>
              </g>
              <defs>
                <linearGradient id="navLogoBg" x1="2" y1="2" x2="46" y2="46">
                  <stop offset="0%" stop-color="#52B788"/>
                  <stop offset="100%" stop-color="#2D6A4F"/>
                </linearGradient>
                <linearGradient id="navLogoBorder" x1="2" y1="2" x2="46" y2="46">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="navLogoLeaf" x1="-11" y1="-13" x2="11" y2="17">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
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
                <circle cx="24" cy="24" r="22" fill="url(#mobileLogoBg)" fill-opacity="0.15"/>
                <circle cx="24" cy="24" r="22" stroke="url(#mobileLogoBorder)" stroke-width="1.5"/>
                <g transform="translate(24, 24)">
                  <path d="M0 -13C0 -13 11 -6 11 5C11 14 5 17 0 17C-5 17 -11 14 -11 5C-11 -6 0 -13 0 -13Z" fill="url(#mobileLogoLeaf)"/>
                  <circle cx="0" cy="-13" r="2.5" fill="#52B788"/>
                </g>
                <defs>
                  <linearGradient id="mobileLogoBg" x1="2" y1="2" x2="46" y2="46">
                    <stop offset="0%" stop-color="#52B788"/>
                    <stop offset="100%" stop-color="#2D6A4F"/>
                  </linearGradient>
                  <linearGradient id="mobileLogoBorder" x1="2" y1="2" x2="46" y2="46">
                    <stop offset="0%" stop-color="#74C69D"/>
                    <stop offset="100%" stop-color="#40916C"/>
                  </linearGradient>
                  <linearGradient id="mobileLogoLeaf" x1="-11" y1="-13" x2="11" y2="17">
                    <stop offset="0%" stop-color="#74C69D"/>
                    <stop offset="100%" stop-color="#40916C"/>
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

          <!-- 移动端底部装饰植物 -->
          <div class="mobile-footer-plant">
            <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
              <path d="M30 55V25" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M30 40C30 40 42 32 42 22C42 16 37 13 30 13C23 13 18 16 18 22C18 32 30 40 30 40Z" fill="#74C69D" fill-opacity="0.2"/>
              <path d="M30 28C30 28 38 23 38 16C38 12 34 9 30 9C26 9 22 12 22 16C22 23 30 28 30 28Z" fill="#52B788" fill-opacity="0.3"/>
            </svg>
          </div>
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
        <!-- 装饰线 -->
        <div class="footer-decoration">
          <div class="deco-line"></div>
          <div class="deco-leaf">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2C10 2 16 6 16 10C16 14 13 16 10 16C7 16 4 14 4 10C4 6 10 2 10 2Z" fill="currentColor" opacity="0.3"/>
            </svg>
          </div>
          <div class="deco-line"></div>
        </div>

        <p class="footer-text">© 2025 天猫宠物用品数据采集系统</p>
        <p class="footer-sub">自然生长 · 数据洞察</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.user-layout {
  --primary-green: #2D6A4F;
  --primary-green-light: #40916C;
  --primary-green-lighter: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);

  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-cream);
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
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

.paper-texture {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.025'/%3E%3C/svg%3E");
  opacity: 0.5;
}

.floating-leaves {
  position: absolute;
  inset: 0;
}

.leaf {
  position: absolute;
  animation: leafFloat 25s ease-in-out infinite;
}

.leaf-1 {
  top: 15%;
  right: 8%;
  width: 80px;
  height: 107px;
  animation-delay: 0s;
}

.leaf-2 {
  top: 60%;
  right: 5%;
  width: 60px;
  height: 84px;
  animation-delay: -12s;
}

.leaf-3 {
  bottom: 20%;
  left: 5%;
  width: 50px;
  height: 75px;
  animation-delay: -6s;
}

@keyframes leafFloat {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(10px, -15px) rotate(3deg); }
  50% { transform: translate(-5px, 10px) rotate(-2deg); }
  75% { transform: translate(15px, 5px) rotate(2deg); }
}

.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  animation: ambientPulse 30s ease-in-out infinite;
}

.glow-green {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(82, 183, 136, 0.2) 0%, transparent 70%);
  top: -150px;
  right: -150px;
  animation-delay: 0s;
}

.glow-blue {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(144, 224, 239, 0.15) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation-delay: -15s;
}

@keyframes ambientPulse {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
  50% { transform: translate(20px, -10px) scale(1.05); opacity: 0.6; }
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
  background: rgba(250, 250, 249, 0.9);
  backdrop-filter: blur(24px);
  border-bottom-color: var(--border-light);
  box-shadow: 0 4px 20px rgba(45, 106, 79, 0.05);
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
  transform: rotate(-3deg);
}

.logo-mark {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  transition: transform 0.3s ease;
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
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-green), var(--primary-green-lighter));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.01em;
  line-height: 1;
}

.logo-tag {
  font-family: 'Nunito', sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.1em;
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
  font-family: 'Noto Serif SC', serif;
}

.nav-item::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--bg-sand);
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-item:hover {
  color: var(--primary-green);
}

.nav-item:hover::before {
  opacity: 1;
}

.nav-item.active {
  color: var(--primary-green);
  background: rgba(116, 198, 157, 0.12);
}

.nav-item.active .nav-dot {
  opacity: 1;
  transform: translateX(-50%) scale(1);
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  position: relative;
  z-index: 1;
}

.nav-label {
  position: relative;
  z-index: 1;
}

.nav-badge {
  padding: 3px 8px;
  background: linear-gradient(135deg, var(--primary-green-light), var(--primary-green));
  color: white;
  font-family: 'Nunito', sans-serif;
  font-size: 10px;
  font-weight: 700;
  border-radius: 6px;
  letter-spacing: 0.03em;
  position: relative;
  z-index: 1;
}

.nav-dot {
  position: absolute;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%) scale(0);
  width: 4px;
  height: 4px;
  background: var(--primary-green);
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
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(45, 106, 79, 0.04);
}

.user-chip:hover {
  box-shadow: var(--shadow-soft);
  border-color: var(--accent-green);
}

.user-chip-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-green-light), var(--primary-green-lighter));
  border-radius: 50%;
}

.avatar-icon {
  width: 16px;
  height: 16px;
  color: white;
}

.user-chip-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Noto Serif SC', serif;
}

.nav-icon-btn {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-icon-btn:hover {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.05);
}

.nav-icon-btn .icon {
  width: 18px;
  height: 18px;
}

.mobile-toggle {
  display: none;
  width: 42px;
  height: 42px;
  align-items: center;
  justify-content: center;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-toggle:hover {
  background: rgba(116, 198, 157, 0.1);
  border-color: var(--accent-green);
  color: var(--primary-green);
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
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
}

.mobile-menu {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 320px;
  max-width: 90vw;
  background: var(--bg-card);
  border-left: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(40px);
  box-shadow: -10px 0 40px rgba(45, 106, 79, 0.1);
}

.mobile-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, rgba(116, 198, 157, 0.03) 0%, transparent 100%);
}

.mobile-logo {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.mobile-logo svg {
  width: 100%;
  height: 100%;
}

.mobile-title {
  flex: 1;
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.mobile-close {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  color: var(--text-tertiary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-close:hover {
  background: var(--bg-card);
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
  font-family: 'Noto Serif SC', serif;
}

.mobile-item:hover,
.mobile-item.active {
  background: rgba(116, 198, 157, 0.12);
  color: var(--primary-green);
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
  background: linear-gradient(135deg, var(--primary-green-light), var(--primary-green));
  color: white;
  font-family: 'Nunito', sans-serif;
  font-size: 10px;
  font-weight: 700;
  border-radius: 6px;
}

.mobile-footer-plant {
  padding: 20px;
  display: flex;
  justify-content: center;
  opacity: 0.5;
  animation: mobilePlantSway 4s ease-in-out infinite;
}

@keyframes mobilePlantSway {
  0%, 100% { transform: rotate(-2deg); }
  50% { transform: rotate(2deg); }
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
  padding: 32px 24px;
  border-top: 1px solid var(--border-light);
  text-align: center;
  background: linear-gradient(180deg, transparent 0%, rgba(116, 198, 157, 0.02) 100%);
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
}

.footer-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 16px;
}

.deco-line {
  width: 40px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-light));
}

.deco-line:last-child {
  background: linear-gradient(90deg, var(--border-light), transparent);
}

.deco-leaf {
  color: var(--accent-green);
}

.footer-text {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0 0 4px 0;
  font-family: 'Nunito', sans-serif;
}

.footer-sub {
  font-family: 'Nunito', sans-serif;
  font-size: 11px;
  color: var(--text-tertiary);
  opacity: 0.7;
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

  .leaf {
    opacity: 0.4;
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
    width: 38px;
    height: 38px;
  }

  .mobile-toggle {
    width: 38px;
    height: 38px;
  }

  .footer-text {
    font-size: 12px;
  }

  .leaf-1, .leaf-2 {
    display: none;
  }
}
</style>
