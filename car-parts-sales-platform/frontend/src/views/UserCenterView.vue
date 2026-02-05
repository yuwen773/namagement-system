<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  getAddressListApi,
  createAddressApi,
  updateAddressApi,
  deleteAddressApi,
  setDefaultAddressApi,
  updateProfileApi,
  changePasswordApi,
  getMessagesApi,
  readMessageApi
} from '@/api/modules/user'
import {
  getMyReviewsApi,
  deleteReviewApi
} from '@/api/modules/product'
import {
  getMyCouponsApi
} from '@/api/modules/marketing'
import {
  getReturnListApi,
  getReturnDetailApi
} from '@/api/modules/order'
import { maskPhone, formatDate } from '@/utils'
import { ElMessage, ElMessageBox } from 'element-plus'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 当前激活的菜单项
const activeMenu = ref('profile')

// 用户菜单配置
const userMenu = [
  { id: 'profile', icon: 'user', label: 'Profile', desc: 'Manage your account information' },
  { id: 'security', icon: 'security', label: 'Security', desc: 'Password and authentication settings' },
  { id: 'addresses', icon: 'location', label: 'Addresses', desc: 'Manage your shipping addresses' },
  { id: 'points', icon: 'star', label: 'My Points', desc: 'View your points history' },
  { id: 'coupons', icon: 'ticket', label: 'My Coupons', desc: 'View available coupons' },
  { id: 'reviews', icon: 'star', label: 'My Reviews', desc: 'Manage your product reviews' },
  { id: 'returns', icon: 'refresh', label: 'After-sales', desc: 'Track return requests' },
  { id: 'messages', icon: 'message', label: 'Messages', desc: 'System notifications' }
]

const user = computed(() => authStore.user)

// ============ 个人资料模块 ============
const loading = ref(false)
const savingProfile = ref(false)
const profileForm = ref({
  nickname: '',
  avatar: ''
})

// 密码修改表单
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})
const changingPassword = ref(false)

// ============ 地址管理模块 ============
const addressList = ref([])
const addressLoading = ref(false)
const addressDialogVisible = ref(false)
const addressFormRef = ref(null)
const editingAddress = ref(null)
const addressForm = ref({
  recipient_name: '',
  recipient_phone: '',
  province: '',
  city: '',
  district: '',
  detailed_address: '',
  is_default: false
})

// ============ 积分模块 ============
const pointsHistory = ref([])
const pointsLoading = ref(false)

// ============ 优惠券模块 ============
const couponList = ref([])
const couponLoading = ref(false)
const activeCouponTab = ref('available')

// ============ 评价模块 ============
const reviewList = ref([])
const reviewLoading = ref(false)

// ============ 售后模块 ============
const returnList = ref([])
const returnLoading = ref(false)
const returnDetailVisible = ref(false)
const currentReturn = ref(null)

// ============ 消息中心模块 ============
const messageList = ref([])
const messageLoading = ref(false)
const messageDetailVisible = ref(false)
const currentMessage = ref(null)

// 初始化
onMounted(async () => {
  // 从路由获取初始菜单
  const menuFromRoute = route.query.tab
  if (menuFromRoute && userMenu.find(m => m.id === menuFromRoute)) {
    activeMenu.value = menuFromRoute
  }

  if (user.value) {
    profileForm.value = {
      nickname: user.value.nickname || '',
      avatar: user.value.avatar || ''
    }
  }

  // 根据当前菜单加载数据
  await loadMenuData(activeMenu.value)
})

// 监听菜单切换
async function goToMenu(menuId) {
  activeMenu.value = menuId
  await loadMenuData(menuId)
}

// 根据菜单加载数据
async function loadMenuData(menuId) {
  switch (menuId) {
    case 'addresses':
      await fetchAddressList()
      break
    case 'points':
      await fetchPointsHistory()
      break
    case 'coupons':
      await fetchCouponList('available')
      break
    case 'reviews':
      await fetchReviewList()
      break
    case 'returns':
      await fetchReturnList()
      break
    case 'messages':
      await fetchMessageList()
      break
  }
}

