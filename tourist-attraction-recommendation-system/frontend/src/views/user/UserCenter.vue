<template>
  <div class="user-center-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-decoration"></div>
      <div class="header-content">
        <div class="avatar-section">
          <div class="avatar-wrapper">
            <div class="avatar-ring">
              <div class="avatar-inner">
                {{ userStore.user?.realName?.charAt(0) || 'U' }}
              </div>
            </div>
            <button class="avatar-edit-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 20h9"/>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
            </button>
          </div>
        </div>
        <div class="user-info">
          <h1 class="user-name">{{ userStore.user?.realName || '游客' }}</h1>
          <p class="user-handle">@{{ userStore.user?.username }}</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <div class="max-width-container">
        <!-- Tab Navigation -->
        <div class="tab-navigation">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            :class="['tab-btn', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            <span class="tab-icon" v-html="tab.icon"></span>
            <span class="tab-label">{{ tab.label }}</span>
            <span class="tab-indicator"></span>
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Profile Tab -->
          <div v-show="activeTab === 'profile'" class="tab-panel" :class="{ active: activeTab === 'profile' }">
            <div class="panel-header">
              <h2>个人信息</h2>
              <p>管理您的个人信息和联系方式</p>
            </div>

            <el-form
              ref="profileFormRef"
              :model="profileForm"
              :rules="profileRules"
              label-position="top"
              class="profile-form"
            >
              <div class="form-row">
                <div class="form-col">
                  <el-form-item label="用户名" prop="username">
                    <el-input v-model="profileForm.username" disabled class="disabled-input">
                      <template #prefix>
                        <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                          <circle cx="12" cy="7" r="4"/>
                        </svg>
                      </template>
                    </el-input>
                  </el-form-item>
                </div>

                <div class="form-col">
                  <el-form-item label="真实姓名" prop="realName">
                    <el-input v-model="profileForm.realName" placeholder="请输入真实姓名">
                      <template #prefix>
                        <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                          <circle cx="12" cy="7" r="4"/>
                        </svg>
                      </template>
                    </el-input>
                  </el-form-item>
                </div>
              </div>

              <div class="form-row">
                <div class="form-col">
                  <el-form-item label="手机号码" prop="phone">
                    <el-input v-model="profileForm.phone" placeholder="请输入手机号码" maxlength="11">
                      <template #prefix>
                        <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                        </svg>
                      </template>
                    </el-input>
                  </el-form-item>
                </div>

                <div class="form-col">
                  <el-form-item label="电子邮箱" prop="email">
                    <el-input v-model="profileForm.email" placeholder="请输入电子邮箱">
                      <template #prefix>
                        <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                          <polyline points="22,6 12,13 2,6"/>
                        </svg>
                      </template>
                    </el-input>
                  </el-form-item>
                </div>
              </div>

              <div class="form-actions">
                <button type="button" class="btn-primary" @click="saveProfile">
                  <span>保存修改</span>
                  <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                    <polyline points="17 21 17 13 7 13 7 21"/>
                    <polyline points="7 3 7 8 15 8"/>
                  </svg>
                </button>
              </div>
            </el-form>
          </div>

          <!-- Password Tab -->
          <div v-show="activeTab === 'password'" class="tab-panel" :class="{ active: activeTab === 'password' }">
            <div class="panel-header">
              <h2>修改密码</h2>
              <p>为了您的账户安全，请定期更换密码</p>
            </div>

            <div class="security-notice">
              <svg class="notice-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <div class="notice-content">
                <h4>安全提示</h4>
                <p>建议使用8位以上包含字母、数字和特殊字符的密码</p>
              </div>
            </div>

            <el-form
              ref="passwordFormRef"
              :model="passwordForm"
              :rules="passwordRules"
              label-position="top"
              class="password-form"
            >
              <el-form-item label="当前密码" prop="oldPassword">
                <el-input
                  v-model="passwordForm.oldPassword"
                  type="password"
                  placeholder="请输入当前密码"
                  show-password
                >
                  <template #prefix>
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                  </template>
                </el-input>
              </el-form-item>

              <el-form-item label="新密码" prop="newPassword">
                <el-input
                  v-model="passwordForm.newPassword"
                  type="password"
                  placeholder="请输入新密码"
                  show-password
                >
                  <template #prefix>
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                  </template>
                </el-input>
              </el-form-item>

              <el-form-item label="确认新密码" prop="confirmPassword">
                <el-input
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  placeholder="请再次输入新密码"
                  show-password
                >
                  <template #prefix>
                    <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                  </template>
                </el-input>
              </el-form-item>

              <div class="form-actions">
                <button type="button" class="btn-primary" @click="changePassword">
                  <span>修改密码</span>
                  <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 9.9-1"/>
                  </svg>
                </button>
              </div>
            </el-form>
          </div>

          <!-- Delete Account Tab -->
          <div v-show="activeTab === 'delete'" class="tab-panel" :class="{ active: activeTab === 'delete' }">
            <div class="delete-section">
              <div class="delete-illustration">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              </div>

              <div class="delete-content">
                <h2>注销账号</h2>
                <p class="delete-warning">此操作不可恢复，请谨慎操作</p>

                <div class="delete-consequences">
                  <h4>注销后，您将失去：</h4>
                  <ul>
                    <li>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                      所有个人信息和账户数据
                    </li>
                    <li>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                      收藏的景点列表
                    </li>
                    <li>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                      历史评论和互动记录
                    </li>
                  </ul>
                </div>

                <button class="btn-danger" @click="confirmDeleteAccount">
                  <span>确认注销账号</span>
                  <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18"/>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()

