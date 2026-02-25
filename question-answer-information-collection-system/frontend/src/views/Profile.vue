<template>
  <div class="profile-page">
    <!-- Header -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="page-title">个人中心</h1>
            <p class="page-subtitle">管理您的账户信息</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="profile-content">
      <div class="content-grid">
        <!-- User Info Card -->
        <section class="profile-card user-card">
          <div class="card-glow"></div>
          <div class="card-header">
            <h2 class="card-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              账户信息
            </h2>
            <button class="edit-btn" @click="openEditDialog" aria-label="编辑个人资料">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              编辑资料
            </button>
          </div>
          <div class="card-body">
            <div class="user-avatar-section">
              <div class="avatar-wrapper">
                <div class="avatar">
                  <span class="avatar-text">{{ userInitials }}</span>
                </div>
                <div class="avatar-ring"></div>
              </div>
              <div class="user-details">
                <h3 class="username">{{ authStore.userInfo?.username || '未知用户' }}</h3>
                <div class="user-meta">
                  <span class="role-badge" :class="authStore.isAdmin ? 'admin' : 'user'">
                    {{ authStore.isAdmin ? '管理员' : '普通用户' }}
                  </span>
                  <span class="user-id">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                      <line x1="16" y1="2" x2="16" y2="6"/>
                      <line x1="8" y1="2" x2="8" y2="6"/>
                      <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    ID: {{ authStore.userInfo?.id || '-' }}
                  </span>
                </div>
              </div>
            </div>

            <div class="info-list">
              <div class="info-item">
                <span class="info-label">用户名</span>
                <span class="info-value">{{ authStore.userInfo?.username || '-' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">角色</span>
                <span class="info-value">
                  <span class="role-badge" :class="authStore.isAdmin ? 'admin' : 'user'">
                    {{ authStore.isAdmin ? '管理员' : '普通用户' }}
                  </span>
                </span>
              </div>
              <div class="info-item">
                <span class="info-label">账户状态</span>
                <span class="info-value status-active">
                  <span class="status-dot"></span>
                  正常
                </span>
              </div>
            </div>
          </div>
        </section>

        <!-- Password Change Card -->
        <section class="profile-card password-card">
          <div class="card-glow"></div>
          <div class="card-header">
            <h2 class="card-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              修改密码
            </h2>
          </div>
          <div class="card-body">
            <el-form
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              class="password-form"
              label-position="top"
              @submit.prevent="handlePasswordSubmit"
            >
              <el-form-item label="当前密码" prop="old_password">
                <div class="input-wrapper">
                  <el-input
                    v-model="passwordForm.old_password"
                    :type="showPasswords.old ? 'text' : 'password'"
                    placeholder="请输入当前密码"
                    class="password-input"
                  >
                    <template #suffix>
                      <button
                        type="button"
                        class="toggle-btn"
                        @click="togglePassword('old')"
                      >
                        <svg v-if="showPasswords.old" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                          <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                    </template>
                  </el-input>
                </div>
              </el-form-item>

              <el-form-item label="新密码" prop="new_password">
                <div class="input-wrapper">
                  <el-input
                    v-model="passwordForm.new_password"
                    :type="showPasswords.new ? 'text' : 'password'"
                    placeholder="请输入新密码（至少6位）"
                    class="password-input"
                  >
                    <template #suffix>
                      <button
                        type="button"
                        class="toggle-btn"
                        @click="togglePassword('new')"
                      >
                        <svg v-if="showPasswords.new" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                          <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                    </template>
                  </el-input>
                </div>
              </el-form-item>

              <el-form-item label="确认新密码" prop="confirm_password">
                <div class="input-wrapper">
                  <el-input
                    v-model="passwordForm.confirm_password"
                    :type="showPasswords.confirm ? 'text' : 'password'"
                    placeholder="请再次输入新密码"
                    class="password-input"
                  >
                    <template #suffix>
                      <button
                        type="button"
                        class="toggle-btn"
                        @click="togglePassword('confirm')"
                      >
                        <svg v-if="showPasswords.confirm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                          <line x1="1" y1="1" x2="23" y2="23"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                    </template>
                  </el-input>
                </div>
              </el-form-item>

              <el-form-item class="submit-item">
                <button
                  type="submit"
                  class="submit-btn"
                  :disabled="submitLoading"
                >
                  <span v-if="!submitLoading" class="btn-content">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                    修改密码
                  </span>
                  <span v-else class="btn-loading">
                    <span class="spinner"></span>
                    处理中...
                  </span>
                </button>
              </el-form-item>
            </el-form>

            <div class="security-tips">
              <div class="tips-header">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 16v-4"/>
                  <path d="M12 8h.01"/>
                </svg>
                <span>安全提示</span>
              </div>
              <ul class="tips-list">
                <li>密码长度至少 6 个字符</li>
                <li>建议使用字母、数字组合</li>
                <li>不要使用与其他网站相同的密码</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </main>

    <!-- Edit Profile Dialog -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑资料"
      width="500px"
      :close-on-click-modal="false"
      class="edit-dialog"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-position="top"
        class="edit-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="editForm.username"
            placeholder="请输入用户名"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="editForm.email"
            placeholder="请输入邮箱（可选）"
            type="email"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="closeEditDialog">取消</button>
          <button class="confirm-btn" @click="handleEditSubmit" :disabled="editLoading">
            <span v-if="!editLoading">保存修改</span>
            <span v-else class="loading-text">
              <span class="spinner"></span>
              保存中...
            </span>
          </button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { changePassword } from '@/api/users'
import router from '@/router'

const authStore = useAuthStore()
const passwordFormRef = ref(null)

// Password visibility toggles
const showPasswords = reactive({
  old: false,
  new: false,
  confirm: false
})

// Form data
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// Submit loading state
const submitLoading = ref(false)

// Edit profile dialog
const editDialogVisible = ref(false)
const editFormRef = ref(null)
const editLoading = ref(false)

const editForm = reactive({
  username: '',
  email: ''
})

// Computed
const userInitials = computed(() => {
  const name = authStore.userInfo?.username || ''
  return name.charAt(0).toUpperCase()
})

// Validation rules
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const validateNewPassword = (rule, value, callback) => {
  if (value && value.length < 6) {
    callback(new Error('密码长度至少6个字符'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { validator: validateNewPassword, trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// Methods
const togglePassword = (field) => {
  showPasswords[field] = !showPasswords[field]
}

const openEditDialog = () => {
  // Pre-fill form with current user info
  editForm.username = authStore.userInfo?.username || ''
  editForm.email = authStore.userInfo?.email || ''
  editDialogVisible = true
}

const closeEditDialog = () => {
  editDialogVisible = false
  // Reset form
  editForm.username = authStore.userInfo?.username || ''
  editForm.email = authStore.userInfo?.email || ''
  // Clear validation errors
  editFormRef.value?.clearValidate()
}

const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
  } catch {
    return
  }

  submitLoading.value = true

  try {
    const res = await changePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })

    if (res.code === 0 || res.code === 200) {
      await ElMessageBox.alert(
        '密码修改成功，请重新登录。',
        '修改成功',
        {
          confirmButtonText: '确定',
          type: 'success',
          center: true
        }
      )
      // Clear form
      passwordForm.old_password = ''
      passwordForm.new_password = ''
      passwordForm.confirm_password = ''
      // Logout and redirect
      authStore.logout()
    } else {
      ElMessage.error(res.message || '修改失败，请检查当前密码是否正确')
    }
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error(e.response?.data?.message || '修改失败，请稍后重试')
    }
  } finally {
    submitLoading.value = false
  }
}
</script>

<style scoped>
/* Page Layout */
.profile-page {
  min-height: 100%;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  position: relative;
}

.profile-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(13, 148, 136, 0.03) 0%, transparent 40%),
    radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.03) 0%, transparent 40%);
  pointer-events: none;
}

