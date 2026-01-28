<template>
  <div class="register-container">
    <!-- 左侧品牌区域 -->
    <div class="brand-section">
      <div class="brand-content">
        <!-- Logo 和标题 -->
        <div class="logo-container">
          <div class="logo-icon">?</div>
          <h1 class="brand-title">食堂管理系统</h1>
          <p class="brand-subtitle">智慧食堂 · 高效管理</p>
        </div>

        <!-- 注册优势 -->
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">??</div>
            <div class="feature-text">
              <h3>快速入职</h3>
              <p>一键注册，即刻使用</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">?️</div>
            <div class="feature-text">
              <h3>安全可靠</h3>
              <p>数据加密，隐私保护</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">?</div>
            <div class="feature-text">
              <h3>移动办公</h3>
              <p>随时查看，便捷管理</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">?⃣</div>
            <div class="feature-text">
              <h3>智能提醒</h3>
              <p>排班考勤，及时通知</p>
            </div>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="stats-footer">
          <div class="stat-item">
            <span class="stat-number">500+</span>
            <span class="stat-label">企业用户</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">99.9%</span>
            <span class="stat-label">系统稳定性</span>
          </div>
        </div>

        <!-- 装饰元素 -->
        <div class="floating-icon icon-1">?</div>
        <div class="floating-icon icon-2">?</div>
        <div class="floating-icon icon-3">?</div>
      </div>

      <!-- 背景图案 -->
      <div class="pattern-overlay"></div>
      <div class="gradient-overlay"></div>
    </div>

    <!-- 右侧注册表单 -->
    <div class="form-section">
      <div class="form-container">
        <div class="form-header">
          <h2>创建账号</h2>
          <p>加入食堂管理系统，开启智能办公体验</p>
        </div>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="formRules"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <!-- 用户名 -->
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
              clearable
              :prefix-icon="User"
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <!-- 密码 -->
          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码（至少4位）"
              size="large"
              clearable
              show-password
              :prefix-icon="Lock"
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <!-- 确认密码 -->
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              size="large"
              clearable
              show-password
              :prefix-icon="Lock"
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <!-- 手机号 -->
          <el-form-item prop="phone">
            <el-input
              v-model="registerForm.phone"
              placeholder="请输入手机号"
              size="large"
              clearable
              :prefix-icon="Phone"
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <!-- 邮箱 -->
          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱（选填）"
              size="large"
              clearable
              :prefix-icon="Message"
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <!-- 注册按钮 -->
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="register-button"
              @click="handleRegister"
            >
              <span v-if="!loading">立即注册</span>
              <span v-else>注册中...</span>
            </el-button>
          </el-form-item>

          <!-- 已有账号提示 -->
          <div class="login-tip">
            已有账号？
            <router-link to="/login" class="login-link">立即登录</router-link>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Phone, Message } from '@element-plus/icons-vue'
import { register } from '@/api/auth'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)

// 表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  phone: '',
  email: ''
})

