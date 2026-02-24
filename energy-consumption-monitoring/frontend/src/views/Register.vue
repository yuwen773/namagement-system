<template>
  <div class="register-container">
    <!-- Animated background elements -->
    <div class="background-gradient"></div>
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
      <div class="shape shape-4"></div>
    </div>

    <!-- Register Card -->
    <div class="register-card">
      <!-- Logo and Title -->
      <div class="register-header">
        <div class="logo-container">
          <svg class="logo-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M24 4L6 14V30C6 35.5225 10.4772 40 16 40H32C37.5228 40 42 35.5225 42 30V14L24 4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M18 24L22 28L30 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="24" cy="18" r="4" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <h1 class="register-title">创建账号</h1>
        <p class="register-subtitle">加入校园智慧能耗监测系统</p>
      </div>

      <!-- Register Form -->
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
        @submit.prevent="handleRegister"
      >
        <!-- Username Field -->
        <el-form-item prop="username">
          <div class="input-group">
            <label class="input-label">用户名</label>
            <div class="input-wrapper">
              <el-icon class="input-icon"><icon-ep-user /></el-icon>
              <el-input
                v-model="registerForm.username"
                placeholder="请输入用户名"
                size="large"
                clearable
              />
            </div>
          </div>
        </el-form-item>

        <!-- Real Name Field -->
        <el-form-item prop="realName">
          <div class="input-group">
            <label class="input-label">真实姓名</label>
            <div class="input-wrapper">
              <el-icon class="input-icon"><icon-ep-avatar /></el-icon>
              <el-input
                v-model="registerForm.realName"
                placeholder="请输入真实姓名"
                size="large"
                clearable
              />
            </div>
          </div>
        </el-form-item>

        <!-- Phone Field -->
        <el-form-item prop="phone">
          <div class="input-group">
            <label class="input-label">手机号码</label>
            <div class="input-wrapper">
              <el-icon class="input-icon"><icon-ep-phone /></el-icon>
              <el-input
                v-model="registerForm.phone"
                placeholder="请输入手机号码"
                size="large"
                clearable
                maxlength="11"
              />
            </div>
          </div>
        </el-form-item>

        <!-- Email Field (Optional) -->
        <el-form-item prop="email">
          <div class="input-group">
            <label class="input-label">邮箱 <span class="optional">(可选)</span></label>
            <div class="input-wrapper">
              <el-icon class="input-icon"><icon-ep-message /></el-icon>
              <el-input
                v-model="registerForm.email"
                placeholder="请输入邮箱地址"
                size="large"
                clearable
              />
            </div>
          </div>
        </el-form-item>

        <!-- Password Field -->
        <el-form-item prop="password">
          <div class="input-group">
            <label class="input-label">设置密码</label>
            <div class="input-wrapper">
              <el-icon class="input-icon"><icon-ep-lock /></el-icon>
              <el-input
                v-model="registerForm.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请设置密码（6-32位）"
                size="large"
                @input="checkPasswordStrength"
              >
                <template #suffix>
                  <el-icon
                    class="password-toggle"
                    @click="showPassword = !showPassword"
                  >
                    <icon-ep-view v-if="!showPassword" />
                    <icon-ep-hide v-else />
                  </el-icon>
                </template>
              </el-input>
            </div>
            <!-- Password Strength Indicator -->
            <div v-if="registerForm.password" class="password-strength">
              <div class="strength-bar">
                <div
                  class="strength-fill"
                  :class="`strength-${passwordStrength.level}`"
                  :style="{ width: passwordStrength.percent }"
                ></div>
              </div>
              <span class="strength-text" :class="`strength-${passwordStrength.level}`">
                {{ passwordStrength.text }}
              </span>
            </div>
          </div>
        </el-form-item>

        <!-- Confirm Password Field -->
        <el-form-item prop="confirmPassword">
          <div class="input-group">
            <label class="input-label">确认密码</label>
            <div class="input-wrapper">
              <el-icon class="input-icon"><icon-ep-lock /></el-icon>
              <el-input
                v-model="registerForm.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="请再次输入密码"
                size="large"
              >
                <template #suffix>
                  <el-icon
                    class="password-toggle"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    <icon-ep-view v-if="!showConfirmPassword" />
                    <icon-ep-hide v-else />
                  </el-icon>
                </template>
              </el-input>
            </div>
          </div>
        </el-form-item>

        <!-- Error Message -->
        <transition name="el-zoom-in-top">
          <div v-if="errorMessage" class="error-message">
            <el-icon><icon-ep-warning-filled /></el-icon>
            <span>{{ errorMessage }}</span>
          </div>
        </transition>

        <!-- Register Button -->
        <el-button
          type="primary"
          size="large"
          class="register-button"
          :loading="loading"
          @click="handleRegister"
        >
          <template v-if="!loading">
            <span>立即注册</span>
          </template>
          <template v-else>
            <span>注册中...</span>
          </template>
        </el-button>
      </el-form>

      <!-- Footer -->
      <div class="register-footer">
        <p>已有账号？ <router-link to="/login" class="login-link">立即登录</router-link></p>
      </div>
    </div>

    <!-- Copyright -->
    <div class="copyright">
      <p>&copy; 2024 校园智慧能耗监测系统</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { register } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

