<template>
  <div class="register-container">
    <!-- 左侧装饰区 -->
    <div class="register-decorative">
      <div class="decorative-content">
        <div class="decorative-icon">
          <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 15 L55 35 L75 35 L60 48 L68 68 L50 55 L32 68 L40 48 L25 35 L45 35 Z" stroke="currentColor" stroke-width="2" fill="none"/>
            <circle cx="50" cy="50" r="42" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.4"/>
            <path d="M20 80 Q50 90, 80 80" stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.3"/>
            <circle cx="30" cy="25" r="4" fill="currentColor" opacity="0.5"/>
            <circle cx="70" cy="20" r="3" fill="currentColor" opacity="0.4"/>
          </svg>
        </div>
        <h1 class="decorative-title">开启<br/>美食之旅</h1>
        <p class="decorative-subtitle">加入我们的美食社区，探索 20,000+ 精选菜谱</p>
        <div class="decorative-features">
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L15 9L22 9L17 14L19 21L12 17L5 21L7 14L2 9L9 9L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="feature-text">
              <span class="feature-title">收藏管理</span>
              <span class="feature-desc">保存喜爱的菜谱</span>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 3V21H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M18 9L13 14L10 11L7 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="feature-text">
              <span class="feature-title">数据分析</span>
              <span class="feature-desc">洞察饮食偏好</span>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="feature-text">
              <span class="feature-title">智能搜索</span>
              <span class="feature-desc">快速找到菜谱</span>
            </div>
          </div>
        </div>
      </div>
      <!-- 装饰性圆圈 -->
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <!-- 右侧注册表单 -->
    <div class="register-form-section">
      <div class="register-form-wrapper">
        <!-- Logo -->
        <div class="register-logo">
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
          <h2 class="form-title">创建账户</h2>
          <p class="form-subtitle">填写以下信息，开始您的美食探索</p>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            class="register-form"
            @submit.prevent="handleRegister"
          >
            <!-- 用户名 -->
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                size="large"
                :prefix-icon="User"
                clearable
              />
            </el-form-item>

            <!-- 邮箱（可选） -->
            <el-form-item prop="email">
              <el-input
                v-model="form.email"
                placeholder="邮箱地址（可选）"
                size="large"
                :prefix-icon="Message"
                clearable
              />
            </el-form-item>

            <!-- 密码 -->
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码（至少8位）"
                size="large"
                :prefix-icon="Lock"
                show-password
                clearable
              />
              <!-- 密码强度指示器 -->
              <div v-if="form.password" class="password-strength">
                <div class="strength-bar">
                  <div
                    class="strength-fill"
                    :class="`strength-${passwordStrength.level}`"
                    :style="{ width: passwordStrength.percent }"
                  ></div>
                </div>
                <span class="strength-text" :class="`strength-${passwordStrength.level}`">
                  {{ passwordStrength.text }}
                </span>
              </div>
            </el-form-item>

            <!-- 确认密码 -->
            <el-form-item prop="password_confirm">
              <el-input
                v-model="form.password_confirm"
                type="password"
                placeholder="请再次输入密码"
                size="large"
                :prefix-icon="Lock"
                show-password
                clearable
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
                <span v-if="!loading">创建账户</span>
                <span v-else>注册中...</span>
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 登录链接 -->
          <div class="form-footer">
            <span class="footer-text">已有账户？</span>
            <router-link to="/login" class="login-link">
              立即登录
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
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message } from '@element-plus/icons-vue'
import { register } from '@/api/auth'
import { getErrorTip } from '@/utils/errorHandler'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

// 表单数据
const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

// 计算密码强度
const passwordStrength = computed(() => {
  const pwd = form.password
  if (!pwd) {
    return { level: 'weak', percent: '0%', text: '' }
  }

  let score = 0
  if (pwd.length >= 8) score++
  if (pwd.length >= 12) score++
  if (/[a-z]/.test(pwd)) score++
  if (/[A-Z]/.test(pwd)) score++
  if (/[0-9]/.test(pwd)) score++
  if (/[^a-zA-Z0-9]/.test(pwd)) score++

  if (score <= 2) {
    return { level: 'weak', percent: '33%', text: '弱' }
  } else if (score <= 4) {
    return { level: 'medium', percent: '66%', text: '中等' }
  } else {
    return { level: 'strong', percent: '100%', text: '强' }
  }
})

