<template>
  <div class="login-page">
    <!-- 左侧品牌展示区 -->
    <div class="brand-side">
      <!-- 装饰性食物图标 -->
      <div class="food-icons">
        <div class="food-icon food-icon-1">🍳</div>
        <div class="food-icon food-icon-2">🥄</div>
        <div class="food-icon food-icon-3">🍜</div>
        <div class="food-icon food-icon-4">🥗</div>
        <div class="food-icon food-icon-5">🍲</div>
        <div class="food-icon food-icon-6">🍚</div>
      </div>

      <div class="brand-bg">
        <div class="bg-gradient"></div>
        <div class="bg-pattern"></div>
        <div class="bg-dots"></div>
      </div>

      <div class="brand-content">
        <!-- 厨师帽Logo -->
        <div class="chef-hat-container">
          <svg class="chef-hat" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 45 C20 25, 45 15, 50 15 C55 15, 80 25, 80 45 C80 55, 70 60, 65 60 L35 60 C30 60, 20 55, 20 45" fill="white"/>
            <rect x="30" y="55" width="40" height="30" rx="3" fill="white"/>
            <path d="M35 60 L35 80 M45 60 L45 80 M55 60 L55 80 M65 60 L65 80" stroke="#FF6B35" stroke-width="2" opacity="0.3"/>
          </svg>
        </div>

        <h1 class="brand-title">食堂管理系统</h1>
        <p class="brand-subtitle">Canteen Management System</p>

        <!-- 特色功能展示 -->
        <div class="features-container">
          <div class="feature-item" v-for="(feature, idx) in features" :key="idx">
            <div class="feature-icon-wrapper">{{ feature.icon }}</div>
            <span class="feature-text">{{ feature.text }}</span>
          </div>
        </div>

        <!-- 数据统计 -->
        <div class="stats-row">
          <div class="stat-item">
            <div class="stat-value">500+</div>
            <div class="stat-label">企业用户</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-value">99.9%</div>
            <div class="stat-label">稳定性</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧登录表单区 -->
    <div class="form-side">
      <div class="form-wrapper">
        <div class="form-header">
          <div class="header-icon">👨‍🍳</div>
          <h2>欢迎回来</h2>
          <p>登录账号，开启高效管理之旅</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <div class="input-group">
              <div class="input-label">账号</div>
              <el-input
                v-model="form.username"
                size="large"
                placeholder="请输入您的账号"
                :prefix-icon="User"
                clearable
                @keyup.enter="handleLogin"
              />
            </div>
          </el-form-item>

          <el-form-item prop="password">
            <div class="input-group">
              <div class="input-label">密码</div>
              <el-input
                v-model="form.password"
                type="password"
                size="large"
                placeholder="请输入您的密码"
                :prefix-icon="Lock"
                show-password
                clearable
                @keyup.enter="handleLogin"
              />
            </div>
          </el-form-item>

          <div class="form-options">
            <el-checkbox v-model="rememberMe" class="custom-checkbox">
              <span>记住账号</span>
            </el-checkbox>
            <el-link class="forgot-link" @click="handleForgot">忘记密码？</el-link>
          </div>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="submit-btn"
              :loading="loading"
              @click="handleLogin"
            >
              <span v-if="!loading">登录</span>
              <span v-else>登录中...</span>
            </el-button>
          </el-form-item>
        </el-form>

        <div class="form-footer">
          <span class="footer-text">还没有账号？</span>
          <router-link to="/register" class="register-link">
            立即注册 →
          </router-link>
        </div>
      </div>

      <!-- 底部装饰 -->
      <div class="bottom-decoration">
        <span class="decoration-text">🍽️ 智慧餐饮 · 高效运营</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

const form = reactive({
  username: localStorage.getItem('rememberedUsername') || '',
  password: ''
})

if (form.username) {
  rememberMe.value = true
}

const features = [
  { icon: '👥', text: '员工管理' },
  { icon: '📅', text: '智能排班' },
  { icon: '⏰', text: '考勤打卡' },
  { icon: '📊', text: '数据统计' }
]

const rules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 2, message: '账号至少2个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 4, message: '密码至少4个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    const result = await userStore.login(form.username, form.password)

    if (result.success) {
      if (rememberMe.value) {
        localStorage.setItem('rememberedUsername', form.username)
      } else {
        localStorage.removeItem('rememberedUsername')
      }

      ElMessage.success('登录成功！')

      const role = userStore.userRole
      if (role === 'ADMIN') {
        router.push('/admin')
      } else if (role === 'EMPLOYEE') {
        router.push('/employee')
      }
    }
  } catch (error) {
    console.error('登录错误:', error)
  } finally {
    loading.value = false
  }
}

const handleForgot = () => {
  ElMessage.info('请联系管理员重置密码')
}
</script>

