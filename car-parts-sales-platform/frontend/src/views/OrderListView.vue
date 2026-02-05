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
  { value: 'all', label: 'All Orders' },
  { value: 'pending_payment', label: 'Pending Payment' },
  { value: 'pending_shipment', label: 'Pending Shipment' },
  {  value: 'shipped', label: 'Shipped' },
  { value: 'completed', label: 'Completed' },
  { value: 'cancelled', label: 'Cancelled' }
]

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
    ElMessage.error('Failed to load orders')
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
    ElMessage.success('Payment successful!')
    await fetchOrders()
  } catch (error) {
    ElMessage.error(error.message || 'Payment failed')
  } finally {
    processingOrder.value = null
  }
}

async function handleCancelOrder(order) {
  try {
    await ElMessageBox.confirm(
      'Are you sure you want to cancel this order? This action cannot be undone.',
      'Cancel Order',
      {
        confirmButtonText: 'Yes, Cancel',
        cancelButtonText: 'No, Keep',
        type: 'warning'
      }
    )
    processingOrder.value = order.id
    await cancelOrderApi(order.id)
    ElMessage.success('Order cancelled successfully')
    await fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || 'Failed to cancel order')
    }
  } finally {
    processingOrder.value = null
  }
}

async function handleConfirmOrder(order) {
  try {
    await ElMessageBox.confirm(
      'Please confirm that you have received the goods. After confirmation, you cannot apply for after-sales service.',
      'Confirm Receipt',
      {
        confirmButtonText: 'Confirm Receipt',
        cancelButtonText: 'Cancel',
        type: 'info'
      }
    )
    processingOrder.value = order.id
    await confirmOrderApi(order.id)
    ElMessage.success('Order completed successfully')
    await fetchOrders()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || 'Failed to confirm order')
    }
  } finally {
    processingOrder.value = null
  }
}

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') return orders.value
  return orders.value.filter(o => o.status === activeTab.value)
})
</script>

<template>
  <div class="order-list-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1 class="page-title">My Orders</h1>
        <p class="page-subtitle">Track and manage your orders</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Tabs -->
      <div class="tabs-container">
        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            :class="['tab', { active: activeTab === tab.value }]"
            @click="handleTabChange(tab.value)"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <!-- Orders List -->
      <div v-loading="loading" class="orders-content">
        <!-- Empty State -->
        <div v-if="filteredOrders.length === 0" class="empty-state">
          <svg class="empty-icon" viewBox="0 0 24 24" fill="none">
            <path d="M9 5H7C5.8654 5 5 5.8654 5 9C5 12.1346 5.8654 15 9 15C11.1346 15 15 11.1346 15 9C15 5.8654 14.1346 5 11 5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 12V12.01M12 16V16.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <h3>No orders found</h3>
          <p>You don't have any orders yet</p>
          <button class="btn btn-secondary" @click="router.push('/products')">
            <span>Start Shopping</span>
          </button>
        </div>

        <!-- Orders List -->
        <div v-else class="orders-list">
          <div
            v-for="order in filteredOrders"
            :key="order.id"
            class="order-card"
          >
            <div class="order-header">
              <div class="order-info">
                <span class="order-number">Order #{{ order.order_no }}</span>
                <span class="order-date">{{ formatDateTime(order.created_at) }}</span>
              </div>
              <div class="order-status" :class="'status-' + order.status">
                {{ getOrderStatusLabel(order.status).label }}
              </div>
            </div>

            <div class="order-body">
              <div class="order-items-preview">
                <div
                  v-for="item in order.items?.slice(0, 3)"
                  :key="item.id"
                  class="item-preview"
                >
                  <img :src="item.product_image || item.product?.image" :alt="item.product_name" />
                  <div class="item-info">
                    <span class="item-name">{{ item.product_name }}</span>
                    <span class="item-quantity">x{{ item.quantity }}</span>
                  </div>
                </div>
                <div v-if="order.items?.length > 3" class="more-items">
                  +{{ order.items.length - 3 }} more
                </div>
              </div>

              <div class="order-summary">
                <div class="summary-row">
                  <span class="summary-label">Items:</span>
                  <span class="summary-value">{{ order.items?.length || 0 }}</span>
                </div>
                <div class="summary-row">
                  <span class="summary-label">Total:</span>
                  <span class="summary-value">{{ formatCurrency(order.pay_amount) }}</span>
                </div>
              </div>
            </div>

            <div class="order-actions">
              <button class="action-btn" @click="handleViewOrder(order.id)">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0 0 0 0 0z" stroke="currentColor" stroke-width="2"/>
                  <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                View Details
              </button>

              <button
                v-if="order.status === 'pending_payment'"
                class="action-btn action-btn--primary"
                :disabled="processingOrder === order.id"
                @click="handlePayOrder(order)"
              >
                <svg v-if="processingOrder !== order.id" viewBox="0 0 24 24" fill="none">
                  <rect x="2" y="5" width="20" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                  <path d="M2 10H22" stroke="currentColor" stroke-width="2"/>
                </svg>
                <svg v-else class="btn-spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-dashoffset="10"/>
                </svg>
                {{ processingOrder === order.id ? 'Processing...' : 'Pay Now' }}
              </button>

              <button
                v-if="order.status === 'shipped'"
                class="action-btn action-btn--success"
                :disabled="processingOrder === order.id"
                @click="handleConfirmOrder(order)"
              >
                <svg v-if="processingOrder !== order.id" viewBox="0 0 24 24" fill="none">
                  <path d="M9 12L11 14L15 10M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else class="btn-spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-dashoffset="10"/>
                </svg>
                {{ processingOrder === order.id ? 'Processing...' : 'Confirm' }}
              </button>

              <button
                v-if="['pending_payment', 'pending_shipment'].includes(order.status)"
                class="action-btn action-btn--danger"
                :disabled="processingOrder === order.id"
                @click="handleCancelOrder(order)"
              >
                <svg v-if="processingOrder !== order.id" viewBox="0 0 24 24" fill="none">
                  <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else class="btn-spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-dashoffset="10"/>
                </svg>
                {{ processingOrder === order.id ? 'Processing...' : 'Cancel' }}
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
  background: #f5f5f5;
}

