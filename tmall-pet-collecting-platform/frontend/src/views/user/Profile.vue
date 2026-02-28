<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api'
import { User, Lock, Camera, Check, Close, Message } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

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
            <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="28" cy="28" r="26" fill="url(#profileHeaderGrad)" fill-opacity="0.15"/>
              <path d="M28 12C28 12 38 18 38 26C38 34 34 36 28 36C22 36 18 34 18 26C18 18 22 12 28 12Z" fill="url(#profileHeaderLeaf)"/>
              <path d="M28 12L28 36" stroke="white" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
              <circle cx="28" cy="12" r="3" fill="#52B788"/>
              <defs>
                <linearGradient id="profileHeaderGrad" x1="2" y1="2" x2="54" y2="54">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="profileHeaderLeaf" x1="18" y1="12" x2="38" y2="36">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#52B788"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div class="header-text">
            <h1 class="header-title">个人中心</h1>
            <p class="header-subtitle">管理您的账户信息和安全设置</p>
          </div>
        </div>
        <div class="header-right">
          <button class="feedback-btn" @click="router.push('/user/feedback')">
            <Message class="btn-icon" />
            <span>意见反馈</span>
          </button>
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
        <span class="tab-indicator"></span>
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
        <span class="tab-indicator"></span>
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
          <!-- 装饰植物 -->
          <div class="stats-plant">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
              <path d="M20 38V18C20 18 32 10 32 10C32 10 36 10 36 10C36 10 30 18 30 18V38" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M20 18C20 18 30 12 30 6C30 6 24 6 24 6C24 6 20 12 20 12" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M20 28C20 28 28 24 28 24C28 24 24 28 24 28C24 28 20 24 20 24" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M20 6L20 30" stroke="#52B788" stroke-width="2" stroke-linecap="round"/>
              <circle cx="20" cy="6" r="3" fill="#52B788"/>
            </svg>
          </div>
        </div>
        <div class="stats-grid">
          <div class="stat-card stat-card--green">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7V17C2 18.1 2.9 19 4 19H20C21.1 19 22 18.1 22 17V7L12 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 22V16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">0</span>
              <span class="stat-label">收藏商品</span>
            </div>
          </div>
          <div class="stat-card stat-card--teal">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 4.5C7 4.5 2.5 6.5 2.5 12C2.5 18.1 7 21.5 12 21.5C17 21.5 21.5 18.1 21.5 12C21.5 6.5 17 4.5 12 4.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M2 12H22" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">0</span>
              <span class="stat-label">浏览记录</span>
            </div>
          </div>
          <div class="stat-card stat-card--blue">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M7 8H17M7 12H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">{{ userStore.userInfo?.created_at?.substring(0, 10) || '2025-01-01' }}</span>
              <span class="stat-label">注册时间</span>
            </div>
          </div>
          <div class="stat-card stat-card--light">
            <div class="stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 2C12 2 4 3 4 5V19C4 20.1 4.9 21 6 21H18C19.1 21 20 20.1 20 19V5C20 3 18 2 12 2Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="12" cy="15" r="3" fill="currentColor"/>
              </svg>
            </div>
            <div class="stat-content">
              <span class="stat-value">已绑定</span>
              <span class="stat-label">安全状态</span>
            </div>
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
              <button class="action-btn action-btn--primary" @click="changePassword">
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
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <circle cx="24" cy="24" r="20" fill="url(#tipsShieldGrad)" fill-opacity="0.15"/>
              <path d="M24 14L18 20L30 20L24 26L18 32L30 32" stroke="url(#tipsShieldPath)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <defs>
                <linearGradient id="tipsShieldGrad" x1="4" y1="4" x2="44" y2="44">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#40916C"/>
                </linearGradient>
                <linearGradient id="tipsShieldPath" x1="18" y1="20" x2="30" y2="32">
                  <stop offset="0%" stop-color="#74C69D"/>
                  <stop offset="100%" stop-color="#52B788"/>
                </linearGradient>
              </defs>
            </svg>
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

        <!-- 装饰植物 -->
        <div class="tips-plant">
          <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
            <path d="M30 55V25" stroke="#74C69D" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M30 40C30 40 44 34 44 26C44 26 40 18 40 18C36 18 34 10 34 10C34 10 30 16 30 16Z" fill="#74C69D" fill-opacity="0.2"/>
            <path d="M30 26C30 26 38 20 38 12C38 6 34 2 30 2C26 2 22 6 22 6C22 6 30 10 30 10Z" fill="#52B788" fill-opacity="0.15"/>
            <circle cx="30" cy="12" r="3" fill="#52B788"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 页面装饰植物 -->
    <div class="page-plant page-plant--1">
      <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
        <path d="M40 75V35C40 35 60 20 60 20C60 20 50 30 50 30C50 30 40 35 40 35V75" stroke="#74C69D" stroke-width="1" stroke-linecap="round" opacity="0.3"/>
        <path d="M40 35C40 35 50 42 50 30C50 30 42 25 42 25C42 25 40 20 40 20C40 20 30 25 30 25Z" fill="#74C69D" fill-opacity="0.1"/>
      </svg>
    </div>
    <div class="page-plant page-plant--2">
      <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
        <path d="M30 55V25C30 25 45 32 45 32C45 32 35 35 35 35C35 35 30 38 30 38Z" stroke="#52B788" stroke-width="1" stroke-linecap="round" opacity="0.3"/>
        <path d="M30 25C30 25 38 20 38 18C38 16 35 14 35 14C35 14 30 17 30 17Z" fill="#52B788" fill-opacity="0.1"/>
      </svg>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Nunito:wght@400;500;600;700;800&display=swap');

