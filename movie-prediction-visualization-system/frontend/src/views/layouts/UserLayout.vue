<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import {
  HomeFilled,
  DataAnalysis,
  TrendCharts,
  UserFilled,
  SwitchButton,
  Fold,
  Expand,
  Film,
  Ticket
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 移动端菜单状态
const mobileMenuOpen = ref(false)
const scrolled = ref(false)

// 导航菜单项
const navItems = [
  { path: '/', name: '数据看板', icon: HomeFilled },
  { path: '/boxoffice', name: '票房查询', icon: Ticket },
  { path: '/visualization', name: '可视化图表', icon: DataAnalysis },
  { path: '/prediction', name: '票房预测', icon: TrendCharts },
  { path: '/profile', name: '个人中心', icon: UserFilled }
]

// 当前激活路由
const activePath = computed(() => route.path)

// 切换移动端菜单
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

// 导航到指定路径
const navigateTo = (path) => {
  mobileMenuOpen.value = false
  router.push(path)
}

// 退出登录
const handleLogout = () => {
  userStore.doLogout()
  router.push('/login')
  ElMessage.success('退出登录成功')
}

// 处理滚动效果
const handleScroll = () => {
  scrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="user-layout min-h-screen bg-slate-950 relative overflow-hidden">
    <!-- 背景效果层 -->
    <div class="background-layer">
      <!-- 胶片颗粒纹理 -->
      <div class="film-grain"></div>
      <!-- 渐变光晕 -->
      <div class="glow-effects">
        <div class="glow-orb glow-gold"></div>
        <div class="glow-orb glow-red"></div>
        <div class="glow-orb glow-cyan"></div>
      </div>
      <!-- 网格背景 -->
      <div class="grid-pattern"></div>
    </div>

    <!-- 头部导航栏 -->
    <header
      class="fixed top-0 left-0 right-0 z-50 transition-all duration-500"
      :class="{ 'header-scrolled': scrolled }"
    >
      <!-- 胶片卷轴装饰 -->
      <div class="film-strip-top"></div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="header-content">
          <!-- Logo 区域 -->
          <div class="logo-section" @click="router.push('/')">
            <div class="film-icon">
              <Film class="w-8 h-8" />
            </div>
            <div class="logo-text">
              <h1 class="logo-title">
                <span class="title-highlight">MOVI</span>PREDICT
              </h1>
              <p class="logo-subtitle">票房预测系统</p>
            </div>
          </div>

          <!-- 桌面端导航 -->
          <nav class="desktop-nav">
            <a
              v-for="item in navItems"
              :key="item.path"
              class="nav-link"
              :class="{ 'nav-link-active': activePath === item.path }"
              @click="navigateTo(item.path)"
            >
              <component :is="item.icon" class="nav-icon" />
              <span class="nav-text">{{ item.name }}</span>
              <span class="nav-indicator"></span>
            </a>
          </nav>

          <!-- 用户区域 -->
          <div class="user-section">
            <div class="user-dropdown">
              <el-dropdown trigger="click" @command="handleLogout">
                <div class="user-info">
                  <div class="user-avatar">
                    <span class="avatar-text">
                      {{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'U' }}
                    </span>
                    <div class="avatar-ring"></div>
                  </div>
                  <span class="user-name">
                    {{ userStore.user?.real_name || userStore.user?.username || '用户' }}
                  </span>
                </div>
                <template #dropdown>
                  <el-dropdown-menu class="custom-dropdown">
                    <el-dropdown-item @click="router.push('/profile')">
                      <UserFilled class="dropdown-icon" /> 个人中心
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <SwitchButton class="dropdown-icon" /> 退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>

          <!-- 移动端菜单按钮 -->
          <button
            class="mobile-menu-btn"
            :class="{ 'mobile-menu-active': mobileMenuOpen }"
            @click="toggleMobileMenu"
            aria-label="Toggle menu"
          >
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </button>
        </div>
      </div>
    </header>

    <!-- 移动端导航菜单 -->
    <div
      class="mobile-nav-overlay"
      :class="{ 'mobile-nav-open': mobileMenuOpen }"
      @click="toggleMobileMenu"
    >
      <div class="mobile-nav-panel" @click.stop>
        <div class="mobile-nav-header">
          <div class="mobile-user-info">
            <div class="mobile-user-avatar">
              {{ userStore.user?.username?.charAt(0)?.toUpperCase() || 'U' }}
            </div>
            <div class="mobile-user-details">
              <p class="mobile-user-name">
                {{ userStore.user?.real_name || userStore.user?.username || '用户' }}
              </p>
              <p class="mobile-user-role">普通用户</p>
            </div>
          </div>
        </div>
        <nav class="mobile-nav-links">
          <a
            v-for="item in navItems"
            :key="item.path"
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': activePath === item.path }"
            @click="navigateTo(item.path)"
          >
            <component :is="item.icon" class="mobile-nav-icon" />
            <span>{{ item.name }}</span>
          </a>
        </nav>
      </div>
    </div>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- 底部 -->
    <footer class="footer">
      <!-- 顶部渐变光晕装饰 -->
      <div class="footer-glow"></div>
      <!-- 胶片卷轴装饰 -->
      <div class="film-strip-bottom"></div>

      <div class="footer-container">
        <!-- 主内容区 -->
        <div class="footer-main">
          <!-- 品牌区域 -->
          <div class="footer-brand">
            <div class="brand-logo">
              <div class="logo-icon-wrapper">
                <Film class="logo-icon" />
              </div>
              <div class="brand-text">
                <h3 class="brand-title">MOVI<span class="brand-accent">PREDICT</span></h3>
                <p class="brand-tagline">智能票房预测系统</p>
              </div>
            </div>
            <p class="brand-desc">
              基于大数据分析与机器学习算法，为电影行业提供专业的票房预测与数据可视化服务。
            </p>
            <!-- 联系方式 -->
            <div class="contact-section">
              <div class="contact-item">
                <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                <span>contact@movipredict.com</span>
              </div>
              <div class="contact-item">
                <svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <span>北京市朝阳区</span>
              </div>
            </div>
          </div>

          <!-- 核心导航 -->
          <div class="footer-nav-section">
            <div class="nav-column">
              <h4 class="nav-title">数据探索</h4>
              <nav class="nav-list">
                <a class="nav-item" @click="router.push('/')">
                  <span class="nav-dot"></span>
                  数据看板
                </a>
                <a class="nav-item" @click="router.push('/boxoffice')">
                  <span class="nav-dot"></span>
                  票房查询
                </a>
                <a class="nav-item" @click="router.push('/visualization')">
                  <span class="nav-dot"></span>
                  可视化图表
                </a>
              </nav>
            </div>

            <div class="nav-column">
              <h4 class="nav-title">预测分析</h4>
              <nav class="nav-list">
                <a class="nav-item" @click="router.push('/prediction')">
                  <span class="nav-dot"></span>
                  票房预测
                </a>
                <a class="nav-item" @click="router.push('/visualization')">
                  <span class="nav-dot"></span>
                  地域分析
                </a>
                <a class="nav-item" @click="router.push('/visualization')">
                  <span class="nav-dot"></span>
                  类型偏好
                </a>
              </nav>
            </div>

            <div class="nav-column">
              <h4 class="nav-title">个人中心</h4>
              <nav class="nav-list">
                <a class="nav-item" @click="router.push('/profile')">
                  <span class="nav-dot"></span>
                  个人资料
                </a>
                <a class="nav-item" @click="router.push('/profile')">
                  <span class="nav-dot"></span>
                  账户设置
                </a>
                <a class="nav-item" @click="handleLogout">
                  <span class="nav-dot nav-dot-red"></span>
                  退出登录
                </a>
              </nav>
            </div>
          </div>
        </div>

        <!-- 底部版权栏 -->
        <div class="footer-bottom">
          <div class="copyright-line">
            <span class="copyright-text">© 2024 MOVIPREDICT. All rights reserved.</span>
            <span class="copyright-divider"></span>
            <span class="copyright-links">
              <a href="#" class="copyright-link">隐私政策</a>
              <a href="#" class="copyright-link">服务条款</a>
              <a href="#" class="copyright-link">帮助中心</a>
            </span>
          </div>
          <!-- 社交媒体 -->
          <div class="social-links">
            <a class="social-btn" href="#" aria-label="WeChat">
              <svg class="social-btn-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 01.213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 00.167-.054l1.903-1.114a.864.864 0 01.717-.098 10.16 10.16 0 002.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348z"/>
              </svg>
            </a>
            <a class="social-btn" href="#" aria-label="Weibo">
              <svg class="social-btn-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M10.098 20c-3.926-.327-7.334-2.42-7.543-5.503-.21-3.09 3.073-5.983 7.347-6.462 4.274-.479 8.054 1.625 8.446 4.702.392 3.076-2.874 5.92-7.25 7.263m1.093-2.275c-.376.598-1.163.836-1.765.64-.59-.19-.702-.76-.236-1.278.48-.535 1.305-.75 1.8-.505.505.25.476.793.2 1.143m.853-1.66c-.135.224-.433.37-.667.328-.226-.043-.28-.257-.146-.476.13-.218.416-.364.643-.322.23.043.28.256.17.47m.19-2.49c-1.982-.54-4.24.48-5.454 2.11-1.215 1.628-1.018 3.42.404 4.324 1.42 1.005 3.815.884 5.38-.373 1.564-1.257 1.932-3.338.867-4.65-1.065-1.31-3.26-1.65-1.197-1.41m7.013-1.243c-.732-.73-1.938-1.027-2.88-.736-.366.116-.566.5-.444.865.12.365.504.563.87.446.475-.15 1.094.012 1.51.426.414.415.576 1.032.426 1.507-.116.365.082.75.447.87.366.123.75-.076.865-.44.294-.942-.003-2.148-.734-2.88-.42-.418-.937-.71-1.496-.855-.56-.145-.98-.405-1.22-.81-.24-.403-.307-.863-.188-1.29.12-.43.41-.798.817-1.02.41-.22.87-.286 1.3-.166.424.117.87.408 1.21.81.34.404.54.903.56 1.416.02.515-.14 1.027-.46 1.44-.32.412-.77.706-1.28.83-.51.122-1.04.06-1.51-.18-.47-.243-.85-.63-1.07-1.11-.22-.48-.28-1.01-.16-1.52.12-.51.41-.965.83-1.29.41-.324.92-.51 1.45-.53.53-.02 1.05.13 1.48.43.43.3.76.72.94 1.21.18.49.19 1.03.03 1.53-.16.5-.48.93-.92 1.24M11.92 7.226c-4.626-.398-8.655 1.488-9.004 4.216-.35 2.727 3.095 5.297 7.7 5.717 4.605.42 8.674-1.47 9.055-4.195.38-2.724-3.045-5.335-7.632-5.738h-.118z"/>
              </svg>
            </a>
            <a class="social-btn" href="#" aria-label="GitHub">
              <svg class="social-btn-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>

      <!-- 装饰性角落元素 -->
      <div class="footer-corner footer-corner-tl"></div>
      <div class="footer-corner footer-corner-tr"></div>
      <div class="footer-corner footer-corner-bl"></div>
      <div class="footer-corner footer-corner-br"></div>
    </footer>
  </div>
</template>

<style scoped>
/* ========================================
   CSS 变量定义 - 影院霓虹配色方案
   ======================================== */
:root {
  --color-bg-dark: #0a0a12;
  --color-bg-secondary: #12121f;
  --color-amber-gold: #f59e0b;
  --color-amber-gold-light: #fbbf24;
  --color-red-primary: #dc2626;
  --color-red-glow: #ef4444;
  --color-cyan-primary: #06b6d4;
  --color-cyan-glow: #22d3ee;
  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-border-glass: rgba(255, 255, 255, 0.1);
  --gradient-gold: linear-gradient(135deg, #f59e0b, #d97706);
  --gradient-red: linear-gradient(135deg, #dc2626, #b91c1c);
  --gradient-cyan: linear-gradient(135deg, #06b6d4, #0891b2);
}

/* ========================================
   背景效果层
   ======================================== */
.background-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

/* 胶片颗粒纹理 */
.film-grain {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
}

/* 渐变光晕 */
.glow-effects {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  animation: orbFloat 20s ease-in-out infinite;
}

.glow-gold {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.15) 0%, transparent 70%);
  top: -100px;
  right: 10%;
  animation-delay: 0s;
}

.glow-red {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(220, 38, 38, 0.12) 0%, transparent 70%);
  bottom: 10%;
  left: 5%;
  animation-delay: -7s;
}

.glow-cyan {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%);
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
  25% { transform: translate(30px, -20px) scale(1.05); opacity: 1; }
  50% { transform: translate(-20px, 30px) scale(0.95); opacity: 0.6; }
  75% { transform: translate(10px, -10px) scale(1.02); opacity: 0.9; }
}

/* 网格背景 */
.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(245, 158, 11, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(245, 158, 11, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
}

/* ========================================
   头部导航栏
   ======================================== */
header {
  background: transparent;
}

header.header-scrolled {
  background: rgba(10, 10, 18, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color-border-glass);
}

/* 胶片卷轴顶部装饰 */
.film-strip-top {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: repeating-linear-gradient(
    90deg,
    var(--color-amber-gold) 0px,
    var(--color-amber-gold) 20px,
    var(--color-bg-dark) 20px,
    var(--color-bg-dark) 24px
  );
  opacity: 0.6;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 80px;
  gap: 2rem;
}

/* Logo 区域 */
.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo-section:hover {
  transform: scale(1.02);
}

.film-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--gradient-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow:
    0 0 20px rgba(245, 158, 11, 0.3),
    0 4px 12px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
}

.film-icon::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
}

