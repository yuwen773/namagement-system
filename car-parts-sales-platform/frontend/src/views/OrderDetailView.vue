<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getOrderDetailApi, payOrderApi, cancelOrderApi, confirmOrderApi, returnOrderApi } from '@/api'
import { getOrderStatusLabel, formatCurrency, formatDateTime } from '@/utils'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()
const route = useRoute()

// State
const loading = ref(true)
const order = ref(null)
const processing = ref(false)
const returnDialogVisible = ref(false)
const returnForm = ref({
  reason: '',
  description: '',
  images: []
})

// Computed
const orderId = computed(() => route.params.id)

// Order status timeline
const statusTimeline = computed(() => {
  if (!order.value) return []
  const timeline = [
    { key: 'created', label: '订单已创建', completed: true },
    { key: 'pending_payment', label: '待付款', completed: ['pending_payment', 'pending_shipment', 'shipped', 'completed'].includes(order.value.status) },
    { key: 'pending_shipment', label: '待发货', completed: ['pending_shipment', 'shipped', 'completed'].includes(order.value.status) },
    { key: 'shipped', label: '已发货', completed: ['shipped', 'completed'].includes(order.value.status) },
    { key: 'completed', label: '已完成', completed: order.value.status === 'completed' }
  ]
  if (order.value.status === 'cancelled') {
    return timeline.filter(t => t.completed || t.key === 'created')
  }
  return timeline
})

// Can actions
const canPay = computed(() => order.value?.status === 'pending_payment')
const canCancel = computed(() => ['pending_payment', 'pending_shipment'].includes(order.value?.status))
const canConfirm = computed(() => order.value?.status === 'shipped')
const canReturn = computed(() => order.value?.status === 'completed')

// Fetch data
onMounted(async () => {
  await fetchOrderDetail()
})

