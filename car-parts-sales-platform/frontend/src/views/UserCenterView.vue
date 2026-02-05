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

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 当前激活的菜单项
const activeMenu = ref('profile')

// 用户菜单配置
const userMenu = [
  { id: 'profile', icon: 'user', label: '个人资料', desc: '管理您的账户信息' },
  { id: 'security', icon: 'security', label: '安全设置', desc: '密码与认证设置' },
  { id: 'addresses', icon: 'location', label: '收货地址', desc: '管理配送地址' },
  { id: 'points', icon: 'star', label: '我的积分', desc: '查看积分明细' },
  { id: 'coupons', icon: 'ticket', label: '我的优惠券', desc: '查看可用优惠券' },
  { id: 'reviews', icon: 'review', label: '我的评价', desc: '管理商品评价' },
  { id: 'returns', icon: 'refresh', label: '售后服务', desc: '售后申请记录' },
  { id: 'messages', icon: 'message', label: '消息中心', desc: '系统通知消息' }
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
    const data = await getMyCouponsApi({ status })
    couponList.value = data.results || []
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
    <!-- Hero Header -->
    <div class="hero-header">
      <div class="hero-mesh"></div>
      <div class="hero-grid"></div>
      <div class="hero-content">
        <div class="hero-badge">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>个人中心</span>
        </div>
        <h1 class="hero-title">{{ user?.nickname || '用户' }}</h1>
        <p class="hero-subtitle">管理您的账户信息与偏好设置</p>

        <!-- User Stats -->
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-value">{{ user?.points || 0 }}</span>
            <span class="stat-label">积分</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">{{ maskPhone(user?.phone || '') }}</span>
            <span class="stat-label">手机号</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">{{ formatDate(user?.date_joined) }}</span>
            <span class="stat-label">注册时间</span>
          </div>
        </div>
      </div>

      <!-- Decorative Elements -->
      <div class="hero-circle hero-circle-1"></div>
      <div class="hero-circle hero-circle-2"></div>
    </div>

    <!-- Main Content -->
    <div class="main-container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <!-- User Card -->
        <div class="user-card">
          <div class="user-avatar">
            <img v-if="user?.avatar" :src="user.avatar" :alt="user?.nickname" />
            <svg v-else viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="user-info">
            <div class="user-name">{{ user?.nickname || '用户' }}</div>
            <div class="user-phone">{{ maskPhone(user?.phone || '') }}</div>
          </div>
          <div class="user-points">
            <span class="points-label">积分</span>
            <span class="points-value">{{ user?.points || 0 }}</span>
          </div>
        </div>

        <!-- Navigation Menu -->
        <nav class="nav-menu">
          <div
            v-for="menu in userMenu"
            :key="menu.id"
            :class="['nav-item', { active: activeMenu === menu.id }]"
            @click="goToMenu(menu.id)"
          >
            <div class="nav-icon">
              <svg v-if="menu.icon === 'user'" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else-if="menu.icon === 'security'" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else-if="menu.icon === 'location'" viewBox="0 0 24 24" fill="none">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
              <svg v-else-if="menu.icon === 'star'" viewBox="0 0 24 24" fill="none">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else-if="menu.icon === 'ticket'" viewBox="0 0 24 24" fill="none">
                <path d="M2 9a3 3 0 013-3h14a3 3 0 013 3v6a3 3 0 01-3 3H5a3 3 0 01-3-3V9z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M13 5v2M13 17v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else-if="menu.icon === 'review'" viewBox="0 0 24 24" fill="none">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else-if="menu.icon === 'refresh'" viewBox="0 0 24 24" fill="none">
                <path d="M23 4v6h-6M1 20v-6h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else-if="menu.icon === 'message'" viewBox="0 0 24 24" fill="none">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div class="nav-content">
              <span class="nav-label">{{ menu.label }}</span>
              <span class="nav-desc">{{ menu.desc }}</span>
            </div>
            <svg class="nav-arrow" viewBox="0 0 24 24" fill="none">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </nav>

        <!-- Logout Button -->
        <button class="logout-btn" @click="handleLogout">
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="16 17 21 12 16 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span>退出登录</span>
        </button>
      </aside>

      <!-- Content Area -->
      <main class="content-area">
        <!-- Profile Section -->
        <div v-if="activeMenu === 'profile'" class="content-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">个人资料</h2>
              <p class="section-subtitle">管理您的账户基本信息</p>
            </div>
          </div>

          <div class="content-card">
            <div class="form-section">
              <h3 class="form-section-title">编辑资料</h3>
              <div class="form-grid">
                <div class="form-group">
                  <label class="form-label">头像链接</label>
                  <div class="input-wrapper">
                    <input v-model="profileForm.avatar" type="text" placeholder="输入头像图片URL" class="form-input" />
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">昵称</label>
                  <div class="input-wrapper">
                    <input v-model="profileForm.nickname" type="text" placeholder="输入您的昵称" class="form-input" />
                  </div>
                </div>
              </div>
              <div class="form-actions">
                <button class="btn btn-primary" :disabled="savingProfile" @click="handleSaveProfile">
                  <svg v-if="!savingProfile" viewBox="0 0 24 24" fill="none" width="18" height="18">
                    <polyline points="20 6 9 17 4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span v-if="savingProfile">保存中...</span>
                  <span v-else>保存更改</span>
                </button>
              </div>
            </div>

            <div class="info-section">
              <h3 class="info-section-title">账户详情</h3>
              <div class="info-grid">
                <div class="info-card">
                  <div class="info-card-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                      <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  <div>
                    <div class="info-card-label">手机号</div>
                    <div class="info-card-value">{{ maskPhone(user?.phone) }}</div>
                  </div>
                </div>
                <div class="info-card">
                  <div class="info-card-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                      <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/>
                      <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/>
                      <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                  <div>
                    <div class="info-card-label">注册时间</div>
                    <div class="info-card-value">{{ formatDate(user?.date_joined) }}</div>
                  </div>
                </div>
                <div class="info-card highlight">
                  <div class="info-card-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  <div>
                    <div class="info-card-label">我的积分</div>
                    <div class="info-card-value">{{ user?.points || 0 }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Security Section -->
        <div v-else-if="activeMenu === 'security'" class="content-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">安全设置</h2>
              <p class="section-subtitle">保护您的账户安全</p>
            </div>
          </div>

          <div class="content-card">
            <div class="security-card">
              <div class="security-header">
                <div class="security-icon warning">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div>
                  <h3>修改密码</h3>
                  <p>定期更换密码以保护账户安全</p>
                </div>
              </div>
              <div class="password-form">
                <div class="form-group">
                  <label class="form-label">当前密码</label>
                  <div class="input-wrapper">
                    <input v-model="passwordForm.old_password" type="password" placeholder="输入当前密码" class="form-input" />
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">新密码</label>
                  <div class="input-wrapper">
                    <input v-model="passwordForm.new_password" type="password" placeholder="输入新密码（至少6位）" class="form-input" />
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">确认新密码</label>
                  <div class="input-wrapper">
                    <input v-model="passwordForm.confirm_password" type="password" placeholder="再次输入新密码" class="form-input" />
                  </div>
                </div>
              </div>
              <button class="btn btn-secondary" :disabled="changingPassword" @click="handleChangePassword">
                <span v-if="changingPassword">处理中...</span>
                <span v-else>修改密码</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Addresses Section -->
        <div v-else-if="activeMenu === 'addresses'" class="content-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">收货地址</h2>
              <p class="section-subtitle">管理您的配送地址</p>
            </div>
            <button class="btn btn-primary" @click="showAddAddressDialog">
              <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                <line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>添加地址</span>
            </button>
          </div>

          <div v-loading="addressLoading" class="content-card addresses-grid">
            <div v-if="addressList.length === 0" class="empty-state">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M3 3h18v18H3zM9 9h6M9 12h6M9 15h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <p>暂无收货地址，请添加您的第一个地址</p>
            </div>
            <div
              v-for="address in addressList"
              :key="address.id"
              class="address-card"
              :class="{ default: address.is_default }"
            >
              <div class="address-badge" v-if="address.is_default">默认</div>
              <div class="address-header">
                <span class="address-name">{{ address.recipient_name }}</span>
                <span class="address-phone">{{ address.recipient_phone }}</span>
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
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">我的积分</h2>
              <p class="section-subtitle">查看您的积分历史</p>
            </div>
          </div>

          <div class="content-card">
            <!-- Points Summary -->
            <div class="points-summary">
              <div class="points-circle">
                <svg viewBox="0 0 100 100" class="points-ring">
                  <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(249, 115, 22, 0.2)" stroke-width="8"/>
                  <circle cx="50" cy="50" r="40" fill="none" stroke="#f97316" stroke-width="8" stroke-linecap="round" stroke-dasharray="251.2" stroke-dashoffset="62.8" transform="rotate(-90 50 50)"/>
                </svg>
                <div class="points-center">
                  <span class="points-value-large">{{ user?.points || 0 }}</span>
                  <span class="points-label-large">当前积分</span>
                </div>
              </div>
            </div>

            <!-- Points History -->
            <div class="history-section">
              <h3 class="history-title">积分明细</h3>
              <div v-loading="pointsLoading" class="points-list">
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
          </div>
        </div>

        <!-- Coupons Section -->
        <div v-else-if="activeMenu === 'coupons'" class="content-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M2 9a3 3 0 013-3h14a3 3 0 013 3v6a3 3 0 01-3 3H5a3 3 0 01-3-3V9z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M13 5v2M13 17v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">我的优惠券</h2>
              <p class="section-subtitle">查看可用优惠券</p>
            </div>
          </div>

          <div class="content-card">
            <el-tabs v-model="activeCouponTab" @tab-change="handleCouponTabChange" class="custom-tabs">
              <el-tab-pane label="可用" name="unused">
                <div v-loading="couponLoading" class="coupons-grid">
                  <div v-if="couponList.length === 0" class="empty-state">
                    <p>暂无可用优惠券</p>
                  </div>
                  <div v-for="coupon in couponList" :key="coupon.id" class="coupon-card available">
                    <div class="coupon-left">
                      <div class="coupon-amount">
                        <span v-if="coupon.coupon?.discount_type === 'full_reduction'">¥{{ coupon.coupon?.discount_amount }}</span>
                        <span v-else>{{ Math.round(coupon.coupon?.discount_rate * 10) || 95 }}折</span>
                      </div>
                      <div class="coupon-condition">满{{ coupon.coupon?.min_amount }}元可用</div>
                    </div>
                    <div class="coupon-right">
                      <div class="coupon-name">{{ coupon.coupon?.name }}</div>
                      <div class="coupon-time">{{ formatDate(coupon.coupon?.valid_until) }} 前有效</div>
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
                        <span v-if="coupon.coupon?.discount_type === 'full_reduction'">¥{{ coupon.coupon?.discount_amount }}</span>
                        <span v-else>{{ Math.round(coupon.coupon?.discount_rate * 10) || 95 }}折</span>
                      </div>
                      <div class="coupon-condition">满{{ coupon.coupon?.min_amount }}元可用</div>
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
                        <span v-if="coupon.coupon?.discount_type === 'full_reduction'">¥{{ coupon.coupon?.discount_amount }}</span>
                        <span v-else>{{ Math.round(coupon.coupon?.discount_rate * 10) || 95 }}折</span>
                      </div>
                      <div class="coupon-condition">满{{ coupon.coupon?.min_amount }}元可用</div>
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
        </div>

        <!-- Reviews Section -->
        <div v-else-if="activeMenu === 'reviews'" class="content-section">
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">我的评价</h2>
              <p class="section-subtitle">管理您的商品评价</p>
            </div>
          </div>

          <div v-loading="reviewLoading" class="content-card reviews-list">
            <div v-if="reviewList.length === 0" class="empty-state">
              <p>您还没有发表过评价</p>
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
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M23 4v6h-6M1 20v-6h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">售后服务</h2>
              <p class="section-subtitle">查看您的售后申请</p>
            </div>
          </div>

          <div v-loading="returnLoading" class="content-card returns-list">
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
          <div class="section-header">
            <div class="section-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
            <div>
              <h2 class="section-title">消息中心</h2>
              <p class="section-subtitle">查看系统通知</p>
            </div>
          </div>

          <div v-loading="messageLoading" class="content-card messages-list">
            <div v-if="messageList.length === 0" class="empty-state">
              <p>暂无消息</p>
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

    <!-- Address Dialog -->
    <el-dialog
      v-model="addressDialogVisible"
      :title="editingAddress ? '编辑地址' : '新增地址'"
      width="500px"
      class="custom-dialog"
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
    <el-dialog v-model="returnDetailVisible" title="售后详情" width="600px" class="custom-dialog">
      <div v-if="currentReturn" class="return-detail">
        <div class="detail-item">
          <span class="detail-label">订单号：</span>
          <span>{{ currentReturn.order_no }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">申请类型：</span>
          <span>{{ currentReturn.return_type === 'return' ? '退货' : '换货' }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">申请原因：</span>
          <span>{{ currentReturn.reason }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">详细说明：</span>
          <p>{{ currentReturn.description }}</p>
        </div>
        <div class="detail-item">
          <span class="detail-label">当前状态：</span>
          <el-tag :type="getReturnStatusType(currentReturn.status)">
            {{ getReturnStatusText(currentReturn.status) }}
          </el-tag>
        </div>
        <div v-if="currentReturn.admin_remark" class="detail-item">
          <span class="detail-label">处理意见：</span>
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
    <el-dialog v-model="messageDetailVisible" :title="currentMessage?.title" width="600px" class="custom-dialog">
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

.hero-subtitle {
  font-size: 16px;
  color: #94a3b8;
  margin-bottom: 40px;
}

.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #f97316;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(249, 115, 22, 0.2);
}

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

/* ==================== Main Container ==================== */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 32px;
}

/* ==================== Sidebar ==================== */
.sidebar {
  position: sticky;
  top: 20px;
  height: fit-content;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
  text-align: center;
}

.user-avatar {
  width: 80px;
  height: 80px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar svg {
  width: 40px;
  height: 40px;
  color: #ffffff;
}

.user-name {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 4px;
}

.user-phone {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 16px;
}

.user-points {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.points-label {
  font-size: 12px;
  color: #64748b;
}

.points-value {
  font-size: 20px;
  font-weight: 700;
  color: #f97316;
}

/* Navigation Menu */
.nav-menu {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  padding: 8px;
  backdrop-filter: blur(10px);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: rgba(249, 115, 22, 0.1);
}

.nav-item.active {
  background: rgba(249, 115, 22, 0.15);
}

.nav-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
  flex-shrink: 0;
}

.nav-item:hover .nav-icon,
.nav-item.active .nav-icon {
  color: #f97316;
}

.nav-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-label {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.nav-desc {
  font-size: 11px;
  color: #64748b;
}

.nav-arrow {
  width: 16px;
  height: 16px;
  color: #475569;
  transition: transform 0.2s ease;
}

.nav-item.active .nav-arrow {
  color: #f97316;
  transform: rotate(90deg);
}

/* Logout Button */
.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 16px;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  color: #94a3b8;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #ef4444;
}

.logout-btn svg {
  width: 18px;
  height: 18px;
}

/* ==================== Content Area ==================== */
.content-area {
  min-width: 0;
}

.content-section {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.section-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 12px;
  color: #ffffff;
}

.section-icon svg {
  width: 24px;
  height: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 4px;
}

.section-subtitle {
  font-size: 13px;
  color: #64748b;
}

/* ==================== Content Card ==================== */
.content-card {
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
}

/* ==================== Buttons ==================== */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(249, 115, 22, 0.4);
}

.btn-secondary {
  background: transparent;
  color: #f97316;
  border: 1px solid #f97316;
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(249, 115, 22, 0.1);
}

.btn svg {
  width: 18px;
  height: 18px;
}

/* ==================== Form Elements ==================== */
.form-section {
  margin-bottom: 32px;
}

.form-section-title {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 10px;
  color: #e2e8f0;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
}

.form-input:focus {
  border-color: #f97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.1);
}

.form-input::placeholder {
  color: #475569;
}

.form-actions {
  display: flex;
  gap: 12px;
}

/* ==================== Info Section ==================== */
.info-section {
  margin-top: 24px;
}

.info-section-title {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 12px;
}

.info-card.highlight {
  border-color: rgba(249, 115, 22, 0.3);
  background: rgba(249, 115, 22, 0.05);
}

.info-card-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(71, 85, 105, 0.3);
  border-radius: 10px;
  color: #64748b;
}

.info-card.highlight .info-card-icon {
  background: rgba(249, 115, 22, 0.2);
  color: #f97316;
}

.info-card-icon svg {
  width: 20px;
  height: 20px;
}

.info-card-label {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 2px;
}

.info-card-value {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
}

.info-card.highlight .info-card-value {
  color: #f97316;
}

/* ==================== Security Card ==================== */
.security-card {
  padding: 24px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 12px;
}

.security-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.security-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(249, 115, 22, 0.1);
  border-radius: 12px;
  color: #f97316;
}

.security-icon svg {
  width: 24px;
  height: 24px;
}

.security-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 4px;
}

