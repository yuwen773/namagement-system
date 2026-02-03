<template>
  <div class="login-container">
    <!-- 左侧装饰区 -->
    <div class="login-decorative">
      <div class="decorative-content">
        <div class="decorative-icon">
          <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="45" stroke="currentColor" stroke-width="2" stroke-dasharray="4 4" opacity="0.3"/>
            <path d="M30 40 C30 35, 35 30, 50 30 C65 30, 70 35, 70 40 L70 65 C70 72, 65 75, 50 75 C35 75, 30 72, 30 65 Z" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M35 50 Q50 55, 65 50" stroke="currentColor" stroke-width="1.5" fill="none"/>
            <circle cx="42" cy="45" r="3" fill="currentColor"/>
            <circle cx="58" cy="45" r="3" fill="currentColor"/>
            <path d="M48 52 L52 52 L50 56 Z" fill="currentColor"/>
          </svg>
        </div>
        <h1 class="decorative-title">探索<br/>万千风味</h1>
        <p class="decorative-subtitle">20,000+ 精选菜谱 · 数据驱动的美食发现之旅</p>
        <div class="decorative-stats">
          <div class="stat-item">
            <span class="stat-value">20K+</span>
            <span class="stat-label">菜谱</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">8</span>
            <span class="stat-label">菜系</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">500+</span>
            <span class="stat-label">食材</span>
          </div>
        </div>
      </div>
      <!-- 装饰性圆圈 -->
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <!-- 右侧登录表单 -->
    <div class="login-form-section">
      <div class="login-form-wrapper">
        <!-- Logo -->
        <div class="login-logo">
          <div class="logo-icon">
            <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="4" y="8" width="32" height="26" rx="3" stroke="currentColor" stroke-width="2"/>
              <path d="M4 14 L36 14" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="11" r="1.5" fill="currentColor"/>
              <circle cx="17" cy="11" r="1.5" fill="currentColor"/>
            </svg>
          </div>
          <span class="logo-text">Recipe Analysis</span>
        </div>

        <!-- 表单卡片 -->
        <div class="form-card">
          <h2 class="form-title">欢迎回来</h2>
          <p class="form-subtitle">登录您的账户，继续美食探索</p>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            class="login-form"
            @submit.prevent="handleLogin"
          >
            <!-- 用户名 -->
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                size="large"
                :prefix-icon="User"
                clearable
                @keyup.enter="handleLogin"
              />
            </el-form-item>

            <!-- 密码 -->
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                size="large"
                :prefix-icon="Lock"
                show-password
                clearable
                @keyup.enter="handleLogin"
              />
            </el-form-item>

            <!-- 记住我 -->
            <div class="form-options">
              <el-checkbox v-model="form.remember">记住我</el-checkbox>
            </div>

            <!-- 登录按钮 -->
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                class="login-button"
                @click="handleLogin"
              >
                <span v-if="!loading">登录</span>
                <span v-else>登录中...</span>
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 注册链接 -->
          <div class="form-footer">
            <span class="footer-text">还没有账户？</span>
            <router-link to="/register" class="register-link">
              立即注册
            </router-link>
          </div>
        </div>

        <!-- 底部版权 -->
        <p class="copyright">© 2026 Recipe Analysis. All rights reserved.</p>
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
import { login } from '@/api/auth'
import { getErrorTip, getFieldError } from '@/utils/errorHandler'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)

