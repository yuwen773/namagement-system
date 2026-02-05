<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getOrderListApi, payOrderApi, cancelOrderApi, confirmOrderApi } from '@/api'
import { getOrderStatusLabel, formatCurrency, formatDateTime } from '@/utils'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()
const loading = ref(false)
const orders = ref([])
const activeTab = ref('all')
const processingOrder = ref(null)

const tabs = [
  { value: 'all', label: '全部订单', icon: 'M4 6h16M4 10h16M4 14h16M4 18h16' },
  { value: 'pending_payment', label: '待付款', icon: 'M12 2v6m0 0v6m0-6h6m-6 0H6', color: '#f59e0b' },
  { value: 'pending_shipment', label: '待发货', icon: 'M20 7h-9m9 0v9m0-9H9m9 9a9 9 0 11-18 0 9 9 0 0118 0z', color: '#3b82f6' },
  { value: 'shipped', label: '已发货', icon: 'M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4', color: '#8b5cf6' },
  { value: 'completed', label: '已完成', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z', color: '#10b981' },
  { value: 'cancelled', label: '已取消', icon: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z', color: '#ef4444' }
]

const orderStats = computed(() => {
  const stats = {
    all: orders.value.length,
    pending_payment: 0,
    pending_shipment: 0,
    shipped: 0,
    completed: 0,
    cancelled: 0
  }
  orders.value.forEach(o => {
    if (stats[o.status] !== undefined) stats[o.status]++
  })
  return stats
})

onMounted(async () => {
  await fetchOrders()
})

async function fetchOrders() {
  loading.value = true
  try {
    const params = {}
    if (activeTab.value !== 'all') {
      params.status = activeTab.value
    }
    const data = await getOrderListApi(params)
    orders.value = data.results || []
  } catch (error) {
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

async function handleTabChange(tab) {
  activeTab.value = tab
  await fetchOrders()
}

function handleViewOrder(id) {
  router.push({ name: 'order-detail', params: { id } })
}

async function handlePayOrder(order) {
  processingOrder.value = order.id
  try {
    await payOrderApi(order.id)
    ElMessage.success('支付成功！')
    await fetchOrders()
  } catch (error) {
    ElMessage.error(error.message || '支付失败')
  } finally {
    processingOrder.value = null
  }
}

async function handleCancelOrder(order) {
  try {
    await ElMessageBox.confirm(
      '确定要取消此订单吗？此操作无法撤销。',
      '取消订单',
      {
        confirmButtonText: '确定取消',
        cancelButtonText: '保留订单',
        type: 'warning'
      }
    )
    processingOrder.value = order.id
    await cancelOrderApi(order.id)
    ElMessage.success('订单已取消')
    await fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '取消失败')
    }
  } finally {
    processingOrder.value = null
  }
}

async function handleConfirmOrder(order) {
  try {
    await ElMessageBox.confirm(
      '请确认您已收到货物。确认后无法申请售后服务。',
      '确认收货',
      {
        confirmButtonText: '确认收货',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    processingOrder.value = order.id
    await confirmOrderApi(order.id)
    ElMessage.success('订单已完成')
    await fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '确认失败')
    }
  } finally {
    processingOrder.value = null
  }
}

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') return orders.value
  return orders.value.filter(o => o.status === activeTab.value)
})

