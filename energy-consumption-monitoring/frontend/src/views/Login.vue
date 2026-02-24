<template>
  <div class="login-container">
    <!-- Animated background elements -->
    <div class="background-gradient"></div>
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <!-- Login Card -->
    <div class="login-card">
      <!-- Logo and Title -->
      <div class="login-header">
        <div class="logo-container">
          <svg class="logo-icon" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M24 4L6 14V30C6 35.5225 10.4772 40 16 40H32C37.5228 40 42 35.5225 42 30V14L24 4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M18 24L22 28L30 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="24" cy="18" r="4" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <h1 class="login-title">校园智慧能耗监测</h1>
        <p class="login-subtitle">Campus Smart Energy Monitoring System</p>
      </div>

      <!-- Login Form -->
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <!-- Username Field -->
        <el-form-item prop="username">
          <div class="input-wrapper">
            <el-icon class="input-icon"><icon-ep-user /></el-icon>
            <el-input
              v-model="loginForm.username"
              placeholder="用户名 / Username"
              size="large"
              clearable
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <span></span>
              </template>
            </el-input>
          </div>
        </el-form-item>

        <!-- Password Field -->
        <el-form-item prop="password">
          <div class="input-wrapper">
            <el-icon class="input-icon"><icon-ep-lock /></el-icon>
            <el-input
              v-model="loginForm.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="密码 / Password"
              size="large"
              @keyup.enter="handleLogin"
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
        </el-form-item>

        <!-- Remember Me & Forgot Password -->
        <div class="form-options">
          <el-checkbox v-model="loginForm.remember" class="remember-checkbox">
            记住我 / Remember me
          </el-checkbox>
        </div>

        <!-- Error Message -->
        <transition name="el-zoom-in-top">
          <div v-if="errorMessage" class="error-message">
            <el-icon><icon-ep-warning-filled /></el-icon>
            <span>{{ errorMessage }}</span>
          </div>
        </transition>

        <!-- Login Button -->
        <el-button
          type="primary"
          size="large"
          class="login-button"
          :loading="loading"
          @click="handleLogin"
        >
          <template v-if="!loading">
            <span>登 录 / Login</span>
          </template>
          <template v-else>
            <span>登录中...</span>
          </template>
        </el-button>
      </el-form>

      <!-- Register Link -->
      <div class="login-footer">
        <p>还没有账号？ <router-link to="/register" class="register-link">立即注册</router-link></p>
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
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { login } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// Form ref
const loginFormRef = ref(null)

// Form state
const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
})

// UI state
const loading = ref(false)
const showPassword = ref(false)
const errorMessage = ref('')

// Form validation rules
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' },
  ],
}

// Handle login
async function handleLogin() {
  // Clear previous error
  errorMessage.value = ''

  // Validate form
  const valid = await loginFormRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    // Call login API
    const response = await login({
      username: loginForm.username,
      password: loginForm.password,
    })

    // Check response format
    if (response.code === 0 && response.data) {
      const { access, refresh, user_info } = response.data

      // Save token and user info to store
      userStore.setToken(access)
      userStore.setUserInfo(user_info)

      // Save refresh token if remember me is checked
      if (loginForm.remember) {
        localStorage.setItem('refreshToken', refresh)
      }

      // Show success message
      ElMessage.success('登录成功 / Login successful')

      // Redirect based on role
      const redirectPath = route.query.redirect || '/'
      if (user_info.role === 'ADMIN') {
        router.push(redirectPath.startsWith('/admin') ? redirectPath : '/admin/dashboard')
      } else {
        router.push(redirectPath.startsWith('/user') ? redirectPath : '/user/dashboard')
      }
    } else {
      // Show error message
      errorMessage.value = response.message || '登录失败，请检查用户名和密码'
    }
  } catch (error) {
    console.error('Login error:', error)
    errorMessage.value = error.response?.data?.message || '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

// Focus username input on mount
onMounted(() => {
  // Auto-focus first input
  const firstInput = document.querySelector('.login-form input')
  firstInput?.focus()
})
</script>

<style scoped>
/* Import distinctive font */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Poppins:wght@400;500;600;700&display=swap');

.login-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-family: 'Poppins', 'Noto Sans SC', sans-serif;
}

/* Animated gradient background */
.background-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #c2410c 100%);
  background-size: 200% 200%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Floating shapes for visual interest */
.floating-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.shape {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 20s ease-in-out infinite;
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  right: -50px;
  animation-delay: -5s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  right: 10%;
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
    opacity: 0.3;
  }
  25% {
    transform: translate(30px, -30px) rotate(90deg);
    opacity: 0.5;
  }
  50% {
    transform: translate(-20px, 20px) rotate(180deg);
    opacity: 0.3;
  }
  75% {
    transform: translate(20px, 30px) rotate(270deg);
    opacity: 0.5;
  }
}

/* Login card with glassmorphism effect */
.login-card {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  margin: 20px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow:
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
  animation: cardAppear 0.6s ease-out;
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Header section */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 16px;
  color: white;
  animation: logoBounce 0.8s ease-out 0.2s both;
}

@keyframes logoBounce {
  0% {
    opacity: 0;
    transform: scale(0.5) rotate(-180deg);
  }
  60% {
    transform: scale(1.1) rotate(10deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.logo-icon {
  width: 36px;
  height: 36px;
}

.login-title {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
  letter-spacing: -0.5px;
}

.login-subtitle {
  margin: 0;
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* Form styling */
.login-form {
  margin-top: 32px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  z-index: 10;
  color: #9ca3af;
  transition: color 0.3s ease;
}

.login-form :deep(.el-input__wrapper) {
  padding-left: 44px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.15);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow:
    0 0 0 3px rgba(249, 115, 22, 0.1),
    0 2px 8px rgba(249, 115, 22, 0.2);
}

.login-form :deep(.el-input__inner) {
  font-family: 'Poppins', sans-serif;
  font-size: 15px;
}

.login-form :deep(.el-input__wrapper.is-focus) ~ .input-icon,
.input-wrapper:focus-within .input-icon {
  color: #f97316;
}

/* Password toggle */
.password-toggle {
  cursor: pointer;
  color: #9ca3af;
  transition: color 0.3s ease;
}

.password-toggle:hover {
  color: #f97316;
}

/* Form options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.remember-checkbox :deep(.el-checkbox__label) {
  font-size: 14px;
  color: #6b7280;
}

.remember-checkbox :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #f97316;
  border-color: #f97316;
}

/* Error message */
.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  margin-bottom: 20px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #dc2626;
  font-size: 14px;
}

.error-message .el-icon {
  flex-shrink: 0;
  font-size: 18px;
}

/* Login button */
.login-button {
  width: 100%;
  height: 48px;
  margin-top: 8px;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(249, 115, 22, 0.4);
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.5);
}

.login-button:active {
  transform: translateY(0);
}

.login-button.is-loading {
  opacity: 0.8;
}

/* Footer */
.login-footer {
  margin-top: 24px;
  text-align: center;
}

.login-footer p {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

.register-link {
  color: #f97316;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.register-link:hover {
  color: #ea580c;
  text-decoration: underline;
}

/* Copyright */
.copyright {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
  z-index: 10;
}

/* Responsive design */
@media (max-width: 480px) {
  .login-card {
    margin: 16px;
    padding: 28px 20px;
  }

  .login-title {
    font-size: 20px;
  }

  .login-subtitle {
    font-size: 12px;
  }

  .shape {
    display: none;
  }
}

/* Element Plus customizations */
:deep(.el-form-item__error) {
  font-size: 12px;
  margin-top: 6px;
}
</style>
