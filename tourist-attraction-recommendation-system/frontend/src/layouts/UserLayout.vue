<template>
  <div class="user-layout">
    <!-- Header -->
    <header class="header" :class="{ 'header--scrolled': isScrolled }">
      <div class="header__background"></div>
      <div class="header__container">
        <!-- Logo -->
        <router-link to="/" class="header__logo">
          <div class="logo-icon">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="2.5" stroke-dasharray="4 2"/>
              <path d="M24 8C24 8 32 18 32 24C32 30.6274 26.6274 36 20 36C13.3726 36 8 30.6274 8 24C8 18 16 8 16 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
              <circle cx="24" cy="24" r="4" fill="currentColor"/>
              <path d="M24 36V44" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M18 42H30" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="logo-text">
            <span class="logo-text__brand">旅途拾光</span>
            <span class="logo-text__tagline">发现世界之美</span>
          </div>
        </router-link>

        <!-- Navigation -->
        <nav class="header__nav">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ 'nav-link--active': $route.path === item.path || (item.path !== '/' && $route.path.startsWith(item.path)) }"
          >
            <span class="nav-link__text">{{ item.label }}</span>
            <span class="nav-link__underline"></span>
          </router-link>
        </nav>

        <!-- User Actions -->
        <div class="header__actions">
          <!-- 管理员入口按钮 -->
          <router-link v-if="userStore.isAdmin" to="/admin" class="admin-entry-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"/>
              <rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/>
              <rect x="3" y="14" width="7" height="7"/>
            </svg>
            <span>管理后台</span>
          </router-link>
          <template v-if="userStore.isLoggedIn">
            <el-dropdown trigger="click" @command="handleCommand" placement="bottom-end" :show-arrow="false">
              <div class="user-menu">
                <div class="user-avatar">
                  {{ userStore.user?.real_name?.charAt(0) || userStore.user?.realName?.charAt(0) || 'U' }}
                </div>
                <span class="user-name">{{ userStore.user?.real_name || userStore.user?.realName || '用户' }}</span>
                <svg class="user-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </div>
              <template #dropdown>
                <el-dropdown-menu class="user-dropdown">
                  <el-dropdown-item command="usercenter">
                    <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                    个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="favorites">
                    <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                    </svg>
                    我的收藏
                  </el-dropdown-item>
                  <el-dropdown-item command="comments">
                    <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                    我的评论
                  </el-dropdown-item>
                  <el-dropdown-item command="notifications">
                    <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                      <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                    </svg>
                    消息中心
                  </el-dropdown-item>
                  <!-- 管理员入口 -->
                  <el-dropdown-item v-if="userStore.isAdmin" divided command="admin">
                    <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="7" height="7"/>
                      <rect x="14" y="3" width="7" height="7"/>
                      <rect x="14" y="14" width="7" height="7"/>
                      <rect x="3" y="14" width="7" height="7"/>
                    </svg>
                    进入管理后台
                  </el-dropdown-item>
                  <el-dropdown-item :divided="!userStore.isAdmin" command="logout">
                    <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                      <polyline points="16 17 21 12 16 7"/>
                      <line x1="21" y1="12" x2="9" y2="12"/>
                    </svg>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <router-link to="/login" class="action-btn action-btn--ghost">
              登录
            </router-link>
            <router-link to="/register" class="action-btn action-btn--primary">
              开始探索
            </router-link>
          </template>
        </div>

        <!-- Mobile Menu Toggle -->
        <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
          <span :class="{ 'active': mobileMenuOpen }"></span>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div class="mobile-menu" :class="{ 'mobile-menu--open': mobileMenuOpen }">
        <nav class="mobile-nav">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="mobile-nav__link"
            @click="mobileMenuOpen = false"
          >
            {{ item.label }}
          </router-link>
        </nav>
        <div class="mobile-actions" v-if="!userStore.isLoggedIn">
          <router-link to="/login" class="action-btn action-btn--ghost" @click="mobileMenuOpen = false">登录</router-link>
          <router-link to="/register" class="action-btn action-btn--primary" @click="mobileMenuOpen = false">注册</router-link>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
      <!-- Wave Decoration -->
      <div class="footer__wave">
        <svg viewBox="0 0 1440 120" preserveAspectRatio="none">
          <path d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,64C960,75,1056,85,1152,80C1248,75,1344,53,1392,42.7L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z" fill="currentColor"/>
        </svg>
      </div>

      <div class="footer__container">
        <div class="footer__grid">
          <!-- Brand Column -->
          <div class="footer__brand">
            <div class="footer-logo">
              <div class="logo-icon logo-icon--light">
                <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="2.5" stroke-dasharray="4 2"/>
                  <path d="M24 8C24 8 32 18 32 24C32 30.6274 26.6274 36 20 36C13.3726 36 8 30.6274 8 24C8 18 16 8 16 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                  <circle cx="24" cy="24" r="4" fill="currentColor"/>
                </svg>
              </div>
              <span class="footer-logo__text">旅途拾光</span>
            </div>
            <p class="footer__description">
              探索世界的每一个角落，发现旅途中的精彩瞬间。我们致力于为您提供最优质的旅游景点推荐服务。
            </p>
            <div class="footer__social">
              <a href="#" class="social-link" title="微信">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12c0 2.17.7 4.19 1.89 5.83L2 22l4.17-1.89C7.81 21.3 9.83 22 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm-2 13H8v-2h2v2zm0-4H8V9h2v2zm4 4h-2v-2h2v2zm0-4h-2V9h2v2z"/>
                </svg>
              </a>
              <a href="#" class="social-link" title="微博">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-9 13H6v-2h5v2zm7-4H6v-2h12v2zm0-4H6V7h12v2z"/>
                </svg>
              </a>
              <a href="#" class="social-link" title="小红书">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14h-2v-6H8l4-4 4 4h-2v6z"/>
                </svg>
              </a>
              <a href="#" class="social-link" title="抖音">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .37z"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Quick Links -->
          <div class="footer__column">
            <h4 class="footer__title">快速链接</h4>
            <ul class="footer__links">
              <li><router-link to="/">首页</router-link></li>
              <li><router-link to="/attractions">景点列表</router-link></li>
              <li><router-link to="/usercenter">个人中心</router-link></li>
              <li><router-link to="/favorites">我的收藏</router-link></li>
            </ul>
          </div>

          <!-- Services -->
          <div class="footer__column">
            <h4 class="footer__title">服务支持</h4>
            <ul class="footer__links">
              <li><a href="#">帮助中心</a></li>
              <li><a href="#">用户协议</a></li>
              <li><a href="#">隐私政策</a></li>
              <li><a href="#">意见反馈</a></li>
            </ul>
          </div>

          <!-- Contact -->
          <div class="footer__column">
            <h4 class="footer__title">联系我们</h4>
            <ul class="footer__contact">
              <li>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/>
                </svg>
                <span>400-888-8888</span>
              </li>
              <li>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                <span>contact@travel.com</span>
              </li>
              <li>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <span>北京市朝阳区建国路88号</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Bottom Bar -->
        <div class="footer__bottom">
          <div class="footer__copyright">
            <p>&copy; 2026 旅途拾光 - 旅游景点推荐系统. All rights reserved.</p>
          </div>
          <div class="footer__legal">
            <a href="#">服务条款</a>
            <span class="divider">|</span>
            <a href="#">隐私政策</a>
            <span class="divider">|</span>
            <a href="#">京ICP备xxxxxxxx号</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const router = useRouter()

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const navItems = [
  { path: '/', label: '首页' },
  { path: '/attractions', label: '景点探索' }
]