function getStatusType(status) {
  const types = {
    pending_payment: 'warning',
    pending_shipment: 'info',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}
</script>

<template>
  <div class="order-list-view">
    <!-- Hero Header -->
    <div class="hero-header">
      <div class="hero-mesh"></div>
      <div class="hero-grid"></div>
      <div class="hero-content">
        <div class="hero-badge">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>我的订单</span>
        </div>
        <h1 class="hero-title">订单管理</h1>
        <p class="hero-subtitle">查看和管理您的所有订单</p>

        <!-- Stats Cards -->
        <div class="stats-grid">
          <div
            v-for="tab in tabs"
            :key="tab.value"
            class="stat-card"
            :class="{ active: activeTab === tab.value }"
            @click="handleTabChange(tab.value)"
          >
            <div class="stat-icon" :style="{ color: tab.color || '#f97316' }">
              <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
                <path :d="tab.icon" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-count">{{ orderStats[tab.value] || 0 }}</span>
              <span class="stat-label">{{ tab.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Decorative Elements -->
      <div class="hero-circle hero-circle-1"></div>
      <div class="hero-circle hero-circle-2"></div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Orders List -->
      <div v-loading="loading" class="orders-container">
        <!-- Empty State -->
        <div v-if="filteredOrders.length === 0" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" width="80" height="80">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9 2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3>暂无订单</h3>
          <p>您还没有任何订单</p>
          <button class="btn btn-primary" @click="router.push('/products')">
            <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
              <path d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            去购物
          </button>
        </div>

        <!-- Order Cards -->
        <div v-else class="orders-list">
          <div
            v-for="order in filteredOrders"
            :key="order.id"
            class="order-card"
          >
            <div class="order-header">
              <div class="order-number">
                <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9 2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ order.order_no }}
              </div>
              <div class="order-meta">
                <span class="order-date">{{ formatDateTime(order.created_at) }}</span>
              </div>
              <el-tag :type="getStatusType(order.status)" size="small" effect="dark">
                {{ getOrderStatusLabel(order.status).label }}
              </el-tag>
            </div>

            <div class="order-body">
              <div class="order-items">
                <!-- 订单列表不返回商品详情，显示提示 -->
                <div class="items-placeholder">
                  <span class="items-count">{{ order.items_count }} 件商品</span>
                  <span class="items-hint">点击查看详情查看商品清单</span>
                </div>
              </div>

              <div class="order-summary">
                <div class="summary-row">
                  <span class="summary-label">商品数量</span>
                  <span class="summary-value">{{ order.items_count || 0 }} 件</span>
                </div>
                <div class="summary-row summary-total">
                  <span class="summary-label">订单总额</span>
                  <span class="summary-value">{{ formatCurrency(order.pay_amount) }}</span>
                </div>
              </div>
            </div>

            <div class="order-footer">
              <button class="action-btn action-btn--view" @click="handleViewOrder(order.id)">
                <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                  <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                查看详情
              </button>

              <button
                v-if="order.status === 'pending_payment'"
                class="action-btn action-btn--pay"
                :disabled="processingOrder === order.id"
                @click="handlePayOrder(order)"
              >
                <svg v-if="processingOrder !== order.id" viewBox="0 0 24 24" fill="none" width="16" height="16">
                  <rect x="2" y="5" width="20" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                  <path d="M2 10H22" stroke="currentColor" stroke-width="2"/>
                </svg>
                <svg v-else class="btn-spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-dashoffset="10"/>
                </svg>
                {{ processingOrder === order.id ? '处理中...' : '立即支付' }}
              </button>

              <button
                v-if="order.status === 'shipped'"
                class="action-btn action-btn--confirm"
                :disabled="processingOrder === order.id"
                @click="handleConfirmOrder(order)"
              >
                <svg v-if="processingOrder !== order.id" viewBox="0 0 24 24" fill="none" width="16" height="16">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else class="btn-spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-dashoffset="10"/>
                </svg>
                {{ processingOrder === order.id ? '处理中...' : '确认收货' }}
              </button>

              <button
                v-if="['pending_payment', 'pending_shipment'].includes(order.status)"
                class="action-btn action-btn--cancel"
                :disabled="processingOrder === order.id"
                @click="handleCancelOrder(order)"
              >
                <svg v-if="processingOrder !== order.id" viewBox="0 0 24 24" fill="none" width="16" height="16">
                  <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else class="btn-spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-dashoffset="10"/>
                </svg>
                {{ processingOrder === order.id ? '处理中...' : '取消订单' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-list-view {
  --font-display: 'Oswald', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* ==================== Hero Header ==================== */
.hero-header {
  position: relative;
  padding: 80px 40px 60px;
  overflow: hidden;
  background: #0f172a;
}

.hero-mesh {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 40%, rgba(249, 115, 22, 0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 60%, rgba(59, 130, 246, 0.1), transparent);
  animation: meshMove 15s ease-in-out infinite;
}

@keyframes meshMove {
  0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
  50% { opacity: 0.8; transform: scale(1.1) rotate(3deg); }
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black, transparent);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.3);
  border-radius: 100px;
  color: #f97316;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 24px;
}

.hero-badge svg {
  width: 16px;
  height: 16px;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-family: var(--font-body);
  font-size: 16px;
  color: #94a3b8;
  margin-bottom: 40px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  max-width: 900px;
  margin: 0 auto;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s ease;
  animation: slideUp 0.5s ease backwards;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.15s; }
.stat-card:nth-child(3) { animation-delay: 0.2s; }
.stat-card:nth-child(4) { animation-delay: 0.25s; }
.stat-card:nth-child(5) { animation-delay: 0.3s; }
.stat-card:nth-child(6) { animation-delay: 0.35s; }

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.stat-card:hover {
  background: rgba(249, 115, 22, 0.1);
  border-color: rgba(249, 115, 22, 0.3);
  transform: translateY(-4px);
}

.stat-card.active {
  background: rgba(249, 115, 22, 0.15);
  border-color: #f97316;
  box-shadow: 0 8px 30px -10px rgba(249, 115, 22, 0.5);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 12px;
  flex-shrink: 0;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: left;
}

.stat-count {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
}

.stat-label {
  font-family: var(--font-body);
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Decorative Circles */
.hero-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.hero-circle-1 {
  width: 400px;
  height: 400px;
  background: #f97316;
  top: -100px;
  right: -100px;
}

.hero-circle-2 {
  width: 300px;
  height: 300px;
  background: #3b82f6;
  bottom: -50px;
  left: -50px;
}

/* ==================== Main Content ==================== */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.orders-container {
  min-height: 400px;
}

/* ==================== Empty State ==================== */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 24px;
  backdrop-filter: blur(10px);
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  color: #475569;
  opacity: 0.5;
}

.empty-state h3 {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 8px;
}

.empty-state p {
  font-family: var(--font-body);
  font-size: 14px;
  color: #64748b;
  margin-bottom: 32px;
}

/* ==================== Orders List ==================== */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 20px;
  overflow: hidden;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  animation: fadeIn 0.4s ease backwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.order-card:hover {
  border-color: rgba(249, 115, 22, 0.3);
  box-shadow: 0 20px 40px -20px rgba(0, 0, 0, 0.3);
}

/* Order Header */
.order-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: rgba(15, 23, 42, 0.5);
  border-bottom: 1px solid rgba(71, 85, 105, 0.3);
  flex-wrap: wrap;
}

.order-number {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  font-size: 14px;
  font-weight: 600;
  color: #f97316;
}

.order-number svg {
  flex-shrink: 0;
}

.order-meta {
  flex: 1;
}

.order-date {
  font-family: var(--font-body);
  font-size: 13px;
  color: #64748b;
}

/* Order Body */
.order-body {
  padding: 24px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 24px;
}

.order-items {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 12px;
  max-width: 200px;
}

.item-image {
  position: relative;
  width: 50px;
  height: 50px;
  flex-shrink: 0;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.item-quantity {
  position: absolute;
  bottom: -4px;
  right: -4px;
  padding: 2px 6px;
  background: #f97316;
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  border-radius: 4px;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.item-name {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: #f97316;
}

.more-items {
  padding: 12px 16px;
  background: rgba(59, 130, 246, 0.1);
  border: 1px dashed rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  font-family: var(--font-body);
  font-size: 12px;
  color: #3b82f6;
  font-weight: 600;
}

/* Order Summary */
.order-summary {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 12px;
  min-width: 160px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-label {
  font-family: var(--font-body);
  font-size: 13px;
  color: #64748b;
}

.summary-value {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 600;
  color: #e2e8f0;
}

.summary-total {
  padding-top: 8px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.summary-total .summary-value {
  font-size: 20px;
  font-weight: 700;
  color: #f97316;
}

/* Items Placeholder */
.items-placeholder {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px dashed rgba(71, 85, 105, 0.3);
  border-radius: 12px;
}

.items-count {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.items-hint {
  font-family: var(--font-body);
  font-size: 12px;
  color: #64748b;
}

/* Order Footer */
.order-footer {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  background: rgba(15, 23, 42, 0.3);
  border-top: 1px solid rgba(71, 85, 105, 0.3);
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  border-radius: 10px;
  border: 1px solid rgba(71, 85, 105, 0.5);
  background: rgba(30, 41, 59, 0.5);
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(249, 115, 22, 0.1);
  border-color: #f97316;
  color: #f97316;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn--view {
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.3);
}

.action-btn--view:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
  color: #3b82f6;
}

.action-btn--pay {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-color: transparent;
  color: #ffffff;
}

.action-btn--pay:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

.action-btn--confirm {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-color: transparent;
  color: #ffffff;
}

.action-btn--confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.action-btn--cancel {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.action-btn--cancel:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #ef4444;
}

.btn-spinner {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ==================== Buttons ==================== */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

/* ==================== Responsive ==================== */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-header {
    padding: 60px 20px 40px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .order-body {
    grid-template-columns: 1fr;
  }

  .order-summary {
    flex-direction: row;
    justify-content: space-between;
    min-width: unset;
  }

  .order-footer {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 16px;
  }

  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .order-meta {
    width: 100%;
  }

  .order-items {
    flex-direction: column;
    align-items: stretch;
  }

  .order-item {
    max-width: 100%;
  }
}
</style>
