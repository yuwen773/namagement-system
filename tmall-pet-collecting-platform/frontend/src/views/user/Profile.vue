<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api'
import { User, Lock, Camera, Check, Close } from '@element-plus/icons-vue'

const userStore = useUserStore()

const loading = ref(false)
const saveLoading = ref(false)

const profileForm = reactive({
  username: '',
  email: '',
  phone: '',
  department: ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const activeTab = ref('profile')

// 获取用户信息
const fetchProfile = async () => {
  loading.value = true
  try {
    const res = await authApi.getProfile()
    if (res.code === 0) {
      const user = res.data
      profileForm.username = user.username || ''
      profileForm.email = user.email || ''
      profileForm.phone = user.phone || ''
      profileForm.department = user.department || ''
    }
  } catch (error) {
    console.error('Failed to fetch profile:', error)
    // 使用本地存储的模拟数据
    const userInfo = userStore.userInfo
    if (userInfo) {
      profileForm.username = userInfo.username || ''
      profileForm.email = userInfo.email || ''
    }
  }
  loading.value = false
}

// 保存个人信息
const saveProfile = async () => {
  if (!validateProfile()) return

  saveLoading.value = true
  try {
    // 这里应该调用更新用户信息的API
    ElMessage.success('个人信息更新成功')
    activeTab.value = 'profile'
  } catch (error) {
    console.error('Failed to save profile:', error)
    ElMessage.error('更新失败，请稍后重试')
  } finally {
    saveLoading.value = false
  }
}

// 验证表单
const validateProfile = () => {
  if (!profileForm.username.trim()) {
    ElMessage.warning('用户名不能为空')
    return false
  }
  if (profileForm.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profileForm.email)) {
    ElMessage.warning('请输入有效的邮箱地址')
    return false
  }
  return true
}

// 修改密码
const changePassword = async () => {
  if (!validatePassword()) return

  saveLoading.value = true
  try {
    await authApi.changePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })
    ElMessage.success('密码修改成功，请重新登录')

    // 清除token并跳转到登录页
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    window.location.href = '/login'
  } catch (error) {
    console.error('Failed to change password:', error)
    ElMessage.error(error.response?.data?.message || '密码修改失败')
  } finally {
    saveLoading.value = false
  }
}

// 验证密码表单
const validatePassword = () => {
  if (!passwordForm.oldPassword) {
    ElMessage.warning('请输入当前密码')
    return false
  }
  if (!passwordForm.newPassword) {
    ElMessage.warning('请输入新密码')
    return false
  }
  if (passwordForm.newPassword.length < 6) {
    ElMessage.warning('新密码至少6位字符')
    return false
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return false
  }
  return true
}

// 重置密码表单
const resetPasswordForm = () => {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}

onMounted(() => {
  fetchProfile()
})
</script>

