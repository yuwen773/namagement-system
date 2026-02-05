<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getOrderDetailApi, payOrderApi } from '@/api'
import { formatCurrency, formatDateTime } from '@/utils'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()
const route = useRoute()

// State
const loading = ref(true)
const paying = ref(false)
const order = ref(null)
const paymentStatus = ref(null) // 'pending', 'processing', 'success', 'failed'
const selectedPaymentMethod = ref('alipay')
const countdown = ref(15 * 60) // 15 minutes in seconds
const countdownTimer = ref(null)

// Payment methods
const paymentMethods = [
  {
    id: 'alipay',
    name: 'Alipay',
    icon: 'M7 11h2v2H7v-2zm4 0h2v2h-2v-2zm4 0h2v2h-2v-2zM5 5h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2zm0 2v10h14V7H5z',
    recommended: true
  },
  {
    id: 'wechat',
    name: 'WeChat Pay',
    icon: 'M8 12h8M8 8h8M8 16h5M5 4h14a2 2 0 012 2v12a2 2 0 01-2 2H5a2 2 0 01-2-2V6a2 2 0 012-2z',
    recommended: false
  },
  {
    id: 'bank',
    name: 'Bank Card',
    icon: 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z',
    recommended: false
  }
]

// Computed
const orderId = computed(() => route.params.id)
const orderAmount = computed(() => route.query.amount || order.value?.pay_amount || 0)
const countdownDisplay = computed(() => {
  const minutes = Math.floor(countdown.value / 60)
  const seconds = countdown.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

// Lifecycle
onMounted(async () => {
  await fetchOrderDetail()
  startCountdown()
})

async function fetchOrderDetail() {
  try {
    order.value = await getOrderDetailApi(orderId.value)
  } catch (error) {
    ElMessage.error('Failed to load order details')
    console.error(error)
  } finally {
    loading.value = false
  }
}

function startCountdown() {
  countdownTimer.value = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer.value)
      handlePaymentTimeout()
    }
  }, 1000)
}

function handlePaymentTimeout() {
  ElMessage.warning('Payment time has expired')
  router.push({ name: 'orders' })
}

async function handlePay() {
  paying.value = true
  paymentStatus.value = 'processing'

  try {
    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, 2000))

    await payOrderApi(orderId.value)

    // Simulate success
    paymentStatus.value = 'success'
    clearInterval(countdownTimer.value)

    // Auto redirect to order detail after 3 seconds
    setTimeout(() => {
      router.push({ name: 'order-detail', params: { id: orderId.value } })
    }, 3000)
  } catch (error) {
    paymentStatus.value = 'failed'
    ElMessage.error(error.message || 'Payment failed')
  } finally {
    paying.value = false
  }
}

function handleCancelPayment() {
  ElMessageBox.confirm(
    'Are you sure you want to cancel payment? You can pay later from your order list.',
    'Cancel Payment',
    {
      confirmButtonText: 'Yes, Cancel',
      cancelButtonText: 'Continue Payment',
      type: 'warning'
    }
  ).then(() => {
    clearInterval(countdownTimer.value)
    router.push({ name: 'orders' })
  }).catch(() => {
    // User clicked continue, do nothing
  })
}

function goToOrderDetail() {
  clearInterval(countdownTimer.value)
  router.push({ name: 'order-detail', params: { id: orderId.value } })
}

// Get icon SVG path for payment method
function getPaymentIconPath(method) {
  return method.icon
}
</script>

