<template>
  <div class="register-page">
    <!-- 左侧品牌展示区 -->
    <div class="brand-side">
      <!-- 装饰性食物图标 -->
      <div class="food-icons">
        <div class="food-icon food-icon-1">🍕</div>
        <div class="food-icon food-icon-2">🍔</div>
        <div class="food-icon food-icon-3">🌮</div>
        <div class="food-icon food-icon-4">🍣</div>
        <div class="food-icon food-icon-5">🥘</div>
        <div class="food-icon food-icon-6">🍛</div>
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

        <h1 class="brand-title">加入我们</h1>
        <p class="brand-subtitle">Start Your Journey</p>

        <!-- 优势展示 -->
        <div class="features-container">
          <div class="feature-item" v-for="(feature, idx) in features" :key="idx">
            <div class="feature-icon-wrapper">{{ feature.icon }}</div>
            <span class="feature-text">{{ feature.text }}</span>
          </div>
        </div>

        <!-- 统计数据 -->
        <div class="stats-row">
          <div class="stat-item">
            <div class="stat-value">10k+</div>
            <div class="stat-label">活跃用户</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-value">24/7</div>
            <div class="stat-label">技术支持</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧注册表单区 -->
    <div class="form-side">
      <div class="form-wrapper">
        <div class="form-header">
          <div class="header-icon">📝</div>
          <h2>创建账号</h2>
          <p>填写信息，开始使用食堂管理系统</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <div class="input-group">
              <div class="input-label">用户名</div>
              <el-input
                v-model="form.username"
                size="large"
                placeholder="请输入用户名"
                :prefix-icon="User"
                clearable
                @keyup.enter="handleRegister"
              />
            </div>
          </el-form-item>

          <el-form-item prop="phone">
            <div class="input-group">
              <div class="input-label">手机号</div>
              <el-input
                v-model="form.phone"
                size="large"
                placeholder="请输入手机号"
                :prefix-icon="Phone"
                clearable
                @keyup.enter="handleRegister"
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
                placeholder="请输入密码（至少4位）"
                :prefix-icon="Lock"
                show-password
                clearable
                @keyup.enter="handleRegister"
              />
            </div>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <div class="input-group">
              <div class="input-label">确认密码</div>
              <el-input
                v-model="form.confirmPassword"
                type="password"
                size="large"
                placeholder="请再次输入密码"
                :prefix-icon="Lock"
                show-password
                clearable
                @keyup.enter="handleRegister"
              />
            </div>
          </el-form-item>

          <el-form-item prop="email">
            <div class="input-group">
              <div class="input-label">邮箱（选填）</div>
              <el-input
                v-model="form.email"
                size="large"
                placeholder="请输入邮箱地址"
                :prefix-icon="Message"
                clearable
                @keyup.enter="handleRegister"
              />
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="submit-btn"
              :loading="loading"
              @click="handleRegister"
            >
              <span v-if="!loading">立即注册</span>
              <span v-else>注册中...</span>
            </el-button>
          </el-form-item>
        </el-form>

        <div class="form-footer">
          <span class="footer-text">已有账号？</span>
          <router-link to="/login" class="login-link">
            立即登录 →
          </router-link>
        </div>
      </div>

      <!-- 底部装饰 -->
      <div class="bottom-decoration">
        <span class="decoration-text">🍽️ 简单注册 · 快速上手</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Phone, Message } from '@element-plus/icons-vue'
import { register } from '@/api/auth'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  phone: '',
  email: ''
})

const features = [
  { icon: '⚡', text: '快速入职' },
  { icon: '📅', text: '智能排班' },
  { icon: '📱', text: '移动办公' },
  { icon: '🔒', text: '数据安全' }
]