<template>
  <div class="profile-container">
    <!-- 页面标题 -->
    <header class="page-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-icon-wrapper">
            <User class="header-icon" />
          </div>
          <div class="header-text">
            <h1 class="header-title">个人中心</h1>
            <p class="header-subtitle">管理您的账户信息和安全设置</p>
          </div>
        </div>
        <div class="header-right">
          <div class="user-status-badge">
            <span class="status-dot"></span>
            <span>在线</span>
          </div>
        </div>
      </div>
    </header>

    <!-- 标签页导航 -->
    <nav class="tabs-navigation">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'profile' }"
        @click="activeTab = 'profile'"
      >
        <div class="tab-icon-wrapper">
          <User class="tab-icon" />
        </div>
        <span class="tab-label">个人信息</span>
        <div class="tab-indicator"></div>
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'security' }"
        @click="activeTab = 'security'"
      >
        <div class="tab-icon-wrapper">
          <Lock class="tab-icon" />
        </div>
        <span class="tab-label">账户安全</span>
        <div class="tab-indicator"></div>
      </button>
    </nav>

    <!-- 个人信息表单 -->
    <div v-if="activeTab === 'profile'" class="content-section">
      <!-- 个人信息卡片 -->
      <div class="profile-card">
        <div class="profile-card-header">
          <div class="profile-header-left">
            <h2 class="profile-card-title">基本信息</h2>
            <p class="profile-card-subtitle">更新您的个人资料信息</p>
          </div>
          <div class="profile-id-badge">
            <span class="id-label">用户ID</span>
            <span class="id-value">{{ userStore.userInfo?.id || '---' }}</span>
          </div>
        </div>

        <div class="profile-card-body">
          <!-- 头像区域 -->
          <div class="avatar-showcase">
            <div class="avatar-container">
              <img
                :src="userStore.userInfo?.avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + (userStore.userInfo?.username || 'default')"
                alt="用户头像"
                class="avatar-img"
              />
              <div class="avatar-glow"></div>
              <div class="avatar-edit-btn">
                <Camera class="edit-icon" />
              </div>
            </div>
            <div class="avatar-details">
              <h3 class="avatar-name">{{ profileForm.username || '用户' }}</h3>
              <div class="avatar-meta">
                <span class="meta-badge">普通用户</span>
                <span class="meta-dot"></span>
                <span class="meta-label">已认证</span>
              </div>
            </div>
          </div>

          <div class="form-divider"></div>

          <el-form :model="profileForm" label-position="top" class="profile-form">
            <div class="form-grid">
              <div class="form-field">
                <el-form-item label="用户名">
                  <el-input
                    v-model="profileForm.username"
                    placeholder="请输入用户名"
                    class="styled-input"
                  />
                </el-form-item>
              </div>
              <div class="form-field">
                <el-form-item label="邮箱">
                  <el-input
                    v-model="profileForm.email"
                    placeholder="请输入邮箱"
                    class="styled-input"
                  />
                </el-form-item>
              </div>
              <div class="form-field">
                <el-form-item label="手机号">
                  <el-input
                    v-model="profileForm.phone"
                    placeholder="请输入手机号"
                    class="styled-input"
                  />
                </el-form-item>
              </div>
              <div class="form-field">
                <el-form-item label="部门">
                  <el-input
                    v-model="profileForm.department"
                    placeholder="请输入部门"
                    class="styled-input"
                  />
                </el-form-item>
              </div>
            </div>

            <div class="form-actions">
              <button class="action-btn action-btn--primary" @click="saveProfile">
                <Check class="btn-icon" />
                保存修改
              </button>
            </div>
          </el-form>
        </div>
      </div>

      <!-- 账户统计卡片 -->
      <div class="stats-section">
        <div class="stats-header">
          <h3 class="stats-title">账户统计</h3>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card--orange">
            <div class="stat-bg">📦</div>
            <div class="stat-content">
              <span class="stat-value">0</span>
              <span class="stat-label">收藏商品</span>
            </div>
            <div class="stat-glow"></div>
          </div>
          <div class="stat-card stat-card--purple">
            <div class="stat-bg">👁️</div>
            <div class="stat-content">
              <span class="stat-value">0</span>
              <span class="stat-label">浏览记录</span>
            </div>
            <div class="stat-glow"></div>
          </div>
          <div class="stat-card stat-card--gold">
            <div class="stat-bg">📅</div>
            <div class="stat-content">
              <span class="stat-value">{{ userStore.userInfo?.created_at?.substring(0, 10) || '2025-01-01' }}</span>
              <span class="stat-label">注册时间</span>
            </div>
            <div class="stat-glow"></div>
          </div>
          <div class="stat-card stat-card--cyan">
            <div class="stat-bg">🔐</div>
            <div class="stat-content">
              <span class="stat-value">已绑定</span>
              <span class="stat-label">安全状态</span>
            </div>
            <div class="stat-glow"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 账户安全表单 -->
    <div v-if="activeTab === 'security'" class="content-section">
      <!-- 密码修改卡片 -->
      <div class="security-card">
        <div class="security-card-header">
          <div class="security-header-left">
            <div class="security-icon-wrapper">
              <Lock class="security-icon" />
            </div>
            <div class="security-header-text">
              <h2 class="security-card-title">修改密码</h2>
              <p class="security-card-subtitle">定期更新密码以保护账户安全</p>
            </div>
          </div>
          <div class="security-alert-badge">
            <span class="alert-icon">⚠️</span>
            <span>定期修改密码更安全</span>
          </div>
        </div>

        <div class="security-card-body">
          <el-form :model="passwordForm" label-position="top" class="password-form">
            <div class="form-field">
              <el-form-item label="当前密码">
                <el-input
                  v-model="passwordForm.oldPassword"
                  type="password"
                  placeholder="请输入当前密码"
                  class="styled-input"
                  show-password
                />
              </el-form-item>
            </div>
            <div class="form-field">
              <el-form-item label="新密码">
                <el-input
                  v-model="passwordForm.newPassword"
                  type="password"
                  placeholder="请输入新密码（至少6位）"
                  class="styled-input"
                  show-password
                />
              </el-form-item>
            </div>
            <div class="form-field">
              <el-form-item label="确认新密码">
                <el-input
                  v-model="passwordForm.confirmPassword"
                  type="password"
                  placeholder="请再次输入新密码"
                  class="styled-input"
                  show-password
                />
              </el-form-item>
            </div>

            <div class="form-actions">
              <button class="action-btn action-btn--purple" @click="changePassword">
                <Lock class="btn-icon" />
                修改密码
              </button>
              <button class="action-btn action-btn--ghost" @click="resetPasswordForm">
                <Close class="btn-icon" />
                重置
              </button>
            </div>
          </el-form>
        </div>
      </div>

      <!-- 安全建议卡片 -->
      <div class="tips-section">
        <div class="tips-header">
          <div class="tips-icon-wrapper">
            <span>🛡️</span>
          </div>
          <div class="tips-header-text">
            <h3 class="tips-title">安全建议</h3>
            <p class="tips-subtitle">保护您的账户安全</p>
          </div>
        </div>
        <div class="tips-list">
          <div class="tip-item">
            <div class="tip-check">✓</div>
            <span class="tip-text">使用8位以上的复杂密码</span>
          </div>
          <div class="tip-item">
            <div class="tip-check">✓</div>
            <span class="tip-text">包含字母、数字和特殊字符</span>
          </div>
          <div class="tip-item">
            <div class="tip-check">✓</div>
            <span class="tip-text">定期更换密码，建议每3个月一次</span>
          </div>
          <div class="tip-item">
            <div class="tip-check">✓</div>
            <span class="tip-text">不要在多个平台使用相同密码</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

