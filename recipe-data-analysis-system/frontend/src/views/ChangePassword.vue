<template>
  <div class="change-password-container">
    <!-- 顶部导航 -->
    <div class="password-header">
      <div class="header-content">
        <button class="back-button" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>返回</span>
        </button>
        <h1 class="page-title">修改密码</h1>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="password-content">
      <div class="password-card">
        <!-- 密码修改表单 -->
        <el-form
          ref="formRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-position="top"
          class="password-form"
        >
          <!-- 提示信息 -->
          <div class="form-tip">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <p>修改密码后，您需要重新登录</p>
          </div>

          <!-- 旧密码 -->
          <el-form-item label="旧密码" prop="old_password">
            <el-input
              v-model="passwordForm.old_password"
              type="password"
              placeholder="请输入当前密码"
              show-password
              clearable
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 14C13.6569 14 15 12.6569 15 11C15 9.34315 13.6569 8 12 8C10.3431 8 9 9.34315 9 11C9 12.6569 10.3431 14 12 14Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M20 11C20 15.4183 16.4183 19 12 19C7.58172 19 4 15.4183 4 11C4 6.58172 7.58172 3 12 3C16.4183 3 20 6.58172 20 11Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 15V21M8 21H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </template>
            </el-input>
          </el-form-item>

          <!-- 新密码 -->
          <el-form-item label="新密码" prop="new_password">
            <el-input
              v-model="passwordForm.new_password"
              type="password"
              placeholder="请输入新密码（至少 8 位）"
              show-password
              clearable
              @input="checkPasswordStrength"
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 14C13.6569 14 15 12.6569 15 11C15 9.34315 13.6569 8 12 8C10.3431 8 9 9.34315 9 11C9 12.6569 10.3431 14 12 14Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M20 11C20 15.4183 16.4183 19 12 19C7.58172 19 4 15.4183 4 11C4 6.58172 7.58172 3 12 3C16.4183 3 20 6.58172 20 11Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 15V21M8 21H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </template>
            </el-input>
            <!-- 密码强度指示器 -->
            <div v-if="passwordForm.new_password" class="password-strength">
              <div class="strength-label">密码强度：</div>
              <div class="strength-bar">
                <div
                  class="strength-fill"
                  :class="strengthClass"
                  :style="{ width: strengthPercent + '%' }"
                ></div>
              </div>
              <div class="strength-text" :class="strengthClass">{{ strengthLabel }}</div>
            </div>
          </el-form-item>

          <!-- 确认新密码 -->
          <el-form-item label="确认新密码" prop="new_password_confirm">
            <el-input
              v-model="passwordForm.new_password_confirm"
              type="password"
              placeholder="请再次输入新密码"
              show-password
              clearable
            >
              <template #prefix>
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </template>
            </el-input>
          </el-form-item>

          <!-- 提交按钮 -->
          <el-form-item>
            <el-button
              type="primary"
              class="submit-button"
              :loading="submitting"
              @click="handleSubmit"
            >
              <template v-if="!submitting">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                确认修改
              </template>
              <template v-else>
                修改中...
              </template>
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { changePassword } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const submitting = ref(false)

// 密码表单
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

// 密码强度相关
const passwordStrength = ref(0)

// 计算密码强度级别
const strengthLabel = computed(() => {
  switch (passwordStrength.value) {
    case 0: return '弱'
    case 1: return '弱'
    case 2: return '中'
    case 3: return '强'
    default: return '弱'
  }
})

const strengthClass = computed(() => {
  switch (passwordStrength.value) {
    case 0: return 'weak'
    case 1: return 'weak'
    case 2: return 'medium'
    case 3: return 'strong'
    default: return 'weak'
  }
})

const strengthPercent = computed(() => {
  switch (passwordStrength.value) {
    case 0: return 25
    case 1: return 25
    case 2: return 66
    case 3: return 100
    default: return 25
  }
})

// 检查密码强度
const checkPasswordStrength = () => {
  const password = passwordForm.new_password
  let strength = 0

  if (password.length >= 8) strength++
  if (password.length >= 12) strength++
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
  if (/\d/.test(password)) strength++
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++

  // 最多3级
  passwordStrength.value = Math.min(strength, 3)
}