<style scoped>
/* ==================== 全局变量 ==================== */
:root {
  --primary-orange: #FF6B35;
  --primary-light: #FF8C42;
  --primary-dark: #E55A2B;
  --secondary-yellow: #F7C52D;
  --accent-green: #4CAF50;
  --bg-cream: #FFF8F0;
  --bg-light: #FFFDF8;
  --text-primary: #2C1810;
  --text-secondary: #6B5D52;
  --text-muted: #9A8B7E;
  --border-color: #E8DCC8;
  --shadow-soft: 0 8px 32px rgba(255, 107, 53, 0.12);
  --shadow-hover: 0 12px 48px rgba(255, 107, 53, 0.18);
}

/* ==================== 主容器 ==================== */
.login-page {
  display: flex;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: var(--bg-cream);
}

/* ==================== 左侧品牌区 ==================== */
.brand-side {
  position: relative;
  width: 54%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* 背景渐变 */
.brand-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 35%, #FFA552 65%, #F7C52D 100%);
}

.bg-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 30% 40%, rgba(255, 255, 255, 0.15) 0%, transparent 50%),
              radial-gradient(ellipse at 70% 60%, rgba(247, 197, 45, 0.2) 0%, transparent 50%);
}

.bg-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.08;
  background-image:
    repeating-linear-gradient(60deg, transparent, transparent 30px, rgba(255,255,255,0.3) 30px, rgba(255,255,255,0.3) 32px),
    repeating-linear-gradient(-60deg, transparent, transparent 30px, rgba(255,255,255,0.3) 30px, rgba(255,255,255,0.3) 32px);
}

.bg-dots {
  position: absolute;
  inset: 0;
  opacity: 0.12;
  background-image: radial-gradient(circle, rgba(255,255,255,0.4) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* 浮动食物图标 */
.food-icons {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.food-icon {
  position: absolute;
  font-size: 32px;
  opacity: 0.2;
  animation: float 6s ease-in-out infinite;
}

.food-icon-1 { top: 12%; left: 8%; animation-delay: 0s; }
.food-icon-2 { top: 25%; right: 12%; animation-delay: 1s; }
.food-icon-3 { bottom: 30%; left: 15%; animation-delay: 2s; }
.food-icon-4 { bottom: 18%; right: 8%; animation-delay: 3s; }
.food-icon-5 { top: 45%; left: 6%; animation-delay: 4s; }
.food-icon-6 { top: 60%; right: 10%; animation-delay: 5s; }

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(8deg);
  }
}

.brand-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 60px 50px;
  color: white;
}

/* 厨师帽Logo */
.chef-hat-container {
  margin-bottom: 28px;
  animation: hatBounce 3s ease-in-out infinite;
}

.chef-hat {
  width: 100px;
  height: 100px;
  filter: drop-shadow(0 12px 32px rgba(0,0,0,0.25));
}

@keyframes hatBounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.brand-title {
  font-size: 44px;
  font-weight: 800;
  margin: 0 0 8px 0;
  letter-spacing: 6px;
  text-shadow: 0 4px 24px rgba(0,0,0,0.2);
  background: linear-gradient(135deg, #FFFFFF 0%, #FFF8F0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 13px;
  opacity: 0.95;
  margin: 0 0 52px 0;
  font-weight: 400;
  letter-spacing: 4px;
  text-transform: uppercase;
}

/* 特色功能 */
.features-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  max-width: 380px;
  margin: 0 auto 48px;
}

.feature-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1.5px solid rgba(255, 255, 255, 0.25);
  font-size: 15px;
  font-weight: 600;
  animation: slideInUp 0.6s ease-out backwards;
  transition: all 0.3s ease;
}

.feature-item:nth-child(1) { animation-delay: 0.1s; }
.feature-item:nth-child(2) { animation-delay: 0.2s; }
.feature-item:nth-child(3) { animation-delay: 0.3s; }
.feature-item:nth-child(4) { animation-delay: 0.4s; }

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.28);
  transform: translateX(6px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.feature-icon-wrapper {
  font-size: 22px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.feature-text {
  letter-spacing: 1px;
}

/* 统计数据 */
.stats-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 6px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.stat-label {
  font-size: 11px;
  opacity: 0.9;
  letter-spacing: 1px;
  font-weight: 500;
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: rgba(255, 255, 255, 0.3);
}

/* ==================== 右侧表单区 ==================== */
.form-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg-light);
  padding: 48px 40px;
  position: relative;
}

.form-side::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-orange), var(--secondary-yellow));
}

.form-wrapper {
  width: 100%;
  max-width: 420px;
}

.form-header {
  text-align: center;
  margin-bottom: 28px;
}

.header-icon {
  font-size: 48px;
  margin-bottom: 14px;
  animation: wave 2s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-8deg); }
  75% { transform: rotate(8deg); }
}

.form-header h2 {
  font-size: 30px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  letter-spacing: -0.5px;
}

.form-header p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