// Form ref
const registerFormRef = ref(null)

// Form state
const registerForm = reactive({
  username: '',
  realName: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: '',
})

// UI state
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const errorMessage = ref('')

// Password strength
const passwordStrength = ref({
  level: 'weak',
  text: '弱',
  percent: '33%',
})

// Custom validator for confirm password
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// Custom validator for phone
const validatePhone = (rule, value, callback) => {
  const phoneRegex = /^1[3-9]\d{9}$/
  if (value && !phoneRegex.test(value)) {
    callback(new Error('请输入正确的手机号码'))
  } else {
    callback()
  }
}

// Custom validator for email
const validateEmail = (rule, value, callback) => {
  if (value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      callback(new Error('请输入正确的邮箱地址'))
    } else {
      callback()
    }
  } else {
    callback()
  }
}

// Form validation rules
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' },
  ],
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度为2-20个字符', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { validator: validatePhone, trigger: 'blur' },
  ],
  email: [
    { validator: validateEmail, trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 32, message: '密码长度为6-32个字符', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
}

// Check password strength
function checkPasswordStrength() {
  const password = registerForm.password
  if (!password) {
    passwordStrength.value = { level: 'weak', text: '弱', percent: '33%' }
    return
  }

  let score = 0
  if (password.length >= 8) score++
  if (password.length >= 12) score++
  if (/[a-z]/.test(password)) score++
  if (/[A-Z]/.test(password)) score++
  if (/[0-9]/.test(password)) score++
  if (/[^a-zA-Z0-9]/.test(password)) score++

  if (score <= 2) {
    passwordStrength.value = { level: 'weak', text: '弱', percent: '33%' }
  } else if (score <= 4) {
    passwordStrength.value = { level: 'medium', text: '中等', percent: '66%' }
  } else {
    passwordStrength.value = { level: 'strong', text: '强', percent: '100%' }
  }
}

// Handle register
async function handleRegister() {
  // Clear previous error
  errorMessage.value = ''

  // Validate form
  const valid = await registerFormRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    // Call register API (always register as USER role)
    const response = await register({
      username: registerForm.username,
      password: registerForm.password,
      real_name: registerForm.realName,
      phone: registerForm.phone,
      email: registerForm.email || undefined,
      role: 'USER', // Always register as regular user
    })

    // Check response format
    if (response.code === 0 && response.data) {
      const { access, refresh, user_info } = response.data

      // Save token and user info to store (auto-login)
      userStore.setToken(access)
      userStore.setUserInfo(user_info)

      // Save refresh token
      localStorage.setItem('refreshToken', refresh)

      // Show success message
      ElMessage.success('注册成功，欢迎加入！')

      // Redirect to user dashboard
      router.push('/user/dashboard')
    } else {
      // Show error message
      errorMessage.value = response.message || '注册失败，请稍后重试'
    }
  } catch (error) {
    console.error('Registration error:', error)
    errorMessage.value = error.response?.data?.message || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// Focus username input on mount
onMounted(() => {
  const firstInput = document.querySelector('.register-form input')
  firstInput?.focus()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

.register-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-family: 'Poppins', 'Noto Sans SC', sans-serif;
  padding: 20px 0;
}

/* Animated gradient background */
.background-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #c2410c 100%);
  background-size: 200% 200%;
  animation: gradientShift 20s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Floating shapes with enhanced animation */
.floating-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.shape {
  position: absolute;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  animation: float 25s ease-in-out infinite;
  backdrop-filter: blur(40px);
}

.shape-1 {
  width: 350px;
  height: 350px;
  top: -120px;
  left: -120px;
  animation-delay: 0s;
}

.shape-2 {
  width: 250px;
  height: 250px;
  bottom: -80px;
  right: -80px;
  animation-delay: -7s;
}

.shape-3 {
  width: 180px;
  height: 180px;
  top: 40%;
  right: 15%;
  animation-delay: -14s;
}

.shape-4 {
  width: 120px;
  height: 120px;
  bottom: 30%;
  left: 10%;
  animation-delay: -21s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.25;
  }
  25% {
    transform: translate(40px, -40px) rotate(90deg) scale(1.05);
    opacity: 0.4;
  }
  50% {
    transform: translate(-30px, 30px) rotate(180deg) scale(0.95);
    opacity: 0.25;
  }
  75% {
    transform: translate(30px, 40px) rotate(270deg) scale(1.05);
    opacity: 0.4;
  }
}

/* Register card with enhanced glassmorphism */
.register-card {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 460px;
  margin: 20px;
  padding: 48px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(30px);
  border-radius: 28px;
  box-shadow:
    0 30px 60px -15px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  animation: cardAppear 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.92);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Enhanced header */
.register-header {
  text-align: center;
  margin-bottom: 36px;
}

.logo-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 20px;
  color: white;
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.4);
  animation: logoFloat 1s ease-out 0.3s both;
}

