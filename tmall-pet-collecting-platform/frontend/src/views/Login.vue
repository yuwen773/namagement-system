<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, UserFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api'

const router = useRouter()
const userStore = useUserStore()

const isLogin = ref(true)
const loading = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: '',
  email: '',
  confirmPassword: ''
})

const activeTab = computed(() => isLogin.value ? 'login' : 'register')

const switchTab = (tab) => {
  isLogin.value = tab === 'login'
}

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    const res = await authApi.login(loginForm.value)
    userStore.setToken(res.data.access_token)
    userStore.setRefreshToken(res.data.refresh_token)
    userStore.setUserInfo(res.data.user)
    ElMessage.success('登录成功')

    if (res.data.user.role === 'admin') {
      router.push('/admin/dashboard')
    } else {
      router.push('/user/market')
    }
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!registerForm.value.username || !registerForm.value.password || !registerForm.value.email) {
    ElMessage.warning('请填写所有必填项')
    return
  }

  if (!validateEmail(registerForm.value.email)) {
    ElMessage.warning('请输入有效的邮箱地址')
    return
  }

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    ElMessage.warning('两次密码输入不一致')
    return
  }

  if (registerForm.value.password.length < 6) {
    ElMessage.warning('密码长度至少为6位')
    return
  }

  loading.value = true
  try {
    await authApi.register({
      username: registerForm.value.username,
      password: registerForm.value.password,
      email: registerForm.value.email
    })
    ElMessage.success('注册成功，请登录')
    isLogin.value = true
    loginForm.value.username = registerForm.value.username
  } catch (error) {
    console.error('注册失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <!-- 自然背景层 -->
    <div class="nature-background">
      <!-- 纸张纹理叠加 -->
      <div class="paper-texture"></div>

      <!-- 渐变光晕 -->
      <div class="ambient-glow glow-green-1"></div>
      <div class="ambient-glow glow-green-2"></div>
      <div class="ambient-glow glow-blue-1"></div>

      <!-- 漂浮叶片装饰 -->
      <div class="floating-leaf leaf-1">
        <svg viewBox="0 0 60 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M30 5C30 5 55 20 55 45C55 65 45 75 30 75C15 75 5 65 5 45C5 20 30 5 30 5Z" fill="url(#leafGrad1)" opacity="0.15"/>
          <path d="M30 5L30 75" stroke="url(#leafGrad1)" stroke-width="1" opacity="0.3"/>
          <defs>
            <linearGradient id="leafGrad1" x1="30" y1="5" x2="30" y2="75">
              <stop offset="0%" stop-color="#52B788"/>
              <stop offset="100%" stop-color="#2D6A4F"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <div class="floating-leaf leaf-2">
        <svg viewBox="0 0 60 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M30 5C30 5 55 20 55 45C55 65 45 75 30 75C15 75 5 65 5 45C5 20 30 5 30 5Z" fill="url(#leafGrad2)" opacity="0.12"/>
          <defs>
            <linearGradient id="leafGrad2" x1="30" y1="5" x2="30" y2="75">
              <stop offset="0%" stop-color="#90E0EF"/>
              <stop offset="100%" stop-color="#00B4D8"/>
            </linearGradient>
          </defs>
        </svg>
      </div>
      <div class="floating-leaf leaf-3">
        <svg viewBox="0 0 40 60" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 5C20 5 35 15 35 30C35 45 30 55 20 55C10 55 5 45 5 30C5 15 20 5 20 5Z" fill="url(#leafGrad3)" opacity="0.1"/>
          <defs>
            <linearGradient id="leafGrad3" x1="20" y1="5" x2="20" y2="55">
              <stop offset="0%" stop-color="#74C69D"/>
              <stop offset="100%" stop-color="#40916C"/>
            </linearGradient>
          </defs>
        </svg>
      </div>

      <!-- 网格图案 -->
      <svg class="grid-pattern" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="leafGrid" x="0" y="0" width="50" height="50" patternUnits="userSpaceOnUse">
            <circle cx="25" cy="25" r="8" fill="none" stroke="rgba(45, 106, 79, 0.03)" stroke-width="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#leafGrid)"/>
      </svg>
    </div>

    <!-- 主内容 -->
    <div class="content-wrapper">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <div class="brand-content">
          <!-- 自然风格 Logo -->
          <div class="brand-logo">
            <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- 背景圆 -->
              <circle cx="40" cy="40" r="38" fill="url(#logoBg)" fill-opacity="0.1"/>
              <circle cx="40" cy="40" r="38" stroke="url(#logoBorder)" stroke-width="2"/>

              <!-- 叶片图标 -->
              <g transform="translate(40, 40)">
                <!-- 主叶 -->
                <path d="M0 -20C0 -20 16 -8 16 8C16 20 10 24 0 24C-10 24 -16 20 -16 8C-16 -8 0 -20 0 -20Z" fill="url(#leafMain)"/>
                <!-- 叶脉 -->
                <path d="M0 -20L0 24" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
                <path d="M0 -8L8 4" stroke="white" stroke-width="1" stroke-linecap="round" opacity="0.3"/>
                <path d="M0 0L-8 10" stroke="white" stroke-width="1" stroke-linecap="round" opacity="0.3"/>
                <path d="M0 8L6 16" stroke="white" stroke-width="1" stroke-linecap="round" opacity="0.3"/>
                <!-- 小叶片 -->
                <circle cx="0" cy="-20" r="4" fill="#52B788"/>
              </g>

              <defs>
                <linearGradient id="logoBg" x1="0" y1="0" x2="80" y2="80">
                  <stop offset="0%" stop-color="#52B788"/>
                  <stop offset="100%" stop-color="#2D6A4F"/>
                </linearGradient>
                <linearGradient id="logoBorder" x1="0" y1="0" x2="80" y2="80">
                  <stop offset="0%" stop-color="#52B788"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="leafMain" x1="-16" y1="-20" x2="16" y2="24">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="50%" stop-color="#52B788"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
              </defs>
            </svg>
          </div>

          <h1 class="brand-title">宠物用品数据平台</h1>
          <p class="brand-tagline">像呵护植物一样，洞察每一份数据</p>

          <!-- 特性卡片 -->
          <div class="brand-features">
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                  <path d="M11 2L3 8V15C3 17.2 4.8 19 7 19H15C17.2 19 19 17.2 19 15V8L11 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M11 10V16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M8 13H14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>
              <div>
                <span class="feature-title">智能采集</span>
                <span class="feature-desc">自动抓取天猫数据</span>
              </div>
            </div>

            <div class="feature-card">
              <div class="feature-icon">
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                  <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M11 7V11L14 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>
              <div>
                <span class="feature-title">实时分析</span>
                <span class="feature-desc">数据可视化展示</span>
              </div>
            </div>

            <div class="feature-card">
              <div class="feature-icon">
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
                  <path d="M3 11L8 6L13 11L19 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M3 17L8 12L13 17L19 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>
                </svg>
              </div>
              <div>
                <span class="feature-title">趋势洞察</span>
                <span class="feature-desc">市场动态及时掌握</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 装饰数字 -->
        <div class="deco-number">01</div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="auth-section">
        <div class="auth-card">
          <!-- 卡片顶部装饰 -->
          <div class="card-decoration">
            <div class="deco-line deco-leaf-1"></div>
            <div class="deco-line deco-leaf-2"></div>
            <div class="deco-line deco-leaf-3"></div>
          </div>

          <!-- 卡片头部 -->
          <div class="card-header">
            <div class="header-icon">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="14" fill="url(#headerIconGrad)" fill-opacity="0.15"/>
                <path d="M16 6C16 6 22 10 22 16C22 22 18 24 16 24C14 24 10 22 10 16C10 10 16 6 16 6Z" fill="url(#headerIconGrad)"/>
                <defs>
                  <linearGradient id="headerIconGrad" x1="10" y1="6" x2="22" y2="24">
                    <stop offset="0%" stop-color="#74C69D"/>
                    <stop offset="100%" stop-color="#40916C"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div>
              <h2 class="card-title">{{ isLogin ? '欢迎回来' : '创建账户' }}</h2>
              <p class="card-subtitle">{{ isLogin ? '登录以继续探索数据世界' : '开启您的数据洞察之旅' }}</p>
            </div>
          </div>

          <!-- Tab 切换 -->
          <div class="tab-switcher">
            <button
              :class="['tab-btn', { active: isLogin }]"
              @click="switchTab('login')"
            >
              登录
            </button>
            <button
              :class="['tab-btn', { active: !isLogin }]"
              @click="switchTab('register')"
            >
              注册
            </button>
            <div class="tab-indicator" :class="{ register: !isLogin }"></div>
          </div>

          <!-- 表单区域 -->
          <transition name="form-slide" mode="out-in">
            <div v-if="isLogin" key="login" class="form-content">
              <div class="form-field">
                <label class="field-label">用户名</label>
                <div class="field-input-wrapper">
                  <User class="field-icon" />
                  <el-input
                    v-model="loginForm.username"
                    placeholder="输入您的用户名"
                    class="field-input"
                    size="large"
                  />
                </div>
              </div>
              <div class="form-field">
                <label class="field-label">密码</label>
                <div class="field-input-wrapper">
                  <Lock class="field-icon" />
                  <el-input
                    v-model="loginForm.password"
                    type="password"
                    placeholder="输入您的密码"
                    class="field-input"
                    size="large"
                    @keyup.enter="handleLogin"
                  />
                </div>
              </div>
              <button class="submit-btn" :class="{ loading }" :disabled="loading" @click="handleLogin">
                <span v-if="!loading" class="btn-text">
                  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" class="btn-icon">
                    <path d="M9 3L4 8H7V13H11V8H14L9 3Z" fill="currentColor"/>
                  </svg>
                  登录账户
                </span>
                <span v-else class="loading-spinner">
                  <svg width="20" height="20" viewBox="0 0 20 20">
                    <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2" opacity="0.2"/>
                    <path d="M10 2A8 8 0 0 1 18 10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </span>
              </button>
            </div>

            <div v-else key="register" class="form-content">
              <div class="form-field">
                <label class="field-label">用户名</label>
                <div class="field-input-wrapper">
                  <UserFilled class="field-icon" />
                  <el-input
                    v-model="registerForm.username"
                    placeholder="设置用户名"
                    class="field-input"
                    size="large"
                  />
                </div>
              </div>
              <div class="form-field">
                <label class="field-label">邮箱地址</label>
                <div class="field-input-wrapper">
                  <svg class="field-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M4 5H16C17.1 5 18 5.9 18 7V15C18 16.1 17.1 17 16 17H4C2.9 17 2 16.1 2 15V7C2 5.9 2.9 5 4 5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M2 7L10 12L18 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                  <el-input
                    v-model="registerForm.email"
                    placeholder="example@email.com"
                    class="field-input"
                    size="large"
                  />
                </div>
              </div>
              <div class="form-field">
                <label class="field-label">密码</label>
                <div class="field-input-wrapper">
                  <Lock class="field-icon" />
                  <el-input
                    v-model="registerForm.password"
                    type="password"
                    placeholder="至少6位字符"
                    class="field-input"
                    size="large"
                  />
                </div>
              </div>
              <div class="form-field">
                <label class="field-label">确认密码</label>
                <div class="field-input-wrapper">
                  <Lock class="field-icon" />
                  <el-input
                    v-model="registerForm.confirmPassword"
                    type="password"
                    placeholder="再次输入密码"
                    class="field-input"
                    size="large"
                    @keyup.enter="handleRegister"
                  />
                </div>
              </div>
              <button class="submit-btn" :class="{ loading }" :disabled="loading" @click="handleRegister">
                <span v-if="!loading" class="btn-text">
                  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" class="btn-icon">
                    <path d="M9 3C9 3 13 5 13 9V11H15V13H13V15H11V13H7V11H5V9H7V7L9 3Z" fill="currentColor"/>
                  </svg>
                  创建账户
                </span>
                <span v-else class="loading-spinner">
                  <svg width="20" height="20" viewBox="0 0 20 20">
                    <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2" opacity="0.2"/>
                    <path d="M10 2A8 8 0 0 1 18 10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </span>
              </button>
            </div>
          </transition>

          <!-- 底部 -->
          <div class="card-footer">
            <div class="footer-divider"></div>
            <p class="footer-text">© 2025 天猫宠物用品数据采集系统 · 自然生长</p>
          </div>
        </div>

        <!-- 卡片阴影装饰 -->
        <div class="card-shadow-1"></div>
        <div class="card-shadow-2"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
:root {
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
}

/* ============================================
   Container
   ============================================ */
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-cream);
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  position: relative;
  overflow: hidden;
}

/* ============================================
   Nature Background
   ============================================ */
.nature-background {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
}

.paper-texture {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  opacity: 0.5;
  pointer-events: none;
}

.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  animation: drift 30s ease-in-out infinite;
}

