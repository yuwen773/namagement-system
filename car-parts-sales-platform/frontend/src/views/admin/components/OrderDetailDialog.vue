<template>
  <el-dialog
    v-model="visible"
    title="订单详情"
    width="900px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="order-detail">
      <template v-if="orderDetail">
        <!-- 订单基本信息 -->
        <div class="section">
          <h3 class="section-title">订单信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="订单号">{{ orderDetail.order_no }}</el-descriptions-item>
            <el-descriptions-item label="订单状态">
              <el-tag :type="getStatusType(orderDetail.status)" size="small">
                {{ orderDetail.status_display }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="用户手机号">{{ orderDetail.user_phone }}</el-descriptions-item>
            <el-descriptions-item label="用户昵称">{{ orderDetail.user_nickname || '-' }}</el-descriptions-item>
            <el-descriptions-item label="商品总额">¥{{ orderDetail.total_amount }}</el-descriptions-item>
            <el-descriptions-item label="优惠金额">
              <span v-if="orderDetail.discount_amount && orderDetail.discount_amount !== '0.00'" class="discount">
                -¥{{ orderDetail.discount_amount }}
              </span>
              <span v-else>-</span>
            </el-descriptions-item>
            <el-descriptions-item label="运费">¥{{ orderDetail.shipping_fee || '0.00' }}</el-descriptions-item>
            <el-descriptions-item label="实付金额">
              <span class="pay-amount">¥{{ orderDetail.pay_amount }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="优惠券">
              {{ orderDetail.coupon_name || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ formatDate(orderDetail.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="支付时间">
              {{ orderDetail.paid_at ? formatDate(orderDetail.paid_at) : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="发货时间">
              {{ orderDetail.shipped_at ? formatDate(orderDetail.shipped_at) : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="完成时间">
              {{ orderDetail.completed_at ? formatDate(orderDetail.completed_at) : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="物流公司" :span="1">
              {{ orderDetail.express_company || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="物流单号" :span="1">
              {{ orderDetail.tracking_number || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="订单备注" :span="2" v-if="orderDetail.remark">
              {{ orderDetail.remark }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 收货地址 -->
        <div class="section">
          <h3 class="section-title">收货地址</h3>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="收货人">{{ orderDetail.recipient_name }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ orderDetail.recipient_phone }}</el-descriptions-item>
            <el-descriptions-item label="收货地址">
              {{ orderDetail.full_address }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 商品列表 -->
        <div class="section">
          <h3 class="section-title">商品列表 ({{ orderDetail.items?.length || 0 }})</h3>
          <el-table :data="orderDetail.items" border style="width: 100%">
            <el-table-column prop="id" label="商品ID" width="80" />
            <el-table-column label="商品图片" width="100">
              <template #default="{ row }">
                <el-image
                  v-if="row.product_image"
                  :src="row.product_image"
                  :preview-src-list="[row.product_image]"
                  fit="cover"
                  style="width: 60px; height: 60px; border-radius: 4px"
                />
                <span v-else class="text-placeholder">-</span>
              </template>
            </el-table-column>
            <el-table-column prop="product_name" label="商品名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="product_price" label="单价" width="100" align="right">
              <template #default="{ row }">
                ¥{{ row.product_price }}
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" align="center" />
            <el-table-column label="小计" width="100" align="right">
              <template #default="{ row }">
                <span class="subtotal">¥{{ row.subtotal }}</span>
              </template>
            </el-table-column>
          </el-table>
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
import { getOrderDetailApi } from '@/api/modules/order'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  orderId: {
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
const orderDetail = ref(null)

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

// 获取订单状态标签类型
const getStatusType = (status) => {
  const typeMap = {
    pending_payment: 'warning',
    pending_shipment: 'info',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取订单详情
const fetchOrderDetail = async () => {
  if (!props.orderId) return

  loading.value = true
  try {
    const data = await getOrderDetailApi(props.orderId)
    orderDetail.value = data
  } catch (error) {
    ElMessage.error('获取订单详情失败')
    orderDetail.value = null
  } finally {
    loading.value = false
  }
}

// 关闭对话框
const handleClose = () => {
  visible.value = false
  orderDetail.value = null
}

// 监听对话框打开
watch(() => props.modelValue, (newVal) => {
  if (newVal && props.orderId) {
    fetchOrderDetail()
  }
})

// 监听 orderId 变化
watch(() => props.orderId, () => {
  if (props.modelValue && props.orderId) {
    fetchOrderDetail()
  }
})
</script>

<style scoped>
.order-detail {
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

.discount {
  color: #f56c6c;
  font-weight: 600;
}

.pay-amount {
  color: #f97316;
  font-weight: 600;
  font-size: 16px;
}

.subtotal {
  font-weight: 600;
  color: #303133;
}

.text-placeholder {
  color: #c0c4cc;
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
.order-detail::-webkit-scrollbar {
  width: 6px;
}

.order-detail::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.order-detail::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.order-detail::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