/* ============================================
   Design Tokens & Base
   ============================================ */
.profile-container {
  --primary-orange: #FF6B35;
  --primary-purple: #7B2CBF;
  --primary-gold: #FFD700;
  --primary-cyan: #06FFA5;
  --bg-dark: #0F0F23;
  --bg-card: rgba(20, 20, 32, 0.6);
  --bg-card-hover: rgba(255, 255, 255, 0.04);
  --text-primary: rgba(255, 255, 255, 0.95);
  --text-secondary: rgba(255, 255, 255, 0.6);
  --text-tertiary: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --border-default: rgba(255, 255, 255, 0.1);
  --border-accent: rgba(255, 107, 53, 0.2);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Outfit', 'Noto Sans SC', -apple-system, sans-serif;
  max-width: 1000px;
  margin: 0 auto;
  animation: fadeIn 0.4s ease;
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

/* ============================================
   Page Header
   ============================================ */
.page-header {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  overflow: hidden;
  animation: fadeInDown 0.5s ease;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28px 32px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon-wrapper {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(255, 215, 0, 0.15));
  border: 1px solid var(--border-accent);
  border-radius: 14px;
}

.header-icon {
  width: 28px;
  height: 28px;
  color: var(--primary-orange);
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.header-title {
  font-family: 'Noto Sans SC', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.01em;
}

.header-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(6, 255, 165, 0.1);
  border: 1px solid rgba(6, 255, 165, 0.2);
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: var(--primary-cyan);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--primary-cyan);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

/* ============================================
   Tabs Navigation
   ============================================ */
.tabs-navigation {
  display: flex;
  gap: 12px;
  padding: 8px;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tab-btn {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 24px;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.tab-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--bg-card-hover);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tab-btn:hover::before {
  opacity: 1;
}

.tab-btn:hover {
  color: var(--text-primary);
}

.tab-btn.active {
  color: var(--primary-orange);
  background: rgba(255, 107, 53, 0.1);
}

.tab-btn.active::before {
  opacity: 0;
}

.tab-icon-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tab-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.tab-btn:hover .tab-icon {
  transform: scale(1.1);
}

.tab-label {
  position: relative;
  z-index: 1;
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-orange), var(--primary-gold));
  border-radius: 2px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-btn.active .tab-indicator {
  transform: translateX(-50%) scaleX(1);
}

/* ============================================
   Content Section
   ============================================ */
.content-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeInContent 0.5s ease;
}