// 密码验证
const validatePassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入密码'))
  } else if (value.length < 4) {
    callback(new Error('密码至少需要4位'))
  } else {
    // 如果确认密码已填写，重新验证确认密码
    if (registerForm.confirmPassword) {
      registerFormRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

// 确认密码验证
const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
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

// 表单验证规则
const formRules = {
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

// 处理注册
const handleRegister = async () => {
  try {
    // 验证表单
    const valid = await registerFormRef.value.validate()
    if (!valid) return

    loading.value = true

    // 调用注册接口
    const { confirmPassword, ...registerData } = registerForm
    const response = await register(registerData)

    if (response.code === 201) {
      ElMessage.success('注册成功！即将跳转到登录页...')

      // 延迟跳转到登录页
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
/* CSS 变量定义 */
:root {
  --primary-color: #FF6B35;
  --secondary-yellow: #F7C52D;
  --secondary-green: #4CAF50;
  --bg-color: #FFF8F0;
  --text-color: #333333;
  --border-radius: 24px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.register-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* 左侧品牌区域 */
.brand-section {
  position: relative;
  width: 52%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary-color) 0%, #FF8C42 50%, var(--secondary-yellow) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.brand-content {
  position: relative;
  z-index: 2;
  padding: clamp(20px, 5vw, 60px);
  max-width: 600px;
  color: white;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Logo 容器 */
.logo-container {
  text-align: center;
  margin-bottom: clamp(30px, 6vw, 60px);
}

.logo-icon {
  font-size: clamp(60px, 10vw, 100px);
  margin-bottom: 20px;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-15px);
  }
}

.brand-title {
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 700;
  margin: 0 0 12px 0;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  letter-spacing: 2px;
}

.brand-subtitle {
  font-size: clamp(14px, 2vw, 18px);
  opacity: 0.95;
  margin: 0;
  font-weight: 300;
  letter-spacing: 4px;
}

/* 功能网格 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: clamp(15px, 3vw, 30px);
  margin-bottom: clamp(30px, 5vw, 60px);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: clamp(12px, 2vw, 20px);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: var(--transition);
}

.feature-item:hover {
  transform: translateX(10px);
  background: rgba(255, 255, 255, 0.2);
}

.feature-icon {
  font-size: clamp(24px, 3vw, 36px);
  flex-shrink: 0;
}

.feature-text h3 {
  font-size: clamp(12px, 1.8vw, 16px);
  font-weight: 600;
  margin: 0 0 4px 0;
}

.feature-text p {
  font-size: clamp(10px, 1.4vw, 13px);
  margin: 0;
  opacity: 0.9;
}

/* 统计信息 */
.stats-footer {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: clamp(20px, 3vw, 28px);
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: clamp(10px, 1.4vw, 13px);
  opacity: 0.9;
}

/* 浮动装饰图标 */
.floating-icon {
  position: absolute;
  font-size: clamp(30px, 5vw, 50px);
  opacity: 0.3;
  animation: floatIcon 6s ease-in-out infinite;
}

.icon-1 {
  top: 15%;
  left: 10%;
  animation-delay: 0s;
}

.icon-2 {
  top: 60%;
  right: 15%;
  animation-delay: 2s;
}

.icon-3 {
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes floatIcon {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(10deg);
  }
}

/* 背景图案 */
.pattern-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    repeating-linear-gradient(
      45deg,
      transparent,
      transparent 35px,
      rgba(255, 255, 255, 0.03) 35px,
      rgba(255, 255, 255, 0.03) 70px
    );
  pointer-events: none;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 40%, rgba(255, 255, 255, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 70% 60%, rgba(247, 197, 45, 0.2) 0%, transparent 50%);
  pointer-events: none;
}

/* 右侧表单区域 */
.form-section {
  width: 48%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-color);
  padding: 40px;
}

.form-container {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: white;
  border-radius: var(--border-radius);
  box-shadow: 0 20px 60px rgba(255, 107, 53, 0.15);
  animation: fadeInRight 0.6s ease-out;
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 表单头部 */
.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-color);
  margin: 0 0 8px 0;
}

.form-header p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* 表单样式 */
.register-form {
  margin-top: 24px;
}

.register-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.register-form :deep(.el-input__wrapper) {
  padding: 8px 15px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: var(--transition);
}

.register-form :deep(.el-input__wrapper:hover),
.register-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.15);
  border-color: var(--primary-color);
}

.register-form :deep(.el-input__inner) {
  font-size: 15px;
  color: var(--text-color);
}

.register-form :deep(.el-input__prefix-inner) {
  color: #999;
}

/* 注册按钮 */
.register-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color) 0%, #FF8C42 100%);
  border: none;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
  transition: var(--transition);
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
}

.register-button:active {
  transform: translateY(0);
}

/* 登录提示 */
.login-tip {
  text-align: center;
  font-size: 14px;
  color: #666;
  margin-top: 16px;
}

.login-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  transition: var(--transition);
}

.login-link:hover {
  color: #FF8C42;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .register-container {
    flex-direction: column;
  }

  .brand-section {
    width: 100%;
    height: 40%;
    min-height: 250px;
  }

  .form-section {
    width: 100%;
    height: 60%;
    padding: 20px;
  }

  .form-container {
    padding: 24px;
  }

  .brand-content {
    padding: 20px;
  }

  .features-grid {
    gap: 10px;
  }

  .feature-item {
    padding: 10px 15px;
  }

  .stats-footer {
    display: none;
  }

  .floating-icon {
    display: none;
  }
}

@media (max-width: 480px) {
  .form-header h2 {
    font-size: 24px;
  }

  .form-container {
    padding: 20px;
  }

  .register-form :deep(.el-input__inner) {
    font-size: 14px;
  }
}
</style>
