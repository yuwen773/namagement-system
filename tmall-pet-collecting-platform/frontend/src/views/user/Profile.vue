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
    <div class="page-header">
      <h1 class="main-title">
        <User class="title-icon" />
        个人中心
      </h1>
      <p class="subtitle">管理您的账户信息和安全设置</p>
    </div>

    <!-- 标签页导航 -->
    <div class="tabs-navigation">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'profile' }"
        @click="activeTab = 'profile'"
      >
        <User class="tab-icon" />
        个人信息
      </button>
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'security' }"
        @click="activeTab = 'security'"
      >
        <Lock class="tab-icon" />
        账户安全
      </button>
    </div>

    <!-- 个人信息表单 -->
    <div v-if="activeTab === 'profile'" class="form-section">
      <div class="section-card">
        <div class="card-header">
          <h2 class="card-title">基本信息</h2>
          <span class="card-badge">用户ID: {{ userStore.userInfo?.id || '---' }}</span>
        </div>

        <div class="card-body">
          <!-- 头像区域 -->
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <img
                :src="userStore.userInfo?.avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + (userStore.userInfo?.username || 'default')"
                alt="用户头像"
                class="avatar-image"
              />
              <div class="avatar-badge">
                <Camera class="camera-icon" />
              </div>
            </div>
            <div class="avatar-info">
              <h3>{{ profileForm.username || '用户' }}</h3>
              <p>普通用户</p>
            </div>
          </div>

          <el-form :model="profileForm" label-position="top" class="profile-form">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="用户名">
                  <el-input
                    v-model="profileForm.username"
                    placeholder="请输入用户名"
                    class="form-input"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="邮箱">
                  <el-input
                    v-model="profileForm.email"
                    placeholder="请输入邮箱"
                    class="form-input"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="手机号">
                  <el-input
                    v-model="profileForm.phone"
                    placeholder="请输入手机号"
                    class="form-input"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="部门">
                  <el-input
                    v-model="profileForm.department"
                    placeholder="请输入部门"
                    class="form-input"
                  />
                </el-form-item>
              </el-col>
            </el-row>

            <div class="form-actions">
              <button class="save-btn" @click="saveProfile" :loading="saveLoading">
                <Check class="btn-icon" />
                保存修改
              </button>
            </div>
          </el-form>
        </div>
      </div>

      <!-- 账户统计 -->
      <div class="stats-card">
        <div class="card-header">
          <h2 class="card-title">账户统计</h2>
        </div>
        <div class="card-body">
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-icon">📦</div>
              <div class="stat-info">
                <span class="stat-value">0</span>
                <span class="stat-label">收藏商品</span>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">👁️</div>
              <div class="stat-info">
                <span class="stat-value">0</span>
                <span class="stat-label">浏览记录</span>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">📅</div>
              <div class="stat-info">
                <span class="stat-value">{{ userStore.userInfo?.created_at?.substring(0, 10) || '2025-01-01' }}</span>
                <span class="stat-label">注册时间</span>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon">🔐</div>
              <div class="stat-info">
                <span class="stat-value">已绑定</span>
                <span class="stat-label">安全状态</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 账户安全表单 -->
    <div v-if="activeTab === 'security'" class="form-section">
      <div class="section-card">
        <div class="card-header">
          <h2 class="card-title">修改密码</h2>
          <span class="card-badge warning">定期修改密码更安全</span>
        </div>

        <div class="card-body">
          <el-form :model="passwordForm" label-position="top" class="password-form">
            <el-form-item label="当前密码">
              <el-input
                v-model="passwordForm.oldPassword"
                type="password"
                placeholder="请输入当前密码"
                class="form-input"
                show-password
              />
            </el-form-item>

            <el-form-item label="新密码">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="请输入新密码（至少6位）"
                class="form-input"
                show-password
              />
            </el-form-item>

            <el-form-item label="确认新密码">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                class="form-input"
                show-password
              />
            </el-form-item>

            <div class="form-actions">
              <button class="save-btn primary" @click="changePassword" :loading="saveLoading">
                <Lock class="btn-icon" />
                修改密码
              </button>
              <button class="reset-form-btn" @click="resetPasswordForm">
                <Close class="btn-icon" />
                重置
              </button>
            </div>
          </el-form>
        </div>
      </div>

      <!-- 安全建议 -->
      <div class="tips-card">
        <div class="card-header">
          <h2 class="card-title">安全建议</h2>
        </div>
        <div class="card-body">
          <ul class="tips-list">
            <li>
              <span class="tip-icon">✓</span>
              使用8位以上的复杂密码
            </li>
            <li>
              <span class="tip-icon">✓</span>
              包含字母、数字和特殊字符
            </li>
            <li>
              <span class="tip-icon">✓</span>
              定期更换密码，建议每3个月一次
            </li>
            <li>
              <span class="tip-icon">✓</span>
              不要在多个平台使用相同密码
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

.profile-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
}

/* 页面标题 */
.page-header {
  padding: 24px 28px;
  background: linear-gradient(135deg, rgba(123, 44, 191, 0.15) 0%, rgba(255, 107, 53, 0.1) 100%);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: 20px;
}

.main-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Orbitron', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px 0;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: #FF6B35;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

/* 标签页导航 */
.tabs-navigation {
  display: flex;
  gap: 12px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
}

.tab-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
}

.tab-btn.active {
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  color: #000;
}

.tab-icon {
  width: 18px;
  height: 18px;
}

/* 表单区域 */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(0, 0, 0, 0.2);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

.card-badge {
  padding: 4px 12px;
  background: rgba(123, 44, 191, 0.2);
  border: 1px solid rgba(123, 44, 191, 0.3);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: #7B2CBF;
}

.card-badge.warning {
  background: rgba(255, 215, 0, 0.15);
  border-color: rgba(255, 215, 0, 0.3);
  color: #FFD700;
}

.card-body {
  padding: 24px;
}

/* 头像区域 */
.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  margin-bottom: 24px;
}

.avatar-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 107, 53, 0.3);
}

.avatar-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  border-radius: 50%;
  cursor: pointer;
}

.camera-icon {
  width: 14px;
  height: 14px;
  color: #000;
}

.avatar-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 4px 0;
}

.avatar-info p {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  margin: 0;
}

/* 表单样式 */
.profile-form,
.password-form {
  margin-top: 16px;
}

.form-input {
  width: 100%;
}

.form-input :deep(.el-input__wrapper) {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  box-shadow: none;
}

.form-input :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 107, 53, 0.3);
}

.form-input :deep(.el-input__wrapper.is-focus) {
  border-color: #FF6B35;
  box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.1) !important;
}

.form-input :deep(.el-input__inner) {
  color: #fff;
  height: 48px;
}

.form-input :deep(.el-form-item__label) {
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  margin-bottom: 8px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.save-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 32px;
  background: linear-gradient(135deg, #FF6B35, #FFD700);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
}

.save-btn.primary {
  background: linear-gradient(135deg, #7B2CBF, #9D4EDD);
  color: #fff;
}

.reset-form-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 32px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
}

.reset-form-btn:hover {
  border-color: rgba(255, 255, 255, 0.3);
  color: #fff;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* 账户统计 */
.stats-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
}

.stat-icon {
  font-size: 24px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #FF6B35;
}

.stat-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
}

/* 安全建议 */
.tips-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tips-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.tip-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(6, 255, 165, 0.2);
  border-radius: 50%;
  font-size: 12px;
  color: #06FFA5;
}

/* 响应式 */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .avatar-section {
    flex-direction: column;
    text-align: center;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
