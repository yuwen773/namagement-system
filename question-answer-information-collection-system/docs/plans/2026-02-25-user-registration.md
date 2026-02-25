# User Registration Feature Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a user registration page that allows new users to sign up for the Q&A collection system with form validation and seamless navigation to/from login.

**Architecture:** The backend registration endpoint (`POST /api/auth/register/`) already exists in `apps/accounts/views.py`. The frontend needs a new `Register.vue` component that calls the existing `createUser()` API function from `api/users.js`. The registration flow follows the existing login pattern with toast notifications and validation.

**Tech Stack:** Vue 3 (Composition API), Pinia store, Element Plus (form validation), existing API layer

---

## Task 1: Add Register Route to Router

**Files:**
- Modify: `frontend/src/router/index.js:9-16`

**Step 1: Add Register route and import**

Edit `frontend/src/router/index.js` to add the Register component import and route.

```javascript
// After line 8, add:
import Register from '@/views/Register.vue'

// In the routes array, after the Login route (around line 17), add:
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
```

**Step 2: Update Login route guard to allow navigation to Register**

Edit the router guard (around line 96) to allow navigation to Register page when logged in:
```javascript
// Change line 96 from:
if (to.name === 'Login' && isLoggedIn) {
// To:
if ((to.name === 'Login' || to.name === 'Register') && isLoggedIn) {
```

**Step 3: Commit**

```bash
cd frontend
git add src/router/index.js
git commit -m "feat: add register route to router configuration"
```

---

## Task 2: Create Register.vue Component (Frontend Design Skill Required)

**Files:**
- Create: `frontend/src/views/Register.vue`
- Reference: `frontend/src/views/Login.vue` (use similar design patterns)

**Step 1: Create Register.vue with form validation**

Create `frontend/src/views/Register.vue` with the following complete implementation. Note: This should use @frontend-design skill for production-quality UI.

