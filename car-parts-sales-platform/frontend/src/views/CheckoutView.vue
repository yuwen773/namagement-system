<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getCartApi,
  getAddressListApi,
  createAddressApi,
  getMyCouponsApi,
  createOrderApi
} from '@/api'
import { formatCurrency, formatDateTime } from '@/utils'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()

// State
const loading = ref(true)
const submitting = ref(false)
const cart = ref(null)
const addresses = ref([])
const coupons = ref([])
const selectedAddressId = ref(null)
const selectedCouponId = ref(null)

// Address form dialog
const addressDialogVisible = ref(false)
const addressFormRef = ref(null)
const addressForm = ref({
  receiver_name: '',
  receiver_phone: '',
  province: '',
  city: '',
  district: '',
  detail_address: '',
  is_default: false
})

const addressRules = {
  receiver_name: [{ required: true, message: '请输入收货人姓名', trigger: 'blur' }],
  receiver_phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  province: [{ required: true, message: '请选择省份', trigger: 'change' }],
  city: [{ required: true, message: '请选择城市', trigger: 'change' }],
  district: [{ required: true, message: '请选择区县', trigger: 'change' }],
  detail_address: [{ required: true, message: '请输入详细地址', trigger: 'blur' }]
}

// Region data (simplified)
const provinces = ref(['北京市', '上海市', '广东省', '江苏省', '浙江省', '山东省', '四川省', '湖北省'])
const cities = ref({
  '北京市': ['北京市'],
  '上海市': ['上海市'],
  '广东省': ['广州市', '深圳市', '东莞市', '佛山市'],
  '江苏省': ['南京市', '苏州市', '无锡市', '常州市'],
  '浙江省': ['杭州市', '宁波市', '温州市', '嘉兴市'],
  '山东省': ['济南市', '青岛市', '烟台市', '潍坊市'],
  '四川省': ['成都市', '绵阳市', '德阳市', '南充市'],
  '湖北省': ['武汉市', '宜昌市', '襄阳市', '荆州市']
})
const districts = ref({
  '北京市': ['朝阳区', '海淀区', '东城区', '西城区'],
  '上海市': ['浦东新区', '黄浦区', '静安区', '徐汇区'],
  '广州市': ['天河区', '越秀区', '海珠区', '白云区'],
  '深圳市': ['福田区', '南山区', '罗湖区', '宝安区'],
  '杭州市': ['西湖区', '拱墅区', '上城区', '滨江区'],
  '南京市': ['玄武区', '秦淮区', '鼓楼区', '建邺区'],
  '武汉市': ['武昌区', '江汉区', '洪山区', '江岸区'],
  '成都市': ['武侯区', '锦江区', '青羊区', '金牛区']
})

// Computed
const selectedItems = computed(() => {
  if (!cart.value?.items) return []
  return cart.value.items.filter(item => item.selected)
})

const subtotalAmount = computed(() => {
  return selectedItems.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})

const couponDiscount = computed(() => {
  if (!selectedCouponId.value) return 0
  const coupon = coupons.value.find(c => c.id === selectedCouponId.value)
  if (!coupon) return 0

  if (coupon.coupon.discount_type === 'full_reduction') {
    return coupon.coupon.discount_amount || 0
  } else if (coupon.coupon.discount_type === 'discount') {
    return Math.round(subtotalAmount.value * (1 - (coupon.coupon.discount_percent || 100) / 100))
  }
  return 0
})

const shippingFee = computed(() => {
  return 0 // Free shipping
})

const totalAmount = computed(() => {
  return Math.max(0, subtotalAmount.value - couponDiscount.value + shippingFee.value)
})

const canSubmit = computed(() => {
  return selectedAddressId.value && selectedItems.value.length > 0 && !submitting.value
})

// Fetch data
onMounted(async () => {
  await Promise.all([fetchCart(), fetchAddresses(), fetchCoupons()])
  loading.value = false
})

