<template>
  <div class="register-page">
    <!-- 左侧品牌展示区 -->
    <div class="brand-side">
      <div class="brand-bg">
        <div class="bg-pattern"></div>
        <div class="bg-gradient"></div>
      </div>

      <div class="brand-content">
        <div class="brand-logo">
          <el-icon class="logo-icon" :size="64"><Coffee /></el-icon>
        </div>
        <h1 class="brand-title">食堂管理系统</h1>
        <p class="brand-subtitle">智慧餐饮 · 高效运营</p>

        <div class="brand-features">
          <div class="feature-badge" v-for="(feature, idx) in features" :key="idx" :style="{ '--delay': idx * 0.1 + 's' }">
            <el-icon class="feature-icon"><component :is="feature.icon" /></el-icon>
            <span>{{ feature.text }}</span>
          </div>
        </div>
      </div>

      <div class="brand-footer">
        <div class="stat">
          <span class="stat-num">500+</span>
          <span class="stat-label">企业用户</span>
        </div>
        <div class="stat">
          <span class="stat-num">99.9%</span>
          <span class="stat-label">系统稳定性</span>
        </div>
      </div>
    </div>

    <!-- 右侧注册表单区 -->
    <div class="form-side">
      <div class="form-wrapper">
        <div class="form-header">
          <h2>创建账号</h2>
          <p>填写信息，开始使用食堂管理系统</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              size="large"
              placeholder="请输入用户名"
              :prefix-icon="User"
              clearable
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              size="large"
              placeholder="请输入密码（至少4位）"
              :prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              size="large"
              placeholder="请再次输入密码"
              :prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item prop="phone">
            <el-input
              v-model="form.phone"
              size="large"
              placeholder="请输入手机号"
              :prefix-icon="Phone"
              clearable
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="form.email"
              size="large"
              placeholder="请输入邮箱（选填）"
              :prefix-icon="Message"
              clearable
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="submit-btn"
              :loading="loading"
              @click="handleRegister"
            >
              立即注册
            </el-button>
          </el-form-item>
        </el-form>

        <div class="form-footer">
          <span>已有账号？</span>
          <router-link to="/login" class="login-link">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Phone, Message, Coffee, UserFilled, Calendar, Clock, Checked } from '@element-plus/icons-vue'
import { register } from '@/api/auth'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  phone: '',
  email: ''
})

const features = [
  { icon: 'UserFilled', text: '快速入职' },
  { icon: 'Calendar', text: '智能排班' },
  { icon: 'Clock', text: '移动办公' },
  { icon: 'Checked', text: '数据安全' }
]

// 密码验证
const validatePassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入密码'))
  } else if (value.length < 4) {
    callback(new Error('密码至少需要4位'))
  } else {
    if (form.confirmPassword) {
      formRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

// 确认密码验证
const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 手机号验证
const validatePhone = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入手机号'))
  } else if (!/^1[3-9]\d{9}$/.test(value)) {
    callback(new Error('请输入正确的手机号'))
  } else {
    callback()
  }
}

