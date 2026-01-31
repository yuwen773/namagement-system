<template>
  <div class="profile-container">
    <!-- 主要内容区 -->
    <div class="profile-content">
      <div class="profile-card">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <el-icon class="is-loading"><Loading /></el-icon>
          <p>加载中...</p>
        </div>

        <!-- 用户信息展示 -->
        <div v-else class="user-info">
          <!-- 头像区域 -->
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <div class="avatar-placeholder">
                <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="50" cy="35" r="20" fill="currentColor" opacity="0.6"/>
                  <path d="M25 85 C25 65, 40 55, 50 55 C60 55, 75 65, 75 85" fill="currentColor" opacity="0.6"/>
                </svg>
              </div>
              <div class="role-badge" :class="{ 'is-admin': userInfo?.role === 'admin' }">
                {{ userInfo?.role === 'admin' ? '管理员' : '用户' }}
              </div>
            </div>
          </div>

          <!-- 基本信息 -->
          <div class="info-section">
            <div class="section-header">
              <h2 class="section-title">基本信息</h2>
              <div class="header-buttons">
                <el-button type="default" @click="goToChangePassword">
                  修改密码
                </el-button>
                <el-button type="primary" :icon="Edit" @click="showEditDialog = true">
                  编辑资料
                </el-button>
              </div>
            </div>

            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">用户名</span>
                <span class="info-value">{{ userInfo?.username || '-' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">邮箱</span>
                <span class="info-value">{{ userInfo?.email || '-' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">昵称</span>
                <span class="info-value">{{ userInfo?.nickname || '-' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">手机号</span>
                <span class="info-value">{{ userInfo?.phone || '-' }}</span>
              </div>
              <div class="info-item full-width">
                <span class="info-label">个人简介</span>
                <span class="info-value bio-text">{{ userInfo?.bio || '暂无简介' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">注册时间</span>
                <span class="info-value">{{ formatDate(userInfo?.created_at) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">账号状态</span>
                <span class="info-value">
                  <el-tag :type="userInfo?.is_active ? 'success' : 'danger'" size="small">
                    {{ userInfo?.is_active ? '正常' : '已禁用' }}
                  </el-tag>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑资料对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑个人资料"
      width="500px"
      :close-on-click-modal="false"
      class="edit-dialog"
    >
      <el-form
        ref="formRef"
        :model="editForm"
        :rules="editRules"
        label-position="top"
        class="edit-form"
      >
        <el-form-item label="昵称" prop="nickname">
          <el-input
            v-model="editForm.nickname"
            placeholder="请输入昵称"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="editForm.email"
            placeholder="请输入邮箱"
            type="email"
          />
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="editForm.phone"
            placeholder="请输入手机号"
            maxlength="11"
          />
        </el-form-item>

        <el-form-item label="个人简介" prop="bio">
          <el-input
            v-model="editForm.bio"
            type="textarea"
            :rows="4"
            placeholder="介绍一下你自己..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Edit, Loading } from '@element-plus/icons-vue'
import { getCurrentUser, updateProfile } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const saving = ref(false)
const showEditDialog = ref(false)
const formRef = ref(null)
const userInfo = ref(null)

// 编辑表单
const editForm = reactive({
  nickname: '',
  email: '',
  phone: '',
  bio: ''
})

// 表单验证规则
const editRules = {
  nickname: [
    { max: 50, message: '昵称最多 50 个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  bio: [
    { max: 500, message: '个人简介最多 500 个字符', trigger: 'blur' }
  ]
}

// 加载用户信息
const loadUserInfo = async () => {
  loading.value = true
  try {
    const response = await getCurrentUser()
    if (response.code === 200) {
      userInfo.value = response.data
      // 同步更新 store 中的用户信息
      userStore.setUserInfo(response.data)
    }
  } catch (error) {
    ElMessage.error('获取用户信息失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 打开编辑对话框时填充表单
const openEditDialog = () => {
  editForm.nickname = userInfo.value?.nickname || ''
  editForm.email = userInfo.value?.email || ''
  editForm.phone = userInfo.value?.phone || ''
  editForm.bio = userInfo.value?.bio || ''
}

// 保存编辑
const handleSave = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    const response = await updateProfile(editForm)
    if (response.code === 200) {
      // 更新本地用户信息
      userInfo.value = { ...userInfo.value, ...response.data }
      userStore.setUserInfo(userInfo.value)

      ElMessage.success('保存成功')
      showEditDialog.value = false
    }
  } catch (error) {
    ElMessage.error('保存失败：' + error.message)
  } finally {
    saving.value = false
  }
}

// 跳转到修改密码页面
const goToChangePassword = () => {
  router.push({ name: 'change-password' })
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 监听对话框打开
watch(showEditDialog, (newVal) => {
  if (newVal) {
    openEditDialog()
  }
})

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

.profile-container {
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
  background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
  padding-top: 1rem;
}

/* ========== 主要内容区 ========== */
.profile-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 1rem 2rem 2rem;
}

.profile-card {
  background: white;
  border-radius: 24px;
  box-shadow: 0 4px 24px rgba(61, 41, 20, 0.08), 0 0 1px rgba(61, 41, 20, 0.1);
  overflow: hidden;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #8b7355;
  font-size: 1rem;
}

.loading-state .el-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #c2622e;
}

/* ========== 用户信息展示 ========== */
.user-info {
  padding: 2.5rem;
}

/* 头像区域 */
.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #f0ebe3;
}

.avatar-wrapper {
  position: relative;
}

.avatar-placeholder {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.avatar-placeholder svg {
  width: 50px;
  height: 50px;
}

.role-badge {
  position: absolute;
  bottom: 0;
  right: -8px;
  padding: 0.25rem 0.75rem;
  background: #8b7355;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 12px;
  white-space: nowrap;
}

.role-badge.is-admin {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
}

/* 信息区域 */
.info-section {
  margin-top: 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #3d2914;
}

.header-buttons {
  display: flex;
  gap: 0.75rem;
}

.section-header .el-button {
  border-radius: 10px;
  font-weight: 600;
}

.section-header .el-button--default {
  background: white;
  border: 1.5px solid #e5ddd3;
  color: #3d2914;
}

.section-header .el-button--default:hover {
  border-color: #d4773a;
  color: #c2622e;
}

.section-header .el-button--primary {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border: none;
}

.section-header .el-button--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(194, 98, 46, 0.3);
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #8b7355;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.info-value {
  font-size: 1rem;
  color: #3d2914;
  font-weight: 500;
}

.info-value.bio-text {
  line-height: 1.6;
  white-space: pre-wrap;
}

/* ========== 编辑对话框样式 ========== */
.edit-dialog :deep(.el-dialog__header) {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f0ebe3;
}

.edit-dialog :deep(.el-dialog__title) {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #3d2914;
}

.edit-dialog :deep(.el-dialog__body) {
  padding: 2rem;
}

.edit-dialog :deep(.el-dialog__footer) {
  padding: 1rem 2rem;
  border-top: 1px solid #f0ebe3;
}

.edit-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #3d2914;
  font-size: 0.9rem;
}

.edit-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  border: 1.5px solid #e5ddd3;
  box-shadow: none;
  transition: all 0.2s ease;
}

.edit-form :deep(.el-input__wrapper:hover) {
  border-color: #d4773a;
}

.edit-form :deep(.el-input__wrapper.is-focus) {
  border-color: #c2622e;
  box-shadow: 0 0 0 3px rgba(194, 98, 46, 0.1);
}

.edit-form :deep(.el-textarea__inner) {
  border-radius: 10px;
  border: 1.5px solid #e5ddd3;
  resize: none;
}

.edit-form :deep(.el-textarea__inner:hover) {
  border-color: #d4773a;
}

.edit-form :deep(.el-textarea__inner:focus) {
  border-color: #c2622e;
  box-shadow: 0 0 0 3px rgba(194, 98, 46, 0.1);
}

.edit-dialog :deep(.el-dialog__footer .el-button--primary) {
  background: linear-gradient(135deg, #d4773a 0%, #c2622e 100%);
  border: none;
  border-radius: 10px;
  font-weight: 600;
}

.edit-dialog :deep(.el-dialog__footer .el-button--primary:hover) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(194, 98, 46, 0.3);
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .profile-content {
    padding: 0 1rem 1rem;
  }

  .user-info {
    padding: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .section-header .el-button {
    width: 100%;
  }

  .edit-dialog :deep(.el-dialog) {
    width: 90% !important;
    margin: 0 auto;
  }

  .edit-dialog :deep(.el-dialog__body) {
    padding: 1.5rem;
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

.profile-card {
  animation: fadeInUp 0.5s ease-out;
}
</style>
