<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { createOrderApi } from '@/api'
import { getMyCouponsApi } from '@/api/modules/marketing'
import { formatCurrency } from '@/utils'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)
const couponLoading = ref(false)
const selectedCoupon = ref(null)
const availableCoupons = ref([])

onMounted(async () => {
  await Promise.all([
    cartStore.fetchCart(),
    fetchAvailableCoupons()
  ])
})

// 获取可用优惠券
async function fetchAvailableCoupons() {
  couponLoading.value = true
  try {
    const data = await getMyCouponsApi({ status: 'unused', page_size: 100 })
    availableCoupons.value = data.results || []
  } catch (error) {
    console.error('获取优惠券失败:', error)
  } finally {
    couponLoading.value = false
  }
}

const cartItems = computed(() => cartStore.items)
const totalQuantity = computed(() => cartStore.totalQuantity)
const totalPrice = computed(() => cartStore.totalPrice)
const selectedItems = computed(() => cartItems.filter(item => item.selected))
const selectedPrice = computed(() => cartItems.filter(item => item.selected).reduce((sum, item) => sum + item.price * item.quantity, 0))

// 优惠券折扣金额
const couponDiscount = computed(() => {
  if (!selectedCoupon.value) return 0

  const coupon = selectedCoupon.value.coupon || selectedCoupon.value
  const discountAmount = coupon.discount_amount || 0
  const discountPercent = coupon.discount_percent || 0

  if (discountAmount > 0) {
    // 满减券：检查是否满足门槛
    const minAmount = coupon.min_purchase_amount || 0
    if (selectedPrice.value >= minAmount) {
      return Math.min(discountAmount, selectedPrice.value)
    }
    return 0
  } else if (discountPercent > 0) {
    // 折扣券
    return Math.round(selectedPrice.value * discountPercent / 100)
  }
  return 0
})

// 最终价格
const finalPrice = computed(() => Math.max(0, selectedPrice.value - couponDiscount.value))

async function handleQuantityChange(item, newQuantity) {
  if (newQuantity < 1) return
  await cartStore.updateQuantity(item.id, newQuantity)
}

async function handleRemoveItem(item) {
  try {
    await ElMessageBox.confirm('确定要删除这个商品吗？', '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await cartStore.removeItem(item.id)
    ElMessage.success('商品已删除')
  } catch {
    // 用户取消
  }
}

function toggleSelect(item) {
  cartStore.toggleSelect(item.id)
}

function toggleSelectAll() {
  const allSelected = cartItems.value.length > 0 && cartItems.value.every(item => item.selected)
  cartStore.toggleSelectAll(!allSelected)
}

async function handleCheckout() {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请选择要结算的商品')
    return
  }

  loading.value = true
  try {
    const orderData = {
      address_id: 1, // TODO: 获取默认地址
      coupon_id: selectedCoupon.value?.id
    }
    await createOrderApi(orderData)
    ElMessage.success('订单创建成功')
    router.push('/orders')
  } catch (error) {
    ElMessage.error(error.message || '订单创建失败')
  } finally {
    loading.value = false
  }
}

async function handleClearCart() {
  try {
    await ElMessageBox.confirm('确定要清空购物车吗？', '确认清空', {
      confirmButtonText: '清空',
      cancelButtonText: '取消',
      type: 'warning'
    })
    cartStore.clearCart()
    ElMessage.success('购物车已清空')
  } catch {
    // 用户取消
  }
}
</script>