async function fetchCart() {
  try {
    cart.value = await getCartApi()
  } catch (error) {
    ElMessage.error('获取购物车失败')
    console.error(error)
  }
}

async function fetchAddresses() {
  try {
    addresses.value = await getAddressListApi()
    // Auto-select default address
    const defaultAddr = addresses.value.find(a => a.is_default)
    if (defaultAddr) {
      selectedAddressId.value = defaultAddr.id
    } else if (addresses.value.length > 0) {
      selectedAddressId.value = addresses.value[0].id
    }
  } catch (error) {
    console.error('Failed to fetch addresses:', error)
  }
}

async function fetchCoupons() {
  try {
    const data = await getMyCouponsApi({ status: 'unused', page: 1, page_size: 100 })
    coupons.value = data.results || []
  } catch (error) {
    console.error('Failed to fetch coupons:', error)
  }
}

// Address dialog
function openAddressDialog() {
  addressDialogVisible.value = true
  resetAddressForm()
}

function resetAddressForm() {
  addressForm.value = {
    receiver_name: '',
    receiver_phone: '',
    province: '',
    city: '',
    district: '',
    detail_address: '',
    is_default: false
  }
  addressFormRef.value?.clearValidate()
}

async function handleProvinceChange() {
  addressForm.value.city = ''
  addressForm.value.district = ''
}

async function handleCityChange() {
  addressForm.value.district = ''
}

async function submitAddress() {
  try {
    await addressFormRef.value.validate()
    await createAddressApi(addressForm.value)
    ElMessage.success('地址添加成功')
    addressDialogVisible.value = false
    await fetchAddresses()
  } catch (error) {
    if (error !== false) {
      ElMessage.error('添加地址失败')
    }
  }
}

// Submit order
async function handleSubmitOrder() {
  if (!canSubmit.value) return

  submitting.value = true
  try {
    const orderData = {
      address_id: selectedAddressId.value
    }
    if (selectedCouponId.value) {
      orderData.coupon_id = selectedCouponId.value
    }

    const result = await createOrderApi(orderData)
    ElMessage.success('订单创建成功')
    // Redirect to payment page
    router.push({
      name: 'payment',
      params: { id: result.id },
      query: { amount: totalAmount.value }
    })
  } catch (error) {
    ElMessage.error(error.message || '创建订单失败')
  } finally {
    submitting.value = false
  }
}

function handleBack() {
  router.back()
}

// Coupon helpers
function getCouponDiscountText(coupon) {
  if (coupon.coupon.discount_type === 'full_reduction') {
    return `¥${coupon.coupon.discount_amount}`
  } else {
    return `${coupon.coupon.discount_percent / 10}折`
  }
}

function getCouponConditionText(coupon) {
  if (coupon.coupon.min_purchase_amount > 0) {
    return `满¥${coupon.coupon.min_purchase_amount}可用`
  }
  return '无门槛'
}
</script>

