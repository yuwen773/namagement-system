<template>
  <div class="login-container">
    <!-- Animated Background -->
    <div class="bg-layer">
      <div class="mesh-gradient"></div>
      <div class="grain-overlay"></div>
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>

    <!-- Main Card -->
    <div class="login-card">
      <!-- Decorative Sidebar -->
      <div class="card-sidebar">
        <div class="logo-mark">
          <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="18" stroke="currentColor" stroke-width="2"/>
            <path d="M12 20C12 15.5817 15.5817 12 20 12C24.4183 12 28 15.5817 28 20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="20" cy="26" r="3" fill="currentColor"/>
            <path d="M16 14H24M20 10V18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="sidebar-decoration">
          <div class="deco-line"></div>
          <div class="deco-dots">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- Form Section -->
      <div class="card-content">
        <div class="content-header">
          <h1 class="brand-name">问答采集系统</h1>
          <p class="brand-tagline">智能数据采集与管理平台</p>
        </div>

        <form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-group" :class="{ focused: form.username, error: errors.username }">
            <label for="username">用户名</label>
            <div class="input-wrapper">
              <input
                id="username"
                v-model="form.username"
                type="text"
                placeholder="请输入用户名"
                @focus="handleFocus('username')"
                @blur="handleBlur('username')"
              />
              <div class="input-accent"></div>
            </div>
            <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
          </div>

          <div class="form-group" :class="{ focused: form.password, error: errors.password }">
            <label for="password">密码</label>
            <div class="input-wrapper">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码"
                @focus="handleFocus('password')"
                @blur="handleBlur('password')"
              />
              <div class="input-accent"></div>
              <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
            <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
          </div>

          <button type="submit" class="submit-btn" :disabled="isLoading">
            <span class="btn-text">{{ isLoading ? '登录中...' : '登 录' }}</span>
            <span class="btn-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </span>
            <div class="btn-shine"></div>
          </button>
        </form>

        <div class="form-footer">
          <p class="register-link">
            还没有账号？
            <router-link to="/register" class="link">立即注册</router-link>
          </p>
        </div>
      </div>
    </div>

    <!-- Toast Notifications -->
    <Transition name="toast">
      <div v-if="toast.show" :class="['toast', toast.type]">
        {{ toast.message }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const errors = reactive({
  username: '',
  password: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const focusedField = ref('')
const toast = reactive({
  show: false,
  message: '',
  type: 'error'
})

const handleFocus = (field) => {
  focusedField.value = field
}

const handleBlur = (field) => {
  focusedField.value = ''
  validateField(field)
}

const validateField = (field) => {
  if (field === 'username') {
    errors.username = !form.username ? '请输入用户名' : ''
  }
  if (field === 'password') {
    errors.password = !form.password ? '请输入密码' : ''
  }
}

const validateForm = () => {
  let valid = true
  if (!form.username) {
    errors.username = '请输入用户名'
    valid = false
  }
  if (!form.password) {
    errors.password = '请输入密码'
    valid = false
  }
  return valid
}

const showToast = (message, type = 'error') => {
  toast.message = message
  toast.type = type
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  errors.username = ''
  errors.password = ''

  try {
    const result = await authStore.login(form.username, form.password)

    if (result.success) {
      showToast('登录成功，欢迎回来！', 'success')
      await new Promise(r => setTimeout(r, 800))
      const redirect = route.query.redirect
      router.push(redirect && redirect !== '/login' ? redirect : '/dashboard')
    } else {
      showToast(result.message || '用户名或密码错误')
    }
  } catch (error) {
    showToast('网络连接失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}

// Keyboard navigation
onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !isLoading.value) {
      handleSubmit()
    }
  })
})
</script>

<style scoped>
/* Design Tokens */
:root {
  --color-bg: #faf9f7;
  --color-surface: #ffffff;
  --color-primary: #1a365d;
  --color-primary-light: #2c5282;
  --color-accent: #c9a227;
  --color-text: #1a202c;
  --color-text-muted: #718096;
  --color-border: #e2e8f0;
  --color-error: #c53030;
  --color-success: #2f855a;
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-md: 0 8px 32px rgba(0,0,0,0.12);
  --shadow-lg: 0 16px 64px rgba(0,0,0,0.16);
  --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-smooth: 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #faf9f7;
  position: relative;
  overflow: hidden;
}

/* Animated Background */
.bg-layer {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.mesh-gradient {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(26, 54, 93, 0.08) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 80% 20%, rgba(201, 162, 39, 0.06) 0%, transparent 50%),
    radial-gradient(ellipse 70% 60% at 50% 80%, rgba(44, 82, 130, 0.05) 0%, transparent 50%);
}

.grain-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.4;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

.floating-shapes {
  position: absolute;
  inset: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.3;
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(26, 54, 93, 0.1) 0%, transparent 70%);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(201, 162, 39, 0.08) 0%, transparent 70%);
  bottom: -50px;
  left: -50px;
  animation-delay: -7s;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(26, 54, 93, 0.06) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -20px) scale(1.05); }
  50% { transform: translate(-10px, 10px) scale(0.95); }
  75% { transform: translate(15px, 15px) scale(1.02); }
}

