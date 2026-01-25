<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Message, Phone } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { register } from '../api/auth'

const router = useRouter()

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  real_name: '',
  email: '',
  phone: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6-20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
  ]
}

const registerFormRef = ref(null)
const loading = ref(false)

async function handleRegister() {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await register({
          username: form.username,
          password: form.password,
          real_name: form.real_name,
          email: form.email,
          phone: form.phone
        })
        ElMessage.success('注册成功，请登录')
        router.push('/login')
      } catch (error) {
        // 错误已在 api 中处理
      } finally {
        loading.value = false
      }
    }
  })
}

function goToLogin() {
  router.push('/login')
}
</script>

<template>
  <div class="register-page">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
      <div class="bg-shape shape-3"></div>
    </div>

    <div class="register-wrapper">
      <div class="register-card">
        <!-- 品牌区域 -->
        <div class="register-brand">
          <div class="brand-icon-wrapper">
            <div class="brand-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="brand-glow"></div>
          </div>
          <h1 class="brand-title">用户注册</h1>
          <p class="brand-subtitle">创建您的企业 HRMS 账号</p>
        </div>

        <!-- 注册表单 -->
        <el-form
          ref="registerFormRef"
          :model="form"
          :rules="rules"
          class="register-form"
          size="large"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item prop="real_name">
            <el-input
              v-model="form.real_name"
              placeholder="请输入真实姓名"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="form.email"
              placeholder="请输入邮箱"
              :prefix-icon="Message"
              clearable
            />
          </el-form-item>

          <el-form-item prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号"
              :prefix-icon="Phone"
              clearable
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请确认密码"
              :prefix-icon="Lock"
              show-password
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item class="form-item">
            <el-button
              type="primary"
              :loading="loading"
              class="submit-btn"
              @click="handleRegister"
            >
              <span class="btn-content">
                <span class="btn-text">{{ loading ? '注册中...' : '注 册' }}</span>
                <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="8.5" cy="7" r="4"/>
                  <line x1="20" y1="8" x2="20" y2="14"/>
                  <line x1="23" y1="11" x2="17" y2="11"/>
                </svg>
              </span>
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-tip">
          <span class="tip-text">已有账号？</span>
          <a href="javascript:;" class="tip-link" @click="goToLogin">立即登录</a>
        </div>
      </div>

      <div class="register-footer">
        <div class="footer-line"></div>
        <span class="footer-text">Enterprise HRMS v1.0</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   Register Page - Modern Corporate Design
   ======================================== */
.register-page {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-primary);
  position: relative;
  overflow: hidden;
}

/* 背景装饰元素 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
}

.bg-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.5;
  filter: blur(80px);
}

.shape-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(99, 102, 241, 0.04) 100%);
  top: -200px;
  right: -100px;
  animation: float 20s ease-in-out infinite;
}

.shape-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.06) 0%, rgba(52, 211, 153, 0.03) 100%);
  bottom: -100px;
  left: -100px;
  animation: float 15s ease-in-out infinite reverse;
}

.shape-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(251, 191, 36, 0.02) 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 8s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -30px); }
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.3; }
}

/* 注册卡片容器 */
.register-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

/* 注册卡片 */
.register-card {
  width: 420px;
  padding: 40px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.register-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light), var(--color-success));
}

.register-card:hover {
  box-shadow: var(--shadow-2xl);
  transform: translateY(-2px);
}

/* 品牌区域 */
.register-brand {
  text-align: center;
  margin-bottom: 28px;
}

.brand-icon-wrapper {
  position: relative;
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
}

.brand-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  z-index: 1;
  box-shadow: var(--shadow-glow-primary);
}

.brand-icon svg {
  width: 32px;
  height: 32px;
}

.brand-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 90px;
  height: 90px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.2) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
}

