<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { isValidPhone, isValidPassword } from '@/utils'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  nickname: ''
})

const loading = ref(false)

async function handleRegister() {
  if (!form.value.username) {
    ElMessage.warning('请输入手机号')
    return
  }
  if (!isValidPhone(form.value.username)) {
    ElMessage.warning('请输入正确的手机号')
    return
  }
  if (!form.value.password) {
    ElMessage.warning('请输入密码')
    return
  }
  if (!isValidPassword(form.value.password)) {
    ElMessage.warning('密码长度6-20位，必须包含字母和数字')
    return
  }
  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  loading.value = true
  try {
    await authStore.register({
      username: form.value.username,
      password: form.value.password,
      nickname: form.value.nickname || form.value.username
    })
    ElMessage.success('注册成功')
    router.push({ name: 'home' })
  } catch (error) {
    ElMessage.error(error.message || '注册失败')
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="register-view">
    <!-- Left Panel - Brand -->
    <div class="register-brand">
      <div class="brand-bg"></div>
      <div class="brand-grid"></div>
      <div class="brand-content">
        <div class="brand-logo">
          <div class="logo-icon">CP</div>
          <span class="logo-text">CAR PARTS</span>
        </div>
        <h1 class="brand-title">Join The Club</h1>
        <p class="brand-subtitle">Create your account and unlock exclusive member benefits</p>
        <div class="brand-features">
          <div class="brand-feature">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none">
              <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>10,000+ Premium Parts</span>
          </div>
          <div class="brand-feature">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none">
              <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Exclusive Member Deals</span>
          </div>
          <div class="brand-feature">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none">
              <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Expert Support Team</span>
          </div>
          <div class="brand-feature">
            <svg class="feature-icon" viewBox="0 0 24 24" fill="none">
              <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Fast Secure Shipping</span>
          </div>
        </div>
      </div>
      <div class="brand-accent"></div>
    </div>

    <!-- Right Panel - Register Form -->
    <div class="register-form-panel">
      <div class="form-content">
        <div class="form-header">
          <span class="form-badge">New Account</span>
          <h2 class="form-title">Create Account</h2>
          <p class="form-subtitle">Fill in your details to get started</p>
        </div>

        <el-form :model="form" label-position="top" class="register-form">
          <el-form-item label="Phone Number">
            <el-input
              v-model="form.username"
              placeholder="Enter your phone number"
              size="large"
              maxlength="11"
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M22 16.92V19.92C22.0021 20.1986 21.9441 20.4742 21.8295 20.7294C21.7149 20.9846 21.5464 21.2137 21.3344 21.4019C21.1224 21.59 20.8716 21.7336 20.5984 21.8228C20.3252 21.912 20.0356 21.9452 19.748 21.92C16.9483 21.5857 14.2664 20.6341 11.924 19.14C9.76182 17.7854 7.94663 15.9704 6.592 13.808C5.092 11.458 4.14 8.768 3.808 5.968C3.78279 5.68123 3.81556 5.39242 3.90418 5.11985C3.9928 4.84728 4.13538 4.59694 4.32263 4.38526C4.50988 4.17358 4.73785 4.00505 4.99216 3.89012C5.24647 3.77518 5.52127 3.71648 5.8 3.718H8.8C9.2982 3.71331 9.77931 3.90254 10.1488 4.2478C10.5183 4.59306 10.7496 5.06912 10.796 5.576C10.8824 6.58074 11.0883 7.57123 11.408 8.528C11.5317 8.90142 11.5355 9.30387 11.419 9.67944C11.3024 10.055 11.0716 10.3855 10.76 10.624L9.432 11.568C10.7852 13.9774 12.7386 15.9308 15.148 17.284L16.092 15.956C16.3305 15.6444 16.661 15.4136 17.0366 15.297C17.4121 15.1804 17.8146 15.1842 18.188 15.308C19.1448 15.6277 20.1353 15.8336 21.14 15.92C21.6476 15.966 22.1244 16.1975 22.4701 16.5674C22.8158 16.9373 23.0051 17.4188 23 17.918Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Nickname (Optional)">
            <el-input
              v-model="form.nickname"
              placeholder="Enter your nickname"
              size="large"
              maxlength="20"
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                </svg>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="Enter your password (6-20 characters, letters & numbers)"
              size="large"
              show-password
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                  <path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Confirm Password">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="Confirm your password"
              size="large"
              show-password
              @keyup.enter="handleRegister"
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                  <path d="M7 11V7C7 5.67392 7.52678 4.40215 8.46447 3.46447C9.40215 2.52678 10.6739 2 12 2C13.3261 2 14.5979 2.52678 15.5355 3.46447C16.4732 4.40215 17 5.67392 17 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </template>
            </el-input>
          </el-form-item>

          <div class="form-actions">
            <el-checkbox>I agree to the Terms of Service and Privacy Policy</el-checkbox>
          </div>

          <button class="btn btn-primary" :disabled="loading" @click="handleRegister">
            <span v-if="loading">Creating Account...</span>
            <span v-else>Create Account</span>
          </button>
        </el-form>

        <div class="form-footer">
          <span>Already have an account?</span>
          <button class="link-btn" @click="goToLogin">Sign in</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-view {
  --font-display: 'Oswald', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  display: flex;
  min-height: 100vh;
}

/* Brand Panel */
.register-brand {
  position: relative;
  width: 50%;
  background: #0a0a0a;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.brand-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 50% 100%, rgba(255, 77, 0, 0.2), transparent),
    radial-gradient(ellipse 50% 40% at 100% 50%, rgba(255, 77, 0, 0.1), transparent);
}

.brand-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 40px 40px;
}

.brand-content {
  position: relative;
  z-index: 2;
  padding: 60px;
  max-width: 500px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 48px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff4d00 0%, #e64600 100%);
  color: white;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 8px 100%, 0 calc(100% - 8px));
}