<template>
  <div class="checkout-view">
    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
    </div>

    <template v-else>
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-bg"></div>
        <div class="header-content">
          <button class="back-btn" @click="handleBack">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M19 12H5M12 19L5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div class="header-text">
            <h1 class="page-title">Checkout</h1>
            <p class="page-subtitle">Confirm your order details</p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="selectedItems.length === 0" class="empty-state">
        <svg class="empty-icon" viewBox="0 0 24 24" fill="none">
          <path d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h3>No items selected</h3>
        <p>Please select items from your cart to checkout</p>
        <button class="btn-primary" @click="router.push('/cart')">
          <span>Go to Cart</span>
        </button>
      </div>

      <template v-else>
        <!-- Main Content -->
        <div class="main-content">
          <!-- Address Section -->
          <section class="checkout-section">
            <div class="section-header">
              <svg class="section-icon" viewBox="0 0 24 24" fill="none">
                <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <h2 class="section-title">Shipping Address</h2>
            </div>

            <div class="address-list">
              <label
                v-for="address in addresses"
                :key="address.id"
                :class="['address-card', { selected: selectedAddressId === address.id }]"
              >
                <input type="radio" v-model="selectedAddressId" :value="address.id" class="sr-only" />
                <div class="address-radio">
                  <div class="radio-inner"></div>
                </div>
                <div class="address-content">
                  <div class="address-header">
                    <span class="receiver-name">{{ address.receiver_name }}</span>
                    <span class="receiver-phone">{{ address.receiver_phone }}</span>
                    <span v-if="address.is_default" class="default-badge">DEFAULT</span>
                  </div>
                  <p class="address-detail">
                    {{ address.province }} {{ address.city }} {{ address.district }} {{ address.detail_address }}
                  </p>
                </div>
              </label>

              <button class="address-card add-address-btn" @click="openAddressDialog">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Add New Address</span>
              </button>
            </div>
          </section>

          <!-- Products Section -->
          <section class="checkout-section">
            <div class="section-header">
              <svg class="section-icon" viewBox="0 0 24 24" fill="none">
                <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <h2 class="section-title">Order Items</h2>
              <span class="item-count">{{ selectedItems.length }} items</span>
            </div>

            <div class="products-list">
              <div v-for="item in selectedItems" :key="item.id" class="product-card">
                <img :src="item.product_image || item.product?.image" :alt="item.product_name" class="product-image" />
                <div class="product-info">
                  <h3 class="product-name">{{ item.product_name }}</h3>
                  <p class="product-spec">{{ item.product_spec || 'Standard Specification' }}</p>
                  <div class="product-meta">
                    <span class="product-sku">SKU: {{ item.product_sku || 'N/A' }}</span>
                  </div>
                </div>
                <div class="product-pricing">
                  <span class="product-price">{{ formatCurrency(item.price) }}</span>
                  <span class="product-qty">× {{ item.quantity }}</span>
                  <span class="product-subtotal">{{ formatCurrency(item.price * item.quantity) }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- Coupon Section -->
          <section class="checkout-section">
            <div class="section-header">
              <svg class="section-icon" viewBox="0 0 24 24" fill="none">
                <path d="M15 5v2M15 11v2M15 17v2M5 5h14a2 2 0 012 2v3a2 2 0 000 4v3a2 2 0 01-2 2H5a2 2 0 01-2-2v-3a2 2 0 000-4V7a2 2 0 012-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <h2 class="section-title">Apply Coupon</h2>
            </div>

            <div class="coupon-list">
              <label :class="['coupon-card', { selected: selectedCouponId === null }]">
                <input type="radio" v-model="selectedCouponId" :value="null" class="sr-only" />
                <div class="coupon-radio">
                  <div class="radio-inner"></div>
                </div>
                <div class="coupon-content">
                  <span class="coupon-name">No Coupon</span>
                  <span class="coupon-desc">Skip coupon application</span>
                </div>
              </label>

              <label
                v-for="coupon in coupons"
                :key="coupon.id"
                :class="['coupon-card', { disabled: subtotalAmount < (coupon.coupon.min_purchase_amount || 0), selected: selectedCouponId === coupon.id }]"
              >
                <input
                  type="radio"
                  v-model="selectedCouponId"
                  :value="coupon.id"
                  :disabled="subtotalAmount < (coupon.coupon.min_purchase_amount || 0)"
                  class="sr-only"
                />
                <div class="coupon-radio">
                  <div class="radio-inner"></div>
                </div>
                <div class="coupon-content">
                  <div class="coupon-header">
                    <span class="coupon-name">{{ coupon.coupon.name }}</span>
                    <span class="coupon-value">{{ getCouponDiscountText(coupon) }}</span>
                  </div>
                  <p class="coupon-desc">{{ getCouponConditionText(coupon) }} · Valid until {{ new Date(coupon.coupon.end_time).toLocaleDateString() }}</p>
                </div>
              </label>

              <div v-if="coupons.length === 0" class="no-coupons">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>No available coupons</span>
              </div>
            </div>
          </section>

          <!-- Price Summary Section -->
          <section class="checkout-section summary-section">
            <h2 class="section-title">Order Summary</h2>
            <div class="summary-row">
              <span>Subtotal</span>
              <span>{{ formatCurrency(subtotalAmount) }}</span>
            </div>
            <div class="summary-row">
              <span>Shipping</span>
              <span :class="{ 'text-green': shippingFee === 0 }">
                {{ shippingFee === 0 ? 'FREE' : formatCurrency(shippingFee) }}
              </span>
            </div>
            <div v-if="couponDiscount > 0" class="summary-row discount-row">
              <span>Coupon Discount</span>
              <span class="discount">-{{ formatCurrency(couponDiscount) }}</span>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-row total-row">
              <span>Total</span>
              <span class="total-amount">{{ formatCurrency(totalAmount) }}</span>
            </div>
          </section>

          <!-- Bottom spacer for fixed bar -->
          <div class="bottom-spacer"></div>
        </div>

        <!-- Fixed Bottom Bar -->
        <div class="bottom-bar">
          <div class="bar-content">
            <div class="bar-summary">
              <span class="bar-label">Total Amount</span>
              <span class="bar-amount">{{ formatCurrency(totalAmount) }}</span>
            </div>
            <button
              class="submit-btn"
              :class="{ disabled: !canSubmit }"
              :disabled="!canSubmit"
              @click="handleSubmitOrder"
            >
              <span v-if="!submitting">Place Order</span>
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
      </template>
    </template>

    <!-- Add Address Dialog -->
    <el-dialog
      v-model="addressDialogVisible"
      title="Add New Address"
      width="500px"
      :close-on-click-modal="false"
      class="address-dialog"
    >
      <el-form
        ref="addressFormRef"
        :model="addressForm"
        :rules="addressRules"
        label-width="80px"
        label-position="left"
      >
        <el-form-item label="Name" prop="receiver_name">
          <el-input v-model="addressForm.receiver_name" placeholder="Enter recipient name" />
        </el-form-item>
        <el-form-item label="Phone" prop="receiver_phone">
          <el-input v-model="addressForm.receiver_phone" placeholder="Enter mobile number" />
        </el-form-item>
        <el-form-item label="Region" prop="province" required>
          <div class="region-selectors">
            <el-select v-model="addressForm.province" placeholder="Province" @change="handleProvinceChange" style="width: 32%">
              <el-option v-for="p in provinces" :key="p" :label="p" :value="p" />
            </el-select>
            <el-select v-model="addressForm.city" placeholder="City" @change="handleCityChange" :disabled="!addressForm.province" style="width: 32%">
              <el-option v-for="c in cities[addressForm.province] || []" :key="c" :label="c" :value="c" />
            </el-select>
            <el-select v-model="addressForm.district" placeholder="District" :disabled="!addressForm.city" style="width: 32%">
              <el-option v-for="d in districts[addressForm.city] || []" :key="d" :label="d" :value="d" />
            </el-select>
          </div>
        </el-form-item>
        <el-form-item label="Address" prop="detail_address">
          <el-input v-model="addressForm.detail_address" type="textarea" :rows="3" placeholder="Enter detailed address" />
        </el-form-item>
        <el-form-item prop="is_default">
          <el-checkbox v-model="addressForm.is_default">Set as default address</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addressDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitAddress" :loading="submitting">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.checkout-view {
  --font-display: 'Oswald', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --color-bg: #0f172a;
  --color-card: #1e293b;
  --color-border: #334155;
  --color-accent: #f97316;
  --color-accent-hover: #ea580c;
  --color-text: #f1f5f9;
  --color-text-muted: #94a3b8;
  min-height: 100vh;
  background: var(--color-bg);
  padding-bottom: 100px;
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  z-index: 100;
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

/* Page Header */
.page-header {
  position: relative;
  background: var(--color-bg);
  padding: 24px 20px;
  border-bottom: 1px solid var(--color-border);
  overflow: hidden;
}

.header-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 100%, rgba(249, 115, 22, 0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 0%, rgba(249, 115, 22, 0.08), transparent);
  opacity: 0.6;
}