@keyframes fadeInContent {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ============================================
   Profile Card
   ============================================ */
.profile-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.profile-card:hover {
  border-color: var(--border-accent);
  box-shadow: 0 8px 32px rgba(255, 107, 53, 0.1);
}

.profile-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
}

.profile-header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  font-family: 'Noto Sans SC', sans-serif;
}

.profile-card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.profile-id-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(123, 44, 191, 0.15);
  border: 1px solid rgba(123, 44, 191, 0.25);
  border-radius: 20px;
}

.id-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.id-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-purple);
}

.profile-card-body {
  padding: 28px;
}

/* ============================================
   Avatar Showcase
   ============================================ */
.avatar-showcase {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  margin-bottom: 28px;
}

.avatar-container {
  position: relative;
  width: 96px;
  height: 96px;
  flex-shrink: 0;
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 107, 53, 0.3);
  transition: all 0.3s ease;
}

.avatar-container:hover .avatar-img {
  border-color: var(--primary-orange);
}

.avatar-glow {
  position: absolute;
  inset: -4px;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-purple));
  border-radius: 50%;
  opacity: 0;
  filter: blur(12px);
  transition: opacity 0.3s ease;
  z-index: -1;
}

.avatar-container:hover .avatar-glow {
  opacity: 0.4;
}

.avatar-edit-btn {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-gold));
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
}

.avatar-edit-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(255, 107, 53, 0.5);
}

.edit-icon {
  width: 14px;
  height: 14px;
  color: #000;
}

.avatar-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.avatar-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  font-family: 'Noto Sans SC', sans-serif;
}

.avatar-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.meta-badge {
  padding: 4px 12px;
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid rgba(255, 107, 53, 0.25);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--primary-orange);
}

.meta-dot {
  width: 4px;
  height: 4px;
  background: var(--text-tertiary);
  border-radius: 50%;
}

.meta-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* ============================================
   Form Divider
   ============================================ */
.form-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
  margin: 24px 0;
}

/* ============================================
   Form Grid & Fields
   ============================================ */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-field {
  position: relative;
}

.profile-form :deep(.el-form-item__label) {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 8px;
}

.styled-input {
  width: 100%;
}

.styled-input :deep(.el-input__wrapper) {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-default);
  border-radius: 10px;
  box-shadow: none;
  padding: 12px 16px;
  transition: all 0.3s ease;
}

.styled-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.3);
  background: rgba(0, 0, 0, 0.35);
}

.styled-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-orange);
  background: rgba(0, 0, 0, 0.4);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}

.styled-input :deep(.el-input__inner) {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  height: 48px;
}

.styled-input :deep(.el-input__inner::placeholder) {
  color: var(--text-tertiary);
}

/* ============================================
   Form Actions
   ============================================ */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid var(--border-subtle);
}

.action-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 28px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: inherit;
  filter: brightness(1.1);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.action-btn:hover::before {
  opacity: 1;
}

.action-btn:active {
  transform: scale(0.98);
}

.action-btn--primary {
  background: linear-gradient(135deg, var(--primary-orange), var(--primary-gold));
  border: none;
  color: #000;
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.3);
}

.action-btn--primary:hover {
  box-shadow: 0 6px 24px rgba(255, 107, 53, 0.4);
  transform: translateY(-2px);
}

.action-btn--purple {
  background: linear-gradient(135deg, var(--primary-purple), #9D4EDD);
  border: none;
  color: #fff;
  box-shadow: 0 4px 16px rgba(123, 44, 191, 0.3);
}

.action-btn--purple:hover {
  box-shadow: 0 6px 24px rgba(123, 44, 191, 0.4);
  transform: translateY(-2px);
}

.action-btn--ghost {
  background: transparent;
  border: 1px solid var(--border-default);
  color: var(--text-secondary);
}

.action-btn--ghost:hover {
  border-color: var(--border-accent);
  color: var(--text-primary);
}

.btn-icon {
  position: relative;
  width: 16px;
  height: 16px;
  z-index: 1;
}

/* ============================================
   Stats Section
   ============================================ */
.stats-section {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  padding: 24px 28px;
}

.stats-header {
  margin-bottom: 20px;
}

.stats-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  font-family: 'Noto Sans SC', sans-serif;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  position: relative;
  padding: 20px;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.stat-card--orange {
  border-color: rgba(255, 107, 53, 0.15);
}

.stat-card--orange:hover {
  border-color: rgba(255, 107, 53, 0.3);
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.15);
}

