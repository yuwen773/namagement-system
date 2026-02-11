<template>
  <div class="notifications-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-decoration"></div>
      <div class="header-content">
        <div class="header-icon-wrapper">
          <svg class="header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-9 9-9s9-2-9-9a6 6 0 0 0-6-8"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            <path d="M12 2v4"/>
          </svg>
        </div>
        <h1 class="page-title">消息中心</h1>
        <p class="page-subtitle">
          <span v-if="unreadCount > 0">有 <span class="unread-badge">{{ unreadCount }}</span> 条未读消息</span>
          <span v-else>暂无新消息</span>
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Empty State -->
      <div v-if="notifications.length === 0 && !loading" class="empty-state">
        <div class="empty-illustration">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-9 9-9s9-2 9-9a6 6 0 0 0-6-8"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            <line x1="12" y1="2" x2="12.01" y2="2"/>
          </svg>
        </div>
        <h2>还没有任何消息</h2>
        <p>系统通知和动态消息将显示在这里</p>
      </div>

      <!-- Notifications List -->
      <div v-else class="notifications-list">
        <div
          v-for="(item, index) in notifications"
          :key="item.id"
          :class="['notification-card', { unread: !item.isRead, reading: item.reading }]"
          :style="{ animationDelay: `${index * 0.08}s` }"
          @click="markAsRead(item)"
        >
          <div class="notification-icon">
            <svg v-if="item.type === 'SYSTEM'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-9 9-9s9-2 9-9a6 6 0 0 0-6-8"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            <svg v-else-if="item.type === 'ANNOUNCEMENT'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 8.4V16.4"/>
              <path d="M15.5 12a3.5 3.5 0 0 0-7 0"/>
              <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              <path d="M9 10h.01M15 10h.01"/>
            </svg>
          </div>

          <div class="notification-content">
            <div class="notification-header">
              <h3 class="notification-title">{{ item.title }}</h3>
              <div class="notification-meta">
                <span class="notification-type">{{ getTypeLabel(item.type) }}</span>
                <span class="notification-time">{{ formatDate(item.createdAt) }}</span>
              </div>
            </div>
            <p class="notification-text">{{ item.content }}</p>
          </div>

          <div class="notification-status">
            <div v-if="!item.isRead" class="unread-dot"></div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>正在加载消息...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import request from '@/api/request'
import { ElMessage } from 'element-plus'

const notifications = ref([])
const loading = ref(true)

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.isRead).length
})

const typeMap = {
  'SYSTEM': '系统通知',
  'ANNOUNCEMENT': '系统公告',
  'COMMENT': '评论互动'
}

function getTypeLabel(type) {
  return typeMap[type] || '通知'
}

function formatDate(date) {
  const d = new Date(date)
  const now = new Date()
  const diff = now - d
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60))
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60))
      return minutes < 1 ? '刚刚' : `${minutes}分钟前`
    }
    return `${hours}小时前`
  }
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}月前`
  return d.toLocaleDateString('zh-CN')
}

async function fetchNotifications() {
  loading.value = true
  try {
    const res = await request.get('/notifications/')
    notifications.value = (res.data || []).map(item => ({ ...item, reading: false }))
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

async function markAsRead(item) {
  if (item.isRead) return

  try {
    item.reading = true
    await request.post(`/notifications/${item.id}/mark_read/`)
    item.isRead = true
    item.reading = false
  } catch (error) {
    item.reading = false
    ElMessage.error('操作失败')
  }
}

onMounted(fetchNotifications)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.notifications-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  padding-bottom: 60px;
}

/* Header Section */
.page-header {
  position: relative;
  padding: 60px 20px 40px;
  text-align: center;
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 300px;
  background: radial-gradient(ellipse at center, rgba(30, 58, 95, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.header-content {
  position: relative;
  z-index: 2;
  animation: fadeInUp 0.6s ease;
}

.header-icon-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.3);
  position: relative;
}

.header-icon-wrapper::after {
  content: '';
  position: absolute;
  top: -4px;
  right: -4px;
  width: 16px;
  height: 16px;
  background: #ef4444;
  border: 3px solid #f8fafc;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.header-icon {
  width: 40px;
  height: 40px;
  color: white;
}

.page-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e3a5f;
  margin-bottom: 12px;
}

.page-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.1rem;
  color: #64748b;
}

.unread-badge {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.9rem;
  margin: 0 4px;
}

/* Content Wrapper */
.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  animation: fadeIn 0.6s ease;
}

.empty-illustration {
  width: 140px;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(30, 58, 95, 0.05) 100%);
  border-radius: 50%;
  margin-bottom: 32px;
}

.empty-illustration svg {
  width: 70px;
  height: 70px;
  color: #cbd5e1;
}

.empty-state h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1e3a5f;
  margin-bottom: 12px;
}

.empty-state p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
  font-size: 1rem;
}

/* Notifications List */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  animation: fadeInUp 0.6s ease;
}

.notification-card {
  display: flex;
  gap: 20px;
  padding: 24px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 16px rgba(30, 58, 95, 0.08);
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  animation: fadeInUp 0.5s ease both;
}

.notification-card:hover {
  box-shadow: 0 8px 24px rgba(30, 58, 95, 0.12);
  transform: translateY(-2px);
}

.notification-card.unread {
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.03) 0%, rgba(30, 58, 95, 0.01) 100%);
  border-color: rgba(30, 58, 95, 0.1);
}

.notification-card.unread::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 60%;
  background: linear-gradient(180deg, #1e3a5f 0%, #f59e0b 100%);
  border-radius: 0 4px 4px 0;
}

.notification-card.reading {
  opacity: 0.7;
  transform: scale(0.98);
}

.notification-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(30, 58, 95, 0.08) 0%, rgba(245, 158, 11, 0.08) 100%);
  border-radius: 16px;
  flex-shrink: 0;
  color: #1e3a5f;
}

.notification-icon svg {
  width: 24px;
  height: 24px;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 16px;
}

.notification-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1e3a5f;
  margin: 0;
}

.notification-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  flex-shrink: 0;
}

.notification-type {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.notification-time {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: #94a3b8;
}

.notification-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #64748b;
  margin: 0;
}

.notification-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.unread-dot {
  width: 10px;
  height: 10px;
  background: linear-gradient(135deg, #1e3a5f 0%, #f59e0b 100%);
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(30, 58, 95, 0.2);
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #f59e0b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  font-family: 'DM Sans', sans-serif;
  color: #64748b;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .notification-card {
    padding: 20px;
  }

  .notification-icon {
    width: 48px;
    height: 48px;
  }

  .notification-icon svg {
    width: 20px;
    height: 20px;
  }

  .notification-header {
    flex-direction: column;
    gap: 8px;
  }

  .notification-meta {
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 40px 20px 24px;
  }

  .page-title {
    font-size: 2rem;
  }

  .header-icon-wrapper {
    width: 64px;
    height: 64px;
  }

  .header-icon {
    width: 32px;
    height: 32px;
  }

  .notification-card {
    padding: 16px;
    gap: 16px;
  }

  .notification-icon {
    width: 44px;
    height: 44px;
  }

  .notification-icon svg {
    width: 18px;
    height: 18px;
  }

  .notification-title {
    font-size: 1rem;
  }
}
</style>