.glow-green-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(82, 183, 136, 0.25) 0%, transparent 70%);
  top: -200px;
  left: -100px;
  animation-delay: 0s;
}

.glow-green-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(116, 198, 157, 0.2) 0%, transparent 70%);
  bottom: -150px;
  right: -100px;
  animation-delay: -15s;
}

.glow-blue-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(144, 224, 239, 0.15) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -7s;
}

@keyframes drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-20px, 30px) scale(0.95); }
  75% { transform: translate(20px, 20px) scale(1.02); }
}

.grid-pattern {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.6;
}

/* Floating Leaves */
.floating-leaf {
  position: absolute;
  animation: sway 20s ease-in-out infinite;
}

.leaf-1 {
  top: 10%;
  right: 15%;
  width: 120px;
  height: 160px;
  animation-delay: 0s;
}

.leaf-2 {
  bottom: 15%;
  left: 10%;
  width: 100px;
  height: 133px;
  animation-delay: -10s;
}

.leaf-3 {
  top: 60%;
  right: 8%;
  width: 60px;
  height: 90px;
  animation-delay: -5s;
}

@keyframes sway {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(10px, -15px) rotate(3deg);
  }
  50% {
    transform: translate(-5px, 10px) rotate(-2deg);
  }
  75% {
    transform: translate(15px, 5px) rotate(2deg);
  }
}

