<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { resetPasswordApi } from '@/api/modules/auth'
import { isValidPhone, isValidPassword } from '@/utils'

const router = useRouter()

const step = ref(1) // 1: 输入手机号, 2: 输入新密码, 3: 完成

const form = ref({
  username: '',
  code: '',
  newPassword: '',
  confirmPassword: ''
})

const loading = ref(false)
const codeSent = ref(false)
const countdown = ref(0)

// 模拟发送验证码
async function sendCode() {
  if (!form.value.username) {
    ElMessage.warning('请输入手机号')
    return
  }
  if (!isValidPhone(form.value.username)) {
    ElMessage.warning('请输入正确的手机号')
    return
  }

  // 模拟发送验证码（实际应调用后端API）
  countdown.value = 60
  codeSent.value = true
  ElMessage.success('验证码已发送（模拟：1234）')

  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      codeSent.value = false
    }
  }, 1000)
}

// 验证验证码
function verifyCode() {
  if (!form.value.code) {
    ElMessage.warning('请输入验证码')
    return
  }
  // 模拟验证码验证（验证码：1234）
  if (form.value.code !== '1234') {
    ElMessage.warning('验证码错误')
    return
  }
  step.value = 2
}

// 重置密码
async function handleReset() {
  if (!form.value.newPassword) {
    ElMessage.warning('请输入新密码')
    return
  }
  if (!isValidPassword(form.value.newPassword)) {
    ElMessage.warning('密码长度6-20位，必须包含字母和数字')
    return
  }
  if (form.value.newPassword !== form.value.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  loading.value = true
  try {
    await resetPasswordApi({
      username: form.value.username,
      new_password: form.value.newPassword,
      code: form.value.code
    })
    step.value = 3
    ElMessage.success('密码重置成功')
  } catch (error) {
    ElMessage.error(error.message || '重置失败')
  } finally {
    loading.value = false
  }
}

// 返回登录
function goToLogin() {
  router.push({ name: 'login' })
}

// 重新开始
function restart() {
  step.value = 1
  form.value = {
    username: '',
    code: '',
    newPassword: '',
    confirmPassword: ''
  }
  codeSent.value = false
  countdown.value = 0
}
</script>

<template>
  <div class="forgot-password-view">
    <!-- Left Panel - Brand -->
    <div class="brand-panel">
      <div class="brand-mesh"></div>
      <div class="brand-grid"></div>
      <div class="brand-content">
        <!-- Logo -->
        <div class="brand-logo">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" width="32" height="32">
              <path d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-7-3c1.66 0 3 1.34 3 3H9c0-1.66 1.34-3 3-3z" fill="currentColor"/>
            </svg>
          </div>
          <span class="logo-text">CAR PARTS PRO</span>
        </div>

        <!-- Title -->
        <h1 class="brand-title">重置密码</h1>
        <p class="brand-subtitle">通过手机号验证并重置您的账户密码</p>

        <!-- Steps Indicator -->
        <div class="steps-indicator">
          <div class="step-item" :class="{ active: step >= 1, completed: step > 1 }">
            <div class="step-number">
              <svg v-if="step > 1" viewBox="0 0 24 24" fill="none" width="16" height="16">
                <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span v-else>1</span>
            </div>
            <span class="step-label">验证手机</span>
          </div>
          <div class="step-line" :class="{ active: step >= 2 }"></div>
          <div class="step-item" :class="{ active: step >= 2, completed: step > 2 }">
            <div class="step-number">
              <svg v-if="step > 2" viewBox="0 0 24 24" fill="none" width="16" height="16">
                <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span v-else>2</span>
            </div>
            <span class="step-label">设置新密码</span>
          </div>
          <div class="step-line" :class="{ active: step >= 3 }"></div>
          <div class="step-item" :class="{ active: step >= 3 }">
            <div class="step-number">
              <svg v-if="step === 3" viewBox="0 0 24 24" fill="none" width="16" height="16">
                <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span v-else>3</span>
            </div>
            <span class="step-label">完成</span>
          </div>
        </div>

        <!-- Tips -->
        <div class="tips-box">
          <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
            <path d="M12 16v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="12" cy="9" r="1" fill="currentColor"/>
          </svg>
          <span>演示验证码固定为：1234</span>
        </div>
      </div>

      <!-- Decorative Elements -->
      <div class="brand-circle brand-circle-1"></div>
      <div class="brand-circle brand-circle-2"></div>
    </div>

    <!-- Right Panel - Form -->
    <div class="form-panel">
      <div class="form-container">
        <!-- Step 1: 验证手机号 -->
        <div v-if="step === 1" class="form-step">
          <div class="form-header">
            <span class="form-badge">步骤 1/3</span>
            <h2 class="form-title">验证手机号</h2>
            <p class="form-subtitle">请输入您的注册手机号以获取验证码</p>
          </div>

          <el-form :model="form" label-position="top" class="reset-form" @submit.prevent="verifyCode">
            <el-form-item label="手机号">
              <el-input
                v-model="form.username"
                placeholder="请输入手机号"
                size="large"
                maxlength="11"
              >
                <template #prefix>
                  <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                    <path d="M22 16.92v3c0 .54-.26 1.04-.7 1.41-.44.37-1.01.56-1.59.48-2.76-.32-5.4-1.25-7.8-2.76-2.25-1.34-4.17-3.26-5.5-5.5-1.51-2.4-2.44-5.04-2.76-7.8-.08-.58.11-1.15.48-1.59.37-.44.87-.7 1.41-.7h3c.55 0 1.08.25 1.42.68.34.43.48.99.38 1.54-.08.5-.2.99-.36 1.47-.17.51-.01 1.07.4 1.45l1.2 1.2c.38.41.94.57 1.45.4.48-.16.97-.28 1.47-.36.55-.1 1.11.04 1.54.38.43.34.68.87.68 1.42z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item label="验证码">
              <div class="code-input-group">
                <el-input
                  v-model="form.code"
                  placeholder="请输入验证码"
                  size="large"
                  maxlength="6"
                >
                  <template #prefix>
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </template>
                </el-input>
                <button
                  class="code-btn"
                  :disabled="countdown > 0"
                  @click="sendCode"
                >
                  {{ countdown > 0 ? `${countdown}秒` : '发送验证码' }}
                </button>
              </div>
            </el-form-item>

            <button type="submit" class="btn btn-primary" @click="verifyCode">
              下一步
            </button>
          </el-form>
        </div>

        <!-- Step 2: 设置新密码 -->
        <div v-if="step === 2" class="form-step">
          <div class="form-header">
            <span class="form-badge">步骤 2/3</span>
            <h2 class="form-title">设置新密码</h2>
            <p class="form-subtitle">请输入您的新密码</p>
          </div>

          <el-form :model="form" label-position="top" class="reset-form" @submit.prevent="handleReset">
            <el-form-item label="新密码">
              <el-input
                v-model="form.newPassword"
                type="password"
                placeholder="6-20位，必须包含字母和数字"
                size="large"
                show-password
              >
                <template #prefix>
                  <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                    <path d="M7 11V7c0-2.76 2.24-5 5-5s5 2.24 5 5v4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item label="确认新密码">
              <el-input
                v-model="form.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                size="large"
                show-password
                @keyup.enter="handleReset"
              >
                <template #prefix>
                  <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                    <path d="M7 11V7c0-2.76 2.24-5 5-5s5 2.24 5 5v4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </template>
              </el-input>
            </el-form-item>

            <div class="form-actions">
              <button class="btn btn-secondary" @click="step = 1">上一步</button>
              <button type="submit" class="btn btn-primary" :disabled="loading" @click="handleReset">
                <span v-if="loading">重置中...</span>
                <span v-else>重置密码</span>
              </button>
            </div>
          </el-form>
        </div>

        <!-- Step 3: 完成 -->
        <div v-if="step === 3" class="form-step">
          <div class="success-content">
            <div class="success-icon">
              <svg viewBox="0 0 24 24" fill="none" width="64" height="64">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M8 12l3 3 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h2 class="success-title">密码重置成功！</h2>
            <p class="success-desc">您的密码已成功重置，现在可以使用新密码登录</p>
            <div class="success-actions">
              <button class="btn btn-primary" @click="goToLogin">立即登录</button>
              <button class="btn btn-secondary" @click="restart">重新设置</button>
            </div>
          </div>
        </div>

        <!-- Back to Login -->
        <div v-if="step < 3" class="form-footer">
          <span>记起密码了？</span>
          <button class="link-btn" @click="goToLogin">返回登录</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.forgot-password-view {
  display: flex;
  min-height: 100vh;
}

/* Brand Panel */
.brand-panel {
  position: relative;
  width: 50%;
  background: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.brand-mesh {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 50% 100%, rgba(249, 115, 22, 0.15), transparent),
    radial-gradient(ellipse 50% 40% at 0% 50%, rgba(59, 130, 246, 0.1), transparent);
  animation: meshMove 15s ease-in-out infinite;
}

@keyframes meshMove {
  0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
  50% { opacity: 0.8; transform: scale(1.1) rotate(3deg); }
}

.brand-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black, transparent);
}

