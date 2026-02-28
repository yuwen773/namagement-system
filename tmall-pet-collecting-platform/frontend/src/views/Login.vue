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
    <!-- 动态背景层 -->
    <div class="bg-layer">
      <!-- 爪印图案装饰 -->
      <svg class="paw-pattern" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="pawPattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
            <g fill="none" stroke="rgba(255, 107, 53, 0.03)" stroke-width="1">
              <circle cx="50" cy="50" r="8"/>
              <circle cx="35" cy="40" r="4"/>
              <circle cx="65" cy="40" r="4"/>
              <circle cx="38" cy="60" r="4"/>
              <circle cx="62" cy="60" r="4"/>
            </g>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#pawPattern)"/>
      </svg>

      <!-- 光晕效果 -->
      <div class="glow-orb glow-1"></div>
      <div class="glow-orb glow-2"></div>
      <div class="glow-orb glow-3"></div>

      <!-- 网格线装饰 -->
      <div class="grid-lines">
        <div class="grid-line" v-for="i in 5" :key="i" :style="{ top: `${i * 20}%` }"></div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="content-wrapper">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="brand-logo">
            <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="80" height="80" rx="20" fill="url(#brandGrad)"/>
              <g transform="translate(20, 15)">
                <path d="M20 5 L32 17 L20 29 L8 17 Z" fill="white"/>
                <path d="M13 29 L20 36 L27 29" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="20" cy="17" r="5" fill="#FF6B35"/>
              </g>
              <defs>
                <linearGradient id="brandGrad" x1="0" y1="0" x2="80" y2="80">
                  <stop offset="0%" stop-color="#FF6B35"/>
                  <stop offset="100%" stop-color="#7B2CBF"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 class="brand-title">宠物用品数据平台</h1>
          <p class="brand-tagline">洞察天猫宠物消费趋势</p>

          <div class="brand-features">
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 2L4 7V15C4 15.55 4.45 16 5 16H15C15.55 16 16 15.55 16 15V7L10 2Z" stroke="currentColor" stroke-width="1.5"/>
                </svg>
              </div>
              <span>数据采集</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M10 6V10L13 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>
              <span>实时分析</span>
            </div>
            <div class="feature-item">
              <div class="feature-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M3 8L8 3L13 8M17 12L12 17L7 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </div>
              <span>智能洞察</span>
            </div>
          </div>
        </div>

        <!-- 装饰数字 -->
        <div class="deco-number">01</div>
      </div>

      <!-- 右侧登录卡片 -->
      <div class="auth-section">
        <div class="auth-card">
          <!-- 卡片头部 -->
          <div class="card-header">
            <h2 class="card-title">{{ isLogin ? '欢迎回来' : '创建账户' }}</h2>
            <p class="card-subtitle">{{ isLogin ? '登录以继续使用数据平台' : '开始您的数据洞察之旅' }}</p>
          </div>

          <!-- Tab 切换 -->
          <div class="tab-switcher">
            <button
              :class="['tab-switch', { active: isLogin }]"
              @click="switchTab('login')"
            >
              <span class="tab-text">登录</span>
            </button>
            <button
              :class="['tab-switch', { active: !isLogin }]"
              @click="switchTab('register')"
            >
              <span class="tab-text">注册</span>
            </button>
            <div class="tab-slider" :class="{ register: !isLogin }"></div>
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
                <span v-if="!loading">登录账户</span>
                <span v-else class="loading-spinner">
                  <svg width="20" height="20" viewBox="0 0 20 20">
                    <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2" opacity="0.3"/>
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
                <span v-if="!loading">创建账户</span>
                <span v-else class="loading-spinner">
                  <svg width="20" height="20" viewBox="0 0 20 20">
                    <circle cx="10" cy="10" r="8" fill="none" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                    <path d="M10 2A8 8 0 0 1 18 10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </span>
              </button>
            </div>
          </transition>

          <!-- 底部链接 -->
          <div class="card-footer">
            <p class="footer-text">© 2025 天猫宠物用品数据采集系统</p>
          </div>
        </div>

        <!-- 装饰元素 -->
        <div class="deco-circle deco-1"></div>
        <div class="deco-circle deco-2"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

:root {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --bg-dark: #0D0D14;
  --bg-card: rgba(20, 20, 32, 0.6);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.5);
  --text-tertiary: rgba(255, 255, 255, 0.3);
  --border-color: rgba(255, 255, 255, 0.08);
  --border-hover: rgba(255, 107, 53, 0.3);
}

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-dark);
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
  position: relative;
  overflow: hidden;
}

/* 动态背景层 */
.bg-layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
}

.paw-pattern {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.4;
}

/* 光晕效果 */
.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  animation: glowFloat 25s ease-in-out infinite;
  opacity: 0.6;
}

.glow-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255, 107, 53, 0.4) 0%, transparent 70%);
  top: -200px;
  left: -100px;
  animation-delay: 0s;
}

.glow-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(123, 44, 191, 0.35) 0%, transparent 70%);
  bottom: -150px;
  right: -100px;
  animation-delay: -8s;
}

.glow-3 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(255, 215, 0, 0.2) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -16s;
}