const activeTab = ref('profile')
const profileFormRef = ref(null)
const passwordFormRef = ref(null)

const tabs = [
  {
    key: 'profile',
    label: '个人信息',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`
  },
  {
    key: 'password',
    label: '修改密码',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>`
  },
  {
    key: 'delete',
    label: '账号注销',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>`
  }
]

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

const profileRules = {
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入电子邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
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
  Object.assign(profileForm, {
    username: info.username,
    realName: info.realName,
    phone: info.phone,
    email: info.email
  })
})

async function saveProfile() {
  await profileFormRef.value.validate()
  await userStore.updateProfile(profileForm)
  ElMessage.success('个人信息已更新')
}

async function changePassword() {
  await passwordFormRef.value.validate()
  await userStore.changePassword(passwordForm.oldPassword, passwordForm.newPassword)
  ElMessage.success('密码修改成功')

  // Reset form
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  passwordFormRef.value.resetFields()
}

async function confirmDeleteAccount() {
  try {
    await ElMessageBox.confirm(
      '注销账号后，您的所有数据将被永久删除且无法恢复。确定要继续吗？',
      '确认注销账号',
      {
        confirmButtonText: '确认注销',
        cancelButtonText: '取消',
        type: 'warning',
        customClass: 'delete-confirm-dialog'
      }
    )

    await ElMessageBox.confirm(
      '这是最后一次确认！注销后您的账号将立即失效。',
      '最终确认',
      {
        confirmButtonText: '我已了解后果，确认注销',
        cancelButtonText: '我再想想',
        type: 'error',
        customClass: 'delete-confirm-dialog'
      }
    )

    // Delete account
    await userStore.deleteAccount()
    ElMessage.success('账号已注销')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Delete account error:', error)
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.user-center-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  padding-bottom: 60px;
}

/* Header Section */
.page-header {
  position: relative;
  padding: 60px 20px 40px;
  text-align: center;
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 300px;
  background: radial-gradient(ellipse at center, rgba(30, 58, 95, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.header-content {
  position: relative;
  max-width: 400px;
  margin: 0 auto;
  animation: fadeInUp 0.6s ease;
}

.avatar-section {
  margin-bottom: 20px;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
}

.avatar-ring {
  width: 120px;
  height: 120px;
  padding: 4px;
  background: linear-gradient(135deg, #1e3a5f 0%, #f59e0b 100%);
  border-radius: 50%;
  animation: rotate 20s linear infinite;
}

.avatar-inner {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
  font-family: 'DM Sans', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  color: #1e3a5f;
}

.avatar-edit-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f59e0b;
  border: 3px solid white;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar-edit-btn:hover {
  transform: scale(1.1);
}

.avatar-edit-btn svg {
  width: 16px;
  height: 16px;
  color: white;
}

.user-name {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 700;
  color: #1e3a5f;
  margin-bottom: 4px;
}

.user-handle {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
  font-size: 0.95rem;
}

/* Content Wrapper */
.content-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.max-width-container {
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 24px rgba(30, 58, 95, 0.08);
  overflow: hidden;
  animation: fadeInUp 0.6s ease 0.1s both;
}

/* Tab Navigation */
.tab-navigation {
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 8px;
}

.tab-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 16px;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.tab-icon {
  width: 24px;
  height: 24px;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.tab-btn:hover .tab-icon {
  color: #64748b;
}

.tab-btn.active .tab-icon {
  color: #1e3a5f;
}

.tab-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  color: #64748b;
  transition: all 0.3s ease;
}

.tab-btn:hover .tab-label {
  color: #475569;
}

.tab-btn.active .tab-label {
  color: #1e3a5f;
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #1e3a5f 0%, #f59e0b 100%);
  border-radius: 3px 3px 0 0;
  transition: transform 0.3s ease;
}

.tab-btn.active .tab-indicator {
  transform: translateX(-50%) scaleX(1);
}

/* Tab Content */
.tab-content {
  padding: 40px;
}

.tab-panel {
  display: none;
  animation: fadeIn 0.4s ease;
}

.tab-panel.active {
  display: block;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.panel-header {
  margin-bottom: 32px;
}

.panel-header h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 8px;
}

.panel-header p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
}

/* Forms */
.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.form-col {
  min-width: 0;
}

:deep(.el-form-item__label) {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  box-shadow: none;
  padding: 8px 16px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1;
}

:deep(.el-input__wrapper.is-focus) {
  border-color: #1e3a5f;
  box-shadow: 0 0 0 4px rgba(30, 58, 95, 0.1);
}

:deep(.el-input__inner) {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
}

.disabled-input :deep(.el-input__wrapper) {
  background: #f1f5f9;
}

.input-icon {
  width: 18px;
  height: 18px;
  color: #94a3b8;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 32px;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 32px;
  background: linear-gradient(135deg, #1e3a5f 0%, #2d4a6f 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(30, 58, 95, 0.25);
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* Security Notice */
.security-notice {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.05) 0%, rgba(245, 158, 11, 0.05) 100%);
  border: 1px solid rgba(30, 58, 95, 0.1);
  border-radius: 16px;
  margin-bottom: 32px;
}

.notice-icon {
  width: 40px;
  height: 40px;
  color: #f59e0b;
  flex-shrink: 0;
}

.notice-content h4 {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 4px;
}

.notice-content p {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #64748b;
}

/* Delete Section */
.delete-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
}

.delete-illustration {
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
  border-radius: 50%;
  margin-bottom: 24px;
}

.delete-illustration svg {
  width: 60px;
  height: 60px;
  color: #ef4444;
}

.delete-content {
  text-align: center;
  max-width: 500px;
}

.delete-content h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 8px;
}

.delete-warning {
  font-family: 'DM Sans', sans-serif;
  color: #ef4444;
  font-weight: 600;
  margin-bottom: 32px;
}

.delete-consequences {
  text-align: left;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
}

.delete-consequences h4 {
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  color: #991b1b;
  margin-bottom: 16px;
}

.delete-consequences ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.delete-consequences li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'DM Sans', sans-serif;
  color: #7f1d1d;
  margin-bottom: 12px;
}

.delete-consequences li:last-child {
  margin-bottom: 0;
}

.delete-consequences li svg {
  width: 18px;
  height: 18px;
  color: #ef4444;
  flex-shrink: 0;
}

.btn-danger {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 40px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(239, 68, 68, 0.35);
}

/* Animations */
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

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .tab-content {
    padding: 24px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .tab-navigation {
    flex-wrap: wrap;
  }

  .tab-btn {
    min-width: 80px;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 40px 20px 24px;
  }

  .user-name {
    font-size: 1.5rem;
  }

  .avatar-ring {
    width: 100px;
    height: 100px;
  }

  .avatar-inner {
    font-size: 2.5rem;
  }

  .tab-content {
    padding: 20px;
  }

  .delete-section {
    padding: 24px 16px;
  }
}
</style>
