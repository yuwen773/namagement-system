<template>
  <el-dialog
    v-model="visible"
    title="用户详情"
    width="700px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="user-detail">
      <template v-if="userDetail">
        <!-- 基本信息 -->
        <div class="section">
          <h3 class="section-title">基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="用户ID">{{ userDetail.user.id }}</el-descriptions-item>
            <el-descriptions-item label="手机号">{{ userDetail.user.phone }}</el-descriptions-item>
            <el-descriptions-item label="昵称">{{ userDetail.user.nickname || '-' }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ userDetail.user.email || '-' }}</el-descriptions-item>
            <el-descriptions-item label="积分">
              <span class="points">{{ userDetail.user.points?.toLocaleString() || 0 }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="userDetail.user.status === 'active' ? 'success' : 'danger'" size="small">
                {{ userDetail.user.status === 'active' ? '正常' : '已禁用' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="用户类型">
              <el-tag :type="userDetail.user.is_staff ? 'warning' : 'info'" size="small">
                {{ userDetail.user.is_staff ? '管理员' : '普通用户' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="注册时间">
              {{ formatDate(userDetail.user.created_at) }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 头像 -->
        <div class="section" v-if="userDetail.user.avatar">
          <h3 class="section-title">头像</h3>
          <el-avatar :src="userDetail.user.avatar" :size="100" />
        </div>

        <!-- 收货地址 -->
        <div class="section">
          <div class="section-header">
            <h3 class="section-title">收货地址 ({{ userDetail.address_count }})</h3>
          </div>
          <template v-if="userDetail.addresses && userDetail.addresses.length > 0">
            <div class="address-list">
              <div
                v-for="address in userDetail.addresses"
                :key="address.id"
                class="address-card"
                :class="{ 'is-default': address.is_default }"
              >
                <div class="address-header">
                  <span class="recipient-name">{{ address.recipient_name }}</span>
                  <el-tag v-if="address.is_default" type="success" size="small">默认</el-tag>
                </div>
                <div class="address-info">
                  <p><span class="label">手机号:</span> {{ address.phone }}</p>
                  <p><span class="label">地址:</span> {{ address.province }} {{ address.city }} {{ address.district }} {{ address.address }}</p>
                </div>
                <div class="address-footer">
                  <span class="address-time">{{ formatDate(address.created_at) }}</span>
                </div>
              </div>
            </div>
          </template>
          <el-empty v-else description="暂无收货地址" :image-size="80" />
        </div>
      </template>
      <el-empty v-else-if="!loading" description="加载失败" />
    </div>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { getUserDetailApi } from '@/api/modules/user'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  userId: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'refresh'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const loading = ref(false)
const userDetail = ref(null)

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

// 获取用户详情
const fetchUserDetail = async () => {
  if (!props.userId) return

  loading.value = true
  try {
    const data = await getUserDetailApi(props.userId)
    userDetail.value = data
  } catch (error) {
    ElMessage.error('获取用户详情失败')
    userDetail.value = null
  } finally {
    loading.value = false
  }
}

// 关闭对话框
const handleClose = () => {
  visible.value = false
  userDetail.value = null
}

// 监听对话框打开
watch(() => props.modelValue, (newVal) => {
  if (newVal && props.userId) {
    fetchUserDetail()
  }
})

// 监听 userId 变化
watch(() => props.userId, () => {
  if (props.modelValue && props.userId) {
    fetchUserDetail()
  }
})
</script>

<style scoped>
.user-detail {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  padding-bottom: 8px;
  border-bottom: 2px solid #f97316;
}

.points {
  font-weight: 600;
  color: #f97316;
  font-size: 16px;
}

.address-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.address-card {
  padding: 12px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  background: #fafafa;
  transition: all 0.3s;
}

.address-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.address-card.is-default {
  border-color: #67c23a;
  background: #f0f9ff;
}

.address-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.recipient-name {
  font-weight: 600;
  color: #303133;
}

.address-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  color: #606266;
  font-size: 14px;
}

.address-info p {
  margin: 0;
}

.address-info .label {
  color: #909399;
  margin-right: 8px;
}

.address-footer {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e8e8e8;
}

.address-time {
  font-size: 12px;
  color: #909399;
}

/* Element Plus 样式调整 */
:deep(.el-descriptions__label) {
  width: 100px;
  font-weight: 500;
}

:deep(.el-descriptions__body) {
  background: #fafafa;
}

:deep(.el-empty) {
  padding: 20px 0;
}

/* 滚动条样式 */
.address-list::-webkit-scrollbar {
  width: 6px;
}

.address-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.address-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.address-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