.header-content {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  max-width: 900px;
  margin: 0 auto;
}

.back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 8px;
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

.header-text {
  flex: 1;
}

.page-title {
  font-family: var(--font-display);
  font-size: 28px;
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

/* Empty State */
.empty-state {
  max-width: 900px;
  margin: 60px auto;
  padding: 80px 40px;
  text-align: center;
  background: var(--color-card);
  border-radius: 12px;
  border: 1px solid var(--color-border);
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: var(--color-text-muted);
  margin-bottom: 24px;
}

.empty-state h3 {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 12px;
}

.empty-state p {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text-muted);
  margin-bottom: 32px;
}

.btn-primary {
  padding: 14px 32px;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: white;
  background: var(--color-accent);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-primary:hover {
  background: var(--color-accent-hover);
}

/* Main Content */
.main-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 20px;
}

/* Checkout Sections */
.checkout-section {
  background: var(--color-card);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  padding: 24px;
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}

.section-icon {
  width: 24px;
  height: 24px;
  color: var(--color-accent);
  flex-shrink: 0;
}

.section-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text);
  margin: 0;
  flex: 1;
}

.item-count {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Address List */
.address-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.address-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 2px solid var(--color-border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.address-card:hover {
  border-color: var(--color-accent);
  background: rgba(249, 115, 22, 0.05);
}

.address-card.selected {
  border-color: var(--color-accent);
  background: rgba(249, 115, 22, 0.1);
}

.address-radio {
  position: relative;
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.2s ease;
}

.address-card.selected .address-radio {
  border-color: var(--color-accent);
}

.radio-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0);
  width: 10px;
  height: 10px;
  background: var(--color-accent);
  border-radius: 50%;
  transition: transform 0.2s ease;
}

