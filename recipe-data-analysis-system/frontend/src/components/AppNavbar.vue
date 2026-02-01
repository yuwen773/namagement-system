<template>
  <nav class="app-navbar" :class="{ 'navbar-scrolled': isScrolled }">
    <div class="navbar-container">
      <!-- Logo -->
      <router-link to="/" class="navbar-logo" @click="handleLogoClick">
        <div class="logo-icon">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 8h24v24H8z" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M8 14h24" stroke="currentColor" stroke-width="2"/>
            <circle cx="14" cy="11" r="1.5" fill="currentColor"/>
            <circle cx="19" cy="11" r="1.5" fill="currentColor"/>
            <path d="M14 24c0-3 6-3 6 0s-6 3-6 0" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <path d="M12 28c2-4 8-4 10 0" stroke="currentColor" stroke-width="1.5" fill="none"/>
          </svg>
        </div>
        <span class="logo-text">食谱分析</span>
      </router-link>

      <!-- 主导航链接 -->
      <div class="nav-links desktop-nav">
        <router-link to="/" class="nav-link" @click="navClick">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>首页</span>
        </router-link>
        <router-link to="/recipes" class="nav-link" @click="navClick">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 4h16v16H4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4 10h16M10 4v16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>菜谱</span>
        </router-link>
        <router-link to="/category" class="nav-link" @click="navClick">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 8h10M5 12h8M5 16h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 2l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 6H8a4 4 0 00-4 4v0a4 4 0 004 4h2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>分类</span>
        </router-link>
        <router-link to="/hot" class="nav-link hot-link" @click="navClick">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2c-2 0-3.5 1.5-4 3.5C7.5 3.5 6 2 4 2 1.5 2 0 4.5 0 7.5c0 4 5 8.5 10 12.5 5-4 10-8.5 10-12.5C20 4.5 18.5 2 16 2c-2 0-3.5 1.5-4 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>热门</span>
        </router-link>
        <router-link to="/analytics" class="nav-link" @click="navClick">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3v16h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M7 12l3-3 2.5 2.5L16 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>数据分析</span>
        </router-link>
        <router-link to="/ingredients-frequency" class="nav-link" @click="navClick">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>食材频率</span>
        </router-link>
                <router-link v-if="userStore.isAdmin" to="/admin/dashboard" class="nav-link admin-link" @click="navClick">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 4a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1v-4zm8-8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V4zm0 8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>管理后台</span>
        </router-link>
      </div>

      <!-- 右侧操作区 -->
      <div class="nav-actions">
        <!-- 搜索按钮 -->
        <button class="nav-icon-btn search-btn" @click="toggleSearch" :class="{ active: searchVisible }">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l-4.5-4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>

        <!-- 用户菜单 -->
        <div v-if="userStore.isLoggedIn" class="user-menu" ref="userMenuRef">
          <button class="nav-user-btn" @click="toggleUserMenu">
            <div class="user-avatar">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 10a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M4 18c0-4 3-6 6-6s6 2 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
            <span class="user-name">{{ userStore.userInfo?.username || '用户' }}</span>
            <svg class="dropdown-arrow" :class="{ active: userMenuOpen }" viewBox="0 0 12 12" fill="none">
              <path d="M3 4l3 3 3-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div class="user-dropdown" :class="{ show: userMenuOpen }">
            <div class="dropdown-header">
              <div class="user-info">
                <span class="user-email">{{ userStore.userInfo?.email || '用户' }}</span>
                <span class="user-role">{{ userStore.isAdmin ? '管理员' : '普通用户' }}</span>
              </div>
            </div>
            <div class="dropdown-divider"></div>
            <router-link to="/profile" class="dropdown-item" @click="userMenuOpen = false">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 10a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M4 18c0-4 3-6 6-6s6 2 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              个人中心
            </router-link>
            <router-link to="/favorites" class="dropdown-item" @click="userMenuOpen = false">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 1.314C12.438-3.248 23.534 4.735 10 15-3.534 4.736 3.562-3.248 10 1.314z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              我的收藏
            </router-link>
            <router-link v-if="userStore.isAdmin" to="/admin/dashboard" class="dropdown-item admin-entry" @click="userMenuOpen = false">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 4a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1H4a1 1 0 01-1-1v-4zm8-8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V4zm0 8a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>管理后台</span>
            </router-link>
            <router-link to="/change-password" class="dropdown-item" @click="userMenuOpen = false">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="11" width="14" height="8" rx="2" stroke="currentColor" stroke-width="1.5"/>
                <path d="M7 11V7a3 3 0 116 0v4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              修改密码
            </router-link>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item logout-item" @click="handleLogout">
              <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              退出登录
            </button>
          </div>
        </div>

        <!-- 登录/注册按钮 -->
        <div v-else class="auth-buttons">
          <router-link to="/login" class="btn-text">登录</router-link>
          <router-link to="/register" class="btn-primary">注册</router-link>
        </div>

        <!-- 移动端菜单按钮 -->
        <button class="mobile-menu-btn" @click="toggleMobileMenu" :class="{ active: mobileMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </div>

    <!-- 搜索栏展开 -->
    <div class="search-bar" :class="{ show: searchVisible }">
      <div class="search-container">
        <input
          ref="searchInput"
          v-model="searchKeyword"
          type="text"
          placeholder="搜索菜谱名称或食材..."
          @keyup.enter="handleSearch"
        >
        <button class="search-btn-submit" @click="handleSearch">
          <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M14 14l-4.5-4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 移动端导航菜单 -->
    <div class="mobile-menu" :class="{ show: mobileMenuOpen }">
      <div class="mobile-menu-content">
        <router-link to="/" class="mobile-nav-link" @click="closeMobileMenu">首页</router-link>
        <router-link to="/recipes" class="mobile-nav-link" @click="closeMobileMenu">菜谱浏览</router-link>
        <router-link to="/category" class="mobile-nav-link" @click="closeMobileMenu">分类浏览</router-link>
        <router-link to="/hot" class="mobile-nav-link hot-mobile" @click="closeMobileMenu">热门菜谱</router-link>
        <router-link to="/analytics" class="mobile-nav-link" @click="closeMobileMenu">数据分析</router-link>
        <router-link to="/ingredients-frequency" class="mobile-nav-link" @click="closeMobileMenu">食材频率</router-link>
        <router-link to="/favorites" class="mobile-nav-link" @click="closeMobileMenu">我的收藏</router-link>
        <div v-if="!userStore.isLoggedIn" class="mobile-auth-section">
          <router-link to="/login" class="mobile-auth-link" @click="closeMobileMenu">登录</router-link>
          <router-link to="/register" class="mobile-auth-link primary" @click="closeMobileMenu">注册</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isScrolled = ref(false)
