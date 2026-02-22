<template>
  <div class="register-page">
    <div class="register-container">
      <!-- Left Side - Brand -->
      <div class="brand-section">
        <div class="brand-logo">
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="24" cy="24" r="16" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M24 12V36M16 24H32" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="24" cy="24" r="4" fill="currentColor"/>
          </svg>
        </div>
        <h1 class="brand-title">创建账号</h1>
        <p class="brand-subtitle">加入空气质量监测平台</p>

        <div class="features">
          <div class="feature-item">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18C14.4183 18 18 14.4183 18 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M10 6V10L13 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>实时数据监测</span>
          </div>
          <div class="feature-item">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M7 10H13M10 7V13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <span>历史数据分析</span>
          </div>
          <div class="feature-item">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M10 6V10L13 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>智能防护建议</span>
          </div>
          <div class="feature-item">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 3V17H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 11L11 7L15 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>数据可视化报告</span>
          </div>
        </div>
      </div>

      <!-- Right Side - Register Form -->
      <div class="form-section">
        <div class="form-header">
          <h2 class="form-title">注册账号</h2>
          <p class="form-subtitle">填写信息创建新账号</p>
        </div>

        <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" class="register-form" @submit.prevent="handleRegister">
          <el-form-item prop="username">
            <label class="input-label">用户名</label>
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
            />
          </el-form-item>

          <el-form-item prop="email">
            <label class="input-label">邮箱</label>
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱地址"
              size="large"
            />
          </el-form-item>

          <el-form-item prop="phone">
            <label class="input-label">手机号（选填）</label>
            <el-input
              v-model="registerForm.phone"
              placeholder="请输入手机号码"
              size="large"
            />
          </el-form-item>

          <el-form-item prop="password">
            <label class="input-label">密码</label>
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password
              @input="updatePasswordStrength"
            />
            <!-- Password Strength Indicator -->
            <div class="password-strength" v-if="registerForm.password">
              <div class="strength-bar">
                <div class="strength-fill" :class="strengthClass" :style="{ width: passwordStrength + '%' }"></div>
              </div>
              <span class="strength-text">{{ strengthText }}</span>
            </div>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <label class="input-label">确认密码</label>
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              size="large"
              show-password
            />
          </el-form-item>

          <el-button
            type="primary"
            size="large"
            class="register-btn"
            :loading="loading"
            @click="handleRegister"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form>

        <div class="form-footer">
          <span>已有账号？</span>
          <router-link to="/login" class="login-link">立即登录</router-link>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="success-modal" @click="showSuccessModal = false">
      <div class="success-content" @click.stop>
        <div class="success-icon">
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="24" cy="24" r="20" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M16 24L21 29L32 18" stroke="var(--success)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3 class="success-title">注册成功！</h3>
        <p class="success-message">欢迎加入空气质量监测平台</p>
        <el-button type="primary" class="success-btn" @click="router.push('/login')">
          前往登录
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/auth'

const router = useRouter()

const registerFormRef = ref(null)
const loading = ref(false)
const showSuccessModal = ref(false)
const passwordStrength = ref(0)

const registerForm = ref({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为 3-20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为 6-20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const strengthClass = computed(() => {
  if (passwordStrength.value <= 20) return 'weak'
  if (passwordStrength.value <= 40) return 'fair'
  if (passwordStrength.value <= 60) return 'good'
  return 'strong'
})

const strengthText = computed(() => {
  if (passwordStrength.value <= 20) return '弱'
  if (passwordStrength.value <= 40) return '一般'
  if (passwordStrength.value <= 60) return '中等'
  return '强'
})

const updatePasswordStrength = () => {
  const password = registerForm.value.password
  if (!password) {
    passwordStrength.value = 0
    return
  }

  let strength = 0
  if (password.length >= 6) strength += 20
  if (password.length >= 10) strength += 10
  if (/[a-z]/.test(password)) strength += 15
  if (/[A-Z]/.test(password)) strength += 15
  if (/\d/.test(password)) strength += 15
  if (/[^a-zA-Z0-9]/.test(password)) strength += 25

  passwordStrength.value = Math.min(strength, 100)
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return

    loading.value = true

    const { confirmPassword, phone, ...registerData } = registerForm.value
    await register(registerData)

    showSuccessModal.value = true
  } catch (error) {
    // Error is handled by request interceptor
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-main);
  padding: var(--spacing-xl);
}

.register-container {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  max-width: 1100px;
  width: 100%;
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

/* Brand Section */
.brand-section {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  padding: var(--spacing-2xl);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.brand-logo {
  width: 56px;
  height: 56px;
  margin-bottom: var(--spacing-lg);
  color: white;
}

.brand-logo svg {
  width: 100%;
  height: 100%;
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  color: white;
}

.brand-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: var(--spacing-2xl);
  color: white;
}

.features {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  font-size: 14px;
  color: white;
}

.feature-item svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  opacity: 0.9;
}

/* Form Section */
.form-section {
  padding: var(--spacing-2xl);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-header {
  margin-bottom: var(--spacing-xl);
}

.form-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: var(--spacing-xs);
}

.form-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.input-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
  margin-bottom: var(--spacing-sm);
}

:deep(.el-input__wrapper) {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: none;
  transition: all var(--transition-fast);
}

:deep(.el-input__wrapper:hover) {
  border-color: var(--primary);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

:deep(.el-input__inner) {
  color: var(--text);
  font-size: 14px;
}

/* Password Strength */
.password-strength {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-sm);
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: all var(--transition-base);
  border-radius: var(--radius-sm);
}

.strength-fill.weak {
  background: var(--error);
}

.strength-fill.fair {
  background: var(--warning);
}

.strength-fill.good {
  background: var(--info);
}

.strength-fill.strong {
  background: var(--success);
}

.strength-text {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  min-width: 32px;
}

.register-btn {
  width: 100%;
  height: 44px;
  margin-top: var(--spacing-sm);
  font-size: 15px;
  font-weight: 500;
  border-radius: var(--radius-md);
}

.form-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-lg);
  font-size: 14px;
  color: var(--text-secondary);
}

.login-link {
  color: var(--primary);
  font-weight: 500;
  text-decoration: none;
}

.login-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

/* Success Modal */
.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fade-in var(--transition-base);
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.success-content {
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  text-align: center;
  box-shadow: var(--shadow-xl);
  animation: slide-up var(--transition-base);
  max-width: 360px;
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--spacing-lg);
  color: var(--success);
}

.success-icon svg {
  width: 100%;
  height: 100%;
}

.success-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: var(--spacing-xs);
}

.success-message {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
}

.success-btn {
  padding: 12px 40px;
  border-radius: var(--radius-md);
}

/* Responsive */
@media (max-width: 768px) {
  .register-container {
    grid-template-columns: 1fr;
    max-width: 450px;
  }

  .brand-section {
    padding: var(--spacing-xl);
    text-align: center;
  }

  .brand-logo {
    margin: 0 auto var(--spacing-md);
  }

  .features {
    display: none;
  }

  .form-section {
    padding: var(--spacing-xl);
  }
}
</style>