// 表单数据
const form = reactive({
  username: '',
  password: '',
  remember: false
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    const response = await login(form.username, form.password)

    if (response.code === 200) {
      const { token, refresh_token, user } = response.data

      // 存储到 Pinia store
      userStore.setToken(token)
      userStore.setUserInfo(user)

      // 如果没勾选记住我，可以选择不存储 refresh_token

      ElMessage.success('登录成功，欢迎回来！')

      // 管理员跳转到管理后台，普通用户跳转到首页
      setTimeout(() => {
        if (user.role === 'admin') {
          router.push('/admin/dashboard')
        } else {
          router.push('/')
        }
      }, 500)
    } else {
      // 业务错误（code !== 200）
      ElMessage.error(response.message || '登录失败')
    }
  } catch (error) {
    const { message } = getErrorTip(error)
    ElMessage.error(message)

    // 字段错误显示在表单下
    const errorData = error.data || error.response?.data
    if (errorData?.errors) {
      formRef.value?.clearValidate()
      for (const [field, errors] of Object.entries(errorData.errors)) {
        if (errors?.[0]) {
          formRef.value?.setFieldError(field, errors[0])
        }
      }
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Google Fonts - 食谱主题字体组合 */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.login-container {
  min-height: 100vh;
  display: flex;
  font-family: 'DM Sans', sans-serif;
  background: #faf8f5;
}

/* ========== 左侧装饰区 ========== */
.login-decorative {
  position: relative;
  width: 55%;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 50%, #a35220 100%);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.decorative-content {
  position: relative;
  z-index: 2;
  color: white;
  text-align: center;
  padding: 3rem;
  max-width: 500px;
}

.decorative-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 2rem;
  opacity: 0.9;
}

.decorative-icon svg {
  width: 100%;
  height: 100%;
}

.decorative-title {
  font-family: 'Playfair Display', serif;
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.decorative-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 3rem;
  font-weight: 400;
}

.decorative-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
}

.stat-label {
  font-size: 0.85rem;
  opacity: 0.8;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.3);
}

/* 装饰圆圈 */
.circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  left: -100px;
}

.circle-2 {
  width: 300px;
  height: 300px;
  bottom: -80px;
  right: 20%;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 30%;
  right: 10%;
  opacity: 0.5;
}

/* ========== 右侧表单区 ========== */
.login-form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
}

.login-form-wrapper {
  width: 100%;
  max-width: 420px;
}

/* Logo */
.login-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2.5rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  color: #c2622e;
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

.logo-text {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #3d2914;
  letter-spacing: -0.02em;
}

/* 表单卡片 */
.form-card {
  background: white;
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08), 0 0 1px rgba(61, 41, 20, 0.1);
}

.form-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #3d2914;
  margin-bottom: 0.5rem;
  font-family: 'Playfair Display', serif;
}

.form-subtitle {
  color: #8b7355;
  font-size: 0.95rem;
  margin-bottom: 2rem;
}

.login-form {
  margin-top: 1.5rem;
}

/* 覆盖 Element Plus 样式 */
.login-form :deep(.el-form-item) {
  margin-bottom: 1.25rem;
}

.login-form :deep(.el-input) {
  --el-input-border-radius: 12px;
  --el-input-border-color: #e5ddd3;
  --el-input-focus-border-color: #c2622e;
  --el-input-hover-border-color: #d4773a;
}

.login-form :deep(.el-input__wrapper) {
  padding: 0.75rem 1rem;
  box-shadow: none;
  border: 1.5px solid var(--el-input-border-color);
  transition: all 0.2s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  border-color: var(--el-input-hover-border-color);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--el-input-focus-border-color);
  box-shadow: 0 0 0 3px rgba(194, 98, 46, 0.1);
}

.login-form :deep(.el-input__inner) {
  font-size: 0.95rem;
  color: #3d2914;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: #b8a99a;
}

.login-form :deep(.el-input__prefix-inner > .el-icon) {
  color: #a89078;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.form-options :deep(.el-checkbox) {
  font-size: 0.9rem;
}

.form-options :deep(.el-checkbox__label) {
  color: #6b5c4d;
}

.form-options :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #c2622e;
  border-color: #c2622e;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border: none;
  margin-top: 0.5rem;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.35);
}

.login-button:active {
  transform: translateY(0);
}

/* 表单底部 */
.form-footer {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0ebe3;
}

.footer-text {
  color: #8b7355;
  font-size: 0.9rem;
}

.register-link {
  color: #c2622e;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.25rem;
  transition: color 0.2s ease;
}

.register-link:hover {
  color: #a35220;
}

/* 版权信息 */
.copyright {
  text-align: center;
  color: #b8a99a;
  font-size: 0.85rem;
  margin-top: 2rem;
}

/* ========== 响应式设计 ========== */
@media (max-width: 1024px) {
  .login-decorative {
    display: none;
  }

  .login-form-section {
    background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
  }
}

@media (max-width: 480px) {
  .login-form-section {
    padding: 1rem;
  }

  .form-card {
    padding: 1.75rem;
    border-radius: 20px;
  }

  .form-title {
    font-size: 1.5rem;
  }
}

/* ========== 动画 ========== */
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

.form-card {
  animation: fadeInUp 0.5s ease-out;
}

.decorative-content {
  animation: fadeInUp 0.6s ease-out 0.1s both;
}
</style>