/* Main Card */
.login-card {
  display: flex;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  width: 100%;
  max-width: 900px;
  position: relative;
  z-index: 10;
}

/* Sidebar */
.card-sidebar {
  width: 200px;
  background: linear-gradient(160deg, #1a365d 0%, #2c5282 100%);
  padding: 3rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.card-sidebar::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 60%);
}

.logo-mark {
  width: 56px;
  height: 56px;
  color: #ffffff;
  margin-bottom: auto;
  position: relative;
  z-index: 1;
}

.logo-mark svg {
  width: 100%;
  height: 100%;
}

.sidebar-decoration {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.deco-line {
  width: 40px;
  height: 2px;
  background: rgba(255,255,255,0.2);
  border-radius: 1px;
}

.deco-dots {
  display: flex;
  gap: 8px;
}

.deco-dots span {
  width: 6px;
  height: 6px;
  background: rgba(255,255,255,0.3);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.deco-dots span:nth-child(2) { animation-delay: 0.3s; }
.deco-dots span:nth-child(3) { animation-delay: 0.6s; }

@keyframes pulse {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

/* Content */
.card-content {
  flex: 1;
  padding: 3.5rem 3rem;
  display: flex;
  flex-direction: column;
}

.content-header {
  margin-bottom: 2.5rem;
}

.brand-name {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2rem;
  font-weight: 600;
  color: #1a202c;
  letter-spacing: -0.02em;
  margin-bottom: 0.25rem;
}

.brand-tagline {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  color: #718096;
  letter-spacing: 0.15em;
  text-transform: uppercase;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  color: #4a5568;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  padding: 1rem 1.25rem;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.95rem;
  color: #1a202c;
  background: #f7fafc;
  border: 2px solid transparent;
  border-radius: 12px;
  outline: none;
  transition: all var(--transition-fast);
}

.input-wrapper input::placeholder {
  color: #a0aec0;
}

.input-wrapper input:focus {
  background: #ffffff;
  border-color: #e2e8f0;
}

.form-group.focused label {
  color: #1a365d;
}

.form-group.focused .input-accent {
  width: 100%;
  opacity: 1;
}

.form-group.error .input-wrapper input {
  border-color: #fc8181;
}

.input-accent {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #1a365d, #c9a227);
  border-radius: 1px;
  transition: width var(--transition-smooth);
  opacity: 0;
}

.error-message {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.75rem;
  color: #c53030;
  margin-top: 0.25rem;
}

.toggle-password {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  color: #a0aec0;
  transition: color var(--transition-fast);
}

.toggle-password:hover {
  color: #4a5568;
}

.toggle-password svg {
  width: 20px;
  height: 20px;
}

/* Submit Button */
.submit-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  transition: all var(--transition-fast);
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(26, 54, 93, 0.35);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-text {
  position: relative;
  z-index: 1;
}

.btn-icon {
  position: relative;
  z-index: 1;
  display: flex;
  transition: transform var(--transition-fast);
}

.submit-btn:hover:not(:disabled) .btn-icon {
  transform: translateX(4px);
}

.btn-icon svg {
  width: 18px;
  height: 18px;
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255,255,255,0.2),
    transparent
  );
  animation: shine 3s infinite;
}

@keyframes shine {
  0% { left: -100%; }
  20% { left: 100%; }
  100% { left: 100%; }
}

/* Footer */
.form-footer {
  margin-top: auto;
  padding-top: 2rem;
}

.demo-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.8rem;
  color: #718096;
}

.register-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.85rem;
  color: #718096;
  margin-bottom: 0.75rem;
}

.register-link .link {
  color: #1a365d;
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transition-fast);
}

.register-link .link:hover {
  color: #c9a227;
}

.hint-icon {
  color: #c9a227;
  font-size: 0.5rem;
}

.demo-hint code {
  padding: 0.2rem 0.5rem;
  background: #edf2f7;
  border-radius: 4px;
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.75rem;
  color: #4a5568;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  padding: 1rem 1.5rem;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.9rem;
  font-weight: 500;
  color: #ffffff;
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  z-index: 1000;
}

.toast.error {
  background: #c53030;
}

.toast.success {
  background: #2f855a;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
}

/* Responsive */
@media (max-width: 768px) {
  .login-card {
    flex-direction: column;
    max-width: 420px;
  }

  .card-sidebar {
    width: 100%;
    padding: 2rem;
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
  }

  .logo-mark {
    margin-bottom: 0;
  }

  .sidebar-decoration {
    margin-top: 0;
    margin-left: auto;
    flex-direction: row;
  }

  .deco-line {
    width: 2px;
    height: 24px;
  }

  .deco-dots {
    flex-direction: column;
  }

  .card-content {
    padding: 2rem;
  }

  .floating-shapes {
    display: none;
  }
}
</style>