function handleScroll() {
  isScrolled.value = window.scrollY > 20
}

function handleCommand(command) {
  mobileMenuOpen.value = false
  switch (command) {
    case 'usercenter':
      router.push('/usercenter')
      break
    case 'favorites':
      router.push('/favorites')
      break
    case 'comments':
      router.push('/comments')
      break
    case 'notifications':
      router.push('/notifications')
      break
    case 'admin':
      router.push('/admin')
      break
    case 'logout':
      ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        userStore.logout()
        router.push('/')
      })
      break
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Noto+Sans+SC:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* CSS Variables */
.user-layout {
  --color-primary: #0d9488;
  --color-primary-dark: #0f766e;
  --color-primary-light: #14b8a6;
  --color-accent: #f97316;
  --color-accent-light: #fb923c;
  --color-bg: #faf9f7;
  --color-bg-card: #ffffff;
  --color-text: #1f2937;
  --color-text-light: #6b7280;
  --color-text-lighter: #9ca3af;
  --color-border: #e5e7eb;
  --font-display: 'Playfair Display', 'Noto Sans SC', serif;
  --font-body: 'DM Sans', 'Noto Sans SC', sans-serif;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;

  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
  font-family: var(--font-body);
}

/* ==================== Header ==================== */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

.header__background {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.header--scrolled .header__background {
  opacity: 1;
  box-shadow: var(--shadow-sm);
}

.header__container {
  position: relative;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo */
.header__logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.header__logo:hover {
  transform: translateY(-2px);
}

.logo-icon {
  width: 44px;
  height: 44px;
  color: var(--color-primary);
  transition: transform 0.4s ease;
}

.header__logo:hover .logo-icon {
  transform: rotate(15deg);
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-text__brand {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: 0.02em;
  line-height: 1.1;
}

.logo-text__tagline {
  font-size: 0.7rem;
  color: var(--color-text-light);
  letter-spacing: 0.1em;
  margin-top: 2px;
}

/* Navigation */
.header__nav {
  display: flex;
  align-items: center;
  gap: 2.5rem;
}

.nav-link {
  position: relative;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--color-text);
  padding: 8px 0;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: var(--color-primary);
}

.nav-link__text {
  position: relative;
  z-index: 1;
}

.nav-link__underline {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  border-radius: 2px;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.nav-link:hover .nav-link__underline,
.nav-link--active .nav-link__underline {
  transform: scaleX(1);
  transform-origin: left;
}

.nav-link--active {
  color: var(--color-primary);
}

/* Actions */
.header__actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.6rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: var(--radius-sm);
  text-decoration: none;
  transition: all 0.3s ease;
}

.action-btn--ghost {
  color: var(--color-text);
  background: transparent;
}

.action-btn--ghost:hover {
  color: var(--color-primary);
  background: rgba(13, 148, 136, 0.08);
}

.action-btn--primary {
  color: white;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.35);
}

.action-btn--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(13, 148, 136, 0.45);
}