.address-card.selected .radio-inner {
  transform: translate(-50%, -50%) scale(1);
}

.address-content {
  flex: 1;
}

.address-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.receiver-name {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
}

.receiver-phone {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text-muted);
}

.default-badge {
  padding: 2px 8px;
  font-family: var(--font-body);
  font-size: 10px;
  font-weight: 600;
  color: var(--color-accent);
  background: rgba(249, 115, 22, 0.15);
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.address-detail {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.5;
}

.add-address-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  background: transparent;
  border: 2px dashed var(--color-border);
  border-radius: 10px;
  color: var(--color-text-muted);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-address-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.add-address-btn svg {
  width: 20px;
  height: 20px;
}

/* Products List */
.products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-card {
  display: grid;
  grid-template-columns: 80px 1fr auto;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  align-items: center;
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  background: var(--color-bg);
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
  line-height: 1.4;
}

.product-spec {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

.product-meta {
  margin-top: 4px;
}

.product-sku {
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 500;
  color: var(--color-text-muted);
  font-family: 'Courier New', monospace;
  letter-spacing: 0.05em;
}

.product-pricing {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.product-price {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
}

.product-qty {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-text-muted);
}

.product-subtotal {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-accent);
}

/* Coupon List */
.coupon-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.coupon-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 2px solid var(--color-border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.coupon-card:hover:not(.disabled) {
  border-color: var(--color-accent);
  background: rgba(249, 115, 22, 0.05);
}

.coupon-card.selected {
  border-color: var(--color-accent);
  background: rgba(249, 115, 22, 0.1);
}

.coupon-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.coupon-radio {
  position: relative;
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.coupon-card.selected .coupon-radio {
  border-color: var(--color-accent);
}

.coupon-radio .radio-inner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0);
  width: 10px;
  height: 10px;
  background: var(--color-accent);
  border-radius: 50%;
  transition: transform 0.2s ease;
}

.coupon-card.selected .coupon-radio .radio-inner {
  transform: translate(-50%, -50%) scale(1);
}

.coupon-content {
  flex: 1;
}

.coupon-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.coupon-name {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
}

.coupon-value {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-accent);
}