/* ============================================
   Content Wrapper
   ============================================ */
.content-wrapper {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  max-width: 1200px;
  width: 100%;
  padding: 60px;
}

/* ============================================
   Brand Section
   ============================================ */
.brand-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
}

.brand-content {
  position: relative;
  z-index: 1;
}

.brand-logo {
  width: 88px;
  height: 88px;
  margin-bottom: 32px;
  animation: logoBreathe 6s ease-in-out infinite;
}

@keyframes logoBreathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

.brand-logo svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 8px 24px rgba(45, 106, 79, 0.15));
}

.brand-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 40px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.brand-tagline {
  font-size: 16px;
  color: var(--text-secondary);
  margin: 0 0 48px 0;
  font-weight: 400;
  font-family: 'Nunito', sans-serif;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.feature-card:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: var(--accent-green);
  box-shadow: var(--shadow-soft);
  transform: translateX(8px);
}

.feature-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent-green), var(--primary-green-lighter));
  border-radius: 12px;
  color: white;
  flex-shrink: 0;
}

.feature-card:nth-child(2) .feature-icon {
  background: linear-gradient(135deg, var(--accent-blue-light), var(--accent-blue));
}

.feature-card:nth-child(3) .feature-icon {
  background: linear-gradient(135deg, var(--primary-green-lighter), var(--primary-green-light));
}