async function fetchOrderDetail() {
  loading.value = true
  try {
    order.value = await getOrderDetailApi(orderId.value)
  } catch (error) {
    ElMessage.error('获取订单详情失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// Actions
async function handlePay() {
  processing.value = true
  try {
    await payOrderApi(orderId.value)
    ElMessage.success('支付成功！')
    await fetchOrderDetail()
  } catch (error) {
    ElMessage.error(error.message || '支付失败')
  } finally {
    processing.value = false
  }
}

async function handleCancel() {
  try {
    await ElMessageBox.confirm(
      '确定要取消此订单吗？',
      '取消订单',
      {
        confirmButtonText: '确定取消',
        cancelButtonText: '保留',
        type: 'warning'
      }
    )
    processing.value = true
    await cancelOrderApi(orderId.value)
    ElMessage.success('订单已取消')
    await fetchOrderDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '取消订单失败')
    }
  } finally {
    processing.value = false
  }
}

async function handleConfirm() {
  try {
    await ElMessageBox.confirm(
      '请确认您已收到货物。',
      '确认收货',
      {
        confirmButtonText: '确认收货',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    processing.value = true
    await confirmOrderApi(orderId.value)
    ElMessage.success('订单已完成')
    await fetchOrderDetail()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '确认收货失败')
    }
  } finally {
    processing.value = false
  }
}

function openReturnDialog() {
  returnDialogVisible.value = true
}

async function handleSubmitReturn() {
  if (!returnForm.value.reason) {
    ElMessage.warning('请选择退货原因')
    return
  }
  processing.value = true
  try {
    await returnOrderApi(orderId.value, returnForm.value)
    ElMessage.success('退货申请提交成功')
    returnDialogVisible.value = false
    returnForm.value = { reason: '', description: '', images: [] }
  } catch (error) {
    ElMessage.error(error.message || '退货申请提交失败')
  } finally {
    processing.value = false
  }
}

function handleBack() {
  router.push({ name: 'orders' })
}

function goToProduct(productId) {
  router.push({ name: 'product-detail', params: { id: productId } })
}
</script>

<template>
  <div class="order-detail-view">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载订单详情中...</p>
    </div>

    <template v-else-if="order">
      <!-- Page Header -->
      <div class="page-header">
        <button class="back-btn" @click="handleBack">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="header-content">
          <h1 class="page-title">订单详情</h1>
          <p class="page-subtitle">订单号：{{ order.order_no }}</p>
        </div>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Status Timeline -->
        <section class="status-section">
          <div class="section-header">
            <svg class="section-icon" viewBox="0 0 24 24" fill="none">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>订单进度</h2>
            <div class="status-badge" :class="'status-' + order.status">
              {{ getOrderStatusLabel(order.status).label }}
            </div>
          </div>
          <div class="timeline">
            <div
              v-for="(step, index) in statusTimeline"
              :key="step.key"
              :class="['timeline-step', { active: step.completed, current: index === statusTimeline.filter(s => s.completed).length - 1 && step.completed }]"
            >
              <div class="timeline-dot">
                <svg v-if="step.completed" viewBox="0 0 24 24" fill="none">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <div v-else class="dot-inner"></div>
              </div>
              <div class="timeline-label">{{ step.label }}</div>
            </div>
          </div>
        </section>

        <!-- Shipping Info -->
        <section v-if="order.shipping_address" class="info-section">
          <div class="section-header">
            <svg class="section-icon" viewBox="0 0 24 24" fill="none">
              <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>收货地址</h2>
          </div>
          <div class="address-card">
            <p class="address-line">
              <span class="label">收货人：</span>
              <span>{{ order.shipping_address.receiver_name }} {{ order.shipping_address.receiver_phone }}</span>
            </p>
            <p class="address-line">
              <span class="label">地址：</span>
              <span>{{ order.shipping_address.province }} {{ order.shipping_address.city }} {{ order.shipping_address.district }} {{ order.shipping_address.detail_address }}</span>
            </p>
          </div>
        </section>

        <!-- Logistics Info (if shipped) -->
        <section v-if="order.express_company" class="info-section">
          <div class="section-header">
            <svg class="section-icon" viewBox="0 0 24 24" fill="none">
              <path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v1a1 1 0 001 1h1m8-1v8a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>物流信息</h2>
          </div>
          <div class="logistics-card">
            <div class="logistics-row">
              <span class="label">快递公司：</span>
              <span>{{ order.express_company }}</span>
            </div>
            <div class="logistics-row">
              <span class="label">物流单号：</span>
              <span class="tracking-number">{{ order.tracking_number }}</span>
            </div>
          </div>
        </section>

        <!-- Order Items -->
        <section class="items-section">
          <div class="section-header">
            <svg class="section-icon" viewBox="0 0 24 24" fill="none">
              <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>商品清单 ({{ order.items?.length || 0 }})</h2>
          </div>
          <div class="items-list">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="item-card"
            >
              <img
                :src="item.product_image || item.product?.image"
                :alt="item.product_name"
                class="item-image"
                @click="goToProduct(item.product_id)"
              />
              <div class="item-info">
                <h3 class="item-name" @click="goToProduct(item.product_id)">{{ item.product_name }}</h3>
                <p v-if="item.product_spec" class="item-spec">{{ item.product_spec }}</p>
                <div class="item-meta">
                  <span class="item-price">{{ formatCurrency(item.product_price) }}</span>
                  <span class="item-qty">× {{ item.quantity }}</span>
                </div>
              </div>
              <div class="item-subtotal">
                {{ formatCurrency(item.product_price * item.quantity) }}
              </div>
            </div>
          </div>
        </section>

        <!-- Price Summary -->
        <section class="price-section">
          <div class="section-header">
            <svg class="section-icon" viewBox="0 0 24 24" fill="none">
              <path d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>费用明细</h2>
          </div>
          <div class="price-details">
            <div class="price-row">
              <span>商品金额</span>
              <span>{{ formatCurrency(order.total_amount) }}</span>
            </div>
            <div class="price-row">
              <span>运费</span>
              <span>免运费</span>
            </div>
            <div v-if="order.discount_amount > 0" class="price-row discount">
              <span>优惠金额</span>
              <span>-{{ formatCurrency(order.discount_amount) }}</span>
            </div>
            <div class="price-divider"></div>
            <div class="price-row total">
              <span>实付金额</span>
              <span class="total-amount">{{ formatCurrency(order.pay_amount) }}</span>
            </div>
          </div>
        </section>

        <!-- Order Info -->
        <section class="info-section">
          <div class="section-header">
            <svg class="section-icon" viewBox="0 0 24 24" fill="none">
              <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>订单信息</h2>
          </div>
          <div class="order-info-grid">
            <div class="info-item">
              <span class="label">订单编号：</span>
              <span class="value order-no">{{ order.order_no }}</span>
            </div>
            <div class="info-item">
              <span class="label">下单时间：</span>
              <span class="value">{{ formatDateTime(order.created_at) }}</span>
            </div>
            <div v-if="order.paid_at" class="info-item">
              <span class="label">支付时间：</span>
              <span class="value">{{ formatDateTime(order.paid_at) }}</span>
            </div>
            <div v-if="order.shipped_at" class="info-item">
              <span class="label">发货时间：</span>
              <span class="value">{{ formatDateTime(order.shipped_at) }}</span>
            </div>
            <div v-if="order.completed_at" class="info-item">
              <span class="label">完成时间：</span>
              <span class="value">{{ formatDateTime(order.completed_at) }}</span>
            </div>
          </div>
        </section>

        <!-- Action Bar -->
        <div class="action-bar">
          <div class="action-buttons">
            <button
              v-if="canPay"
              class="btn btn-primary"
              :disabled="processing"
              @click="handlePay"
            >
              <svg v-if="!processing" viewBox="0 0 24 24" fill="none">
                <rect x="2" y="5" width="20" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M2 10H22" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>{{ processing ? '处理中...' : '立即支付' }}</span>
            </button>

            <button
              v-if="canCancel"
              class="btn btn-danger"
              :disabled="processing"
              @click="handleCancel"
            >
              <svg v-if="!processing" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>{{ processing ? '处理中...' : '取消订单' }}</span>
            </button>

            <button
              v-if="canConfirm"
              class="btn btn-success"
              :disabled="processing"
              @click="handleConfirm"
            >
              <svg v-if="!processing" viewBox="0 0 24 24" fill="none">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>{{ processing ? '处理中...' : '确认收货' }}</span>
            </button>

            <button
              v-if="canReturn"
              class="btn btn-secondary"
              @click="openReturnDialog"
            >
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M16 15v-1a4 4 0 00-4-4H8m0 0l3 3m-3-3l3-3m9 14V5a2 2 0 00-2-2H6a2 2 0 00-2 2v16l4-2 4 2 4-2 4 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>申请退货</span>
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Return Dialog -->
    <el-dialog
      v-model="returnDialogVisible"
      title="申请退货/换货"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form label-width="80px">
        <el-form-item label="退货原因" required>
          <el-select v-model="returnForm.reason" placeholder="请选择退货原因">
            <el-option label="商品质量问题" value="quality" />
            <el-option label="商品损坏" value="damaged" />
            <el-option label="发错货" value="wrong_item" />
            <el-option label="与描述不符" value="not_as_described" />
            <el-option label="其他原因" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="详细描述">
          <el-input
            v-model="returnForm.description"
            type="textarea"
            :rows="4"
            placeholder="请详细描述您遇到的问题"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="returnDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="processing" @click="handleSubmitReturn">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.order-detail-view {
  --font-display: 'Oswald', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --color-bg: #0f172a;
  --color-card: #1e293b;
  --color-border: #334155;
  --color-accent: #f97316;
  --color-accent-hover: #ea580c;
  --color-success: #10b981;
  --color-danger: #ef4444;
  --color-text: #f1f5f9;
  --color-text-muted: #94a3b8;
  min-height: 100vh;
  background: var(--color-bg);
  padding-bottom: 100px;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 20px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text-muted);
}