.brand-content {
  position: relative;
  z-index: 2;
  padding: 60px;
  max-width: 480px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 48px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(249, 115, 22, 0.4);
}

.brand-logo .logo-text {
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.brand-title {
  font-size: 48px;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.1;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 16px;
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 48px;
}

.steps-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 32px;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 41, 59, 0.5);
  border: 2px solid rgba(71, 85, 105, 0.5);
  border-radius: 50%;
  color: #64748b;
  font-size: 14px;
  font-weight: 700;
  transition: all 0.3s ease;
}

.step-item.active .step-number {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  color: #f97316;
}

.step-item.completed .step-number {
  background: rgba(34, 197, 94, 0.15);
  border-color: #22c55e;
  color: #22c55e;
}

.step-label {
  font-size: 12px;
  color: #64748b;
}

.step-item.active .step-label {
  color: #f97316;
}

.step-line {
  width: 60px;
  height: 2px;
  background: rgba(71, 85, 105, 0.5);
  margin-top: -20px;
  transition: all 0.3s ease;
}

.step-line.active {
  background: #f97316;
}

.tips-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  font-size: 13px;
  color: #3b82f6;
}

.tips-box svg {
  flex-shrink: 0;
}

.brand-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.brand-circle-1 {
  width: 400px;
  height: 400px;
  background: #f97316;
  top: -100px;
  right: -100px;
}