// ============ 个人资料相关 ============
async function handleSaveProfile() {
  savingProfile.value = true
  try {
    await updateProfileApi(profileForm.value)
    authStore.updateUser(profileForm.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    savingProfile.value = false
  }
}

async function handleChangePassword() {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  if (passwordForm.value.new_password.length < 6) {
    ElMessage.error('密码长度不能少于6位')
    return
  }

  changingPassword.value = true
  try {
    await changePasswordApi({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })
    ElMessage.success('密码修改成功，请重新登录')
    passwordForm.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
    setTimeout(() => {
      authStore.logout()
      router.push('/login')
    }, 1500)
  } catch (error) {
    ElMessage.error(error.message || '密码修改失败')
  } finally {
    changingPassword.value = false
  }
}

// ============ 地址管理相关 ============
async function fetchAddressList() {
  addressLoading.value = true
  try {
    addressList.value = await getAddressListApi()
  } catch (error) {
    ElMessage.error('获取地址列表失败')
  } finally {
    addressLoading.value = false
  }
}

function showAddAddressDialog() {
  editingAddress.value = null
  addressForm.value = {
    recipient_name: '',
    recipient_phone: '',
    province: '',
    city: '',
    district: '',
    detailed_address: '',
    is_default: false
  }
  addressDialogVisible.value = true
}

function showEditAddressDialog(address) {
  editingAddress.value = address
  addressForm.value = {
    recipient_name: address.recipient_name,
    recipient_phone: address.recipient_phone,
    province: address.province,
    city: address.city,
    district: address.district,
    detailed_address: address.detailed_address,
    is_default: address.is_default
  }
  addressDialogVisible.value = true
}

async function handleSaveAddress() {
  addressFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      if (editingAddress.value) {
        await updateAddressApi(editingAddress.value.id, addressForm.value)
        ElMessage.success('地址更新成功')
      } else {
        await createAddressApi(addressForm.value)
        ElMessage.success('地址添加成功')
      }
      addressDialogVisible.value = false
      await fetchAddressList()
    } catch (error) {
      ElMessage.error(error.message || '保存失败')
    }
  })
}