@keyframes glowFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(40px, -30px) scale(1.1); }
  50% { transform: translate(-20px, 40px) scale(0.9); }
  75% { transform: translate(30px, 20px) scale(1.05); }
}

/* 网格线 */
.grid-lines {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.grid-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.1), transparent);
}

/* 内容包装器 */
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

/* 品牌区域 */
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
  width: 80px;
  height: 80px;
  margin-bottom: 28px;
  animation: brandPulse 4s ease-in-out infinite;
}

@keyframes brandPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.brand-logo svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 8px 24px rgba(255, 107, 53, 0.3));
}

.brand-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 42px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px 0;
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.brand-tagline {
  font-size: 17px;
  color: var(--text-secondary);
  margin: 0 0 48px 0;
  font-weight: 400;
}

.brand-features {
  display: flex;
  gap: 24px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  background: rgba(255, 107, 53, 0.08);
  border: 1px solid rgba(255, 107, 53, 0.15);
  border-radius: 12px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(255, 107, 53, 0.12);
  border-color: rgba(255, 107, 53, 0.25);
  color: var(--text-primary);
  transform: translateY(-2px);
}

.feature-icon {
  color: var(--primary-orange);
  display: flex;
  align-items: center;
  justify-content: center;
}

.deco-number {
  position: absolute;
  bottom: -40px;
  left: 0;
  font-family: 'Outfit', sans-serif;
  font-size: 180px;
  font-weight: 800;
  color: rgba(255, 107, 53, 0.03);
  line-height: 1;
  pointer-events: none;
}

/* 认证区域 */
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
  backdrop-filter: blur(40px);
  border: 1px solid var(--border-color);
  border-radius: 32px;
  padding: 44px;
  box-shadow:
    0 40px 80px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
  position: relative;
  overflow: hidden;
}

.auth-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-orange), var(--primary-purple), var(--primary-orange));
  background-size: 200% 100%;
  animation: shimmer 3s linear infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.card-header {
  margin-bottom: 36px;
}

.card-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.card-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

/* Tab 切换 */
.tab-switcher {
  position: relative;
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 16px;
  padding: 4px;
  margin-bottom: 32px;
  border: 1px solid var(--border-color);
}

.tab-switch {
  flex: 1;
  padding: 12px 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}

.tab-switch .tab-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-tertiary);
  transition: color 0.3s ease;
}

.tab-switch.active .tab-text {
  color: var(--text-primary);
}

.tab-slider {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc(50% - 4px);
  height: calc(100% - 8px);
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  border-radius: 12px;
  transition: transform 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.3);
}

.tab-slider.register {
  transform: translateX(calc(100% + 8px));
}

/* 表单内容 */
.form-content {
  min-height: 280px;
}

.form-field {
  margin-bottom: 20px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.field-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 16px;
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
  transition: color 0.3s ease;
  z-index: 1;
}

.field-input :deep(.el-input__wrapper) {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  padding: 0 16px 0 48px;
  box-shadow: none;
  transition: all 0.3s ease;
  min-height: 52px;
}

.field-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.2);
  background: rgba(0, 0, 0, 0.25);
}

.field-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-orange);
  background: rgba(0, 0, 0, 0.2);
  box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
}

.field-input :deep(.el-input__inner) {
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 500;
  font-family: inherit;
}

.field-input :deep(.el-input__inner::placeholder) {
  color: var(--text-tertiary);
}

.field-input-wrapper:focus-within .field-icon {
  color: var(--primary-orange);
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 18px 24px;
  margin-top: 12px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  color: white;
  font-size: 16px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 12px 32px rgba(255, 107, 53, 0.3);
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary-purple), var(--primary-orange));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.submit-btn:hover:not(:disabled)::before {
  opacity: 1;
}

.submit-btn span {
  position: relative;
  z-index: 1;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 20px 48px rgba(255, 107, 53, 0.4);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(-1px);
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

/* 表单切换动画 */
.form-slide-enter-active,
.form-slide-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-slide-enter-from {
  opacity: 0;
  transform: translateX(40px);
}

.form-slide-leave-to {
  opacity: 0;
  transform: translateX(-40px);
}

/* 卡片底部 */
.card-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.footer-text {
  font-size: 12px;
  color: var(--text-tertiary);
  margin: 0;
}

/* 装饰圆圈 */
.deco-circle {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.deco-1 {
  width: 120px;
  height: 120px;
  border: 1px solid rgba(255, 107, 53, 0.15);
  top: -40px;
  right: -40px;
  animation: decoFloat 8s ease-in-out infinite;
}

.deco-2 {
  width: 80px;
  height: 80px;
  border: 1px solid rgba(123, 44, 191, 0.15);
  bottom: 60px;
  left: -30px;
  animation: decoFloat 10s ease-in-out infinite reverse;
}

@keyframes decoFloat {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(10px, 10px); }
}

/* 响应式设计 */
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
    justify-content: center;
  }

  .deco-number {
    display: none;
  }

  .auth-card {
    max-width: 100%;
  }
}

@media (max-width: 640px) {
  .brand-title {
    font-size: 32px;
  }

  .brand-features {
    flex-direction: column;
    align-items: stretch;
  }

  .auth-card {
    padding: 32px 24px;
    border-radius: 24px;
  }
}
</style>
