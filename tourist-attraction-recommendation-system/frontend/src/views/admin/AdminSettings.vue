<template>
  <div class="admin-settings-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">个人设置</h1>
          <p class="page-subtitle">管理您的账户信息和安全设置</p>
        </div>
      </div>
    </div>

    <!-- Settings Container -->
    <div class="settings-container">
      <el-tabs v-model="activeTab" class="settings-tabs">
        <!-- Profile Tab -->
        <el-tab-pane name="profile">
          <template #label>
            <div class="tab-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <span>基本信息</span>
            </div>
          </template>

          <div class="tab-content">
            <div class="profile-section">
              <div class="profile-header">
                <div class="profile-avatar">
                  {{ profileForm.realName?.charAt(0) || profileForm.username?.charAt(0) || 'A' }}
                </div>
                <div class="profile-info">
                  <h3>{{ profileForm.realName || '管理员' }}</h3>
                  <p>{{ profileForm.username }}</p>
                </div>
                <div class="profile-badge">
                  <svg viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 2L3 7v11c0 .55.45 1 1 1h12c.55 0 1-.45 1-1V7l-7-5z"/>
                  </svg>
                  <span>管理员</span>
                </div>
              </div>

              <el-form :model="profileForm" label-width="100px" class="settings-form">
                <div class="form-section">
                  <div class="section-title">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                    </svg>
                    <span>账户信息</span>
                  </div>

                  <div class="form-grid">
                    <el-form-item label="用户名">
                      <el-input v-model="profileForm.username" disabled>
                        <template #prefix>
                          <svg viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
                          </svg>
                        </template>
                      </el-input>
                    </el-form-item>

                    <el-form-item label="真实姓名">
                      <el-input v-model="profileForm.realName" placeholder="请输入真实姓名">
                        <template #prefix>
                          <svg viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
                          </svg>
                        </template>
                      </el-input>
                    </el-form-item>

                    <el-form-item label="手机号">
                      <el-input v-model="profileForm.phone" placeholder="请输入手机号">
                        <template #prefix>
                          <svg viewBox="0 0 20 20" fill="currentColor">
                            <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                          </svg>
                        </template>
                      </el-input>
                    </el-form-item>

                    <el-form-item label="邮箱">
                      <el-input v-model="profileForm.email" placeholder="请输入邮箱">
                        <template #prefix>
                          <svg viewBox="0 0 20 20" fill="currentColor">
                            <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                            <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                          </svg>
                        </template>
                      </el-input>
                    </el-form-item>
                  </div>
                </div>
              </el-form>

              <div class="form-actions">
                <button @click="saveProfile" class="action-button save" :disabled="saving">
                  <svg v-if="!saving" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="spin" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" opacity="0.3"/>
                    <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
                  </svg>
                  {{ saving ? '保存中...' : '保存更改' }}
                </button>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Password Tab -->
        <el-tab-pane name="password">
          <template #label>
            <div class="tab-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <span>修改密码</span>
            </div>
          </template>

          <div class="tab-content">
            <div class="password-section">
              <div class="security-header">
                <div class="security-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </div>
                <div>
                  <h3>安全设置</h3>
                  <p>定期更换密码以保护账户安全</p>
                </div>
              </div>

              <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px" class="settings-form">
                <div class="form-section">
                  <div class="section-title">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
                    </svg>
                    <span>更改密码</span>
                  </div>

                  <div class="password-fields">
                    <el-form-item label="当前密码" prop="oldPassword">
                      <el-input v-model="passwordForm.oldPassword" type="password" show-password placeholder="请输入当前密码">
                        <template #prefix>
                          <svg viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
                          </svg>
                        </template>
                      </el-input>
                    </el-form-item>

                    <el-form-item label="新密码" prop="newPassword">
                      <el-input v-model="passwordForm.newPassword" type="password" show-password placeholder="请输入新密码">
                        <template #prefix>
                          <svg viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
                          </svg>
                        </template>
                      </el-input>
                      <div class="password-hint">
                        <svg viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                        </svg>
                        <span>密码长度至少6位，建议包含字母、数字和特殊字符</span>
                      </div>
                    </el-form-item>

                    <el-form-item label="确认密码" prop="confirmPassword">
                      <el-input v-model="passwordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码">
                        <template #prefix>
                          <svg viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
                          </svg>
                        </template>
                      </el-input>
                    </el-form-item>
                  </div>
                </div>
              </el-form>

              <div class="form-actions">
                <button @click="changePassword" class="action-button save" :disabled="changingPassword">
                  <svg v-if="!changingPassword" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else class="spin" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" opacity="0.3"/>
                    <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
                  </svg>
                  {{ changingPassword ? '修改中...' : '修改密码' }}
                </button>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const activeTab = ref('profile')
