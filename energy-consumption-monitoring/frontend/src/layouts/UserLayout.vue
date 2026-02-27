<template>
  <div class="user-layout">
    <!-- Top Navigation Bar -->
    <header class="top-nav">
      <div class="nav-container">
        <!-- Logo Section -->
        <div class="logo-section">
          <div class="logo-wrapper">
            <div class="logo-icon">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M24 6L8 16V32C8 37.5225 12.4772 42 18 42H30C35.5228 42 40 37.5225 40 32V16L24 6Z" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M18 26L22 30L30 22" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="24" cy="18" r="4" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="logo-text">
              <span class="logo-title">能耗监测</span>
              <span class="logo-subtitle">用户中心</span>
            </div>
          </div>
        </div>

        <!-- Main Navigation -->
        <nav class="main-nav">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ 'nav-item-active': isActiveRoute(item.path) }"
          >
            <span class="nav-icon">
              <component :is="item.icon" />
            </span>
            <span class="nav-label">{{ item.label }}</span>
            <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
          </router-link>
        </nav>

        <!-- Right Actions -->
        <div class="nav-actions">
          <!-- Room Selector -->
          <el-dropdown trigger="click" class="room-selector" @command="switchRoom">
            <button class="room-trigger">
              <el-icon><icon-ep-house /></el-icon>
              <span class="room-label">{{ currentRoomLabel }}</span>
              <el-icon class="dropdown-icon"><icon-ep-arrow-down /></el-icon>
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item
                  v-for="room in boundRooms"
                  :key="room.id"
                  :command="room.id"
                  :class="{ 'is-active': room.id === currentRoomId }"
                >
                  <div class="room-option">
                    <el-icon><icon-ep-house /></el-icon>
                    <div class="room-info">
                      <span class="room-name">{{ room.name }}</span>
                      <span class="room-detail">{{ room.building }} · {{ room.floor }}</span>
                    </div>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item divided command="bind-room">
                  <el-icon><icon-ep-plus /></el-icon>
                  <span>绑定房间</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <!-- Notifications -->
          <el-badge :value="unreadNoticeCount" :hidden="unreadNoticeCount === 0" class="notice-badge">
            <button class="action-btn" @click="showNotices = true">
              <el-icon><icon-ep-bell /></el-icon>
            </button>
          </el-badge>

          <!-- User Menu -->
          <el-dropdown trigger="click" class="user-dropdown" @command="handleUserCommand">
            <button class="user-trigger">
              <div class="user-avatar">
                <img v-if="userAvatar" :src="userAvatar" alt="Avatar" />
                <el-icon v-else><icon-ep-user /></el-icon>
              </div>
              <span class="user-name">{{ displayName }}</span>
              <el-icon class="dropdown-icon"><icon-ep-arrow-down /></el-icon>
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><icon-ep-user /></el-icon>
                  <span>个人中心</span>
                </el-dropdown-item>
                <!-- <el-dropdown-item command="settings">
                  <el-icon><icon-ep-setting /></el-icon>
                  <span>设置</span>
                </el-dropdown-item> -->
                <el-dropdown-item divided command="logout">
                  <el-icon><icon-ep-switch-button /></el-icon>
                  <span>退出登录</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Notices Drawer -->
    <el-drawer v-model="showNotices" title="通知中心" size="400px" class="notices-drawer">
      <div class="notices-content">
        <div v-for="notice in notices" :key="notice.id" class="notice-item" :class="{ 'is-unread': !notice.read }">
          <div class="notice-icon" :class="`type-${notice.type}`">
            <el-icon>
              <icon-ep-warning v-if="notice.type === 'warning'" />
              <icon-ep-success-filled v-else-if="notice.type === 'success'" />
              <icon-ep-info-filled v-else />
            </el-icon>
          </div>
          <div class="notice-body">
            <h4 class="notice-title">{{ notice.title }}</h4>
            <p class="notice-text">{{ notice.content }}</p>
            <span class="notice-time">{{ notice.time }}</span>
          </div>
        </div>
        <el-empty v-if="notices.length === 0" description="暂无通知" />
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getMyProfile, getMyBindRooms } from '@/api/profile'
import { getNotices } from '@/api/system'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// UI State
const showNotices = ref(false)
const currentRoomId = ref(null)
const boundRooms = ref([])
const notices = ref([])

