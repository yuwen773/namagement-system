<template>
  <el-dialog
    v-model="visible"
    title="退换货详情"
    width="800px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="return-detail">
      <template v-if="returnDetail">
        <!-- 退换货申请信息 -->
        <div class="section">
          <h3 class="section-title">申请信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="申请ID">{{ returnDetail.id }}</el-descriptions-item>
            <el-descriptions-item label="申请类型">
              <el-tag :type="returnDetail.request_type === 'return' ? 'danger' : 'warning'" size="small">
                {{ returnDetail.request_type_display }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="处理状态">
              <el-tag :type="getReturnStatusType(returnDetail.status)" size="small">
                {{ returnDetail.status_display }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="申请时间">
              {{ formatDate(returnDetail.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="处理时间" :span="2">
              {{ returnDetail.processed_at ? formatDate(returnDetail.processed_at) : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="申请原因" :span="2">
              {{ returnDetail.reason }}
            </el-descriptions-item>
            <el-descriptions-item v-if="returnDetail.admin_note" label="处理意见" :span="2">
              {{ returnDetail.admin_note }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 订单信息 -->
        <div class="section">
          <h3 class="section-title">订单信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="订单号">{{ returnDetail.order_info?.order_no }}</el-descriptions-item>
            <el-descriptions-item label="用户">{{ returnDetail.user_phone }}</el-descriptions-item>
            <el-descriptions-item label="订单状态">
              <el-tag :type="getOrderStatusType(returnDetail.order_info?.status)" size="small">
                {{ returnDetail.order_info?.status_display }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="商品数量">
              {{ returnDetail.order_info?.items_count || 0 }} 件
            </el-descriptions-item>
            <el-descriptions-item label="订单总额">¥{{ returnDetail.order_info?.total_amount }}</el-descriptions-item>
            <el-descriptions-item label="实付金额">
              <span class="pay-amount">¥{{ returnDetail.order_info?.pay_amount }}</span>
            </el-descriptions-item>
            <el-descriptions-item v-if="returnDetail.order_info?.express_company" label="物流公司">
              {{ returnDetail.order_info.express_company }}
            </el-descriptions-item>
            <el-descriptions-item v-if="returnDetail.order_info?.tracking_number" label="物流单号">
              {{ returnDetail.order_info.tracking_number }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 凭证图片 -->
        <div v-if="returnDetail.evidence_images && returnDetail.evidence_images.length > 0" class="section">
          <h3 class="section-title">凭证图片</h3>
          <div class="image-list">
            <el-image
              v-for="(image, index) in returnDetail.evidence_images"
              :key="index"
              :src="image"
              :preview-src-list="returnDetail.evidence_images"
              fit="cover"
              style="width: 120px; height: 120px; border-radius: 8px"
              :initial-index="index"
            />
          </div>
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
import { getReturnDetailApi } from '@/api/modules/order'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  returnId: {
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
const returnDetail = ref(null)

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

// 获取退换货状态标签类型
const getReturnStatusType = (status) => {
  const typeMap = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    completed: 'info'
  }
  return typeMap[status] || 'info'
}

// 获取订单状态标签类型
const getOrderStatusType = (status) => {
  const typeMap = {
    pending_payment: 'warning',
    pending_shipment: 'info',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取退换货详情
const fetchReturnDetail = async () => {
  if (!props.returnId) return

  loading.value = true
  try {
    const data = await getReturnDetailApi(props.returnId)
    returnDetail.value = data
  } catch (error) {
    ElMessage.error('获取退换货详情失败')
    returnDetail.value = null
  } finally {
    loading.value = false
  }
}

// 关闭对话框
const handleClose = () => {
  visible.value = false
  returnDetail.value = null
}

// 监听对话框打开
watch(() => props.modelValue, (newVal) => {
  if (newVal && props.returnId) {
    fetchReturnDetail()
  }
})

// 监听 returnId 变化
watch(() => props.returnId, () => {
  if (props.modelValue && props.returnId) {
    fetchReturnDetail()
  }
})
</script>

<style scoped>
.return-detail {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 8px;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  padding-bottom: 8px;
  border-bottom: 2px solid #f97316;
}

.pay-amount {
  color: #f97316;
  font-weight: 600;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
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
.return-detail::-webkit-scrollbar {
  width: 6px;
}

.return-detail::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.return-detail::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.return-detail::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