.logo-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 48px;
}

.logo-title {
  font-family: 'Impact', 'Arial Black', sans-serif;
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: 2px;
  line-height: 1;
  background: linear-gradient(135deg, #fff 0%, #f1f5f9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(245, 158, 11, 0.3);
  margin-bottom: 2px;
}

.title-highlight {
  color: var(--color-amber-gold);
  -webkit-text-fill-color: var(--color-amber-gold);
  text-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
}

.logo-subtitle {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-top: 0;
  line-height: 1;
}

/* 桌面端导航 */
.desktop-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border-radius: 10px;
  color: #cbd5e1;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  background: transparent;
  border: 1px solid transparent;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-gold);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-icon {
  width: 18px;
  height: 18px;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.nav-text {
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.nav-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 20px;
  height: 2px;
  background: var(--color-amber-gold);
  transition: transform 0.3s ease;
}

.nav-link:hover {
  color: white;
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.2);
}

.nav-link:hover .nav-indicator {
  transform: translateX(-50%) scaleX(1);
}

.nav-link-active {
  color: white !important;
  background: rgba(245, 158, 11, 0.15) !important;
  border-color: rgba(245, 158, 11, 0.3) !important;
}

.nav-link-active::before {
  opacity: 1;
}

.nav-link-active .nav-indicator {
  transform: translateX(-50%) scaleX(1.5);
  width: 30px;
}