<template>
  <div class="cart-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-mesh"></div>
      <div class="header-grid"></div>
      <div class="header-content">
        <div class="header-badge">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M3 3h2l.4 2M7 5h10l1.4 8.4A2 2 0 0116.4 16H7.6a2 2 0 01-2-1.6L3 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="9" cy="21" r="1" fill="currentColor"/>
            <circle cx="20" cy="21" r="1" fill="currentColor"/>
          </svg>
          <span>购物车</span>
        </div>
        <h1 class="page-title">我的购物车</h1>
        <p class="page-subtitle">{{ totalQuantity }} 件商品</p>
      </div>
      <div class="header-circle header-circle-1"></div>
      <div class="header-circle header-circle-2"></div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Empty State -->
      <div v-if="cartItems.length === 0" class="empty-cart">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" width="96" height="96">
            <path d="M3 3h2l.4 2M7 5h10l1.4 8.4A2 2 0 0116.4 16H7.6a2 2 0 01-2-1.6L3 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="9" cy="21" r="1" fill="currentColor"/>
            <circle cx="20" cy="21" r="1" fill="currentColor"/>
          </svg>
        </div>
        <h2 class="empty-title">购物车是空的</h2>
        <p class="empty-desc">您还没有添加任何配件</p>
        <button class="btn btn-primary" @click="router.push('/products')">
          <span>浏览商品</span>
          <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
            <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>

      <!-- Cart Content -->
      <div v-else class="cart-content">
        <!-- Cart Items List -->
        <div class="cart-items-section">
          <!-- Select All Bar -->
          <div class="select-all-bar">
            <el-checkbox
              :model-value="cartItems.length > 0 && cartItems.every(item => item.selected)"
              @change="toggleSelectAll"
              size="large"
            >
              <span class="select-all-text">全选 ({{ cartItems.length }})</span>
            </el-checkbox>
            <button class="clear-cart-btn" @click="handleClearCart">
              <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              清空购物车
            </button>
          </div>

          <!-- Cart Items -->
          <div class="cart-items-list">
            <div
              v-for="item in cartItems"
              :key="item.id"
              :class="['cart-item', { selected: item.selected }]"
            >
              <div class="item-checkbox">
                <el-checkbox :model-value="item.selected" @change="toggleSelect(item)" size="large" />
              </div>
              <div class="item-image">
                <img :src="item.product_image || item.product?.image" :alt="item.product_name" />
              </div>
              <div class="item-info">
                <h3 class="item-name">{{ item.product_name }}</h3>
                <p class="item-sku">编号: {{ item.product_id }}</p>
              </div>
              <div class="item-price">{{ formatCurrency(item.price) }}</div>
              <div class="item-quantity">
                <button class="qty-btn" @click="handleQuantityChange(item, item.quantity - 1)" :disabled="item.quantity <= 1">
                  <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                    <path d="M19 12H5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
                <span class="qty-value">{{ item.quantity }}</span>
                <button class="qty-btn" @click="handleQuantityChange(item, item.quantity + 1)">
                  <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
                    <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>
              <div class="item-total">{{ formatCurrency(item.price * item.quantity) }}</div>
              <div class="item-actions">
                <button class="action-btn" @click="handleRemoveItem(item)">
                  <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="order-summary">
          <h2 class="summary-title">订单摘要</h2>

          <!-- Coupon Selector -->
          <div class="coupon-section">
            <label class="coupon-label">选择优惠券</label>
            <el-select
              v-model="selectedCoupon"
              placeholder="选择优惠券"
              clearable
              :loading="couponLoading"
              class="coupon-select"
            >
              <el-option
                v-for="userCoupon in availableCoupons"
                :key="userCoupon.id"
                :label="`${userCoupon.coupon.name} - ${userCoupon.coupon.discount_amount ? '¥' + userCoupon.coupon.discount_amount : userCoupon.coupon.discount_percent + '%折'}`"
                :value="userCoupon"
              >
                <div class="coupon-option">
                  <div class="coupon-option-name">{{ userCoupon.coupon.name }}</div>
                  <div class="coupon-option-value">
                    {{ userCoupon.coupon.discount_amount ? '¥' + userCoupon.coupon.discount_amount : userCoupon.coupon.discount_percent + '%折' }}
                  </div>
                </div>
              </el-option>
            </el-select>
            <div v-if="selectedCoupon" class="coupon-hint">
              <span v-if="selectedCoupon.coupon.min_purchase_amount && selectedPrice < selectedCoupon.coupon.min_purchase_amount" class="coupon-hint-warning">
                还差 ¥{{ (selectedCoupon.coupon.min_purchase_amount - selectedPrice).toFixed(2) }} 可用
              </span>
              <span v-else class="coupon-hint-success">
                可优惠 ¥{{ couponDiscount.toFixed(2) }}
              </span>
            </div>
          </div>

          <!-- Price Details -->
          <div class="price-details">
            <div class="price-row">
              <span class="price-label">商品小计 ({{ selectedItems.length }} 件)</span>
              <span class="price-value">{{ formatCurrency(selectedPrice) }}</span>
            </div>
            <div class="price-row">
              <span class="price-label">运费</span>
              <span class="price-value price-free">结算时计算</span>
            </div>
            <div class="price-row" v-if="couponDiscount > 0">
              <span class="price-label">优惠券</span>
              <span class="price-value price-discount">-{{ formatCurrency(couponDiscount) }}</span>
            </div>
            <div class="price-divider"></div>
            <div class="price-row price-row-total">
              <span class="price-label">合计</span>
              <span class="price-value">{{ formatCurrency(finalPrice) }}</span>
            </div>
          </div>

          <!-- Checkout Button -->
          <button
            class="btn btn-checkout"
            :disabled="selectedItems.length === 0 || loading"
            @click="handleCheckout"
          >
            <span v-if="loading">处理中...</span>
            <span v-else>立即结算</span>
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none">
              <path d="M5 12H14M12 5L19 12M12 5V19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>

          <!-- Trust Badges -->
          <div class="trust-badges">
            <div class="trust-badge">
              <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>安全支付</span>
            </div>
            <div class="trust-badge">
              <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7c0-2.76 2.24-5 5-5s5 2.24 5 5v4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>SSL 加密</span>
            </div>
            <div class="trust-badge">
              <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l8.91-1.01L12 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>正品保障</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Page Header */
.page-header {
  position: relative;
  padding: 80px 40px 60px;
  overflow: hidden;
  background: #0f172a;
}

