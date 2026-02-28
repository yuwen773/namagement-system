<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { announcementApi } from '@/api'
import Pagination from '@/components/common/Pagination.vue'
import {
  Bell, Top, Refresh, Sparkles
} from '@element-plus/icons-vue'

const announcements = ref([])
const loading = ref(false)
const total = ref(0)

const pagination = ref({
  page: 1,
  page_size: 10
})

const pinnedAnnouncements = computed(() => {
  return announcements.value.filter(a => a.is_pinned)
})

const normalAnnouncements = computed(() => {
  return announcements.value.filter(a => !a.is_pinned)
})

const loadAnnouncements = async () => {
  try {
    loading.value = true
    const params = { ...pagination.value }

    const res = await announcementApi.getList(params)
    if (res.code === 0) {
      announcements.value = res.data || []
      total.value = res.total || 0
    }
  } catch (error) {
    ElMessage.error('加载公告失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  pagination.value.page = page
  loadAnnouncements()
}

const handlePageSizeChange = (size) => {
  pagination.value.page_size = size
  pagination.value.page = 1
  loadAnnouncements()
}

const getPriorityConfig = (priority) => {
  const configs = {
    1: {
      color: '#3b82f6',
      bg: 'linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)',
      text: '普通',
      icon: '📢'
    },
    2: {
      color: '#f59e0b',
      bg: 'linear-gradient(135deg, #d97706 0%, #f59e0b 100%)',
      text: '重要',
      icon: '⚠️'
    },
    3: {
      color: '#ef4444',
      bg: 'linear-gradient(135deg, #dc2626 0%, #ef4444 100%)',
      text: '紧急',
      icon: '🔔'
    }
  }
  return configs[priority] || configs[1]
}

const formatTime = (time) => {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getRelativeTime = (time) => {
  if (!time) return ''
  const now = new Date()
  const target = new Date(time)
  const diff = now - target
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor(diff / (1000 * 60))

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  return formatTime(time)
}

onMounted(() => {
  loadAnnouncements()
})
</script>

<template>
  <div class="announcement-center-page">
    <!-- Hero Header -->
    <div class="hero-header">
      <div class="hero-bg">
        <div class="hero-gradient"></div>
        <div class="hero-pattern"></div>
      </div>
      <div class="hero-content">
        <div class="hero-badge">
          <Sparkles :size="16" />
          <span>系统公告</span>
        </div>
        <h1 class="hero-title">公告中心</h1>
        <p class="hero-subtitle">了解最新动态与重要通知</p>
        <button class="refresh-btn" @click="loadAnnouncements">
          <Refresh :size="18" />
          <span>刷新</span>
        </button>
      </div>
    </div>

    <div v-loading="loading" class="content-wrapper">
      <!-- Pinned Announcements -->
      <div v-if="pinnedAnnouncements.length > 0" class="pinned-section">
        <div class="section-header pinned">
          <div class="header-icon">
            <Top :size="20" />
          </div>
          <div>
            <h2>置顶公告</h2>
            <p>重要通知，请务必阅读</p>
          </div>
        </div>
        <div class="announcement-grid pinned">
          <div
            v-for="item in pinnedAnnouncements"
            :key="item.id"
            class="announcement-card pinned-card"
            :style="{ '--priority-color': getPriorityConfig(item.priority).color }"
          >
            <div class="card-decoration"></div>
            <div class="card-header">
              <div class="priority-badge" :style="{ background: getPriorityConfig(item.priority).bg }">
                <span class="priority-icon">{{ getPriorityConfig(item.priority).icon }}</span>
                <span>{{ getPriorityConfig(item.priority).text }}</span>
              </div>
              <div class="pin-indicator">
                <Top :size="16" />
                <span>置顶</span>
              </div>
            </div>
            <h3 class="card-title">{{ item.title }}</h3>
            <p class="card-content">{{ item.content }}</p>
            <div class="card-footer">
              <span class="time-badge">
                {{ getRelativeTime(item.published_at) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Normal Announcements -->
      <div class="normal-section">
        <div class="section-header">
          <div class="header-icon">
            <Bell :size="20" />
          </div>
          <div>
            <h2>全部公告</h2>
            <p>查看历史通知与公告</p>
          </div>
        </div>
        <div v-if="normalAnnouncements.length > 0" class="announcement-list">
          <div
            v-for="(item, index) in normalAnnouncements"
            :key="item.id"
            class="announcement-item"
            :style="{ '--delay': index * 50 + 'ms' }"
          >
            <div class="item-timeline">
              <div class="timeline-dot" :style="{ backgroundColor: getPriorityConfig(item.priority).color }"></div>
              <div v-if="index < normalAnnouncements.length - 1" class="timeline-line"></div>
            </div>
            <div class="item-content">
              <div class="item-header">
                <div class="priority-tag" :style="{ color: getPriorityConfig(item.priority).color }">
                  {{ getPriorityConfig(item.priority).icon }} {{ getPriorityConfig(item.priority).text }}
                </div>
                <span class="item-time">{{ formatTime(item.published_at) }}</span>
              </div>
              <h3 class="item-title">{{ item.title }}</h3>
              <p class="item-text">{{ item.content }}</p>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <div class="empty-illustration">
            <div class="empty-icon">📭</div>
            <p>暂无公告</p>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="total > 0" class="pagination-section">
        <Pagination
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="total"
          @page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.announcement-center-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

/* Hero Header */
.hero-header {
  position: relative;
  padding: 48px 24px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 30% 20%, rgba(255, 107, 53, 0.3) 0%, transparent 50%),
              radial-gradient(circle at 70% 80%, rgba(123, 44, 191, 0.3) 0%, transparent 50%);
}

.hero-pattern {
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.4;
}

.hero-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  color: #fff;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 30px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.hero-title {
  margin: 0 0 12px 0;
  font-size: 42px;
  font-weight: 800;
  letter-spacing: -1px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.hero-subtitle {
  margin: 0 0 28px 0;
  font-size: 18px;
  opacity: 0.9;
  font-weight: 400;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

/* Content Wrapper */
.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

/* Section Headers */
.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.section-header.pinned h2 {
  color: #f59e0b;
}

.header-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.section-header h2 {
  margin: 0 0 4px 0;
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
}

.section-header p {
  margin: 0;
  font-size: 14px;
  color: #64748b;
}

/* Pinned Section */
.pinned-section {
  margin-bottom: 48px;
}

.announcement-grid.pinned {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.pinned-card {
  position: relative;
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.pinned-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  border-color: var(--priority-color);
}

.card-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle at top right, var(--priority-color) 0%, transparent 70%);
  opacity: 0.1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.priority-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 20px;
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.priority-icon {
  font-size: 14px;
}

.pin-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #f59e0b;
  font-size: 12px;
  font-weight: 600;
}

.card-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.4;
}

.card-content {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #64748b;
  line-height: 1.7;
  white-space: pre-wrap;
}

.card-footer {
  padding-top: 12px;
  border-top: 1px solid #e2e8f0;
}

.time-badge {
  font-size: 13px;
  color: #94a3b8;
}

/* Normal Section */
.normal-section {
  margin-bottom: 32px;
}

.announcement-list {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.announcement-item {
  display: flex;
  gap: 20px;
  padding: 20px 0;
  position: relative;
}

.announcement-item:last-child .timeline-line {
  display: none;
}

.item-timeline {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.8);
}

.timeline-line {
  flex: 1;
  width: 2px;
  background: linear-gradient(180deg, #e2e8f0 0%, transparent 100%);
  min-height: 40px;
}

.item-content {
  flex: 1;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.priority-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
}

.item-time {
  font-size: 13px;
  color: #94a3b8;
}

.item-title {
  margin: 0 0 10px 0;
  font-size: 17px;
  font-weight: 700;
  color: #1e293b;
}

.item-text {
  margin: 0;
  font-size: 14px;
  color: #64748b;
  line-height: 1.7;
  white-space: pre-wrap;
}

/* Empty State */
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.empty-illustration {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  font-size: 64px;
  opacity: 0.5;
}

.empty-illustration p {
  margin: 0;
  font-size: 16px;
  color: #94a3b8;
}

/* Pagination */
.pagination-section {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.pagination-section :deep(.el-pagination) {
  justify-content: center;
}

.pagination-section :deep(.el-pager li) {
  background: #f8fafc;
  border-radius: 8px;
  font-weight: 600;
}

.pagination-section :deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.pagination-section :deep(.btn-prev),
.pagination-section :deep(.btn-next) {
  background: #f8fafc;
  border-radius: 8px;
}
</style>