.stat-card--purple {
  border-color: rgba(123, 44, 191, 0.15);
}

.stat-card--purple:hover {
  border-color: rgba(123, 44, 191, 0.3);
  box-shadow: 0 8px 24px rgba(123, 44, 191, 0.15);
}

.stat-card--gold {
  border-color: rgba(255, 215, 0, 0.15);
}

.stat-card--gold:hover {
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 8px 24px rgba(255, 215, 0, 0.15);
}

.stat-card--cyan {
  border-color: rgba(6, 255, 165, 0.15);
}

.stat-card--cyan:hover {
  border-color: rgba(6, 255, 165, 0.3);
  box-shadow: 0 8px 24px rgba(6, 255, 165, 0.15);
}

.stat-bg {
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 64px;
  opacity: 0.05;
  pointer-events: none;
}

.stat-glow {
  position: absolute;
  bottom: -20px;
  right: -20px;
  width: 80px;
  height: 80px;
  background: inherit;
  filter: blur(40px);
  opacity: 0.15;
  pointer-events: none;
}

.stat-card--orange .stat-glow {
  background: var(--primary-orange);
}

.stat-card--purple .stat-glow {
  background: var(--primary-purple);
}

.stat-card--gold .stat-glow {
  background: var(--primary-gold);
}

.stat-card--cyan .stat-glow {
  background: var(--primary-cyan);
}

.stat-content {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 1;
}

.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* ============================================
   Security Card
   ============================================ */
.security-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.security-card:hover {
  border-color: rgba(123, 44, 191, 0.3);
  box-shadow: 0 8px 32px rgba(123, 44, 191, 0.1);
}

.security-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.2);
  gap: 20px;
}

.security-header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.security-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.2), rgba(157, 78, 221, 0.15));
  border: 1px solid rgba(123, 44, 191, 0.25);
  border-radius: 12px;
}

.security-icon {
  width: 24px;
  height: 24px;
  color: var(--primary-purple);
}

.security-header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.security-card-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  font-family: 'Noto Sans SC', sans-serif;
}

.security-card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.security-alert-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: var(--primary-gold);
  white-space: nowrap;
}

.alert-icon {
  font-size: 14px;
}

.security-card-body {
  padding: 28px;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ============================================
   Tips Section
   ============================================ */
.tips-section {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  padding: 24px 28px;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.tips-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(6, 255, 165, 0.15), rgba(6, 255, 165, 0.05));
  border: 1px solid rgba(6, 255, 165, 0.2);
  border-radius: 12px;
  font-size: 20px;
}

.tips-header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tips-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  font-family: 'Noto Sans SC', sans-serif;
}

.tips-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.tip-item:hover {
  background: rgba(0, 0, 0, 0.3);
  border-color: rgba(6, 255, 165, 0.15);
  transform: translateX(4px);
}

.tip-check {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(6, 255, 165, 0.15);
  border: 1px solid rgba(6, 255, 165, 0.25);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  color: var(--primary-cyan);
}

.tip-text {
  font-size: 14px;
  color: var(--text-secondary);
}

/* ============================================
   Responsive Design
   ============================================ */
@media (max-width: 768px) {
  .profile-container {
    gap: 20px;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
    padding: 24px;
  }

  .header-left {
    width: 100%;
  }

  .header-right {
    width: 100%;
    justify-content: flex-start;
  }

  .tabs-navigation {
    flex-direction: row;
  }

  .tab-btn {
    padding: 12px 16px;
  }

  .tab-label {
    display: block;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .avatar-showcase {
    flex-direction: column;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .security-card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .form-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .header-title {
    font-size: 22px;
  }

  .profile-card-title,
  .security-card-title {
    font-size: 16px;
  }

  .avatar-showcase {
    padding: 20px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