/* 用户区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-dropdown :deep(.el-dropdown) {
  display: flex;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--color-border-glass);
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--gradient-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.avatar-text {
  font-weight: 700;
  font-size: 1rem;
  color: white;
  position: relative;
  z-index: 1;
}

.avatar-ring {
  position: absolute;
  inset: -2px;
  border-radius: 12px;
  background: var(--gradient-gold);
  z-index: 0;
  animation: ringPulse 2s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.2; transform: scale(1.05); }
}

.user-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-primary);
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 自定义下拉菜单 */
:deep(.custom-dropdown) {
  background: rgba(18, 18, 31, 0.95);
  border: 1px solid var(--color-border-glass);
  backdrop-filter: blur(20px);
  padding: 0.5rem;
}

:deep(.custom-dropdown .el-dropdown-menu__item) {
  color: var(--color-text-secondary);
  border-radius: 8px;
  padding: 0.625rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

:deep(.custom-dropdown .el-dropdown-menu__item:hover) {
  background: rgba(245, 158, 11, 0.1);
  color: white;
}

:deep(.custom-dropdown .el-dropdown-menu__item.is-divided) {
  border-top: 1px solid var(--color-border-glass);
  margin-top: 0.25rem;
  padding-top: 0.625rem;
}

.dropdown-icon {
  width: 16px;
  height: 16px;
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border-glass);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-menu-btn:hover {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
}

.hamburger-line {
  width: 20px;
  height: 2px;
  background: var(--color-text-primary);
  border-radius: 1px;
  transition: all 0.3s ease;
}

.mobile-menu-active .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(4px, 4px);
}