.page-header {
  position: relative;
  background: #0a0a0a;
  padding: 80px 40px 60px;
  overflow: hidden;
}

.header-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 50% 100%, rgba(255, 77, 0, 0.2), transparent);
}

.header-content {
  position: relative;
  z-index: 2;
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}

.page-title {
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 48px);
  font-weight: 700;
  text-transform: uppercase;
  color: white;
  margin-bottom: 8px;
}

.page-subtitle {
  font-family: var(--font-body);
  font-size: 14px;
  color: #9ca3af;
}

.main-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Tabs */
.tabs-container {
  background: white;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  margin-bottom: 24px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
}

.tab {
  flex: 1;
  padding: 16px 20px;
  background: none;
  border: none;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease;
}

.tab::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #ff4d00;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.tab:hover {
  color: #0a0a0a;
}

.tab.active {
  color: #ff4d00;
  font-weight: 600;
}

.tab.active::after {
  transform: scaleX(1);
}

/* Orders Content */
.orders-content {
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: white;
  border-radius: 8px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 24px;
}

.empty-state h3 {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: #0a0a0a;
  margin-bottom: 8px;
}

.empty-state p {
  font-family: var(--font-body);
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 32px;
}

.btn {
  padding: 12px 24px;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: transparent;
  color: #ff4d00;
  border: 1px solid #ff4d00;
}

.btn-secondary:hover {
  background: #ff4d00;
  color: white;
}

/* Orders List */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  transition: box-shadow 0.3s ease;
}

.order-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-number {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: #0a0a0a;
}

.order-date {
  font-family: var(--font-body);
  font-size: 12px;
  color: #9ca3af;
}

.order-status {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 4px;
  text-transform: uppercase;
}

.status-pending_payment {
  background: #fef3c7;
  color: #92400e;
}

.status-pending_shipment {
  background: #dbeafe;
  color: #059669;
}

.status-shipped {
  background: #e0e7ff;
  color: #1d4ed8;
}

.status-completed {
  background: #d1fae5;
  color: #065f46;
}

.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.order-body {
  padding: 16px 0;
}

.order-items-preview {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.item-preview {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-preview img {
  width: 50px;
  height: 50px;
  border-radius: 4px;
  object-fit: cover;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-name {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-quantity {
  font-family: var(--font-body);
  font-size: 11px;
  color: #9ca3af;
}

.more-items {
  font-family: var(--font-body);
  font-size: 12px;
  color: #9ca3af;
}

.order-summary {
  display: flex;
  justify-content: space-between;
  gap: 32px;
}

.summary-row {
  display: flex;
  gap: 8px;
}

.summary-label {
  font-family: var(--font-body);
  font-size: 13px;
  color: #6b7280;
}

.summary-value {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: #0a0a0a;
}

.order-actions {
  display: flex;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #374151;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  border-color: #ff4d00;
  color: #ff4d00;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn--primary {
  background: #ff4d00;
  color: white;
  border-color: #ff4d00;
}

.action-btn--primary:hover {
  background: #e64600;
}

.action-btn--success {
  border-color: #059669;
  color: #059669;
}

.action-btn--success:hover {
  background: #059669;
  color: white;
}

.action-btn--danger {
  border-color: #ef4444;
  color: #ef4444;
}

.action-btn--danger:hover {
  background: #ef4444;
  color: white;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-spinner {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .order-items-preview {
    flex-wrap: wrap;
  }

  .order-summary {
    flex-direction: column;
    gap: 8px;
  }

  .order-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    flex: 1;
    min-width: 120px;
  }
}
</style>
