<template>
  <div id="app" class="app-container">
    <!-- 导航栏 -->
    <AppNavbar v-if="showNavbar" />

    <!-- 主内容区 -->
    <main class="app-main" :class="{ 'with-navbar': showNavbar }">
      <router-view />
    </main>

    <!-- 页脚 -->
    <footer v-if="showFooter" class="app-footer">
      <div class="footer-content">
        <div class="footer-section">
          <div class="footer-logo">
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
            <span class="footer-logo-text">食谱分析</span>
          </div>
          <p class="footer-desc">探索美食，品味生活。20,000+ 精选菜谱，数据驱动的美食发现之旅。</p>
        </div>

        <div class="footer-section">
          <h4 class="footer-title">探索</h4>
          <router-link to="/recipes" class="footer-link">菜谱浏览</router-link>
          <router-link to="/category/cuisine" class="footer-link">菜系分类</router-link>
          <router-link to="/hot" class="footer-link">热门菜谱</router-link>
        </div>

        <div class="footer-section">
          <h4 class="footer-title">账户</h4>
          <router-link v-if="userStore.isLoggedIn" to="/profile" class="footer-link">个人中心</router-link>
          <router-link v-else to="/login" class="footer-link">登录</router-link>
          <router-link v-if="userStore.isLoggedIn" to="/change-password" class="footer-link">修改密码</router-link>
          <router-link v-else to="/register" class="footer-link">注册</router-link>
        </div>

        <div class="footer-section">
          <h4 class="footer-title">关于</h4>
          <a href="#" class="footer-link">关于我们</a>
          <a href="#" class="footer-link">使用条款</a>
          <a href="#" class="footer-link">隐私政策</a>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© 2026 Recipe Analysis. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppNavbar from '@/components/AppNavbar.vue'

const route = useRoute()
const userStore = useUserStore()

// 登录/注册页面不显示导航栏和页脚
const showNavbar = computed(() => {
  return !['login', 'register'].includes(route.name?.toLowerCase())
})

const showFooter = computed(() => {
  return !['login', 'register'].includes(route.name?.toLowerCase())
})
</script>

<style>
/* ========== 全局样式 ========== */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {
  height: 100%;
  overflow-x: hidden;
}

body {
  font-family: 'DM Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  min-height: calc(100vh - 72px);
}

.app-main.with-navbar {
  padding-top: 72px;
}

/* ========== 页脚样式 ========== */
.app-footer {
  background: #3d2914;
  color: #f5f0e8;
  padding: 3rem 0 1rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.footer-logo .logo-icon {
  width: 36px;
  height: 36px;
  color: #d4773a;
}

.footer-logo-text {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #f5f0e8;
}

.footer-desc {
  color: #b8a99a;
  font-size: 0.9rem;
  line-height: 1.6;
  max-width: 250px;
}

.footer-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 1rem;
  font-weight: 600;
  color: #f5f0e8;
  margin-bottom: 0.5rem;
}

.footer-link {
  color: #b8a99a;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: #d4773a;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 2rem 0;
  border-top: 1px solid rgba(245, 240, 232, 0.1);
  text-align: center;
}

.footer-bottom p {
  color: #8b7355;
  font-size: 0.85rem;
}

/* ========== 滚动条样式 ========== */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #faf8f5;
}

::-webkit-scrollbar-thumb {
  background: #d4c4b0;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #c2622e;
}

/* ========== Element Plus 样式覆盖 ========== */
:root {
  --el-color-primary: #c2622e;
  --el-color-primary-light-3: #d4773a;
  --el-color-primary-light-5: #e5a57c;
  --el-color-primary-light-7: #f2d4c0;
  --el-color-primary-light-8: #f8ede4;
  --el-color-primary-light-9: #fcf6f1;
  --el-color-primary-dark-2: #a35220;
}

.el-message {
  --el-message-bg-color: rgba(61, 41, 20, 0.95);
  --el-message-text-color: #f5f0e8;
  border: none;
  backdrop-filter: blur(12px);
}

.el-message--success {
  --el-message-bg-color: rgba(52, 168, 83, 0.95);
}

.el-message--warning {
  --el-message-bg-color: rgba(240, 173, 78, 0.95);
}

.el-message--error {
  --el-message-bg-color: rgba(217, 83, 79, 0.95);
}

/* ========== 响应式设计 ========== */
@media (max-width: 968px) {
  .footer-content {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .app-main.with-navbar {
    padding-top: 72px;
  }
}
</style>