.mobile-menu-active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-active .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

/* ========================================
   移动端导航
   ======================================== */
.mobile-nav-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 100;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.mobile-nav-open {
  opacity: 1;
  visibility: visible;
}

.mobile-nav-panel {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 280px;
  background: var(--color-bg-secondary);
  border-left: 1px solid var(--color-border-glass);
  padding: 2rem 1.5rem;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.mobile-nav-open .mobile-nav-panel {
  transform: translateX(0);
}

.mobile-nav-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border-glass);
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mobile-user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--gradient-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
  color: white;
}

.mobile-user-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.mobile-user-role {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  margin-top: 2px;
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 12px;
  color: #cbd5e1;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.mobile-nav-link:hover {
  background: rgba(245, 158, 11, 0.1);
  color: white;
}

.mobile-nav-link-active {
  background: rgba(245, 158, 11, 0.15) !important;
  color: white !important;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.mobile-nav-icon {
  width: 20px;
  height: 20px;
}

/* ========================================
   主内容区
   ======================================== */
.main-content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  padding-top: 80px;
}

/* ========================================
   底部 - 重新设计
   ======================================== */
.footer {
  position: relative;
  z-index: 10;
  margin-top: auto;
  background: linear-gradient(180deg, rgba(10, 10, 18, 0.85) 0%, rgba(5, 5, 12, 0.98) 100%);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-top: 1px solid rgba(245, 158, 11, 0.15);
  overflow: hidden;
}