.coupon-desc {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

.no-coupons {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 32px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 10px;
  color: var(--color-text-muted);
  font-family: var(--font-body);
  font-size: 14px;
}

.no-coupons svg {
  width: 24px;
  height: 24px;
}

/* Summary Section */
.summary-section {
  background: linear-gradient(135deg, var(--color-card) 0%, rgba(30, 41, 59, 0.8) 100%);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--color-text-muted);
}

.summary-row span:first-child {
  font-weight: 500;
}

.summary-row span:last-child {
  font-weight: 600;
  color: var(--color-text);
}

.summary-row.discount-row {
  color: var(--color-accent);
}

.summary-row.discount-row .discount {
  font-weight: 700;
}

.summary-divider {
  height: 1px;
  background: var(--color-border);
  margin: 8px 0;
}

.total-row {
  padding-top: 16px;
}

.total-row span:first-child {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text);
}

.total-amount {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: var(--color-accent) !important;
}

.text-green {
  color: #10b981 !important;
}

/* Bottom Bar */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--color-border);
}

.bar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 900px;
  margin: 0 auto;
  gap: 20px;
}

.bar-summary {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.bar-label {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.bar-amount {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--color-accent);
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px 40px;
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
}

.submit-btn:hover:not(.disabled) {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(249, 115, 22, 0.3);
}

.submit-btn.disabled {
  opacity: 0.5;
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

.bottom-spacer {
  height: 100px;
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

/* Address Dialog */
:deep(.address-dialog) {
  background: var(--color-card);
}

:deep(.address-dialog .el-dialog) {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 12px;
}

:deep(.address-dialog .el-dialog__header) {
  border-bottom: 1px solid var(--color-border);
  padding: 20px 24px;
}

:deep(.address-dialog .el-dialog__title) {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-text);
}

:deep(.address-dialog .el-dialog__body) {
  padding: 24px;
}

:deep(.address-dialog .el-dialog__footer) {
  border-top: 1px solid var(--color-border);
  padding: 16px 24px;
}

:deep(.address-dialog .el-form-item__label) {
  color: var(--color-text-muted);
  font-weight: 500;
}

:deep(.address-dialog .el-input__wrapper) {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--color-border);
  box-shadow: none;
}

:deep(.address-dialog .el-input__wrapper:hover),
:deep(.address-dialog .el-input__wrapper.is-focus) {
  border-color: var(--color-accent);
}

:deep(.address-dialog .el-input__inner) {
  color: var(--color-text);
}

:deep(.address-dialog .el-textarea__inner) {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--color-border);
  color: var(--color-text);
}

:deep(.address-dialog .el-textarea__inner:hover),
:deep(.address-dialog .el-textarea__inner:focus) {
  border-color: var(--color-accent);
}

:deep(.address-dialog .el-select .el-input__wrapper) {
  background: rgba(15, 23, 42, 0.5);
}

.region-selectors {
  display: flex;
  gap: 8px;
  width: 100%;
}

:deep(.address-dialog .el-checkbox__label) {
  color: var(--color-text-muted);
}

:deep(.address-dialog .el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--color-accent);
  border-color: var(--color-accent);
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 22px;
  }

  .product-card {
    grid-template-columns: 60px 1fr;
    gap: 12px;
  }

  .product-image {
    width: 60px;
    height: 60px;
  }

  .product-pricing {
    grid-column: 1 / -1;
    flex-direction: row;
    justify-content: space-between;
    padding-top: 8px;
    border-top: 1px solid var(--color-border);
  }

  .bar-content {
    flex-direction: column;
    align-items: stretch;
  }

  .bar-summary {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .submit-btn {
    width: 100%;
  }

  .region-selectors {
    flex-direction: column;
  }

  :deep(.region-selectors .el-select) {
    width: 100% !important;
  }
}
</style>