.feature-title {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.feature-desc {
  display: block;
  font-size: 12px;
  color: var(--text-tertiary);
}

.deco-number {
  position: absolute;
  bottom: -60px;
  left: 0;
  font-family: 'Nunito', sans-serif;
  font-size: 200px;
  font-weight: 800;
  color: rgba(45, 106, 79, 0.04);
  line-height: 1;
  pointer-events: none;
}

/* ============================================
   Auth Section
   ============================================ */
.auth-section {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  background: var(--bg-card);
  border-radius: 28px;
  padding: 40px;
  box-shadow:
    0 20px 60px rgba(45, 106, 79, 0.08),
    0 0 0 1px rgba(255, 255, 255, 0.8) inset;
  position: relative;
  overflow: hidden;
}

/* Card Decoration */
.card-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 8px;
  padding-top: 16px;
}

.deco-line {
  width: 40px;
  height: 4px;
  border-radius: 2px;
  animation: decoPulse 3s ease-in-out infinite;
}

.deco-leaf-1 {
  background: var(--primary-green-lighter);
  animation-delay: 0s;
}

.deco-leaf-2 {
  background: var(--accent-green);
  animation-delay: 0.5s;
}

.deco-leaf-3 {
  background: var(--accent-blue-light);
  animation-delay: 1s;
}

