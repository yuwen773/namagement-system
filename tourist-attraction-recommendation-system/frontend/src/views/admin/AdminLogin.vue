<template>
  <div class="admin-login-container">
    <!-- Background with animated gradient -->
    <div class="background-gradient">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="grid-pattern"></div>
    </div>

    <!-- Decorative elements -->
    <div class="decorative-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <!-- Main content -->
    <div class="content-wrapper">
      <!-- Left side - Brand -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 2C12 2 16 8 16 12C16 15.3137 13.3137 18 10 18C6.68629 18 4 15.3137 4 12C4 8 8 2 8 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M12 22V18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1 class="brand-title">管理后台</h1>
          <p class="brand-subtitle">高效管理 · 数据洞察 · 智能推荐</p>
          <div class="brand-features">
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <path d="M3 9h18"/>
                <path d="M9 21V9"/>
              </svg>
              <span class="feature-text">数据看板</span>
            </div>
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a2 2 0 0 0-2-2-2 2 0 0 0-2 2"/>
                <circle cx="16" cy="7" r="4"/>
              </svg>
              <span class="feature-text">用户管理</span>
            </div>
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 20h9"/>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
              <span class="feature-text">内容审核</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right side - Login form -->
      <div class="form-section">
        <div class="form-container">
          <div class="form-header">
            <div class="admin-badge">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
              </svg>
              <span>管理员</span>
            </div>
            <h2 class="form-title">登录管理后台</h2>
            <p class="form-subtitle">请使用管理员账号登录</p>
          </div>

          <el-form :model="form" :rules="rules" ref="formRef" class="login-form" @submit.prevent="handleLogin">
            <el-form-item prop="username">
              <div class="input-wrapper">
                <el-input
                  v-model="form.username"
                  placeholder="用户名"
                  size="large"
                  :prefix-icon="User"
                  class="custom-input"
                />
              </div>
            </el-form-item>

            <el-form-item prop="password">
              <div class="input-wrapper">
                <el-input
                  v-model="form.password"
                  type="password"
                  placeholder="密码"
                  size="large"
                  :prefix-icon="Lock"
                  show-password
                  class="custom-input"
                  @keyup.enter="handleLogin"
                />
              </div>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="login-button"
                :loading="loading"
                @click="handleLogin"
              >
                <span v-if="!loading">登录</span>
                <span v-else>登录中...</span>
              </el-button>
            </el-form-item>
          </el-form>

          <div class="form-footer">
            <router-link to="/" class="back-link">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
              </svg>
              返回前台首页
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

async function handleLogin() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    await userStore.login(form.username, form.password)

    if (userStore.user?.role === 'ADMIN') {
      ElMessage.success('登录成功！')
      router.push('/admin')
    } else {
      userStore.logout()
      ElMessage.error('非管理员账号，无法访问管理后台')
    }
  } catch (error) {
    console.error('Login error:', error)
    if (error?.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error?.message) {
      ElMessage.error(error.message)
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  document.querySelector('.form-container')?.classList.add('animate-in')
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

:deep(.custom-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

:deep(.custom-input .el-input__wrapper:hover) {
  border-color: rgba(30, 58, 95, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

:deep(.custom-input .el-input__wrapper.is-focus) {
  border-color: #1e3a5f;
  box-shadow: 0 4px 16px rgba(30, 58, 95, 0.2);
}

:deep(.custom-input .el-input__inner) {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #1f2937;
}

:deep(.login-button) {
  width: 100%;
  height: 52px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(30, 58, 95, 0.3);
  transition: all 0.3s ease;
}

:deep(.login-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(30, 58, 95, 0.4);
}

:deep(.login-button:active) {
  transform: translateY(0);
}

.admin-login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  font-family: 'DM Sans', sans-serif;
}

.background-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 50%, #bcccdc 100%);
  z-index: 0;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 49px, rgba(30, 58, 95, 0.03) 49px, rgba(30, 58, 95, 0.03) 50px),
    repeating-linear-gradient(90deg, transparent, transparent 49px, rgba(30, 58, 95, 0.03) 49px, rgba(30, 58, 95, 0.03) 50px);
  opacity: 0.5;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  animation: float 8s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: rgba(30, 58, 95, 0.2);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: rgba(15, 23, 42, 0.15);
  bottom: -50px;
  left: -50px;
  animation-delay: -2s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: rgba(71, 85, 105, 0.15);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -4s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.05);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.95);
  }
}

