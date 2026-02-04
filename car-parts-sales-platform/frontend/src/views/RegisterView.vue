<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { isValidPhone, isValidPassword } from '@/utils'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  phone: '',
  password: '',
  password_confirm: '',
  nickname: ''
})

const loading = ref(false)
const agreedToTerms = ref(false)

async function handleRegister() {
  if (!form.value.phone) {
    ElMessage.warning('请输入手机号')
    return
  }
  if (!isValidPhone(form.value.phone)) {
    ElMessage.warning('请输入正确的手机号')
    return
  }
  if (!form.value.password) {
    ElMessage.warning('请输入密码')
    return
  }
  if (!isValidPassword(form.value.password)) {
    ElMessage.warning('密码长度6-20位，必须包含字母和数字')
    return
  }
  if (form.value.password !== form.value.password_confirm) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  if (!agreedToTerms.value) {
    ElMessage.warning('请阅读并同意服务条款和隐私政策')
    return
  }

  loading.value = true
  try {
    await authStore.register({
      phone: form.value.phone,
      password: form.value.password,
      password_confirm: form.value.password_confirm,
      nickname: form.value.nickname || form.value.phone
    })
    ElMessage.success('注册成功')
    router.push({ name: 'home' })
  } catch (error) {
    ElMessage.error(error.message || '注册失败')
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="register-view">
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

        <!-- Welcome Message -->
        <h1 class="brand-title">加入会员</h1>
        <p class="brand-subtitle">创建您的账户，开启专业改装之旅</p>

        <!-- Benefits -->
        <div class="brand-benefits">
          <div class="benefit-item">
            <div class="benefit-icon">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="benefit-info">
              <span class="benefit-title">会员专享价</span>
              <span class="benefit-desc">注册即享会员优惠价</span>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <path d="M12 8V13L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="benefit-info">
              <span class="benefit-title">快速发货</span>
              <span class="benefit-desc">当日下单当日发货</span>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <path d="M22 16.92v3c0 .54-.26 1.04-.7 1.41-.44.37-1.01.56-1.59.48-2.76-.32-5.4-1.25-7.8-2.76-2.25-1.34-4.17-3.26-5.5-5.5-1.51-2.4-2.44-5.04-2.76-7.8-.08-.58.11-1.15.48-1.59.37-.44.87-.7 1.41-.7h3c.55 0 1.08.25 1.42.68.34.43.48.99.38 1.54-.08.5-.2.99-.36 1.47-.17.51-.01 1.07.4 1.45l1.2 1.2c.38.41.94.57 1.45.4.48-.16.97-.28 1.47-.36.55-.1 1.11.04 1.54.38.43.34.68.87.68 1.42z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="benefit-info">
              <span class="benefit-title">专业支持</span>
              <span class="benefit-desc">7x24小时技术支持</span>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="benefit-info">
              <span class="benefit-title">正品保障</span>
              <span class="benefit-desc">100%正品质量保证</span>
            </div>
          </div>
        </div>

        <!-- Trust Badge -->
        <div class="trust-badge">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>已有 10,000+ 用户信赖</span>
        </div>
      </div>

      <!-- Decorative Elements -->
      <div class="brand-circle brand-circle-1"></div>
      <div class="brand-circle brand-circle-2"></div>
    </div>

    <!-- Right Panel - Register Form -->
    <div class="form-panel">
      <div class="form-container">
        <!-- Form Header -->
        <div class="form-header">
          <span class="form-badge">新用户注册</span>
          <h2 class="form-title">创建账户</h2>
          <p class="form-subtitle">填写信息加入我们的改装社区</p>
        </div>

        <!-- Register Form -->
        <el-form :model="form" label-position="top" class="register-form" @submit.prevent="handleRegister">
          <el-form-item label="手机号">
            <el-input
              v-model="form.phone"
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

          <el-form-item label="昵称（可选）">
            <el-input
              v-model="form.nickname"
              placeholder="请输入昵称，默认使用手机号"
              size="large"
              maxlength="20"
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                </svg>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="密码">
            <el-input
              v-model="form.password"
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

          <el-form-item label="确认密码">
            <el-input
              v-model="form.password_confirm"
              type="password"
              placeholder="请再次输入密码"
              size="large"
              show-password
              @keyup.enter="handleRegister"
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
            <el-checkbox v-model="agreedToTerms">
              我已阅读并同意
              <el-link type="primary">《服务条款》</el-link>
              和
              <el-link type="primary">《隐私政策》</el-link>
            </el-checkbox>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading" @click="handleRegister">
            <span v-if="loading">
              <svg class="loading-icon" viewBox="0 0 24 24" fill="none" width="20" height="20">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                <path d="M22 12c0-5.52-4.48-10-10-10" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
                </path>
              </svg>
              注册中...
            </span>
            <span v-else>立即注册</span>
          </button>
        </el-form>

        <!-- Form Footer -->
        <div class="form-footer">
          <span>已有账户？</span>
          <button class="link-btn" @click="goToLogin">立即登录</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-view {
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
  margin-bottom: 40px;
}

.brand-benefits {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.benefit-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(249, 115, 22, 0.15);
  border-radius: 10px;
  color: #f97316;
  flex-shrink: 0;
}

.benefit-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.benefit-title {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.benefit-desc {
  font-size: 12px;
  color: #94a3b8;
}

.trust-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: 8px;
  font-size: 13px;
  color: #22c55e;
}

.trust-badge svg {
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
  margin-bottom: 40px;
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

.register-form {
  margin-bottom: 32px;
}

.register-form :deep(.el-form-item__label) {
  font-size: 13px;
  font-weight: 600;
  color: #e2e8f0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.register-form :deep(.el-input__wrapper) {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  box-shadow: none;
  transition: all 0.3s ease;
}

.register-form :deep(.el-input__wrapper:hover),
.register-form :deep(.el-input__wrapper.is-focus) {
  border-color: #f97316;
  background: rgba(30, 41, 59, 0.8);
}

.register-form :deep(.el-input__inner) {
  color: #e2e8f0;
}

.register-form :deep(.el-input__inner)::placeholder {
  color: #64748b;
}

.input-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
}

.form-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
}

.form-actions :deep(.el-checkbox__label) {
  font-size: 13px;
  color: #94a3b8;
}

.form-actions :deep(.el-link--primary) {
  color: #f97316;
  font-size: 13px;
}

.form-actions :deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: #f97316;
}

.form-actions :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #f97316;
  border-color: #f97316;
}

.btn {
  width: 100%;
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

.loading-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

  .brand-benefits {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .benefit-item {
    flex: 1;
    min-width: 140px;
  }
}
</style>
