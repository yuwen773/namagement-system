<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { maskPhone } from '@/utils'
import { ElMessage } from 'element-plus'
import '@fontsource/oswald'
import '@fontsource/dm-sans'

const router = useRouter()
const authStore = useAuthStore()

const activeMenu = ref('profile')
const userMenu = [
  { id: 'profile', icon: 'user', label: 'Profile', desc: 'Manage your account information' },
  { id: 'security', icon: 'security', label: 'Security', desc: 'Password and authentication settings' },
  { id: 'addresses', icon: 'location', label: 'Addresses', desc: 'Manage your shipping addresses' },
  { id: 'orders', icon: 'shopping-cart', label: 'My Orders', desc: 'View order history and status' },
  { id: 'reviews', icon: 'star', label: 'My Reviews', desc: 'Manage your product reviews' },
  { id: 'coupons', icon: 'ticket', label: 'My Coupons', desc: 'View available coupons' },
  { id: 'messages', icon: 'message', label: 'Messages', desc: 'System notifications' }
]

const loading = ref(false)
const savingProfile = ref(false)

const profileForm = ref({
  nickname: '',
  avatar: ''
})

const user = computed(() => authStore.user)

onMounted(() => {
  if (user.value) {
    profileForm.value = {
      nickname: user.value.nickname || '',
      avatar: user.value.avatar || ''
    }
  }
})

async function handleLogout() {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}

async function handleSaveProfile() {
  savingProfile.value = true
  try {
    // TODO: Call update profile API
    authStore.updateUser(profileForm.value)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    savingProfile.value = false
  }
}

function goToMenu(menuId) {
  activeMenu.value = menuId
  if (menuId === 'orders') {
    router.push('/orders')
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
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M20 21V19C20 19.1046 19.5786 19.4142 19.2929C19.0374 19.1694 18.7113 19 18.25 19C17.7887 19 17.2653 18.8263 16.2439C19.5279 15.3051 19.9832 14.1708 20.4142 13C20.7562 12.1493 20.2646 11.361 19.4142 11C18.5638 11 17.7888 11.1694 16.2439C10.6722 15.3051 10.1272 14.1708 9.58579 13C9.04435 12.1493 8.72363 11.361 8.20001 11C7.67636 11.1694 7.26748 11.3051 6.75701 11C6.24653 11.361 5.78473 11.1694 5.34298 11C4.90124 11.1694 4.50003 10.9476 4.20001 11C3.89997 11.1694 3.63402 11.3051 3.34298 11C3.06596 11.1694 2.87597 11.1493 2.74298 11H1ZM1 19C1 20.1046 1.89543 21 3 21H21C22.1046 21 23 20.1046 23 19C23 17.8954 22.1046 17 21 17H3C1.89543 17 1 17.8954 1 19C1 20.1046 1.89543 21 3 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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
                  <span class="info-value">{{ new Date(user?.date_joined || '').toLocaleDateString() }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Addresses Section -->
          <div v-else-if="activeMenu === 'addresses'" class="content-section">
            <div class="section-header">
              <h2 class="section-title">Shipping Addresses</h2>
              <button class="btn btn-primary">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Add Address</span>
              </button>
            </div>
            <div class="addresses-list">
              <p class="empty-text">No addresses found. Add your first shipping address.</p>
            </div>
          </div>

          <!-- Orders Section -->
          <div v-else-if="activeMenu === 'orders'" class="content-section">
            <div class="section-header">
              <h2 class="section-title">My Orders</h2>
              <button class="btn btn-primary" @click="router.push('/orders')">
                <span>View All Orders</span>
              </button>
            </div>
            <div class="recent-orders">
              <p class="empty-text">View all your orders in the Orders section.</p>
            </div>
          </div>

          <!-- Reviews Section -->
          <div v-else-if="activeMenu === 'reviews'" class="content-section">
            <h2 class="section-title">My Reviews</h2>
            <div class="reviews-list">
              <p class="empty-text">You haven't written any reviews yet.</p>
            </div>
          </div>

          <!-- Coupons Section -->
          <div v-else-if="activeMenu === 'coupons'" class="content-section">
            <h2 class="section-title">My Coupons</h2>
            <div class="coupons-list">
              <p class="empty-text">No available coupons.</p>
            </div>
          </div>

          <!-- Messages Section -->
          <div v-else-if="activeMenu === 'messages'" class="content-section">
            <h2 class="section-title">Messages</h2>
            <div class="messages-list">
              <p class="empty-text">No messages yet.</p>
            </div>
          </div>

          <!-- Security Section -->
          <div v-else-if="activeMenu === 'security'" class="content-section">
            <h2 class="section-title">Security Settings</h2>
            <div class="security-options">
              <div class="security-option">
                <h3>Change Password</h3>
                <p>Update your password to keep your account secure</p>
                <button class="btn btn-secondary">Change Password</button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-center-view {
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
  background: linear-gradient(135deg, #ff4d00 0%, #e64600 100%);
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
  color: #0a0a0a;
  margin-bottom: 4px;
}

.user-phone {
  font-family: var(--font-body);
  font-size: 13px;
  color: #9ca3af;
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
  color: #ff4d00;
}

.points-label {
  font-family: var(--font-body);
  font-size: 12px;
  color: #9ca3af;
  text-transform: uppercase;
}

/* Menu */
.user-menu {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
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
  color: #6b7280;
  flex-shrink: 0;
}

.menu-item.active .menu-icon {
  color: #ff4d00;
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
  color: #0a0a0a;
}

.menu-desc {
  font-family: var(--font-body);
  font-size: 12px;
  color: #9ca3af;
}

.menu-arrow {
  width: 16px;
  height: 16px;
  color: #9ca3af;
}

.menu-item.active .menu-arrow {
  color: #ff4d00;
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
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
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
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
  color: #0a0a0a;
  margin-bottom: 24px;
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
}

.btn-primary {
  background: #ff4d00;
  color: white;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-primary:hover {
  background: #e64600;
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

.form-group :deep(.el-input__wrapper) {
  border: 1px solid #e5e7eb;
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
  color: #0a0a0a;
  margin-bottom: 16px;
}

.info-grid {
  display: grid;
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
  color: #6b7280;
  text-transform: uppercase;
}

.info-value {
  font-family: var(--font-body);
  font-size: 14px;
  color: #0a0a0a;
}

/* Empty States */
.empty-text {
  font-family: var(--font-body);
  font-size: 14px;
  color: #9ca3af;
  text-align: center;
  padding: 40px 0;
}

/* Responsive */
@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }

  .user-menu {
    overflow-x: auto;
  }

  .menu-item {
    min-width: 200px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
