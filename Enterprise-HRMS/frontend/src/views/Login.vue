<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '../stores/auth'
import { User, Lock } from '@element-plus/icons-vue'

const authStore = useAuthStore()

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

const loginFormRef = ref(null)

async function handleLogin() {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await authStore.login(form.username, form.password)
      } catch (error) {
        // 错误已在 store 中处理
      }
    }
  })
}
</script>

<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-shape shape-1"></div>
      <div class="bg-shape shape-2"></div>
      <div class="bg-shape shape-3"></div>
    </div>

    <div class="login-wrapper">
      <div class="login-card">
        <!-- 品牌区域 -->
        <div class="login-brand">
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
          <h1 class="brand-title">企业 HRMS</h1>
          <p class="brand-subtitle">人力资源管理系统</p>
        </div>

        <!-- 登录表单 -->
        <el-form
          ref="loginFormRef"
          :model="form"
          :rules="rules"
          class="login-form"
        >
          <el-form-item prop="username" class="form-item">
            <div class="input-wrapper">
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                :prefix-icon="User"
                clearable
                @keyup.enter="handleLogin"
                class="custom-input"
              />
            </div>
          </el-form-item>

          <el-form-item prop="password" class="form-item">
            <div class="input-wrapper">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                :prefix-icon="Lock"
                show-password
                @keyup.enter="handleLogin"
                class="custom-input"
              />
            </div>
          </el-form-item>

          <el-form-item class="form-item">
            <el-button
              type="primary"
              :loading="authStore.loading"
              class="submit-btn"
              @click="handleLogin"
            >
              <span class="btn-content">
                <span class="btn-text">{{ authStore.loading ? '登录中...' : '登 录' }}</span>
                <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </span>
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-tip">
          <span class="tip-text">首次使用请先</span>
          <a href="#" class="tip-link">注册账号</a>
        </div>
      </div>

      <div class="login-footer">
        <div class="footer-line"></div>
        <span class="footer-text">Enterprise HRMS v1.0</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   Login Page - Modern Corporate Design
   ======================================== */
.login-page {
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

/* 登录卡片容器 */
.login-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

/* 登录卡片 */
.login-card {
  width: 420px;
  padding: 48px 40px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light), var(--color-success));
}

.login-card:hover {
  box-shadow: var(--shadow-2xl);
  transform: translateY(-2px);
}

/* 品牌区域 */
.login-brand {
  text-align: center;
  margin-bottom: 36px;
}

.brand-icon-wrapper {
  position: relative;
  width: 72px;
  height: 72px;
  margin: 0 auto 20px;
}

.brand-icon {
  width: 72px;
  height: 72px;
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
  width: 36px;
  height: 36px;
}

.brand-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.2) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
}

.brand-title {
  font-size: 26px;
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
.login-form {
  margin-top: 20px;
}

.form-item {
  margin-bottom: 24px;
}

.form-item:last-of-type {
  margin-bottom: 0;
}

.input-wrapper {
  position: relative;
}

.custom-input :deep(.el-input__wrapper) {
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--color-gray-50);
  border: 1px solid var(--color-border-light);
  box-shadow: none;
  transition: all var(--transition-fast);
}

.custom-input :deep(.el-input__wrapper:hover) {
  border-color: var(--color-primary);
  background: var(--color-bg-secondary);
}

.custom-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--color-primary);
  background: var(--color-bg-secondary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.custom-input :deep(.el-input__inner) {
  height: 48px;
  font-size: 15px;
  color: var(--color-text-primary);
}

.custom-input :deep(.el-input__inner::placeholder) {
  color: var(--color-text-tertiary);
}

.custom-input :deep(.el-input__prefix) {
  color: var(--color-text-tertiary);
}

.custom-input :deep(.el-input__prefix:hover) {
  color: var(--color-primary);
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 2px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  border: none;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
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
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}

.submit-btn:hover::before {
  left: 100%;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow-primary), var(--shadow-lg);
}

.submit-btn:active {
  transform: translateY(0);
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
  transition: transform var(--transition-fast);
}

.submit-btn:hover .btn-icon {
  transform: translateX(4px);
}

/* 登录提示 */
.login-tip {
  text-align: center;
  margin-top: 32px;
  padding-top: 28px;
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
  transition: all var(--transition-fast);
}

.tip-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

/* 底部 */
.login-footer {
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
@media (max-width: 480px) {
  .login-card {
    width: calc(100% - 32px);
    padding: 40px 28px;
  }

  .brand-title {
    font-size: 22px;
  }

  .brand-icon-wrapper {
    width: 60px;
    height: 60px;
  }

  .brand-icon {
    width: 60px;
    height: 60px;
  }

  .brand-icon svg {
    width: 30px;
    height: 30px;
  }

  .custom-input :deep(.el-input__wrapper) {
    height: 44px;
  }

  .submit-btn {
    height: 44px;
  }
}
</style>