.brand-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 8px;
  letter-spacing: 0.5px;
  background: linear-gradient(135deg, var(--color-text-primary) 0%, var(--color-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 14px;
  color: var(--color-text-tertiary);
  margin: 0;
  font-weight: 400;
}

/* 表单样式 */
.register-form {
  margin-top: 4px;
}

:deep(.el-form-item) {
  margin-bottom: 16px;
}

:deep(.el-form-item__error) {
  font-size: 12px;
  padding-top: 4px;
}

:deep(.el-input__wrapper) {
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--color-gray-50);
  border: 1.5px solid var(--color-border-light);
  box-shadow: none;
  transition: all 0.2s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: var(--color-primary);
  background: var(--color-bg-secondary);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: var(--color-primary);
  background: var(--color-bg-secondary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

:deep(.el-input__inner) {
  height: 44px;
  font-size: 14px;
  color: var(--color-text-primary);
}

:deep(.el-input__inner::placeholder) {
  color: var(--color-text-tertiary);
}

:deep(.el-input__prefix) {
  color: var(--color-text-tertiary);
  padding-left: 4px;
}

:deep(.el-input__prefix:hover) {
  color: var(--color-primary);
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  height: 44px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 4px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, #818cf8 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.submit-btn:hover::before {
  left: 100%;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
}

.submit-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2);
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.2s ease;
}

.submit-btn:hover .btn-icon {
  transform: translateY(2px);
}

/* 注册提示 */
.register-tip {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border-light);
}

.tip-text {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

.tip-link {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-primary);
  margin-left: 4px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.tip-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

/* 底部 */
.register-footer {
  text-align: center;
  position: relative;
}

.footer-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--color-border-default), transparent);
  margin: 0 auto 16px;
}

.footer-text {
  font-size: 12px;
  color: var(--color-text-tertiary);
  letter-spacing: 0.5px;
}

/* 响应式 */
@media (max-width: 768px) {
  .register-container {
    min-height: 100vh;
    padding: 20px;
  }

  .register-card {
    width: 100%;
    max-width: 440px;
    margin: 0 auto;
    padding: 36px 32px;
    border-radius: var(--radius-xl);
  }

  .brand-icon-wrapper {
    width: 64px;
    height: 64px;
    margin-bottom: 20px;
  }

  .brand-icon {
    width: 64px;
    height: 64px;
  }

  .brand-icon svg {
    width: 32px;
    height: 32px;
  }

  .brand-title {
    font-size: 26px;
    margin-bottom: 8px;
  }

  .brand-subtitle {
    font-size: 14px;
    margin-bottom: 32px;
  }

  .form-item {
    margin-bottom: 20px;
  }

  :deep(.el-input__wrapper) {
    height: 46px;
  }

  :deep(.el-form-item__label) {
    font-size: 14px;
  }

  .submit-btn {
    height: 46px;
    font-size: 15px;
    margin-top: 8px;
  }

  .register-tip {
    margin-top: 20px;
    padding-top: 20px;
  }

  .tip-text,
  .tip-link {
    font-size: 14px;
  }

  .register-footer {
    margin-top: 24px;
  }
}

@media (max-width: 480px) {
  .register-container {
    padding: 16px;
    align-items: flex-start;
    padding-top: 30px;
  }

  .register-card {
    padding: 24px 20px;
    border-radius: var(--radius-lg);
  }

  .brand-icon-wrapper {
    width: 52px;
    height: 52px;
    margin-bottom: 16px;
  }

  .brand-icon {
    width: 52px;
    height: 52px;
  }

  .brand-icon svg {
    width: 26px;
    height: 26px;
  }

  .brand-title {
    font-size: 22px;
  }

  .brand-subtitle {
    font-size: 13px;
    margin-bottom: 24px;
  }

  .form-item {
    margin-bottom: 16px;
  }

  :deep(.el-input__wrapper) {
    height: 42px;
  }

  :deep(.el-form-item__label) {
    font-size: 13px;
    padding-bottom: 6px;
  }

  .submit-btn {
    height: 42px;
    font-size: 14px;
  }

  .submit-btn .btn-icon {
    width: 16px;
    height: 16px;
  }

  .register-tip {
    margin-top: 16px;
    padding-top: 16px;
  }

  .tip-text,
  .tip-link {
    font-size: 13px;
  }

  .register-footer {
    margin-top: 20px;
  }

  .footer-text {
    font-size: 11px;
  }
}
</style>
