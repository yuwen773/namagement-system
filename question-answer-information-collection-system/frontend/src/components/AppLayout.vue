<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <span class="logo-text" v-if="!sidebarCollapsed">问答采集</span>
        </div>
        <div class="header-actions">
          <!-- Notice Icon -->
          <button class="notice-btn" @click="openNoticeDialog" title="公告">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 13a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2Z"/>
              <path d="m9 9 2 2 4-4"/>
            </svg>
            <span v-if="noticeCount > 0" class="notice-badge">{{ noticeCount > 9 ? '9+' : noticeCount }}</span>
          </button>
          <button class="collapse-btn" @click="toggleSidebar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline :points="sidebarCollapsed ? '9 18 15 12 9 6' : '15 18 9 12 15 6'"/>
            </svg>
          </button>
        </div>
      </div>

      <nav class="sidebar-nav">
        <ul class="nav-list">
          <li v-for="item in navItems" :key="item.path">
            <router-link
              :to="item.path"
              class="nav-item"
              :class="{ active: isActive(item.path) }"
            >
              <span class="nav-icon" v-html="item.icon"></span>
              <span class="nav-text" v-if="!sidebarCollapsed">{{ item.name }}</span>
              <el-tooltip
                v-if="sidebarCollapsed"
                :content="item.name"
                placement="right"
                effect="dark"
              >
                <span class="nav-icon-only" v-html="item.icon"></span>
              </el-tooltip>
            </router-link>
          </li>
        </ul>
      </nav>

      <div class="sidebar-footer">
        <div class="user-card" v-if="authStore.userInfo">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-info" v-if="!sidebarCollapsed">
            <span class="user-name">{{ authStore.userInfo.username }}</span>
            <span class="user-role">{{ authStore.isAdmin ? '管理员' : '普通用户' }}</span>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout" :title="sidebarCollapsed ? '退出登录' : ''">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          <span v-if="!sidebarCollapsed">退出登录</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Notice Dialog -->
    <el-dialog
      v-model="noticeDialogVisible"
      title="公告列表"
      width="520px"
      class="notice-dialog"
      :close-on-click-modal="true"
    >
      <div class="notice-list" v-loading="noticeLoading" element-loading-text="加载中...">
        <div v-if="noticeList.length === 0" class="empty-notice">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 13a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2Z"/>
            <path d="m9 9 2 2 4-4"/>
          </svg>
          <p>暂无公告</p>
        </div>
        <div
          v-for="notice in noticeList"
          :key="notice.id"
          class="notice-item"
          @click="viewNoticeDetail(notice)"
        >
          <div class="notice-item-header">
            <h4 class="notice-item-title">{{ notice.title }}</h4>
            <span class="notice-item-time">{{ formatDate(notice.created_at) }}</span>
          </div>
          <p class="notice-item-content">{{ getContentPreview(notice.content) }}</p>
        </div>
      </div>
    </el-dialog>

    <!-- Notice Detail Dialog -->
    <el-dialog
      v-model="noticeDetailVisible"
      :title="currentNotice?.title"
      width="600px"
      class="notice-detail-dialog"
    >
      <div class="notice-detail-content" v-if="currentNotice">
        <p>{{ currentNotice.content }}</p>
      </div>
      <div class="notice-detail-footer">
        <span class="notice-detail-time">发布时间：{{ formatDate(currentNotice?.created_at) }}</span>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getNoticeList } from '@/api/notices'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const sidebarCollapsed = ref(false)

// Notice state
const noticeDialogVisible = ref(false)
const noticeDetailVisible = ref(false)
const noticeLoading = ref(false)
const noticeList = ref([])
const noticeCount = ref(0)
const currentNotice = ref(null)

const userInitials = computed(() => {
  const name = authStore.userInfo?.username || ''
  return name.charAt(0).toUpperCase()
})

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const isActive = (path) => {
  return route.path === path
}

const handleLogout = async () => {
  await authStore.logout()
}

// Notice methods
const openNoticeDialog = async () => {
  noticeDialogVisible.value = true
  await fetchNotices()
}

const fetchNotices = async () => {
  noticeLoading.value = true
  try {
    const res = await getNoticeList({ page_size: 20 })
    if (res.code === 0 || res.code === 200) {
      noticeList.value = res.data || []
      noticeCount.value = res.total || 0
    }
  } catch (e) {
    console.error('Failed to fetch notices:', e)
  } finally {
    noticeLoading.value = false
  }
}