/* 顶部渐变光晕装饰 */
.footer-glow {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 200px;
  background: radial-gradient(ellipse at top, rgba(245, 158, 11, 0.08) 0%, transparent 60%);
  pointer-events: none;
}

/* 胶片卷轴底部装饰 */
.film-strip-bottom {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: repeating-linear-gradient(
    90deg,
    var(--color-amber-gold) 0px,
    var(--color-amber-gold) 15px,
    transparent 15px,
    transparent 18px
  );
  opacity: 0.5;
}

.footer-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 4rem 2rem 2rem;
  position: relative;
  z-index: 1;
}

/* 底部主内容区 */
.footer-main {
  display: grid;
  grid-template-columns: 1.2fr 1.8fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

/* 品牌区域 */
.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(245, 158, 11, 0.02) 100%);
  border: 1px solid rgba(245, 158, 11, 0.1);
  transition: all 0.4s ease;
}

.brand-logo:hover {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(245, 158, 11, 0.03) 100%);
  border-color: rgba(245, 158, 11, 0.2);
  transform: translateY(-2px);
}

.logo-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--gradient-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow:
    0 4px 20px rgba(245, 158, 11, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.logo-icon-wrapper::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 70%
  );
  animation: logoShine 3s ease-in-out infinite;
}

@keyframes logoShine {
  0% { transform: translateX(-100%) rotate(45deg); }
  100% { transform: translateX(100%) rotate(45deg); }
}