// 密码验证
const validatePassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入密码'))
  } else if (value.length < 4) {
    callback(new Error('密码至少需要4位'))
  } else {
    if (form.confirmPassword) {
      formRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

// 确认密码验证
const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 手机号验证
const validatePhone = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入手机号'))
  } else if (!/^1[3-9]\d{9}$/.test(value)) {
    callback(new Error('请输入正确的手机号'))
  } else {
    callback()
  }
}

// 邮箱验证
const validateEmail = (rule, value, callback) => {
  if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    callback(new Error('请输入正确的邮箱地址'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, message: '用户名至少需要2位', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  phone: [
    { required: true, validator: validatePhone, trigger: 'blur' }
  ],
  email: [
    { validator: validateEmail, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    const { confirmPassword, ...registerData } = form
    const response = await register(registerData)

    if (response.code === 201) {
      ElMessage.success('注册成功！即将跳转到登录页...')
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      ElMessage.error(response.message || '注册失败，请重试')
    }
  } catch (error) {
    console.error('注册错误:', error)
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error.response?.data?.username) {
      ElMessage.error(error.response.data.username[0] || '用户名已存在')
    } else {
      ElMessage.error('注册失败，请检查网络连接')
    }
  } finally {
    loading.value = false
  }
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
.register-page {
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
  background: linear-gradient(135deg, #F7C52D 0%, #FFA552 35%, #FF8C42 65%, #FF6B35 100%);
}

.bg-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 30% 40%, rgba(255, 255, 255, 0.15) 0%, transparent 50%),
              radial-gradient(ellipse at 70% 60%, rgba(255, 107, 53, 0.2) 0%, transparent 50%);
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
  background: linear-gradient(90deg, var(--secondary-yellow), var(--primary-orange));
}

.form-wrapper {
  width: 100%;
  max-width: 420px;
}

.form-header {
  text-align: center;
  margin-bottom: 20px;
}

.header-icon {
  font-size: 42px;
  margin-bottom: 10px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.form-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px 0;
  letter-spacing: -0.5px;
}

.form-header p {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

.register-form {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: var(--shadow-soft);
  border: 1px solid var(--border-color);
}

.register-form :deep(.el-form-item) {
  margin-bottom: 14px;
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

.register-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  padding: 4px 14px;
  box-shadow: none;
  border: 2px solid var(--border-color);
  background: var(--bg-light);
  transition: all 0.3s ease;
}

.register-form :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-light);
  background: white;
}

.register-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-orange);
  background: white;
  box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
}

.register-form :deep(.el-input__inner) {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.register-form :deep(.el-input__prefix-inner) {
  color: var(--primary-orange);
  font-size: 18px;
}

.register-form :deep(.el-input__suffix-inner) {
  color: var(--text-muted);
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
  margin-top: 6px !important;

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

/* 表单底部 */
.form-footer {
  text-align: center;
  margin-top: 8px;
  margin-bottom: 44px;
  font-size: 14px;
}

.footer-text {
  color: var(--text-secondary);
  margin-right: 6px;
}

.login-link {
  color: var(--primary-orange);
  text-decoration: none;
  font-weight: 700;
  transition: all 0.2s;
}

.login-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

/* 底部装饰 */
.bottom-decoration {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  background: rgba(247, 197, 45, 0.1);
  border-radius: 30px;
  border: 1px solid rgba(247, 197, 45, 0.2);
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
  .register-page {
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
    max-height: none;
    overflow: visible;
  }

  .form-header {
    margin-bottom: 24px;
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

  .register-form {
    padding: 24px 20px;
    border-radius: 20px;
    max-height: none;
    overflow: visible;
  }

  .register-form :deep(.el-form-item) {
    margin-bottom: 18px;
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

  .register-form {
    padding: 20px 16px;
  }

  .input-label {
    font-size: 12px;
  }

  .register-form :deep(.el-input__inner) {
    font-size: 14px;
  }

  .form-footer {
    font-size: 14px;
  }

  .submit-btn {
    height: 48px;
    font-size: 15px;
  }
}
</style>