.security-header p {
  font-size: 13px;
  color: #64748b;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

/* ==================== Addresses ==================== */
.addresses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.address-card {
  position: relative;
  padding: 20px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.address-card:hover {
  border-color: rgba(249, 115, 22, 0.5);
  transform: translateY(-4px);
  box-shadow: 0 12px 30px -10px rgba(249, 115, 22, 0.3);
}

.address-card.default {
  border-color: #f97316;
  background: rgba(249, 115, 22, 0.05);
}

.address-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 10px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  color: #ffffff;
}

.address-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.address-name {
  font-size: 15px;
  font-weight: 600;
  color: #e2e8f0;
}

.address-phone {
  font-size: 13px;
  color: #94a3b8;
}

.address-body {
  margin-bottom: 16px;
}

.address-body p {
  font-size: 13px;
  color: #64748b;
  margin: 4px 0;
}

.address-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  background: transparent;
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 6px;
  color: #94a3b8;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  border-color: #f97316;
  color: #f97316;
}

.action-btn.danger:hover {
  border-color: #ef4444;
  color: #ef4444;
}

/* ==================== Points ==================== */
.points-summary {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.points-circle {
  position: relative;
  width: 200px;
  height: 200px;
}

.points-ring {
  width: 100%;
  height: 100%;
}

.points-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.points-value-large {
  font-size: 48px;
  font-weight: 800;
  color: #f97316;
  line-height: 1;
}

.points-label-large {
  font-size: 14px;
  color: #64748b;
  margin-top: 8px;
}

.history-section {
  margin-top: 32px;
}

.history-title {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 16px;
}

.points-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.point-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 10px;
}

