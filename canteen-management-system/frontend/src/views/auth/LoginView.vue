<template>
  <div class="login-container">
    <!-- 左侧品牌区域 -->
    <div class="brand-section">
      <!-- 背景装饰图案 -->
      <div class="pattern-overlay"></div>
      <div class="gradient-overlay"></div>

      <!-- 内容 -->
      <div class="brand-content">
        <!-- Logo 和标题 -->
        <div class="brand-header">
          <div class="logo-wrapper">
            <span class="logo-icon">🍲</span>
            <div class="logo-glow"></div>
          </div>
          <h1 class="brand-title">
            <span class="title-line">食堂管理</span>
            <span class="title-line title-accent">系统</span>
          </h1>
          <p class="brand-tagline">专业的餐饮管理解决方案</p>
        </div>

        <!-- 功能特性 -->
        <div class="features-grid">
          <div class="feature-card" v-for="(feature, index) in features" :key="index" :style="{ animationDelay: `${index * 0.1}s` }">
            <span class="feature-icon">{{ feature.icon }}</span>
            <span class="feature-label">{{ feature.label }}</span>
          </div>
        </div>

        <!-- 装饰元素 -->
        <div class="floating-elements">
          <div class="float-item float-1">🥄</div>
          <div class="float-item float-2">🍽️</div>
          <div class="float-item float-3">🥢</div>
        </div>
      </div>

      <!-- 底部信息 -->
      <div class="brand-footer">
        <div class="stat-item">
          <span class="stat-value">500+</span>
          <span class="stat-label">企业用户</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">99.9%</span>
          <span class="stat-label">稳定性</span>
        </div>
      </div>
    </div>

    <!-- 右侧登录区域 -->
    <div class="login-section">
      <div class="login-wrapper">
        <!-- 顶部导航 -->
        <div class="login-nav">
          <span class="nav-label">欢迎回来</span>
          <router-link to="/register" class="nav-link">创建账号 →</router-link>
        </div>

        <!-- 登录表单 -->
        <div class="login-card">
          <div class="card-header">
            <h2 class="card-title">登录账号</h2>
            <p class="card-subtitle">输入您的账号信息以继续</p>
          </div>

          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            @submit.prevent="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="账号"
                size="large"
                clearable
                :prefix-icon="User"
                @keyup.enter="handleLogin"
                class="custom-input"
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                size="large"
                clearable
                show-password
                :prefix-icon="Lock"
                @keyup.enter="handleLogin"
                class="custom-input"
              />
            </el-form-item>

            <div class="form-actions">
              <el-checkbox v-model="rememberMe" class="custom-checkbox">
                <span class="checkbox-label">记住账号</span>
              </el-checkbox>
              <a href="#" class="forgot-link" @click.prevent="handleForgotPassword">忘记密码？</a>
            </div>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="login-button"
                :loading="loading"
                @click="handleLogin"
              >
                <template v-if="!loading">
                  <span class="button-text">登录</span>
                  <span class="button-arrow">→</span>
                </template>
                <template v-else>
                  <span>登录中...</span>
                </template>
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 版权信息 -->
        <div class="login-footer">
          <p>© 2026 食堂管理系统</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '../../stores/user'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const features = [
  { icon: '👨‍🍳', label: '员工管理' },
  { icon: '📅', label: '智能排班' },
  { icon: '⏰', label: '考勤打卡' },
  { icon: '💰', label: '薪资核算' }
]

const savedUsername = localStorage.getItem('rememberedUsername')
if (savedUsername) {
  loginForm.username = savedUsername
  rememberMe.value = true
}