.login-form {
  background: white;
  padding: 28px 28px;
  border-radius: 20px;
  box-shadow: var(--shadow-soft);
  border: 1px solid var(--border-color);
}

.login-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.input-group {
  width: 100%;
}

.input-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
  letter-spacing: 0.5px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  padding: 4px 14px;
  box-shadow: none;
  border: 2px solid var(--border-color);
  background: var(--bg-light);
  transition: all 0.3s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-light);
  background: white;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-orange);
  background: white;
  box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
}

.login-form :deep(.el-input__inner) {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.login-form :deep(.el-input__prefix-inner) {
  color: var(--primary-orange);
  font-size: 18px;
}

.login-form :deep(.el-input__suffix-inner) {
  color: var(--text-muted);
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.custom-checkbox {
  font-size: 14px;
}

.custom-checkbox :deep(.el-checkbox__label) {
  color: var(--text-secondary);
  font-weight: 500;
}

.custom-checkbox :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--primary-orange);
  border-color: var(--primary-orange);
}

.forgot-link {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-orange);
  text-decoration: none;
  transition: all 0.2s;
}

.forgot-link:hover {
  color: var(--primary-dark);
}

/* 提交按钮 */
.submit-btn {
  width: 100% !important;
  height: 48px !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
  background: #E55A2B !important;
  border: none !important;
  box-shadow: 0 4px 16px rgba(229, 90, 43, 0.35) !important;
  transition: all 0.3s ease !important;
  letter-spacing: 1px !important;
  color: #FFFFFF !important;
}

.submit-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 24px rgba(229, 90, 43, 0.45) !important;
  background: #D14920 !important;
  color: #FFFFFF !important;
}

.submit-btn:active {
  transform: translateY(0) !important;
  color: #FFFFFF !important;
}

/* 确保Element Plus按钮文字颜色 */
.submit-btn :deep(.el-button__text) {
  color: #FFFFFF !important;
}

.submit-btn :deep(span) {
  color: #FFFFFF !important;
}

.submit-btn:active {
  transform: translateY(0);
}

/* 表单底部 */
.form-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.footer-text {
  color: var(--text-secondary);
  margin-right: 6px;
}

.register-link {
  color: var(--primary-orange);
  text-decoration: none;
  font-weight: 700;
  transition: all 0.2s;
}

.register-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

/* 底部装饰 */
.bottom-decoration {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  background: rgba(255, 107, 53, 0.08);
  border-radius: 30px;
  border: 1px solid rgba(255, 107, 53, 0.15);
}

.decoration-text {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-orange);
  letter-spacing: 2px;
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 1024px) {
  .brand-side {
    width: 50%;
  }

  .brand-title {
    font-size: 38px;
    letter-spacing: 4px;
  }

  .brand-subtitle {
    letter-spacing: 3px;
  }
}

@media (max-width: 768px) {
  .login-page {
    flex-direction: column;
  }

  .brand-side {
    width: 100%;
    min-height: 42vh;
    padding: 32px 24px;
  }

  .food-icons {
    display: none;
  }

  .brand-content {
    padding: 20px;
  }

  .chef-hat-container {
    margin-bottom: 16px;
  }

  .chef-hat {
    width: 70px;
    height: 70px;
  }

  .brand-title {
    font-size: 32px;
    letter-spacing: 3px;
  }

  .brand-subtitle {
    font-size: 11px;
    margin-bottom: 32px;
    letter-spacing: 2px;
  }

  .features-container {
    margin-bottom: 32px;
    gap: 10px;
  }

  .feature-item {
    padding: 12px 16px;
    font-size: 13px;
  }

  .feature-icon-wrapper {
    font-size: 18px;
  }

  .stats-row {
    gap: 20px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-label {
    font-size: 10px;
  }

  .form-side {
    padding: 32px 24px;
    flex: 1;
  }

  .form-wrapper {
    max-width: 100%;
  }

  .form-header {
    margin-bottom: 28px;
  }

  .header-icon {
    font-size: 44px;
    margin-bottom: 16px;
  }

  .form-header h2 {
    font-size: 28px;
  }

  .form-header p {
    font-size: 14px;
  }

  .login-form {
    padding: 28px 24px;
    border-radius: 20px;
  }

  .submit-btn {
    height: 50px;
    font-size: 16px;
  }

  .bottom-decoration {
    display: none;
  }
}

@media (max-width: 480px) {
  .brand-title {
    font-size: 26px;
    letter-spacing: 2px;
  }

  .brand-subtitle {
    font-size: 10px;
    letter-spacing: 1px;
  }

  .features-container {
    grid-template-columns: 1fr;
    max-width: 200px;
  }

  .form-header h2 {
    font-size: 24px;
  }

  .login-form {
    padding: 24px 16px;
  }

  .input-label {
    font-size: 12px;
  }

  .login-form :deep(.el-input__inner) {
    font-size: 14px;
  }

  .form-footer {
    font-size: 14px;
  }
}
</style>