.brand-circle-2 {
  width: 300px;
  height: 300px;
  background: #3b82f6;
  bottom: -50px;
  left: -50px;
}

/* Form Panel */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 40px;
}

.form-container {
  width: 100%;
  max-width: 420px;
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.3);
  border-radius: 100px;
  color: #f97316;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.form-title {
  font-size: 36px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 12px;
}

.form-subtitle {
  font-size: 14px;
  color: #94a3b8;
}

.reset-form {
  margin-bottom: 32px;
}

.reset-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.reset-form :deep(.el-input__wrapper) {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  box-shadow: none;
  transition: all 0.3s ease;
}

.reset-form :deep(.el-input__wrapper:hover),
.reset-form :deep(.el-input__wrapper.is-focus) {
  border-color: #f97316;
  background: rgba(30, 41, 59, 0.8);
}

.reset-form :deep(.el-input__inner) {
  color: #e2e8f0;
}

.reset-form :deep(.el-input__inner)::placeholder {
  color: #64748b;
}

.input-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
}

.code-input-group {
  display: flex;
  gap: 12px;
}

.code-input-group :deep(.el-input) {
  flex: 1;
}

.code-btn {
  padding: 0 20px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.5);
  border-radius: 8px;
  color: #f97316;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.code-btn:hover:not(:disabled) {
  background: rgba(249, 115, 22, 0.2);
}

.code-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 12px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 32px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  flex: 1;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(249, 115, 22, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  flex: 1;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(71, 85, 105, 0.5);
  color: #94a3b8;
}

.btn-secondary:hover {
  border-color: #f97316;
  color: #f97316;
}

.form-footer {
  text-align: center;
  font-size: 14px;
  color: #94a3b8;
}

.link-btn {
  background: none;
  border: none;
  color: #f97316;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  margin-left: 4px;
  transition: all 0.2s ease;
}

.link-btn:hover {
  text-decoration: underline;
}

/* Success Content */
.success-content {
  text-align: center;
  padding: 40px 0;
}

.success-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(34, 197, 94, 0.15);
  border-radius: 50%;
  color: #22c55e;
}

.success-title {
  font-size: 28px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 12px;
}

.success-desc {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 32px;
}

.success-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Responsive */
@media (max-width: 1024px) {
  .brand-panel {
    width: 40%;
  }
}

@media (max-width: 768px) {
  .brand-panel {
    display: none;
  }

  .form-panel {
    padding: 24px;
  }

  .form-title {
    font-size: 28px;
  }

  .steps-indicator {
    display: none;
  }
}
</style>