const loginRules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 2, message: '账号长度不能少于 2 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, message: '密码长度不能少于 4 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
    loading.value = true

    const result = await userStore.login(loginForm.username, loginForm.password)

    if (result.success) {
      if (rememberMe.value) {
        localStorage.setItem('rememberedUsername', loginForm.username)
      } else {
        localStorage.removeItem('rememberedUsername')
      }

      ElMessage.success('登录成功！')

      const userRole = userStore.userRole
      if (userRole === 'ADMIN') {
        router.push('/admin')
      } else if (userRole === 'EMPLOYEE') {
        router.push('/employee')
      } else {
        router.push('/login')
      }
    } else {
      ElMessage.error(result.message || '登录失败，请检查账号和密码')
    }
  } catch (error) {
    console.error('登录错误:', error)
    if (error.message) {
      ElMessage.error(error.message)
    }
  } finally {
    loading.value = false
  }
}

const handleForgotPassword = () => {
  ElMessage.info('请联系管理员重置密码')
}
</script>

<style scoped>
/* ==================== 全局变量 ==================== */
:root {
  --color-primary: #FF6B35;
  --color-secondary: #F7C52D;
  --color-accent: #FF8C42;
  --color-text: #2D3436;
  --color-text-light: #636E72;
  --color-border: #DFE6E9;
  --color-bg: #FFFFFF;
  --shadow-sm: 0 2px 8px rgba(45, 52, 54, 0.08);
  --shadow-md: 0 8px 24px rgba(45, 52, 54, 0.12);
  --shadow-lg: 0 16px 48px rgba(45, 52, 54, 0.16);
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
}

/* 隐藏滚动条但保持滚动功能 */
.login-container {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE 10+ */
}

.login-container::-webkit-scrollbar {
  display: none; /* Chrome Safari */
}

.brand-content {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.brand-content::-webkit-scrollbar {
  display: none;
}

/* ==================== 容器布局 ==================== */
.login-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* ==================== 左侧品牌区域 ==================== */
.brand-section {
  position: relative;
  width: 52%;
  min-width: 0;
  background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #F7C52D 100%);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 图案叠加层 */
.pattern-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0.08;
  background-image:
    repeating-linear-gradient(
      45deg,
      transparent,
      transparent 35px,
      rgba(255, 255, 255, 0.3) 35px,
      rgba(255, 255, 255, 0.3) 70px
    );
}

.gradient-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.15), transparent);
  pointer-events: none;
}

.brand-content {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(24px, 4vw, 60px);
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Logo 和标题 */
.brand-header {
  margin-bottom: clamp(24px, 4vw, 48px);
  flex-shrink: 0;
}

.logo-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: clamp(16px, 2vw, 24px);
}

.logo-icon {
  font-size: clamp(40px, 6vw, 64px);
  display: block;
  filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.2));
  animation: logoFloat 4s ease-in-out infinite;
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-12px) rotate(3deg); }
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120%;
  height: 120%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent 70%);
  border-radius: 50%;
  animation: glowPulse 3s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.1); }
}

.brand-title {
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  font-size: clamp(26px, 4vw, 48px);
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 clamp(8px, 1.5vw, 14px) 0;
  color: white;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  letter-spacing: 0.02em;
}

.title-line {
  display: block;
}

.title-accent {
  color: #FFF8F0;
  font-weight: 800;
}

.brand-tagline {
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  font-size: clamp(12px, 1.5vw, 16px);
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 300;
  letter-spacing: 0.05em;
}

/* 功能特性网格 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: clamp(10px, 1.5vw, 16px);
  max-width: 100%;
}

.feature-card {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 12px);
  padding: clamp(10px, 1.5vw, 16px) clamp(12px, 2vw, 18px);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateX(8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: clamp(20px, 2.5vw, 28px);
  flex-shrink: 0;
}

.feature-label {
  font-size: clamp(13px, 1.6vw, 16px);
  color: white;
  font-weight: 500;
}

/* 浮动元素 */
.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  overflow: hidden;
}

.float-item {
  position: absolute;
  font-size: clamp(24px, 3vw, 36px);
  opacity: 0.2;
  animation: floatAround 20s ease-in-out infinite;
}