/* Header */
.page-header {
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(13, 148, 136, 0.12) 0%, rgba(20, 184, 166, 0.12) 100%);
  border: 1px solid rgba(13, 148, 136, 0.2);
  border-radius: 16px;
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: #0d9488;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.page-title {
  font-family: 'Outfit', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  max-width: 1200px;
  position: relative;
  z-index: 1;
}

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

/* Profile Card */
.profile-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  overflow: hidden;
  animation: cardFadeIn 0.6s ease-out forwards;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.profile-card:first-child {
  animation-delay: 0.1s;
}

.profile-card:last-child {
  animation-delay: 0.2s;
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #0d9488, #14b8a6);
}

.password-card .card-glow {
  background: linear-gradient(90deg, #8b5cf6, #a78bfa);
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.card-title svg {
  width: 22px;
  height: 22px;
  color: #0d9488;
}

.password-card .card-title svg {
  color: #8b5cf6;
}

.card-body {
  padding: 1.5rem;
}

/* User Card Styles */
.user-avatar-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.avatar-wrapper {
  position: relative;
}

.avatar {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  border-radius: 20px;
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
}

.avatar-ring {
  position: absolute;
  inset: -4px;
  border: 2px solid rgba(13, 148, 136, 0.3);
  border-radius: 24px;
  animation: ringPulse 2s ease-in-out infinite;
}

@keyframes ringPulse {
  0%, 100% {
    opacity: 0.5;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.02);
  }
}

.user-details {
  flex: 1;
}

.username {
  font-size: 1.375rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.role-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.role-badge.admin {
  background: rgba(13, 148, 136, 0.1);
  color: #0d9488;
  border: 1px solid rgba(13, 148, 136, 0.2);
}

.role-badge.user {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.user-id {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8rem;
  color: #64748b;
}

.user-id svg {
  width: 14px;
  height: 14px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}

.info-label {
  font-size: 0.875rem;
  color: #64748b;
}

.info-value {
  font-size: 0.875rem;
  color: #1e293b;
  font-weight: 500;
}

.status-active {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border-radius: 50%;
  animation: statusPulse 2s ease-in-out infinite;
}

@keyframes statusPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

/* Password Form Styles */
.password-form {
  margin-bottom: 1.5rem;
}

.input-wrapper {
  width: 100%;
}

.password-input {
  width: 100%;
}

.password-input :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: none;
  padding: 0.25rem 0.75rem;
  height: 48px;
}

.password-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(139, 92, 246, 0.5);
}

.password-input :deep(.el-input__wrapper.is-focus) {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.password-input :deep(.el-input__inner) {
  color: #1e293b;
  font-size: 0.9rem;
}

.password-input :deep(.el-input__inner::placeholder) {
  color: #94a3b8;
}

.password-input :deep(.el-form-item__label) {
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
  padding-bottom: 0.5rem;
}

.toggle-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  transition: color 0.2s ease;
}

.toggle-btn:hover {
  color: #8b5cf6;
}

.toggle-btn svg {
  width: 18px;
  height: 18px;
}

.submit-item {
  margin-top: 1.5rem;
  margin-bottom: 0;
}

.submit-btn {
  width: 100%;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border: none;
  border-radius: 12px;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-content svg {
  width: 20px;
  height: 20px;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Security Tips */
.security-tips {
  padding: 1rem;
  background: rgba(139, 92, 246, 0.04);
  border: 1px solid rgba(139, 92, 246, 0.1);
  border-radius: 12px;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #8b5cf6;
}

.tips-header svg {
  width: 16px;
  height: 16px;
}

.tips-list {
  margin: 0;
  padding-left: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.tips-list li {
  font-size: 0.8rem;
  color: #64748b;
  line-height: 1.5;
}

/* Element Plus Form Override */
.password-form :deep(.el-form-item) {
  margin-bottom: 1.25rem;
}

.password-form :deep(.el-form-item__error) {
  color: #ef4444;
  font-size: 0.8rem;
  padding-top: 0.375rem;
}

/* Responsive */
@media (max-width: 640px) {
  .profile-page {
    padding: 1rem;
  }

  .user-avatar-section {
    flex-direction: column;
    text-align: center;
  }

  .user-meta {
    flex-direction: column;
    gap: 0.5rem;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

/* Edit Button */
.edit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(13, 148, 136, 0.1);
  border: 1px solid rgba(13, 148, 136, 0.2);
  border-radius: 8px;
  color: #0d9488;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: auto;
}

.edit-btn:hover {
  background: rgba(13, 148, 136, 0.15);
  border-color: rgba(13, 148, 136, 0.3);
  transform: translateY(-1px);
}

.edit-btn svg {
  width: 16px;
  height: 16px;
}

/* Dialog Styles */
.edit-dialog :deep(.el-dialog__header) {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.edit-dialog :deep(.el-dialog__title) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.edit-dialog :deep(.el-dialog__body) {
  padding: 1.5rem;
}

.edit-dialog :deep(.el-dialog__footer) {
  padding: 1rem 1.5rem;
  border-top: 1px solid #f1f5f9;
}

/* Edit Form */
.edit-form :deep(.el-form-item__label) {
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
  padding-bottom: 0.5rem;
}

.edit-form :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: none;
  padding: 0.5rem 0.75rem;
  height: 44px;
}

.edit-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(13, 148, 136, 0.5);
}

.edit-form :deep(.el-input__wrapper.is-focus) {
  border-color: #0d9488;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.edit-form :deep(.el-input__inner) {
  color: #1e293b;
  font-size: 0.9rem;
}

.edit-form :deep(.el-input__inner::placeholder) {
  color: #94a3b8;
}

/* Dialog Footer */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.cancel-btn {
  padding: 0.625rem 1.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.confirm-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.5rem;
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  border: none;
  border-radius: 10px;
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading-text .spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
</style>