<template>
  <div class="payment-view">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading payment details...</p>
    </div>

    <!-- Payment Success Modal -->
    <div v-else-if="paymentStatus === 'success'" class="success-modal">
      <div class="success-content">
        <div class="success-icon">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h2 class="success-title">Payment Successful!</h2>
        <p class="success-message">Your order has been paid successfully.</p>
        <p class="success-redirect">Redirecting to order details...</p>
        <button class="btn-primary" @click="goToOrderDetail">
          View Order Now
        </button>
      </div>
    </div>

    <!-- Payment Failed Modal -->
    <div v-else-if="paymentStatus === 'failed'" class="failed-modal">
      <div class="failed-content">
        <div class="failed-icon">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h2 class="failed-title">Payment Failed</h2>
        <p class="failed-message">An error occurred during payment. Please try again.</p>
        <div class="failed-actions">
          <button class="btn-secondary" @click="paymentStatus = 'pending'">
            Try Again
          </button>
          <button class="btn-primary" @click="goToOrderDetail">
            View Order
          </button>
        </div>
      </div>
    </div>

    <!-- Main Payment Content -->
    <template v-else>
      <!-- Page Header -->
      <div class="page-header">
        <button class="back-btn" @click="router.back()">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div class="header-content">
          <h1 class="page-title">Secure Payment</h1>
          <p class="page-subtitle">Complete your purchase safely</p>
        </div>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Order Summary Card -->
        <div class="order-summary-card">
          <div class="card-header">
            <svg class="header-icon" viewBox="0 0 24 24" fill="none">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>Order Summary</h2>
          </div>

          <div class="order-info">
            <div class="info-row">
              <span>Order Number</span>
              <span class="order-number">{{ order?.order_no || 'Loading...' }}</span>
            </div>
            <div class="info-row">
              <span>Payment Amount</span>
              <span class="amount">{{ formatCurrency(orderAmount) }}</span>
            </div>
            <div class="info-row">
              <span>Items Count</span>
              <span>{{ order?.items?.length || 0 }} items</span>
            </div>
          </div>

          <!-- Order Items Preview -->
          <div class="items-preview">
            <div v-for="item in order?.items?.slice(0, 3)" :key="item.id" class="preview-item">
              <img :src="item.product_image || item.product?.image" :alt="item.product_name" />
            </div>
            <div v-if="order?.items?.length > 3" class="more-items">
              +{{ order.items.length - 3 }}
            </div>
          </div>
        </div>

        <!-- Payment Methods Card -->
        <div class="payment-methods-card">
          <div class="card-header">
            <svg class="header-icon" viewBox="0 0 24 24" fill="none">
              <path d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h2>Payment Method</h2>
          </div>

          <div class="payment-options">
            <label
              v-for="method in paymentMethods"
              :key="method.id"
              :class="['payment-option', { selected: selectedPaymentMethod === method.id }]"
            >
              <input type="radio" v-model="selectedPaymentMethod" :value="method.id" class="sr-only" />
              <div class="option-content">
                <div class="option-icon">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path :d="getPaymentIconPath(method)" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="option-info">
                  <span class="option-name">{{ method.name }}</span>
                </div>
                <div v-if="method.recommended" class="recommended-badge">RECOMMENDED</div>
                <div class="option-check">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
            </label>
          </div>
        </div>

        <!-- Security Notice Card -->
        <div class="security-card">
          <svg class="security-icon" viewBox="0 0 24 24" fill="none">
            <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="security-content">
            <h3>Secure Payment</h3>
            <p>Your payment information is protected with industry-standard encryption</p>
          </div>
        </div>
      </div>

      <!-- Bottom Payment Bar -->
      <div class="payment-bar">
        <div class="bar-content">
          <div class="timer-section">
            <svg class="timer-icon" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 6v6l4 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="timer-info">
              <span class="timer-label">Payment expires in</span>
              <span :class="['timer-value', { warning: countdown < 300 }]">{{ countdownDisplay }}</span>
            </div>
          </div>

          <div class="action-section">
            <button class="cancel-btn" @click="handleCancelPayment" :disabled="paying">
              Cancel
            </button>
            <button class="pay-btn" @click="handlePay" :disabled="paying">
              <span v-if="!paying">Pay {{ formatCurrency(orderAmount) }}</span>
              <span v-else class="btn-loading">
                <svg class="spinner-sm" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-dashoffset="10">
                    <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
                  </circle>
                </svg>
                Processing...
              </span>
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.payment-view {
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

/* Success Modal */
.success-modal {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.95);
  z-index: 100;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.success-content {
  text-align: center;
  padding: 60px 40px;
  background: var(--color-card);
  border-radius: 20px;
  border: 1px solid var(--color-border);
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  color: var(--color-success);
  animation: checkmark 0.5s ease;
}

@keyframes checkmark {
  0% { transform: scale(0) rotate(-45deg); opacity: 0; }
  50% { transform: scale(1.2) rotate(0deg); }
  100% { transform: scale(1) rotate(0deg); opacity: 1; }
}

.success-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: var(--color-success);
  margin-bottom: 12px;
  text-transform: uppercase;
}