```vue
<template>
  <div class="register-container">
    <!-- Animated Background (reuse from Login.vue) -->
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
    <div class="register-card">
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
          <h1 class="brand-name">创建账号</h1>
          <p class="brand-tagline">加入问答采集系统</p>
        </div>

        <form @submit.prevent="handleSubmit" class="register-form">
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

          <div class="form-group" :class="{ focused: form.email, error: errors.email }">
            <label for="email">邮箱 (可选)</label>
            <div class="input-wrapper">
              <input
                id="email"
                v-model="form.email"
                type="email"
                placeholder="请输入邮箱地址"
                @focus="handleFocus('email')"
                @blur="handleBlur('email')"
              />
              <div class="input-accent"></div>
            </div>
            <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
          </div>

          <div class="form-group" :class="{ focused: form.password, error: errors.password }">
            <label for="password">密码</label>
            <div class="input-wrapper">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码 (至少6位)"
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
            <!-- Password strength indicator -->
            <div v-if="form.password && !errors.password" class="password-strength">
              <div class="strength-bar">
                <div class="strength-fill" :class="passwordStrength.class" :style="{ width: passwordStrength.width }"></div>
              </div>
              <span class="strength-text">{{ passwordStrength.text }}</span>
            </div>
          </div>

          <div class="form-group" :class="{ focused: form.confirmPassword, error: errors.confirmPassword }">
            <label for="confirmPassword">确认密码</label>
            <div class="input-wrapper">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="请再次输入密码"
                @focus="handleFocus('confirmPassword')"
                @blur="handleBlur('confirmPassword')"
              />
              <div class="input-accent"></div>
              <button type="button" class="toggle-password" @click="showConfirmPassword = !showConfirmPassword">
                <svg v-if="!showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
            <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
          </div>

          <button type="submit" class="submit-btn" :disabled="isLoading">
            <span class="btn-text">{{ isLoading ? '注册中...' : '注 册' }}</span>
            <span class="btn-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </span>
            <div class="btn-shine"></div>
          </button>
        </form>

        <div class="form-footer">
          <p class="login-link">
            已有账号？
            <router-link to="/login" class="link">立即登录</router-link>
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
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { createUser } from '@/api/users'

const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const toast = reactive({
  show: false,
  message: '',
  type: 'error'
})

// Password strength calculator
const passwordStrength = computed(() => {
  const pwd = form.password
  if (!pwd) return { width: '0%', text: '', class: '' }

  let score = 0
  if (pwd.length >= 6) score++
  if (pwd.length >= 8) score++
  if (/[A-Z]/.test(pwd)) score++
  if (/[0-9]/.test(pwd)) score++
  if (/[^A-Za-z0-9]/.test(pwd)) score++

  const levels = [
    { width: '20%', text: '弱', class: 'weak' },
    { width: '40%', text: '较弱', class: 'weak' },
    { width: '60%', text: '中等', class: 'medium' },
    { width: '80%', text: '较强', class: 'strong' },
    { width: '100%', text: '强', class: 'strong' }
  ]

  return levels[Math.min(score, 4)]
})

const handleFocus = (field) => {
  // Clear error when user focuses on field
  errors[field] = ''
}

const handleBlur = (field) => {
  validateField(field)
}

const validateField = (field) => {
  if (field === 'username') {
    if (!form.username) {
      errors.username = '请输入用户名'
    } else if (form.username.length < 3) {
      errors.username = '用户名至少3个字符'
    } else if (!/^[a-zA-Z0-9_]+$/.test(form.username)) {
      errors.username = '用户名只能包含字母、数字和下划线'
    } else {
      errors.username = ''
    }
  }

  if (field === 'email') {
    if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      errors.email = '请输入有效的邮箱地址'
    } else {
      errors.email = ''
    }
  }

  if (field === 'password') {
    if (!form.password) {
      errors.password = '请输入密码'
    } else if (form.password.length < 6) {
      errors.password = '密码至少6个字符'
    } else {
      errors.password = ''
    }
    // Also revalidate confirm password if it was already filled
    if (form.confirmPassword) {
      validateField('confirmPassword')
    }
  }

  if (field === 'confirmPassword') {
    if (!form.confirmPassword) {
      errors.confirmPassword = '请确认密码'
    } else if (form.confirmPassword !== form.password) {
      errors.confirmPassword = '两次输入的密码不一致'
    } else {
      errors.confirmPassword = ''
    }
  }
}

const validateForm = () => {
  validateField('username')
  validateField('email')
  validateField('password')
  validateField('confirmPassword')

  return !errors.username && !errors.email && !errors.password && !errors.confirmPassword
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

  try {
    const response = await createUser({
      username: form.username,
      email: form.email || undefined,
      password: form.password
    })

    if (response.code === 0) {
      showToast('注册成功！请登录', 'success')
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      showToast(response.message || '注册失败，请稍后重试')
    }
  } catch (error) {
    console.error('Registration error:', error)
    const message = error.response?.data?.message || error.response?.data?.username?.[0] || '注册失败，请稍后重试'
    showToast(message)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Design Tokens - same as Login.vue */
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

.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #faf9f7;
  position: relative;
  overflow: hidden;
}

/* Animated Background - reuse from Login.vue */
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
.register-card {
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
  margin-bottom: 2rem;
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
.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

/* Password Strength Indicator */
.password-strength {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 2px;
}

.strength-fill.weak {
  background: #fc8181;
}

.strength-fill.medium {
  background: #f6e05e;
}

.strength-fill.strong {
  background: #68d391;
}

.strength-text {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  color: #718096;
  min-width: 2rem;
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
  padding-top: 1.5rem;
}

.login-link {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 0.85rem;
  color: #718096;
  text-align: center;
}

.login-link .link {
  color: #1a365d;
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transition-fast);
}

.login-link .link:hover {
  color: #c9a227;
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
  .register-card {
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
```

**Step 2: Commit**

```bash
cd frontend
git add src/views/Register.vue
git commit -m "feat: add user registration page with form validation"
```

---

## Task 3: Add Register Link to Login Page

**Files:**
- Modify: `frontend/src/views/Login.vue:94-101`

**Step 1: Add register link to login form footer**

Edit `frontend/src/views/Login.vue` to replace the demo-hint section with a register link.

Find the form-footer section (around line 95-101) and replace it with:

```vue
        <div class="form-footer">
          <p class="register-link">
            还没有账号？
            <router-link to="/register" class="link">立即注册</router-link>
          </p>
          <p class="demo-hint">
            <span class="hint-icon">●</span>
            演示账号: <code>admin</code> / <code>admin123</code>
          </p>
        </div>
```

**Step 2: Add CSS for register-link**

Add the following CSS to the style section in `Login.vue` (after the `.demo-hint` rule around line 633):

```css
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
```

**Step 3: Commit**

```bash
cd frontend
git add src/views/Login.vue
git commit -m "feat: add registration link to login page"
```

---

## Task 4: Update Backend Registration View (Optional Enhancement)

**Files:**
- Modify: `backend/apps/accounts/serializers.py:45-62`

**Step 1: Add email validation to UserCreateSerializer**

The existing `UserCreateSerializer` already has email field, but we should add validation for duplicate username.

Edit `backend/apps/accounts/serializers.py`, update the `UserCreateSerializer` class:

```python
class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器（注册用）- 明文密码存储"""

    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        """验证用户名唯一性"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被使用")
        return value

    def create(self, validated_data):
        # 明文存储密码，不使用 create_user() 的哈希处理
        user = User(**validated_data)
        # 直接设置密码，不哈希
        user.password = validated_data['password']
        user.role = validated_data.get('role', 'user')
        user.save()
        return user
```

**Step 2: Update RegisterView for better error handling**

Edit `backend/apps/accounts/views.py` in the `RegisterView.create` method (around line 15-24):

```python
    def create(self, request):
        """POST /api/auth/register/ - 创建新用户"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'code': 0,
            'message': '注册成功',
            'data': UserSerializer(user, context=self.get_serializer_context()).data
        }, status=status.HTTP_201_CREATED)
```

**Step 3: Commit**

```bash
cd backend
git add apps/accounts/serializers.py apps/accounts/views.py
git commit -m "feat: enhance registration with username uniqueness validation"
```

---

## Task 5: Test Registration Flow

**Files:**
- Test: Manual testing in browser

**Step 1: Start backend server**

```bash
cd backend
python manage.py runserver
```
Expected: Server starts on http://127.0.0.1:8000

**Step 2: Start frontend dev server**

```bash
cd frontend
npm run dev
```
Expected: Dev server starts on http://localhost:5173

**Step 3: Test registration flow**

1. Navigate to http://localhost:5173/login
2. Click "立即注册" link
3. Verify Register page loads correctly

Test cases:
- **Empty form submission** - Should show validation errors
- **Short username** (< 3 chars) - Should show "用户名至少3个字符"
- **Invalid email format** - Should show email validation error
- **Short password** (< 6 chars) - Should show "密码至少6个字符"
- **Mismatched passwords** - Should show "两次输入的密码不一致"
- **Valid registration** - Should show success toast and redirect to login

**Step 4: Verify user was created**

```bash
cd backend
python manage.py shell
>>> from apps.accounts.models import User
>>> User.objects.all().values('username', 'email', 'role')
```

**Step 5: Test login with new user**

1. On login page, enter newly registered credentials
2. Verify successful login and redirect to dashboard

**Step 6: Test duplicate username**

1. Try to register with the same username again
2. Should show "该用户名已被使用" error

---

## Summary Checklist

After implementation, verify:

- [ ] `/register` route is accessible
- [ ] Login page has "立即注册" link
- [ ] Register page has "立即登录" link
- [ ] Form validation works for all fields
- [ ] Password strength indicator displays
- [ ] Registration creates user in database
- [ ] Successful registration redirects to login
- [ ] Duplicate username is rejected
- [ ] New user can login with registered credentials
- [ ] Toast notifications display correctly
- [ ] Responsive design works on mobile

---

## Notes for Developers

1. **Password Storage**: As per PRD requirement, passwords are stored in plain text (no hashing). This is intentional for this project.

2. **Default Role**: New users get `role='user'` by default. Only admins can create admin users.

3. **Email Field**: Email is optional in registration form but validated if provided.

4. **API Response Format**: All responses follow `{ code: 0, data: {...}, message: "..." }` format.

5. **Design Consistency**: Register.vue reuses the same design tokens and background effects as Login.vue for visual consistency.