@keyframes logoFloat {
  0% {
    opacity: 0;
    transform: scale(0.4) rotate(-90deg);
  }
  70% {
    transform: scale(1.05) rotate(5deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.logo-icon {
  width: 40px;
  height: 40px;
}

.register-title {
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
  letter-spacing: -0.5px;
}

.register-subtitle {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
}

/* Enhanced form layout */
.register-form {
  margin-top: 28px;
}

.register-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  letter-spacing: 0.3px;
}

.optional {
  font-weight: 400;
  color: #9ca3af;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  z-index: 10;
  font-size: 18px;
  color: #9ca3af;
  transition: all 0.3s ease;
}

.register-form :deep(.el-input__wrapper) {
  padding-left: 50px;
  padding-right: 16px;
  height: 50px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.register-form :deep(.el-input__wrapper:hover) {
  border-color: #fdba74;
  background: #fff;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

.register-form :deep(.el-input__wrapper.is-focus) {
  border-color: #f97316;
  background: #fff;
  box-shadow:
    0 0 0 4px rgba(249, 115, 22, 0.1),
    0 4px 16px rgba(249, 115, 22, 0.2);
}

.register-form :deep(.el-input__inner) {
  font-family: 'Poppins', sans-serif;
  font-size: 15px;
  color: #1f2937;
  background: transparent;
}

.register-form :deep(.el-input__wrapper.is-focus) ~ .input-icon,
.input-wrapper:focus-within .input-icon {
  color: #f97316;
  transform: scale(1.1);
}

/* Enhanced password strength indicator */
.password-strength {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.strength-bar {
  flex: 1;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  border-radius: 3px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.strength-fill::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3));
  border-radius: 3px;
}

.strength-fill.strength-weak {
  background: linear-gradient(90deg, #ef4444, #f87171);
  width: 33% !important;
}

.strength-fill.strength-medium {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
  width: 66% !important;
}

.strength-fill.strength-strong {
  background: linear-gradient(90deg, #22c55e, #4ade80);
  width: 100% !important;
}

.strength-text {
  font-size: 13px;
  font-weight: 600;
  min-width: 32px;
  text-align: right;
}

.strength-text.strength-weak {
  color: #ef4444;
}

.strength-text.strength-medium {
  color: #f59e0b;
}

.strength-text.strength-strong {
  color: #22c55e;
}

/* Password toggle */
.password-toggle {
  cursor: pointer;
  color: #9ca3af;
  transition: all 0.3s ease;
  padding: 4px;
}

.password-toggle:hover {
  color: #f97316;
  transform: scale(1.1);
}

/* Enhanced error message */
.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
}

.error-message .el-icon {
  flex-shrink: 0;
  font-size: 20px;
}

/* Enhanced register button */
.register-button {
  width: 100%;
  height: 52px;
  margin-top: 24px;
  font-size: 17px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 14px;
  box-shadow:
    0 6px 20px rgba(249, 115, 22, 0.4),
    0 0 0 0 rgba(249, 115, 22, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.register-button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.register-button:hover::before {
  opacity: 1;
}

.register-button:hover {
  transform: translateY(-3px);
  box-shadow:
    0 10px 30px rgba(249, 115, 22, 0.5),
    0 0 0 0 rgba(249, 115, 22, 0.2);
}

.register-button:active {
  transform: translateY(-1px);
}

.register-button.is-loading {
  opacity: 0.85;
}

/* Footer */
.register-footer {
  margin-top: 28px;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #f3f4f6;
}

.register-footer p {
  margin: 0;
  font-size: 15px;
  color: #6b7280;
}

.login-link {
  color: #f97316;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
}

.login-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #f97316;
  transition: width 0.3s ease;
}

.login-link:hover::after {
  width: 100%;
}

/* Copyright */
.copyright {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  color: rgba(255, 255, 255, 0.85);
  font-size: 13px;
  z-index: 10;
}

/* Responsive design */
@media (max-width: 480px) {
  .register-card {
    margin: 16px;
    padding: 32px 24px;
    border-radius: 24px;
  }

  .register-title {
    font-size: 24px;
  }

  .register-subtitle {
    font-size: 13px;
  }

  .shape {
    display: none;
  }

  .logo-container {
    width: 64px;
    height: 64px;
  }

  .logo-icon {
    width: 36px;
    height: 36px;
  }
}

/* Element Plus customizations */
:deep(.el-form-item__error) {
  font-size: 12px;
  margin-top: 4px;
  padding-left: 4px;
  color: #ef4444;
}

:deep(.el-input__clear) {
  font-size: 16px;
}
</style>