// Navigation items
const navItems = [
  { path: '/user/dashboard', label: '首页', icon: 'icon-ep-house' },
  { path: '/user/usage', label: '用能查询', icon: 'icon-ep-data-line' },
  { path: '/user/comparison', label: '能耗对比', icon: 'icon-ep-trend-charts' },
  { path: '/user/notices', label: '公告', icon: 'icon-ep-bell' },
  { path: '/user/profile', label: '个人中心', icon: 'icon-ep-user' },
]

// Computed properties
const displayName = computed(() => {
  return userStore.userInfo?.real_name || userStore.userInfo?.username || '用户'
})

const userAvatar = computed(() => {
  return userStore.userInfo?.avatar || null
})

const currentRoomLabel = computed(() => {
  if (!currentRoomId.value) return '选择房间'
  const room = boundRooms.value.find(r => r.id === currentRoomId.value)
  return room ? room.name : '选择房间'
})

const unreadNoticeCount = computed(() => {
  return notices.value.filter(n => !n.read).length
})

// Methods
function isActiveRoute(path) {
  return route.path === path || route.path.startsWith(path + '/')
}

async function switchRoom(roomId) {
  if (roomId === 'bind-room') {
    router.push('/user/profile')
    return
  }

  currentRoomId.value = roomId
  const room = boundRooms.value.find(r => r.id === roomId)
  if (room) {
    ElMessage.success(`已切换至: ${room.name}`)
  }
}

async function handleUserCommand(command) {
  switch (command) {
    case 'profile':
      router.push('/user/profile')
      break
    case 'settings':
      ElMessage.info('设置功能开发中')
      break
    case 'logout':
      await handleLogout()
      break
  }
}

async function handleLogout() {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '退出确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // User cancelled
  }
}

// Load user data
async function loadUserData() {
  try {
    const response = await getMyProfile()
    if (response.code === 0 && response.data) {
      // Update user info if needed
    }
  } catch (error) {
    console.error('Failed to load user profile:', error)
  }
}

// Load bound rooms
async function loadBoundRooms() {
  try {
    const response = await getMyBindRooms()
    if (response.code === 0 && response.data) {
      boundRooms.value = response.data.map(room => ({
        id: room.id,
        name: room.room_number || `房间${room.id}`,
        building: room.building_name || '未知建筑',
        floor: room.floor_name || '未知楼层',
      }))

      // Auto select first room
      if (boundRooms.value.length > 0 && !currentRoomId.value) {
        currentRoomId.value = boundRooms.value[0].id
      }
    }
  } catch (error) {
    console.error('Failed to load bound rooms:', error)
    boundRooms.value = []
    ElMessage.error('加载绑定房间失败，请稍后重试')
  }
}

// Load notices
async function loadNotices() {
  try {
    const response = await getNotices({ limit: 10 })
    if (response.code === 0 && response.data) {
      notices.value = response.data.map(notice => ({
        id: notice.id,
        title: notice.title,
        content: notice.content,
        type: notice.priority === 'high' ? 'warning' : notice.priority === 'low' ? 'success' : 'info',
        time: formatTime(notice.publish_time),
        read: notice.is_read || false,
      }))
    }
  } catch (error) {
    console.error('Failed to load notices:', error)
    notices.value = []
    // Don't show error message for notices as it's not critical
  }
}

function formatTime(timeStr) {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60)

  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  return `${Math.floor(diff / 1440)}天前`
}

// Lifecycle
onMounted(() => {
  loadUserData()
  loadBoundRooms()
  loadNotices()
})

