<template>
  <div class="profile-page">
    <!-- 装饰元素 -->
    <div class="corner-decoration top-left"></div>
    <div class="corner-decoration top-right"></div>
    <div class="corner-decoration bottom-left"></div>
    <div class="corner-decoration bottom-right"></div>

    <!-- 主体布局 -->
    <div class="profile-layout">
      <!-- 左侧：用户信息卡片 -->
      <aside class="profile-sidebar">
        <div class="name-card">
          <!-- 印章头像 -->
          <div class="seal-avatar">
            <div class="seal-inner">
              <span class="seal-char">{{ avatarChar }}</span>
            </div>
            <div class="seal-ribbon"></div>
          </div>

          <!-- 用户名 -->
          <h2 class="username">{{ profileForm.username || '用户' }}</h2>

          <!-- 角色标签 -->
          <div class="role-badge" :class="profileForm.role">
            <span class="badge-icon">{{ profileForm.role === 'admin' ? '令' : '民' }}</span>
            <span class="badge-text">{{ profileForm.role === 'admin' ? '管理员' : '普通用户' }}</span>
          </div>

          <!-- 分隔线 -->
          <div class="divider">
            <div class="divider-line"></div>
            <div class="divider-ornament">✦</div>
            <div class="divider-line"></div>
          </div>

          <!-- 用户信息列表 -->
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">邮箱</span>
              <span class="info-value">{{ profileForm.email || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">手机</span>
              <span class="info-value">{{ profileForm.phone || '未设置' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">注册于</span>
              <span class="info-value">{{ formatDate(profileForm.date_joined) }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">上次登录</span>
              <span class="info-value">{{ profileForm.last_login_time ? formatDate(profileForm.last_login_time) : '首次登录' }}</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- 右侧：编辑区域 -->
      <main class="profile-main">
        <!-- 书签式Tab导航 -->
        <div class="tab-bookmark">
          <button
            class="bookmark-item"
            :class="{ active: activeTab === 'profile' }"
            @click="activeTab = 'profile'"
          >
            <span class="bookmark-icon">✎</span>
            <span class="bookmark-text">基本信息</span>
          </button>
          <button
            class="bookmark-item"
            :class="{ active: activeTab === 'password' }"
            @click="activeTab = 'password'"
          >
            <span class="bookmark-icon">🔑</span>
            <span class="bookmark-text">修改密码</span>
          </button>
        </div>

        <!-- Tab内容 -->
        <div class="tab-content">
          <!-- 基本信息表单 -->
          <transition name="fade-slide" mode="out-in">
            <div v-if="activeTab === 'profile'" key="profile" class="form-panel">
              <div class="panel-header">
                <h3 class="panel-title">编辑个人信息</h3>
                <p class="panel-desc">修改您的联系信息</p>
              </div>

              <el-form
                ref="profileFormRef"
                :model="profileForm"
                :rules="profileRules"
                label-position="top"
                class="profile-form"
                @submit.prevent="saveProfile"
              >
                <el-form-item label="用户名" prop="username">
                  <el-input v-model="profileForm.username" disabled>
                    <template #prefix>
                      <span class="input-icon">人</span>
                    </template>
                  </el-input>
                </el-form-item>

                <el-form-item label="邮箱地址" prop="email">
                  <el-input v-model="profileForm.email" placeholder="请输入邮箱地址">
                    <template #prefix>
                      <span class="input-icon">✉</span>
                    </template>
                  </el-input>
                </el-form-item>

                <el-form-item label="手机号码" prop="phone">
                  <el-input v-model="profileForm.phone" placeholder="请输入手机号码">
                    <template #prefix>
                      <span class="input-icon">☎</span>
                    </template>
                  </el-input>
                </el-form-item>

                <el-form-item class="form-actions">
                  <el-button
                    type="primary"
                    :loading="saving"
                    class="submit-btn"
                    @click="saveProfile"
                  >
                    <span v-if="!saving" class="btn-text">保存修改</span>
                    <span v-else class="btn-loading">保存中...</span>
                  </el-button>
                </el-form-item>
              </el-form>
            </div>

            <!-- 修改密码表单 -->
            <div v-else key="password" class="form-panel">
              <div class="panel-header">
                <h3 class="panel-title">修改密码</h3>
                <p class="panel-desc">保障账户安全，定期更换密码</p>
              </div>

              <el-form
                ref="passwordFormRef"
                :model="passwordForm"
                :rules="passwordRules"
                label-position="top"
                class="profile-form"
                @submit.prevent="handlePasswordChange"
              >
                <el-form-item label="当前密码" prop="old_password">
                  <el-input
                    v-model="passwordForm.old_password"
                    type="password"
                    placeholder="请输入当前密码"
                    show-password
                  >
                    <template #prefix>
                      <span class="input-icon">🔒</span>
                    </template>
                  </el-input>
                </el-form-item>

                <el-form-item label="新密码" prop="new_password">
                  <el-input
                    v-model="passwordForm.new_password"
                    type="password"
                    placeholder="请输入新密码（至少8位）"
                    show-password
                  >
                    <template #prefix>
                      <span class="input-icon">🔑</span>
                    </template>
                  </el-input>
                </el-form-item>

                <el-form-item label="确认新密码" prop="confirm_password">
                  <el-input
                    v-model="passwordForm.confirm_password"
                    type="password"
                    placeholder="请再次输入新密码"
                    show-password
                  >
                    <template #prefix>
                      <span class="input-icon">✓</span>
                    </template>
                  </el-input>
                </el-form-item>

                <el-form-item class="form-actions">
                  <el-button
                    type="primary"
                    :loading="changingPwd"
                    class="submit-btn danger"
                    @click="handlePasswordChange"
                  >
                    <span v-if="!changingPwd" class="btn-text">修改密码</span>
                    <span v-else class="btn-loading">处理中...</span>
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </transition>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { getCurrentUser, updateProfile, changePassword as changePasswordApi } from '@/api/auth'
import type { UserProfile } from '@/types'

const activeTab = ref('profile')
const saving = ref(false)
const changingPwd = ref(false)

const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

const profileForm = reactive<UserProfile>({
  id: 0,
  username: '',
  role: 'user',
  email: '',
  phone: '',
  is_active: true,
  last_login_time: null,
  date_joined: '',
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

// 计算头像字符
const avatarChar = computed(() => {
  return profileForm.username ? profileForm.username.charAt(0).toUpperCase() : '?'
})

const profileRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' },
  ],
}

const validateConfirmPwd = (_rule: any, value: string, callback: any) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules: FormRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' },
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' },
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPwd, trigger: 'blur' },
  ],
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

const loadProfile = async () => {
  try {
    const res = await getCurrentUser()
    Object.assign(profileForm, res.data)
  } catch (error) {
    ElMessage.error('加载个人信息失败')
  }
}

const saveProfile = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        await updateProfile({
          email: profileForm.email,
          phone: profileForm.phone,
        })
        ElMessage.success('保存成功')
      } catch (error: any) {
        ElMessage.error(error.response?.data?.message || '保存失败')
      } finally {
        saving.value = false
      }
    }
  })
}