.point-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.point-desc {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.point-time {
  font-size: 12px;
  color: #64748b;
}

.point-amount {
  font-size: 18px;
  font-weight: 700;
}

.point-amount.earn {
  color: #22c55e;
}

.point-amount.spend {
  color: #ef4444;
}

/* ==================== Coupons ==================== */
.custom-tabs {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.custom-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(71, 85, 105, 0.5);
}

.custom-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.custom-tabs :deep(.el-tabs__item) {
  color: #94a3b8;
  font-size: 14px;
  font-weight: 600;
}

.custom-tabs :deep(.el-tabs__item:hover) {
  color: #f97316;
}

.custom-tabs :deep(.el-tabs__item.is-active) {
  color: #f97316;
}

.custom-tabs :deep(.el-tabs__active-bar) {
  background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
  height: 3px;
  border-radius: 3px 3px 0 0;
}

.coupons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.coupon-card {
  display: flex;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(71, 85, 105, 0.5);
  transition: all 0.3s ease;
}

.coupon-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px -10px rgba(249, 115, 22, 0.3);
}

.coupon-card.available {
  border-color: rgba(249, 115, 22, 0.5);
}

.coupon-card.used,
.coupon-card.expired {
  opacity: 0.5;
}

.coupon-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: #ffffff;
  min-width: 100px;
}