@keyframes decoPulse {
  0%, 100% { opacity: 0.6; transform: scaleX(1); }
  50% { opacity: 1; transform: scaleX(1.1); }
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
  margin-top: 20px;
}

.header-icon {
  width: 56px;
  height: 56px;
  flex-shrink: 0;
}

.header-icon svg {
  width: 100%;
  height: 100%;
}

.card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'Nunito', sans-serif;
}

/* Tab Switcher */
.tab-switcher {
  position: relative;
  display: flex;
  background: var(--bg-sand);
  border-radius: 14px;
  padding: 4px;
  margin-bottom: 28px;
  border: 1px solid var(--border-light);
}

.tab-btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 10px;
  font-family: 'Nunito', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-tertiary);
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.tab-btn.active {
  color: var(--primary-green);
}

.tab-indicator {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc(50% - 4px);
  height: calc(100% - 8px);
  background: white;
  border-radius: 10px;
  transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 2px 8px rgba(45, 106, 79, 0.08);
}

.tab-indicator.register {
  transform: translateX(calc(100% + 8px));
}

/* Form Content */
.form-content {
  min-height: 260px;
}

.form-field {
  margin-bottom: 18px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-family: 'Nunito', sans-serif;
}

.field-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 14px;
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
  transition: color 0.3s ease;
  z-index: 1;
}

.field-input :deep(.el-input__wrapper) {
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  padding: 0 14px 0 46px;
  box-shadow: none;
  transition: all 0.3s ease;
  min-height: 48px;
}

.field-input :deep(.el-input__wrapper:hover) {
  border-color: var(--accent-green);
  background: white;
}

.field-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-green-light);
  background: white;
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.1);
}

.field-input :deep(.el-input__inner) {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  font-family: inherit;
}

.field-input :deep(.el-input__inner::placeholder) {
  color: var(--text-tertiary);
}

.field-input-wrapper:focus-within .field-icon {
  color: var(--primary-green-light);
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 16px 24px;
  margin-top: 16px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--primary-green-light), var(--primary-green));
  color: white;
  font-size: 15px;
  font-weight: 700;
  font-family: 'Nunito', sans-serif;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-soft);
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary-green-lighter), var(--primary-green-light));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.submit-btn:hover:not(:disabled)::before {
  opacity: 1;
}

.submit-btn .btn-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  z-index: 1;
}

.submit-btn .btn-icon {
  color: rgba(255, 255, 255, 0.9);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Form Slide Animation */
.form-slide-enter-active,
.form-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.form-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Card Footer */
.card-footer {
  margin-top: 28px;
  padding-top: 20px;
  text-align: center;
}

.footer-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-light), transparent);
  margin-bottom: 16px;
}

.footer-text {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'Nunito', sans-serif;
}

/* Card Shadow Decorations */
.card-shadow-1,
.card-shadow-2 {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  pointer-events: none;
  z-index: -1;
}

.card-shadow-1 {
  width: 200px;
  height: 200px;
  background: rgba(116, 198, 157, 0.15);
  top: -50px;
  right: -50px;
}

.card-shadow-2 {
  width: 150px;
  height: 150px;
  background: rgba(144, 224, 239, 0.12);
  bottom: -30px;
  left: -30px;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 1024px) {
  .content-wrapper {
    grid-template-columns: 1fr;
    gap: 40px;
    padding: 40px 24px;
  }

  .brand-section {
    text-align: center;
    align-items: center;
  }

  .brand-features {
    align-items: stretch;
  }

  .deco-number {
    display: none;
  }

  .auth-card {
    max-width: 100%;
  }

  .floating-leaf {
    opacity: 0.6;
  }
}

@media (max-width: 640px) {
  .brand-title {
    font-size: 32px;
  }

  .brand-logo {
    width: 64px;
    height: 64px;
  }

  .auth-card {
    padding: 28px 20px;
    border-radius: 20px;
  }

  .feature-card {
    padding: 14px 16px;
  }

  .feature-icon {
    width: 36px;
    height: 36px;
  }
}
</style>