// 邮箱验证
const validateEmail = (rule, value, callback) => {
  if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    callback(new Error('请输入正确的邮箱地址'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, message: '用户名至少需要2位', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  phone: [
    { required: true, validator: validatePhone, trigger: 'blur' }
  ],
  email: [
    { validator: validateEmail, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    const { confirmPassword, ...registerData } = form
    const response = await register(registerData)

    if (response.code === 201) {
      ElMessage.success('注册成功！即将跳转到登录页...')
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    } else {
      ElMessage.error(response.message || '注册失败，请重试')
    }
  } catch (error) {
    console.error('注册错误:', error)
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else if (error.response?.data?.username) {
      ElMessage.error(error.response.data.username[0] || '用户名已存在')
    } else {
      ElMessage.error('注册失败，请检查网络连接')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ===== 全局变量 ===== */
:root {
  --primary: #FF6B35;
  --primary-light: #FF8C42;
  --primary-dark: #E55A2B;
  --secondary: #F7C52D;
  --bg-cream: #FFF8F0;
  --text-dark: #2C3E50;
  --text-gray: #7F8C8D;
  --border: #E8EEF2;
  --shadow: 0 10px 40px rgba(255, 107, 53, 0.15);
}

/* ===== 主容器 ===== */
.register-page {
  display: flex;
  min-height: 100vh;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* ===== 左侧品牌区 ===== */
.brand-side {
  position: relative;
  width: 52%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.brand-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, var(--secondary) 100%);
}

.bg-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.1;
  background-image:
    repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(255,255,255,0.1) 20px, rgba(255,255,255,0.1) 40px);
}

.bg-gradient {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to top, rgba(0,0,0,0.15), transparent);
}

.brand-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 60px 40px;
  color: white;
}

.brand-logo {
  margin-bottom: 24px;
}

.logo-icon {
  color: white;
  filter: drop-shadow(0 8px 24px rgba(0,0,0,0.2));
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

.brand-title {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 12px 0;
  letter-spacing: 4px;
  text-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.brand-subtitle {
  font-size: 16px;
  opacity: 0.95;
  margin: 0 0 48px 0;
  font-weight: 300;
  letter-spacing: 6px;
}

.brand-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  max-width: 400px;
  margin: 0 auto;
}

.feature-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 20px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.2);
  font-size: 14px;
  font-weight: 500;
  animation: fadeInUp 0.6s ease-out backwards;
  animation-delay: var(--delay);
}

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

.feature-badge:hover {
  background: rgba(255,255,255,0.25);
  transform: translateX(8px);
}

.feature-icon {
  font-size: 20px;
}

.brand-footer {
  position: relative;
  z-index: 2;
  display: flex;
  gap: 60px;
  margin-top: 60px;
  padding: 0 40px 40px;
}

.stat {
  text-align: center;
}

.stat-num {
  display: block;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
}

/* ===== 右侧表单区 ===== */
.form-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-cream);
  padding: 40px;
}

.form-wrapper {
  width: 100%;
  max-width: 420px;
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-dark);
  margin: 0 0 8px 0;
}

.form-header p {
  font-size: 14px;
  color: var(--text-gray);
  margin: 0;
}

.register-form {
  background: white;
  padding: 32px;
  border-radius: 20px;
  box-shadow: var(--shadow);
}

.register-form :deep(.el-form-item) {
  margin-bottom: 18px;
}

.register-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  padding: 4px 16px;
  box-shadow: none;
  border: 2px solid var(--border);
  transition: all 0.3s;
}

.register-form :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-light);
}

.register-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
}

.register-form :deep(.el-input__inner) {
  font-size: 15px;
  font-weight: 500;
}

.register-form :deep(.el-input__prefix-inner) {
  color: var(--primary);
}

.submit-btn {
  width: 100%;
  height: 50px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.3);
  transition: all 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
}

.form-footer {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--text-gray);
}

.login-link {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: color 0.2s;
}

.login-link:hover {
  color: var(--primary-light);
}

/* ===== 响应式 ===== */
@media (max-width: 960px) {
  .register-page {
    flex-direction: column;
  }

  .brand-side {
    width: 100%;
    min-height: 40vh;
    padding: 30px 20px;
  }

  .brand-content {
    padding: 0;
  }

  .brand-title {
    font-size: 32px;
  }

  .brand-subtitle {
    margin-bottom: 30px;
  }

  .brand-features {
    display: none;
  }

  .brand-footer {
    display: none;
  }

  .form-side {
    padding: 24px 20px;
  }

  .form-header h2 {
    font-size: 28px;
  }

  .register-form {
    padding: 24px 20px;
  }
}

@media (max-width: 480px) {
  .form-header h2 {
    font-size: 24px;
  }

  .brand-title {
    font-size: 28px;
  }

  .register-form :deep(.el-input__inner) {
    font-size: 14px;
  }
}
</style>