.logo-text {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: white;
  letter-spacing: 2px;
}

.brand-title {
  font-family: var(--font-display);
  font-size: 56px;
  font-weight: 700;
  color: white;
  line-height: 1.1;
  margin-bottom: 16px;
}

.brand-subtitle {
  font-family: var(--font-body);
  font-size: 16px;
  color: #9ca3af;
  line-height: 1.6;
  margin-bottom: 48px;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.brand-feature {
  display: flex;
  align-items: center;
  gap: 16px;
  color: white;
  font-family: var(--font-body);
  font-size: 15px;
}

.feature-icon {
  width: 24px;
  height: 24px;
  color: #ff4d00;
  flex-shrink: 0;
}

.brand-accent {
  position: absolute;
  top: -100px;
  left: -100px;
  width: 300px;
  height: 300px;
  background: radial-gradient(ellipse, rgba(255, 77, 0, 0.15) 0%, transparent 70%);
  filter: blur(60px);
}

/* Form Panel */
.register-form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9fafb;
  padding: 40px;
}

.form-content {
  width: 100%;
  max-width: 420px;
}

.form-header {
  text-align: center;
  margin-bottom: 48px;
}

.form-badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(255, 77, 0, 0.1);
  border: 1px solid rgba(255, 77, 0, 0.2);
  color: #ff4d00;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.form-title {
  font-family: var(--font-display);
  font-size: 42px;
  font-weight: 700;
  text-transform: uppercase;
  color: #0a0a0a;
  margin-bottom: 12px;
}

.form-subtitle {
  font-family: var(--font-body);
  font-size: 14px;
  color: #6b7280;
}

.register-form {
  margin-bottom: 32px;
}

.register-form :deep(.el-form-item__label) {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.register-form :deep(.el-input__wrapper) {
  background: white;
  border: 1px solid #e5e7eb;
  box-shadow: none;
  transition: all 0.3s ease;
}

.register-form :deep(.el-input__wrapper:hover),
.register-form :deep(.el-input__wrapper.is-focus) {
  border-color: #ff4d00;
}

.register-form :deep(.el-input__inner) {
  font-family: var(--font-body);
  color: #0a0a0a;
}

.input-icon {
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.form-actions {
  margin-bottom: 24px;
}

.form-actions :deep(.el-checkbox__label) {
  font-family: var(--font-body);
  font-size: 13px;
  color: #6b7280;
}

.btn {
  width: 100%;
  padding: 16px 32px;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #ff4d00;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #e64600;
  transform: translateY(-2px);
  box-shadow: 0 10px 30px -10px rgba(255, 77, 0, 0.5);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-footer {
  text-align: center;
  font-family: var(--font-body);
  font-size: 14px;
  color: #6b7280;
}

.link-btn {
  background: none;
  border: none;
  color: #ff4d00;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-left: 4px;
}

.link-btn:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .register-brand {
    display: none;
  }

  .form-title {
    font-size: 32px;
  }
}
</style>