const searchVisible = ref(false)
const searchKeyword = ref('')
const userMenuOpen = ref(false)
const mobileMenuOpen = ref(false)
const userMenuRef = ref(null)
const searchInput = ref(null)

// 滚动处理
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

// 搜索
const toggleSearch = () => {
  searchVisible.value = !searchVisible.value
  if (searchVisible.value) {
    setTimeout(() => searchInput.value?.focus(), 100)
  }
}

const handleSearch = () => {
  const keyword = searchKeyword.value.trim()
  if (keyword) {
    searchVisible.value = false
    router.push({ name: 'recipe-list', query: { search: keyword } })
  }
}

// 用户菜单
const toggleUserMenu = () => {
  userMenuOpen.value = !userMenuOpen.value
}

const handleLogout = () => {
  userStore.logout()
  userMenuOpen.value = false
  ElMessage.success('已退出登录')
  router.push('/')
}

// 移动端菜单
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  if (mobileMenuOpen.value) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
  document.body.style.overflow = ''
}

const navClick = () => {
  closeMobileMenu()
}

const handleLogoClick = () => {
  closeMobileMenu()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 点击外部关闭用户菜单
const handleClickOutside = (e) => {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    userMenuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('click', handleClickOutside)
  document.body.style.overflow = ''
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ========== 导航栏容器 ========== */
.app-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: transparent;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

.app-navbar.navbar-scrolled {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  box-shadow: 0 2px 20px rgba(61, 41, 20, 0.08);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

/* ========== Logo ========== */
.navbar-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-icon {
  width: 40px;
  height: 40px;
  color: #c2622e;
  transition: transform 0.3s ease;
}

.navbar-logo:hover .logo-icon {
  transform: rotate(-10deg);
}

.logo-text {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #3d2914;
  letter-spacing: 0.02em;
}

/* ========== 导航链接 ========== */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  text-decoration: none;
  color: #6b5c4d;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 10px;
  transition: all 0.2s ease;
  position: relative;
}

.nav-link svg {
  width: 18px;
  height: 18px;
}

.nav-link:hover {
  color: #c2622e;
  background: rgba(194, 98, 46, 0.08);
}

.nav-link.router-link-active {
  color: #c2622e;
  font-weight: 600;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-radius: 2px;
}

.hot-link {
  color: #ff6b35;
}

.hot-link:hover {
  color: #e55a2b;
  background: rgba(255, 107, 53, 0.1);
}

.hot-link.router-link-active::after {
  background: linear-gradient(135deg, #ff8c5a 0%, #ff6b35 100%);
}

/* ========== 管理员入口 ========== */
.admin-link {
  background: linear-gradient(135deg, rgba(194, 98, 46, 0.12) 0%, rgba(194, 98, 46, 0.08) 100%);
  color: #c2622e;
  font-weight: 600;
}

.admin-link:hover {
  background: linear-gradient(135deg, rgba(194, 98, 46, 0.18) 0%, rgba(194, 98, 46, 0.12) 100%);
  color: #a35220;
}

.admin-link.router-link-active {
  color: #a35220;
}

.admin-link.router-link-active::after {
  background: linear-gradient(135deg, #c2622e 0%, #a35220 100%);
}

/* 下拉菜单中的管理员入口 */
.dropdown-item.admin-entry {
  background: linear-gradient(135deg, rgba(194, 98, 46, 0.1) 0%, rgba(194, 98, 46, 0.05) 100%);
  color: #c2622e;
  font-weight: 500;
}

.dropdown-item.admin-entry:hover {
  background: linear-gradient(135deg, rgba(194, 98, 46, 0.15) 0%, rgba(194, 98, 46, 0.1) 100%);
  color: #a35220;
}

.dropdown-item.admin-entry svg {
  color: #c2622e;
}

.dropdown-item.admin-entry:hover svg {
  color: #a35220;
}

/* ========== 右侧操作区 ========== */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

/* 图标按钮 */
.nav-icon-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #6b5c4d;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-icon-btn svg {
  width: 20px;
  height: 20px;
}

.nav-icon-btn:hover {
  color: #c2622e;
  background: rgba(194, 98, 46, 0.08);
}

.nav-icon-btn.active {
  color: #c2622e;
  background: rgba(194, 98, 46, 0.12);
}

/* ========== 用户菜单 ========== */
.user-menu {
  position: relative;
}

.nav-user-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.75rem 0.4rem 0.4rem;
  background: rgba(194, 98, 46, 0.08);
  border: none;
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-user-btn:hover {
  background: rgba(194, 98, 46, 0.12);
}

.user-avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-radius: 50%;
  color: white;
}

.user-avatar svg {
  width: 16px;
  height: 16px;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 500;
  color: #3d2914;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-arrow {
  width: 14px;
  height: 14px;
  color: #8b7355;
  transition: transform 0.2s ease;
}

.dropdown-arrow.active {
  transform: rotate(180deg);
}

/* 用户下拉菜单 */
.user-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 200px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(61, 41, 20, 0.12);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  overflow: hidden;
}

.user-dropdown.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-header {
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(212, 119, 58, 0.08) 0%, rgba(194, 98, 46, 0.08) 100%);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.user-email {
  font-weight: 600;
  color: #3d2914;
  font-size: 0.95rem;
}

.user-role {
  font-size: 0.8rem;
  color: #8b7355;
}

.dropdown-divider {
  height: 1px;
  background: #f0ebe3;
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.85rem 1.25rem;
  background: none;
  border: none;
  color: #6b5c4d;
  font-size: 0.9rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dropdown-item svg {
  width: 18px;
  height: 18px;
  color: #a89078;
}

.dropdown-item:hover {
  background: rgba(194, 98, 46, 0.05);
  color: #c2622e;
}

.dropdown-item:hover svg {
  color: #c2622e;
}

.logout-item {
  color: #e74c3c;
}

.logout-item svg {
  color: #e74c3c;
}

.logout-item:hover {
  background: rgba(231, 76, 60, 0.08);
  color: #c0392b;
}

.logout-item:hover svg {
  color: #c0392b;
}

/* ========== 登录/注册按钮 ========== */
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-text {
  padding: 0.5rem 1rem;
  color: #6b5c4d;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

.btn-text:hover {
  color: #c2622e;
}

.btn-primary {
  padding: 0.5rem 1.25rem;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 20px;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(194, 98, 46, 0.35);
}

/* ========== 移动端菜单按钮 ========== */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}

.mobile-menu-btn span {
  display: block;
  width: 20px;
  height: 2px;
  background: #6b5c4d;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.mobile-menu-btn.active span:nth-child(1) {
  transform: translateY(6px) rotate(45deg);
}

.mobile-menu-btn.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active span:nth-child(3) {
  transform: translateY(-6px) rotate(-45deg);
}

/* ========== 搜索栏 ========== */
.search-bar {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  height: 0;
  overflow: hidden;
  background: white;
  transition: height 0.3s ease;
  border-bottom: 1px solid transparent;
}

.search-bar.show {
  height: 70px;
  border-bottom-color: #f0ebe3;
}

.search-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 100%;
  display: flex;
  align-items: center;
}

.search-container input {
  flex: 1;
  height: 44px;
  padding: 0 1rem;
  border: 1.5px solid #e5ddd3;
  border-radius: 12px 0 0 12px;
  font-size: 0.95rem;
  font-family: inherit;
  color: #3d2914;
  outline: none;
  transition: border-color 0.2s ease;
}

.search-container input:focus {
  border-color: #c2622e;
}

.search-container input::placeholder {
  color: #b8a99a;
}

.search-btn-submit {
  width: 50px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border: none;
  border-radius: 0 12px 12px 0;
  cursor: pointer;
  color: white;
}

.search-btn-submit svg {
  width: 18px;
  height: 18px;
}

/* ========== 移动端菜单 ========== */
.mobile-menu {
  position: fixed;
  top: 72px;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.mobile-menu.show {
  transform: translateX(0);
}

.mobile-menu-content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav-link {
  display: block;
  padding: 1rem;
  color: #3d2914;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  background: rgba(194, 98, 46, 0.08);
  color: #c2622e;
}

.hot-mobile {
  color: #ff6b35;
}

.hot-mobile:hover,
.hot-mobile.router-link-active {
  background: rgba(255, 107, 53, 0.1);
  color: #e55a2b;
}

.mobile-auth-section {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f0ebe3;
}

.mobile-auth-link {
  flex: 1;
  padding: 0.85rem;
  text-align: center;
  color: #6b5c4d;
  text-decoration: none;
  font-weight: 500;
  border-radius: 12px;
  border: 1.5px solid #e5ddd3;
  transition: all 0.2s ease;
}

.mobile-auth-link.primary {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  color: white;
  border-color: transparent;
}

/* ========== 响应式设计 ========== */
@media (max-width: 968px) {
  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .user-name {
    display: none;
  }

  .auth-buttons {
    display: none;
  }

  .search-bar {
    position: fixed;
    top: 72px;
    left: 0;
    right: 0;
    z-index: 999;
  }
}

@media (max-width: 640px) {
  .navbar-container {
    padding: 0.75rem 1rem;
  }

  .logo-text {
    font-size: 1rem;
  }

  .logo-icon {
    width: 36px;
    height: 36px;
  }
}

/* ========== 动画 ========== */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.navbar-scrolled .navbar-container {
  animation: slideDown 0.3s ease;
}
</style>