.float-1 {
  top: 15%;
  right: 10%;
  animation-delay: 0s;
}

.float-2 {
  bottom: 25%;
  left: 8%;
  animation-delay: 7s;
}

.float-3 {
  top: 45%;
  right: 15%;
  animation-delay: 14s;
}

@keyframes floatAround {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(20px, -30px) rotate(5deg);
  }
  50% {
    transform: translate(-15px, -20px) rotate(-3deg);
  }
  75% {
    transform: translate(10px, 15px) rotate(3deg);
  }
}

/* 底部统计信息 */
.brand-footer {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(20px, 3vw, 32px);
  padding: clamp(16px, 2.5vw, 32px);
  flex-shrink: 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: clamp(16px, 2vw, 24px);
  font-weight: 700;
  color: white;
  line-height: 1;
  margin-bottom: clamp(2px, 0.3vw, 4px);
}

.stat-label {
  display: block;
  font-size: clamp(10px, 1.2vw, 12px);
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}

.stat-divider {
  width: 1px;
  height: clamp(24px, 3vw, 32px);
  background: rgba(255, 255, 255, 0.3);
}

/* ==================== 右侧登录区域 ==================== */
.login-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  padding: clamp(20px, 3vw, 40px);
  min-width: 0;
  position: relative;
  overflow: hidden;
}

.login-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 0;
}

/* 顶部导航 */
.login-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: clamp(20px, 3vw, 32px);
  flex-shrink: 0;
}

.nav-label {
  font-size: clamp(11px, 1.5vw, 13px);
  color: var(--color-text-light);
  font-weight: 500;
}

.nav-link {
  font-size: clamp(12px, 1.6vw, 14px);
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: var(--color-accent);
  transform: translateX(3px);
}

/* 登录卡片 */
.login-card {
  background: white;
  padding: clamp(28px, 3vw, 40px);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  flex-shrink: 0;
}

.card-header {
  margin-bottom: clamp(20px, 3vw, 28px);
}

.card-title {
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
  font-size: clamp(22px, 3vw, 28px);
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px 0;
  letter-spacing: -0.01em;
}

.card-subtitle {
  font-size: 14px;
  color: var(--color-text-light);
  margin: 0;
  font-weight: 400;
}

/* 表单样式 */
.login-form {
  margin-bottom: 8px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: clamp(14px, 2vw, 18px);
}

.custom-input :deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
  padding: clamp(10px, 1.5vw, 12px) clamp(12px, 2vw, 16px);
  box-shadow: none;
  border: 2px solid var(--color-border);
  background: #FAFBFC;
  transition: all 0.2s ease;
}

.custom-input :deep(.el-input__wrapper:hover) {
  border-color: #CBD5E0;
  background: white;
}

.custom-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--color-primary);
  background: white;
  box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
}

.custom-input :deep(.el-input__inner) {
  font-size: clamp(13px, 1.8vw, 15px);
  color: var(--color-text);
  font-weight: 500;
  letter-spacing: 0.01em;
}

.custom-input :deep(.el-input__prefix) {
  font-size: clamp(16px, 2vw, 20px);
  color: var(--color-primary);
}

/* 表单操作 */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: clamp(18px, 2.5vw, 24px);
}

.custom-checkbox :deep(.el-checkbox__label) {
  font-size: 14px;
  color: var(--color-text);
}

.checkbox-label {
  font-weight: 500;
}

.custom-checkbox :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
}

.forgot-link {
  font-size: 14px;
  color: var(--color-text-light);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: var(--color-primary);
  text-decoration: underline;
}