/* Admin Entry Button */
.admin-entry-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: var(--radius-sm);
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.admin-entry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.admin-entry-btn svg {
  width: 16px;
  height: 16px;
}

/* User Menu */
.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px 6px 6px;
  background: var(--color-bg-card);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.user-menu:hover {
  box-shadow: var(--shadow-md);
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  border-radius: 50%;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text);
}

.user-arrow {
  width: 16px;
  height: 16px;
  color: var(--color-text-light);
  transition: transform 0.3s ease;
}

.user-menu:hover .user-arrow {
  transform: rotate(180deg);
}

/* Mobile Toggle */
.mobile-toggle {
  display: none;
  width: 32px;
  height: 32px;
  position: relative;
  background: transparent;
  border: none;
  cursor: pointer;
}

.mobile-toggle span,
.mobile-toggle span::before,
.mobile-toggle span::after {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-text);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.mobile-toggle span {
  position: relative;
}

.mobile-toggle span::before,
.mobile-toggle span::after {
  content: '';
  position: absolute;
  left: 0;
}

.mobile-toggle span::before {
  top: -8px;
}

.mobile-toggle span::after {
  top: 8px;
}

.mobile-toggle span.active {
  background: transparent;
}

.mobile-toggle span.active::before {
  top: 0;
  transform: rotate(45deg);
}

.mobile-toggle span.active::after {
  top: 0;
  transform: rotate(-45deg);
}

/* Mobile Menu */
.mobile-menu {
  display: none;
  position: fixed;
  top: 80px;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  padding: 1.5rem;
  transform: translateY(-100%);
  opacity: 0;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-lg);
}