// 自定义验证规则 - 密码匹配
const validatePasswordConfirm = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 自定义验证规则 - 邮箱格式
const validateEmail = (rule, value, callback) => {
  if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    callback(new Error('请输入正确的邮箱格式'))
  } else {
    callback()
  }
}

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为 3-20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { validator: validateEmail, trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码至少 8 位字符', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePasswordConfirm, trigger: 'blur' }
  ]
}

// 处理注册
const handleRegister = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    const response = await register({
      username: form.username,
      email: form.email || undefined,
      password: form.password,
      password_confirm: form.password_confirm
    })

    if (response.code === 201) {
      ElMessage.success('注册成功！即将跳转到登录页...')

      // 延迟跳转到登录页
      setTimeout(() => {
        router.push({
          name: 'login',
          query: { username: form.username }
        })
      }, 1500)
    } else {
      ElMessage.error(response.message || '注册失败')
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

.register-container {
  min-height: 100vh;
  display: flex;
  font-family: 'DM Sans', sans-serif;
  background: #faf8f5;
}

/* ========== 左侧装饰区 ========== */
.register-decorative {
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

.decorative-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(5px);
}

.feature-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.feature-icon svg {
  width: 20px;
  height: 20px;
}

.feature-text {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.feature-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.feature-desc {
  font-size: 0.8rem;
  opacity: 0.8;
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
.register-form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
}

.register-form-wrapper {
  width: 100%;
  max-width: 440px;
}

/* Logo */
.register-logo {
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

.register-form {
  margin-top: 1.5rem;
}

/* 覆盖 Element Plus 样式 */
.register-form :deep(.el-form-item) {
  margin-bottom: 1.25rem;
}

.register-form :deep(.el-input) {
  --el-input-border-radius: 12px;
  --el-input-border-color: #e5ddd3;
  --el-input-focus-border-color: #c2622e;
  --el-input-hover-border-color: #d4773a;
}

.register-form :deep(.el-input__wrapper) {
  padding: 0.75rem 1rem;
  box-shadow: none;
  border: 1.5px solid var(--el-input-border-color);
  transition: all 0.2s ease;
}

.register-form :deep(.el-input__wrapper:hover) {
  border-color: var(--el-input-hover-border-color);
}

.register-form :deep(.el-input__wrapper.is-focus) {
  border-color: var(--el-input-focus-border-color);
  box-shadow: 0 0 0 3px rgba(194, 98, 46, 0.1);
}

.register-form :deep(.el-input__inner) {
  font-size: 0.95rem;
  color: #3d2914;
}

.register-form :deep(.el-input__inner::placeholder) {
  color: #b8a99a;
}

.register-form :deep(.el-input__prefix-inner > .el-icon) {
  color: #a89078;
}

/* 密码强度指示器 */
.password-strength {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #e5ddd3;
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.strength-fill.strength-weak {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.strength-fill.strength-medium {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.strength-fill.strength-strong {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 600;
  min-width: 30px;
}

.strength-text.strength-weak {
  color: #ef4444;
}

.strength-text.strength-medium {
  color: #f59e0b;
}

.strength-text.strength-strong {
  color: #10b981;
}

.register-button {
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

.register-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(194, 98, 46, 0.35);
}

.register-button:active {
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

.login-link {
  color: #c2622e;
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.25rem;
  transition: color 0.2s ease;
}

.login-link:hover {
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
  .register-decorative {
    display: none;
  }

  .register-form-section {
    background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
  }
}

@media (max-width: 480px) {
  .register-form-section {
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

.feature-item {
  animation: fadeInUp 0.5s ease-out both;
}

.feature-item:nth-child(1) {
  animation-delay: 0.2s;
}

.feature-item:nth-child(2) {
  animation-delay: 0.3s;
}

.feature-item:nth-child(3) {
  animation-delay: 0.4s;
}
</style>
