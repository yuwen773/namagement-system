<template>
  <div class="profile-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>个人信息中心</h1>
      <p>查看您的个人档案、岗位信息及资质证书</p>
    </div>

    <!-- 个人信息卡片 -->
    <el-card class="info-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon :size="20" color="#FF6B35"><User /></el-icon>
          <span>基本信息</span>
        </div>
      </template>
      <div class="info-content" v-loading="loading">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="姓名">
            <span class="info-value">{{ employeeProfile?.name || '-' }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="性别">
            <span class="info-value">{{ formatGender(employeeProfile?.gender) }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="岗位">
            <el-tag :type="getPositionTagType(employeeProfile?.position)" effect="dark">
              {{ formatPosition(employeeProfile?.position) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="在职状态">
            <el-tag :type="getStatusTagType(employeeProfile?.status)" effect="plain">
              {{ formatStatus(employeeProfile?.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="手机号码">
            <span class="info-value">{{ employeeProfile?.phone || '-' }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="身份证号">
            <span class="info-value">{{ maskIdCard(employeeProfile?.id_card) }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="家庭住址" :span="2">
            <span class="info-value">{{ employeeProfile?.address || '-' }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="入职日期">
            <span class="info-value">{{ employeeProfile?.entry_date || '-' }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>

    <!-- 证书信息卡片 -->
    <el-card class="info-card certificate-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon :size="20" color="#F7C52D"><Document /></el-icon>
          <span>资质证书</span>
        </div>
      </template>
      <div class="certificate-content" v-loading="loading">
        <!-- 健康证 -->
        <div class="certificate-item" :class="{ 'warning': isHealthCertExpiringSoon }">
          <div class="cert-icon">
            <el-icon :size="32" :color="isHealthCertExpiringSoon ? '#E6A23C' : '#4CAF50'">
              <CircleCheck />
            </el-icon>
          </div>
          <div class="cert-info">
            <div class="cert-name">健康证</div>
            <div class="cert-no">{{ employeeProfile?.health_certificate_no || '未登记' }}</div>
            <div class="cert-expiry" :class="{ 'expiring-soon': isHealthCertExpiringSoon }">
              <el-icon v-if="isHealthCertExpiringSoon"><Warning /></el-icon>
              有效期至：{{ employeeProfile?.health_certificate_expiry || '未登记' }}
              <el-tag v-if="isHealthCertExpiringSoon" type="warning" size="small" effect="dark" style="margin-left: 8px">
                即将到期
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 厨师等级证（如果有） -->
        <div class="certificate-item" v-if="employeeProfile?.chef_certificate_level">
          <div class="cert-icon">
            <el-icon :size="32" color="#FF6B35">
              <Medal />
            </el-icon>
          </div>
          <div class="cert-info">
            <div class="cert-name">厨师等级证</div>
            <div class="cert-level">{{ employeeProfile.chef_certificate_level }}</div>
          </div>
        </div>

        <!-- 无证书提示 -->
        <el-empty v-if="!employeeProfile?.health_certificate_no && !employeeProfile?.chef_certificate_level"
                  description="暂无资质证书信息" :image-size="100" />
      </div>
    </el-card>

    <!-- 密码修改卡片 -->
    <el-card class="info-card password-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon :size="20" color="#4CAF50"><Lock /></el-icon>
          <span>修改密码</span>
        </div>
      </template>
      <div class="password-content">
        <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
          <el-form-item label="旧密码" prop="old_password">
            <el-input v-model="passwordForm.old_password" type="password" placeholder="请输入当前密码"
                      show-password style="max-width: 400px" />
          </el-form-item>
          <el-form-item label="新密码" prop="new_password">
            <el-input v-model="passwordForm.new_password" type="password" placeholder="请输入新密码（至少4位）"
                      show-password style="max-width: 400px" />
            <div class="password-strength" v-if="passwordForm.new_password">
              <span :class="getPasswordStrengthClass()">密码强度：{{ getPasswordStrength() }}</span>
            </div>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirm_password">
            <el-input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码"
                      show-password style="max-width: 400px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" color="#FF6B35" :loading="passwordLoading" @click="handleChangePassword">
              修改密码
            </el-button>
            <el-button @click="resetPasswordForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <!-- 账号信息卡片 -->
    <el-card class="info-card account-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon :size="20" color="#67C23A"><UserFilled /></el-icon>
          <span>账号信息</span>
        </div>
      </template>
      <div class="account-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="登录账号">
            <span class="info-value">{{ userStore.userInfo?.username || '-' }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="账号角色">
            <el-tag :type="userStore.userInfo?.role === 'ADMIN' ? 'danger' : 'primary'" effect="dark">
              {{ userStore.userInfo?.role === 'ADMIN' ? '管理员' : '普通员工' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="账号状态">
            <el-tag :type="userStore.userInfo?.status === 'ENABLED' ? 'success' : 'info'" effect="plain">
              {{ userStore.userInfo?.status === 'ENABLED' ? '正常' : '已禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" v-if="userStore.userInfo?.created_at">
            <span class="info-value">{{ formatDate(userStore.userInfo.created_at) }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User, Document, Lock, UserFilled, CircleCheck, Medal, Warning
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getEmployeeDetail } from '@/api/employee'
import { changePassword } from '@/api/auth'

const userStore = useUserStore()

// 员工档案数据
const employeeProfile = ref(null)
const loading = ref(false)

// 密码修改表单
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})
const passwordFormRef = ref(null)
const passwordLoading = ref(false)

// 表单验证规则
const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 4, message: '密码长度至少4位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 检查健康证是否即将到期（30天内）
const isHealthCertExpiringSoon = computed(() => {
  if (!employeeProfile.value?.health_certificate_expiry) return false
  const expiryDate = new Date(employeeProfile.value.health_certificate_expiry)
  const today = new Date()
  const daysUntilExpiry = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24))
  return daysUntilExpiry <= 30 && daysUntilExpiry >= 0
})

// 获取员工档案信息
const fetchEmployeeProfile = async () => {
  const employeeId = userStore.userInfo?.employee
  if (!employeeId) {
    ElMessage.warning('未关联员工档案')
    return
  }

  loading.value = true
  try {
    const res = await getEmployeeDetail(employeeId)
    if (res.code === 200) {
      employeeProfile.value = res.data
    } else {
      ElMessage.error(res.message || '获取员工信息失败')
    }
  } catch (error) {
    console.error('获取员工信息错误:', error)
    ElMessage.error('获取员工信息失败')
  } finally {
    loading.value = false
  }
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return

    passwordLoading.value = true
    try {
      const userId = userStore.userInfo?.id
      const res = await changePassword(userId, {
        old_password: passwordForm.value.old_password,
        new_password: passwordForm.value.new_password
      })

      if (res.code === 200) {
        ElMessage.success('密码修改成功，请重新登录')
        resetPasswordForm()
        // 延迟退出登录，让用户看到成功提示
        setTimeout(() => {
          userStore.logout()
          window.location.href = '/login'
        }, 1500)
      } else {
        ElMessage.error(res.message || '密码修改失败')
      }
    } catch (error) {
      console.error('修改密码错误:', error)
      ElMessage.error(error.response?.data?.message || '密码修改失败，请检查旧密码是否正确')
    } finally {
      passwordLoading.value = false
    }
  })
}

// 重置密码表单
const resetPasswordForm = () => {
  passwordForm.value = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  }
  passwordFormRef.value?.clearValidate()
}

// 计算密码强度
const getPasswordStrength = () => {
  const password = passwordForm.value.new_password
  if (password.length < 4) return '弱'
  if (password.length < 6) return '中等'
  if (password.length < 8) return '较强'
  return '强'
}

const getPasswordStrengthClass = () => {
  const strength = getPasswordStrength()
  if (strength === '弱') return 'strength-weak'
  if (strength === '中等') return 'strength-medium'
  if (strength === '较强') return 'strength-strong'
  return 'strength-very-strong'
}

// 格式化性别
const formatGender = (gender) => {
  const map = { 'MALE': '男', 'FEMALE': '女' }
  return map[gender] || '-'
}

// 格式化岗位
const formatPosition = (position) => {
  const map = {
    'CHEF': '厨师',
    'PASTRY': '面点',
    'PREP': '切配',
    'CLEANER': '保洁',
    'SERVER': '服务员',
    'MANAGER': '经理'
  }
  return map[position] || position || '-'
}

// 获取岗位标签颜色
const getPositionTagType = (position) => {
  const map = {
    'CHEF': 'warning',
    'PASTRY': 'danger',
    'PREP': 'primary',
    'CLEANER': 'success',
    'SERVER': 'info',
    'MANAGER': ''
  }
  return map[position] || ''
}

// 格式化状态
const formatStatus = (status) => {
  const map = { 'ACTIVE': '在职', 'INACTIVE': '离职', 'LEAVE_WITHOUT_PAY': '停薪留职' }
  return map[status] || status || '-'
}

// 获取状态标签颜色
const getStatusTagType = (status) => {
  const map = { 'ACTIVE': 'success', 'INACTIVE': 'info', 'LEAVE_WITHOUT_PAY': 'warning' }
  return map[status] || ''
}

// 身份证号脱敏
const maskIdCard = (idCard) => {
  if (!idCard) return '-'
  return idCard.replace(/(\d{6})\d{8}(\d{4})/, '$1********$2')
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchEmployeeProfile()
})
</script>

<style scoped>
.profile-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
  text-align: center;
}

.page-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 600;
}

.page-header p {
  font-size: 14px;
  color: #666;
}

.info-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.info-card:last-child {
  margin-bottom: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.info-content {
  padding: 10px 0;
}

.info-value {
  color: #333;
  font-weight: 500;
}

/* 证书样式 */
.certificate-content {
  padding: 10px 0;
}

.certificate-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 16px;
  transition: all 0.3s;
  border-left: 4px solid #4CAF50;
}

.certificate-item:last-child {
  margin-bottom: 0;
}

.certificate-item:hover {
  background: #f0f1f3;
  transform: translateX(4px);
}

.certificate-item.warning {
  background: #fef8f0;
  border-left-color: #E6A23C;
}

.cert-icon {
  flex-shrink: 0;
}

.cert-info {
  flex: 1;
}

.cert-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.cert-no,
.cert-level {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.cert-expiry {
  font-size: 13px;
  color: #4CAF50;
  display: flex;
  align-items: center;
  gap: 4px;
}

.cert-expiry.expiring-soon {
  color: #E6A23C;
  font-weight: 600;
}

/* 密码表单样式 */
.password-content {
  padding: 10px 0;
}

.password-strength {
  margin-top: 8px;
  font-size: 12px;
}

.strength-weak { color: #F56C6C; }
.strength-medium { color: #E6A23C; }
.strength-strong { color: #4CAF50; }
.strength-very-strong { color: #67C23A; }

/* 账号信息样式 */
.account-content {
  padding: 10px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-view {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 22px;
  }

  .certificate-item {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }

  .cert-expiry {
    justify-content: center;
  }
}
</style>