// Export current room ID for child components
defineExpose({
  currentRoomId,
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

.user-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(180deg, #fef7f0 0%, #fff 200px);
  font-family: 'Poppins', 'Noto Sans SC', sans-serif;
}

/* ========================================
   TOP NAVIGATION
   ======================================== */
.top-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(249, 115, 22, 0.1);
  box-shadow: 0 4px 30px rgba(249, 115, 22, 0.05);
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 64px;
}

/* Logo Section */
.logo-section {
  flex-shrink: 0;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo-wrapper:hover {
  transform: scale(1.02);
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.logo-icon svg {
  width: 22px;
  height: 22px;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-title {
  font-size: 16px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 10px;
  font-weight: 500;
  color: #f97316;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Main Navigation */
.main-nav {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 24px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  color: #64748b;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
}

.nav-item:hover {
  background: rgba(249, 115, 22, 0.08);
  color: #f97316;
}

.nav-item-active {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(234, 88, 12, 0.1) 100%);
  color: #f97316;
}

.nav-item-active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 3px;
  background: linear-gradient(90deg, #f97316, #ea580c);
  border-radius: 2px;
}

.nav-icon {
  display: flex;
  align-items: center;
  font-size: 18px;
}

.nav-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 600;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Nav Actions */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Room Selector */
.room-selector .room-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 1px solid rgba(249, 115, 22, 0.2);
  border-radius: 12px;
  color: #92400e;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.room-selector .room-trigger:hover {
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.2);
  transform: translateY(-1px);
}

.room-label {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.room-selector:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* Action Button */
.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 18px;
}

.action-btn:hover {
  background: #fef3c7;
  border-color: #fcd34d;
  color: #f97316;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.15);
}

.notice-badge :deep(.el-badge__content) {
  background: #ef4444;
  border: 2px solid #fff;
}

/* User Dropdown */
.user-dropdown .user-trigger {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px 6px 6px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-dropdown .user-trigger:hover {
  background: #fef3c7;
  border-color: #fcd34d;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  border-radius: 10px;
  color: white;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Room Option in Dropdown */
.room-option {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.room-info {
  display: flex;
  flex-direction: column;
}

.room-name {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.room-detail {
  font-size: 12px;
  color: #64748b;
}

/* ========================================
   MAIN CONTENT
   ======================================== */
.main-content {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}

/* Page Transition */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(16px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-16px);
}

/* ========================================
   NOTICES DRAWER
   ======================================== */
.notices-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notice-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notice-item:hover {
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.notice-item.is-unread {
  background: linear-gradient(135deg, #fffbeb 0%, #f9fafb 100%);
  border-color: #fcd34d;
}

.notice-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.notice-icon.type-warning {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.notice-icon.type-success {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.notice-icon.type-info {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.notice-body {
  flex: 1;
  min-width: 0;
}

.notice-title {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.notice-text {
  margin: 0 0 8px;
  font-size: 13px;
  color: #64748b;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notice-time {
  font-size: 12px;
  color: #9ca3af;
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
}

:deep(.el-dropdown-menu__item.is-active) {
  background: rgba(249, 115, 22, 0.1);
  color: #f97316;
}

:deep(.el-dropdown-menu__item .el-icon) {
  font-size: 18px;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1024px) {
  .nav-container {
    padding: 0 16px;
  }

  .main-nav {
    margin: 0 12px;
  }

  .nav-item .nav-label {
    display: none;
  }

  .nav-item {
    padding: 10px;
  }

  .main-content {
    padding: 16px;
  }
}

@media (max-width: 640px) {
  .logo-text {
    display: none;
  }

  .nav-actions {
    gap: 8px;
  }

  .room-label {
    display: none;
  }

  .user-name {
    display: none;
  }

  .nav-container {
    padding: 0 12px;
  }

  .main-content {
    padding: 12px;
  }
}
</style>