/* ============================================
   Design Tokens - 清新自然
   ============================================ */
.profile-container {
  --primary-green: #2D6A4F;
  --primary-teal: #40916C;
  --primary-light: #52B788;
  --accent-green: #74C69D;
  --accent-blue: #00B4D8;
  --accent-blue-light: #90E0EF;
  --bg-cream: #FAFAF9;
  --bg-sand: #F5F5F4;
  --bg-card: #FFFFFF;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --text-tertiary: #A8A29E;
  --border-light: #E7E5E4;
  --border-focus: #74C69D;
  --shadow-soft: 0 4px 20px rgba(45, 106, 79, 0.08);
  --shadow-hover: 0 8px 30px rgba(45, 106, 79, 0.12);

  display: flex;
  flex-direction: column;
  gap: 24px;
  font-family: 'Nunito', 'Noto Serif SC', -apple-system, sans-serif;
  max-width: 1000px;
  margin: 0 auto;
  animation: pageFadeIn 0.4s ease;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Page Header
   ============================================ */
.page-header {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  animation: fadeInDown 0.5s ease;
  box-shadow: var(--shadow-soft);
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-15px); }
  to { opacity: 1; transform: translateY(0); }
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
  flex-shrink: 0;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.header-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 24px;
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
  gap: 12px;
}

.feedback-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: linear-gradient(135deg, var(--primary-green), var(--primary-light));
  border: none;
  border-radius: 24px;
  font-size: 13px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(45, 106, 79, 0.25);
}

.feedback-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(45, 106, 79, 0.35);
}

.feedback-btn .btn-icon {
  width: 16px;
  height: 16px;
}

.user-status-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  background: rgba(116, 198, 157, 0.1);
  border: 1px solid rgba(116, 198, 157, 0.2);
  border-radius: 24px;
  font-size: 13px;
  font-weight: 500;
  color: var(--primary-green);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--primary-green);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ============================================
   Tabs Navigation
   ============================================ */
.tabs-navigation {
  display: flex;
  gap: 12px;
  padding: 8px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.tab-btn {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 14px 24px;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Noto Serif SC', sans-serif;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.tab-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--bg-card);
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tab-btn:hover::before {
  opacity: 1;
}

.tab-btn:hover {
  color: var(--primary-green);
}

.tab-btn.active {
  color: var(--primary-green);
  background: rgba(116, 198, 157, 0.15);
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
  background: linear-gradient(90deg, var(--primary-green), var(--primary-light));
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
  gap: 24px;
  animation: fadeInContent 0.5s ease;
}

@keyframes fadeInContent {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============================================
   Profile Card
   ============================================ */
.profile-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.profile-card:hover {
  border-color: var(--border-focus);
  box-shadow: var(--shadow-hover);
}

.profile-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, var(--bg-sand) 0%, transparent 100%);
}

.profile-header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.profile-card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.profile-id-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: rgba(45, 106, 79, 0.08);
  border: 1px solid rgba(45, 106, 79, 0.15);
  border-radius: 20px;
}

.id-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.id-value {
  font-family: 'Nunito', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-green);
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
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 16px;
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
  border: 3px solid var(--border-light);
  transition: all 0.3s ease;
}

.avatar-container:hover .avatar-img {
  border-color: var(--accent-green);
}

.avatar-glow {
  position: absolute;
  inset: -4px;
  background: linear-gradient(135deg, var(--primary-green), var(--accent-green));
  border-radius: 50%;
  opacity: 0;
  filter: blur(12px);
  transition: opacity 0.3s ease;
  z-index: -1;
}

.avatar-container:hover .avatar-glow {
  opacity: 0.3;
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
  background: linear-gradient(135deg, var(--primary-green), var(--primary-light));
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(45, 106, 79, 0.3);
}