const handlePasswordChange = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      changingPwd.value = true
      try {
        await changePasswordApi({
          old_password: passwordForm.old_password,
          new_password: passwordForm.new_password,
        })
        ElMessage.success('密码修改成功，请重新登录')
        passwordForm.old_password = ''
        passwordForm.new_password = ''
        passwordForm.confirm_password = ''
      } catch (error: any) {
        ElMessage.error(error.response?.data?.message || '修改密码失败')
      } finally {
        changingPwd.value = false
      }
    }
  })
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
/* ========== 页面基础布局 ========== */
.profile-page {
  min-height: calc(100vh - 72px);
  padding: 32px;
  position: relative;
  background:
    radial-gradient(ellipse at 20% 20%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(139, 69, 19, 0.03) 0%, transparent 50%),
    linear-gradient(180deg, #F7F4ED 0%, #EDE8DC 100%);
}

/* 角落装饰 */
.corner-decoration {
  position: absolute;
  width: 80px;
  height: 80px;
  pointer-events: none;
}

.corner-decoration::before,
.corner-decoration::after {
  content: '';
  position: absolute;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  opacity: 0.15;
}

.top-left {
  top: 16px;
  left: 16px;
}
.top-left::before {
  width: 40px;
  height: 2px;
  top: 0;
  left: 0;
}
.top-left::after {
  width: 2px;
  height: 40px;
  top: 0;
  left: 0;
}

.top-right {
  top: 16px;
  right: 16px;
}
.top-right::before {
  width: 40px;
  height: 2px;
  top: 0;
  right: 0;
}
.top-right::after {
  width: 2px;
  height: 40px;
  top: 0;
  right: 0;
}

.bottom-left {
  bottom: 16px;
  left: 16px;
}
.bottom-left::before {
  width: 40px;
  height: 2px;
  bottom: 0;
  left: 0;
}
.bottom-left::after {
  width: 2px;
  height: 40px;
  bottom: 0;
  left: 0;
}

.bottom-right {
  bottom: 16px;
  right: 16px;
}
.bottom-right::before {
  width: 40px;
  height: 2px;
  bottom: 0;
  right: 0;
}
.bottom-right::after {
  width: 2px;
  height: 40px;
  bottom: 0;
  right: 0;
}

/* ========== 主布局 ========== */
.profile-layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 32px;
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* ========== 左侧：名片卡片 ========== */
.profile-sidebar {
  position: sticky;
  top: 32px;
  height: fit-content;
}

.name-card {
  background: linear-gradient(145deg, #FFFCF7 0%, #F7F0E3 100%);
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  box-shadow:
    0 4px 24px rgba(139, 69, 19, 0.08),
    0 1px 3px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(212, 175, 55, 0.2);
  position: relative;
  overflow: hidden;
}

.name-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #C23531, #D4AF37, #C23531);
}

/* 印章头像 */
.seal-avatar {
  position: relative;
  display: inline-block;
  margin-bottom: 16px;
}

.seal-inner {
  width: 80px;
  height: 80px;
  background: linear-gradient(145deg, #C23531 0%, #8B0000 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    0 4px 12px rgba(194, 53, 49, 0.4),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
  position: relative;
}

.seal-inner::before {
  content: '';
  position: absolute;
  inset: 4px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
}

.seal-char {
  font-size: 32px;
  font-weight: 700;
  color: #FFFCF7;
  font-family: "STSong", "SimSun", serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.seal-ribbon {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 10px solid #8B0000;
}

/* 用户名 */
.username {
  font-size: 22px;
  font-weight: 600;
  color: #2F3640;
  margin: 12px 0;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 2px;
}

/* 角色标签 */
.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 20px;
}

.role-badge.admin {
  background: linear-gradient(135deg, #C23531 0%, #A52A2A 100%);
  color: #FFFCF7;
  box-shadow: 0 2px 8px rgba(194, 53, 49, 0.3);
}

.role-badge.user {
  background: linear-gradient(135deg, #5D8AA8 0%, #4682B4 100%);
  color: #FFFCF7;
  box-shadow: 0 2px 8px rgba(70, 130, 180, 0.3);
}

.badge-icon {
  font-family: "STSong", "SimSun", serif;
}

/* 分隔线 */
.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 20px 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent);
}

.divider-ornament {
  color: #D4AF37;
  font-size: 10px;
}

/* 信息列表 */
.info-list {
  text-align: left;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px dashed rgba(139, 69, 19, 0.1);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 13px;
  color: #909399;
}

.info-value {
  font-size: 13px;
  color: #2F3640;
  font-weight: 500;
}

/* ========== 右侧：编辑区域 ========== */
.profile-main {
  min-height: 400px;
}

/* 书签式Tab */
.tab-bookmark {
  display: flex;
  gap: 8px;
  margin-bottom: -1px;
  position: relative;
  z-index: 2;
}

.bookmark-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(180deg, #F7F4ED 0%, #EDE8DC 100%);
  border: 1px solid rgba(139, 69, 19, 0.15);
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  font-size: 14px;
  color: #606266;
  transition: all 0.3s ease;
  position: relative;
}

.bookmark-item::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: transparent;
  transition: background 0.3s ease;
}

.bookmark-item:hover {
  color: #2F3640;
  background: linear-gradient(180deg, #FFFCF7 0%, #F7F4ED 100%);
}

.bookmark-item.active {
  background: linear-gradient(180deg, #FFFCF7 0%, #FFFCF7 100%);
  color: #C23531;
  border-color: rgba(194, 53, 49, 0.2);
  box-shadow: 0 -2px 8px rgba(194, 53, 49, 0.05);
}

.bookmark-item.active::after {
  background: #FFFCF7;
}

.bookmark-icon {
  font-size: 14px;
}

.bookmark-text {
  font-weight: 500;
}

/* Tab内容面板 */
.tab-content {
  background: #FFFCF7;
  border-radius: 0 12px 12px 12px;
  box-shadow:
    0 4px 24px rgba(139, 69, 19, 0.08),
    0 1px 3px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(139, 69, 19, 0.1);
  overflow: hidden;
  position: relative;
}

.tab-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #C23531, #D4AF37, #5D8AA8);
}

.form-panel {
  padding: 32px;
}

.panel-header {
  margin-bottom: 28px;
  text-align: center;
}

.panel-title {
  font-size: 20px;
  font-weight: 600;
  color: #2F3640;
  margin: 0 0 8px 0;
  font-family: "STSong", "SimSun", serif;
  letter-spacing: 2px;
}

.panel-desc {
  font-size: 13px;
  color: #909399;
  margin: 0;
}

/* 表单样式 */
.profile-form {
  max-width: 400px;
  margin: 0 auto;
}

.profile-form :deep(.el-form-item__label) {
  font-size: 13px;
  color: #606266;
  padding-bottom: 6px;
}

.profile-form :deep(.el-input__wrapper) {
  background: #FFFCF7;
  border: 1px solid rgba(139, 69, 19, 0.2);
  border-radius: 6px;
  box-shadow: none;
  transition: all 0.3s ease;
}

.profile-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(212, 175, 55, 0.5);
}

.profile-form :deep(.el-input__wrapper.is-focus) {
  border-color: #D4AF37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}

.profile-form :deep(.el-input__inner) {
  color: #2F3640;
}

.profile-form :deep(.el-input__inner::placeholder) {
  color: #C0C4CC;
}

.profile-form :deep(.el-input.is-disabled .el-input__wrapper) {
  background: #F5F5F5;
  border-color: #E4E7ED;
}

.input-icon {
  font-size: 14px;
  opacity: 0.6;
}

/* 提交按钮 */
.form-actions {
  margin-top: 28px;
  text-align: center;
}

.submit-btn {
  min-width: 160px;
  height: 44px;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  border: none;
  border-radius: 22px;
  font-size: 15px;
  font-weight: 600;
  color: #2F3640;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
}

.submit-btn.danger {
  background: linear-gradient(135deg, #C23531 0%, #8B0000 100%);
  color: #FFFCF7;
  box-shadow: 0 4px 12px rgba(194, 53, 49, 0.3);
}

.submit-btn.danger:hover {
  box-shadow: 0 6px 20px rgba(194, 53, 49, 0.4);
}

.btn-text {
  letter-spacing: 2px;
}

.btn-loading {
  letter-spacing: 1px;
}

/* ========== 动画 ========== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }

  .profile-sidebar {
    position: static;
  }

  .profile-page {
    padding: 16px;
  }

  .tab-bookmark {
    flex-direction: column;
  }

  .bookmark-item {
    border-radius: 8px;
    justify-content: center;
  }

  .tab-content {
    border-radius: 12px;
  }
}
</style>