.success-message {
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--color-text);
  margin-bottom: 8px;
}

.success-redirect {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text-muted);
  margin-bottom: 32px;
}

/* Failed Modal */
.failed-modal {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.95);
  z-index: 100;
}

.failed-content {
  text-align: center;
  padding: 60px 40px;
  background: var(--color-card);
  border-radius: 20px;
  border: 1px solid var(--color-border);
  max-width: 400px;
}

.failed-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  color: var(--color-danger);
}

.failed-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: var(--color-danger);
  margin-bottom: 12px;
  text-transform: uppercase;
}

.failed-message {
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--color-text);
  margin-bottom: 32px;
  line-height: 1.6;
}

.failed-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-primary, .btn-secondary {
  padding: 14px 32px;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  color: white;
  background: var(--color-accent);
}

.btn-primary:hover {
  background: var(--color-accent-hover);
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
  font-size: 26px;
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
}

/* Main Content */
.main-content {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Cards */
.order-summary-card,
.payment-methods-card {
  background: var(--color-card);
  border-radius: 16px;
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border-bottom: 1px solid var(--color-border);
}

.header-icon {
  width: 24px;
  height: 24px;
  color: var(--color-accent);
}

.card-header h2 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text);
  margin: 0;
}

/* Order Summary */
.order-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-body);
  font-size: 14px;
}

.info-row span:first-child {
  color: var(--color-text-muted);
}

.order-number {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: var(--color-text);
  letter-spacing: 0.05em;
}

.amount {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--color-accent);
}

.items-preview {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 20px 20px;
}

.preview-item {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.more-items {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
}

/* Payment Methods */
.payment-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px 20px 20px;
}

.payment-option {
  display: block;
  cursor: pointer;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 2px solid var(--color-border);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.payment-option:hover .option-content {
  border-color: var(--color-accent);
  background: rgba(249, 115, 22, 0.05);
}

.payment-option.selected .option-content {
  border-color: var(--color-accent);
  background: rgba(249, 115, 22, 0.1);
}

.option-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  border-radius: 10px;
}

.option-icon svg {
  width: 24px;
  height: 24px;
  color: var(--color-text);
}

.option-info {
  flex: 1;
}

.option-name {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
}

.recommended-badge {
  padding: 4px 10px;
  font-family: var(--font-body);
  font-size: 10px;
  font-weight: 700;
  color: var(--color-accent);
  background: rgba(249, 115, 22, 0.15);
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.option-check {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-accent);
  border-radius: 50%;
  opacity: 0;
  transform: scale(0);
  transition: all 0.2s ease;
}

.payment-option.selected .option-check {
  opacity: 1;
  transform: scale(1);
}

.option-check svg {
  width: 14px;
  height: 14px;
  color: white;
}

/* Security Card */
.security-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
}

.security-icon {
  width: 40px;
  height: 40px;
  color: var(--color-success);
  flex-shrink: 0;
}

.security-content h3 {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-success);
  margin: 0 0 4px 0;
}

.security-content p {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

/* Payment Bar */
.payment-bar {
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

.bar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 600px;
  margin: 0 auto;
  gap: 20px;
}

.timer-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.timer-icon {
  width: 24px;
  height: 24px;
  color: var(--color-accent);
}

.timer-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.timer-label {
  font-family: var(--font-body);
  font-size: 11px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.timer-value {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}

.timer-value.warning {
  color: var(--color-danger);
  animation: pulse 1s ease infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.action-section {
  display: flex;
  gap: 12px;
}

.cancel-btn {
  padding: 14px 24px;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover:not(:disabled) {
  border-color: var(--color-text);
  color: var(--color-text);
}

.cancel-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pay-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: white;
  background: var(--color-accent);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 180px;
}

.pay-btn:hover:not(:disabled) {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.3);
}

.pay-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-loading {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner-sm {
  width: 18px;
  height: 18px;
  animation: spin 0.8s linear infinite;
}

/* Utility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .bar-content {
    flex-direction: column;
    align-items: stretch;
  }

  .timer-section {
    justify-content: center;
  }

  .action-section {
    flex-direction: column;
  }

  .cancel-btn,
  .pay-btn {
    width: 100%;
  }

  .success-content,
  .failed-content {
    margin: 20px;
    padding: 40px 24px;
  }
}
</style>