const passwordFormRef = ref(null)
const saving = ref(false)
const changingPassword = ref(false)

const profileForm = reactive({
  username: '',
  realName: '',
  phone: '',
  email: ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  oldPassword: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

onMounted(async () => {
  const info = await userStore.getUserInfo()
  Object.assign(profileForm, info)
})

async function saveProfile() {
  saving.value = true
  try {
    await userStore.updateProfile(profileForm)
    ElMessage.success('保存成功')
  } catch (error) {
    console.error(error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

async function changePassword() {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    changingPassword.value = true
    await userStore.changePassword(passwordForm.oldPassword, passwordForm.newPassword)
    ElMessage.success('密码修改成功')
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (error) {
    if (error !== false) {
      console.error(error)
      ElMessage.error('修改失败')
    }
  } finally {
    changingPassword.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.admin-settings-page {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Header */
.page-header {
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e9d5ff 0%, #d8b4fe 100%);
  border-radius: 16px;
  color: #1e3a5f;
}

.header-icon svg {
  width: 28px;
  height: 28px;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #6b7280;
}

/* Settings Container */
.settings-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.settings-tabs {
  padding: 0;
}

:deep(.settings-tabs .el-tabs__header) {
  margin: 0;
  padding: 0 24px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

:deep(.settings-tabs .el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.settings-tabs .el-tabs__item) {
  padding: 20px 24px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 600;
}

:deep(.settings-tabs .el-tabs__item.is-active) {
  color: #1e3a5f;
}

:deep(.settings-tabs .el-tabs__active-bar) {
  background: linear-gradient(90deg, #fbbf24 0%, #f97316 100%);
  height: 3px;
}

:deep(.settings-tabs .el-tabs__content) {
  padding: 0;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-label svg {
  width: 18px;
  height: 18px;
}

.tab-content {
  padding: 32px;
}

/* Profile Section */
.profile-section,
.password-section {
  max-width: 700px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  border-radius: 16px;
  margin-bottom: 32px;
  color: white;
}

.profile-avatar {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%);
  color: white;
  font-size: 32px;
  font-weight: 700;
  border-radius: 18px;
  flex-shrink: 0;
}

.profile-info h3 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 4px;
}

.profile-info p {
  font-size: 14px;
  opacity: 0.8;
}

.profile-badge {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.profile-badge svg {
  width: 14px;
  height: 14px;
}

/* Security Header */
.security-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
  border-radius: 16px;
  margin-bottom: 32px;
}

.security-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 14px;
  color: #f97316;
}

.security-icon svg {
  width: 28px;
  height: 28px;
}

.security-header h3 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.security-header p {
  font-size: 14px;
  color: #6b7280;
}

/* Form */
.settings-form {
  max-width: 600px;
}

.form-section {
  margin-bottom: 32px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.section-title svg {
  width: 20px;
  height: 20px;
  color: #fbbf24;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.password-fields {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  border: 2px solid #e5e7eb;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #fbbf24;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #fbbf24;
  box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.1);
}

:deep(.el-input__inner) {
  font-size: 14px;
  color: #1f2937;
}

:deep(.el-input__prefix) {
  color: #9ca3af;
}

:deep(.el-input__prefix svg) {
  width: 18px;
  height: 18px;
}

.password-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  font-size: 12px;
  color: #9ca3af;
}

.password-hint svg {
  width: 14px;
  height: 14px;
  color: #fbbf24;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
  color: white;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  min-width: 140px;
}

.action-button svg {
  width: 18px;
  height: 18px;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(30, 58, 95, 0.3);
}

.action-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .tab-content {
    padding: 20px;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .profile-badge {
    margin-left: 0;
  }

  .security-header {
    flex-direction: column;
    text-align: center;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    justify-content: stretch;
  }

  .action-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