.decorative-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.shape {
  position: absolute;
  background: rgba(30, 58, 95, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(30, 58, 95, 0.1);
}

.shape-1 {
  width: 120px;
  height: 120px;
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  top: 10%;
  left: 8%;
  animation: morph 15s ease-in-out infinite;
}

.shape-2 {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  bottom: 20%;
  right: 15%;
  animation: morph 12s ease-in-out infinite reverse;
}

.shape-3 {
  width: 60px;
  height: 60px;
  transform: rotate(45deg);
  top: 30%;
  right: 25%;
  animation: morph 10s ease-in-out infinite;
}

@keyframes morph {
  0%, 100% {
    border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
    transform: rotate(0deg);
  }
  25% {
    border-radius: 58% 42% 75% 25% / 76% 46% 54% 24%;
  }
  50% {
    border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%;
    transform: rotate(90deg);
  }
  75% {
    border-radius: 33% 67% 58% 42% / 63% 68% 32% 37%;
  }
}

.content-wrapper {
  display: flex;
  width: 90%;
  max-width: 1200px;
  min-height: 600px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 10;
  position: relative;
}

.brand-section {
  flex: 1;
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  padding: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.brand-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="0" y="0" width="100" height="100" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.5"/></svg>') repeat;
  background-size: 50px 50px;
  opacity: 0.5;
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.brand-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 32px;
  color: #fbbf24;
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
}

.brand-title {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 48px;
  font-weight: 400;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: flex-start;
  max-width: 280px;
  margin: 0 auto;
}

.feature {
  display: flex;
  align-items: center;
  gap: 12px;
}

.feature-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  color: #22c55e;
  stroke-width: 2.5;
}

.feature-text {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
}

.form-section {
  flex: 1;
  padding: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-container {
  width: 100%;
  max-width: 400px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease-out;
}

.form-container.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.admin-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.1) 0%, rgba(15, 23, 42, 0.1) 100%);
  border: 1px solid rgba(30, 58, 95, 0.2);
  border-radius: 20px;
  color: #1e3a5f;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
}

.admin-badge svg {
  width: 16px;
  height: 16px;
}

.form-title {
  font-family: 'Playfair Display', serif;
  font-size: 36px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

.form-subtitle {
  font-size: 16px;
  color: #6b7280;
}

.login-form {
  margin-bottom: 32px;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

.input-wrapper {
  position: relative;
}

.form-footer {
  text-align: center;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #1e3a5f;
  text-decoration: none;
  transition: all 0.3s ease;
}

.back-link:hover {
  gap: 10px;
  color: #0f172a;
}

.back-link svg {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.back-link:hover svg {
  transform: translateX(-4px);
}

/* Responsive */
@media (max-width: 1024px) {
  .content-wrapper {
    flex-direction: column;
    width: 95%;
    min-height: auto;
  }

  .brand-section {
    padding: 40px;
  }

  .brand-title {
    font-size: 36px;
  }

  .brand-subtitle {
    font-size: 16px;
  }

  .form-section {
    padding: 40px;
  }

  .form-container {
    max-width: 100%;
  }
}

@media (max-width: 640px) {
  .brand-section {
    padding: 32px;
  }

  .brand-features {
    gap: 16px;
  }

  .feature-text {
    font-size: 14px;
  }

  .form-section {
    padding: 32px 24px;
  }

  .form-title {
    font-size: 28px;
  }
}
</style>
