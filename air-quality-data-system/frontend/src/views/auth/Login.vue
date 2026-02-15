<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Left Side - Brand -->
      <div class="brand-section">
        <div class="brand-logo">
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="24" cy="24" r="16" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M24 12V36M16 24H32" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="24" cy="24" r="4" fill="currentColor"/>
          </svg>
        </div>
        <h1 class="brand-title">空气质量监测平台</h1>
        <p class="brand-subtitle">全国空气质量数据监测与居民防护指南</p>

        <div class="features">
          <div class="feature-item">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18C14.4183 18 18 14.4183 18 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M10 6V10L13 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>实时数据更新</span>
          </div>
          <div class="feature-item">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="3" width="14" height="14" rx="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M7 10H13M10 7V13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <span>全国城市覆盖</span>
          </div>
          <div class="feature-item">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 3V17H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 11L11 7L15 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>专业数据分析</span>
          </div>
        </div>
      </div>

      <!-- Right Side - Login Form -->
      <div class="form-section">
        <div class="form-header">
          <h2 class="form-title">登录账号</h2>
          <p class="form-subtitle">欢迎回来，请输入您的账号信息</p>
        </div>

        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" class="login-form" @submit.prevent="handleLogin">
          <el-form-item prop="username">
            <label class="input-label">用户名</label>
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-form-item prop="password">
            <label class="input-label">密码</label>
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>

          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form>

        <div class="form-footer">
          <span>还没有账号？</span>
          <router-link to="/register" class="register-link">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为 6-20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    loading.value = true

    const res = await login(loginForm.value.username, loginForm.value.password)
    userStore.setUser(res.data.user, res.data.token)
    ElMessage.success('登录成功')

    if (res.data.user.role === 'ADMIN') {
      router.push('/admin')
    } else {
      router.push('/')
    }
  } catch (error) {
    // Error is handled by request interceptor
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-main);
  padding: var(--spacing-xl);
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
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

.login-form {
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

.login-btn {
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

.register-link {
  color: var(--primary);
  font-weight: 500;
  text-decoration: none;
}

.register-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .login-container {
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