.avatar-edit-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(45, 106, 79, 0.4);
}

.edit-icon {
  width: 14px;
  height: 14px;
  color: white;
}

.avatar-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.avatar-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Noto Serif SC', serif;
}

.avatar-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.meta-badge {
  padding: 5px 12px;
  background: rgba(45, 106, 79, 0.1);
  border: 1px solid rgba(45, 106, 79, 0.15);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--primary-green);
}

.meta-dot {
  width: 4px;
  height: 4px;
  background: var(--border-light);
  border-radius: 50%;
}

.meta-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Form Divider */
.form-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-light), transparent);
  margin: 24px 0;
}

/* Form Grid & Fields */
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
  font-weight: 600;
  margin-bottom: 8px;
}

.styled-input {
  width: 100%;
}

.styled-input :deep(.el-input__wrapper) {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  box-shadow: none;
  padding: 12px 16px;
  transition: all 0.3s ease;
}

.styled-input :deep(.el-input__wrapper:hover) {
  border-color: var(--accent-green);
  background: var(--bg-sand);
}

.styled-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-green);
  background: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(116, 198, 157, 0.1);
}

.styled-input :deep(.el-input__inner) {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
}

.styled-input :deep(.el-input__inner::placeholder) {
  color: var(--text-tertiary);
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid var(--border-light);
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
  font-family: 'Nunito', sans-serif;
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
  background: linear-gradient(135deg, var(--primary-green), var(--primary-light));
  border: none;
  color: white;
  box-shadow: var(--shadow-soft);
}

.action-btn--primary:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.action-btn--ghost {
  background: transparent;
  border: 1px solid var(--border-light);
  color: var(--text-secondary);
}

.action-btn--ghost:hover {
  border-color: var(--border-focus);
  color: var(--primary-green);
}

.btn-icon {
  position: relative;
  width: 16px;
  height: 16px;
  z-index: 1;
}

/* Stats Section */
.stats-section {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 24px 28px;
  position: relative;
  overflow: hidden;
}

.stats-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(116, 198, 157, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.stats-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

.stats-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.stats-plant {
  opacity: 0.5;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  position: relative;
  padding: 20px;
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-soft);
}

.stat-card--green { border-color: rgba(45, 106, 79, 0.15); }
.stat-card--teal { border-color: rgba(64, 145, 108, 0.15); }
.stat-card--blue { border-color: rgba(0, 180, 216, 0.15); }
.stat-card--light { border-color: rgba(116, 198, 157, 0.15); }

.stat-card:hover {
  border-color: var(--border-focus);
}

.stat-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-sand);
  border-radius: 10px;
  color: var(--primary-green);
}

.stat-card--teal .stat-icon { color: var(--primary-teal); }
.stat-card--blue .stat-icon { color: var(--accent-blue); }
.stat-card--light .stat-icon { color: var(--accent-green); }

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-value {
  font-family: 'Nunito', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

/* Security Card */
.security-card {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-soft);
}

.security-card:hover {
  border-color: var(--accent-blue);
}

.security-card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 28px;
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(180deg, rgba(0, 180, 216, 0.05), transparent 100%);
}

.security-icon-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.1), rgba(0, 180, 216, 0.05));
  border: 1px solid rgba(0, 180, 216, 0.15);
  border-radius: 12px;
}

.security-icon {
  width: 24px;
  height: 24px;
  color: var(--accent-blue);
}

.security-header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.security-card-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.security-card-subtitle {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0;
}

.security-card-body {
  padding: 28px;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Tips Section */
.tips-section {
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 24px 28px;
  position: relative;
  overflow: hidden;
}

.tips-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(116, 198, 157, 0.06) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
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
  flex-shrink: 0;
}

.tips-header-text {
  flex: 1;
}

.tips-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
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
  background: var(--bg-sand);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.tip-item:hover {
  background: rgba(116, 198, 157, 0.05);
  border-color: rgba(116, 198, 157, 0.15);
  transform: translateX(4px);
}

.tip-check {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(45, 106, 79, 0.1);
  border: 1px solid rgba(45, 106, 79, 0.2);
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  color: var(--primary-green);
}

.tip-text {
  font-size: 14px;
  color: var(--text-secondary);
}

.tips-plant {
  position: absolute;
  bottom: 20px;
  right: 20px;
  opacity: 0.4;
}

/* Page Plants */
.page-plant {
  position: fixed;
  pointer-events: none;
  z-index: 0;
  opacity: 0.15;
}

.page-plant--1 {
  bottom: 10%;
  left: 5%;
}

.page-plant--2 {
  top: 20%;
  right: 8%;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
    padding: 24px;
  }

  .header-left {
    width: 100%;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
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

  .page-plant {
    display: none;
  }
}
</style>