/* 登录按钮 */
.login-button {
  width: 100%;
  height: clamp(46px, 6vw, 52px);
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  border: none;
  font-size: clamp(14px, 2vw, 16px);
  font-weight: 600;
  letter-spacing: 0.05em;
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.button-text {
  margin-right: clamp(6px, 1vw, 8px);
}

.button-arrow {
  display: inline-block;
  transition: transform 0.3s ease;
}

.login-button:hover .button-arrow {
  transform: translateX(4px);
}

/* 版权信息 */
.login-footer {
  margin-top: clamp(16px, 2vw, 24px);
  text-align: center;
  flex-shrink: 0;
}

.login-footer p {
  font-size: clamp(11px, 1.3vw, 13px);
  color: var(--color-text-light);
  margin: 0;
}

/* ==================== 响应式设计 ==================== */

/* 小屏 PC/平板横屏 */
@media (max-width: 1200px) {
  .brand-section {
    width: 48%;
  }

  .features-grid {
    max-width: 280px;
  }

  .brand-footer {
    padding: clamp(16px, 2vw, 24px);
  }
}

/* 平板竖屏 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }

  .brand-section {
    width: 100%;
    min-width: 0;
    flex-shrink: 0;
    max-height: 40vh;
  }

  .brand-content {
    padding: clamp(12px, 2vw, 20px);
  }

  .brand-header {
    margin-bottom: clamp(12px, 2vw, 20px);
    text-align: center;
  }

  .logo-wrapper {
    margin-bottom: 12px;
  }

  .logo-icon {
    font-size: clamp(32px, 5vw, 48px);
  }

  .brand-title {
    font-size: clamp(20px, 3.5vw, 28px);
  }

  .brand-tagline {
    font-size: clamp(11px, 1.5vw, 13px);
  }

  .features-grid {
    max-width: 100%;
    gap: 8px;
  }

  .feature-card {
    padding: 10px 14px;
  }

  .feature-icon {
    font-size: clamp(16px, 2.5vw, 20px);
  }

  .feature-label {
    font-size: clamp(11px, 1.5vw, 13px);
  }

  .floating-elements {
    display: none;
  }

  .brand-footer {
    display: none;
  }

  .login-section {
    flex: 1;
    padding: clamp(12px, 2vw, 24px);
    min-width: 0;
    min-height: 0;
  }

  .login-wrapper {
    max-width: 100%;
  }

  .login-card {
    padding: clamp(18px, 2.5vw, 28px);
  }

  .login-nav {
    margin-bottom: clamp(12px, 2vw, 20px);
  }

  .card-header {
    margin-bottom: clamp(16px, 2vw, 24px);
  }

  .login-form :deep(.el-form-item) {
    margin-bottom: 14px;
  }

  .form-actions {
    margin-bottom: 16px;
  }
}

/* 手机 */
@media (max-width: 480px) {
  .brand-section {
    max-height: 35vh;
  }

  .brand-content {
    padding: clamp(10px, 2vw, 16px);
  }

  .logo-icon {
    font-size: clamp(28px, 5vw, 40px);
  }

  .brand-title {
    font-size: clamp(18px, 3.5vw, 24px);
  }

  .brand-tagline {
    font-size: clamp(10px, 2vw, 12px);
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .feature-card {
    padding: 8px 12px;
  }

  .feature-icon {
    font-size: clamp(14px, 2.5vw, 18px);
  }

  .feature-label {
    font-size: clamp(10px, 2vw, 12px);
  }

  .login-section {
    padding: clamp(10px, 2vw, 20px);
  }

  .login-card {
    padding: clamp(14px, 2.5vw, 24px);
    border-radius: var(--radius-md);
  }

  .card-title {
    font-size: clamp(16px, 3vw, 20px);
  }

  .card-subtitle {
    font-size: clamp(11px, 2vw, 13px);
  }

  .login-form :deep(.el-form-item) {
    margin-bottom: 12px;
  }

  .form-actions {
    margin-bottom: 14px;
  }

  .login-button {
    height: clamp(42px, 6vw, 48px);
    font-size: clamp(13px, 2.5vw, 15px);
  }

  .login-footer {
    margin-top: clamp(10px, 2vw, 16px);
  }
}
</style>