.coupon-amount {
  font-size: 24px;
  font-weight: 800;
}

.coupon-condition {
  font-size: 12px;
  opacity: 0.9;
  margin-top: 4px;
}

.coupon-right {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  background: rgba(15, 23, 42, 0.5);
}

.coupon-name {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.coupon-time,
.coupon-status {
  font-size: 12px;
  color: #64748b;
}

/* ==================== Reviews ==================== */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  padding: 20px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 12px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
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
  border-radius: 8px;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.review-date {
  font-size: 12px;
  color: #64748b;
}

.review-comment {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 12px;
  line-height: 1.6;
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
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.review-image:hover {
  transform: scale(1.05);
}

.review-actions {
  display: flex;
  gap: 8px;
}

/* ==================== Returns ==================== */
.returns-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.return-card {
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.return-card:hover {
  border-color: rgba(249, 115, 22, 0.5);
}

.return-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.return-order {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.return-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.return-type {
  font-size: 13px;
  font-weight: 600;
  color: #f97316;
}

.return-reason {
  font-size: 14px;
  color: #94a3b8;
}

.return-time {
  font-size: 12px;
  color: #64748b;
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

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
}

.detail-item span,
.detail-item p {
  font-size: 14px;
  color: #e2e8f0;
}

.timeline-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(71, 85, 105, 0.3);
}

.timeline-section h4 {
  font-size: 14px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 12px;
}

/* ==================== Messages ==================== */
.messages-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-card {
  padding: 16px;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.message-card:hover {
  border-color: rgba(249, 115, 22, 0.5);
}

.message-card.unread {
  background: rgba(249, 115, 22, 0.05);
  border-color: rgba(249, 115, 22, 0.3);
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.message-title {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
}

.message-time {
  font-size: 12px;
  color: #64748b;
}

.message-preview {
  font-size: 13px;
  color: #64748b;
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
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  background: rgba(71, 85, 105, 0.3);
  border-radius: 6px;
  color: #94a3b8;
}

.message-content-full {
  font-size: 14px;
  line-height: 1.6;
  color: #e2e8f0;
}

/* ==================== Empty State ==================== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  opacity: 0.3;
}

.empty-state p {
  font-size: 14px;
}

/* ==================== Dialog ==================== */
.custom-dialog :deep(.el-dialog) {
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 16px;
  backdrop-filter: blur(20px);
}

.custom-dialog :deep(.el-dialog__header) {
  border-bottom: 1px solid rgba(71, 85, 105, 0.3);
  padding: 20px 24px;
}

.custom-dialog :deep(.el-dialog__title) {
  color: #e2e8f0;
  font-size: 18px;
  font-weight: 700;
}

.custom-dialog :deep(.el-dialog__body) {
  padding: 24px;
  color: #94a3b8;
}

.custom-dialog :deep(.el-dialog__footer) {
  border-top: 1px solid rgba(71, 85, 105, 0.3);
  padding: 16px 24px;
}

.custom-dialog :deep(.el-input__wrapper) {
  background: rgba(15, 23, 42, 0.5);
  border-color: rgba(71, 85, 105, 0.5);
}

.custom-dialog :deep(.el-input__wrapper:hover),
.custom-dialog :deep(.el-input__wrapper.is-focus) {
  border-color: #f97316;
}

.custom-dialog :deep(.el-input__inner) {
  color: #e2e8f0;
}

.custom-dialog :deep(.el-form-item__label) {
  color: #94a3b8;
}

/* ==================== Responsive ==================== */
@media (max-width: 1024px) {
  .main-container {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }

  .nav-menu {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 8px;
  }

  .nav-arrow {
    display: none;
  }

  .hero-stats {
    gap: 16px;
  }

  .stat-divider {
    display: none;
  }
}

@media (max-width: 640px) {
  .hero-header {
    padding: 60px 20px 40px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .section-icon {
    width: 40px;
    height: 40px;
  }

  .section-icon svg {
    width: 20px;
    height: 20px;
  }

  .section-title {
    font-size: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .addresses-grid {
    grid-template-columns: 1fr;
  }

  .coupons-grid {
    grid-template-columns: 1fr;
  }
}
</style>