const viewNoticeDetail = (notice) => {
  currentNotice.value = notice
  noticeDetailVisible.value = true
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

const getContentPreview = (content) => {
  if (!content) return ''
  return content.length > 80 ? content.substring(0, 80) + '...' : content
}

const navItems = computed(() => {
  const items = [
    {
      path: '/dashboard',
      name: '仪表盘',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>'
    },
    {
      path: '/data',
      name: '数据中心',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>'
    }
  ]

  // 公告管理 - 管理员可见
  if (authStore.userInfo && authStore.userInfo.role === 'admin') {
    items.push({
      path: '/users',
      name: '用户管理',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
    })
    items.push({
      path: '/notices',
      name: '公告管理',
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 13a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2Z"/><path d="m9 9 2 2 4-4"/></svg>'
    })
  }

  items.push({
    path: '/profile',
    name: '个人中心',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
  })

  return items
})
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background: #0d1117;
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #0f172a 0%, #0a0e17 100%);
  border-right: 1px solid rgba(51, 65, 85, 0.4);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
}

.sidebar.collapsed {
  width: 72px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem;
  border-bottom: 1px solid rgba(51, 65, 85, 0.3);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.notice-btn {
  position: relative;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(51, 65, 85, 0.3);
  border: none;
  border-radius: 6px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.notice-btn:hover {
  background: rgba(71, 85, 105, 0.5);
  color: #f1f5f9;
}

.notice-btn svg {
  width: 16px;
  height: 16px;
}

.notice-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background: #ef4444;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 600;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0a500 0%, #f5af19 100%);
  border-radius: 12px;
  flex-shrink: 0;
}

.logo-icon svg {
  width: 24px;
  height: 24px;
  color: #0a0e17;
}

.logo-text {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f1f5f9;
  white-space: nowrap;
}

.collapse-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(51, 65, 85, 0.3);
  border: none;
  border-radius: 6px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.collapse-btn:hover {
  background: rgba(71, 85, 105, 0.5);
  color: #f1f5f9;
}

.collapse-btn svg {
  width: 16px;
  height: 16px;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 1rem 0.75rem;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  color: #94a3b8;
  text-decoration: none;
  transition: all 0.2s ease;
  position: relative;
}

.nav-item:hover {
  background: rgba(240, 165, 0, 0.08);
  color: #f1f5f9;
}

.nav-item.active {
  background: rgba(240, 165, 0, 0.12);
  color: #f0a500;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 24px;
  background: linear-gradient(180deg, #f0a500 0%, #f5af19 100%);
  border-radius: 0 3px 3px 0;
}

.nav-icon {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.nav-text {
  font-size: 0.9rem;
  font-weight: 500;
  white-space: nowrap;
}

.nav-icon-only {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.nav-icon-only :deep(svg) {
  width: 100%;
  height: 100%;
}

/* Footer */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(51, 65, 85, 0.3);
}

.user-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(51, 65, 85, 0.3);
  border-radius: 12px;
  margin-bottom: 0.75rem;
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0a500 0%, #f5af19 100%);
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #0a0e17;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #f1f5f9;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.75rem;
  color: #64748b;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 10px;
  color: #94a3b8;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(255, 107, 107, 0.1);
  border-color: rgba(255, 107, 107, 0.3);
  color: #ff6b6b;
}

.logout-btn svg {
  width: 18px;
  height: 18px;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 240px;
  min-height: 100vh;
  transition: margin-left 0.3s ease;
}

.sidebar.collapsed + .main-content,
.sidebar.collapsed ~ .main-content {
  margin-left: 72px;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 72px;
  }

  .sidebar-header {
    padding: 1rem 0.5rem;
    justify-content: center;
  }

  .collapse-btn {
    display: none;
  }

  .logo-text,
  .user-info,
  .user-card .user-avatar {
    display: none;
  }

  .user-card {
    justify-content: center;
    padding: 0.5rem;
  }

  .nav-text {
    display: none;
  }

  .nav-item {
    justify-content: center;
    padding: 0.75rem;
  }

  .logout-btn span {
    display: none;
  }

  .main-content {
    margin-left: 72px;
  }
}

/* Notice Dialog Styles */
.notice-list {
  max-height: 400px;
  overflow-y: auto;
}

.empty-notice {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: #64748b;
}

.empty-notice svg {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
  color: #cbd5e1;
}

.empty-notice p {
  margin: 0;
  font-size: 0.9rem;
}

.notice-item {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: background 0.2s ease;
}

.notice-item:hover {
  background: rgba(139, 92, 246, 0.05);
}

.notice-item:last-child {
  border-bottom: none;
}

.notice-item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
}

.notice-item-title {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-item-time {
  font-size: 0.75rem;
  color: #94a3b8;
  flex-shrink: 0;
}

.notice-item-content {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Notice Detail Dialog */
.notice-detail-content {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.notice-detail-content p {
  margin: 0;
  color: #334155;
  line-height: 1.8;
  white-space: pre-wrap;
}

.notice-detail-footer {
  display: flex;
  justify-content: flex-end;
}

.notice-detail-time {
  font-size: 0.8rem;
  color: #94a3b8;
}
</style>
