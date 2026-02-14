<template>
  <div class="register-container">
    <!-- Background with animated gradient -->
    <div class="background-gradient">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
      <div class="map-pattern"></div>
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
          <h1 class="brand-title">开启旅程<br>即刻出发</h1>
          <p class="brand-subtitle">加入我们，探索更多精彩景点</p>
          <div class="brand-features">
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 13l4 4L19 7"/>
              </svg>
              <span class="feature-text">个性化推荐</span>
            </div>
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 13l4 4L19 7"/>
              </svg>
              <span class="feature-text">真实用户评价</span>
            </div>
            <div class="feature">
              <svg class="feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 13l4 4L19 7"/>
              </svg>
              <span class="feature-text">收藏分享功能</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right side - Register form -->
      <div class="form-section">
        <div class="form-container">
          <div class="form-header">
            <h2 class="form-title">创建账号</h2>
            <p class="form-subtitle">填写信息开始您的探索之旅</p>
          </div>

          <el-form :model="form" :rules="rules" ref="formRef" class="register-form" @submit.prevent="handleRegister">
            <el-row :gutter="16">
              <el-col :span="12">
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
              </el-col>
              <el-col  :span="12">
            <el-form-item prop="email">
              <div class="input-wrapper">
                <el-input
                  v-model="form.email"
                  placeholder="邮箱"
                  size="large"
                  :prefix-icon="Message"
                  class="custom-input"
                />
              </div>
            </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="16">
              <el-col :xs="24" :sm="12">
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
                    />
                  </div>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item prop="confirmPassword">
                  <div class="input-wrapper">
                    <el-input
                      v-model="form.confirmPassword"
                      type="password"
                      placeholder="确认密码"
                      size="large"
                      :prefix-icon="Lock"
                      show-password
                      class="custom-input"
                    />
                  </div>
                </el-form-item>
              </el-col>
            </el-row>


            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="register-button"
                :loading="loading"
                @click="handleRegister"
              >
                <span v-if="!loading">注册</span>
                <span v-else>注册中...</span>
              </el-button>
            </el-form-item>
          </el-form>

          <div class="form-footer">
            <p class="login-prompt">
              已有账号？
              <router-link to="/login" class="login-link">立即登录</router-link>
            </p>
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
import { User, Lock, Message } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)
const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: ''
})

const validatePassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else if (value.length < 6) {
    callback(new Error('密码长度至少6位'))
  } else {
    if (form.confirmPassword !== '') {
      formRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请确认密码'))
  } else if (value !== form.password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

async function handleRegister() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    await userStore.register(
      form.username,
      form.password,
      form.confirmPassword,
      form.email
    )

    ElMessage.success('注册成功！请登录')

    // Reset form
    Object.keys(form).forEach(key => {
      form[key] = ''
    })

    router.push('/login')
  } catch (error) {
    console.error('Register error:', error)
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
  // Add entrance animation
  document.querySelector('.form-container')?.classList.add('animate-in')
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.custom-input {
  width: 100%;
}

:deep(.custom-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

:deep(.custom-input .el-input__wrapper:hover) {
  border-color: rgba(249, 115, 22, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

:deep(.custom-input .el-input__wrapper.is-focus) {
  border-color: #f97316;
  box-shadow: 0 4px 16px rgba(249, 115, 22, 0.2);
}

:deep(.custom-input .el-input__inner) {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #1f2937;
}

:deep(.register-button) {
  width: 100%;
  height: 52px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(249, 115, 22, 0.3);
  transition: all 0.3s ease;
}

:deep(.register-button:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.4);
}

:deep(.register-button:active) {
  transform: translateY(0);
}

.register-container {
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
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 50%, #fecaca 100%);
  z-index: 0;
}

.map-pattern {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 49px, rgba(249, 115, 22, 0.03) 49px, rgba(249, 115, 22, 0.03) 50px),
    repeating-linear-gradient(90deg, transparent, transparent 49px, rgba(249, 115, 22, 0.03) 49px, rgba(249, 115, 22, 0.03) 50px);
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
  background: rgba(249, 115, 22, 0.3);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: rgba(234, 179, 8, 0.25);
  bottom: -50px;
  left: -50px;
  animation-delay: -2s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: rgba(251, 146, 60, 0.2);
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
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
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
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.5"/></svg>') repeat;
  background-size: 100px 100px;
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
  stroke-width: 3;
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
  max-width: 480px;
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

.register-form {
  margin-bottom: 32px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-row) {
  margin: 0 -8px;
}

:deep(.el-col) {
  padding: 0 8px;
}

.input-wrapper {
  position: relative;
}

.form-footer {
  text-align: center;
}

.login-prompt {
  font-size: 15px;
  color: #6b7280;
}

.login-link {
  color: #f97316;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #ea580c;
  text-decoration: underline;
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

  :deep(.el-col) {
    padding: 0 4px;
  }
}
</style>