.mobile-menu--open {
  transform: translateY(0);
  opacity: 1;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav__link {
  display: block;
  padding: 1rem;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-text);
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.mobile-nav__link:hover {
  background: rgba(13, 148, 136, 0.08);
  color: var(--color-primary);
}

.mobile-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.mobile-actions .action-btn {
  flex: 1;
  padding: 1rem;
}

/* ==================== Main Content ==================== */
.main-content {
  flex: 1;
  margin-top: 80px;
}

/* ==================== Footer ==================== */
.footer {
  position: relative;
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
  color: white;
  margin-top: auto;
}

.footer__wave {
  position: absolute;
  top: -1px;
  left: 0;
  right: 0;
  height: 80px;
  color: var(--color-bg);
  overflow: hidden;
}

.footer__wave svg {
  width: 100%;
  height: 100%;
}

.footer__container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 6rem 2rem 2rem;
}

.footer__grid {
  display: grid;
  grid-template-columns: 1.8fr 1fr 1fr 1.2fr;
  gap: 3rem;
}

/* Footer Brand */
.footer__brand {
  max-width: 320px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1.5rem;
}

.footer-logo .logo-icon--light {
  width: 40px;
  height: 40px;
  color: var(--color-primary-light);
}

.footer-logo__text {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
}

.footer__description {
  font-size: 0.9rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 1.5rem;
}

.footer__social {
  display: flex;
  gap: 0.75rem;
}

.social-link {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
}

.social-link:hover {
  background: var(--color-primary);
  color: white;
  transform: translateY(-3px);
}

.social-link svg {
  width: 18px;
  height: 18px;
}

/* Footer Columns */
.footer__column {
  padding-top: 0.5rem;
}

.footer__title {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1.5rem;
  letter-spacing: 0.02em;
}

.footer__links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer__links li {
  margin-bottom: 0.75rem;
}

.footer__links a {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  display: inline-block;
}

.footer__links a:hover {
  color: var(--color-primary-light);
  transform: translateX(4px);
}

/* Footer Contact */
.footer__contact {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer__contact li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.footer__contact svg {
  width: 18px;
  height: 18px;
  color: var(--color-primary-light);
  flex-shrink: 0;
  margin-top: 2px;
}

/* Footer Bottom */
.footer__bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  margin-top: 3rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer__copyright p {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

.footer__legal {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.footer__legal a {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer__legal a:hover {
  color: var(--color-primary-light);
}

.footer__legal .divider {
  color: rgba(255, 255, 255, 0.2);
}

/* Dropdown Menu Styles */
:deep(.user-dropdown) {
  padding: 8px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-lg);
  min-width: 180px;
}

:deep(.user-dropdown .el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  color: var(--color-text);
  transition: all 0.2s ease;
}

:deep(.user-dropdown .el-dropdown-menu__item:hover) {
  background: rgba(13, 148, 136, 0.08);
  color: var(--color-primary);
}

.dropdown-icon {
  width: 18px;
  height: 18px;
  color: var(--color-text-light);
}

:deep(.user-dropdown .el-dropdown-menu__item:hover .dropdown-icon) {
  color: var(--color-primary);
}

/* ==================== Responsive ==================== */
@media (max-width: 1024px) {
  .header__nav {
    display: none;
  }

  .header__actions {
    display: none;
  }

  .mobile-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .mobile-menu {
    display: block;
  }

  .footer__grid {
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }

  .footer__brand {
    grid-column: span 2;
    max-width: 100%;
  }
}

@media (max-width: 640px) {
  .header__container {
    padding: 0 1rem;
    height: 70px;
  }

  .logo-text__brand {
    font-size: 1.25rem;
  }

  .logo-text__tagline {
    display: none;
  }

  .main-content {
    margin-top: 70px;
  }

  .mobile-menu {
    top: 70px;
  }

  .footer__container {
    padding: 4rem 1rem 1.5rem;
  }

  .footer__grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .footer__brand {
    grid-column: span 1;
    text-align: center;
  }

  .footer__social {
    justify-content: center;
  }

  .footer__bottom {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .footer__legal {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
