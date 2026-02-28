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
    userStore.setRefreshToken(res.data.refresh_token)  // 新增：保存 refresh_token
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
    <!-- 背景装饰 -->
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <div class="login-wrapper">
      <!-- Logo 区域 -->
      <div class="logo-section">
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
        <h1 class="logo-title">天猫宠物用品数据</h1>
        <p class="logo-subtitle">Tmall Pet Supplies Data Platform</p>
      </div>

      <!-- 登录/注册卡片 -->
      <div class="auth-card">
        <!-- Tab 切换 -->
        <div class="auth-tabs">
          <button
            :class="['tab-btn', { active: activeTab === 'login' }]"
            @click="switchTab('login')"
          >
            登录
          </button>
          <button
            :class="['tab-btn', { active: activeTab === 'register' }]"
            @click="switchTab('register')"
          >
            注册
          </button>
          <div class="tab-indicator" :class="`indicator-${activeTab}`"></div>
        </div>

        <!-- 登录表单 -->
        <transition name="slide-fade" mode="out-in">
          <div v-if="isLogin" key="login" class="form-container">
            <div class="input-group">
              <el-input
                v-model="loginForm.username"
                placeholder="用户名"
                :prefix-icon="User"
                size="large"
                class="custom-input"
              />
            </div>
            <div class="input-group">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                :prefix-icon="Lock"
                size="large"
                class="custom-input"
                @keyup.enter="handleLogin"
              />
            </div>
            <button
              class="submit-btn"
              :class="{ loading }"
              :disabled="loading"
              @click="handleLogin"
            >
              <span v-if="!loading">登录</span>
              <span v-else class="loading-text">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </span>
            </button>
          </div>

          <!-- 注册表单 -->
          <div v-else key="register" class="form-container">
            <div class="input-group">
              <el-input
                v-model="registerForm.username"
                placeholder="用户名"
                :prefix-icon="UserFilled"
                size="large"
                class="custom-input"
              />
            </div>
            <div class="input-group">
              <el-input
                v-model="registerForm.email"
                placeholder="邮箱地址"
                :prefix-icon="UserFilled"
                size="large"
                class="custom-input"
              />
            </div>
            <div class="input-group">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="密码（至少6位）"
                :prefix-icon="Lock"
                size="large"
                class="custom-input"
              />
            </div>
            <div class="input-group">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="确认密码"
                :prefix-icon="Lock"
                size="large"
                class="custom-input"
                @keyup.enter="handleRegister"
              />
            </div>
            <button
              class="submit-btn"
              :class="{ loading }"
              :disabled="loading"
              @click="handleRegister"
            >
              <span v-if="!loading">注册</span>
              <span v-else class="loading-text">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </span>
            </button>
          </div>
        </transition>
      </div>

      <!-- 底部信息 -->
      <p class="footer-text">© 2025 天猫宠物用品数据采集系统</p>
    </div>
  </div>
</template>

<style scoped>
/* 引入字体 */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
  font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
  overflow: hidden;
}

/* 背景装饰图形 */
.bg-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: float 20s ease-in-out infinite;
}

.shape-1 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #FF6B35, #FF8E53);
  top: -200px;
  left: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #7B2CBF, #9D4EDD);
  bottom: -150px;
  right: -100px;
  animation-delay: -7s;
}

.shape-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #00D9FF, #0099CC);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, -30px) scale(1.05);
  }
  50% {
    transform: translate(-20px, 20px) scale(0.95);
  }
  75% {
    transform: translate(20px, 30px) scale(1.02);
  }
}

.login-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

/* Logo 区域 */
.logo-section {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
  animation: logoFloat 3s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.logo-title {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, #FF6B35, #FFD700, #7B2CBF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.logo-subtitle {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 500;
  margin: 0;
  letter-spacing: 0.5px;
}

/* 认证卡片 */
.auth-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Tab 切换 */
.auth-tabs {
  position: relative;
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 14px;
  padding: 4px;
  margin-bottom: 28px;
}

.tab-btn {
  flex: 1;
  padding: 12px 24px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
  font-size: 15px;
  font-weight: 600;
  font-family: 'Nunito', sans-serif;
  cursor: pointer;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}

.tab-btn.active {
  color: #1a1a2e;
}

.tab-indicator {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc(50% - 4px);
  height: calc(100% - 8px);
  background: linear-gradient(135deg, #FF6B35, #7B2CBF);
  border-radius: 12px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.indicator-login {
  transform: translateX(0);
}

.indicator-register {
  transform: translateX(100%);
}

/* 表单容器 */
.form-container {
  min-height: 200px;
}

.input-group {
  margin-bottom: 16px;
}

.custom-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 4px 16px;
  box-shadow: none;
  transition: all 0.3s ease;
}

.custom-input :deep(.el-input__wrapper:hover),
.custom-input :deep(.el-input__wrapper.is-focus) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 107, 53, 0.5);
  box-shadow: 0 0 20px rgba(255, 107, 53, 0.1);
}

.custom-input :deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
  font-size: 15px;
  font-weight: 500;
}

.custom-input :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.custom-input :deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.4);
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 16px;
  margin-top: 8px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #FF6B35, #7B2CBF);
  color: white;
  font-size: 16px;
  font-weight: 700;
  font-family: 'Nunito', sans-serif;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.3);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(255, 107, 53, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 加载动画 */
.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.dot {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite;
}

.dot:nth-child(1) {
  animation-delay: 0s;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 过渡动画 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 底部信息 */
.footer-text {
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  font-size: 12px;
  margin-top: 24px;
}
</style>