// 自定义验证规则：确认密码匹配
const validatePasswordConfirm = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 自定义验证规则：新密码不能与旧密码相同
const validateNewPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入新密码'))
  } else if (value === passwordForm.old_password) {
    callback(new Error('新密码不能与旧密码相同'))
  } else if (value.length < 8) {
    callback(new Error('密码长度至少 8 位'))
  } else {
    callback()
  }
}

// 表单验证规则
const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, validator: validateNewPassword, trigger: 'blur' }
  ],
  new_password_confirm: [
    { required: true, validator: validatePasswordConfirm, trigger: 'blur' }
  ]
}

// 提交修改
const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    const response = await changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
      new_password_confirm: passwordForm.new_password_confirm
    })

    if (response.code === 200) {
      ElMessage.success('密码修改成功，请重新登录')

      // 清除登录状态
      userStore.logout()

      // 延迟跳转到登录页
      setTimeout(() => {
        router.push({ name: 'login' })
      }, 1500)
    }
  } catch (error) {
    ElMessage.error('修改失败：' + error.message)
  } finally {
    submitting.value = false
  }
}

// 返回上一页
const goBack = () => {
  router.back()
}
</script>

<style scoped>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.change-password-container {
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
  background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
}

/* ========== 顶部导航 ========== */
.password-header {
  background: white;
  border-bottom: 1px solid #f0ebe3;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-content {
  max-width: 500px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  color: #8b7355;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: #f5f0e8;
  color: #c2622e;
}

.back-button svg {
  width: 20px;
  height: 20px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #3d2914;
}

/* ========== 主要内容区 ========== */
.password-content {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
}

.password-card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08), 0 0 1px rgba(61, 41, 20, 0.1);
  padding: 2.5rem;
  animation: fadeInUp 0.5s ease-out;
}

/* ========== 提示信息 ========== */
.form-tip {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, rgba(212, 119, 58, 0.1) 0%, rgba(194, 98, 46, 0.1) 100%);
  border: 1.5px solid rgba(212, 119, 58, 0.2);
  border-radius: 12px;
  margin-bottom: 2rem;
}

.form-tip svg {
  width: 20px;
  height: 20px;
  color: #c2622e;
  flex-shrink: 0;
}

.form-tip p {
  margin: 0;
  font-size: 0.9rem;
  color: #a35220;
  font-weight: 500;
}

/* ========== 表单样式 ========== */
.password-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.password-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #3d2914;
  font-size: 0.9rem;
}

.password-form :deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 1.5px solid #e5ddd3;
  box-shadow: none;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  transition: all 0.2s ease;
  background: #fafafa;
}

.password-form :deep(.el-input__wrapper:hover) {
  border-color: #d4773a;
  background: white;
}

.password-form :deep(.el-input__wrapper.is-focus) {
  border-color: #c2622e;
  box-shadow: 0 0 0 3px rgba(194, 98, 46, 0.1);
  background: white;
}

.password-form :deep(.el-input__inner) {
  font-size: 0.95rem;
  color: #3d2914;
}

.password-form :deep(.el-input__prefix) {
  left: 0.75rem;
}

.input-icon {
  width: 18px;
  height: 18px;
  color: #8b7355;
}

/* ========== 密码强度指示器 ========== */
.password-strength {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.strength-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #8b7355;
  white-space: nowrap;
}

.strength-bar {
  flex: 1;
  height: 6px;
  background: #e5ddd3;
  border-radius: 3px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  border-radius: 3px;
  transition: all 0.3s ease;
}

.strength-fill.weak {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.strength-fill.medium {
  background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
}

.strength-fill.strong {
  background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
}

.strength-text {
  font-size: 0.8rem;
  font-weight: 700;
  min-width: 2rem;
  text-align: right;
}

.strength-text.weak {
  color: #dc2626;
}

.strength-text.medium {
  color: #d97706;
}

.strength-text.strong {
  color: #16a34a;
}

/* ========== 提交按钮 ========== */
.submit-button {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border: none;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(194, 98, 46, 0.3);
}

.submit-button:active {
  transform: translateY(0);
}

.submit-button svg {
  width: 18px;
  height: 18px;
}

.submit-button.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-button.is-disabled:hover {
  transform: none;
  box-shadow: none;
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .password-content {
    padding: 1rem;
  }

  .password-card {
    padding: 1.5rem;
  }

  .header-content {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.25rem;
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
</style>