async function handleDeleteAddress(id) {
  try {
    await ElMessageBox.confirm('确定要删除这个地址吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteAddressApi(id)
    ElMessage.success('删除成功')
    await fetchAddressList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

async function handleSetDefaultAddress(id) {
  try {
    await setDefaultAddressApi(id)
    ElMessage.success('默认地址设置成功')
    await fetchAddressList()
  } catch (error) {
    ElMessage.error(error.message || '设置失败')
  }
}

// ============ 积分相关 ============
async function fetchPointsHistory() {
  pointsLoading.value = true
  try {
    // 积分明细可以从用户信息或单独的接口获取
    // 这里模拟一些积分记录数据
    pointsHistory.value = [
      { id: 1, type: 'earn', amount: 100, description: '订单完成获得积分', created_at: '2026-02-04T10:00:00Z' },
      { id: 2, type: 'spend', amount: -50, description: '积分抵扣', created_at: '2026-02-03T15:30:00Z' },
      { id: 3, type: 'earn', amount: 200, description: '注册赠送积分', created_at: '2026-02-01T00:00:00Z' }
    ]
  } catch (error) {
    ElMessage.error('获取积分记录失败')
  } finally {
    pointsLoading.value = false
  }
}

// ============ 优惠券相关 ============
async function fetchCouponList(status) {
  couponLoading.value = true
  try {
    couponList.value = await getMyCouponsApi({ status })
  } catch (error) {
    ElMessage.error('获取优惠券列表失败')
  } finally {
    couponLoading.value = false
  }
}

async function handleCouponTabChange(tabName) {
  activeCouponTab.value = tabName
  await fetchCouponList(tabName)
}

function getCouponStatusText(status) {
  const map = {
    unused: '可用',
    used: '已使用',
    expired: '已过期'
  }
  return map[status] || status
}

// ============ 评价相关 ============
async function fetchReviewList() {
  reviewLoading.value = true
  try {
    const data = await getMyReviewsApi()
    reviewList.value = data.results || []
  } catch (error) {
    ElMessage.error('获取评价列表失败')
  } finally {
    reviewLoading.value = false
  }
}

async function handleDeleteReview(id) {
  try {
    await ElMessageBox.confirm('确定要删除这条评价吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteReviewApi(id)
    ElMessage.success('删除成功')
    await fetchReviewList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// ============ 售后相关 ============
async function fetchReturnList() {
  returnLoading.value = true
  try {
    const data = await getReturnListApi()
    returnList.value = data.results || []
  } catch (error) {
    ElMessage.error('获取售后列表失败')
  } finally {
    returnLoading.value = false
  }
}

async function showReturnDetail(returnItem) {
  try {
    const data = await getReturnDetailApi(returnItem.id)
    currentReturn.value = data
    returnDetailVisible.value = true
  } catch (error) {
    ElMessage.error('获取售后详情失败')
  }
}

function getReturnStatusText(status) {
  const map = {
    pending: '待审核',
    approved: '已批准',
    rejected: '已拒绝',
    processing: '处理中',
    completed: '已完成'
  }
  return map[status] || status
}

function getReturnStatusType(status) {
  const map = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    processing: 'primary',
    completed: 'info'
  }
  return map[status] || 'info'
}

// ============ 消息中心相关 ============
async function fetchMessageList() {
  messageLoading.value = true
  try {
    const data = await getMessagesApi()
    messageList.value = data.results || []
  } catch (error) {
    ElMessage.error('获取消息列表失败')
  } finally {
    messageLoading.value = false
  }
}

async function showMessageDetail(message) {
  currentMessage.value = message
  messageDetailVisible.value = true

  // 标记为已读
  if (!message.is_read) {
    try {
      await readMessageApi(message.id)
      message.is_read = true
    } catch (error) {
      console.error('标记已读失败', error)
    }
  }
}

// ============ 退出登录 ============
async function handleLogout() {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch (error) {
    // 用户取消
  }
}
</script>

<template>
  <div class="user-center-view">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-bg"></div>
      <div class="header-content">
        <h1 class="page-title">My Account</h1>
        <p class="page-subtitle">Manage your account and preferences</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="content-grid">
        <!-- Sidebar Menu -->
        <aside class="sidebar">
          <div class="user-card">
            <div class="user-avatar">{{ user?.nickname?.charAt(0) || 'U' }}</div>
            <div class="user-info">
              <div class="user-name">{{ user?.nickname || 'User' }}</div>
              <div class="user-phone">{{ maskPhone(user?.phone || '') }}</div>
            </div>
            <div class="user-points">
              <span class="points-value">{{ user?.points || 0 }}</span>
              <span class="points-label">Points</span>
            </div>
          </div>

          <nav class="user-menu">
            <div
              v-for="menu in userMenu"
              :key="menu.id"
              :class="['menu-item', { active: activeMenu === menu.id }]"
              @click="goToMenu(menu.id)"
            >
              <div class="menu-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path v-if="menu.icon === 'user'" d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"/>
                  <circle v-if="menu.icon === 'user'" cx="12" cy="7" r="4"/>
                  <rect v-if="menu.icon === 'security'" x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path v-if="menu.icon === 'security'" d="M7 11V7a5 5 0 0110 0v4"/>
                  <path v-if="menu.icon === 'location'" d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                  <circle v-if="menu.icon === 'location'" cx="12" cy="10" r="3"/>
                  <polygon v-if="menu.icon === 'star'" points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                  <path v-if="menu.icon === 'ticket'" d="M2 9a3 3 0 013-3h14a3 3 0 013 3v6a3 3 0 01-3 3H5a3 3 0 01-3-3V9z"/>
                  <path v-if="menu.icon === 'ticket'" d="M13 5v2M13 17v2"/>
                  <path v-if="menu.icon === 'refresh'" d="M23 4v6h-6M1 20v-6h6"/>
                  <path v-if="menu.icon === 'refresh'" d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>
                  <path v-if="menu.icon === 'message'" d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline v-if="menu.icon === 'message'" points="22,6 12,13 2,6"/>
                </svg>
              </div>
              <div class="menu-content">
                <span class="menu-label">{{ menu.label }}</span>
                <span class="menu-desc">{{ menu.desc }}</span>
              </div>
              <svg class="menu-arrow" viewBox="0 0 24 24" fill="none">
                <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </nav>

          <button class="logout-btn" @click="handleLogout">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M16 17L21 12M16 7L21 12M16 17L8 17M8 17C6.89543 17 6 17.8954 6 19V21C6 22.1046 6.89543 23 8 23H16C17.1046 23 18 22.1046 18 21V19C18 17.8954 17.1046 17 16 17Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M15 7H4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Logout</span>
          </button>
        </aside>

        <!-- Main Content Area -->
        <main class="content-area">
          <!-- Profile Section -->
          <div v-if="activeMenu === 'profile'" class="content-section">
            <h2 class="section-title">Profile Information</h2>
            <div class="profile-form">
              <div class="form-row">
                <div class="form-group">
                  <label>Avatar URL</label>
                  <el-input v-model="profileForm.avatar" placeholder="Enter avatar URL" />
                </div>
                <div class="form-group">
                  <label>Nickname</label>
                  <el-input v-model="profileForm.nickname" placeholder="Enter your nickname" />
                </div>
              </div>
              <div class="form-actions">
                <button class="btn btn-primary" :disabled="savingProfile" @click="handleSaveProfile">
                  <span v-if="savingProfile">Saving...</span>
                  <span v-else>Save Changes</span>
                </button>
              </div>
            </div>

            <div class="info-section">
              <h3>Account Details</h3>
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">Phone</span>
                  <span class="info-value">{{ maskPhone(user?.phone) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Member Since</span>
                  <span class="info-value">{{ formatDate(user?.date_joined) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Points</span>
                  <span class="info-value points-highlight">{{ user?.points || 0 }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Security Section -->
          <div v-else-if="activeMenu === 'security'" class="content-section">
            <h2 class="section-title">Security Settings</h2>
            <div class="security-options">
              <div class="security-option">
                <h3>Change Password</h3>
                <p>Update your password to keep your account secure</p>
                <div class="password-form">
                  <el-form ref="passwordFormRef" :model="passwordForm" label-width="100px">
                    <el-form-item label="当前密码">
                      <el-input v-model="passwordForm.old_password" type="password" show-password placeholder="请输入当前密码" />
                    </el-form-item>
                    <el-form-item label="新密码">
                      <el-input v-model="passwordForm.new_password" type="password" show-password placeholder="请输入新密码（至少6位）" />
                    </el-form-item>
                    <el-form-item label="确认密码">
                      <el-input v-model="passwordForm.confirm_password" type="password" show-password placeholder="请再次输入新密码" />
                    </el-form-item>
                  </el-form>
                </div>
                <button class="btn btn-secondary" :disabled="changingPassword" @click="handleChangePassword">
                  <span v-if="changingPassword">处理中...</span>
                  <span v-else>Change Password</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Addresses Section -->
          <div v-else-if="activeMenu === 'addresses'" class="content-section">
            <div class="section-header">
              <h2 class="section-title">Shipping Addresses</h2>
              <button class="btn btn-primary" @click="showAddAddressDialog">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Add Address</span>
              </button>
            </div>
            <div v-loading="addressLoading" class="addresses-list">
              <div v-if="addressList.length === 0" class="empty-state">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M3 3h18v18H3zM9 9h6M9 12h6M9 15h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <p>No addresses found. Add your first shipping address.</p>
              </div>
              <div v-for="address in addressList" :key="address.id" class="address-card" :class="{ default: address.is_default }">
                <div class="address-header">
                  <span class="address-name">{{ address.recipient_name }}</span>
                  <span class="address-phone">{{ address.recipient_phone }}</span>
                  <el-tag v-if="address.is_default" type="warning" size="small">默认</el-tag>
                </div>
                <div class="address-body">
                  <p>{{ address.province }} {{ address.city }} {{ address.district }}</p>
                  <p>{{ address.detailed_address }}</p>
                </div>
                <div class="address-actions">
                  <button v-if="!address.is_default" class="action-btn" @click="handleSetDefaultAddress(address.id)">设为默认</button>
                  <button class="action-btn" @click="showEditAddressDialog(address)">编辑</button>
                  <button class="action-btn danger" @click="handleDeleteAddress(address.id)">删除</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Points Section -->
          <div v-else-if="activeMenu === 'points'" class="content-section">
            <h2 class="section-title">My Points</h2>
            <div class="points-summary">
              <div class="points-card">
                <div class="points-value-large">{{ user?.points || 0 }}</div>
                <div class="points-label-large">当前积分</div>
              </div>
            </div>
            <h3 class="subsection-title">积分明细</h3>
            <div v-loading="pointsLoading" class="points-history">
              <div v-if="pointsHistory.length === 0" class="empty-state">
                <p>暂无积分记录</p>
              </div>
              <div v-for="item in pointsHistory" :key="item.id" class="point-item">
                <div class="point-info">
                  <div class="point-desc">{{ item.description }}</div>
                  <div class="point-time">{{ formatDate(item.created_at) }}</div>
                </div>
                <div :class="['point-amount', { earn: item.amount > 0, spend: item.amount < 0 }]">
                  {{ item.amount > 0 ? '+' : '' }}{{ item.amount }}
                </div>
              </div>
            </div>
          </div>

          <!-- Coupons Section -->
          <div v-else-if="activeMenu === 'coupons'" class="content-section">
            <h2 class="section-title">My Coupons</h2>
            <el-tabs v-model="activeCouponTab" @tab-change="handleCouponTabChange">
              <el-tab-pane label="可用" name="available">
                <div v-loading="couponLoading" class="coupons-grid">
                  <div v-if="couponList.length === 0" class="empty-state">
                    <p>暂无可用优惠券</p>
                  </div>
                  <div v-for="coupon in couponList" :key="coupon.id" class="coupon-card available">
                    <div class="coupon-left">
                      <div class="coupon-amount">
                        <span v-if="coupon.coupon?.discount_type === 'full_reduction'">
                          ¥{{ coupon.coupon?.discount_amount }}
                        </span>
                        <span v-else>{{ coupon.coupon?.discount_percent }}折</span>
                      </div>
                      <div class="coupon-condition">满{{ coupon.coupon?.min_purchase_amount }}元可用</div>
                    </div>
                    <div class="coupon-right">
                      <div class="coupon-name">{{ coupon.coupon?.name }}</div>
                      <div class="coupon-time">{{ formatDate(coupon.coupon?.end_time) }} 前有效</div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="已使用" name="used">
                <div v-loading="couponLoading" class="coupons-grid">
                  <div v-if="couponList.length === 0" class="empty-state">
                    <p>暂无已使用优惠券</p>
                  </div>
                  <div v-for="coupon in couponList" :key="coupon.id" class="coupon-card used">
                    <div class="coupon-left">
                      <div class="coupon-amount">
                        <span v-if="coupon.coupon?.discount_type === 'full_reduction'">
                          ¥{{ coupon.coupon?.discount_amount }}
                        </span>
                        <span v-else>{{ coupon.coupon?.discount_percent }}折</span>
                      </div>
                      <div class="coupon-condition">满{{ coupon.coupon?.min_purchase_amount }}元可用</div>
                    </div>
                    <div class="coupon-right">
                      <div class="coupon-name">{{ coupon.coupon?.name }}</div>
                      <div class="coupon-status">已使用</div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="已过期" name="expired">
                <div v-loading="couponLoading" class="coupons-grid">
                  <div v-if="couponList.length === 0" class="empty-state">
                    <p>暂无过期优惠券</p>
                  </div>
                  <div v-for="coupon in couponList" :key="coupon.id" class="coupon-card expired">
                    <div class="coupon-left">
                      <div class="coupon-amount">
                        <span v-if="coupon.coupon?.discount_type === 'full_reduction'">
                          ¥{{ coupon.coupon?.discount_amount }}
                        </span>
                        <span v-else>{{ coupon.coupon?.discount_percent }}折</span>
                      </div>
                      <div class="coupon-condition">满{{ coupon.coupon?.min_purchase_amount }}元可用</div>
                    </div>
                    <div class="coupon-right">
                      <div class="coupon-name">{{ coupon.coupon?.name }}</div>
                      <div class="coupon-status">已过期</div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>

          <!-- Reviews Section -->
          <div v-else-if="activeMenu === 'reviews'" class="content-section">
            <h2 class="section-title">My Reviews</h2>
            <div v-loading="reviewLoading" class="reviews-list">
              <div v-if="reviewList.length === 0" class="empty-state">
                <p>You haven't written any reviews yet.</p>
              </div>
              <div v-for="review in reviewList" :key="review.id" class="review-card">
                <div class="review-header">
                  <div class="review-product">
                    <img :src="review.product?.image || '/placeholder.png'" class="product-thumb" />
                    <div class="product-info">
                      <div class="product-name">{{ review.product?.name }}</div>
                      <el-rate v-model="review.rating" disabled size="small" />
                    </div>
                  </div>
                  <div class="review-date">{{ formatDate(review.created_at) }}</div>
                </div>
                <div class="review-comment">{{ review.comment }}</div>
                <div v-if="review.images && review.images.length" class="review-images">
                  <img v-for="(img, idx) in review.images" :key="idx" :src="img" class="review-image" />
                </div>
                <div class="review-actions">
                  <button class="action-btn danger" @click="handleDeleteReview(review.id)">删除评价</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Returns Section -->
          <div v-else-if="activeMenu === 'returns'" class="content-section">
            <h2 class="section-title">After-sales / Returns</h2>
            <div v-loading="returnLoading" class="returns-list">
              <div v-if="returnList.length === 0" class="empty-state">
                <p>暂无售后申请记录</p>
              </div>
              <div v-for="ret in returnList" :key="ret.id" class="return-card" @click="showReturnDetail(ret)">
                <div class="return-header">
                  <span class="return-order">订单号：{{ ret.order_no }}</span>
                  <el-tag :type="getReturnStatusType(ret.status)" size="small">
                    {{ getReturnStatusText(ret.status) }}
                  </el-tag>
                </div>
                <div class="return-body">
                  <div class="return-type">{{ ret.return_type === 'return' ? '退货' : '换货' }}</div>
                  <div class="return-reason">{{ ret.reason }}</div>
                  <div class="return-time">{{ formatDate(ret.created_at) }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Messages Section -->
          <div v-else-if="activeMenu === 'messages'" class="content-section">
            <h2 class="section-title">Messages</h2>
            <div v-loading="messageLoading" class="messages-list">
              <div v-if="messageList.length === 0" class="empty-state">
                <p>No messages yet.</p>
              </div>
              <div
                v-for="msg in messageList"
                :key="msg.id"
                class="message-card"
                :class="{ unread: !msg.is_read }"
                @click="showMessageDetail(msg)"
              >
                <div class="message-header">
                  <span class="message-title">{{ msg.title }}</span>
                  <span class="message-time">{{ formatDate(msg.created_at) }}</span>
                </div>
                <div class="message-preview">{{ msg.content?.substring(0, 50) }}...</div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- Address Dialog -->
    <el-dialog
      v-model="addressDialogVisible"
      :title="editingAddress ? '编辑地址' : '新增地址'"
      width="500px"
    >
      <el-form ref="addressFormRef" :model="addressForm" label-width="100px">
        <el-form-item label="收货人" required>
          <el-input v-model="addressForm.recipient_name" placeholder="请输入收货人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" required>
          <el-input v-model="addressForm.recipient_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="省份" required>
          <el-input v-model="addressForm.province" placeholder="请输入省份" />
        </el-form-item>
        <el-form-item label="城市" required>
          <el-input v-model="addressForm.city" placeholder="请输入城市" />
        </el-form-item>
        <el-form-item label="区/县" required>
          <el-input v-model="addressForm.district" placeholder="请输入区/县" />
        </el-form-item>
        <el-form-item label="详细地址" required>
          <el-input v-model="addressForm.detailed_address" type="textarea" :rows="2" placeholder="请输入详细地址" />
        </el-form-item>
        <el-form-item label="设为默认">
          <el-switch v-model="addressForm.is_default" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addressDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveAddress">保存</el-button>
      </template>
    </el-dialog>

    <!-- Return Detail Dialog -->
    <el-dialog v-model="returnDetailVisible" title="售后详情" width="600px">
      <div v-if="currentReturn" class="return-detail">
        <div class="detail-item">
          <span class="label">订单号：</span>
          <span>{{ currentReturn.order_no }}</span>
        </div>
        <div class="detail-item">
          <span class="label">申请类型：</span>
          <span>{{ currentReturn.return_type === 'return' ? '退货' : '换货' }}</span>
        </div>
        <div class="detail-item">
          <span class="label">申请原因：</span>
          <span>{{ currentReturn.reason }}</span>
        </div>
        <div class="detail-item">
          <span class="label">详细说明：</span>
          <p>{{ currentReturn.description }}</p>
        </div>
        <div class="detail-item">
          <span class="label">当前状态：</span>
          <el-tag :type="getReturnStatusType(currentReturn.status)">
            {{ getReturnStatusText(currentReturn.status) }}
          </el-tag>
        </div>
        <div v-if="currentReturn.admin_remark" class="detail-item">
          <span class="label">处理意见：</span>
          <p>{{ currentReturn.admin_remark }}</p>
        </div>
        <div class="timeline-section">
          <h4>处理进度</h4>
          <el-timeline>
            <el-timeline-item timestamp="申请提交" :type="currentReturn.status !== 'rejected' ? 'primary' : 'danger'">
              {{ formatDate(currentReturn.created_at) }}
            </el-timeline-item>
            <el-timeline-item v-if="currentReturn.status !== 'pending'" timestamp="审核完成" :type="currentReturn.status === 'rejected' ? 'danger' : 'success'">
              {{ formatDate(currentReturn.processed_at) }}
            </el-timeline-item>
            <el-timeline-item v-if="currentReturn.status === 'completed'" timestamp="处理完成" type="success">
              {{ formatDate(currentReturn.completed_at) }}
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </el-dialog>

    <!-- Message Detail Dialog -->
    <el-dialog v-model="messageDetailVisible" :title="currentMessage?.title" width="600px">
      <div v-if="currentMessage" class="message-detail">
        <div class="message-meta">
          <span class="message-type">{{ currentMessage.message_type === 'announcement' ? '系统公告' : '通知' }}</span>
          <span class="message-time">{{ formatDate(currentMessage.created_at) }}</span>
        </div>
        <div class="message-content-full">{{ currentMessage.content }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.user-center-view {
  --font-display: 'Oswald', sans-serif;
  --font-body: 'DM Sans', sans-serif;
  --primary-color: #ff4d00;
  --primary-hover: #e64600;
  --bg-dark: #0a0a0a;
  --bg-gray: #f5f5f5;
  --text-primary: #0a0a0a;
  --text-secondary: #6b7280;
  --border-color: #e5e7eb;
  min-height: 100vh;
  background: var(--bg-gray);
}

.page-header {
  position: relative;
  background: var(--bg-dark);
  padding: 80px 40px 60px;
  overflow: hidden;
}

.header-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 50% at 50% 100%, rgba(255, 77, 0, 0.2), transparent);
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

.content-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
}

/* Sidebar */
.sidebar {
  position: sticky;
  top: 40px;
  height: fit-content;
}

.user-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  margin-bottom: 16px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
  color: white;
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 700;
  margin: 0 auto 16px;
  line-height: 80px;
}

.user-name {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.user-phone {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-secondary);
}

.user-points {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.points-value {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
}

.points-label {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
}

/* Menu */
.user-menu {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--border-color);
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover {
  background: #f9fafb;
}

.menu-item.active {
  background: rgba(255, 77, 0, 0.1);
}

.menu-icon {
  width: 20px;
  height: 20px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.menu-item.active .menu-icon {
  color: var(--primary-color);
}

.menu-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.menu-label {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.menu-desc {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-secondary);
}

.menu-arrow {
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

.menu-item.active .menu-arrow {
  color: var(--primary-color);
  transform: rotate(-90deg);
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: #fee2e2;
  border-color: #ef4444;
  color: #ef4444;
}

.logout-btn svg {
  width: 16px;
  height: 16px;
}

/* Content Area */
.content-area {
  background: white;
  border-radius: 8px;
  padding: 32px;
  min-height: 500px;
}

.content-section {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.subsection-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 24px 0 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.btn-secondary:hover {
  background: var(--primary-color);
  color: white;
}

/* Profile Form */
.profile-form {
  margin-bottom: 32px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
}

.form-actions {
  display: flex;
  gap: 12px;
}

/* Info Section */
.info-section {
  padding: 24px;
  background: #f9fafb;
  border-radius: 8px;
}

.info-section h3 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.info-value {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-primary);
}

.info-value.points-highlight {
  color: var(--primary-color);
  font-size: 18px;
  font-weight: 600;
}

/* Security Options */
.security-options {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.security-option {
  padding: 24px;
  background: #f9fafb;
  border-radius: 8px;
}

.security-option h3 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.security-option p {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.password-form {
  margin-bottom: 16px;
}

/* Address List */
.addresses-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.address-card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px;
  transition: all 0.2s ease;
}

.address-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.address-card.default {
  border-color: var(--primary-color);
  background: rgba(255, 77, 0, 0.02);
}

.address-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.address-name {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.address-phone {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-secondary);
}

.address-body {
  margin-bottom: 12px;
}

.address-body p {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-primary);
  margin: 4px 0;
}

.address-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #f9fafb;
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.action-btn.danger:hover {
  background: #fee2e2;
  border-color: #ef4444;
  color: #ef4444;
}

/* Points */
.points-summary {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.points-card {
  text-align: center;
  padding: 32px 48px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
  border-radius: 12px;
  color: white;
}

.points-value-large {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
}

.points-label-large {
  font-family: var(--font-body);
  font-size: 14px;
  text-transform: uppercase;
  margin-top: 8px;
  opacity: 0.9;
}

.points-history {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.point-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.point-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.point-desc {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.point-time {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-secondary);
}

.point-amount {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
}

.point-amount.earn {
  color: #10b981;
}

.point-amount.spend {
  color: #ef4444;
}

/* Coupons */
.coupons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.coupon-card {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.coupon-card.available {
  border-color: var(--primary-color);
}

.coupon-card.used,
.coupon-card.expired {
  opacity: 0.6;
}

.coupon-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
  color: white;
  min-width: 100px;
}

.coupon-amount {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
}

.coupon-condition {
  font-family: var(--font-body);
  font-size: 12px;
  opacity: 0.9;
}

.coupon-right {
  flex: 1;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
}

.coupon-name {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.coupon-time,
.coupon-status {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-secondary);
}

/* Reviews */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.review-product {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-thumb {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.review-date {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-secondary);
}

.review-comment {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.review-images {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.review-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
}

.review-actions {
  display: flex;
  gap: 8px;
}

/* Returns */
.returns-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.return-card {
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.return-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.return-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.return-order {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.return-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.return-type {
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-color);
}

.return-reason {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-primary);
}

.return-time {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-secondary);
}

.return-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item .label {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.detail-item span,
.detail-item p {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--text-primary);
}

.timeline-section {
  margin-top: 16px;
}

.timeline-section h4 {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

/* Messages */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-card {
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.message-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-card.unread {
  background: rgba(255, 77, 0, 0.05);
  border-color: var(--primary-color);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.message-title {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.message-time {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--text-secondary);
}

.message-preview {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--text-secondary);
}

.message-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.message-type {
  font-family: var(--font-body);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  background: #f3f4f6;
  border-radius: 4px;
  color: var(--text-secondary);
}

.message-content-full {
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-primary);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}

.empty-state svg {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  opacity: 0.5;
}

.empty-state p {
  font-family: var(--font-body);
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>