.header-mesh {
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

.header-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(249, 115, 22, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(249, 115, 22, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 70% 70% at 50% 50%, black, transparent);
}

.header-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.header-badge {
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

.page-title {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 16px;
  color: #94a3b8;
}

.header-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.header-circle-1 {
  width: 400px;
  height: 400px;
  background: #f97316;
  top: -100px;
  right: -100px;
}

.header-circle-2 {
  width: 300px;
  height: 300px;
  background: #3b82f6;
  bottom: -50px;
  left: -50px;
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Empty Cart */
.empty-cart {
  text-align: center;
  padding: 80px 40px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px dashed rgba(71, 85, 105, 0.5);
  border-radius: 16px;
}

.empty-icon {
  width: 96px;
  height: 96px;
  margin: 0 auto 24px;
  color: #475569;
}

.empty-icon svg {
  width: 100%;
  height: 100%;
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 8px;
}

.empty-desc {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 32px;
}

/* Cart Content */
.cart-content {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 32px;
}

/* Cart Items Section */
.cart-items-section {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  overflow: hidden;
}

.select-all-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(71, 85, 105, 0.5);
}

.select-all-text {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.clear-cart-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: #ef4444;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.clear-cart-btn:hover {
  background: rgba(239, 68, 68, 0.1);
}

.cart-items-list {
  display: flex;
  flex-direction: column;
}

.cart-item {
  display: grid;
  grid-template-columns: auto 80px 1fr auto auto auto auto;
  gap: 16px;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(71, 85, 105, 0.3);
  transition: all 0.2s ease;
}

.cart-item:hover {
  background: rgba(15, 23, 42, 0.3);
}

.cart-item.selected {
  background: rgba(249, 115, 22, 0.05);
}

.item-checkbox :deep(.el-checkbox__label) {
  color: #94a3b8;
}

.item-checkbox :deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: #f97316;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  background: rgba(15, 23, 42, 0.5);
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-sku {
  font-size: 12px;
  color: #64748b;
}

.item-price {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  min-width: 80px;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  padding: 4px;
}

.qty-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 41, 59, 0.5);
  border: none;
  color: #94a3b8;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.qty-btn:hover:not(:disabled) {
  background: rgba(249, 115, 22, 0.15);
  color: #f97316;
}

.qty-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qty-value {
  width: 40px;
  text-align: center;
  font-size: 14px;
  font-weight: 700;
  color: #e2e8f0;
}

.item-total {
  font-size: 18px;
  font-weight: 800;
  color: #f97316;
  min-width: 90px;
  text-align: right;
}

.item-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  border-color: #ef4444;
  color: #ef4444;
}

/* Order Summary */
.order-summary {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  padding: 24px;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.summary-title {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 24px;
}

/* Coupon Section */
.coupon-section {
  margin-bottom: 20px;
}

.coupon-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 8px;
}

.coupon-select {
  width: 100%;
}

.coupon-select :deep(.el-input__wrapper) {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  box-shadow: none;
}

.coupon-select :deep(.el-input__inner) {
  color: #e2e8f0;
}

.coupon-select :deep(.el-input__wrapper:hover) {
  border-color: rgba(249, 115, 22, 0.5);
}

.coupon-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.coupon-option-name {
  font-size: 14px;
  color: #e2e8f0;
}

.coupon-option-value {
  font-size: 13px;
  font-weight: 600;
  color: #f97316;
}

.coupon-hint {
  margin-top: 8px;
  font-size: 12px;
}

.coupon-hint-warning {
  color: #f59e0b;
}

.coupon-hint-success {
  color: #22c55e;
}

.price-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-label {
  font-size: 14px;
  color: #94a3b8;
}

.price-value {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.price-free {
  color: #22c55e;
}

.price-discount {
  color: #ef4444;
}

.price-divider {
  height: 1px;
  background: rgba(71, 85, 105, 0.5);
  margin: 4px 0;
}

.price-row-total {
  padding-top: 8px;
}

.price-row-total .price-label {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
}

.price-row-total .price-value {
  font-size: 24px;
  font-weight: 800;
  color: #f97316;
}

.btn-checkout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 24px;
}

.btn-checkout:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(249, 115, 22, 0.4);
}

.btn-checkout:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.trust-badges {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 24px;
  border-top: 1px solid rgba(71, 85, 105, 0.5);
}

.trust-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #94a3b8;
}

.trust-badge svg {
  color: #f97316;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border: none;
  border-radius: 12px;
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(249, 115, 22, 0.4);
}

/* Responsive */
@media (max-width: 1024px) {
  .cart-content {
    grid-template-columns: 1fr;
  }

  .order-summary {
    position: static;
  }

  .cart-item {
    grid-template-columns: auto 60px 1fr;
    gap: 12px;
  }

  .item-price,
  .item-quantity,
  .item-total,
  .item-actions {
    grid-column: 3;
  }

  .item-price {
    font-size: 14px;
    margin-bottom: 8px;
  }

  .item-quantity {
    margin-bottom: 8px;
  }

  .item-total {
    font-size: 16px;
  }

  .item-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 640px) {
  .page-header {
    padding: 60px 20px 40px;
  }

  .cart-item {
    padding: 16px;
  }

  .item-image {
    width: 60px;
    height: 60px;
  }
}
</style>