/* Page Header */
.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px 20px;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
}

.back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.back-btn svg {
  width: 20px;
  height: 20px;
}

.header-content {
  flex: 1;
}

.page-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text);
  margin: 0;
}

.page-subtitle {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 4px 0 0 0;
  font-family: 'Courier New', monospace;
}

/* Main Content */
.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Sections */
section {
  background: var(--color-card);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border-bottom: 1px solid var(--color-border);
}

.section-icon {
  width: 20px;
  height: 20px;
  color: var(--color-accent);
  flex-shrink: 0;
}

.section-header h2 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text);
  margin: 0;
  flex: 1;
}

.status-badge {
  padding: 4px 12px;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 700;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-pending_payment { background: rgba(234, 179, 8, 0.15); color: #eab308; }
.status-pending_shipment { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.status-shipped { background: rgba(168, 85, 247, 0.15); color: #a855f7; }
.status-completed { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.status-cancelled { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

/* Status Timeline */
.status-section {
  padding: 20px;
}

.timeline {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.timeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
  position: relative;
}

.timeline-step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 12px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: var(--color-border);
  z-index: 0;
}

.timeline-step.completed:not(:last-child)::after {
  background: var(--color-accent);
}

.timeline-dot {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: 50%;
  z-index: 1;
  transition: all 0.3s ease;
}

.timeline-step.completed .timeline-dot {
  border-color: var(--color-accent);
  background: var(--color-accent);
}

.timeline-step.current .timeline-dot {
  box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.2);
}

.timeline-dot svg {
  width: 14px;
  height: 14px;
  color: white;
}

.dot-inner {
  width: 8px;
  height: 8px;
  background: var(--color-border);
  border-radius: 50%;
}

.timeline-label {
  font-family: var(--font-body);
  font-size: 11px;
  color: var(--color-text-muted);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.timeline-step.completed .timeline-label {
  color: var(--color-text);
  font-weight: 600;
}

/* Address & Info Cards */
.address-card,
.logistics-card {
  padding: 20px;
}

.address-line,
.logistics-row {
  display: flex;
  gap: 12px;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text-muted);
}

.address-line:not(:last-child),
.logistics-row:not(:last-child) {
  margin-bottom: 12px;
}

.label {
  flex-shrink: 0;
  width: 80px;
  color: var(--color-text-muted);
}

.tracking-number {
  font-family: 'Courier New', monospace;
  color: var(--color-accent);
}

/* Items List */
.items-list {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.item-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  align-items: center;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.item-image:hover {
  transform: scale(1.05);
}

.item-info {
  flex: 1;
}

.item-name {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 4px 0;
  cursor: pointer;
  transition: color 0.2s ease;
}

.item-name:hover {
  color: var(--color-accent);
}

.item-spec {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0 0 8px 0;
}

.item-meta {
  display: flex;
  gap: 12px;
  align-items: center;
}

.item-price {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.item-qty {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-text-muted);
}

.item-subtotal {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-accent);
}

/* Price Details */
.price-section {
  padding: 20px;
}

.price-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text-muted);
}

.price-row.discount {
  color: var(--color-accent);
}

.price-divider {
  height: 1px;
  background: var(--color-border);
  margin: 8px 0;
}

.price-row.total {
  margin-top: 8px;
}

.price-row.total span:first-child {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text);
}

.total-amount {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--color-accent) !important;
}

/* Order Info Grid */
.order-info-grid {
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  width: auto;
}

.info-item .value {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text);
}

.order-no {
  font-family: 'Courier New', monospace;
  font-weight: 600;
}

/* Action Bar */
.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--color-border);
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  max-width: 800px;
  margin: 0 auto;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn svg {
  width: 18px;
  height: 18px;
}

.btn-primary {
  color: white;
  background: var(--color-accent);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.3);
}

.btn-success {
  color: white;
  background: var(--color-success);
}

.btn-success:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}

.btn-danger {
  color: white;
  background: var(--color-danger);
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
}

.btn-secondary {
  color: var(--color-text);
  background: transparent;
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* Responsive */
@media (max-width: 768px) {
  .timeline {
    overflow-x: auto;
    padding-bottom: 10px;
  }

  .timeline-step {
    min-width: 70px;
  }

  .item-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .item-image {
    width: 100%;
    height: 200px;
  }

  .order-info-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-wrap: wrap;
  }

  .btn {
    flex: 1;
    min-width: 140px;
  }
}
</style>