.logo-icon {
  width: 22px;
  height: 22px;
  position: relative;
  z-index: 1;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-family: 'Impact', 'Arial Black', sans-serif;
  font-size: 1.125rem;
  font-weight: 900;
  letter-spacing: 1.5px;
  line-height: 1.2;
  background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-accent {
  color: var(--color-amber-gold);
  -webkit-text-fill-color: var(--color-amber-gold);
  text-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
}

.brand-tagline {
  font-size: 0.6875rem;
  color: #cbd5e1;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 2px;
}

.brand-desc {
  font-size: 0.8125rem;
  line-height: 1.8;
  color: #cbd5e1;
  padding-left: 0.25rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* 联系方式 */
.contact-section {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.8125rem;
  color: #cbd5e1;
  transition: all 0.3s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.contact-item:hover {
  color: var(--color-amber-gold);
  transform: translateX(4px);
}

.contact-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.contact-item:hover .contact-icon {
  opacity: 1;
  color: var(--color-amber-gold);
}

/* 导航区域 */
.footer-nav-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
}

.nav-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-title {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--color-amber-gold);
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(245, 158, 11, 0.15);
  text-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  font-size: 0.8125rem;
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  padding-left: 0.5rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.nav-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #cbd5e1;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.nav-dot-red {
  background: var(--color-red-primary);
}

.nav-item:hover {
  color: white;
  padding-left: 0.75rem;
}

.nav-item:hover .nav-dot {
  background: var(--color-amber-gold);
  width: 8px;
  box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
}

.nav-item:hover .nav-dot-red {
  background: var(--color-red-glow);
  box-shadow: 0 0 8px rgba(220, 38, 38, 0.5);
}

/* 底部版权栏 */
.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.copyright-line {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.copyright-text {
  font-size: 0.75rem;
  color: #94a3b8;
  letter-spacing: 0.5px;
}

.copyright-divider {
  width: 1px;
  height: 14px;
  background: rgba(255, 255, 255, 0.1);
}

.copyright-links {
  display: flex;
  gap: 1rem;
}

.copyright-link {
  font-size: 0.75rem;
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.3s ease;
}

.copyright-link:hover {
  color: var(--color-amber-gold);
}

/* 社交媒体按钮 */
.social-links {
  display: flex;
  gap: 0.5rem;
}

.social-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.social-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--gradient-gold);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.social-btn:hover::before {
  opacity: 1;
}

.social-btn:hover {
  border-color: transparent;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(245, 158, 11, 0.25);
}

.social-btn:hover .social-btn-icon {
  color: white;
}

.social-btn-icon {
  width: 16px;
  height: 16px;
  position: relative;
  z-index: 1;
  transition: color 0.3s ease;
  color: #cbd5e1;
}

/* 装饰性角落元素 */
.footer-corner {
  position: absolute;
  width: 60px;
  height: 60px;
  pointer-events: none;
  opacity: 0.4;
}

/* 装饰性角落元素 */
.footer-corner {
  position: absolute;
  width: 60px;
  height: 60px;
  pointer-events: none;
  opacity: 0.3;
}

.footer-corner::before,
.footer-corner::after {
  content: '';
  position: absolute;
  background: linear-gradient(90deg, transparent, var(--color-amber-gold), transparent);
}

.footer-corner-tl {
  top: 20px;
  left: 20px;
}

.footer-corner-tl::before {
  top: 0;
  left: 0;
  width: 30px;
  height: 1px;
}

.footer-corner-tl::after {
  top: 0;
  left: 0;
  width: 1px;
  height: 30px;
}

.footer-corner-tr {
  top: 20px;
  right: 20px;
}

.footer-corner-tr::before {
  top: 0;
  right: 0;
  width: 30px;
  height: 1px;
}

.footer-corner-tr::after {
  top: 0;
  right: 0;
  width: 1px;
  height: 30px;
}

.footer-corner-bl {
  bottom: 20px;
  left: 20px;
}

.footer-corner-bl::before {
  bottom: 0;
  left: 0;
  width: 30px;
  height: 1px;
}

.footer-corner-bl::after {
  bottom: 0;
  left: 0;
  width: 1px;
  height: 30px;
}

.footer-corner-br {
  bottom: 20px;
  right: 20px;
}

.footer-corner-br::before {
  bottom: 0;
  right: 0;
  width: 30px;
  height: 1px;
}

.footer-corner-br::after {
  bottom: 0;
  right: 0;
  width: 1px;
  height: 30px;
}

/* ========================================
   响应式设计
   ======================================== */
@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .footer-main {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .footer-nav-section {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
}

@media (max-width: 640px) {
  .header-content {
    height: 70px;
  }

  .logo-subtitle {
    display: none;
  }

  .logo-title {
    font-size: 1.25rem;
  }

  .user-name {
    display: none;
  }

  .main-content {
    padding-top: 70px;
  }

  .footer-container {
    padding: 3rem 1.5rem 1.5rem;
  }

  .footer-main {
    gap: 2rem;
  }

  .footer-nav-section {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .copyright-line {
    flex-direction: column;
    gap: 0.5rem;
  }

  .copyright-divider {
    display: none;
  }

  .footer-corner {
    display: none;
  }
}
</style>
